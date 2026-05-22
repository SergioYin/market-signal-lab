# Market Signal Lab

Market Signal Lab is a public, research-only sandbox for reproducible trading-signal experiments. Its main value is the artifact trail: one local CSV can produce Markdown, JSON, HTML, and manifest outputs that a reviewer can inspect, rerun, diff, or publish as a static demo without connecting to brokers or live market data.

The v1.1 exposure/trade review increment adds historical model-exposure metadata to single backtest Markdown and JSON artifacts, including periods in market/cash, average exposure, exposure changes, modeled entries/exits, and modeled fee drag. These fields are review metadata only, not advice, trading guidance, or a list of trades to place. For beginners, exposure changes, modeled entries, and modeled exits are historical model states, not executed trades or instructions.

The v1.3 promotion increment makes the cold-user first screen explicit: start with the static gallery at `reports/index.html`, then use the static demo manifest at `docs/static-gallery-manifest.md` to confirm that the checked-in demo uses local relative links, no JavaScript, and no external assets.

The v1.2 fee sensitivity increment adds a research-only single-backtest comparison artifact under `reports/fee-sensitivity.md` and `reports/fee-sensitivity.json`. It reruns the bundled sample CSV with several `fee_bps` assumptions for the existing 20/50 moving-average settings and reports historical total return, buy-and-hold comparison, max drawdown, modeled exposure changes, modeled entries/exits, average exposure, and fee drag.

The v1.0.0 readiness increment adds checked static fixture provenance for the bundled sample CSV, so generated sample reports, JSON payloads, and manifests label the data as synthetic, static, and research-only without performing live downloads.

The v0.9.0 demo increment adds a beginner-readable split-sweep walkthrough and checked-in sample gallery, so a new reader can review the output shape before installing anything:

- [Artifact Gallery](docs/artifact-gallery.md) - what each checked-in report, sweep, JSON file, HTML page, and manifest is for.
- [Static Sample Gallery](reports/index.html) - browser-openable guide to the generated sample artifacts.
- [Static Demo Manifest](docs/static-gallery-manifest.md) - Pages-safe link and asset contract for the checked-in gallery.
- [Fee Sensitivity Comparison](reports/fee-sensitivity.md) - research-only fee assumption comparison for the bundled single backtest.
- [Split Sweep Walkthrough](docs/split-sweep-walkthrough.md) - how to read train/test ranks, return gaps, and `robustness_flag` labels as review diagnostics only.

This is not a trading bot, signal service, forecast engine, or recommendation system.

Worth saving if you want a compact reference for how to package research outputs with visible assumptions, static artifacts, and no execution surface.

## First inspection path

Before installing anything, open [`reports/index.html`](reports/index.html) from the checkout. That static gallery is the first screen for cold review: it links to the checked-in sample reports, JSON payloads, manifests, and caveat docs using local relative paths only. Use [`docs/static-gallery-manifest.md`](docs/static-gallery-manifest.md) to verify the gallery contract and artifact inventory.

## What you get in 60 seconds

From the repository root, install the CLI and use the bundled sample CSV to create the main research artifacts:

```bash
python -m pip install -e .
```

Normal report:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --fee-bps 10.0 \
  --output reports/sample-report.md
```

Sweep report:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --sweep \
  --short-windows 10,20 \
  --long-windows 50,100 \
  --fee-bps 10.0 \
  --top-n 3 \
  --output reports/sample-sweep.md
```

Sweep report with train/test comparison diagnostics:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --sweep \
  --short-windows 1,2 \
  --long-windows 2,3 \
  --fee-bps 10.0 \
  --split-ratio 0.5 \
  --top-n 3 \
  --output reports/sample-sweep-split.md
```

The same split-sweep workflow can be run from the bundled JSON config:

```bash
market-signal-lab --config examples/configs/split-sweep.json
```

CLI flags override config values when explicitly supplied:

```bash
market-signal-lab --config examples/configs/split-sweep.json \
  --top-n 1 \
  --output reports/my-split-sweep.md
```

When a sweep uses `--split-ratio` or `--split-cutoff`, the Markdown and HTML
tables include `train_rank`, `test_rank`, `rank_delta`, `train_total_return`,
`test_total_return`, `train_test_return_gap`, and `robustness_flag` columns for
train/test comparison. JSON `ranked_results` rows keep the returns under
`train_metrics.total_return` and `test_metrics.total_return`, and keep
`train_rank`, `test_rank`, `rank_delta`, `train_test_return_gap`, and
`robustness_flag` under the `robustness` object. These fields are research
diagnostics for checking how historical rankings and return gaps differ across
two partitions. They are not predictions, forecasts, recommendations, stability
claims, or evidence of future performance.

For beginners, read `robustness_flag` as a review label only. `fragile` means
the row crossed the project's deterministic rank-movement, return-gap, or
train-positive/test-nonpositive review rules inside the supplied sample.
`not_flagged` only means those review rules were not crossed; it does not mean
the setting is safe, robust in future data, or suitable for trading.

JSON export:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --json-output reports/sample-report.json
```

Fee sensitivity artifact:

```bash
python scripts/fee_sensitivity.py
```

This script reads the bundled sample CSV and writes
`reports/fee-sensitivity.md` plus `reports/fee-sensitivity.json`. It is a
research-only comparison of several `fee_bps` values for the existing 20/50
moving-average single-backtest settings. In the bundled eight-row sample, the
model has no exposure changes, so changing `fee_bps` does not change the
reported return; the artifact states that caveat directly.

