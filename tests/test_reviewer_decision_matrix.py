from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from market_signal_lab.reviewer_decision_matrix import (
    REVIEWER_DECISION_MATRIX_CATEGORY_KEYS,
    REVIEWER_DECISION_MATRIX_SUMMARY_KEYS,
    REVIEWER_DECISION_MATRIX_GATES_READING_KEYS,
    REVIEWER_DECISION_MATRIX_TOP_LEVEL_KEYS,
    REVIEWER_DECISION_MATRIX_RELEASE_GATE_KEY,
    REVIEWER_DECISION_MATRIX_PROMOTION_GATE_KEY,
    REVIEWER_DECISION_MATRIX_PUBLIC_BOUNDARIES,
    REVIEWER_DECISION_MATRIX_VERIFICATION_COMMANDS,
    GATE_RESULT_OPTIONS,
    build_reviewer_decision_matrix,
    render_reviewer_decision_matrix,
)


SAMPLE_DATA = Path("examples/data/sample_tqqq_qld_like.csv")
SAMPLE_CONFIG = Path("examples/configs/single-backtest-report.json")


def test_reviewer_decision_matrix_builder_and_render() -> None:
    payload = build_reviewer_decision_matrix()
    markdown = render_reviewer_decision_matrix(payload)

    assert tuple(payload) == REVIEWER_DECISION_MATRIX_TOP_LEVEL_KEYS
    assert payload["artifact_type"] == "reviewer_decision_matrix"
    assert payload["schema_version"] == "1.0"
    summary = payload["summary"]
    assert tuple(summary) == REVIEWER_DECISION_MATRIX_SUMMARY_KEYS
    assert summary[REVIEWER_DECISION_MATRIX_RELEASE_GATE_KEY] in GATE_RESULT_OPTIONS
    assert summary[REVIEWER_DECISION_MATRIX_PROMOTION_GATE_KEY] in GATE_RESULT_OPTIONS
    gates_reading = payload["gates_reading"]
    assert tuple(gates_reading) == REVIEWER_DECISION_MATRIX_GATES_READING_KEYS
    assert isinstance(gates_reading["disclaimer"], list)
    assert len(gates_reading["disclaimer"]) == 2
    categories = payload["decision_categories"]
    assert len(categories) == 8
    assert payload["verification_commands"] == list(REVIEWER_DECISION_MATRIX_VERIFICATION_COMMANDS)
    assert all(
        tuple(category) == REVIEWER_DECISION_MATRIX_CATEGORY_KEYS
        for category in categories
    )
    assert summary["pass_count"] + summary["warn_count"] + summary["fail_count"] == len(categories)
    assert "How to Read the Gates" in markdown
    assert "Release Gate" in markdown
    assert "Promotion Gate" in markdown
    assert "A Release Gate PASS/WARN result is not a buy/sell signal." in markdown
    assert "Promotion Gate is about public demo quality, not proof of strategy profitability." in markdown
    assert "## Decision Criteria" in markdown
    assert payload["public_boundaries"] == list(REVIEWER_DECISION_MATRIX_PUBLIC_BOUNDARIES)
    assert "does not provide investment advice" in markdown
    assert "buy/sell/hold signals" in markdown
    assert "future performance" in markdown
    assert "Daily reset mechanics make multi-day outcomes path-dependent" in markdown


def test_reviewer_decision_matrix_json_matches_builder_output() -> None:
    expected = json.loads(Path("reports/reviewer-decision-matrix.json").read_text())
    actual = build_reviewer_decision_matrix()
    assert actual == expected


def test_reviewer_decision_matrix_markdown_matches_renderer_output() -> None:
    expected = Path("reports/reviewer-decision-matrix.md").read_text(
        encoding="utf-8"
    )
    actual = render_reviewer_decision_matrix(build_reviewer_decision_matrix())
    assert actual == expected


def test_cli_reviewer_decision_matrix_writes_default_artifacts(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": str(repo_root)}

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--reviewer-decision-matrix",
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

    markdown_path = tmp_path / "reports" / "reviewer-decision-matrix.md"
    json_path = tmp_path / "reports" / "reviewer-decision-matrix.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert "# Reviewer Decision Matrix" in markdown
    assert payload["artifact_type"] == "reviewer_decision_matrix"
    assert payload["default_outputs"] == {
        "markdown": "reports/reviewer-decision-matrix.md",
        "json": "reports/reviewer-decision-matrix.json",
    }


def test_cli_reviewer_decision_matrix_rejects_incompatible_prediction_mode() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--reviewer-decision-matrix",
            "--prediction-readiness-audit",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        "--reviewer-decision-matrix cannot be combined with "
        "--prediction-readiness-audit" in result.stderr
        or "--prediction-readiness-audit cannot be combined with "
        "--reviewer-decision-matrix" in result.stderr
    )


def test_reviewer_decision_matrix_docs_key_contract_mentions_runtime_keys() -> None:
    markdown = Path("docs/reviewer-decision-matrix.md").read_text(encoding="utf-8")

    assert "reviewer-decision-matrix.md" in markdown
    assert "If **Release Gate** is `FAIL`, do not release for public review." in markdown
    assert (
        "If **Release Gate** is `WARN`, release only as a review artifact "
        "with visible follow-up items; do not promote it."
    ) in markdown
    assert "If **Release Gate** is not `PASS`, do not release" not in markdown
    for key in REVIEWER_DECISION_MATRIX_TOP_LEVEL_KEYS:
        assert f"`{key}`" in markdown
    for key in REVIEWER_DECISION_MATRIX_CATEGORY_KEYS:
        assert f"`{key}`" in markdown


@pytest.mark.parametrize(
    ("extra_args", "message"),
    [
        (
            [str(SAMPLE_DATA)],
            "--reviewer-decision-matrix does not take csv_path",
        ),
        (
            ["--config", str(SAMPLE_CONFIG)],
            "--reviewer-decision-matrix does not take --config",
        ),
        (
            ["--html-output", "decision-matrix.html"],
            "--reviewer-decision-matrix writes Markdown/JSON, not HTML",
        ),
        (
            ["--reviewer-rerun-receipt"],
            "--reviewer-rerun-receipt cannot be combined with --reviewer-decision-matrix",
        ),
    ],
)
def test_cli_reviewer_decision_matrix_rejects_invalid_arguments(
    extra_args: list[str],
    message: str,
) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--reviewer-decision-matrix",
            *extra_args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert message in result.stderr
