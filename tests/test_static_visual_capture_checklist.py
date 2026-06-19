from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from market_signal_lab.static_visual_capture_checklist import (
    BOUNDARY_FLAGS,
    CAPTURE_CHECKLIST_ITEM_KEYS,
    CAPTURE_OPTION_KEYS,
    CAPTURE_SOURCE_PATHS,
    STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_PATH,
    STATIC_VISUAL_CAPTURE_CHECKLIST_MARKDOWN_PATH,
    STATIC_VISUAL_CAPTURE_CHECKLIST_TOP_LEVEL_KEYS,
    STATIC_VISUAL_CAPTURE_DEFAULT_OUTPUT_KEYS,
    build_static_visual_capture_checklist,
    render_static_visual_capture_checklist,
)


def test_static_visual_capture_checklist_schema_and_markdown_are_public_safe() -> None:
    payload = build_static_visual_capture_checklist()
    markdown = render_static_visual_capture_checklist(payload)

    assert tuple(payload) == STATIC_VISUAL_CAPTURE_CHECKLIST_TOP_LEVEL_KEYS
    assert payload["artifact_type"] == "static_visual_capture_checklist"
    assert payload["schema_version"] == "1.0"
    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert (
        tuple(payload["default_outputs"])
        == STATIC_VISUAL_CAPTURE_DEFAULT_OUTPUT_KEYS
    )
    assert payload["default_outputs"] == {
        "markdown": STATIC_VISUAL_CAPTURE_CHECKLIST_MARKDOWN_PATH,
        "json": STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_PATH,
    }
    assert payload["capture_scope"]["allowed_sources"] == list(CAPTURE_SOURCE_PATHS)
    assert all(
        tuple(option) == CAPTURE_OPTION_KEYS
        for option in payload["capture_options"]
    )
    assert all(
        tuple(item) == CAPTURE_CHECKLIST_ITEM_KEYS
        for item in payload["checklist"]
    )
    assert "# Static Visual Capture Checklist" in markdown
    assert "reports/index.html" in markdown
    assert "docs/static-gallery-walkthrough.svg" in markdown
    assert "screenshot" in markdown
    assert "GIF" in markdown
    assert "no live data" in markdown
    assert "broker/account" in markdown
    assert "position sizing" in markdown
    assert "investment advice" in markdown
    assert "private names" in markdown
    assert "absolute local paths" in markdown
    assert "python -m market_signal_lab.cli --static-visual-capture-checklist" in markdown

    public_text = json.dumps(payload, sort_keys=True) + markdown
    forbidden_terms = ("/" + "home/", "work" + "space", "ag" + "ent")
    for term in forbidden_terms:
        assert term not in public_text.lower()


def test_static_visual_capture_checklist_builds_fresh_nested_objects() -> None:
    payload = build_static_visual_capture_checklist()
    payload["default_outputs"]["unexpected"] = "extra"
    payload["capture_scope"]["allowed_sources"].append("extra")
    payload["capture_options"][0]["unexpected"] = "extra"
    payload["checklist"][0]["unexpected"] = "extra"
    payload["verification_commands"].append("extra")
    payload["do_not_capture"].append("extra")

    fresh_payload = build_static_visual_capture_checklist()

    assert tuple(fresh_payload["default_outputs"]) == (
        STATIC_VISUAL_CAPTURE_DEFAULT_OUTPUT_KEYS
    )
    assert fresh_payload["capture_scope"]["allowed_sources"] == list(
        CAPTURE_SOURCE_PATHS
    )
    assert tuple(fresh_payload["capture_options"][0]) == CAPTURE_OPTION_KEYS
    assert tuple(fresh_payload["checklist"][0]) == CAPTURE_CHECKLIST_ITEM_KEYS
    assert "extra" not in fresh_payload["verification_commands"]
    assert "extra" not in fresh_payload["do_not_capture"]


def test_static_visual_capture_checklist_marks_missing_artifacts(
    tmp_path: Path,
) -> None:
    payload = build_static_visual_capture_checklist(tmp_path)
    markdown = render_static_visual_capture_checklist(payload)

    integrity = payload["artifact_integrity_summary"]

    assert integrity["integrity_status"] == "WARN"
    assert integrity["artifact_count"] == len(CAPTURE_SOURCE_PATHS)
    assert integrity["present_count"] == 0
    assert integrity["missing_count"] == len(CAPTURE_SOURCE_PATHS)
    assert "| reports/index.html | missing | 0 | missing |" in markdown


def test_cli_writes_static_visual_capture_checklist_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--static-visual-capture-checklist",
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
    markdown_path = tmp_path / STATIC_VISUAL_CAPTURE_CHECKLIST_MARKDOWN_PATH
    json_path = tmp_path / STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_PATH
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Static Visual Capture Checklist" in markdown
    assert payload["artifact_type"] == "static_visual_capture_checklist"
    assert payload["default_outputs"] == {
        "markdown": STATIC_VISUAL_CAPTURE_CHECKLIST_MARKDOWN_PATH,
        "json": STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_PATH,
    }
    assert payload["artifact_integrity_summary"]["integrity_status"] == "PASS"
    assert (
        payload["artifact_integrity_summary"]["present_count"]
        == len(CAPTURE_SOURCE_PATHS)
    )


def test_cli_writes_static_visual_capture_checklist_custom_paths(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    markdown_path = tmp_path / "custom" / "capture.md"
    json_path = tmp_path / "custom-json" / "capture.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--static-visual-capture-checklist",
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
    assert "# Static Visual Capture Checklist" in markdown_path.read_text(
        encoding="utf-8"
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["artifact_type"] == "static_visual_capture_checklist"
