# Data Provenance

The bundled CSV at `examples/data/sample_tqqq_qld_like.csv` is synthetic sample data. It was hand-authored for deterministic tests and examples, so every run can produce the same artifacts.

The rows do not come from a broker, exchange, data vendor, fund provider, or live market feed. They are not historical prices, they do not model real fund mechanics, and they should not be used to make claims about actual market behavior.

The symbols are placeholders:

- `QQQ_LIKE`
- `QLD_LIKE`
- `TQQQ_LIKE`

The `_LIKE` names mean "example-shaped input," not real QQQ, QLD, or TQQQ data.

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
