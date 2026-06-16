from __future__ import annotations

import hashlib
from pathlib import Path

from market_signal_lab.acceptance_receipt_index import (
    ACCEPTANCE_RECEIPT_INDEX_COMMAND,
    BOUNDARY_FLAGS,
    INDEX_ARTIFACT_PATHS,
    build_acceptance_receipt_index,
    render_acceptance_receipt_index,
)


ACCEPTANCE_RECEIPT_INDEX_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "verification_command",
    "indexed_receipts",
    "fixture_provenance",
    "reviewer_rerun_commands",
    "artifact_integrity_summary",
    "not_claimed",
)

INDEXED_RECEIPT_KEYS = (
    "label",
    "markdown_path",
    "json_path",
    "source_command",
    "evidence_role",
)
FIXTURE_PROVENANCE_KEYS = ("fixture_path", "provenance_path", "use")


def test_acceptance_receipt_index_hashes_receipts_and_fixture_provenance(
    tmp_path: Path,
) -> None:
    receipt_path = tmp_path / "reports" / "reviewer-rerun-receipt.md"
    receipt_path.parent.mkdir()
    receipt_path.write_text("# Reviewer Rerun Receipt\n", encoding="utf-8")
    provenance_path = (
        tmp_path / "examples" / "data" / "sample_tqqq_qld_like.csv.provenance.json"
    )
    provenance_path.parent.mkdir(parents=True)
    provenance_path.write_text('{"source":"synthetic"}\n', encoding="utf-8")

    payload = build_acceptance_receipt_index(tmp_path)

    for key in BOUNDARY_FLAGS:
        assert payload[key] is True
    assert payload["artifact_type"] == "acceptance_receipt_index"
    assert payload["verification_command"] == ACCEPTANCE_RECEIPT_INDEX_COMMAND
    assert payload["default_outputs"] == {
        "markdown": "reports/acceptance-receipt-index.md",
        "json": "reports/acceptance-receipt-index.json",
    }
    integrity = payload["artifact_integrity_summary"]
    assert integrity["artifact_count"] == len(INDEX_ARTIFACT_PATHS)
    assert integrity["present_count"] == 2
    assert integrity["missing_count"] == len(INDEX_ARTIFACT_PATHS) - 2
    assert {
        artifact["path"]: artifact["sha256"]
        for artifact in integrity["artifacts"]
        if artifact["status"] == "present"
    } == {
        "reports/reviewer-rerun-receipt.md": hashlib.sha256(
            b"# Reviewer Rerun Receipt\n"
        ).hexdigest(),
        "examples/data/sample_tqqq_qld_like.csv.provenance.json": hashlib.sha256(
            b'{"source":"synthetic"}\n'
        ).hexdigest(),
    }


def test_acceptance_receipt_index_preserves_deterministic_schema_order() -> None:
    payload = build_acceptance_receipt_index()

    assert tuple(payload) == ACCEPTANCE_RECEIPT_INDEX_TOP_LEVEL_KEYS
    assert [artifact["path"] for artifact in payload["artifact_integrity_summary"]["artifacts"]] == list(
        INDEX_ARTIFACT_PATHS
    )
    assert all(tuple(receipt) == INDEXED_RECEIPT_KEYS for receipt in payload["indexed_receipts"])
    assert all(
        tuple(fixture) == FIXTURE_PROVENANCE_KEYS
        for fixture in payload["fixture_provenance"]
    )


def test_acceptance_receipt_index_builds_fresh_nested_objects() -> None:
    payload = build_acceptance_receipt_index()
    payload["indexed_receipts"][0]["unexpected"] = "extra"
    payload["fixture_provenance"][0]["unexpected"] = "extra"
    payload["reviewer_rerun_commands"].append("extra")
    payload["artifact_integrity_summary"]["artifacts"][0]["path"] = "extra"
    payload["not_claimed"].append("extra")

    fresh_payload = build_acceptance_receipt_index()

    assert tuple(fresh_payload["indexed_receipts"][0]) == INDEXED_RECEIPT_KEYS
    assert tuple(fresh_payload["fixture_provenance"][0]) == FIXTURE_PROVENANCE_KEYS
    assert "extra" not in fresh_payload["reviewer_rerun_commands"]
    assert fresh_payload["artifact_integrity_summary"]["artifacts"][0]["path"] == (
        INDEX_ARTIFACT_PATHS[0]
    )
    assert "extra" not in fresh_payload["not_claimed"]


def test_acceptance_receipt_index_markdown_surfaces_boundaries() -> None:
    payload = build_acceptance_receipt_index()

    markdown = render_acceptance_receipt_index(payload)

    assert "# Acceptance Receipt Index" in markdown
    assert "## Indexed Receipts" in markdown
    assert "reports/public-demo-evidence-receipt.md" in markdown
    assert "reports/reviewer-rerun-receipt.md" in markdown
    assert "reports/reviewer-evidence-bundle.md" in markdown
    assert "## Fixture Provenance" in markdown
    assert "examples/data/sample_tqqq_qld_like.csv.provenance.json" in markdown
    assert "## Artifact Hash Index" in markdown
    assert "No live data, broker, account" in markdown
    assert "not_investment_advice" in markdown
