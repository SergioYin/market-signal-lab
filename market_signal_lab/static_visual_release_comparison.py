"""Deterministic release-to-release comparison for static visual receipts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_signal_lab.reviewer_bundle import build_artifact_integrity_summary
from market_signal_lab.static_visual_capture_receipt import (
    STATIC_VISUAL_CAPTURE_ARTIFACTS,
    STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS,
    STATIC_VISUAL_CAPTURE_RECEIPT_COMMAND,
    STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH,
    STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH,
    build_static_visual_capture_receipt,
)


STATIC_VISUAL_RELEASE_COMPARISON_MARKDOWN_PATH = (
    "reports/static-visual-release-comparison.md"
)
STATIC_VISUAL_RELEASE_COMPARISON_JSON_PATH = (
    "reports/static-visual-release-comparison.json"
)
STATIC_VISUAL_RELEASE_COMPARISON_FLAG = "--static-visual-release-comparison"
STATIC_VISUAL_RELEASE_COMPARISON_COMMAND = (
    "python -m market_signal_lab.cli --static-visual-release-comparison"
)

PREVIOUS_RELEASE_LABEL = "v1.30.7 static visual capture receipt baseline"
CURRENT_RELEASE_LABEL = "working-tree static visual capture receipt candidate"

BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "public_safe": True,
    "fixture_or_static_data_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
    "not_investment_advice": True,
    "no_private_data": True,
}

STATIC_VISUAL_RELEASE_COMPARISON_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "verification_command",
    "comparison_scope",
    "source_receipt_artifacts",
    "release_comparison",
    "reviewer_checklist",
    "source_receipt_integrity_summary",
    "current_receipt_artifact_integrity_summary",
    "not_claimed",
)
STATIC_VISUAL_RELEASE_COMPARISON_DEFAULT_OUTPUT_KEYS = ("markdown", "json")
STATIC_VISUAL_RELEASE_COMPARISON_SCOPE_KEYS = (
    "previous_release_label",
    "current_release_label",
    "comparison_surface",
    "baseline_policy",
)
STATIC_VISUAL_RELEASE_COMPARISON_SOURCE_ARTIFACT_KEYS = (
    "path",
    "role",
    "required",
)
STATIC_VISUAL_RELEASE_COMPARISON_ROW_KEYS = (
    "path",
    "previous_release_label",
    "current_release_label",
    "previous_status",
    "current_status",
    "comparison_status",
    "previous_role",
    "current_role",
    "current_sha256",
    "review_note",
)
STATIC_VISUAL_RELEASE_COMPARISON_CHECK_KEYS = (
    "check",
    "label",
    "status",
    "review_note",
)

SOURCE_RECEIPT_ARTIFACTS = (
    {
        "path": STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH,
        "role": "human-readable static visual capture receipt",
        "required": True,
    },
    {
        "path": STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH,
        "role": "machine-readable static visual capture receipt",
        "required": True,
    },
    {
        "path": "reports/static-visual-capture-checklist.md",
        "role": "public-safe reviewer capture checklist",
        "required": True,
    },
    {
        "path": "reports/static-visual-capture-checklist.json",
        "role": "machine-readable reviewer capture checklist",
        "required": True,
    },
)
SOURCE_RECEIPT_ARTIFACT_PATHS = tuple(
    artifact["path"] for artifact in SOURCE_RECEIPT_ARTIFACTS
)

PREVIOUS_RELEASE_BASELINE = tuple(
    {
        "path": artifact["path"],
        "status": "present",
        "role": artifact["role"],
    }
    for artifact in STATIC_VISUAL_CAPTURE_ARTIFACTS
)

NOT_CLAIMED = (
    "This comparison is a static review checklist, not release approval or financial validation.",
    "It compares expected receipt inventory shape and current local file-byte hashes only.",
    "It does not fetch tags, releases, live market data, broker data, account data, or external services.",
    "PASS labels do not validate financial correctness, future performance, suitability, profitability, trading readiness, recommendations, or investment advice.",
    "Optional screenshots or GIFs remain reviewer-created artifacts and are not generated, captured, or validated by this command.",
)


def build_static_visual_release_comparison(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a deterministic comparison for static visual receipt continuity."""

    current_receipt = build_static_visual_capture_receipt(artifact_root)
    current_by_path = {
        artifact["path"]: artifact for artifact in current_receipt["scanned_artifacts"]
    }
    rows = [
        _comparison_row(baseline, current_by_path.get(baseline["path"]))
        for baseline in PREVIOUS_RELEASE_BASELINE
    ]
    source_integrity = build_artifact_integrity_summary(
        artifact_root,
        SOURCE_RECEIPT_ARTIFACT_PATHS,
    )

    return {
        "artifact_type": "static_visual_release_comparison",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "Compare the v1.30.7 static visual capture receipt baseline with "
            "the current working-tree static visual capture receipt scan, so "
            "public reviewers can see whether expected static visual receipt "
            "paths, roles, presence, hashes, and review boundaries carried "
            "forward without opening live data, broker, account, order, "
            "forecast, recommendation, or advice surfaces."
        ),
        "default_outputs": {
            "markdown": STATIC_VISUAL_RELEASE_COMPARISON_MARKDOWN_PATH,
            "json": STATIC_VISUAL_RELEASE_COMPARISON_JSON_PATH,
        },
        "verification_command": STATIC_VISUAL_RELEASE_COMPARISON_COMMAND,
        "comparison_scope": {
            "previous_release_label": PREVIOUS_RELEASE_LABEL,
            "current_release_label": CURRENT_RELEASE_LABEL,
            "comparison_surface": (
                "existing static visual capture receipt artifacts and their "
                "current repo-relative scanned artifact inventory"
            ),
            "baseline_policy": (
                "baseline paths and roles are embedded from the v1.30.7 "
                "static visual capture receipt contract; current status and "
                "hashes come from the local static artifact scan"
            ),
        },
        "source_receipt_artifacts": [
            dict(artifact) for artifact in SOURCE_RECEIPT_ARTIFACTS
        ],
        "release_comparison": rows,
        "reviewer_checklist": _reviewer_checklist(rows, current_receipt),
        "source_receipt_integrity_summary": source_integrity,
        "current_receipt_artifact_integrity_summary": current_receipt[
            "artifact_integrity_summary"
        ],
        "not_claimed": list(NOT_CLAIMED),
    }


