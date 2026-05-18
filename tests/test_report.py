from datetime import date

from market_signal_lab.backtest import EquityCurveRecord
from market_signal_lab.report import render_experiment_report


def test_render_experiment_report_contains_backtest_caveats() -> None:
    report = render_experiment_report(
        strategy_config={
            "name": "MA crossover",
            "symbols": ["SPY"],
            "short_window": 20,
            "long_window": 50,
        },
        backtest_curve=_curve(),
        metrics={
            "total_return": 0.10,
            "buy_and_hold_total_return": 0.05,
            "strategy_minus_buy_and_hold_return": 0.05,
            "sharpe_like": 1.25,
        },
        risk_notes=["Uses daily closing prices."],
    )

    assert "## Backtest Caveats" in report
    assert "- **Buy-and-hold total return**: 5.00%" in report
    assert "- **Strategy minus buy-and-hold return**: 5.00%" in report
    assert "Backtest results are hypothetical" in report
    assert "future performance" in report
    assert "survivorship bias" in report
    assert "TQQQ" not in report
    assert "QLD" not in report


def test_render_experiment_report_warns_for_leveraged_etfs() -> None:
    report = render_experiment_report(
        strategy_config={"symbols": ["TQQQ", "QLD"]},
        backtest_curve=_curve(),
        metrics={"max_drawdown": -0.25},
        risk_notes=[],
    )

    assert "Leveraged ETF warning" in report
    assert "TQQQ, QLD" in report
    assert "leveraged daily returns" in report
    assert "volatility decay" in report
    assert "longer holding periods" in report


def _curve() -> list[EquityCurveRecord]:
    return [
        EquityCurveRecord(
            date=date(2024, 1, 1),
            equity=1.0,
            exposure=0.0,
            market_return=0.0,
            strategy_return=0.0,
            fee=0.0,
        ),
        EquityCurveRecord(
            date=date(2024, 1, 2),
            equity=1.1,
            exposure=1.0,
            market_return=0.1,
            strategy_return=0.1,
            fee=0.0,
        ),
    ]
