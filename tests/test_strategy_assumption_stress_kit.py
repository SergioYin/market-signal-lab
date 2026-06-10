from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from market_signal_lab.strategy_assumption_stress_kit import (
    ASSUMPTION_GROUP_KEYS,
    BEGINNER_RISK_BOUNDARY_KEYS,
    BOUNDARY_FLAGS,
    HYPOTHETICAL_STRESS_REVIEW_OUTCOME_ITEM_KEYS,
    HYPOTHETICAL_STRESS_REVIEW_OUTCOME_KEYS,
    LEVERAGED_ETF_LIKE_CAVEAT_KEYS,
    RELEASE_READINESS_BOUNDARY_CLAIM_KEYS,
    RELEASE_READINESS_OUTPUT_PATH_KEYS,
    RELEASE_READINESS_RECEIPT_KEYS,
    RELEASE_READINESS_RERUN_COMMAND_KEYS,
    STRATEGY_ASSUMPTION_STRESS_KIT_TOP_LEVEL_KEYS,
    STRESS_CHECK_KEYS,
    build_strategy_assumption_stress_kit,
    render_strategy_assumption_stress_kit,
)


def test_strategy_assumption_stress_kit_payload_and_markdown() -> None:
    payload = build_strategy_assumption_stress_kit()
    markdown = render_strategy_assumption_stress_kit(payload)

    assert tuple(payload) == STRATEGY_ASSUMPTION_STRESS_KIT_TOP_LEVEL_KEYS
    assert payload["artifact_type"] == "strategy_assumption_stress_kit"
    assert payload["schema_version"] == "1.0"
    assert payload["default_outputs"] == {
        "markdown": "reports/strategy-assumption-stress-kit.md",
        "json": "reports/strategy-assumption-stress-kit.json",
    }
    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert tuple(payload["assumption_groups"][0]) == ASSUMPTION_GROUP_KEYS
    assert tuple(payload["stress_checks"][0]) == STRESS_CHECK_KEYS
    assert (
        tuple(payload["hypothetical_stress_review_outcome"])
        == HYPOTHETICAL_STRESS_REVIEW_OUTCOME_KEYS
    )
    assert (
        tuple(payload["hypothetical_stress_review_outcome"]["items"][0])
        == HYPOTHETICAL_STRESS_REVIEW_OUTCOME_ITEM_KEYS
    )
    assert payload["hypothetical_stress_review_outcome"]["overall_label"] == "WARN"
    assert [
        item["label"]
        for item in payload["hypothetical_stress_review_outcome"]["items"]
    ] == ["PASS", "WARN"]
    fixture_text = json.dumps(
        payload["hypothetical_stress_review_outcome"],
        sort_keys=True,
    ).lower()
    assert "return" not in fixture_text
    assert "recommend" not in fixture_text
    assert (
        tuple(payload["beginner_risk_boundaries"][0])
        == BEGINNER_RISK_BOUNDARY_KEYS
    )
    assert (
        tuple(payload["leveraged_etf_like_caveats"][0])
        == LEVERAGED_ETF_LIKE_CAVEAT_KEYS
    )
    receipt = payload["release_readiness_receipt"]
    assert tuple(receipt) == RELEASE_READINESS_RECEIPT_KEYS
    assert (
        receipt["receipt_type"]
        == "strategy_assumption_stress_kit_release_readiness"
    )
    assert tuple(receipt["rerun_commands"][0]) == RELEASE_READINESS_RERUN_COMMAND_KEYS
    assert (
        receipt["rerun_commands"][0]["command"]
        == "python -m market_signal_lab.cli --strategy-assumption-stress-kit"
    )
    assert receipt["rerun_commands"][0]["generated_output_paths"] == [
        "reports/strategy-assumption-stress-kit.html",
        "reports/strategy-assumption-stress-kit.md",
        "reports/strategy-assumption-stress-kit.json",
    ]
    assert (
        tuple(receipt["generated_output_paths"][0])
        == RELEASE_READINESS_OUTPUT_PATH_KEYS
    )
    assert [
        item["path"] for item in receipt["generated_output_paths"]
    ] == [
        "reports/strategy-assumption-stress-kit.html",
        "reports/strategy-assumption-stress-kit.md",
        "reports/strategy-assumption-stress-kit.json",
    ]
    assert (
        tuple(receipt["boundary_claims"][0])
        == RELEASE_READINESS_BOUNDARY_CLAIM_KEYS
    )
    assert {item["claim"] for item in receipt["boundary_claims"]} == {
        "no_live_data",
        "no_broker_or_account",
        "no_orders_or_position_sizing",
        "no_recommendations_or_forecasts",
        "not_investment_advice",
    }
    assert all(item["status"] == "PASS" for item in receipt["boundary_claims"])
    assert "# Strategy Assumption Stress Kit" in markdown
    assert "## Assumptions To Stress" in markdown
    assert "## Stress Checks" in markdown
    assert "## Hypothetical Stress Review Outcome" in markdown
    assert "`hypothetical_static_review_001`" in markdown
    assert "| PASS | window_sensitivity |" in markdown
    assert "| WARN | fee_drag_visibility |" in markdown
    assert "## Beginner Risk Boundaries" in markdown
    assert "## Leveraged ETF-Like Caveats" in markdown
    assert "## Release-Readiness Receipt" in markdown
    assert "### Exact Rerun Commands" in markdown
    assert "### Generated Output Paths" in markdown
    assert "### No-Live-Data / No-Advice Boundaries" in markdown
    assert "`reports/strategy-assumption-stress-kit.html`" in markdown
    assert "`reports/strategy-assumption-stress-kit.md`" in markdown
    assert "`reports/strategy-assumption-stress-kit.json`" in markdown
    assert "**PASS no_live_data**" in markdown
    assert "does not prove financial correctness" in markdown
    assert "path dependency, volatility drag, and extreme drawdown caveats" in markdown
    assert "as a prediction, recommendation, trading instruction" in markdown
    assert "live market data" in markdown


