# v1.7.0 Release Notes

Market Signal Lab v1.7.0 adds a pre-trade research packet MVP while keeping the project offline, deterministic, and zero-dependency.

## Changes

- Adds `market-signal-lab --pretrade-packet` for generating `reports/pretrade-packet.md` and `reports/pretrade-packet.json` from the existing single-backtest path.
- Adds packet sections for assumptions, historical diagnostics, scenario/risk summaries, a beginner checklist, and explicit non-advice, sample/backtest limitation, and leveraged ETF-like risk boundaries.
- Updates selfcheck so the checked sample packet is regenerated with the rest of the static artifact set.
- Updates the static gallery, artifact docs, README, and documentation map to include the packet artifacts.
- Updates package and CLI version metadata to `1.7.0`.

## Scope Boundaries

This release does not add broker connectivity, live data, account workflows, order workflows, private fields, external dependencies, recommendation features, or any promise of future returns from the sample/backtest outputs.
