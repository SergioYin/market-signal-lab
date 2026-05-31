# Methodology Audit Review File Schema

This page documents the JSON shape accepted by:

```bash
python -m market_signal_lab.cli --score-methodology-audit PATH
```

The file is a local reviewer-entered methodology audit review. It is static input for PASS/WARN/FAIL counting only. It does not read CSV market data, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, certify strategy quality, or provide investment advice.

## Root Object

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `audit_type` | string | No | Recommended value: `methodology_audit_review`. |
| `schema_version` | string | No | Recommended value: `1.0`. |
| `artifact_reviewed` | string | No | Local path or short description of the reviewed artifact. |
| `reviewer` | string | No | Reviewer name or identifier. |
| `review_date` | string | No | Suggested format: `YYYY-MM-DD`. |
| `checks` | array | Yes | Must contain exactly the six check objects below, in order. |

Optional metadata fields are copied into the score summary when present. If supplied, `artifact_reviewed`, `reviewer`, and `review_date` must be strings.

## Check Objects

Each item in `checks` must be a JSON object:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `check` | string | Yes | Must match the template check name at that row. |
| `status` | string | Yes | One of `PASS`, `WARN`, or `FAIL`. Lowercase input is accepted and normalized in the score output. |
| `notes` | string | No | Reviewer note. `null` is treated as an empty string. |

The accepted `check` names and order are:

1. `Look-ahead bias`
2. `Survivorship bias`
3. `Overfitting`
4. `Fees and slippage`
5. `Daily reset leveraged ETF risk`
6. `Live trading and advice boundary`

Invalid check names and invalid statuses produce CLI errors that identify the affected row or check. For example, a misspelled second check reports:

```text
error: checks[2].check must be 'Survivorship bias', got 'Survival bias'
```

An invalid status reports the check name and accepted values:

```text
error: Look-ahead bias: invalid status 'MAYBE'; expected one of PASS, WARN, FAIL
```

## Minimal Example

```json
{
  "audit_type": "methodology_audit_review",
  "schema_version": "1.0",
  "artifact_reviewed": "reports/sample-report.md",
  "reviewer": "Example reviewer",
  "review_date": "2026-06-01",
  "checks": [
    {
      "check": "Look-ahead bias",
      "status": "PASS",
      "notes": "Historical diagnostics are labeled as supplied-row comparisons."
    },
    {
      "check": "Survivorship bias",
      "status": "PASS",
      "notes": "Synthetic fixture and placeholder symbols are visible."
    },
    {
      "check": "Overfitting",
      "status": "WARN",
      "notes": "Sweep output remains a review prompt, not model-selection proof."
    },
    {
      "check": "Fees and slippage",
      "status": "PASS",
      "notes": "fee_bps and missing real-world cost caveats are visible."
    },
    {
      "check": "Daily reset leveraged ETF risk",
      "status": "PASS",
      "notes": "Leveraged ETF-like examples are described as placeholders."
    },
    {
      "check": "Live trading and advice boundary",
      "status": "PASS",
      "notes": "The artifact stays research-only and has no broker or order workflow."
    }
  ]
}
```

See [`examples/configs/methodology-audit-review.json`](../examples/configs/methodology-audit-review.json) for the checked-in example review file.

## Score Output

The scorer writes Markdown to stdout or `--output PATH`. With `--json-output PATH`, it writes a compact JSON score summary with:

- `summary_type`: `methodology_audit_score`
- `counts`: lowercase `pass`, `warn`, and `fail` counts
- `promotion_gate_suggestion`: `promote`, `promote_with_warnings`, or `do_not_promote`
- `checks`: normalized check rows with uppercase statuses and string notes
- public-safe boundary flags such as `research_only`, `static_only`, `no_live_data`, `no_broker_or_account`, `no_orders_or_position_sizing`, and `no_recommendations_or_forecasts`

The promotion gate is only a review workflow label. It is not a trading recommendation, performance validation, forecast, or advice.
