# Methodology Audit Score

Offline methodology-audit scoring summary from reviewer-entered PASS/WARN/FAIL statuses only; not investment advice, not a recommendation, not a forecast, and not a live-data, broker, account, order, or position-sizing workflow.

## Reviewer Metadata

- **Artifact reviewed**: reports/sample-report.md
- **Reviewer**: Example reviewer
- **Review date**: 2026-06-01
- **Source checklist**: `docs/methodology-audit.md`

## Score Summary

- **PASS**: 5
- **WARN**: 1
- **FAIL**: 0
- **Promotion gate suggestion**: promote_with_warnings
- **Reason**: No FAIL statuses, but at least one audit check is marked WARN.

## Audit Checks

| Check | Status | Reviewer notes |
| --- | --- | --- |
| Look-ahead bias | PASS | Historical diagnostics are labeled as supplied-row comparisons. |
| Survivorship bias | PASS | Synthetic fixture and placeholder symbols are visible. |
| Overfitting | WARN | Sweep output is framed as review material, but public copy should avoid implying model selection proof. |
| Fees and slippage | PASS | fee_bps and missing real-world cost caveats are visible. |
| Daily reset leveraged ETF risk | PASS | Leveraged ETF-like examples are described as placeholders. |
| Live trading and advice boundary | PASS | The artifact stays research-only and has no broker or order workflow. |

## Boundary

This scorer only summarizes a local reviewer-filled JSON file. It does not read market data, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, certify strategy quality, or provide investment advice.
