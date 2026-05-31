# v1.15.0 Release Notes

Market Signal Lab v1.15.0 adds a focused offline methodology-audit scoring utility for reviewer-filled JSON files. It summarizes static PASS/WARN/FAIL audit statuses into Markdown and optional compact JSON without expanding the project into live data, broker, advice, recommendation, forecast, account, order, or execution workflows.

## Added

- `market-signal-lab --score-methodology-audit PATH`, which reads a local reviewer-filled methodology audit JSON file and prints a Markdown score summary.
- Optional compact JSON scoring output via `--json-output PATH`.
- Deterministic pass/warn/fail counts and a promotion gate suggestion: `promote`, `promote_with_warnings`, or `do_not_promote`.
- Example reviewer input at `examples/configs/methodology-audit-review.json`.

## Changed

- Updates package and CLI version metadata to `1.15.0`.
- Registers the v1.15.0 release checklist and release notes in the public documentation surfaces and selfcheck link sources.

## Boundaries

The scorer only summarizes reviewer-entered statuses from a local JSON file. It does not read CSV market data, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, certify strategy quality, validate investment suitability, or provide investment advice.
