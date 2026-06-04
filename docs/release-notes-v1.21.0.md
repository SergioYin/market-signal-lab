# v1.21.0 Release Notes

Market Signal Lab v1.21.0 adds a static reviewer evidence bundle for cold reviewers who want one compact handoff tying together the first-screen gallery, thesis-ledger acceptance route, methodology risks, and public-safe research boundaries.

## Added

- `--reviewer-evidence-bundle`, a deterministic CLI flag that writes `reports/reviewer-evidence-bundle.md` and `reports/reviewer-evidence-bundle.json` by default.
- `market_signal_lab.reviewer_bundle`, a stdlib-only payload and Markdown renderer with inspection steps, verification commands, and explicit no-live-data/no-broker/no-order/no-recommendation boundary flags.
- Checked-in reviewer evidence bundle artifacts under `reports/` for static demo review.
- README, docs index, root landing, and selfcheck/test coverage for the reviewer bundle route.

## Boundaries

This increment is static research packaging only. It does not add live data, broker/account/order workflows, position sizing, forecasts, recommendations, or investment advice. QLD_LIKE and TQQQ_LIKE examples remain historical sample diagnostics and include daily-reset leveraged ETF risk language: path dependency, volatility drag, extreme drawdowns, and no guarantee of future returns.
