from __future__ import annotations

from pathlib import Path

from market_signal_lab.packet import (
    build_pretrade_research_packet,
    render_pretrade_research_packet,
)


def test_pretrade_research_packet_has_stable_downstream_keys() -> None:
    packet = build_pretrade_research_packet(
        {
            "strategy_config": {"symbol": "QQQ_LIKE"},
            "metrics": {"total_return": 0.0},
            "exposure_trade_review": {"average_exposure": 0.0},
            "scenario_risk_interpretation": {"research_only": True},
            "first_date": "2024-01-02",
            "last_date": "2024-01-11",
            "row_count": 8,
        },
        input_path=Path("examples/data/sample_tqqq_qld_like.csv"),
    )

    assert set(packet) == {
        "packet_type",
        "schema_version",
        "research_only",
        "historical_diagnostics_only",
        "no_broker_or_live_data",
        "note",
        "source",
        "strategy_config",
        "assumptions",
        "historical_diagnostics",
        "beginner_checklist",
        "risk_boundaries",
    }
    assert set(packet["source"]) == {
        "input_path",
        "first_date",
        "last_date",
        "row_count",
    }
    assert set(packet["historical_diagnostics"]) == {
        "metrics",
        "exposure_trade_review",
        "scenario_risk_interpretation",
    }
    assert set(packet["beginner_checklist"][0]) == {"item", "status"}
    assert set(packet["risk_boundaries"]) == {
        "non_advice",
        "sample_backtest_limits",
        "leveraged_etf_like",
        "scope_limits",
    }
    assert "not evidence of future returns" in packet["risk_boundaries"][
        "sample_backtest_limits"
    ]


def test_render_pretrade_research_packet_preserves_zero_diagnostics() -> None:
    packet = build_pretrade_research_packet(
        {
            "metrics": {
                "total_return": 0.0,
                "buy_and_hold_total_return": 0.0,
                "strategy_minus_buy_and_hold_return": 0.0,
                "max_drawdown": 0.0,
            },
            "exposure_trade_review": {
                "average_exposure": 0.0,
                "percent_periods_in_market": 0.0,
                "exposure_changes": 0,
                "entries_to_market": 0,
                "exits_to_cash": 0,
                "total_fee_drag": 0.0,
            },
        },
        input_path=Path("zero.csv"),
    )

    markdown = render_pretrade_research_packet(packet)

    assert "- **Strategy total return**: 0.00%" in markdown
    assert "- **Buy-and-hold total return**: 0.00%" in markdown
    assert "- **Max drawdown**: 0.00%" in markdown
    assert "- **Average exposure**: 0.00%" in markdown
    assert "- **Exposure changes**: 0" in markdown
    assert "- No scenario/risk interpretation was available." in markdown
