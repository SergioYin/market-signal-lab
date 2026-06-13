# Reviewer Decision Matrix (Public Guide)

The Reviewer Decision Matrix is a **public, deterministic review artifact** for the static sample packet. It helps a reviewer decide whether a static backtest package is ready to proceed between two gates:

- **Release Gate**: evidence is sufficient for public review release, with `WARN` allowed only when follow-up items remain visible.
- **Promotion Gate**: evidence is strong enough for broader public references, documentation, and demo quality.

## PASS / WARN / FAIL interpretation

The artifact uses three outcomes for each check:

- **PASS**: required evidence is present and internally consistent.
- **WARN**: evidence is present but incomplete, unclear, or missing optional context; safe for review, not yet promotion-ready.
- **FAIL**: required checks are missing or inconsistent, so the packet should not be promoted until fixed.

Use these outcomes this way:

- If **Release Gate** is `FAIL`, do not release for public review.
- If **Release Gate** is `WARN`, release only as a review artifact with visible follow-up items; do not promote it.
- If **Promotion Gate** is `WARN` or `FAIL`, keep promotion on hold for follow-up edits.
- Only promote publicly when both gates are `PASS`.

## No-advice and static-data boundaries

This matrix is a review aid only. It does not provide recommendations, forecasts, or trading signals.
All labels and examples are derived from checked-in sample artifacts and synthetic/static data.
No local file path or section in this guide is meant as live-market access, broker workflow, order routing, account inspection, position sizing, or investment advice.

## Deterministic JSON Contract (Review Metadata Only)

The generated JSON payload is deterministic and contains only review metadata about static artifacts.

```json
{
  "artifact_type": "reviewer_decision_matrix",
  "schema_version": "1.0",
  "research_only": true,
  "static_only": true,
  "historical_diagnostics_only": true,
  "no_live_data": true,
  "no_broker_or_account": true,
  "no_orders_or_position_sizing": true,
  "no_recommendations_or_forecasts": true,
  "not_investment_advice": true,
  "source_artifact": "reports/sample-report.json",
  "purpose": "Help cold reviewers decide whether a static artifact is safe for release.",
  "default_outputs": {
    "markdown": "reports/reviewer-decision-matrix.md",
    "json": "reports/reviewer-decision-matrix.json"
  },
  "gates_reading": {
    "heading": "How to Read the Gates",
    "release_gate": "PASS|WARN|FAIL",
    "promotion_gate": "PASS|WARN|FAIL",
    "disclaimer": ["string", "string"]
  },
  "summary": {
    "release_gate": "PASS|WARN|FAIL",
    "promotion_gate": "PASS|WARN|FAIL",
    "pass_count": 0,
    "warn_count": 0,
    "fail_count": 0
  },
  "decision_categories": [
    {
      "criterion": "data_provenance",
      "label": "PASS|WARN|FAIL",
      "evidence": "string",
      "review_note": "string"
    }
  ],
  "public_boundaries": ["string", ...],
  "verification_commands": ["string", ...]
}
```

Top-level JSON keys (fixed contract order):
`artifact_type`, `schema_version`, `research_only`, `static_only`, `historical_diagnostics_only`, `no_live_data`, `no_broker_or_account`, `no_orders_or_position_sizing`, `no_recommendations_or_forecasts`, `not_investment_advice`, `source_artifact`, `purpose`, `default_outputs`, `gates_reading`, `summary`, `decision_categories`, `public_boundaries`, `verification_commands`.

`decision_categories` entries always include:
`criterion`, `label`, `evidence`, `review_note`.

The matrix artifact is generated with the usual selfcheck workflow and documented in:

- [Reviewer Decision Matrix artifact](../reports/reviewer-decision-matrix.md)
- [Reviewer Decision Matrix JSON](../reports/reviewer-decision-matrix.json)
