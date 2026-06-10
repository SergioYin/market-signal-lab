"""Deterministic stress kit for reviewing strategy assumptions."""

from __future__ import annotations

from typing import Any


STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND = (
    "python -m market_signal_lab.cli --strategy-assumption-stress-kit"
)
STRATEGY_ASSUMPTION_STRESS_KIT_SELF_CHECK_COMMAND = "python scripts/selfcheck.py"
STRATEGY_ASSUMPTION_STRESS_KIT_FOCUSED_TEST_COMMAND = (
    "python -m pytest tests/test_strategy_assumption_stress_kit.py "
    "tests/test_selfcheck.py"
)
STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH = (
    "reports/strategy-assumption-stress-kit.md"
)
STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH = (
    "reports/strategy-assumption-stress-kit.json"
)
STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH = (
    "reports/strategy-assumption-stress-kit.html"
)
STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT_PATHS = (
    STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH,
    STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
    STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH,
)
STRATEGY_ASSUMPTION_STRESS_KIT_HTML_TITLE = (
    "Strategy Assumption Stress Kit - Market Signal Lab"
)
STRATEGY_ASSUMPTION_STRESS_KIT_HTML_ARTIFACT_LINKS = (
    ("Markdown kit", "strategy-assumption-stress-kit.md"),
    ("JSON kit", "strategy-assumption-stress-kit.json"),
)

BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "historical_diagnostics_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
    "not_investment_advice": True,
}

STRATEGY_ASSUMPTION_STRESS_KIT_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "assumption_groups",
    "stress_checks",
    "hypothetical_stress_review_outcome",
    "beginner_risk_boundaries",
    "leveraged_etf_like_caveats",
    "do_not_use_for",
    "release_readiness_receipt",
    "verification_commands",
)
ASSUMPTION_GROUP_KEYS = ("group", "assumption", "stress_question")
STRESS_CHECK_KEYS = ("check", "review_prompt", "failure_boundary")
HYPOTHETICAL_STRESS_REVIEW_OUTCOME_KEYS = (
    "fixture_id",
    "review_scope",
    "overall_label",
    "items",
    "research_only_note",
)
HYPOTHETICAL_STRESS_REVIEW_OUTCOME_ITEM_KEYS = (
    "label",
    "check",
    "outcome",
    "review_note",
)
BEGINNER_RISK_BOUNDARY_KEYS = ("boundary", "plain_language_note")
LEVERAGED_ETF_LIKE_CAVEAT_KEYS = ("caveat", "review_note")
RELEASE_READINESS_RECEIPT_KEYS = (
    "receipt_type",
    "rerun_commands",
    "generated_output_paths",
    "boundary_claims",
    "reviewer_notes",
)
RELEASE_READINESS_RERUN_COMMAND_KEYS = (
    "command",
    "purpose",
    "generated_output_paths",
)
RELEASE_READINESS_OUTPUT_PATH_KEYS = ("path", "format", "source_command")
RELEASE_READINESS_BOUNDARY_CLAIM_KEYS = ("claim", "status", "note")

ASSUMPTION_GROUPS = (
    {
        "group": "data_window",
        "assumption": "A result only describes the static rows included in the artifact.",
        "stress_question": "Would the conclusion still be labeled carefully if the date window, symbol mix, or missing rows changed?",
    },
    {
        "group": "signal_rule",
        "assumption": "A strategy rule is a simplified historical model state, not an action instruction.",
        "stress_question": "Does the writeup keep entries, exits, and exposure labels separate from what a reader should do?",
    },
    {
        "group": "costs_and_frictions",
        "assumption": "Fees, spreads, liquidity, taxes, tracking difference, and market impact can change realized outcomes.",
        "stress_question": "Does the artifact avoid treating simplified modeled fees as complete implementation costs?",
    },
    {
        "group": "benchmark_context",
        "assumption": "Same-window benchmarks are reference points for review, not recommendations.",
        "stress_question": "Does the comparison explain underperformance, drawdown, exposure, and fee drag without ranking products for future use?",
    },
)

