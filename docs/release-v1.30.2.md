# v1.30.2 Release Notes

Market Signal Lab v1.30.2 adds a small public maturity increment for reviewers reading the assumption ledger summary.

## Start Here

- [Reviewer FAQ](reviewer-faq.md) - concise answers for tradability and first verification questions.
- [Assumption Ledger Summary Guide](assumption-ledger-summary.md) - cold-review workflow for the generated summary.
- [Assumption Ledger Summary Markdown](../reports/assumption-ledger-summary.md) - compact static handoff for assumptions, boundaries, evidence paths, and non-claims.
- [Assumption Ledger Summary JSON](../reports/assumption-ledger-summary.json) - structured version of the same public-safe summary.

## Changed

- Added reviewer-facing FAQ language clarifying that the backtest is not made tradable by the assumption ledger summary.
- Named the first reviewer verification step: confirm static-only, no-live-data, no-broker/account, no-order, no-position-sizing, no-forecast, no-recommendation, and no-advice boundaries before reading metrics.
- Refreshed release links and version metadata for `1.30.2`.

## Boundaries

The assumption ledger summary, FAQ, and checked-in backtest artifacts are static research-review surfaces only. They do not provide live data, broker/account access, order routing, position sizing, forecasts, recommendations, trading signals, suitability review, or investment advice.