Single backtest reports include `buy_and_hold_total_return` and
`strategy_minus_buy_and_hold_return` metrics. These compare the strategy result
with a simple same-period buy-and-hold baseline over the supplied CSV. They are
historical research diagnostics only, not advice to buy, hold, sell, or follow
the strategy.

Manifest:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --output reports/sample-report.md \
  --json-output reports/sample-report.json \
  --manifest-output reports/sample-manifest.md
```

## Not a trading bot

Market Signal Lab is for research and learning. It does not connect to brokers, place trades, or tell you what to buy or sell. Treat every result as a historical experiment, not a live trading instruction.

Leveraged ETF examples such as TQQQ/QLD need extra caution, especially for beginners. Many of these products reset exposure every day, so a multi-day result depends on the order of daily moves and cannot be estimated by simply multiplying the underlying index's start-to-end return. Leverage can magnify losses quickly, and choppy markets can erode longer-period returns even when the underlying index ends near flat. The bundled leveraged ETF-like sample data is synthetic and simplified; it is useful for checking artifact shape, not for estimating real fund behavior. It is not a full model of real fund fees, tracking differences, financing costs, taxes, liquidity, or market impact.

## Purpose

- Provide a small, explainable workflow for signal research and backtesting.
- Keep experiments deterministic and scriptable so results can be reproduced.
- Make assumptions explicit through generated experiment reports.
- Compare strategy results with a simple buy-and-hold baseline for context.

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

Print the installed CLI version:

```bash
market-signal-lab --version
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

The selfcheck compiles Python files, runs tests, validates local documentation
links, checks static fixture provenance metadata, and regenerates checked-in
sample artifacts.

## Scope boundaries

This project intentionally stays narrow:

- It is research-only and does **not** include broker/exchange integrations.
- It runs historical backtests only; it is not a forecasting engine.
- It currently uses a single strategy family: moving-average crossover signals.
- It is built around CSV-based OHLC input and does not fetch market data automatically.
- Performance metrics are educational and diagnostic, not investment advice.
- Buy-and-hold benchmark metrics are historical diagnostics, not recommendations.
- Fee sensitivity artifacts compare historical model assumptions only; they do not estimate real execution costs.
- Exposure/trade review fields are historical model metadata, not advice or trade instructions.
- Train/test sweep rankings and robustness flags are research diagnostics, not predictions or stability claims.
- Outputs are reproducible artifacts for analysis, not execution signals for live systems.

## Roadmap

Planned improvements (not guaranteed):

- More strategy templates beyond moving-average crossover.
- Expanded risk and slippage modeling controls.
- More reusable JSON config examples for repeatable experiments.
- Better report visuals and summary exports.
- Cleaner CLI UX for batch runs and symbol sweeps.

## Risk documentation

Before using any findings, read:

- [Documentation Map](docs/index.md)
- [Risk Boundaries](docs/risk-boundaries.md)
- [Metric Guide](docs/metric-guide.md)
- [Split Sweep Walkthrough](docs/split-sweep-walkthrough.md)
- [Example Data and Synthetic Data Caveats](docs/example-data.md)
- [Data Provenance](docs/data-provenance.md)
- [Config Files](docs/config-files.md)
- [Artifact Gallery](docs/artifact-gallery.md)
- [Static Demo Manifest](docs/static-gallery-manifest.md)
- [v1.3.1 Release Notes](docs/release-notes-v1.3.1.md)
- [v1.3.1 Release Checklist](docs/release-v1.3.1.md)
- [v1.3.0 Release Notes](docs/release-notes-v1.3.0.md)
- [v1.3.0 Release Checklist](docs/release-v1.3.0.md)
- [v1.2.1 Release Notes](docs/release-notes-v1.2.1.md)
- [v1.2.1 Release Checklist](docs/release-v1.2.1.md)
- [v1.2.0 Release Notes](docs/release-notes-v1.2.0.md)
- [v1.2.0 Release Checklist](docs/release-v1.2.0.md)
- [v1.1 Release Notes](docs/release-notes-v1.1.0.md)
- [v0.9.0 Release Notes](docs/release-notes-v0.9.0.md)
- [v0.9.0 Release Checklist](docs/release-v0.9.0.md)
- [v0.8.0 Release Notes](docs/release-notes-v0.8.0.md)
- [v0.8.0 Release Checklist](docs/release-v0.8.0.md)
- [v0.7.0 Release Notes](docs/release-notes-v0.7.0.md)
- [v0.7.0 Release Checklist](docs/release-v0.7.0.md)
- [v0.6.0 Release Notes](docs/release-notes-v0.6.0.md)
- [v0.6.0 Release Checklist](docs/release-v0.6.0.md)
- [v0.5.0 Release Notes](docs/release-notes-v0.5.0.md)
- [v0.5.0 Release Checklist](docs/release-v0.5.0.md)
- [v0.4.0 Release Notes](docs/release-notes-v0.4.0.md)
- [v0.4.0 Release Checklist](docs/release-v0.4.0.md)
- [v0.3.0 Release Notes](docs/release-notes-v0.3.0.md)
- [v0.3.0 Release Checklist](docs/release-v0.3.0.md)