STRESS_CHECKS = (
    {
        "check": "window_sensitivity",
        "review_prompt": "Re-read the artifact as if the start or end date moved. The claim should remain limited to the supplied static rows.",
        "failure_boundary": "The wording implies the same result applies in another period.",
    },
    {
        "check": "drawdown_tolerance_language",
        "review_prompt": "Confirm max drawdown is presented as a historical diagnostic and not as a loss limit, guarantee, or comfort label.",
        "failure_boundary": "The wording makes a large drawdown sound acceptable, bounded, or suitable for a reader.",
    },
    {
        "check": "fee_drag_visibility",
        "review_prompt": "Confirm fees and friction limits are visible near return and benchmark comparisons.",
        "failure_boundary": "Return comparisons appear without cost, friction, or implementation caveats.",
    },
    {
        "check": "leverage_path_dependency",
        "review_prompt": "For leveraged ETF-like examples, confirm daily reset, path dependency, volatility drag, and extreme drawdown caveats are named.",
        "failure_boundary": "The artifact implies multi-day returns can be read as a simple fixed multiple.",
    },
)

HYPOTHETICAL_STRESS_REVIEW_OUTCOME = {
    "fixture_id": "hypothetical_static_review_001",
    "review_scope": (
        "Example documentation review of one hypothetical strategy writeup; "
        "no market data, portfolio holdings, or account context is used."
    ),
    "overall_label": "WARN",
    "items": (
        {
            "label": "PASS",
            "check": "window_sensitivity",
            "outcome": (
                "The writeup states that conclusions are limited to the fixed "
                "sample rows."
            ),
            "review_note": (
                "PASS means the documentation boundary is visible enough for "
                "research review."
            ),
        },
        {
            "label": "WARN",
            "check": "fee_drag_visibility",
            "outcome": (
                "The writeup mentions modeled fees but separates other "
                "frictions into a later caveat."
            ),
            "review_note": (
                "WARN means reviewers should inspect whether cost and friction "
                "limits are visible near comparison text."
            ),
        },
    ),
    "research_only_note": (
        "This fixture demonstrates PASS/WARN wording for a static review "
        "artifact only; it is not a forecast, suitability view, trading "
        "instruction, or investment advice."
    ),
}

BEGINNER_RISK_BOUNDARIES = (
    {
        "boundary": "research_scope",
        "plain_language_note": "This kit is a static review aid. It does not say what to buy, sell, hold, size, or trade.",
    },
    {
        "boundary": "historical_results",
        "plain_language_note": "Historical sample results are diagnostics from fixed assumptions and rows. They are not predictions of future returns.",
    },
    {
        "boundary": "stress_check_limits",
        "plain_language_note": "A passed stress check means a documentation boundary is visible; it does not prove a strategy is safe, robust, or suitable.",
    },
)

LEVERAGED_ETF_LIKE_CAVEATS = (
    {
        "caveat": "path_dependency",
        "review_note": "Daily reset and compounding can make multi-day outcomes depend heavily on the order of gains and losses.",
    },
    {
        "caveat": "volatility_drag",
        "review_note": "High volatility can reduce compounded results even when the simple average move looks favorable.",
    },
    {
        "caveat": "extreme_drawdown",
        "review_note": "Leveraged ETF-like paths can lose value quickly and may experience severe or near-total drawdowns in adverse paths.",
    },
    {
        "caveat": "implementation_gap",
        "review_note": "Real products can differ from simplified examples because of expenses, financing, tracking difference, spreads, taxes, liquidity, and market impact.",
    },
)

RELEASE_READINESS_RERUN_COMMANDS = (
    {
        "command": STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
        "purpose": (
            "Regenerate the Strategy Assumption Stress Kit Markdown, JSON, "
            "and browser-openable HTML from deterministic stdlib-only code."
        ),
        "generated_output_paths": list(STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT_PATHS),
    },
    {
        "command": STRATEGY_ASSUMPTION_STRESS_KIT_SELF_CHECK_COMMAND,
        "purpose": (
            "Regenerate checked-in sample artifacts and verify the stress-kit "
            "payload, Markdown, HTML, gallery links, and public boundaries."
        ),
        "generated_output_paths": [
            *STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT_PATHS,
            "reports/index.html",
        ],
    },
    {
        "command": STRATEGY_ASSUMPTION_STRESS_KIT_FOCUSED_TEST_COMMAND,
        "purpose": (
            "Run the focused tests that cover the stress-kit schema, rendered "
            "release-readiness receipt, CLI defaults, and selfcheck contract."
        ),
        "generated_output_paths": [],
    },
)

