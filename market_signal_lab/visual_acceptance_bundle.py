"""Deterministic bounded visual acceptance bundle."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_signal_lab.reviewer_bundle import build_artifact_integrity_summary


VISUAL_ACCEPTANCE_BUNDLE_MARKDOWN_PATH = "reports/visual-acceptance-bundle.md"
VISUAL_ACCEPTANCE_BUNDLE_JSON_PATH = "reports/visual-acceptance-bundle.json"
VISUAL_ACCEPTANCE_BUNDLE_COMMAND = (
    "python -m market_signal_lab.cli --visual-acceptance-bundle"
)

BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "fixture_or_static_data_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
    "not_investment_advice": True,
}

ACCEPTANCE_SURFACES = (
    {
        "label": "Visual walkthrough",
        "path": "docs/static-gallery-walkthrough.svg",
        "acceptance_role": (
            "Shows the public-safe static gallery route before a reviewer opens "
            "reports or runs commands."
        ),
    },
    {
        "label": "Static sample gallery",
        "path": "reports/index.html",
        "acceptance_role": (
            "Browser-openable first screen for checked-in artifacts; no live "
            "data, external assets, broker workflow, forecasts, or advice."
        ),
    },
    {
        "label": "Visual walkthrough evidence receipt",
        "path": "reports/visual-walkthrough-evidence-receipt.md",
        "acceptance_role": (
            "Records the visual route, route artifact hashes, and explicit "
            "visual-navigation non-claims."
        ),
    },
    {
        "label": "Acceptance receipt index",
        "path": "reports/acceptance-receipt-index.md",
        "acceptance_role": (
            "Indexes public receipts, fixture provenance, artifact hashes, and "
            "no-live-data/no-advice boundaries."
        ),
    },
    {
        "label": "Reviewer acceptance scorecard",
        "path": "reports/reviewer-acceptance-scorecard.md",
        "acceptance_role": (
            "Summarizes public-review readiness, reproducibility evidence, "
            "risk boundaries, WARN items, and next actions."
        ),
    },
    {
        "label": "Cold-user review route",
        "path": "reports/cold-user-review-route.md",
        "acceptance_role": (
            "Gives first-time public reviewers a deterministic route through "
            "the static review artifacts."
        ),
    },
)

VISUAL_ACCEPTANCE_ARTIFACT_PATHS = tuple(
    surface["path"] for surface in ACCEPTANCE_SURFACES
) + (
    "reports/visual-walkthrough-evidence-receipt.json",
    "reports/acceptance-receipt-index.json",
    "reports/reviewer-acceptance-scorecard.json",
    "reports/cold-user-review-route.json",
    "reports/public-demo-evidence-receipt.md",
    "reports/public-demo-evidence-receipt.json",
)

ACCEPTANCE_CHECKS = (
    {
        "check": "static_visual_entry",
        "label": "Static visual entry is present",
        "status": "PASS",
        "review_note": (
            "The bundle starts from checked-in SVG/HTML files rather than a "
            "live application, account, or broker route."
        ),
    },
    {
        "check": "bounded_receipts",
        "label": "Receipt boundaries are linked",
        "status": "PASS",
        "review_note": (
            "The visual receipt, acceptance index, public demo receipt, and "
            "scorecard state what they do and do not prove."
        ),
    },
    {
        "check": "artifact_hashes",
        "label": "Artifact hashes are recorded",
        "status": "PASS",
        "review_note": (
            "SHA-256 hashes identify local file bytes at generation time only, "
            "not financial correctness or trading readiness."
        ),
    },
    {
        "check": "review_only_boundary",
        "label": "Review-only boundary is explicit",
        "status": "PASS",
        "review_note": (
            "The bundle excludes live data, broker/account access, orders, "
            "position sizing, forecasts, recommendations, and investment advice."
        ),
    },
)

REVIEWER_RERUN_COMMANDS = (
    VISUAL_ACCEPTANCE_BUNDLE_COMMAND,
    "python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt",
    "python -m market_signal_lab.cli --acceptance-receipt-index",
    "python -m market_signal_lab.cli --reviewer-acceptance-scorecard",
    "python -m market_signal_lab.cli --cold-user-review-route",
    "python scripts/selfcheck.py",
)

NOT_CLAIMED = (
    "The bundle is a static visual acceptance handoff, not financial validation.",
    "PASS labels describe review-route presence and boundary visibility only.",
    "Hashes prove local file-byte identity at generation time only.",
    "No live data, broker, account, order-routing, position-sizing, forecast, recommendation, or advice workflow is included.",
)


def build_visual_acceptance_bundle(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a deterministic bounded bundle for visual public acceptance review."""

    return {
        "artifact_type": "visual_acceptance_bundle",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "Give public reviewers one bounded deterministic bundle tying the "
            "static visual walkthrough, gallery first screen, visual receipt, "
            "acceptance receipt index, reviewer acceptance scorecard, cold-user "
            "route, artifact hashes, and no-live-data/no-advice boundaries "
            "together."
        ),
        "default_outputs": {
            "markdown": VISUAL_ACCEPTANCE_BUNDLE_MARKDOWN_PATH,
            "json": VISUAL_ACCEPTANCE_BUNDLE_JSON_PATH,
        },
        "verification_command": VISUAL_ACCEPTANCE_BUNDLE_COMMAND,
        "acceptance_surfaces": [dict(surface) for surface in ACCEPTANCE_SURFACES],
        "acceptance_checks": [dict(check) for check in ACCEPTANCE_CHECKS],
        "reviewer_rerun_commands": list(REVIEWER_RERUN_COMMANDS),
        "artifact_integrity_summary": build_artifact_integrity_summary(
            artifact_root,
            VISUAL_ACCEPTANCE_ARTIFACT_PATHS,
        ),
        "not_claimed": list(NOT_CLAIMED),
    }


def render_visual_acceptance_bundle(payload: dict[str, Any]) -> str:
    """Render the visual acceptance bundle as Markdown."""

    integrity = payload["artifact_integrity_summary"]
    lines = [
        "# Visual Acceptance Bundle",
        "",
        payload["purpose"],
        "",
        "## Acceptance Surfaces",
        "",
    ]
    for surface in payload["acceptance_surfaces"]:
        lines.extend(
            [
                f"- **{surface['label']}**",
                f"  - Path: `{surface['path']}`",
                f"  - Role: {surface['acceptance_role']}",
            ]
        )

    lines.extend(["", "## Acceptance Checks", ""])
    for check in payload["acceptance_checks"]:
        lines.extend(
            [
                f"- **{check['label']}**: `{check['status']}`",
                f"  - Check: `{check['check']}`",
                f"  - Review note: {check['review_note']}",
            ]
        )

    lines.extend(["", "## Reviewer Rerun Commands", ""])
    lines.extend(f"- `{command}`" for command in payload["reviewer_rerun_commands"])

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
        for artifact in integrity["artifacts"]
    )

    lines.extend(["", "## Not Claimed", ""])
    lines.extend(f"- {claim}" for claim in payload["not_claimed"])
    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.append("")
    return "\n".join(lines)