def _comparison_row(
    baseline: dict[str, str],
    current: dict[str, Any] | None,
) -> dict[str, Any]:
    current_status = current["status"] if current else "missing"
    current_role = current["role"] if current else None
    if current is None or current_status != "present":
        comparison_status = "WARN"
        review_note = (
            "Expected static visual receipt artifact is missing from the "
            "current scan; regenerate static artifacts before release review."
        )
    elif current_role != baseline["role"]:
        comparison_status = "REVIEW"
        review_note = (
            "Path is present but its role changed from the previous release "
            "baseline; review the visual handoff wording before public sharing."
        )
    else:
        comparison_status = "PASS"
        review_note = (
            "Expected path and role carried forward; current SHA-256 records "
            "local file bytes at comparison generation time only."
        )

    return {
        "path": baseline["path"],
        "previous_release_label": PREVIOUS_RELEASE_LABEL,
        "current_release_label": CURRENT_RELEASE_LABEL,
        "previous_status": baseline["status"],
        "current_status": current_status,
        "comparison_status": comparison_status,
        "previous_role": baseline["role"],
        "current_role": current_role,
        "current_sha256": current["sha256"] if current else None,
        "review_note": review_note,
    }


def _reviewer_checklist(
    rows: list[dict[str, Any]],
    current_receipt: dict[str, Any],
) -> list[dict[str, str]]:
    all_present = all(row["current_status"] == "present" for row in rows)
    all_roles_match = all(row["comparison_status"] == "PASS" for row in rows)
    boundaries_preserved = all(
        current_receipt.get(key) is True for key in BOUNDARY_FLAGS
    )
    current_paths = [row["path"] for row in rows]
    baseline_paths = [artifact["path"] for artifact in PREVIOUS_RELEASE_BASELINE]

    return [
        {
            "check": "receipt_source_artifacts_present",
            "label": "Source receipt artifacts are listed for review",
            "status": "PASS",
            "review_note": (
                "The comparison lists the existing Markdown/JSON static visual "
                "capture receipt and checklist as source receipt artifacts."
            ),
        },
        {
            "check": "artifact_set_matches_baseline",
            "label": "Compared artifact set matches the previous release baseline",
            "status": "PASS" if current_paths == baseline_paths else "WARN",
            "review_note": (
                "The comparison rows keep the v1.30.7 static visual capture "
                "receipt path order so release reviewers can spot additions or "
                "removals deterministically."
            ),
        },
        {
            "check": "current_artifacts_present",
            "label": "Current static visual receipt artifacts are present",
            "status": "PASS" if all_present else "WARN",
            "review_note": (
                "All compared paths should be present before sharing the "
                "release comparison as public static review evidence."
            ),
        },
        {
            "check": "roles_carried_forward",
            "label": "Artifact roles carried forward",
            "status": "PASS" if all_roles_match else "REVIEW",
            "review_note": (
                "Role changes are allowed only after a reviewer confirms the "
                "visual handoff wording still describes static review evidence."
            ),
        },
        {
            "check": "boundaries_preserved",
            "label": "Research-only and no-advice boundaries are preserved",
            "status": "PASS" if boundaries_preserved else "FAIL",
            "review_note": (
                "Boundary flags must remain true: no live data, broker/account "
                "workflow, orders, position sizing, forecasts, recommendations, "
                "private data, or investment advice."
            ),
        },
        {
            "check": "hashes_are_limited",
            "label": "Hash interpretation remains limited",
            "status": "PASS",
            "review_note": (
                "SHA-256 values are file-byte receipts only; they do not prove "
                "financial correctness, performance, suitability, or trading "
                "readiness."
            ),
        },
    ]


