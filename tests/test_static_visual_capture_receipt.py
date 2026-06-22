from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from market_signal_lab.static_visual_capture_receipt import (
    BOUNDARY_FLAGS,
    STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS,
    STATIC_VISUAL_CAPTURE_RECEIPT_ARTIFACT_KEYS,
    STATIC_VISUAL_CAPTURE_RECEIPT_DEFAULT_OUTPUT_KEYS,
    STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH,
    STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH,
    STATIC_VISUAL_CAPTURE_RECEIPT_SCOPE_KEYS,
    STATIC_VISUAL_CAPTURE_RECEIPT_TOP_LEVEL_KEYS,
    build_static_visual_capture_receipt,
    render_static_visual_capture_receipt,
)


def test_static_visual_capture_receipt_schema_and_markdown_are_public_safe() -> None:
    payload = build_static_visual_capture_receipt()
    markdown = render_static_visual_capture_receipt(payload)

    assert tuple(payload) == STATIC_VISUAL_CAPTURE_RECEIPT_TOP_LEVEL_KEYS
    assert payload["artifact_type"] == "static_visual_capture_receipt"
    assert payload["schema_version"] == "1.0"
    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert (
        tuple(payload["default_outputs"])
        == STATIC_VISUAL_CAPTURE_RECEIPT_DEFAULT_OUTPUT_KEYS
    )
    assert payload["default_outputs"] == {
        "markdown": STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH,
        "json": STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH,
    }
    assert tuple(payload["capture_receipt_scope"]) == (
        STATIC_VISUAL_CAPTURE_RECEIPT_SCOPE_KEYS
    )
    assert [artifact["path"] for artifact in payload["scanned_artifacts"]] == list(
        STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS
    )
    assert all(
        tuple(artifact) == STATIC_VISUAL_CAPTURE_RECEIPT_ARTIFACT_KEYS
        for artifact in payload["scanned_artifacts"]
    )
    assert "# Static Visual Capture Receipt" in markdown
    assert "reports/index.html" in markdown
    assert "docs/static-gallery-walkthrough.svg" in markdown
    assert "reports/static-visual-capture-checklist.md" in markdown
    assert "reports/visual-acceptance-bundle.md" in markdown
    assert "docs/static-gallery-manifest.md" in markdown
    assert "present" in markdown
    assert "SHA-256" in markdown
    assert "Regeneration command" in markdown
    assert "public evidence" in markdown
    assert "no live data" in markdown
    assert "broker" in markdown
    assert "position-sizing" in markdown
    assert "investment advice" in markdown
    assert "python -m market_signal_lab.cli --static-visual-capture-receipt" in markdown

    public_text = json.dumps(payload, sort_keys=True) + markdown
    forbidden_terms = ("/" + "home/", "work" + "space", "ag" + "ent")
    for term in forbidden_terms:
        assert term not in public_text.lower()


def test_static_visual_capture_receipt_builds_fresh_nested_objects() -> None:
    payload = build_static_visual_capture_receipt()
    payload["default_outputs"]["unexpected"] = "extra"
    payload["capture_receipt_scope"]["unexpected"] = "extra"
    payload["scanned_artifacts"][0]["unexpected"] = "extra"
    payload["public_evidence_notes"].append("extra")
    payload["not_claimed"].append("extra")

    fresh_payload = build_static_visual_capture_receipt()

    assert tuple(fresh_payload["default_outputs"]) == (
        STATIC_VISUAL_CAPTURE_RECEIPT_DEFAULT_OUTPUT_KEYS
    )
    assert tuple(fresh_payload["capture_receipt_scope"]) == (
        STATIC_VISUAL_CAPTURE_RECEIPT_SCOPE_KEYS
    )
    assert tuple(fresh_payload["scanned_artifacts"][0]) == (
        STATIC_VISUAL_CAPTURE_RECEIPT_ARTIFACT_KEYS
    )
    assert "extra" not in fresh_payload["public_evidence_notes"]
    assert "extra" not in fresh_payload["not_claimed"]


def test_static_visual_capture_receipt_marks_missing_artifacts(tmp_path: Path) -> None:
    payload = build_static_visual_capture_receipt(tmp_path)
    markdown = render_static_visual_capture_receipt(payload)

    integrity = payload["artifact_integrity_summary"]

    assert integrity["integrity_status"] == "WARN"
    assert integrity["artifact_count"] == len(STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS)
    assert integrity["present_count"] == 0
    assert integrity["missing_count"] == len(STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS)
    assert payload["scanned_artifacts"][0]["status"] == "missing"
    assert payload["scanned_artifacts"][0]["sha256"] is None
    assert "| reports/index.html | missing | 0 | missing |" in markdown


def test_cli_writes_static_visual_capture_receipt_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--static-visual-capture-receipt",
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
    markdown_path = tmp_path / STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH
    json_path = tmp_path / STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Static Visual Capture Receipt" in markdown
    assert payload["artifact_type"] == "static_visual_capture_receipt"
    assert payload["default_outputs"] == {
        "markdown": STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH,
        "json": STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH,
    }
    assert payload["artifact_integrity_summary"]["integrity_status"] == "PASS"
    assert (
        payload["artifact_integrity_summary"]["present_count"]
        == len(STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS)
    )


def test_cli_writes_static_visual_capture_receipt_custom_paths(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    markdown_path = tmp_path / "custom" / "capture-receipt.md"
    json_path = tmp_path / "custom-json" / "capture-receipt.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--static-visual-capture-receipt",
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
    assert "# Static Visual Capture Receipt" in markdown_path.read_text(
        encoding="utf-8"
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["artifact_type"] == "static_visual_capture_receipt"
