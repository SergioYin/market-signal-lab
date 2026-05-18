# v0.3.0 Release Checklist

This checklist covers the public release readiness items for the v0.3.0 train/test sweep release.

See [v0.3.0 Release Notes](release-notes-v0.3.0.md) for the concise public summary.

## Feature Summary

- Parameter sweeps can include train/test comparison diagnostics with `--split-ratio` or `--split-cutoff`.
- Sweep Markdown, JSON, and HTML outputs can show `train_total_return` and `test_total_return` fields when the requested partitions can be evaluated.
- Sample split-sweep artifacts are checked in so reviewers can inspect the expected output shape without running new experiments.
- Documentation clarifies that sweep rankings and train/test comparisons are historical research diagnostics only.

## Commands To Verify

Run the test suite:

```bash
pytest
```

Run the project selfcheck, which also regenerates sample artifacts:

```bash
python scripts/selfcheck.py
```

Regenerate the split-sweep sample directly:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --sweep \
  --short-windows 1,2 \
  --long-windows 2,3 \
  --split-ratio 0.5 \
  --top-n 3 \
  --output reports/sample-sweep-split.md
```

## Generated Artifacts

Expected public sample artifacts for this release:

- `reports/sample-sweep-split.md`
- `reports/sample-sweep-split.json`
- `reports/sample-sweep-split.html`
- Existing report, sweep, and manifest samples under `reports/`

Review generated diffs before publishing to confirm that artifact changes are intentional and reproducible.

## No-Advice And Data-Provenance Boundaries

- Market Signal Lab remains research-only software. It does not provide investment advice, trading recommendations, forecasts, or live execution signals.
- Train/test sweep comparisons are historical diagnostics over the supplied CSV, not predictions of future returns.
- The bundled sample CSV is synthetic example data, not broker, exchange, vendor, fund-provider, or live market data.
- Placeholder symbols such as `QQQ_LIKE`, `QLD_LIKE`, and `TQQQ_LIKE` describe example-shaped inputs only.
- The project reads local CSV files and does not fetch market data automatically.

## Future Work

- More strategy templates beyond moving-average crossovers.
- Expanded transaction cost, slippage, and risk modeling controls.
- Config-first experiment definitions for repeatable sweep runs.
- Cleaner batch-run ergonomics for multiple symbols and parameter sets.
- Better report visualizations and summary exports.
