# Market Signal Lab

Market Signal Lab is a public sandbox for transparent trading-signal research. It helps users run reproducible moving-average crossover backtests on OHLC data, inspect risk metrics, and generate Markdown reports for review.

## Purpose

- Provide a small, explainable workflow for signal research and backtesting.
- Keep experiments deterministic and scriptable so results can be reproduced.
- Make assumptions explicit through generated experiment reports.

## Target users

- Students and analysts exploring systematic trading ideas.
- Product, research, and quant teams evaluating baseline signal behavior.
- Engineers building learning projects around market-data pipelines.
- Anyone comparing strategy settings against historical price data.

## Quickstart

Requirements:

- Python 3.10+

Install from source:

```bash
python -m pip install -e .
```

Run help:

```bash
market-signal-lab --help
```

Offline sample command (uses the repository's bundled sample CSV):

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --fee-bps 10.0
```

This command prints a full Markdown report to the terminal. To save it to a file:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --fee-bps 10.0 \
  --output reports/qqq_like_report.md
```

If you prefer not to install, run directly:

```bash
python -m market_signal_lab.cli examples/data/sample_tqqq_qld_like.csv --symbol QQQ_LIKE
```

Run the project selfcheck:

```bash
python scripts/selfcheck.py
```

## Scope boundaries

This project intentionally stays narrow:

- It is research-only and does **not** include broker/exchange integrations.
- It runs historical backtests only; it is not a forecasting engine.
- It currently uses a single strategy family: moving-average crossover signals.
- It is built around CSV-based OHLC input and does not fetch market data automatically.
- Performance metrics are educational and diagnostic, not investment advice.
- Outputs are reproducible artifacts for analysis, not execution signals for live systems.

## Roadmap

Planned improvements (not guaranteed):

- More strategy templates beyond moving-average crossover.
- Expanded risk and slippage modeling controls.
- Config-first and JSON/YAML experiment definitions.
- Better report visuals and summary exports.
- Cleaner CLI UX for batch runs and symbol sweeps.

## Risk documentation

Before using any findings, read:

- [Risk Boundaries](docs/risk-boundaries.md)
- [Example Data and Synthetic Data Caveats](docs/example-data.md)
