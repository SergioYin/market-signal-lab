from __future__ import annotations

from pathlib import Path

from market_signal_lab.thesis_ledger import (
    THESIS_LEDGER_SYMBOLS,
    build_cross_asset_thesis_ledger,
    render_cross_asset_thesis_ledger,
)


SAMPLE_DATA = Path("examples/data/sample_tqqq_qld_like.csv")


def test_cross_asset_thesis_ledger_has_stable_shape() -> None:
    packet = build_cross_asset_thesis_ledger(SAMPLE_DATA)

    assert set(packet) == {
        "packet_type",
        "schema_version",
        "research_only",
        "historical_diagnostics_only",
        "offline_only",
        "no_broker_or_live_data",
        "note",
        "source",
        "strategy_config",
        "assumptions",
        "assets",
        "cross_asset_evidence",
        "risk_boundaries",
        "data_provenance",
    }
    assert packet["packet_type"] == "cross_asset_thesis_ledger_evidence_packet"
    assert packet["research_only"] is True
    assert packet["offline_only"] is True
    assert packet["no_broker_or_live_data"] is True
    assert packet["source"]["symbols"] == list(THESIS_LEDGER_SYMBOLS)
    assert packet["source"]["rows_per_symbol"] == {
        "QLD_LIKE": 8,
        "QQQ_LIKE": 8,
        "TQQQ_LIKE": 8,
    }
    assert packet["strategy_config"] == {
        "short_window": 2,
        "long_window": 3,
        "fee_bps": 10.0,
    }
    assert [asset["symbol"] for asset in packet["assets"]] == list(
        THESIS_LEDGER_SYMBOLS
    )

    for asset in packet["assets"]:
        assert set(asset) == {
            "symbol",
            "source",
            "strategy_config",
            "metrics",
            "exposure_trade_review",
            "scenario_risk_interpretation",
            "scenario_card",
            "scenario_card_markdown",
        }
        assert asset["scenario_card"]["card_type"] == "scenario_card"
        assert "# Scenario Card" in asset["scenario_card_markdown"]
        assert asset["exposure_trade_review"]["research_only"] is True
        assert asset["scenario_risk_interpretation"]["research_only"] is True


def test_render_cross_asset_thesis_ledger_includes_public_boundaries() -> None:
    packet = build_cross_asset_thesis_ledger(SAMPLE_DATA)
    markdown = render_cross_asset_thesis_ledger(packet)

    assert "# Cross-Asset Thesis-Ledger Evidence Packet" in markdown
    assert "## Cross-Asset Evidence" in markdown
    assert "QQQ_LIKE" in markdown
    assert "QLD_LIKE" in markdown
    assert "TQQQ_LIKE" in markdown
    assert "Embedded Scenario Cards" in markdown
    assert "not investment advice" in markdown
    assert "not a recommendation" in markdown
    assert "no live data" in markdown.lower()
    assert "broker workflow" in markdown
    assert "will outperform" not in markdown
