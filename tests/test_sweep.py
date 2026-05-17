from datetime import date, timedelta

from market_signal_lab.data import PriceBar
from market_signal_lab.sweep import (
    SweepResult,
    moving_average_parameter_grid,
    rank_sweep_results,
    run_moving_average_sweep,
)


def test_moving_average_parameter_grid_filters_invalid_pairs_and_deduplicates() -> None:
    assert moving_average_parameter_grid([2, 3, 2], [3, 3, 4]) == [
        (2, 3),
        (2, 4),
        (3, 4),
    ]


def test_run_moving_average_sweep_ranks_by_total_return() -> None:
    bars = _bars([100, 101, 102, 103, 104, 105])

    ranked = run_moving_average_sweep(
        bars,
        short_windows=(1, 2),
        long_windows=(2, 3),
        top_n=2,
    )

    assert [(result.short_window, result.long_window) for result in ranked] == [
        (1, 2),
        (1, 3),
    ]


def test_rank_sweep_results_uses_max_drawdown_as_tie_breaker() -> None:
    ranked = rank_sweep_results(
        [
            SweepResult(
                short_window=3,
                long_window=8,
                metrics={"total_return": 0.4, "max_drawdown": -0.30},
            ),
            SweepResult(
                short_window=2,
                long_window=5,
                metrics={"total_return": 0.4, "max_drawdown": -0.10},
            ),
        ]
    )

    assert ranked[0].short_window == 2
    assert ranked[0].long_window == 5


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
            )
        )

    return bars
