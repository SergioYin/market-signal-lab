"""Train/test splitting helpers for price-bar research workflows."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from market_signal_lab.data import PriceBar


@dataclass(frozen=True)
class TrainTestSplit:
    """Named train/test slices of a price-bar sequence."""

    train: list[PriceBar]
    test: list[PriceBar]


def split_train_test(
    bars: Sequence[PriceBar],
    *,
    train_ratio: float | None = None,
    cutoff_date: str | None = None,
) -> TrainTestSplit:
    """Split price bars into train/test slices by ratio or ISO cutoff date.

    Ratio splits put the first ``train_ratio`` share of ordered bars into train.
    Cutoff splits put bars before the cutoff date into train and bars on or after
    the cutoff date into test.
    """

    _validate_split_selector(train_ratio, cutoff_date)
    _validate_ordered_bars(bars)

    if train_ratio is not None:
        split_index = int(len(bars) * train_ratio)
    else:
        cutoff = _parse_cutoff_date(cutoff_date)
        split_index = _cutoff_index(bars, cutoff)

    train = list(bars[:split_index])
    test = list(bars[split_index:])
    _validate_non_empty_partitions(train, test)
    return TrainTestSplit(train=train, test=test)


def _validate_split_selector(
    train_ratio: float | None,
    cutoff_date: str | None,
) -> None:
    if (train_ratio is None) == (cutoff_date is None):
        raise ValueError("provide exactly one split selector: train_ratio or cutoff_date")

    if train_ratio is not None and not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be greater than 0 and less than 1")


def _validate_ordered_bars(bars: Sequence[PriceBar]) -> None:
    for previous, current in zip(bars, bars[1:]):
        if current.date <= previous.date:
            raise ValueError("bars must be ordered by strictly increasing date")


def _parse_cutoff_date(cutoff_date: str | None) -> date:
    if cutoff_date is None:
        raise ValueError("cutoff_date is required")

    try:
        return date.fromisoformat(cutoff_date)
    except ValueError as exc:
        raise ValueError(
            f"split cutoff must be an ISO date (YYYY-MM-DD): {cutoff_date!r}"
        ) from exc


def _cutoff_index(bars: Sequence[PriceBar], cutoff: date) -> int:
    for index, bar in enumerate(bars):
        if bar.date >= cutoff:
            return index
    return len(bars)


def _validate_non_empty_partitions(
    train: Sequence[PriceBar],
    test: Sequence[PriceBar],
) -> None:
    if not train:
        raise ValueError(
            "validation split produced an empty training partition; choose a "
            "larger split ratio or a later split cutoff"
        )
    if not test:
        raise ValueError(
            "validation split produced an empty test partition; choose a "
            "smaller split ratio or an earlier split cutoff"
        )
