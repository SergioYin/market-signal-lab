# Split Sweep Walkthrough

This beginner walkthrough explains how to read the checked-in split-sweep robustness report without treating it as advice. It is a static GitHub Pages-friendly page: all links are relative, and no JavaScript, remote data, broker connection, or live market feed is required.

Use it with the sample artifacts:

- [HTML split sweep](../reports/sample-sweep-split.html)
- [Markdown split sweep](../reports/sample-sweep-split.md)
- [JSON split sweep](../reports/sample-sweep-split.json)

The sample uses synthetic data and placeholder symbols. The output is a historical research artifact only. It is not investment advice, a recommendation, a forecast, a stability claim, or an instruction to buy, sell, hold, or trade anything. A row in the table is never a "do this" message.

## What The Report Is

A split sweep tries several moving-average parameter pairs on one historical dataset. The data is divided into two parts:

- Train: the earlier rows used for the first ranking.
- Test: the later rows used for a second ranking.

The report then compares how each parameter pair looked in the train partition versus the test partition. This can help a reviewer ask better questions about possible overfitting or sample sensitivity. It does not tell the reviewer which setting will work in the future.

## Read This First

Before looking at the ranked rows, check the warning text at the top of the report and the `Validation split` section. In the checked-in sample, the report says the train range covers `2024-01-02` to `2024-01-05`, and the test range covers `2024-01-08` to `2024-01-11`.

Those dates matter because every number in the table is limited to those rows. A row that looks good in this tiny sample may fail in other dates, other symbols, other costs, or live markets.

## Leveraged ETF-Like Sample Limits

The bundled file name refers to TQQQ/QLD-like sample data, but the rows are synthetic placeholders. They are useful for checking report shape, not for estimating how real leveraged ETFs will behave.

Leveraged ETFs can be hard for beginners because many reset their exposure every day. That means a multi-day result depends on the order of daily gains and losses, not just the first and last price. A simple example: up 10% and then down 10% does not get you back to even, and leverage can make that gap larger.

Choppy markets can also reduce longer-period returns even when the underlying index ends near flat. Losses can happen faster than in broad unleveraged funds. These reports also do not model many real-world details, including fund expenses, financing costs, tracking differences, taxes, liquidity, or market impact.

## Column Reading Order

For a first pass, read the columns in this order:

1. `short_window` and `long_window`: the moving-average settings being tested.
2. `total_return`: the modeled result across the full supplied sample.
3. `train_rank` and `test_rank`: where the same setting ranked in each partition.
4. `rank_delta`: `test_rank` minus `train_rank`. Positive means the setting ranked worse in the test partition; negative means it ranked better.
5. `train_total_return` and `test_total_return`: the modeled return in each partition.
6. `train_test_return_gap`: `train_total_return` minus `test_total_return`.
7. `robustness_flag`: a deterministic review label, not an advice label.

The remaining metrics, such as `annualized_return`, `max_drawdown`, `volatility`, `sharpe_like`, and `win_rate`, are historical diagnostics. See the [Metric Guide](metric-guide.md) for definitions and caveats.

## How To Read `robustness_flag`

`fragile` means the row crossed this project's deterministic review rules for train/test rank movement, return gap, or train-positive/test-nonpositive behavior inside the supplied sample.

`not_flagged` only means those review rules were not crossed in this sample. It does not mean the setting is safe, robust in future data, suitable for trading, or better than another setting.

Treat both labels as prompts for review:

- If a row is `fragile`, ask why train and test behavior differed.
- If a row is `not_flagged`, still ask whether the sample is too short, too synthetic, too clean, or too narrow.
- If any row has a high return, remember that the report is still a historical experiment, not a recommendation.

## Example Walkthrough

In the checked-in sample report, the first displayed row uses `short_window` 2 and `long_window` 3. It has train rank 1 and test rank 3, so `rank_delta` is 2. That means it ranked lower in the later test partition than it did in the earlier train partition.

The same row has a positive train return and a negative test return. Its `robustness_flag` is `fragile`, which tells a reviewer that the sample crossed the project's review rules. It does not prove the setting is bad, and it does not recommend any action. It only says this row deserves skepticism inside this historical sample.

Another row may show `not_flagged`. That label should be read narrowly: the configured rules did not flag it here. It is not a green light, a safety label, or a suggestion to trade.

## Beginner Checklist

Use this checklist before sharing or interpreting a split-sweep report:

1. Confirm the report uses the intended local CSV and symbol.
2. Check the train and test date ranges.
3. Look for very short samples, synthetic data, placeholder symbols, or leveraged ETF-like examples.
4. Compare train and test ranks rather than focusing only on full-sample `total_return`.
5. Treat `fragile` and `not_flagged` as review labels only.
6. Read the [Risk Boundaries](risk-boundaries.md) before making any conclusion.

## Recreate The Sample

From the repository root:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
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

You can also run the full project selfcheck:

```bash
python scripts/selfcheck.py
```
