from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from market_signal_lab.thesis_ledger import (
    THESIS_LEDGER_SYMBOLS,
    build_cross_asset_thesis_ledger,
    render_cross_asset_thesis_ledger,
    render_thesis_ledger_acceptance_summary,
    validate_cross_asset_thesis_ledger_packet,
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


def test_validate_cross_asset_thesis_ledger_accepts_valid_packet() -> None:
    packet = build_cross_asset_thesis_ledger(SAMPLE_DATA)

    summary = validate_cross_asset_thesis_ledger_packet(packet)
    markdown = render_thesis_ledger_acceptance_summary(summary)

    assert summary["summary_type"] == "cross_asset_thesis_ledger_acceptance"
    assert summary["accepted"] is True
    assert summary["error_count"] == 0
    assert summary["asset_symbols"] == list(THESIS_LEDGER_SYMBOLS)
    assert summary["research_only"] is True
    assert summary["offline_only"] is True
    assert "not investment advice" in summary["note"]
    assert "# Thesis-Ledger Acceptance Summary" in markdown
    assert "- **Accepted**: True" in markdown
    assert "does not fetch live data" in markdown


def test_validate_cross_asset_thesis_ledger_rejects_missing_risk_boundaries() -> None:
    packet = build_cross_asset_thesis_ledger(SAMPLE_DATA)
    del packet["risk_boundaries"]

    summary = validate_cross_asset_thesis_ledger_packet(packet)

    assert summary["accepted"] is False
    assert summary["error_count"] >= 1
    messages = " ".join(check["message"] for check in summary["checks"])
    assert "Missing top-level key(s): risk_boundaries" in messages
    assert "Risk boundaries must include" in messages


def test_validate_cross_asset_thesis_ledger_rejects_bad_asset_shape() -> None:
    packet = build_cross_asset_thesis_ledger(SAMPLE_DATA)
    packet["assets"] = deepcopy(packet["assets"])
    packet["assets"][0]["metrics"] = {"total_return": "1.0"}

    summary = validate_cross_asset_thesis_ledger_packet(packet)

    assert summary["accepted"] is False
    failed_checks = {
        check["check"]
        for check in summary["checks"]
        if check["accepted"] is False
    }
    assert "asset.QQQ_LIKE.metrics" in failed_checks


def test_validate_cross_asset_thesis_ledger_handles_non_object_packet() -> None:
    summary = validate_cross_asset_thesis_ledger_packet(["not", "an", "object"])

    assert summary["accepted"] is False
    assert summary["error_count"] == 1
    assert summary["checks"][0]["check"] == "packet_object"
