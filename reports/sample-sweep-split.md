# Moving Average Sweep Report

> Research-only: this sweep is a historical parameter screen, not investment advice, not a recommendation, and not evidence of future performance.

## Validation split

- Research metadata only; this split is not a trading recommendation.
- Train: 2024-01-02 to 2024-01-05 (4 rows).
- Test: 2024-01-08 to 2024-01-11 (4 rows).

> Train/test columns are a comparison aid for historical research only; a large train/test gap can prompt review for possible parameter overfitting and is not a trading recommendation.
> The robustness_flag label compares historical train/test ranks and return gaps inside this sample only. 'not_flagged' only means the deterministic review thresholds were not crossed; it is not a prediction, a stability claim, or a recommendation to buy, sell, or hold.

| rank | short_window | long_window | total_return | train_rank | test_rank | rank_delta | train_total_return | test_total_return | train_test_return_gap | robustness_flag | annualized_return | max_drawdown | volatility | sharpe_like | win_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 1.51% | 1 | 3 | 2 | 1.80% | -1.64% | 3.44% | fragile | 71.46% | -1.74% | 17.09% | 3.2432 | 28.57% |
| 2 | 1 | 3 | -1.76% | 2 | 2 | 0 | 0.00% | -1.64% | 1.64% | not_flagged | -47.19% | -1.76% | 12.09% | -5.2143 | 14.29% |
| 3 | 1 | 2 | -3.02% | 3 | 1 | -2 | -1.29% | -0.59% | -0.70% | fragile | -66.86% | -3.02% | 12.86% | -8.5009 | 14.29% |
