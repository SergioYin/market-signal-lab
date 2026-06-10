"""Reviewer acceptance scorecard for public static artifacts."""

from __future__ import annotations

from typing import Any


ARTIFACT_TYPE = "reviewer_acceptance_scorecard"
SCHEMA_VERSION = "1.0"
PASS = "PASS"
WARN = "WARN"

BOUNDARY_FLAG_KEYS = (
    "research_only",
    "static_only",
    "historical_diagnostics_only",
    "no_live_data",
    "no_broker_or_account",
    "no_orders_or_position_sizing",
    "no_recommendations_or_forecasts",
    "not_investment_advice",
)
BOUNDARY_FLAGS = {key: True for key in BOUNDARY_FLAG_KEYS}

REVIEWER_ACCEPTANCE_SCORECARD_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "acceptance_metadata",
    "overall_label",
    "scorecard",
    "risk_boundaries",
    "does_not_prove",
    "artifact_paths",
    "next_actions",
    "verification_commands",
)
REVIEWER_ACCEPTANCE_SCORECARD_ITEM_KEYS = (
    "category",
    "label",
    "status",
    "evidence_paths",
    "review_note",
)
REVIEWER_ACCEPTANCE_NEXT_ACTION_KEYS = (
    "action",
    "label",
    "path_or_command",
    "review_note",
)
REVIEWER_ACCEPTANCE_METADATA_KEYS = (
    "version",
    "generated_by",
    "review_scope",
)

DEFAULT_OUTPUTS = {
    "markdown": "reports/reviewer-acceptance-scorecard.md",
    "json": "reports/reviewer-acceptance-scorecard.json",
}
ACCEPTANCE_METADATA = {
    "version": "1.0",
    "generated_by": "python -m market_signal_lab.cli --reviewer-acceptance-scorecard",
    "review_scope": "static public reviewer acceptance scorecard artifacts",
}

ARTIFACT_PATHS = {
    "public_review_readiness": [
        "reports/index.html",
        "reports/cold-user-review-route.md",
        "reports/reviewer-evidence-bundle.md",
        "reports/beginner-prediction-checklist.md",
    ],
    "reproducibility_evidence": [
        "reports/cross-asset-thesis-ledger.json",
        "reports/cross-asset-thesis-ledger-acceptance.md",
        "reports/cross-asset-thesis-ledger-acceptance.json",
        "reports/sample-manifest.md",
    ],
    "risk_boundaries": [
        "docs/methodology-audit.md",
        "docs/risk-boundaries.md",
        "reports/prediction-readiness-audit.md",
        "reports/prediction-readiness-audit.json",
    ],
}

SCORECARD_ITEMS = (
    {
        "category": "public_review_readiness",
        "label": PASS,
        "status": (
            "Public review starts from checked-in static Markdown, JSON, and "
            "HTML artifacts with first-time-reader route guidance."
        ),
        "evidence_paths": ARTIFACT_PATHS["public_review_readiness"],
        "review_note": (
            "Acceptance means the repository exposes a review route; it does "
            "not approve any trading use or future-performance claim."
        ),
    },
    {
        "category": "reproducibility_evidence",
        "label": PASS,
        "status": (
            "Deterministic CLI commands and checked-in JSON/Markdown artifacts "
            "support local reruns and byte-level review handoffs."
        ),
        "evidence_paths": ARTIFACT_PATHS["reproducibility_evidence"],
        "review_note": (
            "Rerun commands verify artifact generation and shape only, not "
            "financial correctness, robustness, suitability, or profitability."
        ),
    },
    {
        "category": "risk_boundaries",
        "label": PASS,
        "status": (
            "Research-only, static-only, no-live-data, no-broker, no-order, "
            "no-recommendation, and no-advice boundaries are explicit."
        ),
        "evidence_paths": ARTIFACT_PATHS["risk_boundaries"],
        "review_note": (
            "Historical diagnostics remain review context and must not be "
            "converted into predictions, recommendations, or execution cues."
        ),
    },
    {
        "category": "next_actions",
        "label": WARN,
        "status": (
            "Before public citation, reviewers should rerun focused generation "
            "commands and inspect the generated diffs."
        ),
        "evidence_paths": [
            "reports/reviewer-acceptance-scorecard.md",
            "reports/reviewer-acceptance-scorecard.json",
        ],
        "review_note": (
            "WARN is intentional: acceptance is a reviewer checklist state, "
            "not a claim that the artifacts are complete for all audiences."
        ),
    },
)

RISK_BOUNDARIES = (
    "All referenced outputs are static historical research diagnostics.",
    (
        "No scorecard item uses live market data, broker/account access, "
        "orders, or position sizing."
    ),
    (
        "No scorecard item is a forecast, recommendation, trading "
        "instruction, suitability review, or investment advice."
    ),
    (
        "Leveraged ETF-like examples are simplified fixtures and do not model "
        "real product costs, liquidity, taxes, financing, tracking "
        "differences, or market impact."
    ),
)

DOES_NOT_PROVE = (
    (
        "Profitability, future robustness, investment suitability, or "
        "financial correctness."
    ),
    (
        "Trading readiness, broker execution readiness, order-routing safety, "
        "or position-sizing appropriateness."
    ),
    (
        "Completeness for every reviewer audience, regulatory use, compliance "
        "approval, or production deployment."
    ),
)

