"""Deterministic assumption ledger summary for cold reviewers."""

from __future__ import annotations

from typing import Any


ASSUMPTION_LEDGER_SUMMARY_COMMAND = (
    "python -m market_signal_lab.cli --assumption-ledger-summary"
)
ASSUMPTION_LEDGER_SUMMARY_MARKDOWN_PATH = (
    "reports/assumption-ledger-summary.md"
)
ASSUMPTION_LEDGER_SUMMARY_JSON_PATH = "reports/assumption-ledger-summary.json"

BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
    "not_investment_advice": True,
}
BOUNDARY_CLAIMS = {
    "no_live_data": (
        "This summary is generated from deterministic static definitions only "
        "and does not fetch, stream, refresh, or inspect live market data."
    ),
    "not_investment_advice": (
        "This summary is a reviewer ledger only, not a forecast, "
        "recommendation, trading instruction, suitability view, or investment "
        "advice."
    ),
}

ASSUMPTION_LEDGER_SUMMARY_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "boundary_claims",
    "purpose",
    "default_outputs",
    "strategy_assumptions",
    "risk_boundaries",
    "generated_evidence_paths",
    "not_claimed",
    "reviewer_use",
    "verification_commands",
)
ASSUMPTION_ITEM_KEYS = ("name", "summary", "review_boundary")
RISK_BOUNDARY_KEYS = ("boundary", "plain_language_note")
EVIDENCE_PATH_KEYS = ("path", "format", "review_use")
NOT_CLAIMED_KEYS = ("claim", "reason")

STRATEGY_ASSUMPTIONS = (
    {
        "name": "static_sample_scope",
        "summary": "Results and labels describe deterministic checked-in sample artifacts only.",
        "review_boundary": "Do not extend any result to live markets, another date window, another product, or an account.",
    },
    {
        "name": "historical_signal_state",
        "summary": "Entries, exits, exposure, and strategy states are historical model diagnostics.",
        "review_boundary": "They are not buy, sell, hold, rebalance, sizing, or timing instructions.",
    },
    {
        "name": "cost_and_friction_limits",
        "summary": "Modeled fees are review inputs, while spreads, taxes, liquidity, financing, tracking difference, and market impact remain caveats.",
        "review_boundary": "Do not treat simplified costs as a complete implementation model.",
    },
    {
        "name": "same_window_benchmarking",
        "summary": "Benchmark comparisons are same-period context for artifact review.",
        "review_boundary": "They are not product rankings, forward expectations, or recommendations.",
    },
)

RISK_BOUNDARIES = (
    {
        "boundary": "research_scope",
        "plain_language_note": "The ledger summarizes documentation assumptions and static evidence paths only.",
    },
    {
        "boundary": "historical_diagnostics",
        "plain_language_note": "Historical metrics are sample diagnostics, not forecasts, guarantees, or loss limits.",
    },
    {
        "boundary": "leveraged_etf_like_examples",
        "plain_language_note": "Leveraged ETF-like samples require daily reset, path dependency, volatility drag, tracking, and severe drawdown caveats.",
    },
    {
        "boundary": "review_labels",
        "plain_language_note": "PASS, WARN, and FAIL labels describe artifact-review boundaries, not strategy quality or suitability.",
    },
)

GENERATED_EVIDENCE_PATHS = (
    {
        "path": "reports/index.html",
        "format": "html",
        "review_use": "First screen for checked-in static sample artifacts.",
    },
    {
        "path": "reports/strategy-assumption-stress-kit.html",
        "format": "html",
        "review_use": "Full assumption and stress-boundary review kit.",
    },
    {
        "path": "reports/stress-kit-quickstart-card.md",
        "format": "markdown",
        "review_use": "Two-minute route into no-advice stress-kit review.",
    },
    {
        "path": "reports/reviewer-evidence-bundle.md",
        "format": "markdown",
        "review_use": "Cold-review handoff with local artifact hash summary.",
    },
    {
        "path": ASSUMPTION_LEDGER_SUMMARY_MARKDOWN_PATH,
        "format": "markdown",
        "review_use": "This compact assumption ledger summary.",
    },
    {
        "path": ASSUMPTION_LEDGER_SUMMARY_JSON_PATH,
        "format": "json",
        "review_use": "Structured version of this compact assumption ledger summary.",
    },
)

