from datetime import date
from io import StringIO

import pytest

from market_signal_lab.data import PriceBar, load_ohlc_csv


def test_load_ohlc_csv_from_file_like() -> None:
    csv_data = StringIO(
        "date,open,high,low,close\n"
        "2024-01-02,10.5,11.25,10.0,10.75\n"
        "2024-01-03,10.75,12.0,10.5,11.5\n"
    )

    bars = load_ohlc_csv(csv_data)

    assert bars == [
        PriceBar(date(2024, 1, 2), 10.5, 11.25, 10.0, 10.75),
        PriceBar(date(2024, 1, 3), 10.75, 12.0, 10.5, 11.5),
    ]


def test_load_ohlc_csv_from_path(tmp_path) -> None:
    csv_path = tmp_path / "prices.csv"
    csv_path.write_text(
        "date,open,high,low,close\n"
        "2024-01-02,10,11,9,10.5\n",
    )

    assert load_ohlc_csv(csv_path) == [
        PriceBar(date(2024, 1, 2), 10.0, 11.0, 9.0, 10.5),
    ]


def test_load_ohlc_csv_requires_header() -> None:
    with pytest.raises(ValueError, match="missing a header row"):
        load_ohlc_csv(StringIO(""))


def test_load_ohlc_csv_requires_ohlc_columns() -> None:
    with pytest.raises(ValueError, match="missing required column\\(s\\): low, close"):
        load_ohlc_csv(StringIO("date,open,high\n2024-01-02,10,11\n"))


def test_load_ohlc_csv_rejects_invalid_date() -> None:
    csv_data = StringIO("date,open,high,low,close\nnot-a-date,10,11,9,10.5\n")

    with pytest.raises(ValueError, match="Invalid date on row 2"):
        load_ohlc_csv(csv_data)


def test_load_ohlc_csv_rejects_invalid_price() -> None:
    csv_data = StringIO("date,open,high,low,close\n2024-01-02,10,nope,9,10.5\n")

    with pytest.raises(ValueError, match="Invalid high on row 2"):
        load_ohlc_csv(csv_data)


def test_load_ohlc_csv_rejects_inconsistent_high_low() -> None:
    high_too_low = StringIO("date,open,high,low,close\n2024-01-02,10,10.5,9,11\n")
    low_too_high = StringIO("date,open,high,low,close\n2024-01-02,10,11,10.5,10\n")

    with pytest.raises(ValueError, match="high is too low"):
        load_ohlc_csv(high_too_low)
    with pytest.raises(ValueError, match="low is too high"):
        load_ohlc_csv(low_too_high)
