"""Reviewer decision-matrix artifact for static backtest promotion review."""

from __future__ import annotations

from typing import Any

from market_signal_lab.packet import LEVERAGED_ETF_RISK_BOUNDARY


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


REVIEWER_DECISION_MATRIX_RELEASE_GATE_KEY = "release_gate"
REVIEWER_DECISION_MATRIX_PROMOTION_GATE_KEY = "promotion_gate"
REVIEWER_DECISION_MATRIX_GATES_READING_HEADING_KEY = "heading"
REVIEWER_DECISION_MATRIX_GATES_READING_DISCLAIMER_KEY = "disclaimer"

REVIEWER_DECISION_MATRIX_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "source_artifact",
    "purpose",
    "default_outputs",
    "gates_reading",
    "summary",
    "decision_categories",
    "public_boundaries",
    "verification_commands",
)

REVIEWER_DECISION_MATRIX_GATES_READING_KEYS = (
    REVIEWER_DECISION_MATRIX_GATES_READING_HEADING_KEY,
    REVIEWER_DECISION_MATRIX_RELEASE_GATE_KEY,
    REVIEWER_DECISION_MATRIX_PROMOTION_GATE_KEY,
    REVIEWER_DECISION_MATRIX_GATES_READING_DISCLAIMER_KEY,
)


REVIEWER_DECISION_MATRIX_SUMMARY_KEYS = (
    REVIEWER_DECISION_MATRIX_RELEASE_GATE_KEY,
    REVIEWER_DECISION_MATRIX_PROMOTION_GATE_KEY,
    "pass_count",
    "warn_count",
    "fail_count",
)


REVIEWER_DECISION_MATRIX_CATEGORY_KEYS = (
    "criterion",
    "label",
    "evidence",
    "review_note",
)

REVIEWER_DECISION_MATRIX_PUBLIC_BOUNDARIES = (
    (
        "This matrix is a static historical research review aid only; it does "
        "not provide investment advice, trading guidance, recommendations, "
        "forecasts, buy/sell/hold signals, order steps, or position sizing."
    ),
    (
        "No generated field, PASS/WARN/FAIL label, or gate result validates "
        "financial correctness, profitability, suitability, or future "
        "performance."
    ),
    LEVERAGED_ETF_RISK_BOUNDARY,
)


PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
GATE_RESULT_OPTIONS = frozenset({PASS, WARN, FAIL})

GATES_READING_HEADING = "How to Read the Gates"

REVIEWER_DECISION_MATRIX_VERIFICATION_COMMANDS = (
    "python -m market_signal_lab.cli --reviewer-decision-matrix",
    "python -m market_signal_lab.cli --prediction-readiness-audit",
    "python -m market_signal_lab.cli --reviewer-rerun-receipt",
    "python -m pytest",
)


DECISION_CATEGORIES = (
    {
        "criterion": "data_provenance",
        "label": PASS,
        "evidence": (
            "Checked-in artifacts are generated from bundled historical CSV files "
            "and checked into provenance sidecar metadata in examples/data."
        ),
        "review_note": (
            "PASS means provenance is explicit and static; reviewers should still "
            "confirm source paths before promoting."
        ),
    },
    {
        "criterion": "benchmark_comparison",
        "label": PASS,
        "evidence": (
            "Static backtest summaries include same-period buy-and-hold comparison "
            "for each configured asset and a strategy-minus-buy-and-hold delta."
        ),
        "review_note": (
            "The benchmark is a historical reference and does not imply future "
            "superiority."
        ),
    },
    {
        "criterion": "fee_drawdown_disclosure",
        "label": PASS,
        "evidence": (
            "Fee drag and max drawdown fields are present in historical metrics, "
            "with explicit notes about modeled fee assumptions."
        ),
        "review_note": (
            "PASS means baseline fee/drawdown exposure is disclosed; promote only "
            "after confirming fee model assumptions in the exact artifact build path."
        ),
    },
    {
        "criterion": "train_test_robustness",
        "label": WARN,
        "evidence": (
            "Train/test metadata is generated only when split options are used and "
            "should be checked on a split run before deciding."
        ),
        "review_note": (
            "WARN means this artifact should be reviewed with train/test run "
            "outputs before any promotion-grade approval."
        ),
    },
    {
        "criterion": "beginner_risk_language",
        "label": PASS,
        "evidence": (
            "Beginner-facing documentation includes no-prediction, no-advice, and "
            "path-dependent risk wording for leveraged examples."
        ),
        "review_note": (
            "PASS indicates suitable language for first-time reviewers and "
            "non-specialist audiences."
        ),
    },
    {
        "criterion": "leveraged_etf_caveat",
        "label": PASS,
        "evidence": (
            "Leveraged ETF-like fixtures are explicitly flagged as simplified examples "
            "with path-dependent daily reset and volatility drag caveats."
        ),
        "review_note": (
            "PASS means the caveat appears in artifact-facing documentation and "
            "risk text."
        ),
    },
    {
        "criterion": "reproducibility_evidence",
        "label": PASS,
        "evidence": (
            "This matrix is generated with reproducible static CLI commands that output "
            "markdown and JSON without live market inputs."
        ),
        "review_note": (
            "PASS means a reviewer can rerun generation locally to validate "
            "consistency before promotion."
        ),
    },
    {
        "criterion": "no_advice_boundary",
        "label": PASS,
        "evidence": (
            "Static artifact flags explicitly disallow live data, broker/account, "
            "order, recommendations, forecasts, and investment-advice workflows."
        ),
        "review_note": (
            "PASS confirms the primary non-advice boundary is stated and preserved "
            "in this artifact package."
        ),
    },
)


