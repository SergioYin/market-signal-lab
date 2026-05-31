"""Static methodology audit template for public reviewers."""

from __future__ import annotations

from typing import Any


METHODOLOGY_AUDIT_CHECKS: tuple[dict[str, str], ...] = (
    {
        "check": "Look-ahead bias",
        "pass_evidence": (
            "Indicators, ranks, and exposure states are described as historical "
            "diagnostics over the supplied rows; same-period buy-and-hold "
            "comparisons are labeled as comparisons, not predictions."
        ),
        "warn_or_fail_evidence": (
            "The report implies future prices, future ranks, or full-sample "
            "outcomes were available when historical decisions were modeled."
        ),
    },
    {
        "check": "Survivorship bias",
        "pass_evidence": (
            "Input files, placeholder symbols, synthetic/static fixture labels, "
            "and provenance are visible. The artifact does not claim a live or "
            "complete market universe."
        ),
        "warn_or_fail_evidence": (
            "The artifact treats a small sample or surviving symbols as proof "
            "of broad market performance."
        ),
    },
    {
        "check": "Overfitting",
        "pass_evidence": (
            "Sweep rankings and train/test diagnostics are framed as review "
            "prompts. `robustness_flag` labels are not described as proof of "
            "stability."
        ),
        "warn_or_fail_evidence": (
            "The artifact treats the top sweep row as the best future setting "
            "or hides how many parameters were tried."
        ),
    },
    {
        "check": "Fees and slippage",
        "pass_evidence": (
            "`fee_bps`, modeled fee drag, and cost caveats are visible. Missing "
            "slippage, taxes, financing, liquidity, and market-impact modeling "
            "are named as limitations."
        ),
        "warn_or_fail_evidence": (
            "Costs are absent, or results are presented as deployable without "
            "explicit cost assumptions and omissions."
        ),
    },
    {
        "check": "Daily reset leveraged ETF risk",
        "pass_evidence": (
            "Leveraged ETF-like labels are described as placeholders or "
            "simplified fixtures. Daily reset, path dependency, magnified "
            "losses, and unmodeled real fund costs are visible."
        ),
        "warn_or_fail_evidence": (
            "Multi-day leveraged returns are treated like a simple multiple of "
            "index return, or real fund behavior is implied from the fixture."
        ),
    },
    {
        "check": "Live trading and advice boundary",
        "pass_evidence": (
            "The artifact says it is research-only and does not add broker, "
            "live-data, account, order, position-sizing, recommendation, "
            "forecast, or advice workflows."
        ),
        "warn_or_fail_evidence": (
            "The artifact contains instructions to trade, claims live signals, "
            "or implies suitability for an account."
        ),
    },
)

METHODOLOGY_AUDIT_REVIEW_NOTES: tuple[str, ...] = (
    "Prefer reproducibility evidence over performance claims: input path, row "
    "count, date range, parameters, manifest, and JSON fields matter more than "
    "a high return value.",
    "Treat short synthetic samples as format and workflow fixtures only.",
    "Treat sweep and split-sweep outputs as questions to investigate, not "
    "model-selection proof.",
    "Treat leveraged ETF-like examples as risk-boundary examples, not product "
    "simulations.",
    "If a report lacks enough information to evaluate any row in the table, "
    "mark that row `WARN` or `FAIL` and ask for the missing artifact rather "
    "than inferring it.",
)

METHODOLOGY_AUDIT_NOTE = (
    "Static methodology audit template for reviewing checked-in research "
    "artifacts only; not investment advice, not a recommendation, not a "
    "forecast, not a validation of future performance, and not a live-trading, "
    "broker, account, order, or position-sizing workflow."
)


def build_methodology_audit_template() -> dict[str, Any]:
    """Return the compact static JSON payload for the audit template."""

    return {
        "template_type": "methodology_audit_template",
        "schema_version": "1.0",
        "research_only": True,
        "static_only": True,
        "no_live_data": True,
        "no_broker_or_account": True,
        "no_orders_or_position_sizing": True,
        "no_recommendations_or_forecasts": True,
        "note": METHODOLOGY_AUDIT_NOTE,
        "review_status_values": ["PASS", "WARN", "FAIL"],
        "checks": list(METHODOLOGY_AUDIT_CHECKS),
        "review_notes": list(METHODOLOGY_AUDIT_REVIEW_NOTES),
        "source_document": "docs/methodology-audit.md",
    }


def render_methodology_audit_template(payload: dict[str, Any]) -> str:
    """Render the static audit template as Markdown."""

    lines = [
        "# Methodology Audit Template",
        "",
        METHODOLOGY_AUDIT_NOTE,
        "",
        "Use this reviewer template alongside `docs/methodology-audit.md`. "
        "For each item below, record `PASS`, `WARN`, or `FAIL`. A `PASS` means "
        "the artifact gives enough information for review. It does not mean "
        "the strategy is reliable, suitable for trading, or likely to work in "
        "future data.",
        "",
        "## Reviewer Metadata",
        "",
        "- **Artifact reviewed**:",
        "- **Reviewer**:",
        "- **Review date**:",
        "- **Input path / manifest checked**:",
        "- **Result**: PASS / WARN / FAIL",
        "",
        "## Audit Checks",
        "",
        "| Check | Status | PASS evidence | WARN or FAIL evidence | Reviewer notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in payload["checks"]:
        lines.append(
            "| {check} |  | {pass_evidence} | {warn_or_fail_evidence} |  |".format(
                **check
            )
        )
    lines.extend(
        [
            "",
            "## Review Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in payload["review_notes"])
    lines.extend(
        [
            "",
            "## Out Of Scope",
            "",
            "This audit does not certify a strategy, approve a model, validate "
            "live performance, estimate tax impact, model real fund operations, "
            "evaluate order execution, or determine account suitability for "
            "buying, selling, holding, trading, or sizing a position.",
            "",
        ]
    )
    return "\n".join(lines)
