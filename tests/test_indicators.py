import pytest

from market_signal_lab.indicators import (
    moving_average,
    percent_change,
    rolling_max,
    rolling_min,
)


def test_moving_average_returns_complete_windows() -> None:
    assert moving_average([10, 12, 14, 16], 2) == [11.0, 13.0, 15.0]
    assert moving_average([10, 12, 14, 16], 4) == [13.0]


def test_moving_average_returns_empty_when_window_is_too_large() -> None:
    assert moving_average([10, 12], 3) == []


def test_rolling_max_returns_complete_windows() -> None:
    assert rolling_max([10, 15, 12, 18, 11], 3) == [15.0, 18.0, 18.0]


def test_rolling_min_returns_complete_windows() -> None:
    assert rolling_min([10, 15, 12, 18, 11], 3) == [10.0, 12.0, 11.0]


def test_rolling_helpers_handle_window_of_one() -> None:
    values = [10, 12.5, 9]

    assert moving_average(values, 1) == [10.0, 12.5, 9.0]
    assert rolling_max(values, 1) == [10.0, 12.5, 9.0]
    assert rolling_min(values, 1) == [10.0, 12.5, 9.0]


def test_percent_change_defaults_to_one_period() -> None:
    assert percent_change([100, 110, 99]) == [0.1, -0.1]


def test_percent_change_supports_multi_period_changes() -> None:
    assert percent_change([100, 110, 121, 133.1], periods=2) == pytest.approx(
        [0.21, 0.21],
    )


@pytest.mark.parametrize(
    ("helper", "argument_name"),
    [
        (moving_average, "window"),
        (rolling_max, "window"),
        (rolling_min, "window"),
        (percent_change, "periods"),
    ],
)
def test_helpers_require_positive_window_or_period(helper, argument_name: str) -> None:
    with pytest.raises(ValueError, match=f"{argument_name} must be at least 1"):
        helper([1, 2, 3], 0)


def test_percent_change_returns_empty_when_period_is_too_large() -> None:
    assert percent_change([100, 110], periods=3) == []


def test_percent_change_rejects_zero_prior_value() -> None:
    with pytest.raises(ValueError, match="zero as a prior value"):
        percent_change([0, 10])
