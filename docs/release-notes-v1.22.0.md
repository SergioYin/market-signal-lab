# v1.22.0 Release Notes

Market Signal Lab v1.22.0 adds a static beginner backtest-reading checklist for reading historical backtest artifacts without treating them as predictions of future returns, recommendations, or advice.

## Added

- New zero-dependency `--beginner-prediction-checklist` CLI route.
- `market_signal_lab.beginner_prediction_checklist`, a stdlib-only payload and Markdown renderer with reading steps, verification commands, and explicit no-live-data/no-broker/no-order/no-recommendation boundary flags.
- Checked-in Markdown and JSON artifacts under `reports/beginner-prediction-checklist.*`.
- Beginner-readable historical-backtest reading steps, static source links, boundary flags, and leveraged ETF daily-reset/path-dependency risk language.
- Public reviewer star/reuse rationale that frames the checklist as a deterministic static review template, not a prediction, recommendation, trading instruction, or investment advice.
- README, docs map, static gallery, root landing, and selfcheck/test coverage for the new artifacts.
- Package metadata and CLI version output identify this release as `1.22.0`.

## Scope

This release adds no live data, broker or account workflow, orders, order routing, position sizing, recommendations, forecasts, or investment advice. The new artifacts are deterministic static research guardrails only.
