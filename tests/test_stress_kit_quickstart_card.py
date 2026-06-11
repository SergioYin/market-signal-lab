from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from market_signal_lab.strategy_assumption_stress_kit import (
    STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
)
from market_signal_lab.stress_kit_quickstart_card import (
    QUICKSTART_BOUNDARY_CLAIMS,
    QUICKSTART_BOUNDARY_FLAGS,
    QUICKSTART_COMPLETION_RECEIPT_KEYS,
    QUICKSTART_OUT_OF_SCOPE_ITEMS,
    QUICKSTART_REVIEWER_CHECKLIST_ITEM_KEYS,
    QUICKSTART_STOP_CONDITION_KEYS,
    STRESS_KIT_QUICKSTART_CARD_COMMAND,
    STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
    STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
    STRESS_KIT_QUICKSTART_CARD_TOP_LEVEL_KEYS,
    build_stress_kit_quickstart_card,
    render_stress_kit_quickstart_card,
)


def assert_quickstart_json_fields_are_structured(payload: dict[str, object]) -> None:
    for key in QUICKSTART_BOUNDARY_FLAGS:
        assert type(payload[key]) is bool
        assert payload[key] is True

    source_artifact = payload["source_artifact"]
    assert isinstance(source_artifact, dict)
    assert isinstance(source_artifact["markdown_path"], str)
    assert source_artifact["markdown_path"].endswith(".md")
    assert isinstance(source_artifact["json_path"], str)
    assert source_artifact["json_path"].endswith(".json")

    default_outputs = payload["default_outputs"]
    assert isinstance(default_outputs, dict)
    assert isinstance(default_outputs["markdown"], str)
    assert default_outputs["markdown"].endswith(".md")
    assert isinstance(default_outputs["json"], str)
    assert default_outputs["json"].endswith(".json")

    receipt = payload["completion_receipt"]
    assert isinstance(receipt, dict)
    assert isinstance(receipt["generated_output_paths"], list)
    assert all(
        isinstance(path, str) and path.startswith("reports/")
        for path in receipt["generated_output_paths"]
    )


def test_stress_kit_quickstart_card_payload_and_markdown() -> None:
    payload = build_stress_kit_quickstart_card()
    markdown = render_stress_kit_quickstart_card(payload)

    assert tuple(payload) == STRESS_KIT_QUICKSTART_CARD_TOP_LEVEL_KEYS
    assert_quickstart_json_fields_are_structured(payload)
    assert payload["artifact_type"] == "stress_kit_quickstart_card"
    assert payload["schema_version"] == "1.0"
    assert payload["estimated_review_time_minutes"] == 2
    assert payload["default_outputs"] == {
        "markdown": STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
        "json": STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
    }
    for key in QUICKSTART_BOUNDARY_FLAGS:
        assert payload[key] is True
    assert payload["boundary_claims"] == QUICKSTART_BOUNDARY_CLAIMS
    assert "does not fetch, stream, refresh, or inspect live market data" in (
        payload["boundary_claims"]["no_live_data"]
    )
    assert "not a forecast, recommendation, trading instruction" in (
        payload["boundary_claims"]["not_investment_advice"]
    )
    assert (
        payload["source_artifact"]["markdown_path"]
        == STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH
    )
    assert (
        tuple(payload["reviewer_checklist"][0])
        == QUICKSTART_REVIEWER_CHECKLIST_ITEM_KEYS
    )
    assert [item["step"] for item in payload["reviewer_checklist"]] == [
        "scope",
        "assumptions",
        "stress_language",
        "leveraged_etf_like_caveats",
        "boundaries",
    ]
    assert tuple(payload["stop_conditions"][0]) == QUICKSTART_STOP_CONDITION_KEYS
    assert tuple(payload["completion_receipt"]) == QUICKSTART_COMPLETION_RECEIPT_KEYS
    assert payload["completion_receipt"]["source_command"] == (
        STRESS_KIT_QUICKSTART_CARD_COMMAND
    )
    assert payload["completion_receipt"]["generated_output_paths"] == [
        STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
        STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
    ]
    assert payload["do_not_use_for"] == list(QUICKSTART_OUT_OF_SCOPE_ITEMS)
    assert "forecast or recommendation surface" in payload["do_not_use_for"]
    assert "investment-advice surface" in payload["do_not_use_for"]
    assert "# Stress Kit Quickstart Card" in markdown
    assert "## Two-Minute Reviewer Checklist" in markdown
    assert "| 0:00-0:20 | scope |" in markdown
    assert "daily reset, path dependency, volatility drag" in markdown
    assert "extreme drawdown caveats" in markdown
    assert "simplified historical diagnostics, not advice" in markdown
    assert "## Stop Conditions" in markdown
    assert "`reports/stress-kit-quickstart-card.md`" in markdown
    assert "`reports/stress-kit-quickstart-card.json`" in markdown
    assert "not validate financial correctness" in markdown
    assert "no_live_data: `True`" in markdown
    assert "not_investment_advice: `True`" in markdown
    assert "## Boundary Claims" in markdown
    assert "does not fetch, stream, refresh, or inspect live market data" in markdown
    assert "not a forecast, recommendation, trading instruction" in markdown


