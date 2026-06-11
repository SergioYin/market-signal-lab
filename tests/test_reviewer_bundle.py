from __future__ import annotations

import hashlib
from pathlib import Path

from market_signal_lab.reviewer_bundle import (
    BOUNDARY_FLAGS,
    build_artifact_integrity_summary,
    build_reviewer_evidence_bundle,
    render_reviewer_evidence_bundle,
)


def assert_bundle_json_fields_are_structured(payload: dict[str, object]) -> None:
    for key in BOUNDARY_FLAGS:
        assert type(payload[key]) is bool
        assert payload[key] is True

    for step in payload["inspection_steps"]:
        if "path" in step:
            assert isinstance(step["path"], str)
            assert step["path"].startswith(("docs/", "reports/"))
        if "command" in step:
            assert isinstance(step["command"], str)
            assert step["command"].startswith("python ")

    integrity = payload["artifact_integrity_summary"]
    assert isinstance(integrity, dict)
    for artifact in integrity["artifacts"]:
        assert isinstance(artifact["path"], str)
        assert artifact["path"].startswith(("docs/", "reports/", "[invalid "))
        assert isinstance(artifact["byte_count"], int)
        assert artifact["sha256"] is None or isinstance(artifact["sha256"], str)


def test_artifact_integrity_summary_hashes_present_files_and_marks_missing(
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
        ),
    )

    expected_digest = hashlib.sha256(
        b"<h1>Static gallery</h1>\n",
    ).hexdigest()
    assert summary["summary_type"] == "artifact_integrity_summary"
    assert summary["algorithm"] == "sha256"
    assert summary["integrity_status"] == "WARN"
    assert summary["interpretation"].startswith("WARN:")
    assert "artifact-integrity evidence only" in summary["caveat"]
    assert summary["artifact_count"] == 2
    assert summary["present_count"] == 1
    assert summary["missing_count"] == 1
    assert summary["invalid_count"] == 0
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
    ]


def test_artifact_integrity_summary_rejects_paths_outside_artifact_root(
    tmp_path: Path,
) -> None:
    summary = build_artifact_integrity_summary(
        tmp_path,
        (
            "../private-token.txt",
            "/absolute/private-token.txt",
        ),
    )

    assert summary["present_count"] == 0
    assert summary["missing_count"] == 0
    assert summary["invalid_count"] == 2
    assert summary["integrity_status"] == "FAIL"
    assert summary["interpretation"].startswith("FAIL:")
    assert summary["artifacts"] == [
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


def test_reviewer_bundle_renders_artifact_integrity_summary(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "methodology-audit.md").write_text(
        "# Methodology Audit\n",
        encoding="utf-8",
    )
    payload = build_reviewer_evidence_bundle(tmp_path)

    markdown = render_reviewer_evidence_bundle(payload)

    assert_bundle_json_fields_are_structured(payload)
    integrity = payload["artifact_integrity_summary"]
    assert integrity["artifact_count"] == 7
    assert integrity["present_count"] == 1
    assert integrity["missing_count"] == 6
    assert integrity["invalid_count"] == 0
    assert integrity["integrity_status"] == "WARN"
    assert [artifact["path"] for artifact in integrity["artifacts"]] == [
        "reports/index.html",
        "reports/cross-asset-thesis-ledger.json",
        "reports/cross-asset-thesis-ledger-acceptance.md",
        "reports/cross-asset-thesis-ledger-acceptance.json",
        "reports/stress-kit-quickstart-card.md",
        "reports/stress-kit-quickstart-card.json",
        "docs/methodology-audit.md",
    ]
    assert "## Artifact hash summary" in markdown
    assert "- Integrity status: `WARN`" in markdown
    assert "- Interpretation: WARN:" in markdown
    assert "- Caveat: This is artifact-integrity evidence only" in markdown
    assert "not financial validation" in markdown
    assert "reports/stress-kit-quickstart-card.md" in markdown
    assert "| docs/methodology-audit.md | present | 20 |" in markdown
    assert "| reports/index.html | missing | 0 | missing |" in markdown
