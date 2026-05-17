"""Stdlib-only performance metrics for fractional return series."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import SupportsFloat

Number = SupportsFloat


def total_return(returns: Sequence[Number]) -> float:
    """Return the compounded total return for fractional period returns."""

    growth = _compound_growth(_to_floats(returns))
    return growth - 1


def annualized_return(returns: Sequence[Number], periods_per_year: int = 252) -> float:
    """Return CAGR-style annualized return from fractional period returns."""

    _validate_periods_per_year(periods_per_year)
    points = _to_floats(returns)
    if not points:
        return 0.0

    growth = _compound_growth(points)
    if growth == 0:
        return -1.0

    return math.pow(growth, periods_per_year / len(points)) - 1


def max_drawdown(returns: Sequence[Number]) -> float:
    """Return the worst drawdown from the compounded equity path."""

    equity = 1.0
    peak = equity
    worst = 0.0

    for period_return in _to_floats(returns):
        _validate_return(period_return)
        equity *= 1 + period_return
        peak = max(peak, equity)
        drawdown = equity / peak - 1
        worst = min(worst, drawdown)

    return worst


def volatility(returns: Sequence[Number], periods_per_year: int = 252) -> float:
    """Return annualized population volatility for fractional period returns."""

    _validate_periods_per_year(periods_per_year)
    points = _to_floats(returns)
    if len(points) < 2:
        return 0.0

    mean = sum(points) / len(points)
    variance = sum(math.pow(point - mean, 2) for point in points) / len(points)
    return math.sqrt(variance) * math.sqrt(periods_per_year)


def sharpe_like(returns: Sequence[Number], periods_per_year: int = 252) -> float:
    """Return a zero-risk-free annualized mean-return-to-volatility ratio."""

    _validate_periods_per_year(periods_per_year)
    points = _to_floats(returns)
    if not points:
        return 0.0

    annualized_volatility = volatility(points, periods_per_year)
    if annualized_volatility == 0:
        return 0.0

    mean = sum(points) / len(points)
    annualized_mean = mean * periods_per_year
    return annualized_mean / annualized_volatility


def win_rate_from_returns(returns: Sequence[Number]) -> float:
    """Return the share of periods with positive fractional returns."""

    points = _to_floats(returns)
    if not points:
        return 0.0

    wins = sum(1 for point in points if point > 0)
    return wins / len(points)


def _compound_growth(returns: Sequence[float]) -> float:
    growth = 1.0
    for period_return in returns:
        _validate_return(period_return)
        growth *= 1 + period_return

    return growth


def _validate_periods_per_year(periods_per_year: int) -> None:
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be at least 1")


def _validate_return(period_return: float) -> None:
    if period_return < -1:
        raise ValueError("period returns cannot be less than -100%")


def _to_floats(values: Sequence[Number]) -> list[float]:
    return [float(value) for value in values]