def build_reviewer_decision_matrix() -> dict[str, Any]:
    """Build a deterministic reviewer decision-matrix payload."""

    categories = [dict(category) for category in DECISION_CATEGORIES]
    labels = [item["label"] for item in categories]
    return {
        "artifact_type": "reviewer_decision_matrix",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "source_artifact": "reports/sample-report.json",
        "purpose": (
            "Help cold reviewers decide whether a checked static backtest artifact "
            "is safe for release and what must be completed before broader "
            "promotion."
        ),
        "default_outputs": {
            "markdown": "reports/reviewer-decision-matrix.md",
            "json": "reports/reviewer-decision-matrix.json",
        },
        "gates_reading": {
            REVIEWER_DECISION_MATRIX_GATES_READING_HEADING_KEY: GATES_READING_HEADING,
            REVIEWER_DECISION_MATRIX_RELEASE_GATE_KEY: (
                "Release Gate is about whether this static review artifact is "
                "safe to release for people to inspect; PASS is clear, WARN means "
                "release is okay for review but still needs follow-up before "
                "promotion."
            ),
            REVIEWER_DECISION_MATRIX_PROMOTION_GATE_KEY: (
                "Promotion Gate is about whether the artifact is ready for broader "
                "public sharing, documentation, and demo quality. It only turns "
                "PASS when all categories are suitable for public presentation."
            ),
            REVIEWER_DECISION_MATRIX_GATES_READING_DISCLAIMER_KEY: [
                "A Release Gate PASS/WARN result is not a buy/sell signal.",
                (
                    "Promotion Gate is about public demo quality, not proof of "
                    "strategy profitability."
                ),
            ],
        },
        "summary": {
            REVIEWER_DECISION_MATRIX_RELEASE_GATE_KEY: _decision_gate(labels, allow_warning=True),
            REVIEWER_DECISION_MATRIX_PROMOTION_GATE_KEY: _decision_gate(labels, allow_warning=False),
            "pass_count": labels.count(PASS),
            "warn_count": labels.count(WARN),
            "fail_count": labels.count(FAIL),
        },
        "decision_categories": categories,
        "public_boundaries": list(REVIEWER_DECISION_MATRIX_PUBLIC_BOUNDARIES),
        "verification_commands": list(REVIEWER_DECISION_MATRIX_VERIFICATION_COMMANDS),
    }


def render_reviewer_decision_matrix(payload: dict[str, Any]) -> str:
    """Render the decision matrix payload as Markdown."""

    summary = dict(payload.get("summary", {}))
    gates_reading = payload.get("gates_reading", {})
    lines = [
        "# Reviewer Decision Matrix",
        "",
        (
            "Use this static review matrix to decide whether a public-facing static "
            "backtest artifact can be released and whether any barriers remain "
            "before promotion. It does not generate "
            "trading signals, predictions, recommendations, or investment advice."
        ),
        "",
        "## Source and Scope",
        f"- **Source artifact**: {payload.get('source_artifact', 'unknown')}",
        f"- **Purpose**: {payload.get('purpose', '')}",
        "",
        "## Decision Gates",
        f"- **Release Gate**: {summary.get('release_gate', 'UNKNOWN')}",
        f"- **Promotion Gate**: {summary.get('promotion_gate', 'UNKNOWN')}",
        (
        f"- **Score counts**: pass={summary.get('pass_count', 0)} / "
        f"warn={summary.get('warn_count', 0)} / fail={summary.get('fail_count', 0)}"
        ),
        "- PASS means static evidence does not block release.",
        "- WARN means release may proceed only for review but requires additional run-time checks "
        "before promotion.",
        "- FAIL means the artifact should not be released or promoted.",
        "",
        *_gates_reading_lines(gates_reading),
        "",
        "## Decision Criteria",
        "| criterion | label | evidence | review note |",
        "|---|---|---|---|",
    ]

    for category in payload.get("decision_categories", ()):
        lines.append(
            "| "
            f"{category.get('criterion', '')} | "
            f"{category.get('label', '')} | "
            f"{category.get('evidence', '')} | "
            f"{category.get('review_note', '')} |"
        )

    lines.extend(
        [
            "",
            "## Public Boundaries",
            *(f"- {boundary}" for boundary in payload.get("public_boundaries", ())),
            "",
            "## Verification Commands",
            *(f"- `{command}`" for command in REVIEWER_DECISION_MATRIX_VERIFICATION_COMMANDS),
            "",
        ]
    )

    lines.extend(
        [
            "## Boundary Flags",
            *[f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS],
            "",
        ]
    )
    return "\n".join(lines)


def _gates_reading_lines(gates_reading: dict[str, Any]) -> list[str]:
    return [
        f"## {gates_reading.get(REVIEWER_DECISION_MATRIX_GATES_READING_HEADING_KEY, GATES_READING_HEADING)}",
        f"- {gates_reading.get(REVIEWER_DECISION_MATRIX_RELEASE_GATE_KEY, '')}",
        f"- {gates_reading.get(REVIEWER_DECISION_MATRIX_PROMOTION_GATE_KEY, '')}",
        "",
        *[
            f"- {note}"
            for note in gates_reading.get(
                REVIEWER_DECISION_MATRIX_GATES_READING_DISCLAIMER_KEY,
                (),
            )
        ],
    ]


def _decision_gate(labels: list[str], *, allow_warning: bool) -> str:
    if any(label == FAIL for label in labels):
        return FAIL
    if any(label == WARN for label in labels):
        return WARN if allow_warning else FAIL
    return PASS
