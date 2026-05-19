"""CSV data loading helpers."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import IO, Any, Iterable

REQUIRED_COLUMNS = ("date", "open", "high", "low", "close")


@dataclass(frozen=True)
class PriceBar:
    """One daily OHLC price bar."""

    date: date
    open: float
    high: float
    low: float
    close: float


@dataclass(frozen=True)
class StaticFixtureProvenance:
    """Research-only provenance metadata for a bundled static fixture."""

    dataset_label: str
    data_kind: str
    source: str
    created_date: str
    as_of_date: str
    limitations: tuple[str, ...]
    metadata_path: str
    research_only: bool = True

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable provenance dictionary."""

        return {
            "dataset_label": self.dataset_label,
            "data_kind": self.data_kind,
            "source": self.source,
            "created_date": self.created_date,
            "as_of_date": self.as_of_date,
            "limitations": list(self.limitations),
            "metadata_path": self.metadata_path,
            "research_only": self.research_only,
        }


def load_ohlc_csv(source: str | Path | IO[str]) -> list[PriceBar]:
    """Load OHLC price bars from a CSV path or text file object."""

    if isinstance(source, (str, Path)):
        with Path(source).open(newline="") as handle:
            return _load_ohlc_rows(handle)

    return _load_ohlc_rows(source)


def load_static_fixture_provenance(path: str | Path) -> StaticFixtureProvenance | None:
    """Load adjacent static fixture provenance metadata when it exists."""

    csv_path = Path(path)
    metadata_path = csv_path.with_suffix(csv_path.suffix + ".provenance.json")
    if not metadata_path.exists():
        return None

    try:
        raw = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid fixture provenance metadata {metadata_path}: {exc.msg}"
        ) from exc

    if not isinstance(raw, dict):
        raise ValueError("Fixture provenance metadata must contain a JSON object")

    return _parse_static_fixture_provenance(raw, metadata_path)


def _load_ohlc_rows(rows: Iterable[str]) -> list[PriceBar]:
    reader = csv.DictReader(rows)
    _validate_columns(reader.fieldnames)

    bars: list[PriceBar] = []
    for row_number, row in enumerate(reader, start=2):
        bars.append(_parse_bar(row, row_number))

    return bars


def _parse_static_fixture_provenance(
    raw: dict[str, Any],
    metadata_path: Path,
) -> StaticFixtureProvenance:
    required_strings = (
        "dataset_label",
        "data_kind",
        "source",
        "created_date",
        "as_of_date",
    )
    values: dict[str, str] = {}
    for key in required_strings:
        value = raw.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Fixture provenance metadata field {key!r} must be a non-empty string"
            )
        values[key] = value

    limitations = raw.get("limitations")
    if (
        not isinstance(limitations, list)
        or not limitations
        or not all(isinstance(item, str) and item.strip() for item in limitations)
    ):
        raise ValueError(
            "Fixture provenance metadata field 'limitations' must be a non-empty "
            "list of strings"
        )

    if raw.get("research_only") is not True:
        raise ValueError(
            "Fixture provenance metadata field 'research_only' must be true"
        )

    if values["data_kind"] != "synthetic_static_fixture":
        raise ValueError(
            "Fixture provenance metadata field 'data_kind' must be "
            "'synthetic_static_fixture'"
        )

    return StaticFixtureProvenance(
        dataset_label=values["dataset_label"],
        data_kind=values["data_kind"],
        source=values["source"],
        created_date=values["created_date"],
        as_of_date=values["as_of_date"],
        limitations=tuple(limitations),
        metadata_path=str(metadata_path),
    )


def _validate_columns(fieldnames: list[str] | None) -> None:
    if fieldnames is None:
        raise ValueError("CSV is missing a header row")

    missing = [name for name in REQUIRED_COLUMNS if name not in fieldnames]
    if missing:
        columns = ", ".join(missing)
        raise ValueError(f"CSV is missing required column(s): {columns}")


def _parse_bar(row: dict[str, str], row_number: int) -> PriceBar:
    try:
        bar_date = date.fromisoformat(row["date"])
    except ValueError as exc:
        raise ValueError(f"Invalid date on row {row_number}: {row['date']!r}") from exc

    open_price = _parse_float(row, "open", row_number)
    high_price = _parse_float(row, "high", row_number)
    low_price = _parse_float(row, "low", row_number)
    close_price = _parse_float(row, "close", row_number)

    if high_price < max(open_price, low_price, close_price):
        raise ValueError(f"Invalid OHLC values on row {row_number}: high is too low")
    if low_price > min(open_price, high_price, close_price):
        raise ValueError(f"Invalid OHLC values on row {row_number}: low is too high")

    return PriceBar(
        date=bar_date,
        open=open_price,
        high=high_price,
        low=low_price,
        close=close_price,
    )


def _parse_float(row: dict[str, str], column: str, row_number: int) -> float:
    value = row[column]
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Invalid {column} on row {row_number}: {value!r}") from exc
