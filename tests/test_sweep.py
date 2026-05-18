from datetime import date, timedelta

from market_signal_lab.data import PriceBar
from market_signal_lab.sweep import (
    SweepResult,
    format_sweep_number,
    format_sweep_percentage,
    moving_average_parameter_grid,
    rank_sweep_results,
    render_sweep_report,
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


def test_format_sweep_percentage_and_number() -> None:
    assert format_sweep_percentage(0.12345) == "12.35%"
    assert format_sweep_percentage(-0.08765) == "-8.77%"
    assert format_sweep_number(1.23456) == "1.2346"


def test_render_sweep_report_contains_research_caveat_and_table() -> None:
    report = render_sweep_report(
        [
            _sweep_result(
                short_window=2,
                long_window=8,
                total_return=0.251,
                annualized_return=0.118,
                max_drawdown=-0.0725,
                volatility=0.1944,
                sharpe_like=0.60711,
                win_rate=0.536,
            )
        ]
    )

    assert "Research-only" in report
    assert "not investment advice" in report
    assert "not evidence of future performance" in report
    assert (
        "| rank | short_window | long_window | total_return | "
        "annualized_return | max_drawdown | volatility | sharpe_like | win_rate |"
    ) in report
    assert "| 1 | 2 | 8 | 25.10% | 11.80% | -7.25% | 19.44% | 0.6071 | 53.60% |" in report


def test_render_sweep_report_uses_input_order_for_rank() -> None:
    report = render_sweep_report(
        [
            _sweep_result(short_window=5, long_window=20, total_return=0.1),
            _sweep_result(short_window=3, long_window=10, total_return=0.2),
        ]
    )

    first_row = "| 1 | 5 | 20 | 10.00%"
    second_row = "| 2 | 3 | 10 | 20.00%"
    assert first_row in report
    assert second_row in report
    assert report.index(first_row) < report.index(second_row)


def test_render_sweep_report_handles_empty_results() -> None:
    report = render_sweep_report([])

    assert "Research-only" in report
    assert "| - | - | - | - | - | - | - | - | - |" in report


def _sweep_result(
    short_window: int,
    long_window: int,
    total_return: float,
    annualized_return: float = 0.0,
    max_drawdown: float = 0.0,
    volatility: float = 0.0,
    sharpe_like: float = 0.0,
    win_rate: float = 0.0,
) -> SweepResult:
    return SweepResult(
        short_window=short_window,
        long_window=long_window,
        metrics={
            "total_return": total_return,
            "annualized_return": annualized_return,
            "max_drawdown": max_drawdown,
            "volatility": volatility,
            "sharpe_like": sharpe_like,
            "win_rate": win_rate,
        },
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
            )
        )

    return bars
