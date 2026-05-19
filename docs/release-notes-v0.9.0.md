# v0.9.0 Release Notes

v0.9.0 adds a public-demo walkthrough for beginners reading split-sweep robustness reports. The release focuses on safer public presentation of existing artifacts and does not add forecasting, live data, broker execution, or trading recommendations.

## What Changed

- Added [Split Sweep Walkthrough](split-sweep-walkthrough.md), a static GitHub Pages-friendly guide that links to the checked-in split-sweep Markdown, HTML, and JSON sample artifacts.
- Expanded documentation navigation so new readers can find the walkthrough from the README, documentation map, and artifact gallery.
- Added selfcheck coverage for the new walkthrough and v0.9.0 release docs.
- Version metadata now reports `market-signal-lab 0.9.0`.

## How To Verify

From the repository root, run `python -m market_signal_lab.cli --version` and confirm it prints `market-signal-lab 0.9.0`. Then run `pytest` and `python scripts/selfcheck.py`. Review the public demo paths `docs/split-sweep-walkthrough.md`, `reports/index.html`, `reports/sample-sweep-split.html`, `reports/sample-sweep-split.md`, and `reports/sample-sweep-split.json`.

To regenerate only the split-sweep demo artifacts, run:

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

## Research-Only Boundary

The walkthrough explains how to read historical train/test rank, return-gap, and `robustness_flag` fields as review aids. It does not turn any split-sweep result into investment advice, trading recommendations, forecasts, stability claims, or instructions to buy, sell, or hold.
