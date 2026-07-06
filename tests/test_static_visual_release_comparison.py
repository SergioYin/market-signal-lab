from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from market_signal_lab.static_visual_release_comparison import (
    BOUNDARY_FLAGS,
    SOURCE_RECEIPT_ARTIFACT_PATHS,
    STATIC_VISUAL_RELEASE_COMPARISON_CHECK_KEYS,
    STATIC_VISUAL_RELEASE_COMPARISON_DEFAULT_OUTPUT_KEYS,
    STATIC_VISUAL_RELEASE_COMPARISON_JSON_PATH,
    STATIC_VISUAL_RELEASE_COMPARISON_MARKDOWN_PATH,
    STATIC_VISUAL_RELEASE_COMPARISON_ROW_KEYS,
    STATIC_VISUAL_RELEASE_COMPARISON_SCOPE_KEYS,
    STATIC_VISUAL_RELEASE_COMPARISON_SOURCE_ARTIFACT_KEYS,
    STATIC_VISUAL_RELEASE_COMPARISON_TOP_LEVEL_KEYS,
    build_static_visual_release_comparison,
    render_static_visual_release_comparison,
)


def test_static_visual_release_comparison_schema_and_markdown_are_public_safe() -> None:
    payload = build_static_visual_release_comparison()
    markdown = render_static_visual_release_comparison(payload)

    assert tuple(payload) == STATIC_VISUAL_RELEASE_COMPARISON_TOP_LEVEL_KEYS
    assert payload["artifact_type"] == "static_visual_release_comparison"
    assert payload["schema_version"] == "1.0"
    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert (
        tuple(payload["default_outputs"])
        == STATIC_VISUAL_RELEASE_COMPARISON_DEFAULT_OUTPUT_KEYS
    )
    assert payload["default_outputs"] == {
        "markdown": STATIC_VISUAL_RELEASE_COMPARISON_MARKDOWN_PATH,
        "json": STATIC_VISUAL_RELEASE_COMPARISON_JSON_PATH,
    }
    assert tuple(payload["comparison_scope"]) == (
        STATIC_VISUAL_RELEASE_COMPARISON_SCOPE_KEYS
    )
    assert [artifact["path"] for artifact in payload["source_receipt_artifacts"]] == (
        list(SOURCE_RECEIPT_ARTIFACT_PATHS)
    )
    assert all(
        tuple(artifact) == STATIC_VISUAL_RELEASE_COMPARISON_SOURCE_ARTIFACT_KEYS
        for artifact in payload["source_receipt_artifacts"]
    )
    assert all(
        tuple(row) == STATIC_VISUAL_RELEASE_COMPARISON_ROW_KEYS
        for row in payload["release_comparison"]
    )
    assert all(
        tuple(item) == STATIC_VISUAL_RELEASE_COMPARISON_CHECK_KEYS
        for item in payload["reviewer_checklist"]
    )
    assert "# Static Visual Release Comparison" in markdown
    assert "v1.30.7 static visual capture receipt baseline" in markdown
    assert "reports/static-visual-capture-receipt.md" in markdown
    assert "reports/static-visual-capture-receipt.json" in markdown
    assert "reports/static-visual-capture-checklist.md" in markdown
    assert "reports/index.html" in markdown
    assert "Release Comparison" in markdown
    assert "Reviewer Checklist" in markdown
    assert "SHA-256" in markdown
    assert "no live data" in markdown
    assert "broker/account" in markdown
    assert "position sizing" in markdown
    assert "investment advice" in markdown
    assert (
        "python -m market_signal_lab.cli --static-visual-release-comparison"
        in markdown
    )

    public_text = json.dumps(payload, sort_keys=True) + markdown
    forbidden_terms = ("/" + "home/", "work" + "space", "ag" + "ent")
    for term in forbidden_terms:
        assert term not in public_text.lower()


def test_static_visual_release_comparison_builds_fresh_nested_objects() -> None:
    payload = build_static_visual_release_comparison()
    payload["default_outputs"]["unexpected"] = "extra"
    payload["comparison_scope"]["unexpected"] = "extra"
    payload["source_receipt_artifacts"][0]["unexpected"] = "extra"
    payload["release_comparison"][0]["unexpected"] = "extra"
    payload["reviewer_checklist"][0]["unexpected"] = "extra"
    payload["not_claimed"].append("extra")

    fresh_payload = build_static_visual_release_comparison()

    assert tuple(fresh_payload["default_outputs"]) == (
        STATIC_VISUAL_RELEASE_COMPARISON_DEFAULT_OUTPUT_KEYS
    )
    assert tuple(fresh_payload["comparison_scope"]) == (
        STATIC_VISUAL_RELEASE_COMPARISON_SCOPE_KEYS
    )
    assert tuple(fresh_payload["source_receipt_artifacts"][0]) == (
        STATIC_VISUAL_RELEASE_COMPARISON_SOURCE_ARTIFACT_KEYS
    )
    assert tuple(fresh_payload["release_comparison"][0]) == (
        STATIC_VISUAL_RELEASE_COMPARISON_ROW_KEYS
    )
    assert tuple(fresh_payload["reviewer_checklist"][0]) == (
        STATIC_VISUAL_RELEASE_COMPARISON_CHECK_KEYS
    )
    assert "extra" not in fresh_payload["not_claimed"]


def test_static_visual_release_comparison_marks_missing_artifacts(
    tmp_path: Path,
) -> None:
    payload = build_static_visual_release_comparison(tmp_path)
    markdown = render_static_visual_release_comparison(payload)

    source_integrity = payload["source_receipt_integrity_summary"]
    current_integrity = payload["current_receipt_artifact_integrity_summary"]

    assert source_integrity["integrity_status"] == "WARN"
    assert source_integrity["present_count"] == 0
    assert source_integrity["missing_count"] == len(SOURCE_RECEIPT_ARTIFACT_PATHS)
    assert current_integrity["integrity_status"] == "WARN"
    assert payload["release_comparison"][0]["current_status"] == "missing"
    assert payload["release_comparison"][0]["current_sha256"] is None
    assert "| reports/index.html | present | missing | WARN | missing |" in markdown


def test_cli_writes_static_visual_release_comparison_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--static-visual-release-comparison",
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
    markdown_path = tmp_path / STATIC_VISUAL_RELEASE_COMPARISON_MARKDOWN_PATH
    json_path = tmp_path / STATIC_VISUAL_RELEASE_COMPARISON_JSON_PATH
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Static Visual Release Comparison" in markdown
    assert "reports/static-visual-capture-receipt.md" in markdown
    assert payload["artifact_type"] == "static_visual_release_comparison"
    assert payload["default_outputs"] == {
        "markdown": STATIC_VISUAL_RELEASE_COMPARISON_MARKDOWN_PATH,
        "json": STATIC_VISUAL_RELEASE_COMPARISON_JSON_PATH,
    }
    assert payload["source_receipt_integrity_summary"]["integrity_status"] == "PASS"
    assert (
        payload["current_receipt_artifact_integrity_summary"]["integrity_status"]
        == "PASS"
    )


def test_cli_writes_static_visual_release_comparison_custom_paths(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    markdown_path = tmp_path / "custom" / "release-comparison.md"
    json_path = tmp_path / "custom-json" / "release-comparison.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--static-visual-release-comparison",
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
    assert "# Static Visual Release Comparison" in markdown_path.read_text(
        encoding="utf-8"
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["artifact_type"] == "static_visual_release_comparison"
