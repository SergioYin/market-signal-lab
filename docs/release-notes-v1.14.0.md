# v1.14.0 Release Notes

Market Signal Lab v1.14.0 adds a static CLI methodology-audit template for reviewers without expanding the project into live data, broker, advice, recommendation, forecast, account, order, or execution workflows.

## Added

- `market-signal-lab --methodology-audit-template`, which prints a Markdown reviewer template based on `docs/methodology-audit.md`.
- Optional compact JSON output for the same static template via `--json-output PATH`.
- Selfcheck-generated `reports/methodology-audit-template.md` and `reports/methodology-audit-template.json` artifacts.

## Changed

- Updates package and CLI version metadata to `1.14.0`.
- Registers the v1.14.0 release checklist and release notes in the public documentation surfaces and selfcheck link sources.

## Boundaries

The methodology audit template is static reviewer scaffolding only. It does not read CSV data, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, certify strategy quality, validate investment suitability, or provide investment advice.
