from __future__ import annotations

import hashlib
from pathlib import Path

from market_signal_lab.public_demo_evidence_receipt import (
    BOUNDARY_FLAGS,
    EVIDENCE_ARTIFACT_PATHS,
    PUBLIC_DEMO_EVIDENCE_RECEIPT_COMMAND,
    build_public_demo_evidence_receipt,
    render_public_demo_evidence_receipt,
)


PUBLIC_DEMO_EVIDENCE_RECEIPT_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "verification_command",
    "reviewer_steps",
    "source_boundaries",
    "generated_artifact_groups",
    "artifact_integrity_summary",
    "not_claimed",
)


def test_public_demo_evidence_receipt_hashes_static_demo_evidence(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "reports" / "sample-report.md"
    report_path.parent.mkdir()
    report_path.write_text("# Sample Report\n", encoding="utf-8")
    data_path = tmp_path / "examples" / "data" / "sample_tqqq_qld_like.csv"
    data_path.parent.mkdir(parents=True)
    data_path.write_text("date,open,high,low,close\n", encoding="utf-8")

    payload = build_public_demo_evidence_receipt(tmp_path)

    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert payload["artifact_type"] == "public_demo_evidence_receipt"
    assert payload["verification_command"] == PUBLIC_DEMO_EVIDENCE_RECEIPT_COMMAND
    assert payload["default_outputs"] == {
        "markdown": "reports/public-demo-evidence-receipt.md",
        "json": "reports/public-demo-evidence-receipt.json",
    }
    assert payload["artifact_integrity_summary"]["artifact_count"] == len(
        EVIDENCE_ARTIFACT_PATHS
    )
    assert payload["artifact_integrity_summary"]["present_count"] == 2
    assert payload["artifact_integrity_summary"]["missing_count"] == (
        len(EVIDENCE_ARTIFACT_PATHS) - 2
    )
    assert {
        artifact["path"]: artifact["sha256"]
        for artifact in payload["artifact_integrity_summary"]["artifacts"]
        if artifact["status"] == "present"
    } == {
        "reports/sample-report.md": hashlib.sha256(b"# Sample Report\n").hexdigest(),
        "examples/data/sample_tqqq_qld_like.csv": hashlib.sha256(
            b"date,open,high,low,close\n"
        ).hexdigest(),
    }


def test_public_demo_evidence_receipt_preserves_deterministic_schema_order() -> None:
    payload = build_public_demo_evidence_receipt()

    assert tuple(payload) == PUBLIC_DEMO_EVIDENCE_RECEIPT_TOP_LEVEL_KEYS
    assert [
        artifact["path"]
        for artifact in payload["artifact_integrity_summary"]["artifacts"]
    ] == list(EVIDENCE_ARTIFACT_PATHS)


def test_public_demo_evidence_receipt_builds_fresh_nested_objects() -> None:
    payload = build_public_demo_evidence_receipt()
    payload["reviewer_steps"].append("extra")
    payload["source_boundaries"][0]["unexpected_boundary_field"] = "extra"
    payload["generated_artifact_groups"][0]["paths"].append("extra")
    payload["artifact_integrity_summary"]["artifacts"][0]["path"] = "extra"
    payload["not_claimed"].append("extra")

    fresh_payload = build_public_demo_evidence_receipt()

    assert "extra" not in fresh_payload["reviewer_steps"]
    assert "unexpected_boundary_field" not in fresh_payload["source_boundaries"][0]
    assert "extra" not in fresh_payload["generated_artifact_groups"][0]["paths"]
    assert (
        fresh_payload["artifact_integrity_summary"]["artifacts"][0]["path"]
        == EVIDENCE_ARTIFACT_PATHS[0]
    )
    assert "extra" not in fresh_payload["not_claimed"]


def test_public_demo_evidence_receipt_markdown_surfaces_boundaries() -> None:
    payload = build_public_demo_evidence_receipt()

    markdown = render_public_demo_evidence_receipt(payload)

    assert "# Public Demo Evidence Receipt" in markdown
    assert "## Generated Artifact Groups" in markdown
    assert "## Source Fixture Boundaries" in markdown
    assert "## Artifact Integrity Summary" in markdown
    assert "## Not Claimed" in markdown
    assert "docs/static-gallery-walkthrough.svg" in markdown
    assert "reports/visual-walkthrough-evidence-receipt.md" in markdown
    assert "reports/sample-manifest.md" in markdown
    assert "examples/data/sample_tqqq_qld_like.csv.provenance.json" in markdown
    assert "No live market data was fetched by this receipt." in markdown
    assert "not_investment_advice" in markdown