RELEASE_READINESS_OUTPUT_PATHS = (
    {
        "path": STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH,
        "format": "html",
        "source_command": STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
    },
    {
        "path": STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
        "format": "markdown",
        "source_command": STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
    },
    {
        "path": STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH,
        "format": "json",
        "source_command": STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
    },
)

RELEASE_READINESS_BOUNDARY_CLAIMS = (
    {
        "claim": "no_live_data",
        "status": "PASS",
        "note": "The stress-kit command does not read CSV data, call network APIs, or fetch current market data.",
    },
    {
        "claim": "no_broker_or_account",
        "status": "PASS",
        "note": "The artifact has no broker connection, account inspection, order routing, or execution workflow.",
    },
    {
        "claim": "no_orders_or_position_sizing",
        "status": "PASS",
        "note": "The kit records documentation stress checks only and does not size positions or give buy, sell, hold, or trade instructions.",
    },
    {
        "claim": "no_recommendations_or_forecasts",
        "status": "PASS",
        "note": "PASS/WARN labels are review labels for artifact wording, not forecasts, product rankings, or recommendations.",
    },
    {
        "claim": "not_investment_advice",
        "status": "PASS",
        "note": "The receipt preserves the research-only, historical-diagnostics-only, non-advice boundary.",
    },
)

RELEASE_READINESS_REVIEWER_NOTES = (
    "Run commands from the repository root after normal Python setup.",
    "A generated output path is release-ready only when the command exits 0 and the checked-in path is present or updated.",
    "This receipt records deterministic rerun instructions and static boundaries; it does not prove financial correctness, future performance, robustness, suitability, or trading readiness.",
)


def build_strategy_assumption_stress_kit() -> dict[str, Any]:
    """Build a deterministic strategy assumption stress kit payload."""

    return {
        "artifact_type": "strategy_assumption_stress_kit",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "It gives reviewers a static checklist for pressure-testing how a "
            "strategy writeup explains assumptions, stress boundaries, and "
            "leveraged ETF-like caveats without turning the artifact into a "
            "forecast, recommendation, order workflow, or investment advice."
        ),
        "default_outputs": {
            "markdown": STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
            "json": STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH,
        },
        "assumption_groups": _copy_rows(ASSUMPTION_GROUPS),
        "stress_checks": _copy_rows(STRESS_CHECKS),
        "hypothetical_stress_review_outcome": {
            "fixture_id": HYPOTHETICAL_STRESS_REVIEW_OUTCOME["fixture_id"],
            "review_scope": HYPOTHETICAL_STRESS_REVIEW_OUTCOME["review_scope"],
            "overall_label": HYPOTHETICAL_STRESS_REVIEW_OUTCOME[
                "overall_label"
            ],
            "items": [
                dict(item)
                for item in HYPOTHETICAL_STRESS_REVIEW_OUTCOME["items"]
            ],
            "research_only_note": HYPOTHETICAL_STRESS_REVIEW_OUTCOME[
                "research_only_note"
            ],
        },
        "beginner_risk_boundaries": _copy_rows(BEGINNER_RISK_BOUNDARIES),
        "leveraged_etf_like_caveats": _copy_rows(LEVERAGED_ETF_LIKE_CAVEATS),
        "do_not_use_for": [
            "live data workflow",
            "broker, account, or order workflow",
            "position sizing",
            "forecasting future returns",
            "trading recommendation",
            "investment advice",
        ],
        "release_readiness_receipt": {
            "receipt_type": "strategy_assumption_stress_kit_release_readiness",
            "rerun_commands": [
                {
                    **command,
                    "generated_output_paths": list(
                        command["generated_output_paths"]
                    ),
                }
                for command in RELEASE_READINESS_RERUN_COMMANDS
            ],
            "generated_output_paths": [
                dict(item) for item in RELEASE_READINESS_OUTPUT_PATHS
            ],
            "boundary_claims": [
                dict(item) for item in RELEASE_READINESS_BOUNDARY_CLAIMS
            ],
            "reviewer_notes": list(RELEASE_READINESS_REVIEWER_NOTES),
        },
        "verification_commands": [
            STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
            STRATEGY_ASSUMPTION_STRESS_KIT_SELF_CHECK_COMMAND,
            "python -m pytest",
        ],
    }


