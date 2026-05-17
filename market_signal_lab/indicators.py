"""Small stdlib-only numeric indicator helpers."""

from __future__ import annotations

from collections.abc import Sequence
from typing import SupportsFloat

Number = SupportsFloat


def moving_average(values: Sequence[Number], window: int) -> list[float]:
    """Return simple moving averages for each complete rolling window."""

    _validate_positive("window", window)
    points = _to_floats(values)
    if len(points) < window:
        return []

    total = sum(points[:window])
    averages = [total / window]
    for index in range(window, len(points)):
        total += points[index] - points[index - window]
        averages.append(total / window)

    return averages


def rolling_max(values: Sequence[Number], window: int) -> list[float]:
    """Return the maximum value for each complete rolling window."""

    _validate_positive("window", window)
    points = _to_floats(values)
    return [max(points[index : index + window]) for index in _window_starts(points, window)]


def rolling_min(values: Sequence[Number], window: int) -> list[float]:
    """Return the minimum value for each complete rolling window."""

    _validate_positive("window", window)
    points = _to_floats(values)
    return [min(points[index : index + window]) for index in _window_starts(points, window)]


def percent_change(values: Sequence[Number], periods: int = 1) -> list[float]:
    """Return fractional percent changes between values separated by periods."""

    _validate_positive("periods", periods)
    points = _to_floats(values)
    changes: list[float] = []

    for index in range(periods, len(points)):
        previous = points[index - periods]
        if previous == 0:
            raise ValueError("percent_change cannot use zero as a prior value")
        changes.append((points[index] - previous) / previous)

    return changes


def _window_starts(values: Sequence[float], window: int) -> range:
    return range(0, max(len(values) - window + 1, 0))


def _validate_positive(name: str, value: int) -> None:
    if value < 1:
        raise ValueError(f"{name} must be at least 1")


def _to_floats(values: Sequence[Number]) -> list[float]:
    return [float(value) for value in values]
