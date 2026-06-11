"""Deterministic quickstart card for the Strategy Assumption Stress Kit."""

from __future__ import annotations

from typing import Any

from market_signal_lab.strategy_assumption_stress_kit import (
    STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH,
    STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
)


STRESS_KIT_QUICKSTART_CARD_FLAG = "--stress-kit-quickstart-card"
STRESS_KIT_QUICKSTART_CARD_COMMAND = (
    "python -m market_signal_lab.cli --stress-kit-quickstart-card"
)
STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH = (
    "reports/stress-kit-quickstart-card.md"
)
STRESS_KIT_QUICKSTART_CARD_JSON_PATH = "reports/stress-kit-quickstart-card.json"
STRESS_KIT_QUICKSTART_CARD_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    "research_only",
    "static_only",
    "no_live_data",
    "no_broker_or_account",
    "no_orders_or_position_sizing",
    "no_recommendations_or_forecasts",
    "not_investment_advice",
    "boundary_claims",
    "purpose",
    "estimated_review_time_minutes",
    "source_artifact",
    "default_outputs",
    "reviewer_checklist",
    "stop_conditions",
    "completion_receipt",
    "do_not_use_for",
)
QUICKSTART_REVIEWER_CHECKLIST_ITEM_KEYS = (
    "step",
    "time_box",
    "check",
    "question",
    "pass_condition",
)
QUICKSTART_STOP_CONDITION_KEYS = ("condition", "reviewer_action")
QUICKSTART_COMPLETION_RECEIPT_KEYS = (
    "source_command",
    "generated_output_paths",
    "review_boundary",
)

QUICKSTART_BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
    "not_investment_advice": True,
}

QUICKSTART_BOUNDARY_CLAIMS = {
    "no_live_data": (
        "This card is generated from static definitions only and does not "
        "fetch, stream, refresh, or inspect live market data."
    ),
    "not_investment_advice": (
        "This card is a reviewer checklist only, not a forecast, "
        "recommendation, trading instruction, suitability view, or "
        "investment advice."
    ),
}

QUICKSTART_OUT_OF_SCOPE_ITEMS = (
    "live data workflow",
    "broker, account, or order workflow",
    "position sizing",
    "forecast or recommendation surface",
    "investment-advice surface",
)

REVIEWER_CHECKLIST = (
    {
        "step": "scope",
        "time_box": "0:00-0:20",
        "check": "Confirm the artifact names a fixed static review scope.",
        "question": "Does the writeup limit every conclusion to the supplied artifact and sample window?",
        "pass_condition": "The text says the review is static, historical, and bounded to the artifact.",
    },
    {
        "step": "assumptions",
        "time_box": "0:20-0:45",
        "check": "Find the strategy rule, data-window, benchmark, and cost assumptions.",
        "question": "Can a reviewer see what assumptions would need stress testing before reading results?",
        "pass_condition": "Key assumptions are explicit and are not phrased as action instructions.",
    },
    {
        "step": "stress_language",
        "time_box": "0:45-1:15",
        "check": "Scan for overclaiming around drawdown, fees, benchmarks, and robustness.",
        "question": "Would the wording still be accurate if another static window or fee assumption looked worse?",
        "pass_condition": "Claims stay diagnostic and avoid guarantees, forecasts, or product rankings.",
    },
    {
        "step": "leveraged_etf_like_caveats",
        "time_box": "1:15-1:40",
        "check": "Verify daily reset, path dependency, volatility drag, and extreme drawdown caveats are visible when leveraged ETF-like examples appear.",
        "question": "Does the artifact avoid implying a simple fixed multiple over multiple days?",
        "pass_condition": "Leveraged ETF-like caveats are framed as simplified historical diagnostics, not advice.",
    },
    {
        "step": "boundaries",
        "time_box": "1:40-2:00",
        "check": "Confirm no live data, broker, account, order, position-sizing, recommendation, forecast, or advice surface is present.",
        "question": "Could a cold reviewer mistake this artifact for something to act on?",
        "pass_condition": "The artifact stays a documentation review checklist only.",
    },
)

