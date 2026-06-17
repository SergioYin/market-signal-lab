"""Deterministic visual walkthrough evidence receipt."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_signal_lab.reviewer_bundle import build_artifact_integrity_summary


VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_MARKDOWN_PATH = (
    "reports/visual-walkthrough-evidence-receipt.md"
)
VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_JSON_PATH = (
    "reports/visual-walkthrough-evidence-receipt.json"
)
VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_COMMAND = (
    "python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt"
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

VISUAL_WALKTHROUGH_ARTIFACT_PATHS = (
    "docs/static-gallery-walkthrough.svg",
    "reports/index.html",
    "reports/public-demo-evidence-receipt.md",
    "reports/public-demo-evidence-receipt.json",
    "reports/reviewer-rerun-receipt.md",
    "reports/reviewer-rerun-receipt.json",
)

WALKTHROUGH_LINKS = (
    {
        "label": "Static gallery walkthrough",
        "path": "docs/static-gallery-walkthrough.svg",
        "evidence_role": (
            "Visual entry point showing the static gallery path a cold reviewer "
            "can inspect before running commands."
        ),
    },
    {
        "label": "Static sample gallery",
        "path": "reports/index.html",
        "evidence_role": (
            "Browser-openable public first screen with no JavaScript, external "
            "assets, live data, broker workflow, orders, forecasts, or advice."
        ),
    },
    {
        "label": "Public demo evidence receipt",
        "path": "reports/public-demo-evidence-receipt.md",
        "evidence_role": (
            "Receipt for gallery/backtest artifacts, fixture boundaries, hashes, "
            "and no-live-data/no-advice claims."
        ),
    },
    {
        "label": "Reviewer rerun receipt",
        "path": "reports/reviewer-rerun-receipt.md",
        "evidence_role": (
            "Receipt for deterministic public rerun commands and expected "
            "review artifacts."
        ),
    },
    {
        "label": "Acceptance receipt index",
        "path": "reports/acceptance-receipt-index.md",
        "evidence_role": (
            "Index tying public receipts, fixture provenance, artifact hashes, "
            "and non-advice boundaries together."
        ),
    },
)

REVIEWER_STEPS = (
    "Open docs/static-gallery-walkthrough.svg to see the intended static gallery path.",
    "Open reports/index.html from local checked-in files, not from a live app or broker workflow.",
    "Compare reports/public-demo-evidence-receipt.md with its JSON output for artifact hashes and source boundaries.",
    "Read reports/reviewer-rerun-receipt.md for deterministic commands and expected artifacts.",
    "Finish with reports/acceptance-receipt-index.md before treating any artifact as public-review evidence.",
)

NOT_CLAIMED = (
    "The SVG is visual navigation evidence only; it does not prove financial correctness.",
    "This receipt does not execute commands or fetch live market data.",
    "The acceptance receipt index is linked as a route step, but not hashed here because it indexes this receipt.",
    "No broker, account, order-routing, position-sizing, forecast, recommendation, or advice workflow is included.",
    "SHA-256 hashes identify local file bytes at generation time only.",
)


def build_visual_walkthrough_evidence_receipt(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a deterministic receipt for the public visual walkthrough route."""

    return {
        "artifact_type": "visual_walkthrough_evidence_receipt",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "Give cold public reviewers one deterministic receipt tying the "
            "static gallery walkthrough SVG, public gallery, public demo "
            "evidence receipt, reviewer rerun receipt, and acceptance receipt "
            "index into a review-only route."
        ),
        "default_outputs": {
            "markdown": VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_MARKDOWN_PATH,
            "json": VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_JSON_PATH,
        },
        "verification_command": VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_COMMAND,
        "reviewer_steps": list(REVIEWER_STEPS),
        "walkthrough_links": [dict(link) for link in WALKTHROUGH_LINKS],
        "artifact_integrity_summary": build_artifact_integrity_summary(
            artifact_root,
            VISUAL_WALKTHROUGH_ARTIFACT_PATHS,
        ),
        "not_claimed": list(NOT_CLAIMED),
    }


def render_visual_walkthrough_evidence_receipt(payload: dict[str, Any]) -> str:
    """Render the visual walkthrough evidence receipt as Markdown."""

    integrity = payload["artifact_integrity_summary"]
    lines = [
        "# Visual Walkthrough Evidence Receipt",
        "",
        payload["purpose"],
        "",
        "## Reviewer Steps",
        "",
    ]
    lines.extend(
        f"{index}. {step}" for index, step in enumerate(payload["reviewer_steps"], 1)
    )

    lines.extend(["", "## Walkthrough Links", ""])
    for link in payload["walkthrough_links"]:
        lines.extend(
            [
                f"- **{link['label']}**",
                f"  - Path: `{link['path']}`",
                f"  - Role: {link['evidence_role']}",
            ]
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