def test_stress_kit_quickstart_card_builds_fresh_nested_objects() -> None:
    payload = build_stress_kit_quickstart_card()
    payload["reviewer_checklist"][0]["unexpected_field"] = "extra"
    payload["stop_conditions"][0]["unexpected_field"] = "extra"
    payload["completion_receipt"]["generated_output_paths"].append("extra")

    fresh_payload = build_stress_kit_quickstart_card()

    assert (
        tuple(fresh_payload["reviewer_checklist"][0])
        == QUICKSTART_REVIEWER_CHECKLIST_ITEM_KEYS
    )
    assert (
        tuple(fresh_payload["stop_conditions"][0])
        == QUICKSTART_STOP_CONDITION_KEYS
    )
    assert fresh_payload["completion_receipt"]["generated_output_paths"] == [
        STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
        STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
    ]


def test_cli_writes_stress_kit_quickstart_card_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--stress-kit-quickstart-card",
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
    markdown_path = tmp_path / "reports" / "stress-kit-quickstart-card.md"
    json_path = tmp_path / "reports" / "stress-kit-quickstart-card.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert_quickstart_json_fields_are_structured(payload)
    assert "# Stress Kit Quickstart Card" in markdown
    assert "Two-Minute Reviewer Checklist" in markdown
    assert payload["artifact_type"] == "stress_kit_quickstart_card"
    assert payload["no_live_data"] is True
    assert payload["not_investment_advice"] is True
    assert "does not fetch, stream, refresh, or inspect live market data" in (
        payload["boundary_claims"]["no_live_data"]
    )
    assert "not a forecast, recommendation, trading instruction" in (
        payload["boundary_claims"]["not_investment_advice"]
    )


def test_cli_help_surfaces_stress_kit_quickstart_reviewer_route() -> None:
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
    help_text = " ".join(result.stdout.split())
    assert "--stress-kit-quickstart-card" in help_text
    assert "shortest reviewer entry point" in help_text
    assert "open the Markdown output first" in help_text
    assert "reports/stress-kit-" in result.stdout
    assert "quickstart-card.md" in result.stdout
    assert "provide investment advice" in help_text
    assert result.stderr == ""


def test_cli_rejects_combined_static_review_routes() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--reviewer-acceptance-scorecard",
            "--stress-kit-quickstart-card",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        "--reviewer-acceptance-scorecard cannot be combined with "
        "--stress-kit-quickstart-card"
    ) in result.stderr


def test_cli_writes_stress_kit_quickstart_card_custom_outputs(
    tmp_path: Path,
) -> None:
    markdown_path = tmp_path / "custom" / "quickstart.md"
    json_path = tmp_path / "custom" / "quickstart.json"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--stress-kit-quickstart-card",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
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
    assert "# Stress Kit Quickstart Card" in markdown_path.read_text(
        encoding="utf-8"
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert_quickstart_json_fields_are_structured(payload)
    assert payload["artifact_type"] == "stress_kit_quickstart_card"
    assert payload["research_only"] is True
    assert payload["static_only"] is True
    assert payload["no_live_data"] is True
    assert payload["not_investment_advice"] is True
    assert not (tmp_path / "reports" / "stress-kit-quickstart-card.md").exists()
    assert not (tmp_path / "reports" / "stress-kit-quickstart-card.json").exists()
