# Methodology Audit

This checklist helps a cold reviewer assess whether a sample backtest is presented as a bounded research artifact rather than a trading system. It is meant for static review of checked-in Markdown, JSON, HTML, manifest, and documentation files. It is not investment advice, a recommendation, a forecast, a validation of future performance, or a live-trading workflow.

Use it alongside the [Methodology Audit Review File Schema](methodology-audit-review-schema.md), [Artifact Gallery](artifact-gallery.md), [Static Demo Manifest](static-gallery-manifest.md), [Data Provenance](data-provenance.md), [Metric Guide](metric-guide.md), and [Risk Boundaries](risk-boundaries.md).

## Fast Pass

Open the sample report, JSON, manifest, and gallery before running code:

1. [Single backtest report](../reports/sample-report.md)
2. [Single backtest JSON](../reports/sample-report.json)
3. [Sample manifest](../reports/sample-manifest.md)
4. [Static sample gallery](../reports/index.html)
5. [Static demo manifest](static-gallery-manifest.md)

For each item below, record `PASS`, `WARN`, or `FAIL`. A `PASS` means the artifact gives enough information for review. It does not mean the strategy is reliable, suitable for trading, or likely to work in future data.

For an offline scoring summary, fill a local JSON file using the same checks as the table below, then run:

```bash
python -m market_signal_lab.cli --score-methodology-audit examples/configs/methodology-audit-review.json \
  --json-output reports/methodology-audit-score.json \
  --html-output reports/methodology-audit-score.html
```

The scorer only counts reviewer-entered `PASS`, `WARN`, and `FAIL` statuses and suggests `promote`, `promote_with_warnings`, or `do_not_promote`. Optional HTML output is a static rendering with local artifact links. It does not read CSV market data, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, certify strategy quality, or provide investment advice.

For the accepted reviewer JSON shape, check order, status values, and validation errors, see the [Methodology Audit Review File Schema](methodology-audit-review-schema.md).

## Audit Checks

| Check | PASS evidence | WARN or FAIL evidence |
| --- | --- | --- |
| Look-ahead bias | Indicators, ranks, and exposure states are described as historical diagnostics over the supplied rows; same-period buy-and-hold comparisons are labeled as comparisons, not predictions. | The report implies future prices, future ranks, or full-sample outcomes were available when historical decisions were modeled. |
| Survivorship bias | Input files, placeholder symbols, synthetic/static fixture labels, and provenance are visible. The artifact does not claim a live or complete market universe. | The artifact treats a small sample or surviving symbols as proof of broad market performance. |
| Overfitting | Sweep rankings and train/test diagnostics are framed as review prompts. `robustness_flag` labels are not described as proof of stability. | The artifact treats the top sweep row as the best future setting or hides how many parameters were tried. |
| Fees and slippage | `fee_bps`, modeled fee drag, and cost caveats are visible. Missing slippage, taxes, financing, liquidity, and market-impact modeling are named as limitations. | Costs are absent, or results are presented as deployable without explicit cost assumptions and omissions. |
| Daily reset leveraged ETF risk | Leveraged ETF-like labels are described as placeholders or simplified fixtures. Daily reset, path dependency, magnified losses, and unmodeled real fund costs are visible. | Multi-day leveraged returns are treated like a simple multiple of index return, or real fund behavior is implied from the fixture. |
| Live trading and advice boundary | The artifact says it is research-only and does not add broker, live-data, account, order, position-sizing, recommendation, forecast, or advice workflows. | The artifact contains instructions to trade, claims live signals, or implies suitability for an account. |

## Review Notes

- Prefer reproducibility evidence over performance claims: input path, row count, date range, parameters, manifest, and JSON fields matter more than a high return value.
- Treat short synthetic samples as format and workflow fixtures only.
- Treat sweep and split-sweep outputs as questions to investigate, not model-selection proof.
- Treat leveraged ETF-like examples as risk-boundary examples, not product simulations.
- If a report lacks enough information to evaluate any row in the table, mark that row `WARN` or `FAIL` and ask for the missing artifact rather than inferring it.

## Out Of Scope

This audit does not certify a strategy, approve a model, validate live performance, estimate tax impact, model real fund operations, evaluate order execution, or determine account suitability for buying, selling, holding, trading, or sizing a position.
