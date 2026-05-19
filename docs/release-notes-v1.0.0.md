# v1.0.0 Release Notes

v1.0.0 adds static fixture provenance to the bundled sample data path. The release keeps the runtime dependency-free and does not add live downloads, forecasting, broker execution, investment advice, or trading recommendations.

## What Changed

- Added `examples/data/sample_tqqq_qld_like.csv.provenance.json` to label the bundled CSV as a synthetic static fixture with source, dates, limitations, and research-only status.
- Added a stdlib-only provenance loader that reads adjacent fixture metadata when present and leaves ordinary CSV inputs unchanged when metadata is absent.
- Included fixture provenance in generated Markdown reports, JSON reports, sweep reports, and experiment manifests where applicable.
- Added tests and selfcheck coverage for fixture metadata shape, generated artifact fields, documentation links, and public no-advice claim boundaries.
- Version metadata now reports `market-signal-lab 1.0.0`.

## How To Verify

From the repository root, run `python -m market_signal_lab.cli --version` and confirm it prints `market-signal-lab 1.0.0`. Then run `pytest` and `python scripts/selfcheck.py`.

Review these provenance surfaces after sample artifact regeneration:

- `examples/data/sample_tqqq_qld_like.csv.provenance.json`
- `reports/sample-report.md`
- `reports/sample-report.json`
- `reports/sample-manifest.md`
- `reports/sample-sweep.md`
- `reports/sample-sweep.json`
- `reports/sample-sweep-split.md`
- `reports/sample-sweep-split.json`

## Research-Only Boundary

The provenance metadata says what the bundled fixture is and what it is not. It is synthetic/static sample data for reproducible artifact checks. It is not historical market data, not live data, not investment advice, not a recommendation, not a forecast, and not evidence of future performance.