STOP_CONDITIONS = (
    {
        "condition": "A claim reads like a prediction, recommendation, suitability view, or trading instruction.",
        "reviewer_action": "Mark WARN or FAIL and request boundary wording before promotion.",
    },
    {
        "condition": "Live data, broker, account, order, or position-sizing behavior appears in the artifact path.",
        "reviewer_action": "Stop using this quickstart card; it is scoped only to static review artifacts.",
    },
)


def build_stress_kit_quickstart_card() -> dict[str, Any]:
    """Build a deterministic two-minute quickstart-card payload."""

    return {
        "artifact_type": "stress_kit_quickstart_card",
        "schema_version": "1.0",
        **QUICKSTART_BOUNDARY_FLAGS,
        "boundary_claims": dict(QUICKSTART_BOUNDARY_CLAIMS),
        "purpose": (
            "Condense the Strategy Assumption Stress Kit into a two-minute "
            "reviewer checklist for static artifact boundary review."
        ),
        "estimated_review_time_minutes": 2,
        "source_artifact": {
            "name": "Strategy Assumption Stress Kit",
            "markdown_path": STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
            "json_path": STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH,
        },
        "default_outputs": {
            "markdown": STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
            "json": STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
        },
        "reviewer_checklist": [dict(item) for item in REVIEWER_CHECKLIST],
        "stop_conditions": [dict(item) for item in STOP_CONDITIONS],
        "completion_receipt": {
            "source_command": STRESS_KIT_QUICKSTART_CARD_COMMAND,
            "generated_output_paths": [
                STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
                STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
            ],
            "review_boundary": (
                "Completion means the checklist was reviewed for static "
                "documentation boundaries only; it does not validate financial "
                "correctness, robustness, suitability, or future performance."
            ),
        },
        "do_not_use_for": list(QUICKSTART_OUT_OF_SCOPE_ITEMS),
    }


def render_stress_kit_quickstart_card(payload: dict[str, Any]) -> str:
    """Render the quickstart card payload as Markdown."""

    source = payload["source_artifact"]
    receipt = payload["completion_receipt"]
    lines = [
        "# Stress Kit Quickstart Card",
        "",
        "Use this deterministic two-minute card to review the Strategy Assumption Stress Kit boundary before promoting a static research artifact.",
        "",
        "## Source",
        "",
        f"- Source artifact: {source['name']}",
        f"- Markdown: `{source['markdown_path']}`",
        f"- JSON: `{source['json_path']}`",
        "",
        "## Two-Minute Reviewer Checklist",
        "",
        "| time box | step | check | pass condition |",
        "|---|---|---|---|",
    ]
    for item in payload["reviewer_checklist"]:
        lines.append(
            f"| {item['time_box']} | {item['step']} | {item['check']} "
            f"{item['question']} | {item['pass_condition']} |"
        )

    lines.extend(["", "## Stop Conditions", ""])
    for item in payload["stop_conditions"]:
        lines.append(f"- **{item['condition']}** {item['reviewer_action']}")

    lines.extend(
        [
            "",
            "## Completion Receipt",
            "",
            f"- Source command: `{receipt['source_command']}`",
            "- Generated output paths: "
            + ", ".join(f"`{path}`" for path in receipt["generated_output_paths"]),
            f"- Review boundary: {receipt['review_boundary']}",
            "",
            "## Boundaries",
            "",
        ]
    )
    lines.extend(f"- {key}: `{payload[key]}`" for key in QUICKSTART_BOUNDARY_FLAGS)
    lines.extend(["", "## Boundary Claims", ""])
    lines.extend(f"- {claim}" for claim in payload["boundary_claims"].values())
    lines.extend(["", "## Do Not Use This For", ""])
    lines.extend(f"- {item}" for item in payload["do_not_use_for"])
    lines.append("")
    return "\n".join(lines)