NOT_CLAIMED = (
    {
        "claim": "future_performance",
        "reason": "Static historical diagnostics do not predict future returns or risk.",
    },
    {
        "claim": "tradability_or_execution",
        "reason": "The artifact has no broker, account, order, routing, fill, or execution workflow.",
    },
    {
        "claim": "position_size_or_suitability",
        "reason": "No portfolio, account, risk tolerance, tax, liquidity, or suitability context is used.",
    },
    {
        "claim": "recommendation_or_advice",
        "reason": "The ledger is a review aid and does not tell a reader what to buy, sell, hold, size, or trade.",
    },
)


def build_assumption_ledger_summary() -> dict[str, Any]:
    """Build a deterministic public-safe assumption ledger summary."""

    return {
        "artifact_type": "assumption_ledger_summary",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "boundary_claims": dict(BOUNDARY_CLAIMS),
        "purpose": (
            "Give cold reviewers one compact ledger of strategy assumptions, "
            "risk boundaries, generated evidence paths, and explicit "
            "non-claims without reading live data or creating any advice "
            "surface."
        ),
        "default_outputs": {
            "markdown": ASSUMPTION_LEDGER_SUMMARY_MARKDOWN_PATH,
            "json": ASSUMPTION_LEDGER_SUMMARY_JSON_PATH,
        },
        "strategy_assumptions": _copy_rows(STRATEGY_ASSUMPTIONS),
        "risk_boundaries": _copy_rows(RISK_BOUNDARIES),
        "generated_evidence_paths": _copy_rows(GENERATED_EVIDENCE_PATHS),
        "not_claimed": _copy_rows(NOT_CLAIMED),
        "reviewer_use": [
            "Open this after the static gallery when reviewing public maturity.",
            "Use it to check whether assumptions and no-advice boundaries are visible before reading deeper artifacts.",
            "Treat every path as generated static evidence, not as financial validation.",
        ],
        "verification_commands": [
            ASSUMPTION_LEDGER_SUMMARY_COMMAND,
            "python scripts/selfcheck.py",
            "python -m pytest",
        ],
    }


def render_assumption_ledger_summary(payload: dict[str, Any]) -> str:
    """Render the assumption ledger summary as Markdown."""

    lines = [
        "# Assumption Ledger Summary",
        "",
        "This deterministic static artifact gives cold reviewers one place to check strategy assumptions, risk boundaries, generated evidence paths, and what Market Signal Lab is not claiming. Read it as a map of the artifact's assumptions and limits, not as a verdict on strategy quality or suitability. It does not read live data, connect to brokers or accounts, route orders, size positions, forecast, recommend, or provide investment advice.",
        "",
        "## Purpose",
        "",
        f"- {payload['purpose']}",
        "",
        "## Strategy Assumptions",
        "",
        "| assumption | summary | review boundary |",
        "|---|---|---|",
    ]
    for item in payload["strategy_assumptions"]:
        lines.append(
            f"| {item['name']} | {item['summary']} | {item['review_boundary']} |"
        )

    lines.extend(["", "## Risk Boundaries", ""])
    for item in payload["risk_boundaries"]:
        lines.append(f"- **{item['boundary']}**: {item['plain_language_note']}")

    lines.extend(
        [
            "",
            "## Generated Evidence Paths",
            "",
            "| path | format | review use |",
            "|---|---|---|",
        ]
    )
    for item in payload["generated_evidence_paths"]:
        linked_path = _markdown_artifact_link(item["path"])
        lines.append(
            f"| {linked_path} | {item['format']} | {item['review_use']} |"
        )

    lines.extend(
        [
            "",
            "## What Is Not Being Claimed",
            "",
            "| claim not made | reason |",
            "|---|---|",
        ]
    )
    for item in payload["not_claimed"]:
        lines.append(f"| {item['claim']} | {item['reason']} |")

    lines.extend(["", "## Reviewer Use", ""])
    lines.extend(f"- {item}" for item in payload["reviewer_use"])
    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.extend(["", "## Boundary Claims", ""])
    lines.extend(f"- {claim}" for claim in payload["boundary_claims"].values())
    lines.extend(["", "## Verification Commands", ""])
    lines.extend(f"- `{command}`" for command in payload["verification_commands"])
    lines.append("")
    return "\n".join(lines)


def _copy_rows(rows: tuple[dict[str, str], ...]) -> list[dict[str, str]]:
    return [dict(item) for item in rows]


def _markdown_artifact_link(path: str) -> str:
    target = path.removeprefix("reports/")
    return f"[`{path}`]({target})"
