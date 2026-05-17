from datetime import date, timedelta

import pytest

from market_signal_lab.data import PriceBar
from market_signal_lab.strategies import (
    StrategyResult,
    moving_average_crossover_strategy,
)


def test_moving_average_crossover_returns_one_result_per_bar() -> None:
    bars = _bars([10, 11, 12, 13])

    results = moving_average_crossover_strategy(bars, short_window=2, long_window=3)

    assert [result.date for result in results] == [bar.date for bar in bars]
    assert all(isinstance(result, StrategyResult) for result in results)


def test_moving_average_crossover_stays_flat_until_long_average_is_available() -> None:
    bars = _bars([10, 11, 12])

    results = moving_average_crossover_strategy(bars, short_window=2, long_window=3)

    assert results[0] == StrategyResult(
        date=date(2024, 1, 1),
        target_exposure=0,
        reason="Insufficient history for 2/3-day moving averages",
        short_average=None,
        long_average=None,
    )
    assert results[1] == StrategyResult(
        date=date(2024, 1, 2),
        target_exposure=0,
        reason="Insufficient history for 2/3-day moving averages",
        short_average=10.5,
        long_average=None,
    )
    assert results[2].target_exposure == 1
    assert results[2].short_average == 11.5
    assert results[2].long_average == 11.0
    assert results[2].reason == "Bullish trend: 2-day average is above 3-day average"


def test_moving_average_crossover_reports_bullish_crossovers() -> None:
    bars = _bars([10, 10, 10, 14])

    results = moving_average_crossover_strategy(bars, short_window=2, long_window=3)

    assert [result.target_exposure for result in results] == [0, 0, 0, 1]
    assert results[2].reason == "Neutral trend: 2-day average equals 3-day average"
    assert results[3].reason == "Bullish crossover: 2-day average moved above 3-day average"


def test_moving_average_crossover_reports_bearish_crossovers() -> None:
    bars = _bars([10, 11, 12, 8])

    results = moving_average_crossover_strategy(bars, short_window=2, long_window=3)

    assert [result.target_exposure for result in results] == [0, 0, 1, 0]
    assert results[2].reason == "Bullish trend: 2-day average is above 3-day average"
    assert results[3].reason == "Bearish crossover: 2-day average moved at or below 3-day average"


@pytest.mark.parametrize(
    ("short_window", "long_window", "message"),
    [
        (0, 3, "short_window must be at least 1"),
        (2, 0, "long_window must be at least 1"),
        (3, 3, "short_window must be less than long_window"),
        (4, 3, "short_window must be less than long_window"),
    ],
)
def test_moving_average_crossover_validates_windows(
    short_window: int,
    long_window: int,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        moving_average_crossover_strategy(
            _bars([10, 11, 12]),
            short_window=short_window,
            long_window=long_window,
        )


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
