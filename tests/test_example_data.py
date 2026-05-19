import csv
import json
from io import StringIO
from pathlib import Path

import pytest

from market_signal_lab.data import (
    REQUIRED_COLUMNS,
    load_ohlc_csv,
    load_static_fixture_provenance,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA_PATH = REPO_ROOT / "examples" / "data" / "sample_tqqq_qld_like.csv"
SAMPLE_PROVENANCE_PATH = SAMPLE_DATA_PATH.with_suffix(
    SAMPLE_DATA_PATH.suffix + ".provenance.json"
)


def test_sample_tqqq_qld_like_data_is_valid_ohlc_by_symbol() -> None:
    with SAMPLE_DATA_PATH.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert rows
    assert set(rows[0]) == {"symbol", *REQUIRED_COLUMNS}
    assert {row["symbol"] for row in rows} == {"QQQ_LIKE", "TQQQ_LIKE", "QLD_LIKE"}

    dates_by_symbol: dict[str, list[str]] = {}
    for row in rows:
        dates_by_symbol.setdefault(row["symbol"], []).append(row["date"])

    assert all(len(dates) == 8 for dates in dates_by_symbol.values())
    assert all(dates == sorted(dates) for dates in dates_by_symbol.values())

    for symbol in dates_by_symbol:
        series_rows = [row for row in rows if row["symbol"] == symbol]
        csv_data = StringIO()
        writer = csv.DictWriter(csv_data, fieldnames=list(REQUIRED_COLUMNS))
        writer.writeheader()
        writer.writerows({column: row[column] for column in REQUIRED_COLUMNS} for row in series_rows)
        csv_data.seek(0)

        bars = load_ohlc_csv(csv_data)

        assert len(bars) == 8


def test_sample_data_has_research_only_static_fixture_provenance() -> None:
    provenance = load_static_fixture_provenance(SAMPLE_DATA_PATH)

    assert provenance is not None
    assert provenance.dataset_label == "sample_tqqq_qld_like"
    assert provenance.data_kind == "synthetic_static_fixture"
    assert provenance.created_date == "2026-05-18"
    assert provenance.as_of_date == "2026-05-18"
    assert provenance.research_only is True
    assert provenance.metadata_path == str(SAMPLE_PROVENANCE_PATH)
    assert "Hand-authored deterministic OHLC sample" in provenance.source
    assert any("not broker" in limitation for limitation in provenance.limitations)
    assert any("do not use for advice" in limitation for limitation in provenance.limitations)


def test_missing_static_fixture_provenance_returns_none(tmp_path: Path) -> None:
    csv_path = tmp_path / "bars.csv"
    csv_path.write_text("date,open,high,low,close\n", encoding="utf-8")

    assert load_static_fixture_provenance(csv_path) is None


def test_static_fixture_provenance_rejects_non_research_metadata(tmp_path: Path) -> None:
    csv_path = tmp_path / "bars.csv"
    csv_path.write_text("date,open,high,low,close\n", encoding="utf-8")
    csv_path.with_suffix(".csv.provenance.json").write_text(
        json.dumps(
            {
                "dataset_label": "bad",
                "data_kind": "synthetic_static_fixture",
                "source": "test",
                "created_date": "2026-05-18",
                "as_of_date": "2026-05-18",
                "limitations": ["test"],
                "research_only": False,
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="'research_only' must be true"):
        load_static_fixture_provenance(csv_path)
