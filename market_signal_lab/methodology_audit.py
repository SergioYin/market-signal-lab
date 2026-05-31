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
METHODOLOGY_AUDIT_STATUS_VALUES = ("PASS", "WARN", "FAIL")
METHODOLOGY_AUDIT_PROMOTION_GATE = {
    "PASS": "promote",
    "WARN": "promote_with_warnings",
    "FAIL": "do_not_promote",
}


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
        "review_status_values": list(METHODOLOGY_AUDIT_STATUS_VALUES),
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


def score_methodology_audit_review(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and score a reviewer-filled methodology audit JSON object."""

    if not isinstance(payload, dict):
        raise ValueError("Methodology audit review must be a JSON object")

    checks = validate_methodology_audit_review_checks(payload)
    scored_checks: list[dict[str, str]] = []
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}

    for row in checks:
        check_name = row["check"]
        status = row["status"].upper()
        notes = row["notes"]
        counts[status] += 1
        scored_checks.append(
            {
                "check": check_name,
                "status": status,
                "notes": notes,
            }
        )

    gate = _methodology_audit_promotion_gate(counts)
    return {
        "summary_type": "methodology_audit_score",
        "schema_version": "1.0",
        "research_only": True,
        "static_only": True,
        "no_live_data": True,
        "no_broker_or_account": True,
        "no_orders_or_position_sizing": True,
        "no_recommendations_or_forecasts": True,
        "source_document": "docs/methodology-audit.md",
        "artifact_reviewed": _optional_string(payload, "artifact_reviewed"),
        "reviewer": _optional_string(payload, "reviewer"),
        "review_date": _optional_string(payload, "review_date"),
        "counts": {
            "pass": counts["PASS"],
            "warn": counts["WARN"],
            "fail": counts["FAIL"],
        },
        "promotion_gate_suggestion": gate,
        "promotion_gate_reason": _promotion_gate_reason(gate),
        "checks": scored_checks,
        "note": (
            "Offline methodology-audit scoring summary from reviewer-entered "
            "PASS/WARN/FAIL statuses only; not investment advice, not a "
            "recommendation, not a forecast, and not a live-data, broker, "
            "account, order, or position-sizing workflow."
        ),
    }


def validate_methodology_audit_review_checks(
    payload: dict[str, Any],
) -> list[dict[str, str]]:
    """Return normalized review rows or raise a clear schema-style error."""

    checks = payload.get("checks")
    if not isinstance(checks, list):
        raise ValueError("Methodology audit review must contain a checks list")

    expected_checks = [row["check"] for row in METHODOLOGY_AUDIT_CHECKS]
    if len(checks) != len(expected_checks):
        raise ValueError(
            "Methodology audit checks must contain exactly "
            f"{len(expected_checks)} rows in template order"
        )

    normalized: list[dict[str, str]] = []
    status_values = ", ".join(METHODOLOGY_AUDIT_STATUS_VALUES)
    for index, row in enumerate(checks, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"checks[{index}] must be a JSON object")

        expected_check = expected_checks[index - 1]
        check_name = row.get("check")
        if not isinstance(check_name, str) or not check_name:
            raise ValueError(f"checks[{index}].check must be a non-empty string")
        if check_name != expected_check:
            raise ValueError(
                f"checks[{index}].check must be {expected_check!r}, "
                f"got {check_name!r}"
            )

        status = row.get("status")
        if not isinstance(status, str):
            raise ValueError(
                f"{check_name}: status must be one of {status_values}"
            )
        status = status.upper()
        if status not in METHODOLOGY_AUDIT_STATUS_VALUES:
            raise ValueError(
                f"{check_name}: invalid status {row.get('status')!r}; "
                f"expected one of {status_values}"
            )

        notes = row.get("notes", "")
        if notes is None:
            notes = ""
        if not isinstance(notes, str):
            raise ValueError(f"{check_name}: notes must be a string when supplied")

        normalized.append(
            {
                "check": check_name,
                "status": status,
                "notes": notes,
            }
        )

    return normalized


def render_methodology_audit_score(summary: dict[str, Any]) -> str:
    """Render a methodology audit score summary as Markdown."""

    counts = summary["counts"]
    lines = [
        "# Methodology Audit Score",
        "",
        summary["note"],
        "",
        "## Reviewer Metadata",
        "",
        f"- **Artifact reviewed**: {summary['artifact_reviewed'] or 'Not supplied'}",
        f"- **Reviewer**: {summary['reviewer'] or 'Not supplied'}",
        f"- **Review date**: {summary['review_date'] or 'Not supplied'}",
        f"- **Source checklist**: `{summary['source_document']}`",
        "",
        "## Score Summary",
        "",
        f"- **PASS**: {counts['pass']}",
        f"- **WARN**: {counts['warn']}",
        f"- **FAIL**: {counts['fail']}",
        (
            "- **Promotion gate suggestion**: "
            f"{summary['promotion_gate_suggestion']}"
        ),
        f"- **Reason**: {summary['promotion_gate_reason']}",
        "",
        "## Audit Checks",
        "",
        "| Check | Status | Reviewer notes |",
        "| --- | --- | --- |",
    ]
    for row in summary["checks"]:
        lines.append(
            "| {check} | {status} | {notes} |".format(
                check=_escape_table_cell(row["check"]),
                status=row["status"],
                notes=_escape_table_cell(row["notes"]),
            )
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This scorer only summarizes a local reviewer-filled JSON file. It "
            "does not read market data, fetch live data, connect to brokers, "
            "inspect accounts, route orders, size positions, forecast, "
            "recommend, certify strategy quality, or provide investment advice.",
            "",
        ]
    )
    return "\n".join(lines)


def _methodology_audit_promotion_gate(counts: dict[str, int]) -> str:
    if counts["FAIL"]:
        return METHODOLOGY_AUDIT_PROMOTION_GATE["FAIL"]
    if counts["WARN"]:
        return METHODOLOGY_AUDIT_PROMOTION_GATE["WARN"]
    return METHODOLOGY_AUDIT_PROMOTION_GATE["PASS"]


def _promotion_gate_reason(gate: str) -> str:
    if gate == "do_not_promote":
        return "At least one audit check is marked FAIL."
    if gate == "promote_with_warnings":
        return "No FAIL statuses, but at least one audit check is marked WARN."
    return "All audit checks are marked PASS."


def _optional_string(payload: dict[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string when supplied")
    return value


def _escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
