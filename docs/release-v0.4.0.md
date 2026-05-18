# v0.4.0 Release Checklist

This checklist covers the public release readiness items for the v0.4.0 JSON config workflow release.

See [v0.4.0 Release Notes](release-notes-v0.4.0.md) for the concise public summary.

## Feature Summary

- JSON config files can define repeatable backtest or sweep runs.
- Explicit CLI flags override config values when supplied.
- The bundled split-sweep config provides a reproducible example command for the existing synthetic sample data.
- Config documentation records the supported JSON shape, precedence rules, and option boundaries.

## Commands To Verify

Run the test suite:

```bash
pytest
```

Run the project selfcheck, which also regenerates sample artifacts:

```bash
python scripts/selfcheck.py
```

Run the bundled JSON config sample:

```bash
market-signal-lab --config examples/configs/split-sweep.json
```

Confirm CLI flags override config values:

```bash
market-signal-lab --config examples/configs/split-sweep.json \
  --top-n 1 \
  --output reports/my-split-sweep.md
```

## Config Files

Expected public config files for this release:

- `docs/config-files.md`
- `examples/configs/split-sweep.json`

Review generated diffs before publishing to confirm that artifact changes are intentional and reproducible.

## No-Advice And Data-Provenance Boundaries

- Market Signal Lab remains research-only software. It does not provide investment advice, trading recommendations, forecasts, or live execution signals.
- Config files define local research runs only; they do not connect to brokers, exchanges, vendors, fund providers, or live market data.
- The bundled sample CSV is synthetic example data with placeholder `_LIKE` symbols.
- Train/test sweep comparisons remain historical diagnostics over the supplied CSV, not predictions of future returns.

## Future Work

- More reusable JSON config examples for repeatable experiments.
- Cleaner batch-run ergonomics for multiple symbols and parameter sets.
- Expanded transaction cost, slippage, and risk modeling controls.
