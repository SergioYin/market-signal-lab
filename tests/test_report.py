from datetime import date

from market_signal_lab.backtest import EquityCurveRecord
from market_signal_lab.report import (
    EXPOSURE_TRADE_REVIEW_NOTE,
    SCENARIO_RISK_COMPARISON_KEYS,
    SCENARIO_RISK_DRAWDOWN_KEYS,
    SCENARIO_RISK_EXPOSURE_KEYS,
    SCENARIO_RISK_FEE_DRAG_KEYS,
    SCENARIO_RISK_INTERPRETATION_KEYS,
    SCENARIO_RISK_INTERPRETATION_NOTE,
    build_exposure_trade_review,
    build_scenario_risk_interpretation,
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
    assert "## Scenario/Risk Interpretation" in report
    assert NOTE_LINE in report
    assert f"- {SCENARIO_RISK_INTERPRETATION_NOTE}" in report
    assert "- **Exposure**: The model was exposed to the market for 100.00%" in report
    assert "- **Drawdown**: The worst modeled peak-to-trough decline" in report
    assert "- **Fee drag**: Modeled fee drag summed to 0.00%" in report
    assert (
        "- **Buy-and-hold comparison**: Strategy minus buy-and-hold was 5.00% "
        "over the same period."
    ) in report
    assert "- **Periods in market**: 1 of 1 close-to-close periods (100.00%)." in report
    assert "- **Exposure changes**: 1." in report
    assert "- **Modeled entries**: 1." in report
    assert "- **Modeled exits**: 0." in report
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


def test_build_scenario_risk_interpretation_summarizes_research_diagnostics() -> None:
    interpretation = build_scenario_risk_interpretation(
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
                equity=1.1,
                exposure=1.0,
                market_return=0.05,
                strategy_return=0.099,
                fee=0.001,
            ),
            EquityCurveRecord(
                date=date(2024, 1, 3),
                equity=1.045,
                exposure=0.0,
                market_return=-0.02,
                strategy_return=-0.05,
                fee=0.001,
            ),
        ],
        {
            "total_return": 0.045,
            "buy_and_hold_total_return": 0.029,
            "strategy_minus_buy_and_hold_return": 0.016,
            "max_drawdown": -0.05,
        },
    )

    assert set(interpretation) == SCENARIO_RISK_INTERPRETATION_KEYS
    assert interpretation["research_only"] is True
    assert interpretation["historical_diagnostics_only"] is True
    assert interpretation["note"] == SCENARIO_RISK_INTERPRETATION_NOTE
    assert set(interpretation["exposure"]) == SCENARIO_RISK_EXPOSURE_KEYS
    assert interpretation["exposure"]["period_count"] == 2
    assert interpretation["exposure"]["average_exposure"] == 0.5
    assert interpretation["exposure"]["percent_periods_in_market"] == 0.5
    assert "Higher exposure" in interpretation["exposure"]["summary"]
    assert set(interpretation["drawdown"]) == SCENARIO_RISK_DRAWDOWN_KEYS
    assert interpretation["drawdown"]["max_drawdown"] == -0.05
    assert "larger interim losses" in interpretation["drawdown"]["summary"]
    assert set(interpretation["fee_drag"]) == SCENARIO_RISK_FEE_DRAG_KEYS
    assert interpretation["fee_drag"]["total_fee_drag"] == 0.002
    assert "not a complete estimate" in interpretation["fee_drag"]["summary"]
    comparison = interpretation["buy_and_hold_comparison"]
    assert set(comparison) == SCENARIO_RISK_COMPARISON_KEYS
    assert comparison["strategy_total_return"] == 0.045
    assert comparison["buy_and_hold_total_return"] == 0.029
    assert comparison["strategy_minus_buy_and_hold_return"] == 0.016
    assert "same period" in comparison["summary"]


def test_scenario_risk_report_labels_stay_clear_and_public_safe() -> None:
    report = render_experiment_report(
        strategy_config={"symbol": "AAA"},
        backtest_curve=_curve(),
        metrics={
            "total_return": 0.10,
            "buy_and_hold_total_return": 0.05,
            "strategy_minus_buy_and_hold_return": 0.05,
            "max_drawdown": -0.02,
        },
    )

    assert "## Scenario/Risk Interpretation" in report
    assert f"- {SCENARIO_RISK_INTERPRETATION_NOTE}" in report
    assert "- **Exposure**:" in report
    assert "- **Drawdown**:" in report
    assert "- **Fee drag**:" in report
    assert "- **Buy-and-hold comparison**:" in report
    assert "not investment advice" in report
    assert "a prediction" in report
    assert "broker connection or execution feature" in report


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
    assert "- **Modeled entries**: 0." in report
    assert "- **Modeled exits**: 0." in report


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