def render_static_visual_release_comparison(payload: dict[str, Any]) -> str:
    """Render the static visual release comparison as Markdown."""

    source_integrity = payload["source_receipt_integrity_summary"]
    current_integrity = payload["current_receipt_artifact_integrity_summary"]
    lines = [
        "# Static Visual Release Comparison",
        "",
        payload["purpose"],
        "",
        "## Scope",
        "",
        f"- Previous release: {payload['comparison_scope']['previous_release_label']}",
        f"- Current release: {payload['comparison_scope']['current_release_label']}",
        f"- Comparison surface: {payload['comparison_scope']['comparison_surface']}",
        f"- Baseline policy: {payload['comparison_scope']['baseline_policy']}",
        f"- Verification command: `{payload['verification_command']}`",
        f"- Source receipt rerun: `{STATIC_VISUAL_CAPTURE_RECEIPT_COMMAND}`",
        "",
        "## Source Receipt Artifacts",
        "",
        "| Path | Role | Required |",
        "| --- | --- | --- |",
    ]
    lines.extend(
        "| {path} | {role} | {required} |".format(
            path=artifact["path"],
            role=artifact["role"],
            required=artifact["required"],
        )
        for artifact in payload["source_receipt_artifacts"]
    )

    lines.extend(
        [
            "",
            "## Release Comparison",
            "",
            "| Path | Previous status | Current status | Comparison | Current SHA-256 | Review note |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(
        "| {path} | {previous_status} | {current_status} | {comparison_status} | {current_sha256} | {review_note} |".format(
            path=row["path"],
            previous_status=row["previous_status"],
            current_status=row["current_status"],
            comparison_status=row["comparison_status"],
            current_sha256=row["current_sha256"] or "missing",
            review_note=row["review_note"],
        )
        for row in payload["release_comparison"]
    )

    lines.extend(["", "## Reviewer Checklist", ""])
    for item in payload["reviewer_checklist"]:
        lines.extend(
            [
                f"- **{item['label']}**: `{item['status']}`",
                f"  - Check: `{item['check']}`",
                f"  - Review note: {item['review_note']}",
            ]
        )

    lines.extend(
        [
            "",
            "## Source Receipt Integrity",
            "",
            f"- Integrity status: `{source_integrity['integrity_status']}`",
            f"- Interpretation: {source_integrity['interpretation']}",
            f"- Caveat: {source_integrity['caveat']}",
            f"- Algorithm: `{source_integrity['algorithm']}`",
            f"- Scope: {source_integrity['scope']}",
            f"- Present artifacts: `{source_integrity['present_count']}` of `{source_integrity['artifact_count']}`",
            "",
            "| Path | Status | Bytes | SHA-256 |",
            "| --- | --- | ---: | --- |",
        ]
    )
    lines.extend(
        "| {path} | {status} | {byte_count} | {sha256} |".format(
            path=artifact["path"],
            status=artifact["status"],
            byte_count=artifact["byte_count"],
            sha256=artifact["sha256"] or "missing",
        )
        for artifact in source_integrity["artifacts"]
    )

    lines.extend(
        [
            "",
            "## Current Receipt Artifact Summary",
            "",
            f"- Integrity status: `{current_integrity['integrity_status']}`",
            f"- Interpretation: {current_integrity['interpretation']}",
            f"- Caveat: {current_integrity['caveat']}",
            f"- Algorithm: `{current_integrity['algorithm']}`",
            f"- Scope: {current_integrity['scope']}",
            f"- Present artifacts: `{current_integrity['present_count']}` of `{current_integrity['artifact_count']}`",
            "",
            "## Not Claimed",
            "",
        ]
    )
    lines.extend(f"- {claim}" for claim in payload["not_claimed"])
    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.append("")
    return "\n".join(lines)
