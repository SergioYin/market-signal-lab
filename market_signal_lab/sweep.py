"""Research-only parameter sweep helpers for moving-average strategies."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from market_signal_lab.backtest import backtest_long_cash
from market_signal_lab.data import PriceBar
from market_signal_lab.metrics import (
    annualized_return,
    max_drawdown,
    sharpe_like,
    total_return,
    volatility,
    win_rate_from_returns,
)
from market_signal_lab.report import render_validation_split_note
from market_signal_lab.strategies import moving_average_crossover_strategy


SWEEP_REPORT_CAVEAT = (
    "Research-only: this sweep is a historical parameter screen, not investment "
    "advice, not a recommendation, and not evidence of future performance."
)

SWEEP_REPORT_COLUMNS = (
    "rank",
    "short_window",
    "long_window",
    "total_return",
    "annualized_return",
    "max_drawdown",
    "volatility",
    "sharpe_like",
    "win_rate",
)

SWEEP_REPORT_SPLIT_COLUMNS = (
    "rank",
    "short_window",
    "long_window",
    "total_return",
    "train_total_return",
    "test_total_return",
    "annualized_return",
    "max_drawdown",
    "volatility",
    "sharpe_like",
    "win_rate",
)

SWEEP_OVERFIT_CAVEAT = (
    "Train/test columns are a comparison aid for historical research only; a "
    "large train/test gap can be a sign of parameter overfitting and is not a "
    "trading recommendation."
)


@dataclass(frozen=True)
class SweepResult:
    """One evaluated short/long moving-average configuration."""

    short_window: int
    long_window: int
    metrics: dict[str, float]
    train_metrics: dict[str, float] | None = None
    test_metrics: dict[str, float] | None = None

    @property
    def total_return(self) -> float:
        return self.metrics["total_return"]

    @property
    def max_drawdown(self) -> float:
        return self.metrics["max_drawdown"]


def moving_average_parameter_grid(
    short_windows: Sequence[int],
    long_windows: Sequence[int],
) -> list[tuple[int, int]]:
    """Return all valid (short, long) pairs preserving input order."""

    short_values = _normalize_window_values(short_windows)
    long_values = _normalize_window_values(long_windows)

    pairs: list[tuple[int, int]] = []
    for short_window in short_values:
        for long_window in long_values:
            if short_window < long_window:
                pairs.append((short_window, long_window))

    return pairs


def run_moving_average_sweep(
    bars: Sequence[PriceBar],
    short_windows: Sequence[int],
    long_windows: Sequence[int],
    fee_bps: float = 0.0,
    initial_equity: float = 1.0,
    top_n: int | None = None,
    train_bars: Sequence[PriceBar] | None = None,
    test_bars: Sequence[PriceBar] | None = None,
) -> list[SweepResult]:
    """Evaluate moving-average configurations and return ranked research results."""

    if top_n is not None and top_n < 1:
        raise ValueError("top_n must be at least 1 when set")
    if (train_bars is None) != (test_bars is None):
        raise ValueError("train_bars and test_bars must be provided together")

    grid = moving_average_parameter_grid(short_windows, long_windows)
    if not grid:
        return []

    results = [
        _evaluate_pair(
            bars=bars,
            short_window=short_window,
            long_window=long_window,
            fee_bps=fee_bps,
            initial_equity=initial_equity,
            train_bars=train_bars,
            test_bars=test_bars,
        )
        for short_window, long_window in grid
    ]

    ranked = rank_sweep_results(results)
    return ranked[:top_n] if top_n is not None else ranked


def rank_sweep_results(results: Sequence[SweepResult]) -> list[SweepResult]:
    """Order results by total return then max drawdown, both descending."""

    return sorted(results, key=lambda result: (result.total_return, result.max_drawdown), reverse=True)


def format_sweep_percentage(value: float) -> str:
    """Format a decimal metric as a percentage for sweep reports."""

    return f"{value * 100:.2f}%"


def format_sweep_number(value: float) -> str:
    """Format a plain numeric metric for sweep reports."""

    return f"{value:.4f}"


def render_sweep_report(
    results: Sequence[SweepResult],
    validation_split: Mapping[str, Any] | None = None,
) -> str:
    """Render ranked moving-average sweep results as a Markdown report."""

    lines = [
        "# Moving Average Sweep Report",
        "",
        f"> {SWEEP_REPORT_CAVEAT}",
        "",
        *render_validation_split_note(validation_split),
    ]
    if validation_split is not None:
        lines.extend([f"> {SWEEP_OVERFIT_CAVEAT}", ""])

    columns = _sweep_report_columns(validation_split)
    lines.extend(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
        ]
    )

    for rank, result in enumerate(results, start=1):
        lines.append(
            _render_sweep_result_row(
                rank,
                result,
                include_split_columns=validation_split is not None,
            )
        )

    if not results:
        lines.append("| " + " | ".join("-" for _ in columns) + " |")

    return "\n".join(lines) + "\n"


def _evaluate_pair(
    bars: Sequence[PriceBar],
    short_window: int,
    long_window: int,
    fee_bps: float,
    initial_equity: float,
    train_bars: Sequence[PriceBar] | None = None,
    test_bars: Sequence[PriceBar] | None = None,
) -> SweepResult:
    return SweepResult(
        short_window=short_window,
        long_window=long_window,
        metrics=_evaluate_metrics(
            bars=bars,
            short_window=short_window,
            long_window=long_window,
            fee_bps=fee_bps,
            initial_equity=initial_equity,
        ),
        train_metrics=(
            _evaluate_metrics(
                bars=train_bars,
                short_window=short_window,
                long_window=long_window,
                fee_bps=fee_bps,
                initial_equity=initial_equity,
            )
            if train_bars is not None
            else None
        ),
        test_metrics=(
            _evaluate_metrics(
                bars=test_bars,
                short_window=short_window,
                long_window=long_window,
                fee_bps=fee_bps,
                initial_equity=initial_equity,
            )
            if test_bars is not None
            else None
        ),
    )


def _evaluate_metrics(
    bars: Sequence[PriceBar],
    short_window: int,
    long_window: int,
    fee_bps: float,
    initial_equity: float,
) -> dict[str, float]:
    signals = moving_average_crossover_strategy(
        bars,
        short_window=short_window,
        long_window=long_window,
    )
    target_exposures = [signal.target_exposure for signal in signals]
    curve = backtest_long_cash(
        bars=bars,
        target_exposures=target_exposures,
        fee_bps=fee_bps,
        initial_equity=initial_equity,
    )
    strategy_returns = [record.strategy_return for record in curve[1:]]
    return {
        "total_return": total_return(strategy_returns),
        "max_drawdown": max_drawdown(strategy_returns),
        "annualized_return": annualized_return(strategy_returns),
        "volatility": volatility(strategy_returns),
        "sharpe_like": sharpe_like(strategy_returns),
        "win_rate": win_rate_from_returns(strategy_returns),
    }


def _sweep_report_columns(
    validation_split: Mapping[str, Any] | None,
) -> tuple[str, ...]:
    if validation_split is None:
        return SWEEP_REPORT_COLUMNS
    return SWEEP_REPORT_SPLIT_COLUMNS


def _render_sweep_result_row(
    rank: int,
    result: SweepResult,
    *,
    include_split_columns: bool,
) -> str:
    values: tuple[str, ...]
    if not include_split_columns:
        values = (
            str(rank),
            str(result.short_window),
            str(result.long_window),
            format_sweep_percentage(result.metrics["total_return"]),
            format_sweep_percentage(result.metrics["annualized_return"]),
            format_sweep_percentage(result.metrics["max_drawdown"]),
            format_sweep_percentage(result.metrics["volatility"]),
            format_sweep_number(result.metrics["sharpe_like"]),
            format_sweep_percentage(result.metrics["win_rate"]),
        )
    else:
        values = (
            str(rank),
            str(result.short_window),
            str(result.long_window),
            format_sweep_percentage(result.metrics["total_return"]),
            _format_optional_total_return(result.train_metrics),
            _format_optional_total_return(result.test_metrics),
            format_sweep_percentage(result.metrics["annualized_return"]),
            format_sweep_percentage(result.metrics["max_drawdown"]),
            format_sweep_percentage(result.metrics["volatility"]),
            format_sweep_number(result.metrics["sharpe_like"]),
            format_sweep_percentage(result.metrics["win_rate"]),
        )

    return "| " + " | ".join(values) + " |"


def _format_optional_total_return(metrics: Mapping[str, float] | None) -> str:
    if metrics is None:
        return "-"
    return format_sweep_percentage(metrics["total_return"])


def _normalize_window_values(values: Sequence[int]) -> list[int]:
    if not values:
        raise ValueError("window sequence cannot be empty")

    normalized: list[int] = []
    seen: set[int] = set()
    for value in values:
        if not isinstance(value, int):
            raise TypeError("window values must be integers")
        if value < 1:
            raise ValueError("window values must be at least 1")
        if value in seen:
            continue
        seen.add(value)
        normalized.append(value)

    return normalized
