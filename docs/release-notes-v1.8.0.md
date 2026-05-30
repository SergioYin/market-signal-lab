# v1.8.0 Release Notes

Market Signal Lab v1.8.0 adds compact scenario-card artifacts for research review and thesis-ledger / portfolio-review embedding while keeping the project offline, deterministic, and zero-dependency.

## Added

- Adds `--scenario-card` for the existing single-backtest path.
- Writes compact Markdown and JSON artifacts at `reports/scenario-card.md` and `reports/scenario-card.json` by default.
- Includes source range, assumptions, key metrics, exposure/fee/drawdown diagnostics, scenario/risk interpretation, public risk labels, and a next-review checklist.
- Adds sparse-payload renderer tests so missing optional fields render as `n/a` / public-safe defaults instead of leaking Python `None` values.

## Updated

- Refreshes README, documentation map, artifact gallery, static gallery manifest, and checked-in static gallery links.
- Extends selfcheck coverage so the scenario-card artifacts are part of the public demo contract.
- Updates package and CLI version metadata to `1.8.0`.

## Boundary

Scenario cards are historical research diagnostics only. They are not investment advice, trading recommendations, forecasts, position-sizing instructions, broker integrations, live-data workflows, alerts, or execution features. Leveraged ETF-like examples remain path-dependent and can experience volatility decay and large drawdowns.
