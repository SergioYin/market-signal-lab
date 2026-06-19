"""Deterministic static visual capture checklist for cold reviewers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_signal_lab.reviewer_bundle import build_artifact_integrity_summary


STATIC_VISUAL_CAPTURE_CHECKLIST_MARKDOWN_PATH = (
    "reports/static-visual-capture-checklist.md"
)
STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_PATH = (
    "reports/static-visual-capture-checklist.json"
)
STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG = "--static-visual-capture-checklist"
STATIC_VISUAL_CAPTURE_CHECKLIST_COMMAND = (
    "python -m market_signal_lab.cli --static-visual-capture-checklist"
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
}

CAPTURE_SOURCE_PATHS = (
    "reports/index.html",
    "docs/static-gallery-walkthrough.svg",
    "reports/visual-acceptance-bundle.md",
    "reports/visual-walkthrough-evidence-receipt.md",
    "reports/cold-user-review-route.md",
    "reports/public-demo-evidence-receipt.md",
)

STATIC_VISUAL_CAPTURE_CHECKLIST_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "capture_scope",
    "capture_options",
    "checklist",
    "reviewer_script",
    "verification_commands",
    "artifact_integrity_summary",
    "do_not_capture",
    "does_not_prove",
)
STATIC_VISUAL_CAPTURE_DEFAULT_OUTPUT_KEYS = ("markdown", "json")
CAPTURE_OPTION_KEYS = ("format", "target", "capture_instruction", "public_note")
CAPTURE_CHECKLIST_ITEM_KEYS = (
    "step",
    "label",
    "status",
    "review_note",
)

CAPTURE_OPTIONS = (
    {
        "format": "screenshot",
        "target": "reports/index.html",
        "capture_instruction": (
            "Open the checked-in gallery from a local checkout or static host, "
            "wait for the static page to render, and capture the visible first "
            "screen only."
        ),
        "public_note": (
            "The image should show repository-local artifact links and the "
            "research-only/no-live-data boundary, not private browser chrome or "
            "machine-specific paths."
        ),
    },
    {
        "format": "gif",
        "target": "reports/index.html -> docs/static-gallery-walkthrough.svg -> reports/visual-acceptance-bundle.md",
        "capture_instruction": (
            "Record a short local navigation loop through checked-in static "
            "files only, stopping before any terminal, editor, account page, "
            "broker page, or external market-data page appears."
        ),
        "public_note": (
            "The GIF is an orientation aid for the static gallery route only; "
            "it must not imply live status, execution readiness, forecasts, "
            "recommendations, or advice."
        ),
    },
)

CHECKLIST = (
    {
        "step": "open_local_static_gallery",
        "label": "Open the local static gallery",
        "status": "PASS",
        "review_note": (
            "Use `reports/index.html` from the repository or static host. Do "
            "not open broker, account, portfolio, order, or live market-data "
            "pages during capture."
        ),
    },
    {
        "step": "hide_private_context",
        "label": "Hide private context before capture",
        "status": "PASS",
        "review_note": (
            "Crop or arrange the capture so it shows only public-safe artifact "
            "content and repo-relative paths, not private names, absolute "
            "paths, browser profiles, terminals, editors, notifications, or "
            "personal files."
        ),
    },
    {
        "step": "show_boundary_text",
        "label": "Show the no-live/no-advice boundary",
        "status": "PASS",
        "review_note": (
            "Include visible text that the gallery is static research output "
            "with no live data, broker/account access, orders, position sizing, "
            "forecasts, recommendations, or investment advice."
        ),
    },
    {
        "step": "keep_motion_bounded",
        "label": "Keep GIF motion bounded",
        "status": "PASS",
        "review_note": (
            "If recording a GIF, keep it to static navigation among checked-in "
            "gallery, walkthrough, and receipt artifacts. Avoid animations that "
            "look like live signals or execution workflows."
        ),
    },
    {
        "step": "label_capture_as_review_evidence",
        "label": "Label the capture as review evidence",
        "status": "PASS",
        "review_note": (
            "Use neutral copy such as `static gallery capture for review`. Do "
            "not label the asset as a trading signal, forecast, recommendation, "
            "approval, or advice."
        ),
    },
)

REVIEWER_SCRIPT = (
    "Open `reports/index.html` locally, capture the first screen or a short "
    "static navigation GIF, then review the capture for public-safe boundaries "
    "before sharing. The capture is visual orientation evidence only."
)

VERIFICATION_COMMANDS = (
    STATIC_VISUAL_CAPTURE_CHECKLIST_COMMAND,
    "python -m market_signal_lab.cli --visual-acceptance-bundle",
    "python -m market_signal_lab.cli --cold-user-review-route",
    "python scripts/selfcheck.py",
    "python -m pytest tests/test_static_visual_capture_checklist.py tests/test_cli.py",
)

DO_NOT_CAPTURE = (
    "private names, absolute local paths, browser profiles, notifications, terminals, editors, or personal files",
    "broker, account, portfolio, holdings, balances, order tickets, trade confirmations, or position-sizing screens",
    "live market-data pages, auto-refreshing quotes, current prices, or real-time signals",
    "wording that tells viewers to buy, sell, hold, trade, size, forecast, or follow a recommendation",
)

DOES_NOT_PROVE = (
    "financial correctness, future performance, robustness, suitability, or profitability",
    "trading readiness, broker execution readiness, order-routing safety, or position-sizing appropriateness",
    "that any historical diagnostic should be treated as a forecast, recommendation, trading instruction, or investment advice",
)


def build_static_visual_capture_checklist(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a public-safe checklist for local static visual captures."""

    return {
        "artifact_type": "static_visual_capture_checklist",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "Tell cold reviewers how to capture a local static gallery "
            "screenshot or short GIF while preserving public-safe, no-live-data, "
            "no-broker, no-order, no-position-sizing, no-forecast, "
            "no-recommendation, and no-advice boundaries."
        ),
        "default_outputs": {
            "markdown": STATIC_VISUAL_CAPTURE_CHECKLIST_MARKDOWN_PATH,
            "json": STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_PATH,
        },
        "capture_scope": {
            "allowed_sources": list(CAPTURE_SOURCE_PATHS),
            "capture_surface": "checked-in static files opened locally or from a static host",
            "capture_asset_status": "optional reviewer-created visual evidence; not generated by this CLI",
        },
        "capture_options": [dict(option) for option in CAPTURE_OPTIONS],
        "checklist": [dict(item) for item in CHECKLIST],
        "reviewer_script": REVIEWER_SCRIPT,
        "verification_commands": list(VERIFICATION_COMMANDS),
        "artifact_integrity_summary": build_artifact_integrity_summary(
            artifact_root,
            CAPTURE_SOURCE_PATHS,
        ),
        "do_not_capture": list(DO_NOT_CAPTURE),
        "does_not_prove": list(DOES_NOT_PROVE),
    }


