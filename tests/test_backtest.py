from datetime import date, timedelta

import pytest

from market_signal_lab.backtest import EquityCurveRecord, backtest_long_cash
from market_signal_lab.data import PriceBar


def test_backtest_applies_targets_to_next_bar_returns_without_lookahead() -> None:
    bars = _bars([100, 50, 100])

    records = backtest_long_cash(bars, [0, 1, 0])

    assert records == [
        EquityCurveRecord(
            date=date(2024, 1, 1),
            equity=1.0,
            exposure=0.0,
            market_return=0.0,
            strategy_return=0.0,
            fee=0.0,
        ),
        EquityCurveRecord(
            date=date(2024, 1, 2),
            equity=1.0,
            exposure=0.0,
            market_return=-0.5,
            strategy_return=0.0,
            fee=0.0,
        ),
        EquityCurveRecord(
            date=date(2024, 1, 3),
            equity=2.0,
            exposure=1.0,
            market_return=1.0,
            strategy_return=1.0,
            fee=0.0,
        ),
    ]


def test_backtest_charges_fee_drag_when_exposure_changes() -> None:
    bars = _bars([100, 100, 100])

    records = backtest_long_cash(bars, [0, 1, 1], fee_bps=10)

    assert records[0].equity == 1.0
    assert records[1].equity == 1.0
    assert records[2].fee == 0.001
    assert records[2].strategy_return == -0.001
    assert records[2].equity == pytest.approx(0.999)


def _bars(closes: list[float]) -> list[PriceBar]:
    start = date(2024, 1, 1)
    bars: list[PriceBar] = []
    for offset, close in enumerate(closes):
        bar_date = start + timedelta(days=offset)
        bars.append(
            PriceBar(
                date=bar_date,
                open=close,
                high=close,
                low=close,
                close=close,
            ),
        )

    return bars