def test_strategy_assumption_stress_kit_builds_fresh_nested_objects() -> None:
    payload = build_strategy_assumption_stress_kit()
    payload["assumption_groups"][0]["unexpected_field"] = "extra"
    payload["stress_checks"][0]["unexpected_field"] = "extra"
    payload["hypothetical_stress_review_outcome"]["items"][0][
        "unexpected_field"
    ] = "extra"
    payload["beginner_risk_boundaries"][0]["unexpected_field"] = "extra"
    payload["leveraged_etf_like_caveats"][0]["unexpected_field"] = "extra"
    payload["release_readiness_receipt"]["rerun_commands"][0][
        "unexpected_field"
    ] = "extra"
    payload["release_readiness_receipt"]["generated_output_paths"][0][
        "unexpected_field"
    ] = "extra"
    payload["release_readiness_receipt"]["boundary_claims"][0][
        "unexpected_field"
    ] = "extra"

    fresh_payload = build_strategy_assumption_stress_kit()

    assert tuple(fresh_payload["assumption_groups"][0]) == ASSUMPTION_GROUP_KEYS
    assert tuple(fresh_payload["stress_checks"][0]) == STRESS_CHECK_KEYS
    assert (
        tuple(fresh_payload["hypothetical_stress_review_outcome"])
        == HYPOTHETICAL_STRESS_REVIEW_OUTCOME_KEYS
    )
    assert (
        tuple(fresh_payload["hypothetical_stress_review_outcome"]["items"][0])
        == HYPOTHETICAL_STRESS_REVIEW_OUTCOME_ITEM_KEYS
    )
    assert (
        tuple(fresh_payload["beginner_risk_boundaries"][0])
        == BEGINNER_RISK_BOUNDARY_KEYS
    )
    assert (
        tuple(fresh_payload["leveraged_etf_like_caveats"][0])
        == LEVERAGED_ETF_LIKE_CAVEAT_KEYS
    )
    receipt = fresh_payload["release_readiness_receipt"]
    assert tuple(receipt) == RELEASE_READINESS_RECEIPT_KEYS
    assert tuple(receipt["rerun_commands"][0]) == RELEASE_READINESS_RERUN_COMMAND_KEYS
    assert (
        tuple(receipt["generated_output_paths"][0])
        == RELEASE_READINESS_OUTPUT_PATH_KEYS
    )
    assert (
        tuple(receipt["boundary_claims"][0])
        == RELEASE_READINESS_BOUNDARY_CLAIM_KEYS
    )


def test_cli_writes_strategy_assumption_stress_kit_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--strategy-assumption-stress-kit",
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
    markdown_path = tmp_path / "reports" / "strategy-assumption-stress-kit.md"
    json_path = tmp_path / "reports" / "strategy-assumption-stress-kit.json"
    html_path = tmp_path / "reports" / "strategy-assumption-stress-kit.html"
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    html = html_path.read_text(encoding="utf-8")
    assert "# Strategy Assumption Stress Kit" in markdown
    assert "Hypothetical Stress Review Outcome" in markdown
    assert "volatility_drag" in markdown
    assert "<title>Strategy Assumption Stress Kit - Market Signal Lab</title>" in html
    assert "Related Artifacts" in html
    assert "Hypothetical Stress Review Outcome" in html
    assert "Release-Readiness Receipt" in html
    assert 'href="strategy-assumption-stress-kit.md"' in html
    assert 'href="strategy-assumption-stress-kit.json"' in html
    assert "not investment advice" in html
    assert payload["artifact_type"] == "strategy_assumption_stress_kit"
    assert payload["no_live_data"] is True
    assert payload["no_broker_or_account"] is True
    assert payload["no_orders_or_position_sizing"] is True
    assert payload["no_recommendations_or_forecasts"] is True
    assert payload["hypothetical_stress_review_outcome"]["overall_label"] == "WARN"
    assert (
        payload["release_readiness_receipt"]["rerun_commands"][0]["command"]
        == "python -m market_signal_lab.cli --strategy-assumption-stress-kit"
    )


