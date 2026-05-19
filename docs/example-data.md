# Example Data

`examples/data/sample_tqqq_qld_like.csv` is a small deterministic OHLC dataset for exercising loaders, indicators, strategies, backtests, and reports with QQQ/TQQQ/QLD-like inputs.

The data is synthetic sample data. It is not historical market data, it does not represent actual QQQ, TQQQ, or QLD prices, and it should not be used to infer future performance. The leveraged series are intentionally simple research fixtures, not precise models of fund mechanics, fees, tracking error, borrowing costs, rebalancing effects, or market impact.

Static fixture provenance lives next to the CSV at `examples/data/sample_tqqq_qld_like.csv.provenance.json`. Generated reports, JSON files, and manifests include that metadata when this sample is used, so reviewers can see that the bundled rows are synthetic/static and not live-downloaded market data.

## Schema

The file uses one row per symbol per trading date:

- `symbol`: Synthetic instrument label. Current values are `QQQ_LIKE`, `TQQQ_LIKE`, and `QLD_LIKE`.
- `date`: ISO-8601 trading date.
- `open`, `high`, `low`, `close`: Daily OHLC prices.

The extra `symbol` column lets tests and examples split the file into separate series. The existing `load_ohlc_csv` helper can still validate the OHLC columns because it only requires `date`, `open`, `high`, `low`, and `close`.

Use this file for reproducible examples only. Replace it with licensed historical data before making any market claim or research conclusion.
