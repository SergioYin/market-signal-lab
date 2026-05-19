# v0.8.0 Release Notes

v0.8.0 adds split-sweep rank/gap diagnostics so a reader can compare how parameter sets ranked in the training window versus the test window. The release does not add forecasting, live data, broker execution, or trading recommendations.

## What Changed

- Split sweeps run with `--split-ratio` or `--split-cutoff` now report `train_rank`, `test_rank`, `rank_delta`, `train_total_return`, `test_total_return`, `train_test_return_gap`, and `robustness_flag` in Markdown and HTML output.
- Train/test ranks are computed across the full parameter grid before any `--top-n` display limit is applied, so displayed rows can still show movement against hidden rows.
- JSON split-sweep `ranked_results` rows now include a `robustness` object with `train_rank`, `test_rank`, `rank_delta`, `train_test_return_gap`, and `robustness_flag`; train and test returns remain in `train_metrics.total_return` and `test_metrics.total_return`.
- The checked-in split-sweep sample artifacts were regenerated to show the new fields.
- Version metadata now reports `market-signal-lab 0.8.0`.

## How To Verify

Run `pytest`, then run `python scripts/selfcheck.py`, then confirm `python -m market_signal_lab.cli --version` prints `market-signal-lab 0.8.0` from the source tree. Review the regenerated split-sweep artifacts in `reports/sample-sweep-split.md`, `reports/sample-sweep-split.json`, and `reports/sample-sweep-split.html`.

## Research-Only Boundary

The split consistency fields are historical/sample backtest review aids only. `robustness_flag` identifies deterministic train/test rank or return-gap conditions inside the supplied data; `not_flagged` only means those review thresholds were not crossed in that sample. These labels are not predictions, stability claims, investment advice, trading recommendations, or signals to buy, sell, or hold.
