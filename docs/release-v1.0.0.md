# v1.0.0 Release Checklist

This checklist covers the v1.0.0 readiness increment for static fixture provenance. It is intended for a reviewer who needs to confirm that bundled sample data is labeled clearly without adding live downloads or runtime dependencies.

See [v1.0.0 Release Notes](release-notes-v1.0.0.md) for the concise public summary.

## Feature Summary

- `examples/data/sample_tqqq_qld_like.csv.provenance.json` labels the bundled CSV as a synthetic static fixture.
- The provenance metadata records source, created date, as-of date, limitations, and `research_only: true`.
- The CLI includes provenance in Markdown reports, JSON outputs, sweep reports, and experiment manifests when adjacent metadata exists.
- Inputs without adjacent provenance metadata keep the previous local CSV behavior.
- Package metadata and CLI version output identify this release as v1.0.0.

## Verification Commands

Run every command from the repository root.

Confirm the source-tree version:

```bash
python -m market_signal_lab.cli --version
```

Expected output:

```text
market-signal-lab 1.0.0
```

Run the test suite:

```bash
pytest
```

Run the project selfcheck, which validates documentation links, public wording boundaries, static fixture provenance, and regenerated sample artifacts:

```bash
python scripts/selfcheck.py
```

Expected selfcheck pass labels:

```text
PASS: compileall
PASS: pytest
PASS: sample artifact generation
PASS: documentation/gallery link check
PASS: v0.9.0 static demo acceptance check
PASS: public claim boundary check
PASS: static fixture provenance check
Selfcheck completed.
```

Review the resulting workspace diff before publishing:

```bash
git status --short
git diff -- market_signal_lab/data.py market_signal_lab/report.py market_signal_lab/sweep.py market_signal_lab/manifest.py market_signal_lab/cli.py examples/data/sample_tqqq_qld_like.csv.provenance.json docs/data-provenance.md docs/example-data.md docs/release-notes-v1.0.0.md docs/release-v1.0.0.md reports/sample-report.md reports/sample-report.json reports/sample-manifest.md
```

## Provenance Artifact Paths

Review the source fixture metadata:

- `examples/data/sample_tqqq_qld_like.csv.provenance.json`

Review generated sample surfaces that should include `data_provenance` or a `Data Provenance` section:

- `reports/sample-report.md`
- `reports/sample-report.json`
- `reports/sample-report.html`
- `reports/sample-manifest.md`
- `reports/sample-sweep.md`
- `reports/sample-sweep.json`
- `reports/sample-sweep.html`
- `reports/sample-sweep-split.md`
- `reports/sample-sweep-split.json`
- `reports/sample-sweep-split.html`

## Release Engineer Notes

- Run `python -m market_signal_lab.cli --version` before publishing and confirm `market-signal-lab 1.0.0`.
- Run `pytest` before publishing.
- Run `python scripts/selfcheck.py` before publishing.
- Confirm package metadata in `pyproject.toml` and `market_signal_lab/__init__.py` both say `1.0.0`.
- Confirm the runtime dependency list remains empty.

## No-Advice And Data-Provenance Boundaries

- Market Signal Lab remains research-only software. It does not provide investment advice, trading recommendations, forecasts, or live execution signals.
- Static fixture provenance is not a data-quality certification, freshness claim, prediction, or recommendation.
- The bundled sample CSV remains synthetic example data with placeholder `_LIKE` symbols.
- The CLI still reads local files only; it does not fetch market data, refresh fixtures, connect to brokers, or place trades.
