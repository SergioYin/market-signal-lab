# Example Data

`examples/data/sample_tqqq_qld_like.csv` is a small deterministic OHLC dataset for exercising loaders, indicators, strategies, backtests, and reports with QQQ/TQQQ/QLD-like inputs.

`examples/data/sample_multi_regime.csv` is a deterministic synthetic OHLC dataset with three placeholder symbols:

- `BULL_REGIME`: upward path for trend-following examples.
- `CHOPPY_REGIME`: alternating path that ends near flat.
- `DRAWDOWN_RECOVERY_REGIME`: decline followed by recovery for drawdown diagnostics.

Each regime is synthetic-only. The close path is constructed to exercise one report behavior, open prices equal the prior close after the first row, and high/low values are generated as padding around open and close. These assumptions are recorded in `examples/data/sample_multi_regime.csv.provenance.json` and carried into generated regime-comparison JSON.

The data is synthetic sample data. It is not historical market data, it does not represent actual QQQ, TQQQ, or QLD prices, and it should not be used to infer future performance. The leveraged series are intentionally simple research fixtures, not precise models of fund mechanics, fees, tracking error, borrowing costs, rebalancing effects, or market impact.

Static fixture provenance lives next to the CSV at `examples/data/sample_tqqq_qld_like.csv.provenance.json`. Generated reports, JSON files, and manifests include that metadata when this sample is used, so reviewers can see that the bundled rows are synthetic/static and not live-downloaded market data.

Multi-regime fixture provenance lives next to the CSV at `examples/data/sample_multi_regime.csv.provenance.json`. It includes the same research-only fixture fields plus deterministic regime metadata. The regime labels are testing scenarios only, not market classifications, predictions, broker guidance, live-trading signals, or recommendations.

## Schema

The file uses one row per symbol per trading date:

- `symbol`: Synthetic instrument label. Current values include `QQQ_LIKE`, `TQQQ_LIKE`, `QLD_LIKE`, `BULL_REGIME`, `CHOPPY_REGIME`, and `DRAWDOWN_RECOVERY_REGIME`.
- `date`: ISO-8601 trading date.
- `open`, `high`, `low`, `close`: Daily OHLC prices.

The extra `symbol` column lets tests and examples split the file into separate series. The existing `load_ohlc_csv` helper can still validate the OHLC columns because it only requires `date`, `open`, `high`, `low`, and `close`.

Use this file for reproducible examples only. Replace it with licensed historical data before making any market claim or research conclusion.

Example multi-regime configs live in `examples/configs/multi-regime-bull-report.json`, `examples/configs/multi-regime-choppy-report.json`, and `examples/configs/multi-regime-drawdown-recovery-report.json`.
