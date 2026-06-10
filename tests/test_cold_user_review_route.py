from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from market_signal_lab.cold_user_review_route import (
    BOUNDARY_FLAGS,
    COLD_USER_REVIEW_CHECKLIST_KEYS,
    COLD_USER_REVIEW_ROUTE_DEFAULT_OUTPUT_KEYS,
    COLD_USER_REVIEW_ROUTE_STEP_KEYS,
    COLD_USER_REVIEW_ROUTE_TOP_LEVEL_KEYS,
    INTEGRITY_ARTIFACT_PATHS,
    build_artifact_integrity_summary,
    build_cold_user_review_route,
    render_cold_user_review_route,
)


def test_cold_user_review_route_schema_and_markdown_are_public_safe() -> None:
    payload = build_cold_user_review_route()
    markdown = render_cold_user_review_route(payload)

    assert tuple(payload) == COLD_USER_REVIEW_ROUTE_TOP_LEVEL_KEYS
    assert payload["artifact_type"] == "cold_user_review_route"
    assert payload["schema_version"] == "1.0"
    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert (
        tuple(payload["default_outputs"])
        == COLD_USER_REVIEW_ROUTE_DEFAULT_OUTPUT_KEYS
    )
    assert all(
        tuple(step) == COLD_USER_REVIEW_ROUTE_STEP_KEYS
        for step in payload["route"]
    )
    assert all(
        tuple(item) == COLD_USER_REVIEW_CHECKLIST_KEYS
        for item in payload["checklist"]
    )
    assert payload["default_outputs"] == {
        "markdown": "reports/cold-user-review-route.md",
        "json": "reports/cold-user-review-route.json",
    }
    assert [step["path"] for step in payload["route"]] == [
        "reports/index.html",
        "reports/sample-report.md",
        "reports/beginner-prediction-checklist.md",
        "reports/reviewer-evidence-bundle.md",
        "reports/reviewer-rerun-receipt.md",
        "docs/methodology-audit.md",
        "reports/reviewer-acceptance-scorecard.md",
    ]
    assert payload["route"][-1]["step"] == "review_acceptance_scorecard"
    assert "research-only handoff" in payload["route"][-1]["expected_public_signal"]
    assert "reports/reviewer-acceptance-scorecard.md" in markdown
    assert "reports/reviewer-rerun-receipt.md" in markdown
    assert "python -m market_signal_lab.cli --reviewer-rerun-receipt" in markdown
    assert "python -m market_signal_lab.cli --reviewer-acceptance-scorecard" in markdown
    assert "# Cold-User Review Route" in markdown
    assert "reports/index.html" in markdown
    assert "no live data" in markdown
    assert "investment advice" in markdown
    public_text = json.dumps(payload, sort_keys=True) + markdown
    forbidden_terms = ("/" + "home/", "work" + "space", "ag" + "ent")
    for term in forbidden_terms:
        assert term not in public_text.lower()


def test_cold_user_review_route_builds_fresh_nested_objects() -> None:
    payload = build_cold_user_review_route()
    payload["default_outputs"]["unexpected_output"] = "extra"
    payload["route"][0]["unexpected_route_field"] = "extra"
    payload["checklist"][0]["unexpected_checklist_field"] = "extra"
    payload["do_not_use_for"].append("extra")
    payload["verification_commands"].append("extra")

    fresh_payload = build_cold_user_review_route()

    assert tuple(fresh_payload["default_outputs"]) == (
        COLD_USER_REVIEW_ROUTE_DEFAULT_OUTPUT_KEYS
    )
    assert tuple(fresh_payload["route"][0]) == COLD_USER_REVIEW_ROUTE_STEP_KEYS
    assert tuple(fresh_payload["checklist"][0]) == COLD_USER_REVIEW_CHECKLIST_KEYS
    assert "extra" not in fresh_payload["do_not_use_for"]
    assert "extra" not in fresh_payload["verification_commands"]


def test_cold_user_artifact_integrity_summary_uses_route_order(
    tmp_path: Path,
) -> None:
    for artifact_path in INTEGRITY_ARTIFACT_PATHS:
        path = tmp_path / artifact_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{artifact_path}\n", encoding="utf-8")

    summary = build_artifact_integrity_summary(tmp_path)

    assert [artifact["path"] for artifact in summary["artifacts"]] == list(
        INTEGRITY_ARTIFACT_PATHS
    )
    assert summary["integrity_status"] == "PASS"