def render_static_visual_capture_checklist(payload: dict[str, Any]) -> str:
    """Render the static visual capture checklist as Markdown."""

    integrity = payload["artifact_integrity_summary"]
    lines = [
        "# Static Visual Capture Checklist",
        "",
        payload["purpose"],
        "",
        "## Capture Scope",
        "",
        f"- Capture surface: {payload['capture_scope']['capture_surface']}",
        f"- Capture asset status: {payload['capture_scope']['capture_asset_status']}",
        "- Allowed sources:",
    ]
    lines.extend(
        f"  - `{path}`" for path in payload["capture_scope"]["allowed_sources"]
    )

    lines.extend(["", "## Capture Options", ""])
    for option in payload["capture_options"]:
        lines.extend(
            [
                f"- **{option['format']}**",
                f"  - Target: `{option['target']}`",
                f"  - Instruction: {option['capture_instruction']}",
                f"  - Public note: {option['public_note']}",
            ]
        )

    lines.extend(["", "## Checklist", ""])
    for item in payload["checklist"]:
        lines.extend(
            [
                f"- **{item['label']}** (`{item['status']}`)",
                f"  - Step: `{item['step']}`",
                f"  - Review note: {item['review_note']}",
            ]
        )

    lines.extend(
        [
            "",
            "## Reviewer Script",
            "",
            payload["reviewer_script"],
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

    lines.extend(["", "## Do Not Capture", ""])
    lines.extend(f"- {item}" for item in payload["do_not_capture"])
    lines.extend(["", "## Does Not Prove", ""])
    lines.extend(f"- {item}" for item in payload["does_not_prove"])
    lines.extend(["", "## Verification Commands", ""])
    lines.extend(f"- `{command}`" for command in payload["verification_commands"])
    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.append("")
    return "\n".join(lines)
