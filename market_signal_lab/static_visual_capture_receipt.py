"""Deterministic receipt for static visual capture evidence artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_signal_lab.reviewer_bundle import build_artifact_integrity_summary


STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH = (
    "reports/static-visual-capture-receipt.md"
)
STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH = "reports/static-visual-capture-receipt.json"
STATIC_VISUAL_CAPTURE_RECEIPT_FLAG = "--static-visual-capture-receipt"
STATIC_VISUAL_CAPTURE_RECEIPT_COMMAND = (
    "python -m market_signal_lab.cli --static-visual-capture-receipt"
)

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

STATIC_VISUAL_CAPTURE_RECEIPT_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "verification_command",
    "capture_receipt_scope",
    "scanned_artifacts",
    "artifact_integrity_summary",
    "public_evidence_notes",
    "not_claimed",
)
STATIC_VISUAL_CAPTURE_RECEIPT_DEFAULT_OUTPUT_KEYS = ("markdown", "json")
STATIC_VISUAL_CAPTURE_RECEIPT_SCOPE_KEYS = (
    "scan_surface",
    "source_policy",
    "capture_asset_policy",
)
STATIC_VISUAL_CAPTURE_RECEIPT_ARTIFACT_KEYS = (
    "path",
    "status",
    "byte_count",
    "sha256",
    "role",
    "route",
    "regeneration_command",
    "public_evidence_note",
)

STATIC_VISUAL_CAPTURE_ARTIFACTS = (
    {
        "path": "reports/index.html",
        "role": "static_gallery_first_screen",
        "route": "open local static gallery before inspecting review artifacts",
        "regeneration_command": "python scripts/selfcheck.py",
        "public_evidence_note": (
            "Browser-openable static gallery with no JavaScript, external "
            "assets, live data, broker/account workflow, orders, forecasts, "
            "recommendations, or advice."
        ),
    },
    {
        "path": "docs/static-gallery-walkthrough.svg",
        "role": "visual_walkthrough_map",
        "route": "start with walkthrough, then open reports/index.html",
        "regeneration_command": "python scripts/selfcheck.py",
        "public_evidence_note": (
            "Static SVG route map for public orientation only; it is not a "
            "live signal surface or execution workflow."
        ),
    },
    {
        "path": "reports/visual-acceptance-bundle.md",
        "role": "visual_acceptance_handoff",
        "route": "gallery -> visual bundle -> linked receipts",
        "regeneration_command": "python -m market_signal_lab.cli --visual-acceptance-bundle",
        "public_evidence_note": (
            "Markdown handoff tying static visual artifacts, hashes, reviewer "
            "checks, and no-live-data/no-advice boundaries together."
        ),
    },
    {
        "path": "reports/visual-acceptance-bundle.json",
        "role": "visual_acceptance_handoff_json",
        "route": "machine-readable pair for reports/visual-acceptance-bundle.md",
        "regeneration_command": "python -m market_signal_lab.cli --visual-acceptance-bundle",
        "public_evidence_note": (
            "Structured visual acceptance evidence for deterministic review."
        ),
    },
    {
        "path": "reports/visual-walkthrough-evidence-receipt.md",
        "role": "walkthrough_route_receipt",
        "route": "walkthrough SVG -> gallery -> demo receipt -> rerun receipt -> acceptance index",
        "regeneration_command": "python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt",
        "public_evidence_note": (
            "Receipt for the static visual walkthrough route and linked public "
            "review evidence."
        ),
    },
    {
        "path": "reports/visual-walkthrough-evidence-receipt.json",
        "role": "walkthrough_route_receipt_json",
        "route": "machine-readable pair for reports/visual-walkthrough-evidence-receipt.md",
        "regeneration_command": "python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt",
        "public_evidence_note": (
            "Structured receipt for deterministic walkthrough-route review."
        ),
    },
    {
        "path": "reports/static-visual-capture-checklist.md",
        "role": "capture_safety_checklist",
        "route": "read before creating any local screenshot or GIF",
        "regeneration_command": "python -m market_signal_lab.cli --static-visual-capture-checklist",
        "public_evidence_note": (
            "Checklist for keeping optional reviewer-created captures public "
            "safe and bounded to static local artifacts."
        ),
    },
    {
        "path": "reports/static-visual-capture-checklist.json",
        "role": "capture_safety_checklist_json",
        "route": "machine-readable pair for reports/static-visual-capture-checklist.md",
        "regeneration_command": "python -m market_signal_lab.cli --static-visual-capture-checklist",
        "public_evidence_note": (
            "Structured checklist with source hashes and do-not-capture rules."
        ),
    },
    {
        "path": "reports/cold-user-review-route.md",
        "role": "cold_reviewer_route",
        "route": "first-time public reviewer orientation path",
        "regeneration_command": "python -m market_signal_lab.cli --cold-user-review-route",
        "public_evidence_note": (
            "Static orientation route only; it does not approve financial "
            "correctness, execution readiness, forecasts, recommendations, or "
            "advice."
        ),
    },
    {
        "path": "reports/cold-user-review-route.json",
        "role": "cold_reviewer_route_json",
        "route": "machine-readable pair for reports/cold-user-review-route.md",
        "regeneration_command": "python -m market_signal_lab.cli --cold-user-review-route",
        "public_evidence_note": "Structured cold-review route evidence.",
    },
    {
        "path": "reports/public-demo-evidence-receipt.md",
        "role": "public_demo_receipt",
        "route": "gallery and fixture-boundary evidence receipt",
        "regeneration_command": "python -m market_signal_lab.cli --public-demo-evidence-receipt",
        "public_evidence_note": (
            "Public receipt for static sample artifacts, fixture boundaries, "
            "hashes, and non-advice claims."
        ),
    },
    {
        "path": "reports/public-demo-evidence-receipt.json",
        "role": "public_demo_receipt_json",
        "route": "machine-readable pair for reports/public-demo-evidence-receipt.md",
        "regeneration_command": "python -m market_signal_lab.cli --public-demo-evidence-receipt",
        "public_evidence_note": "Structured public demo evidence receipt.",
    },
    {
        "path": "docs/static-gallery-manifest.md",
        "role": "static_gallery_manifest_doc",
        "route": "documentation map for the static gallery link contract",
        "regeneration_command": "python scripts/selfcheck.py",
        "public_evidence_note": (
            "Documentation for the static gallery contract using repo-relative "
            "paths only."
        ),
    },
)

STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS = tuple(
    artifact["path"] for artifact in STATIC_VISUAL_CAPTURE_ARTIFACTS
)

PUBLIC_EVIDENCE_NOTES = (
    "All paths are repo-relative and intended for public static review.",
    "SHA-256 values identify local file bytes at generation time only.",
    "The receipt records existing static artifacts; it does not create screenshots or GIFs.",
    "Optional captures must follow the static visual capture checklist before sharing.",
)

NOT_CLAIMED = (
    "No live market data, broker, account, order, portfolio, holdings, or position-sizing surface is scanned.",
    "No forecast, recommendation, buy/sell/hold advice, suitability review, or investment advice is provided.",
    "Hashes do not validate financial correctness, future performance, robustness, profitability, or trading readiness.",
    "The receipt does not inspect private files, private paths, browser profiles, terminals, editors, notifications, or secrets.",
)


def build_static_visual_capture_receipt(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a deterministic receipt for static visual capture evidence."""

    integrity = build_artifact_integrity_summary(
        artifact_root,
        STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS,
    )
    artifacts_by_path = {
        artifact["path"]: artifact for artifact in integrity["artifacts"]
    }
    scanned_artifacts = [
        _scanned_artifact_record(artifact, artifacts_by_path[artifact["path"]])
        for artifact in STATIC_VISUAL_CAPTURE_ARTIFACTS
    ]

    return {
        "artifact_type": "static_visual_capture_receipt",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "Scan the existing static visual, gallery, walkthrough, route, and "
            "checklist artifacts that support a public-safe local visual "
            "capture handoff, recording relative paths, presence, byte counts, "
            "SHA-256 hashes, roles, routes, known regeneration commands, and "
            "public evidence notes."
        ),
        "default_outputs": {
            "markdown": STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH,
            "json": STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH,
        },
        "verification_command": STATIC_VISUAL_CAPTURE_RECEIPT_COMMAND,
        "capture_receipt_scope": {
            "scan_surface": "checked-in static visual/gallery/walkthrough/checklist artifacts only",
        "source_policy": "repo-relative public artifacts; no private paths, secrets, live data, or external services",
            "capture_asset_policy": "optional reviewer-created screenshots or GIFs are not generated or hashed by this receipt; no live data is captured",
        },
        "scanned_artifacts": scanned_artifacts,
        "artifact_integrity_summary": integrity,
        "public_evidence_notes": list(PUBLIC_EVIDENCE_NOTES),
        "not_claimed": list(NOT_CLAIMED),
    }


