# v1.13.0 Release Notes

Market Signal Lab v1.13.0 packages the methodology-audit docs increment for reviewing checked-in sample backtests without expanding the project into live trading, advice, or execution workflows.

## Added

- `docs/methodology-audit.md`, a static PASS/WARN/FAIL checklist for common sample-backtest methodology risks: look-ahead bias, survivorship bias, overfitting, fees and slippage, leveraged ETF-like daily reset risk, and no-advice/no-live-trading boundaries.

## Changed

- Updates package and CLI version metadata to `1.13.0`.
- Registers the v1.13.0 release checklist and release notes in the public documentation surfaces.
- Registers the methodology audit in the README, documentation map, root landing page, static demo manifest, and selfcheck link sources.
- Updates the static demo manifest release label to `v1.13.0`.

## Boundaries

The methodology audit is static documentation for public review of research artifacts only. It does not fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, certify strategy quality, validate investment suitability, or provide investment advice.
