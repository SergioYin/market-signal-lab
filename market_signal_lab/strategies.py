"""Explainable trading strategy helpers."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from market_signal_lab.data import PriceBar
from market_signal_lab.indicators import moving_average


@dataclass(frozen=True)
class StrategyResult:
    """One daily strategy target with the reason for that target."""

    date: date
    target_exposure: int
    reason: str
    short_average: float | None = None
    long_average: float | None = None


def moving_average_crossover_strategy(
    bars: Sequence[PriceBar],
    short_window: int = 20,
    long_window: int = 50,
) -> list[StrategyResult]:
    """Return daily 0/1 exposure targets from a moving-average crossover rule."""

    _validate_windows(short_window, long_window)

    closes = [bar.close for bar in bars]
    short_averages = _align_complete_windows(
        moving_average(closes, short_window),
        len(closes),
    )
    long_averages = _align_complete_windows(
        moving_average(closes, long_window),
        len(closes),
    )

    results: list[StrategyResult] = []
    previous_relation: int | None = None
    for index, bar in enumerate(bars):
        short_average = short_averages[index]
        long_average = long_averages[index]

        if short_average is None or long_average is None:
            results.append(
                StrategyResult(
                    date=bar.date,
                    target_exposure=0,
                    reason=(
                        "Insufficient history for "
                        f"{short_window}/{long_window}-day moving averages"
                    ),
                    short_average=short_average,
                    long_average=long_average,
                ),
            )
            continue

        relation = _compare(short_average, long_average)
        target_exposure = 1 if relation > 0 else 0
        reason = _signal_reason(
            relation=relation,
            previous_relation=previous_relation,
            short_window=short_window,
            long_window=long_window,
        )
        results.append(
            StrategyResult(
                date=bar.date,
                target_exposure=target_exposure,
                reason=reason,
                short_average=short_average,
                long_average=long_average,
            ),
        )
        previous_relation = relation

    return results


def _align_complete_windows(
    averages: Sequence[float],
    total_count: int,
) -> list[float | None]:
    missing_count = total_count - len(averages)
    return [None] * missing_count + list(averages)


def _validate_windows(short_window: int, long_window: int) -> None:
    if short_window < 1:
        raise ValueError("short_window must be at least 1")
    if long_window < 1:
        raise ValueError("long_window must be at least 1")
    if short_window >= long_window:
        raise ValueError("short_window must be less than long_window")


def _compare(left: float, right: float) -> int:
    if left > right:
        return 1
    if left < right:
        return -1
    return 0


def _signal_reason(
    relation: int,
    previous_relation: int | None,
    short_window: int,
    long_window: int,
) -> str:
    pair = f"{short_window}-day average"
    benchmark = f"{long_window}-day average"

    if relation > 0 and previous_relation is not None and previous_relation <= 0:
        return f"Bullish crossover: {pair} moved above {benchmark}"
    if relation <= 0 and previous_relation is not None and previous_relation > 0:
        return f"Bearish crossover: {pair} moved at or below {benchmark}"
    if relation > 0:
        return f"Bullish trend: {pair} is above {benchmark}"
    if relation < 0:
        return f"Bearish trend: {pair} is below {benchmark}"
    return f"Neutral trend: {pair} equals {benchmark}"
