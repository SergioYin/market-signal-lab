from datetime import date, timedelta

import pytest

from market_signal_lab.data import PriceBar
from market_signal_lab.split import TrainTestSplit, split_train_test


def _bars(count: int) -> list[PriceBar]:
    start = date(2024, 1, 2)
    return [_bar(start + timedelta(days=index)) for index in range(count)]


def _bar(bar_date: date) -> PriceBar:
    return PriceBar(bar_date, 10.0, 11.0, 9.0, 10.5)


def test_split_train_test_by_ratio() -> None:
    bars = _bars(5)

    result = split_train_test(bars, train_ratio=0.6)

    assert result == TrainTestSplit(train=bars[:3], test=bars[3:])


def test_split_train_test_by_cutoff_date() -> None:
    bars = _bars(4)

    result = split_train_test(bars, cutoff_date="2024-01-04")

    assert result.train == bars[:2]
    assert result.test == bars[2:]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"train_ratio": 0.0}, "train_ratio must be greater than 0"),
        ({"train_ratio": 1.0}, "train_ratio must be greater than 0"),
        ({}, "provide exactly one"),
        (
            {"train_ratio": 0.5, "cutoff_date": "2024-01-03"},
            "provide exactly one",
        ),
        ({"cutoff_date": "not-a-date"}, "cutoff_date must be an ISO date"),
    ],
)
def test_split_train_test_rejects_invalid_split_inputs(
    kwargs: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        split_train_test(_bars(3), **kwargs)


@pytest.mark.parametrize(
    ("bars", "kwargs", "message"),
    [
        ([], {"train_ratio": 0.5}, "train partition must not be empty"),
        (_bars(1), {"train_ratio": 0.5}, "train partition must not be empty"),
        (_bars(2), {"cutoff_date": "2024-01-02"}, "train partition must not be empty"),
        (_bars(2), {"cutoff_date": "2024-01-05"}, "test partition must not be empty"),
    ],
)
def test_split_train_test_rejects_empty_partitions(
    bars: list[PriceBar],
    kwargs: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        split_train_test(bars, **kwargs)


def test_split_train_test_requires_strictly_increasing_dates() -> None:
    bars = [
        _bar(date(2024, 1, 3)),
        _bar(date(2024, 1, 2)),
    ]

    with pytest.raises(ValueError, match="strictly increasing date"):
        split_train_test(bars, train_ratio=0.5)


def test_split_train_test_rejects_duplicate_dates() -> None:
    bars = [
        _bar(date(2024, 1, 2)),
        _bar(date(2024, 1, 2)),
    ]

    with pytest.raises(ValueError, match="strictly increasing date"):
        split_train_test(bars, train_ratio=0.5)
