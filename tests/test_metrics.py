import math

import pytest

from market_signal_lab.metrics import (
    annualized_return,
    max_drawdown,
    sharpe_like,
    total_return,
    volatility,
    win_rate_from_returns,
)


def test_total_return_compounds_fractional_returns() -> None:
    assert total_return([0.10, -0.20, 0.25]) == pytest.approx(0.10)


def test_annualized_return_uses_compounded_growth() -> None:
    assert annualized_return([0.10, 0.10], periods_per_year=2) == pytest.approx(0.21)
    assert annualized_return([0.10], periods_per_year=2) == pytest.approx(0.21)


def test_annualized_return_handles_total_loss() -> None:
    assert annualized_return([-1.0], periods_per_year=252) == -1.0


def test_max_drawdown_uses_compounded_equity_path() -> None:
    returns = [0.10, -0.20, 0.05, -0.10, 0.30]

    assert max_drawdown(returns) == pytest.approx(-0.244)


def test_volatility_returns_annualized_population_standard_deviation() -> None:
    returns = [0.10, -0.10]

    assert volatility(returns, periods_per_year=4) == pytest.approx(0.20)


def test_sharpe_like_uses_annualized_mean_over_annualized_volatility() -> None:
    returns = [0.10, 0.00, 0.10]
    expected_volatility = math.sqrt(2 / 900) * math.sqrt(9)
    expected_sharpe = 0.60 / expected_volatility

    assert sharpe_like(returns, periods_per_year=9) == pytest.approx(expected_sharpe)


def test_sharpe_like_returns_zero_when_volatility_is_zero() -> None:
    assert sharpe_like([0.01, 0.01], periods_per_year=252) == 0.0


def test_win_rate_from_returns_counts_positive_periods() -> None:
    assert win_rate_from_returns([0.05, 0.0, -0.01, 0.02]) == 0.5


def test_metrics_return_zero_for_empty_inputs() -> None:
    assert total_return([]) == 0.0
    assert annualized_return([]) == 0.0
    assert max_drawdown([]) == 0.0
    assert volatility([]) == 0.0
    assert sharpe_like([]) == 0.0
    assert win_rate_from_returns([]) == 0.0


@pytest.mark.parametrize(
    "helper",
    [
        annualized_return,
        volatility,
        sharpe_like,
    ],
)
def test_annualized_metrics_require_positive_periods_per_year(helper) -> None:
    with pytest.raises(ValueError, match="periods_per_year must be at least 1"):
        helper([0.01], periods_per_year=0)


@pytest.mark.parametrize(
    "helper",
    [
        total_return,
        annualized_return,
        max_drawdown,
    ],
)
def test_compounding_metrics_reject_impossible_period_losses(helper) -> None:
    with pytest.raises(ValueError, match="less than -100%"):
        helper([-1.01])
