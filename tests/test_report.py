from datetime import date

from market_signal_lab.backtest import EquityCurveRecord
from market_signal_lab.report import (
    EXPOSURE_TRADE_REVIEW_NOTE,
    build_exposure_trade_review,
    render_experiment_report,
)

NOTE_LINE = f"- {EXPOSURE_TRADE_REVIEW_NOTE}"


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
    assert "## Modeled Exposure Review" in report
    assert NOTE_LINE in report
    assert "- **Periods in market**: 1 of 1 close-to-close periods (100.00%)." in report
    assert "- **Exposure changes**: 1." in report
    assert "- **Entries to market**: 1." in report
    assert "- **Exits to cash**: 0." in report
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


def test_render_experiment_report_includes_static_fixture_provenance() -> None:
    report = render_experiment_report(
        strategy_config={"symbol": "QQQ_LIKE"},
        backtest_curve=_curve(),
        metrics={"total_return": 0.10},
        data_provenance={
            "dataset_label": "sample_tqqq_qld_like",
            "data_kind": "synthetic_static_fixture",
            "source": "Hand-authored deterministic OHLC sample.",
            "created_date": "2026-05-18",
            "as_of_date": "2026-05-18",
            "limitations": [
                "Synthetic rows are not live-feed data.",
                "Do not use for advice, recommendations, predictions, or market claims.",
            ],
            "metadata_path": "examples/data/sample_tqqq_qld_like.csv.provenance.json",
            "research_only": True,
        },
    )

    assert "## Data Provenance" in report
    assert "Research-only fixture metadata" in report
    assert "- **Dataset label**: sample_tqqq_qld_like" in report
    assert "- **Data kind**: synthetic_static_fixture" in report
    assert "not investment advice" in report
    assert "not a prediction" in report
    assert "not live-feed data" in report


def test_build_exposure_trade_review_summarizes_curve_for_json() -> None:
    review = build_exposure_trade_review(
        [
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
                equity=1.0,
                exposure=1.0,
                market_return=0.01,
                strategy_return=0.009,
                fee=0.001,
            ),
            EquityCurveRecord(
                date=date(2024, 1, 3),
                equity=1.0,
                exposure=0.0,
                market_return=-0.01,
                strategy_return=-0.001,
                fee=0.001,
            ),
        ]
    )

    assert review == {
        "period_count": 2,
        "periods_in_market": 1,
        "periods_in_cash": 1,
        "percent_periods_in_market": 0.5,
        "percent_periods_in_cash": 0.5,
        "average_exposure": 0.5,
        "exposure_changes": 2,
        "entries_to_market": 1,
        "exits_to_cash": 1,
        "total_fee_drag": 0.002,
        "research_only": True,
        "note": EXPOSURE_TRADE_REVIEW_NOTE,
    }


def test_exposure_trade_review_stays_stable_for_no_trade_case() -> None:
    curve = [
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
            equity=1.0,
            exposure=0.0,
            market_return=0.01,
            strategy_return=0.0,
            fee=0.0,
        ),
        EquityCurveRecord(
            date=date(2024, 1, 3),
            equity=1.0,
            exposure=0.0,
            market_return=-0.01,
            strategy_return=0.0,
            fee=0.0,
        ),
    ]

    assert build_exposure_trade_review(curve) == {
        "period_count": 2,
        "periods_in_market": 0,
        "periods_in_cash": 2,
        "percent_periods_in_market": 0.0,
        "percent_periods_in_cash": 1.0,
        "average_exposure": 0.0,
        "exposure_changes": 0,
        "entries_to_market": 0,
        "exits_to_cash": 0,
        "total_fee_drag": 0.0,
        "research_only": True,
        "note": EXPOSURE_TRADE_REVIEW_NOTE,
    }

    report = render_experiment_report(
        strategy_config={"symbol": "AAA"},
        backtest_curve=curve,
        metrics={"total_return": 0.0},
    )

    assert NOTE_LINE in report
    assert "- **Periods in market**: 0 of 2 close-to-close periods (0.00%)." in report
    assert "- **Periods in cash**: 2 of 2 close-to-close periods (100.00%)." in report
    assert "- **Exposure changes**: 0." in report
    assert "- **Entries to market**: 0." in report
    assert "- **Exits to cash**: 0." in report


def test_exposure_trade_review_handles_single_record_without_periods() -> None:
    curve = [
        EquityCurveRecord(
            date=date(2024, 1, 1),
            equity=1.0,
            exposure=0.0,
            market_return=0.0,
            strategy_return=0.0,
            fee=0.0,
        ),
    ]

    assert build_exposure_trade_review(curve) == {
        "period_count": 0,
        "periods_in_market": 0,
        "periods_in_cash": 0,
        "percent_periods_in_market": 0.0,
        "percent_periods_in_cash": 0.0,
        "average_exposure": 0.0,
        "exposure_changes": 0,
        "entries_to_market": 0,
        "exits_to_cash": 0,
        "total_fee_drag": 0.0,
        "research_only": True,
        "note": EXPOSURE_TRADE_REVIEW_NOTE,
    }

    report = render_experiment_report(
        strategy_config={"symbol": "AAA"},
        backtest_curve=curve,
        metrics={"total_return": 0.0},
    )

    assert NOTE_LINE in report
    assert "- No close-to-close periods were available to review." in report


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
