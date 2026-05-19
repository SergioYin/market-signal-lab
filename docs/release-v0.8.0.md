# v0.8.0 Release Checklist

This checklist covers the public release readiness items for the v0.8.0 split-sweep rank/gap diagnostics release. It is intended for a reviewer who needs to understand what changed, how to verify it, and why the output remains research-only.

See [v0.8.0 Release Notes](release-notes-v0.8.0.md) for the concise public summary.

## Feature Summary

- Split sweep reports compare full-grid train/test rankings before applying `--top-n`, so displayed rows can show rank movement between the two historical partitions.
- Markdown and HTML split sweep tables include `train_rank`, `test_rank`, `rank_delta`, `train_total_return`, `test_total_return`, `train_test_return_gap`, and `robustness_flag`.
- JSON split sweep rows include a `robustness` object with `train_rank`, `test_rank`, `rank_delta`, `train_test_return_gap`, and `robustness_flag`; train and test returns remain in `train_metrics.total_return` and `test_metrics.total_return`.
- Checked-in split sweep sample artifacts were regenerated to show the new fields.
- Package metadata and CLI version output identify this release as v0.8.0.

## Commands To Verify

Run the test suite:

```bash
pytest
```

Run the project selfcheck, which validates documentation links and regenerates sample artifacts:

```bash
python scripts/selfcheck.py
```

Confirm the source-tree CLI version output:

```bash
python -m market_signal_lab.cli --version
```

Expected output:

```text
market-signal-lab 0.8.0
```

Regenerate the split-sweep sample directly:

```bash
python -m market_signal_lab.cli examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --sweep \
  --short-windows 1,2 \
  --long-windows 2,3 \
  --fee-bps 10.0 \
  --top-n 3 \
  --split-ratio 0.5 \
  --output reports/sample-sweep-split.md \
  --json-output reports/sample-sweep-split.json \
  --html-output reports/sample-sweep-split.html
```

## Public Artifacts

Review regenerated diffs for the split-sweep sample artifacts:

- `reports/sample-sweep-split.md`
- `reports/sample-sweep-split.json`
- `reports/sample-sweep-split.html`

## Release Engineer Notes

- Verified `pytest`: 113 tests passed.
- Verified `python scripts/selfcheck.py`: compileall, pytest, documentation link check, and sample artifact generation passed.
- Verified `python -m market_signal_lab.cli --version`: printed `market-signal-lab 0.8.0`.
- Packaging smoke tests should be run before publishing with the release environment's standard build tooling.

## No-Advice And Data-Provenance Boundaries

- Market Signal Lab remains research-only software. It does not provide investment advice, trading recommendations, forecasts, or live execution signals.
- `robustness_flag` labels compare historical train/test ranks and return gaps inside the supplied sample. They are review aids for within-sample train/test consistency, not predictions, stability claims, or recommendations to buy, sell, or hold.
- `not_flagged` means only that deterministic review thresholds were not crossed in that sample; it is not a safety, suitability, or future-performance label.
- The bundled sample CSV remains synthetic example data with placeholder `_LIKE` symbols.
