# v1.10.0 Release Notes

Market Signal Lab v1.10.0 adds a focused, zero-dependency acceptance validator for the existing cross-asset thesis-ledger JSON packet.

## Added

- Public `validate_cross_asset_thesis_ledger_packet` and `render_thesis_ledger_acceptance_summary` helpers in `market_signal_lab.thesis_ledger`.
- `market-signal-lab --validate-thesis-ledger [PATH]` for validating a local ledger JSON file, defaulting to `reports/cross-asset-thesis-ledger.json`.
- Default Markdown/JSON acceptance artifacts at `reports/cross-asset-thesis-ledger-acceptance.md` and `reports/cross-asset-thesis-ledger-acceptance.json` when no output paths are supplied.

## Boundaries

The validator checks JSON packet shape and public research boundaries only. It does not fetch live data, connect to brokers, inspect accounts, create orders, size positions, forecast, recommend, or provide investment advice.

