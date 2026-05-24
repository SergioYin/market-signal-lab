# Data Provenance

The bundled CSVs at `examples/data/sample_tqqq_qld_like.csv` and `examples/data/sample_multi_regime.csv` are synthetic sample data. They are deterministic fixtures for tests and examples, so every run can produce the same artifacts.

The adjacent metadata files `examples/data/sample_tqqq_qld_like.csv.provenance.json` and `examples/data/sample_multi_regime.csv.provenance.json` label the CSVs as `synthetic_static_fixture` data. The CLI reads this file when present and includes the metadata in generated Markdown reports, JSON payloads, and experiment manifests. This is static provenance only; Market Signal Lab does not download, refresh, or validate live market data.

| Field | Sample value | Meaning |
| --- | --- | --- |
| `dataset_label` | `sample_tqqq_qld_like` | Stable fixture label for reports and manifests. |
| `data_kind` | `synthetic_static_fixture` | Explicitly marks the data as bundled synthetic fixture data. |
| `source` | Hand-authored deterministic OHLC sample | Human-readable source statement for the fixture. |
| `created_date` | `2026-05-18` | Date assigned to the static fixture metadata. |
| `as_of_date` | `2026-05-18` | Static metadata date, not a market-data freshness claim. |
| `limitations` | Synthetic/static caveats | Research-only limits that travel with generated artifacts. |

`sample_multi_regime.csv.provenance.json` also records a `regimes` list with placeholder symbol, regime name, description, generation assumptions, row count, and explicit `synthetic_only`, `not_predictive`, and `not_live_trading` flags for each deterministic synthetic scenario. These labels exist to make tests and examples easier to inspect; they are not data-quality certifications, forecasts, market classifications, broker guidance, live-trading signals, or recommendations.

The rows do not come from a broker, exchange, data vendor, fund provider, or live market feed. They are not historical prices, they do not model real fund mechanics, and they should not be used to make claims about actual market behavior. For beginners, read every bundled backtest as a software-output example: it can show whether the command and reports work, but it cannot show whether a strategy will work with real money.

The symbols are placeholders:

- `QQQ_LIKE`
- `QLD_LIKE`
- `TQQQ_LIKE`
- `BULL_REGIME`
- `CHOPPY_REGIME`
- `DRAWDOWN_RECOVERY_REGIME`

The `_LIKE` names mean "example-shaped input," not real QQQ, QLD, or TQQQ data. The `_REGIME` names mean synthetic scenario paths for reproducible tests only.

## Bring Your Own CSV

You can use your own CSV without connecting any broker account. Export or prepare a local file with these columns:

- `date`
- `open`
- `high`
- `low`
- `close`

Then pass the file path to the CLI:

```bash
market-signal-lab path/to/your-data.csv --symbol YOUR_SYMBOL
```

If your file includes multiple symbols, keep a `symbol` column and choose the label you want with `--symbol`. Market Signal Lab reads local CSV files only; it does not fetch market data, place trades, or provide investment advice.

For your own CSVs, absence of an adjacent `.provenance.json` file simply means the generated artifacts omit fixture provenance. It does not imply that the data is live, licensed, complete, suitable for market claims, or appropriate for trading decisions.
