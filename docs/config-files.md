# Config Files

Market Signal Lab accepts an optional JSON config file for repeatable local
experiments:

```bash
market-signal-lab --config examples/configs/split-sweep.json
```

Config files must be plain JSON objects with known option names. YAML and TOML
are intentionally not supported, and the CLI does not add broker, execution,
forecast, or advice behavior.

Supported keys:

- `csv_path`
- `symbol`
- `short_window`
- `long_window`
- `fee_bps`
- `sweep`
- `short_windows`
- `long_windows`
- `split_ratio`
- `split_cutoff`
- `top_n`
- `output`
- `json_output`
- `html_output`
- `manifest_output`

CLI flags override config values when explicitly supplied. For example, this
uses the sample config but writes only the top sweep result to a different
Markdown file:

```bash
market-signal-lab --config examples/configs/split-sweep.json \
  --top-n 1 \
  --output reports/my-split-sweep.md
```

When `--config` is omitted, existing CLI defaults and positional-argument
behavior are unchanged. A run still needs a CSV path, either as the positional
CLI argument or as `csv_path` in the JSON config.

Unknown keys are rejected so misspelled options fail fast. A `null` value is
treated the same as omitting that key, allowing the CLI default or explicit flag
to take effect.

The bundled `examples/configs/split-sweep.json` uses synthetic sample data and
train/test diagnostics. Those outputs are research artifacts only: they are not
broker instructions, trading recommendations, forecasts, or evidence of future
performance.
