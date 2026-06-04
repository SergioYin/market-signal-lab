"""Static reviewer evidence bundle for cold review handoffs."""

from __future__ import annotations

from typing import Any


INSPECTION_STEPS = (
    {
        "step": "open_static_gallery",
        "label": "Open the static gallery first screen",
        "path": "reports/index.html",
        "purpose": "Review checked-in Markdown/JSON/HTML artifacts before installing anything.",
    },
    {
        "step": "read_thesis_ledger_acceptance",
        "label": "Read the thesis-ledger acceptance summary",
        "path": "reports/cross-asset-thesis-ledger-acceptance.md",
        "purpose": "Confirm the cross-asset packet shape and research-boundary checks.",
    },
    {
        "step": "run_acceptance_command",
        "label": "Rerun the deterministic acceptance command",
        "command": "python -m market_signal_lab.cli --validate-thesis-ledger",
        "purpose": "Regenerate the acceptance artifacts from the checked-in JSON packet.",
    },
    {
        "step": "review_methodology_risks",
        "label": "Review methodology and leverage-risk caveats",
        "path": "docs/methodology-audit.md",
        "purpose": "Check look-ahead, survivorship, overfitting, fees/slippage, and daily-reset leveraged ETF risk.",
    },
)


BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
}


def build_reviewer_evidence_bundle() -> dict[str, Any]:
    """Build a deterministic public-safe reviewer evidence bundle payload."""

    return {
        "bundle_type": "reviewer_evidence_bundle",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "primary_route": "reports/index.html -> reports/cross-asset-thesis-ledger-acceptance.md -> python -m market_signal_lab.cli --validate-thesis-ledger",
        "inspection_steps": list(INSPECTION_STEPS),
        "risk_boundaries": [
            "All metrics are historical diagnostics from bundled static/synthetic sample data.",
            "QLD_LIKE and TQQQ_LIKE examples model daily-reset leveraged ETF-like behavior; path dependency, volatility drag, and extreme drawdowns can make multi-day results differ sharply from simple 2x/3x expectations.",
            "The bundle is not a trading bot, signal service, broker workflow, order workflow, position-sizing workflow, forecast engine, recommendation, or investment advice.",
        ],
        "verification_commands": [
            "python -m market_signal_lab.cli --reviewer-evidence-bundle",
            "python -m market_signal_lab.cli --validate-thesis-ledger",
            "python scripts/selfcheck.py",
            "python -m pytest",
        ],
    }


def render_reviewer_evidence_bundle(payload: dict[str, Any]) -> str:
    """Render the reviewer evidence bundle as Markdown."""

    lines = [
        "# Reviewer Evidence Bundle",
        "",
        "This bundle is a compact cold-review handoff for Market Signal Lab. It points a reviewer to the static first screen, the thesis-ledger acceptance artifact, the deterministic rerun command, and the methodology-risk caveats without adding live data, broker/account access, orders, forecasts, recommendations, or investment advice.",
        "",
        "## First-screen route",
        "",
        f"1. Open `{payload['inspection_steps'][0]['path']}` to inspect checked-in sample artifacts before installing anything.",
        f"2. Read `{payload['inspection_steps'][1]['path']}` for the current cross-asset thesis-ledger acceptance summary.",
        f"3. Rerun `{payload['inspection_steps'][2]['command']}` to regenerate the acceptance artifacts from the checked-in JSON packet.",
        f"4. Review `{payload['inspection_steps'][3]['path']}` before treating any historical diagnostic as reusable evidence.",
        "",
        "## Verification commands",
        "",
    ]
    lines.extend(f"- `{command}`" for command in payload["verification_commands"])
    lines.extend(
        [
            "",
            "## Beginner risk boundaries",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in payload["risk_boundaries"])
    lines.extend(
        [
            "",
            "## Boundary flags",
            "",
            f"- research_only: `{payload['research_only']}`",
            f"- static_only: `{payload['static_only']}`",
            f"- no_live_data: `{payload['no_live_data']}`",
            f"- no_broker_or_account: `{payload['no_broker_or_account']}`",
            f"- no_orders_or_position_sizing: `{payload['no_orders_or_position_sizing']}`",
            f"- no_recommendations_or_forecasts: `{payload['no_recommendations_or_forecasts']}`",
            "",
        ]
    )
    return "\n".join(lines)
