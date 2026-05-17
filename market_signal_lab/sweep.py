"""Research-only parameter sweep helpers for moving-average strategies."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

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
from market_signal_lab.strategies import moving_average_crossover_strategy


@dataclass(frozen=True)
class SweepResult:
    """One evaluated short/long moving-average configuration."""

    short_window: int
    long_window: int
    metrics: dict[str, float]

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
) -> list[SweepResult]:
    """Evaluate moving-average configurations and return ranked research results."""

    if top_n is not None and top_n < 1:
        raise ValueError("top_n must be at least 1 when set")

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
        )
        for short_window, long_window in grid
    ]

    ranked = rank_sweep_results(results)
    return ranked[:top_n] if top_n is not None else ranked


def rank_sweep_results(results: Sequence[SweepResult]) -> list[SweepResult]:
    """Order results by total return then max drawdown, both descending."""

    return sorted(results, key=lambda result: (result.total_return, result.max_drawdown), reverse=True)


def _evaluate_pair(
    bars: Sequence[PriceBar],
    short_window: int,
    long_window: int,
    fee_bps: float,
    initial_equity: float,
) -> SweepResult:
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

    return SweepResult(
        short_window=short_window,
        long_window=long_window,
        metrics={
            "total_return": total_return(strategy_returns),
            "max_drawdown": max_drawdown(strategy_returns),
            "annualized_return": annualized_return(strategy_returns),
            "volatility": volatility(strategy_returns),
            "sharpe_like": sharpe_like(strategy_returns),
            "win_rate": win_rate_from_returns(strategy_returns),
        },
    )


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
