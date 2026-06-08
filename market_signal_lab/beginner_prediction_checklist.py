"""Beginner checklist for reading historical backtest artifacts safely."""

from __future__ import annotations

from typing import Any


BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "historical_diagnostics_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
}

BEGINNER_PREDICTION_CHECKLIST_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "public_reviewer_reuse_reason",
    "default_outputs",
    "recommended_sources_to_open",
    "reading_steps",
    "do_not_use_for",
    "risk_boundaries",
    "verification_commands",
)

BEGINNER_PREDICTION_CHECKLIST_DEFAULT_OUTPUT_KEYS = ("markdown", "json")
BEGINNER_PREDICTION_CHECKLIST_READING_STEP_KEYS = (
    "step",
    "label",
    "beginner_note",
)

READING_STEPS = (
    {
        "step": "identify_artifact",
        "label": "Identify what file you are reading",
        "beginner_note": "A backtest report is a historical review artifact. It describes how a model behaved under fixed assumptions on supplied rows.",
    },
    {
        "step": "check_source_window",
        "label": "Check the source rows and date range",
        "beginner_note": "Results only describe the included historical rows, symbols, fees, and strategy settings. Changing any of those inputs can change the result.",
    },
    {
        "step": "read_metrics_as_diagnostics",
        "label": "Read returns, drawdown, and exposure as diagnostics",
        "beginner_note": "Metrics summarize that historical run. They are not instructions and do not predict future returns or prices.",
    },
    {
        "step": "compare_buy_and_hold",
        "label": "Compare with same-period buy-and-hold",
        "beginner_note": "The comparison is a same-window historical reference point, not guidance about what to buy, sell, or hold.",
    },
    {
        "step": "review_risk_boundaries",
        "label": "Review the risk boundaries before sharing",
        "beginner_note": "Do not turn sample diagnostics into advice, forecasts, position sizes, order steps, or claims about future returns.",
    },
)

RISK_BOUNDARIES = {
    "historical_backtest_limits": (
        "Historical backtests and related checklist artifacts are limited to the "
        "supplied rows, fixed assumptions, and simplified calculations. They are "
        "examples for review only, not evidence of future returns."
    ),
    "leveraged_etf_daily_reset_path_dependency": (
        "Leveraged ETF-like examples require extra caution. QLD_LIKE and "
        "TQQQ_LIKE are placeholder examples for risk review, not guidance about "
        "QLD, TQQQ, or any leveraged ETF. Daily reset mechanics make multi-day "
        "outcomes path-dependent; volatility drag and compounding can make "
        "realized paths differ sharply from simple 2x/3x expectations, and "
        "losses can grow quickly."
    ),
    "scope_limits": (
        "Static artifact only. No live-data workflow, broker or account workflow, "
        "orders or order routing, position sizing, recommendation engine, forecast "
        "engine, or investment advice is provided."
    ),
}

BEGINNER_PREDICTION_CHECKLIST_RISK_BOUNDARY_KEYS = tuple(RISK_BOUNDARIES)


def build_beginner_prediction_checklist() -> dict[str, Any]:
    """Build a deterministic beginner-readable checklist payload."""

    return {
        "artifact_type": "beginner_prediction_checklist",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "It explains how to read a historical backtest or a related review "
            "checklist without treating either one as a prediction of future "
            "returns, recommendation, or advice."
        ),
        "public_reviewer_reuse_reason": (
            "Public reviewers can reference this artifact as a deterministic "
            "static review template for checking whether backtest writeups keep "
            "historical results separate from future-return predictions, "
            "recommendations, trading instructions, and investment advice."
        ),
        "default_outputs": {
            "markdown": "reports/beginner-prediction-checklist.md",
            "json": "reports/beginner-prediction-checklist.json",
        },
        "recommended_sources_to_open": [
            "reports/sample-report.md",
            "reports/sample-report.json",
            "reports/pretrade-packet.md",
            "reports/scenario-card.md",
            "docs/methodology-audit.md",
            "docs/risk-boundaries.md",
        ],
        "reading_steps": [dict(step) for step in READING_STEPS],
        "do_not_use_for": [
            "prediction of future returns",
            "investment advice",
            "trading recommendation",
            "live execution or signal use",
            "broker, account, or order workflow",
            "position sizing",
        ],
        "risk_boundaries": dict(RISK_BOUNDARIES),
        "verification_commands": [
            "python -m market_signal_lab.cli --beginner-prediction-checklist",
            "python scripts/selfcheck.py",
            "python -m pytest",
        ],
    }


def render_beginner_prediction_checklist(payload: dict[str, Any]) -> str:
    """Render the beginner prediction checklist as Markdown."""

    lines = [
        "# Beginner Backtest Reading Checklist",
        "",
        "Use this static checklist to read historical backtest artifacts without treating sample results, labels, or checked items as predictions of future returns, recommendations, trading instructions, or investment advice.",
        "",
        "## What This Artifact Is",
        "",
        f"- {payload['purpose']}",
        "- It is deterministic and generated without live market data, broker connections, account access, orders, or position sizing.",
        "",
        "## Why Public Reviewers Might Reference It",
        "",
        f"- {payload['public_reviewer_reuse_reason']}",
        "",
        "## First-Use Route",
        "",
        "1. Open `reports/sample-report.md`.",
        "2. Keep this checklist beside that report and use the steps below before opening the other static sources.",
        "3. To regenerate the checklist from the repo root, run `python -m market_signal_lab.cli --beginner-prediction-checklist`.",
        "",
        "## How To Read A Historical Backtest",
        "",
    ]
    for index, step in enumerate(payload["reading_steps"], start=1):
        lines.append(f"{index}. **{step['label']}**: {step['beginner_note']}")

    lines.extend(
        [
            "",
            "## Open These Static Sources",
            "",
        ]
    )
    lines.extend(
        f"- [{path}]({_relative_markdown_link(path)})"
        for path in payload["recommended_sources_to_open"]
    )

    boundaries = payload["risk_boundaries"]
    lines.extend(
        [
            "",
            "## Risk Boundaries",
            "",
            f"- **Historical backtest limits**: {boundaries['historical_backtest_limits']}",
            f"- **Leveraged ETF daily-reset and path-dependency risk**: {boundaries['leveraged_etf_daily_reset_path_dependency']}",
            f"- **Scope limits**: {boundaries['scope_limits']}",
            "",
            "## Do Not Use This For",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["do_not_use_for"])
    lines.extend(
        [
            "",
            "## Boundary Flags",
            "",
        ]
    )
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.extend(
        [
            "",
            "## Verification Commands",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in payload["verification_commands"])
    lines.append("")
    return "\n".join(lines)


def _relative_markdown_link(path: str) -> str:
    """Return a link target relative to reports/beginner-prediction-checklist.md."""

    if path.startswith("reports/"):
        return path.removeprefix("reports/")
    if path.startswith("docs/"):
        return f"../{path}"
    return path
