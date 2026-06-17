from __future__ import annotations

import hashlib
from pathlib import Path

from market_signal_lab.visual_walkthrough_evidence_receipt import (
    BOUNDARY_FLAGS,
    VISUAL_WALKTHROUGH_ARTIFACT_PATHS,
    VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_COMMAND,
    build_visual_walkthrough_evidence_receipt,
    render_visual_walkthrough_evidence_receipt,
)


VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "verification_command",
    "reviewer_steps",
    "walkthrough_links",
    "artifact_integrity_summary",
    "not_claimed",
)

WALKTHROUGH_LINK_KEYS = ("label", "path", "evidence_role")


def test_visual_walkthrough_evidence_receipt_hashes_route_artifacts(
    tmp_path: Path,
) -> None:
    svg_path = tmp_path / "docs" / "static-gallery-walkthrough.svg"
    svg_path.parent.mkdir()
    svg_path.write_text("<svg></svg>\n", encoding="utf-8")
    index_path = tmp_path / "reports" / "index.html"
    index_path.parent.mkdir()
    index_path.write_text("<!doctype html>\n", encoding="utf-8")

    payload = build_visual_walkthrough_evidence_receipt(tmp_path)

    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert payload["artifact_type"] == "visual_walkthrough_evidence_receipt"
    assert payload["verification_command"] == (
        VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_COMMAND
    )
    assert payload["default_outputs"] == {
        "markdown": "reports/visual-walkthrough-evidence-receipt.md",
        "json": "reports/visual-walkthrough-evidence-receipt.json",
    }
    integrity = payload["artifact_integrity_summary"]
    assert integrity["artifact_count"] == len(VISUAL_WALKTHROUGH_ARTIFACT_PATHS)
    assert integrity["present_count"] == 2
    assert integrity["missing_count"] == (
        len(VISUAL_WALKTHROUGH_ARTIFACT_PATHS) - 2
    )
    assert {
        artifact["path"]: artifact["sha256"]
        for artifact in integrity["artifacts"]
        if artifact["status"] == "present"
    } == {
        "docs/static-gallery-walkthrough.svg": hashlib.sha256(
            b"<svg></svg>\n"
        ).hexdigest(),
        "reports/index.html": hashlib.sha256(b"<!doctype html>\n").hexdigest(),
    }


def test_visual_walkthrough_evidence_receipt_preserves_schema_order() -> None:
    payload = build_visual_walkthrough_evidence_receipt()

    assert tuple(payload) == VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_TOP_LEVEL_KEYS
    assert [
        artifact["path"]
        for artifact in payload["artifact_integrity_summary"]["artifacts"]
    ] == list(VISUAL_WALKTHROUGH_ARTIFACT_PATHS)
    assert all(
        tuple(link) == WALKTHROUGH_LINK_KEYS
        for link in payload["walkthrough_links"]
    )


def test_visual_walkthrough_evidence_receipt_builds_fresh_nested_objects() -> None:
    payload = build_visual_walkthrough_evidence_receipt()
    payload["reviewer_steps"].append("extra")
    payload["walkthrough_links"][0]["unexpected"] = "extra"
    payload["artifact_integrity_summary"]["artifacts"][0]["path"] = "extra"
    payload["not_claimed"].append("extra")

    fresh_payload = build_visual_walkthrough_evidence_receipt()

    assert "extra" not in fresh_payload["reviewer_steps"]
    assert tuple(fresh_payload["walkthrough_links"][0]) == WALKTHROUGH_LINK_KEYS
    assert fresh_payload["artifact_integrity_summary"]["artifacts"][0]["path"] == (
        VISUAL_WALKTHROUGH_ARTIFACT_PATHS[0]
    )
    assert "extra" not in fresh_payload["not_claimed"]


def test_visual_walkthrough_evidence_receipt_markdown_surfaces_boundaries() -> None:
    payload = build_visual_walkthrough_evidence_receipt()

    markdown = render_visual_walkthrough_evidence_receipt(payload)

    assert "# Visual Walkthrough Evidence Receipt" in markdown
    assert "docs/static-gallery-walkthrough.svg" in markdown
    assert "reports/index.html" in markdown
    assert "reports/public-demo-evidence-receipt.md" in markdown
    assert "reports/reviewer-rerun-receipt.md" in markdown
    assert "reports/acceptance-receipt-index.md" in markdown
    assert "## Artifact Integrity Summary" in markdown
    assert "No broker, account, order-routing" in markdown
    assert "not_investment_advice" in markdown