def test_cli_strategy_assumption_stress_kit_accepts_custom_outputs(
    tmp_path: Path,
) -> None:
    markdown_path = tmp_path / "stress-kit.md"
    json_path = tmp_path / "stress-kit.json"
    html_path = tmp_path / "stress-kit.html"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--strategy-assumption-stress-kit",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
            "--html-output",
            str(html_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert "# Strategy Assumption Stress Kit" in markdown_path.read_text(
        encoding="utf-8"
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["artifact_type"] == "strategy_assumption_stress_kit"
    assert payload["hypothetical_stress_review_outcome"]["items"][1]["label"] == "WARN"
    html = html_path.read_text(encoding="utf-8")
    assert "Strategy Assumption Stress Kit - Market Signal Lab" in html
    assert "hypothetical_static_review_001" in html
    assert "Release-Readiness Receipt" in html
    assert 'href="stress-kit.md"' in html
    assert 'href="stress-kit.json"' in html
    assert "no_live_data" in html


def test_cli_strategy_assumption_stress_kit_custom_markdown_does_not_write_default_html(
    tmp_path: Path,
) -> None:
    markdown_path = tmp_path / "stress-kit.md"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--strategy-assumption-stress-kit",
            "--output",
            str(markdown_path),
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
    assert "# Strategy Assumption Stress Kit" in markdown_path.read_text(
        encoding="utf-8"
    )
    assert not (tmp_path / "reports" / "strategy-assumption-stress-kit.html").exists()
    assert not (tmp_path / "reports" / "strategy-assumption-stress-kit.json").exists()


def test_cli_strategy_assumption_stress_kit_custom_html_preserves_default_data_outputs(
    tmp_path: Path,
) -> None:
    html_path = tmp_path / "stress-kit.html"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--strategy-assumption-stress-kit",
            "--html-output",
            str(html_path),
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
    assert html_path.is_file()
    assert (tmp_path / "reports" / "strategy-assumption-stress-kit.md").is_file()
    assert (tmp_path / "reports" / "strategy-assumption-stress-kit.json").is_file()
    html = html_path.read_text(encoding="utf-8")
    assert 'href="reports/strategy-assumption-stress-kit.md"' in html
    assert 'href="reports/strategy-assumption-stress-kit.json"' in html


def test_cli_strategy_assumption_stress_kit_help_describes_boundaries() -> None:
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
    assert "--strategy-assumption-stress-kit" in help_text
    assert "leveraged ETF-like path dependency" in help_text
    assert "Does not read CSV data" in help_text
    assert "use strategy parameters" in help_text


@pytest.mark.parametrize(
    ("extra_args", "flag"),
    [
        (["--sweep"], "--sweep"),
        (["--short-window", "10"], "--short-window"),
        (["--long-window", "50"], "--long-window"),
        (["--fee-bps", "5"], "--fee-bps"),
        (["--split-ratio", "0.7"], "--split-ratio"),
    ],
)
def test_cli_strategy_assumption_stress_kit_rejects_strategy_execution_flags(
    extra_args: list[str],
    flag: str,
) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--strategy-assumption-stress-kit",
            *extra_args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        f"--strategy-assumption-stress-kit cannot be combined with {flag}"
        in result.stderr
    )


@pytest.mark.parametrize(
    ("extra_args", "message"),
    [
        (
            ["examples/data/sample_tqqq_qld_like.csv"],
            "--strategy-assumption-stress-kit does not take csv_path",
        ),
        (
            ["--config", "examples/configs/single-backtest-report.json"],
            "--strategy-assumption-stress-kit does not take --config",
        ),
        (
            ["--manifest-output", "manifest.md"],
            "--strategy-assumption-stress-kit does not write experiment manifests",
        ),
        (
            ["--symbol", "QQQ_LIKE"],
            "--strategy-assumption-stress-kit cannot be combined with --symbol",
        ),
        (
            ["--prediction-readiness-audit"],
            (
                "--prediction-readiness-audit cannot be combined with "
                "--strategy-assumption-stress-kit"
            ),
        ),
    ],
)
def test_cli_strategy_assumption_stress_kit_rejects_incompatible_options(
    extra_args: list[str],
    message: str,
) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--strategy-assumption-stress-kit",
            *extra_args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert message in result.stderr
