from __future__ import annotations

from pathlib import Path

from market_signal_lab.scenario_card import build_scenario_card, render_scenario_card


def test_render_scenario_card_uses_public_safe_defaults_for_sparse_payload() -> None:
    markdown = render_scenario_card(
        {
            "source": {},
            "key_metrics": {},
            "diagnostics": {
                "scenario_risk_interpretation": {"research_only": True},
            },
            "assumptions": [],
            "next_review_checklist": [],
            "risk_labels": {},
        }
    )

    assert "- Research-only scenario card" in markdown
    assert "- No assumptions supplied." in markdown
    assert "- No scenario/risk interpretation was available." in markdown
    assert "- [ ] No checklist supplied." in markdown
    assert "- \n" not in markdown
    assert "not investment advice" in markdown
    assert "No broker workflow" in markdown


def test_render_scenario_card_formats_none_strings_and_numbers_in_lists() -> None:
    markdown = render_scenario_card(
        {
            "assumptions": [None, "String assumption", 7, 0.125],
            "next_review_checklist": [
                {"item": None},
                "String checklist item",
                3,
                0.5,
            ],
        }
    )

    assert "- n/a" in markdown
    assert "- String assumption" in markdown
    assert "- 7" in markdown
    assert "- 0.1250" in markdown
    assert "- [ ] n/a" in markdown
    assert "- [ ] String checklist item" in markdown
    assert "- [ ] 3" in markdown
    assert "- [ ] 0.5000" in markdown
    assert "- None" not in markdown
    assert "- [ ] None" not in markdown


def test_build_scenario_card_keeps_json_shape_and_markdown_headings() -> None:
    card = build_scenario_card(
        {
            "first_date": "2024-01-02",
            "last_date": "2024-01-11",
            "row_count": 8,
            "strategy_config": {
                "short_window": 20,
                "long_window": 50,
                "symbol": "QQQ_LIKE",
                "fee_bps": 10.0,
            },
            "metrics": {
                "total_return": 0.01,
                "buy_and_hold_total_return": 0.02,
                "strategy_minus_buy_and_hold_return": -0.01,
                "max_drawdown": -0.03,
                "volatility": 0.04,
                "sharpe_like": 0.25,
                "win_rate": 0.5,
            },
            "exposure_trade_review": {
                "average_exposure": 0.75,
                "percent_periods_in_market": 0.8,
                "exposure_changes": 2,
                "entries_to_market": 1,
                "exits_to_cash": 1,
                "total_fee_drag": -0.001,
            },
            "scenario_risk_interpretation": {
                "note": "Historical diagnostics only.",
                "exposure": {"summary": "Exposure summary."},
                "drawdown": {"summary": "Drawdown summary."},
                "fee_drag": {"summary": "Fee summary."},
                "buy_and_hold_comparison": {"summary": "Comparison summary."},
            },
        },
        Path("examples/data/sample_tqqq_qld_like.csv"),
    )

    assert set(card) == {
        "card_type",
        "schema_version",
        "research_only",
        "historical_diagnostics_only",
        "no_broker_or_live_data",
        "note",
        "source",
        "strategy_config",
        "assumptions",
        "key_metrics",
        "diagnostics",
        "risk_labels",
        "next_review_checklist",
    }
    assert card["card_type"] == "scenario_card"
    assert card["source"] == {
        "input_path": "examples/data/sample_tqqq_qld_like.csv",
        "first_date": "2024-01-02",
        "last_date": "2024-01-11",
        "row_count": 8,
    }
    assert set(card["key_metrics"]) == {
        "total_return",
        "buy_and_hold_total_return",
        "strategy_minus_buy_and_hold_return",
        "max_drawdown",
        "volatility",
        "sharpe_like",
        "win_rate",
    }
    assert set(card["diagnostics"]) == {
        "exposure",
        "fees",
        "drawdown",
        "scenario_risk_interpretation",
    }
    assert set(card["risk_labels"]) == {
        "non_advice",
        "sample_backtest_limits",
        "leveraged_etf_like",
        "scope_limits",
    }
    assert card["next_review_checklist"] == [
        {"item": item, "status": "review_required"}
        for item in (
            "Confirm input path, symbol filter, date range, and row count.",
            "Review assumptions and static fixture provenance when present.",
            "Compare key metrics with same-period buy-and-hold.",
            "Check exposure, fee drag, and max drawdown diagnostics.",
            "Re-read leveraged ETF-like daily-reset and path-dependency limits.",
        )
    ]

    heading_lines = [
        line for line in render_scenario_card(card).splitlines() if line.startswith("#")
    ]
    assert heading_lines == [
        "# Scenario Card",
        "## Source",
        "## Assumptions",
        "## Key Metrics",
        "## Diagnostics",
        "## Scenario/Risk Interpretation",
        "## Risk Labels",
        "## Next Review Checklist",
    ]