def _scanned_artifact_record(
    artifact: dict[str, str],
    integrity_record: dict[str, Any],
) -> dict[str, Any]:
    return {
        "path": artifact["path"],
        "status": integrity_record["status"],
        "byte_count": integrity_record["byte_count"],
        "sha256": integrity_record["sha256"],
        "role": artifact["role"],
        "route": artifact["route"],
        "regeneration_command": artifact["regeneration_command"],
        "public_evidence_note": artifact["public_evidence_note"],
    }


def render_static_visual_capture_receipt(payload: dict[str, Any]) -> str:
    """Render the static visual capture receipt as Markdown."""

    integrity = payload["artifact_integrity_summary"]
    lines = [
        "# Static Visual Capture Receipt",
        "",
        payload["purpose"],
        "",
        "## Scope",
        "",
        f"- Scan surface: {payload['capture_receipt_scope']['scan_surface']}",
        f"- Source policy: {payload['capture_receipt_scope']['source_policy']}",
        f"- Capture asset policy: {payload['capture_receipt_scope']['capture_asset_policy']}",
        f"- Verification command: `{payload['verification_command']}`",
        "",
        "## Scanned Artifacts",
        "",
        "| Path | Status | Bytes | SHA-256 | Role | Route | Regeneration command | Public evidence note |",
        "| --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        "| {path} | {status} | {byte_count} | {sha256} | {role} | {route} | `{regeneration_command}` | {public_evidence_note} |".format(
            path=artifact["path"],
            status=artifact["status"],
            byte_count=artifact["byte_count"],
            sha256=artifact["sha256"] or "missing",
            role=artifact["role"],
            route=artifact["route"],
            regeneration_command=artifact["regeneration_command"],
            public_evidence_note=artifact["public_evidence_note"],
        )
        for artifact in payload["scanned_artifacts"]
    )
    lines.extend(
        [
            "",
            "## Artifact Integrity Summary",
            "",
            f"- Integrity status: `{integrity['integrity_status']}`",
            f"- Interpretation: {integrity['interpretation']}",
            f"- Caveat: {integrity['caveat']}",
            f"- Algorithm: `{integrity['algorithm']}`",
            f"- Scope: {integrity['scope']}",
            f"- Present artifacts: `{integrity['present_count']}` of `{integrity['artifact_count']}`",
            "",
            "## Public Evidence Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in payload["public_evidence_notes"])
    lines.extend(["", "## Not Claimed", ""])
    lines.extend(f"- {claim}" for claim in payload["not_claimed"])
    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.append("")
    return "\n".join(lines)
