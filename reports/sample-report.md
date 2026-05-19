# Market Signal Experiment Report

## Strategy Config

- **short_window**: 20
- **long_window**: 50
- **symbol**: QQQ_LIKE
- **fee_bps**: 10.0000

## Backtest Summary

- **Start date**: 2024-01-02
- **End date**: 2024-01-11
- **Starting equity**: 1.0000
- **Ending equity**: 1.0000
- **Backtest total return**: 0.00%
- **Exposure changes**: 0

## Metrics

- **Strategy total return**: 0.00%
- **Buy-and-hold total return**: 1.69%
- **Strategy minus buy-and-hold return**: -1.69%
- **Annualized return**: 0.00%
- **Max drawdown**: 0.00%
- **Volatility**: 0.00%
- **Sharpe-like score**: 0.0000
- **Win rate**: 0.00%

## Data Provenance

- Research-only fixture metadata; not live data, not investment advice, and not a prediction.
- **Dataset label**: sample_tqqq_qld_like
- **Data kind**: synthetic_static_fixture
- **Source**: Hand-authored deterministic OHLC sample bundled with Market Signal Lab for offline examples and tests.
- **Created date**: 2026-05-18
- **As-of date**: 2026-05-18
- **Metadata path**: examples/data/sample_tqqq_qld_like.csv.provenance.json
- **Limitations**: Synthetic rows are not broker, exchange, fund-provider, vendor, or live-feed data.; Placeholder symbols QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE are example-shaped labels, not real instrument histories.; Leveraged ETF-like rows do not model fund mechanics, fees, tracking differences, financing costs, taxes, liquidity, or market impact.; Use only for deterministic research artifact checks; do not use for advice, recommendations, predictions, or market claims.

## Risk Notes

- Model exposure states use close-price moving averages only.
- Filtered to symbol: QQQ_LIKE.

## Backtest Caveats

- Backtest results are hypothetical and do not guarantee future performance.
- Model exposure states are calculated from historical data only. They can be affected by data quality, survivorship bias, and parameter overfitting, and they are not trading instructions.
- Reported returns are model outputs before taxes, market impact, and any costs not explicitly included in the backtest.
