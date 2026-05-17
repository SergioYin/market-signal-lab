"""CSV data loading helpers."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import IO, Iterable

REQUIRED_COLUMNS = ("date", "open", "high", "low", "close")


@dataclass(frozen=True)
class PriceBar:
    """One daily OHLC price bar."""

    date: date
    open: float
    high: float
    low: float
    close: float


def load_ohlc_csv(source: str | Path | IO[str]) -> list[PriceBar]:
    """Load OHLC price bars from a CSV path or text file object."""

    if isinstance(source, (str, Path)):
        with Path(source).open(newline="") as handle:
            return _load_ohlc_rows(handle)

    return _load_ohlc_rows(source)


def _load_ohlc_rows(rows: Iterable[str]) -> list[PriceBar]:
    reader = csv.DictReader(rows)
    _validate_columns(reader.fieldnames)

    bars: list[PriceBar] = []
    for row_number, row in enumerate(reader, start=2):
        bars.append(_parse_bar(row, row_number))

    return bars


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
