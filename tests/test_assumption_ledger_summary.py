from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from market_signal_lab.assumption_ledger_summary import (
    ASSUMPTION_ITEM_KEYS,
    ASSUMPTION_LEDGER_SUMMARY_TOP_LEVEL_KEYS,
    BOUNDARY_CLAIMS,
    BOUNDARY_FLAGS,
    EVIDENCE_PATH_KEYS,
    NOT_CLAIMED_KEYS,
    RISK_BOUNDARY_KEYS,
    build_assumption_ledger_summary,
    render_assumption_ledger_summary,
)


def test_assumption_ledger_summary_payload_and_markdown() -> None:
    payload = build_assumption_ledger_summary()
    markdown = render_assumption_ledger_summary(payload)

    assert tuple(payload) == ASSUMPTION_LEDGER_SUMMARY_TOP_LEVEL_KEYS
    assert payload["artifact_type"] == "assumption_ledger_summary"
    assert payload["schema_version"] == "1.0"
    assert payload["default_outputs"] == {
        "markdown": "reports/assumption-ledger-summary.md",
        "json": "reports/assumption-ledger-summary.json",
    }
    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert payload["boundary_claims"] == BOUNDARY_CLAIMS
    assert "does not fetch, stream, refresh, or inspect live market data" in (
        payload["boundary_claims"]["no_live_data"]
    )
    assert "not a forecast, recommendation, trading instruction" in (
        payload["boundary_claims"]["not_investment_advice"]
    )
    assert tuple(payload["strategy_assumptions"][0]) == ASSUMPTION_ITEM_KEYS
    assert tuple(payload["risk_boundaries"][0]) == RISK_BOUNDARY_KEYS
    assert tuple(payload["generated_evidence_paths"][0]) == EVIDENCE_PATH_KEYS
    assert tuple(payload["not_claimed"][0]) == NOT_CLAIMED_KEYS
    assert {item["claim"] for item in payload["not_claimed"]} == {
        "future_performance",
        "tradability_or_execution",
        "position_size_or_suitability",
        "recommendation_or_advice",
    }
    assert "reports/strategy-assumption-stress-kit.html" in {
        item["path"] for item in payload["generated_evidence_paths"]
    }
    assert "# Assumption Ledger Summary" in markdown
    assert "## Strategy Assumptions" in markdown
    assert "## Risk Boundaries" in markdown
    assert "## Generated Evidence Paths" in markdown
    assert "## What Is Not Being Claimed" in markdown
    assert (
        "[`reports/assumption-ledger-summary.md`](assumption-ledger-summary.md)"
        in markdown
    )
    assert (
        "[`reports/assumption-ledger-summary.json`](assumption-ledger-summary.json)"
        in markdown
    )
    assert "map of the artifact's assumptions and limits" in markdown
    assert "not as a verdict on strategy quality or suitability" in markdown
    assert "no_live_data: `True`" in markdown
    assert "no_broker_or_account: `True`" in markdown
    assert "no_orders_or_position_sizing: `True`" in markdown
    assert "no_recommendations_or_forecasts: `True`" in markdown
    assert "not_investment_advice: `True`" in markdown
    assert "## Boundary Claims" in markdown
    assert "does not fetch, stream, refresh, or inspect live market data" in markdown
    assert "not a forecast, recommendation, trading instruction" in markdown
    assert "does not tell a reader what to buy, sell, hold, size, or trade" in markdown


def test_assumption_ledger_summary_builds_fresh_nested_objects() -> None:
    payload = build_assumption_ledger_summary()
    payload["strategy_assumptions"][0]["unexpected_field"] = "extra"
    payload["risk_boundaries"][0]["unexpected_field"] = "extra"
    payload["generated_evidence_paths"][0]["unexpected_field"] = "extra"
    payload["not_claimed"][0]["unexpected_field"] = "extra"

    fresh_payload = build_assumption_ledger_summary()

    assert tuple(fresh_payload["strategy_assumptions"][0]) == ASSUMPTION_ITEM_KEYS
    assert tuple(fresh_payload["risk_boundaries"][0]) == RISK_BOUNDARY_KEYS
    assert tuple(fresh_payload["generated_evidence_paths"][0]) == EVIDENCE_PATH_KEYS
    assert tuple(fresh_payload["not_claimed"][0]) == NOT_CLAIMED_KEYS


def test_cli_writes_assumption_ledger_summary_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--assumption-ledger-summary",
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    markdown_path = tmp_path / "reports" / "assumption-ledger-summary.md"
    json_path = tmp_path / "reports" / "assumption-ledger-summary.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Assumption Ledger Summary" in markdown
    assert "What Is Not Being Claimed" in markdown
    assert "generated static evidence, not as financial validation" in markdown
    assert payload["artifact_type"] == "assumption_ledger_summary"
    assert payload["no_live_data"] is True
    assert payload["no_broker_or_account"] is True
    assert payload["no_orders_or_position_sizing"] is True
    assert payload["no_recommendations_or_forecasts"] is True
    assert payload["not_investment_advice"] is True


def test_cli_help_surfaces_assumption_ledger_summary() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--help",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    help_text = " ".join(result.stdout.replace("-\n", "-").split())
    assert "--assumption-ledger-summary" in help_text
    assert "static assumption ledger summary for cold reviewers" in help_text
    assert "reports/assumption-" in result.stdout
    assert "ledger-summary.md" in result.stdout
    assert "summary.json" in result.stdout


def test_cli_assumption_ledger_summary_accepts_custom_outputs(
    tmp_path: Path,
) -> None:
    markdown_path = tmp_path / "ledger.md"
    json_path = tmp_path / "ledger.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--assumption-ledger-summary",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert "# Assumption Ledger Summary" in markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["artifact_type"] == "assumption_ledger_summary"