NEXT_ACTIONS = (
    {
        "action": "regenerate_scorecard",
        "label": "Regenerate the reviewer acceptance scorecard",
        "path_or_command": (
            "python -m market_signal_lab.cli --reviewer-acceptance-scorecard"
        ),
        "review_note": (
            "Refreshes the Markdown and JSON scorecard artifacts from "
            "deterministic static definitions."
        ),
    },
    {
        "action": "rerun_acceptance",
        "label": "Rerun thesis-ledger acceptance",
        "path_or_command": "python -m market_signal_lab.cli --validate-thesis-ledger",
        "review_note": (
            "Checks the public thesis-ledger packet shape and "
            "research-boundary validation output."
        ),
    },
    {
        "action": "inspect_evidence_bundle",
        "label": "Inspect reviewer evidence hashes",
        "path_or_command": "reports/reviewer-evidence-bundle.md",
        "review_note": (
            "Confirms local static artifact bytes at generation time only; "
            "hashes are not financial validation."
        ),
    },
    {
        "action": "run_focused_tests",
        "label": "Run focused scorecard and CLI tests",
        "path_or_command": (
            "python -m pytest tests/test_reviewer_acceptance_scorecard.py "
            "tests/test_cli.py"
        ),
        "review_note": (
            "Keeps acceptance mechanics covered without adding live data or "
            "trading logic."
        ),
    },
)

VERIFICATION_COMMANDS = tuple(
    item["path_or_command"]
    for item in NEXT_ACTIONS
    if item["path_or_command"].startswith("python ")
)


def build_reviewer_acceptance_scorecard() -> dict[str, Any]:
    """Build a deterministic reviewer acceptance scorecard payload."""

    return {
        "artifact_type": ARTIFACT_TYPE,
        "schema_version": SCHEMA_VERSION,
        **BOUNDARY_FLAGS,
        "purpose": (
            "Summarize whether the checked-in Market Signal Lab public review "
            "artifacts are ready for research-only reviewer handoff, with "
            "visible reproducibility evidence, risk boundaries, and next actions."
        ),
        "default_outputs": dict(DEFAULT_OUTPUTS),
        "acceptance_metadata": dict(ACCEPTANCE_METADATA),
        "overall_label": WARN,
        "scorecard": [
            {
                **item,
                "evidence_paths": list(item["evidence_paths"]),
            }
            for item in SCORECARD_ITEMS
        ],
        "risk_boundaries": list(RISK_BOUNDARIES),
        "does_not_prove": list(DOES_NOT_PROVE),
        "artifact_paths": {
            category: list(paths) for category, paths in ARTIFACT_PATHS.items()
        },
        "next_actions": [dict(item) for item in NEXT_ACTIONS],
        "verification_commands": list(VERIFICATION_COMMANDS),
    }


def render_reviewer_acceptance_scorecard(payload: dict[str, Any]) -> str:
    """Render a reviewer acceptance scorecard payload as Markdown."""

    lines = [
        "# Reviewer Acceptance Scorecard",
        "",
        (
            "Static research-only scorecard for public-review readiness, "
            "reproducibility evidence, risk boundaries, and next actions. It "
            "uses no live data, does not connect to brokers, create orders, size "
            "positions, forecast returns, recommend trades, or provide "
            "investment advice."
        ),
        "",
        "## Summary",
        "",
        f"- **Overall label**: {payload['overall_label']}",
        f"- **Purpose**: {payload['purpose']}",
        f"- **Default Markdown**: `{payload['default_outputs']['markdown']}`",
        f"- **Default JSON**: `{payload['default_outputs']['json']}`",
        "",
        "## Metadata",
        "",
        f"- **Version**: {payload['acceptance_metadata']['version']}",
        f"- **Generated by**: `{payload['acceptance_metadata']['generated_by']}`",
        f"- **Review scope**: {payload['acceptance_metadata']['review_scope']}",
        "",
        "## Scorecard",
        "",
        "| Category | Label | Status |",
        "| --- | --- | --- |",
    ]
    for item in payload["scorecard"]:
        lines.append(
            f"| {item['category']} | {item['label']} | {item['status']} |"
        )

    lines.extend(["", "## Evidence Paths", ""])
    for item in payload["scorecard"]:
        lines.append(f"### {item['category']}")
        lines.append("")
        lines.append(f"- **Label**: {item['label']}")
        lines.append(f"- **Review note**: {item['review_note']}")
        lines.extend(f"- `{path}`" for path in item["evidence_paths"])
        lines.append("")

    lines.extend(["## Risk Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in payload["risk_boundaries"])
    lines.extend(["", "## What this does not prove", ""])
    lines.extend(f"- {limitation}" for limitation in payload["does_not_prove"])
    lines.extend(["", "## Next Actions", ""])
    for action in payload["next_actions"]:
        lines.append(f"- **{action['label']}**: `{action['path_or_command']}`")
        lines.append(f"  - {action['review_note']}")

    lines.extend(["", "## Boundary Flags", ""])
    for key in BOUNDARY_FLAG_KEYS:
        lines.append(f"- {key}: `{payload[key]}`")

    lines.append("")
    return "\n".join(lines)
