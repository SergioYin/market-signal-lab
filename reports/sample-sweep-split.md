# Moving Average Sweep Report

> Research-only: this sweep is a historical parameter screen, not investment advice, not a recommendation, and not evidence of future performance.

## Validation split

- Research metadata only; this split is not trading guidance.
- Train: 2024-01-02 to 2024-01-05 (4 rows).
- Test: 2024-01-08 to 2024-01-11 (4 rows).

## Data Provenance

- Research-only fixture metadata; not live data, not investment advice, and not a prediction.
- **Dataset label**: sample_tqqq_qld_like
- **Data kind**: synthetic_static_fixture
- **Source**: Hand-authored deterministic OHLC sample bundled with Market Signal Lab for offline examples and tests.
- **Created date**: 2026-05-18
- **As-of date**: 2026-05-18
- **Metadata path**: examples/data/sample_tqqq_qld_like.csv.provenance.json
- **Limitations**: Synthetic rows are not broker, exchange, fund-provider, vendor, or live-feed data.; Placeholder symbols QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE are example-shaped labels, not real instrument histories.; Leveraged ETF-like rows do not model fund mechanics, fees, tracking differences, financing costs, taxes, liquidity, or market impact.; Use only for deterministic research artifact checks; do not use for advice, recommendations, predictions, or market claims.

> Train/test columns are a comparison aid for historical research only; a large train/test gap can prompt review for possible parameter overfitting and is not trading guidance.
> The robustness_flag label compares historical train/test ranks and return gaps inside this sample only. 'not_flagged' only means the deterministic review thresholds were not crossed; it is not a prediction, a stability claim, or a recommendation to buy, sell, or hold.

| rank | short_window | long_window | total_return | train_rank | test_rank | rank_delta | train_total_return | test_total_return | train_test_return_gap | robustness_flag | annualized_return | max_drawdown | volatility | sharpe_like | win_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 1.51% | 1 | 3 | 2 | 1.80% | -1.64% | 3.44% | fragile | 71.46% | -1.74% | 17.09% | 3.2432 | 28.57% |
| 2 | 1 | 3 | -1.76% | 2 | 2 | 0 | 0.00% | -1.64% | 1.64% | not_flagged | -47.19% | -1.76% | 12.09% | -5.2143 | 14.29% |
| 3 | 1 | 2 | -3.02% | 3 | 1 | -2 | -1.29% | -0.59% | -0.70% | fragile | -66.86% | -3.02% | 12.86% | -8.5009 | 14.29% |
