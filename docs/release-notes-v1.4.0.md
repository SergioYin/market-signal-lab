# v1.4.0 Release Notes

Market Signal Lab v1.4.0 is a scenario/risk interpretation increment for single backtest artifacts.

## Changed

- Adds a beginner-readable `## Scenario/Risk Interpretation` section to single backtest Markdown and HTML reports.
- Adds a matching `scenario_risk_interpretation` object to single backtest JSON output with exposure, drawdown, fee-drag, and buy-and-hold comparison summaries.
- Adds glossary and documentation links for interpreting exposure, modeled entries/exits, fee drag, drawdown, and buy-and-hold gap diagnostics.
- Keeps checked sample artifacts aligned with the new interpretation fields and research-only wording.
- Updates package and CLI version metadata to `1.4.0`.

## Boundaries

- No broker connection, live market data, forecasts, or buy/sell recommendations.
- Scenario/risk interpretation fields are historical diagnostics only.
- Modeled entries, exits, fee drag, drawdown, and buy-and-hold comparison fields are not advice, trade instructions, or evidence of future performance.