def render_strategy_assumption_stress_kit(payload: dict[str, Any]) -> str:
    """Render the strategy assumption stress kit payload as Markdown."""

    lines = [
        "# Strategy Assumption Stress Kit",
        "",
        "Use this deterministic static kit to review strategy assumptions, stress checks, beginner risk boundaries, and leveraged ETF-like caveats without treating any item as a prediction, recommendation, trading instruction, order workflow, or investment advice.",
        "",
        "## What This Artifact Is",
        "",
        f"- {payload['purpose']}",
        "- It is generated without live market data, broker connections, account access, orders, forecasts, recommendations, or position sizing.",
        "",
        "## Assumptions To Stress",
        "",
        "| group | assumption | stress question |",
        "|---|---|---|",
    ]
    for item in payload["assumption_groups"]:
        lines.append(
            f"| {item['group']} | {item['assumption']} | {item['stress_question']} |"
        )

    lines.extend(
        [
            "",
            "## Stress Checks",
            "",
            "| check | review prompt | failure boundary |",
            "|---|---|---|",
        ]
    )
    for item in payload["stress_checks"]:
        lines.append(
            f"| {item['check']} | {item['review_prompt']} | {item['failure_boundary']} |"
        )

    example = payload["hypothetical_stress_review_outcome"]
    lines.extend(
        [
            "",
            "## Hypothetical Stress Review Outcome",
            "",
            f"- Fixture: `{example['fixture_id']}`",
            f"- Review scope: {example['review_scope']}",
            f"- Overall label: `{example['overall_label']}`",
            "",
            "| label | check | outcome | review note |",
            "|---|---|---|---|",
        ]
    )
    for item in example["items"]:
        lines.append(
            f"| {item['label']} | {item['check']} | {item['outcome']} | {item['review_note']} |"
        )
    lines.extend(["", f"- {example['research_only_note']}"])

    lines.extend(["", "## Beginner Risk Boundaries", ""])
    for item in payload["beginner_risk_boundaries"]:
        lines.append(f"- **{item['boundary']}**: {item['plain_language_note']}")

    lines.extend(["", "## Leveraged ETF-Like Caveats", ""])
    for item in payload["leveraged_etf_like_caveats"]:
        lines.append(f"- **{item['caveat']}**: {item['review_note']}")

    lines.extend(["", "## Do Not Use This For", ""])
    lines.extend(f"- {item}" for item in payload["do_not_use_for"])

    receipt = payload["release_readiness_receipt"]
    lines.extend(
        [
            "",
            "## Release-Readiness Receipt",
            "",
            f"- Receipt type: `{receipt['receipt_type']}`",
            "",
            "### Exact Rerun Commands",
            "",
        ]
    )
    for item in receipt["rerun_commands"]:
        lines.extend(
            [
                f"- `{item['command']}`",
                f"  - Purpose: {item['purpose']}",
                "  - Generated output paths: "
                + _format_output_paths(item["generated_output_paths"]),
            ]
        )

    lines.extend(["", "### Generated Output Paths", ""])
    for item in receipt["generated_output_paths"]:
        lines.append(
            f"- `{item['path']}` ({item['format']}), from "
            f"`{item['source_command']}`"
        )

    lines.extend(["", "### No-Live-Data / No-Advice Boundaries", ""])
    for item in receipt["boundary_claims"]:
        lines.append(f"- **{item['status']} {item['claim']}**: {item['note']}")

    lines.extend(["", "### Reviewer Notes", ""])
    lines.extend(f"- {item}" for item in receipt["reviewer_notes"])

    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.extend(["", "## Verification Commands", ""])
    lines.extend(f"- `{command}`" for command in payload["verification_commands"])
    lines.append("")
    return "\n".join(lines)


def _format_output_paths(paths: list[str]) -> str:
    if not paths:
        return "`none`"
    return ", ".join(f"`{path}`" for path in paths)


def _copy_rows(rows: tuple[dict[str, str], ...]) -> list[dict[str, str]]:
    return [dict(item) for item in rows]