def test_cold_user_review_route_marks_missing_integrity_artifacts(
    tmp_path: Path,
) -> None:
    payload = build_cold_user_review_route(tmp_path)
    markdown = render_cold_user_review_route(payload)

    summary = payload["artifact_integrity_summary"]

    assert summary["integrity_status"] == "WARN"
    assert summary["artifact_count"] == len(INTEGRITY_ARTIFACT_PATHS)
    assert summary["present_count"] == 0
    assert summary["missing_count"] == len(INTEGRITY_ARTIFACT_PATHS)
    assert summary["invalid_count"] == 0
    assert summary["artifacts"][0] == {
        "path": "reports/index.html",
        "status": "missing",
        "byte_count": 0,
        "sha256": None,
    }
    assert "- Integrity status: `WARN`" in markdown
    assert "| reports/index.html | missing | 0 | missing |" in markdown


def test_cold_user_artifact_integrity_summary_hashes_and_rejects_paths(
    tmp_path: Path,
) -> None:
    artifact_path = tmp_path / "reports" / "index.html"
    artifact_path.parent.mkdir()
    artifact_path.write_text("<h1>Static gallery</h1>\n", encoding="utf-8")

    summary = build_artifact_integrity_summary(
        tmp_path,
        (
            "reports/index.html",
            "reports/missing.md",
            "../private.txt",
            "/private.txt",
        ),
    )

    expected_digest = hashlib.sha256(b"<h1>Static gallery</h1>\n").hexdigest()
    assert summary["summary_type"] == "cold_user_artifact_integrity_summary"
    assert summary["algorithm"] == "sha256"
    assert summary["integrity_status"] == "FAIL"
    assert summary["present_count"] == 1
    assert summary["missing_count"] == 1
    assert summary["invalid_count"] == 2
    assert summary["artifacts"] == [
        {
            "path": "reports/index.html",
            "status": "present",
            "byte_count": 24,
            "sha256": expected_digest,
        },
        {
            "path": "reports/missing.md",
            "status": "missing",
            "byte_count": 0,
            "sha256": None,
        },
        {
            "path": "[invalid artifact path]",
            "status": "invalid_path",
            "byte_count": 0,
            "sha256": None,
        },
        {
            "path": "[invalid artifact path]",
            "status": "invalid_path",
            "byte_count": 0,
            "sha256": None,
        },
    ]


def test_cli_writes_cold_user_review_route_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--cold-user-review-route",
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
    markdown_path = tmp_path / "reports" / "cold-user-review-route.md"
    json_path = tmp_path / "reports" / "cold-user-review-route.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Cold-User Review Route" in markdown
    assert payload["artifact_type"] == "cold_user_review_route"
    assert payload["default_outputs"]["markdown"] == (
        "reports/cold-user-review-route.md"
    )
    integrity = payload["artifact_integrity_summary"]
    assert integrity["integrity_status"] == "PASS"
    assert integrity["artifact_count"] == 7
    assert integrity["present_count"] == 7
    assert integrity["missing_count"] == 0
    assert "| reports/index.html | present |" in markdown


def test_cli_writes_cold_user_review_route_custom_paths(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    markdown_path = tmp_path / "custom" / "route.md"
    json_path = tmp_path / "custom-json" / "route.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--cold-user-review-route",
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
    assert "# Cold-User Review Route" in markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["artifact_type"] == "cold_user_review_route"
    assert payload["default_outputs"] == {
        "markdown": "reports/cold-user-review-route.md",
        "json": "reports/cold-user-review-route.json",
    }
    assert not (tmp_path / "reports" / "cold-user-review-route.md").exists()
    assert not (tmp_path / "reports" / "cold-user-review-route.json").exists()


@pytest.mark.parametrize(
    ("extra_args", "message"),
    [
        (
            ["--symbol", "QQQ_LIKE"],
            "--cold-user-review-route cannot be combined with --symbol",
        ),
        (
            ["--beginner-prediction-checklist"],
            (
                "--cold-user-review-route cannot be combined with "
                "--beginner-prediction-checklist"
            ),
        ),
    ],
)
def test_cli_rejects_conflicts_for_cold_user_review_route(
    extra_args: list[str],
    message: str,
) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--cold-user-review-route",
            *extra_args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert message in result.stderr
