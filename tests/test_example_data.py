import csv
from io import StringIO
from pathlib import Path

from market_signal_lab.data import REQUIRED_COLUMNS, load_ohlc_csv


REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA_PATH = REPO_ROOT / "examples" / "data" / "sample_tqqq_qld_like.csv"


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
