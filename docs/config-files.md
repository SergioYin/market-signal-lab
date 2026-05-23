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
train/test rank and `robustness_flag` label diagnostics. In JSON outputs,
`train_rank`, `test_rank`, `rank_delta`, `train_test_return_gap`, and
`robustness_flag` appear under each row's `robustness` object; train and test
returns appear as `train_metrics.total_return` and `test_metrics.total_return`.
Those outputs are research artifacts only: they are not broker instructions,
trading recommendations, forecasts, or evidence of future performance.

To regenerate the checked-in single-backtest report and its structured
scenario/risk interpretation fields without any live market fetches, use the
bundled synthetic fixture config:

```bash
market-signal-lab --config examples/configs/single-backtest-report.json
```

That config reads only `examples/data/sample_tqqq_qld_like.csv`, filters the
synthetic `QQQ_LIKE` rows, and writes the Markdown, JSON, HTML, and manifest
artifacts under `reports/`. The Markdown/HTML outputs include
`## Scenario/Risk Interpretation`; the JSON output includes
`scenario_risk_interpretation` with `exposure`, `drawdown`, `fee_drag`, and
`buy_and_hold_comparison` sections. These fields are historical diagnostics for
reviewing report shape only, not advice, forecasts, live signals, or broker
instructions.
