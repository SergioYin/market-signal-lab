# Pre-Trade Research Packet

- Research-only packet built from historical sample/backtest data; not investment advice, not trading guidance, not a recommendation, not a prediction, and not a broker connection or execution feature.
- Built from the existing single-backtest path.

## Source

- **Input path**: examples/data/sample_tqqq_qld_like.csv
- **Date range**: 2024-01-02 to 2024-01-11
- **Rows reviewed**: 8

## Assumptions

- Uses the existing single-backtest moving-average workflow.
- Uses only the supplied local CSV path and optional symbol filter.
- Uses historical close-to-close sample rows; no live data is requested.
- Uses configured fee_bps as a simplified historical cost assumption.
- Does not connect to brokers, create orders, or provide execution steps.
- Adjacent static fixture provenance is included when available.

## Historical Diagnostics

- **Strategy total return**: 0.00%
- **Buy-and-hold total return**: 1.69%
- **Strategy minus buy-and-hold return**: -1.69%
- **Max drawdown**: 0.00%
- **Average exposure**: 0.00%
- **Periods in market**: 0.00%
- **Exposure changes**: 0
- **Modeled entries**: 0
- **Modeled exits**: 0
- **Modeled fee drag**: 0.00%

## Scenario/Risk Interpretation

- Historical diagnostics only; this scenario/risk interpretation is not investment advice, trading guidance, a prediction, or a broker connection or execution feature.
- **Exposure**: The model was exposed to the market for 0.00% of reviewed periods. Higher exposure means the historical result depended more on market moves; lower exposure means more periods were modeled as cash.
- **Drawdown**: The worst modeled peak-to-trough decline was 0.00%. Larger negative drawdowns mean the historical equity curve had larger interim losses.
- **Fee drag**: Modeled fee drag summed to 0.00% across reviewed periods. This is a simplified historical cost assumption, not a complete estimate of taxes, spreads, market impact, or broker execution.
- **Buy-and-hold comparison**: Strategy minus buy-and-hold was -1.69% over the same period. A positive gap means the model finished above buy-and-hold in this historical sample; a negative gap means it finished below it.

## Beginner Checklist

- [ ] Confirm the CSV path, symbol filter, row count, and date range match the review.
- [ ] Read static fixture provenance before interpreting any metric.
- [ ] Compare strategy return with same-period buy-and-hold return.
- [ ] Review exposure, cash time, exposure changes, and modeled fee drag.
- [ ] Check max drawdown as an interim-loss diagnostic, not a forecast.
- [ ] Treat all modeled states as historical diagnostics, not instructions.
- [ ] For leveraged ETF-like labels, read the daily-reset and path-dependency boundary.

## Risk Boundaries

- **Non-advice boundary**: Research-only packet built from historical sample/backtest data; not investment advice, not trading guidance, not a recommendation, not a prediction, and not a broker connection or execution feature.
- **Sample/backtest limits**: Backtest and sample results are limited to the supplied historical rows and simplified assumptions. They are examples for review only, not evidence of future returns.
- **Leveraged ETF-like boundary**: Leveraged ETF-like examples require extra caution. Daily reset mechanics make multi-day outcomes path-dependent; losses can grow quickly; and real fund results can differ because of expenses, financing costs, tracking differences, taxes, liquidity, spreads, and market impact that this packet does not model.
- **Scope limits**: Local artifact only. No broker workflow, live-data workflow, private account fields, order routing, position sizing instruction, or recommendation engine.
