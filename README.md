# Market Signal Lab

Market Signal Lab is a public, research-only reference repo for packaging reproducible market-signal review artifacts. From a bundled static sample CSV, it generates Markdown, JSON, HTML, manifest, scenario-card, and thesis-ledger outputs that a reviewer can inspect, rerun, diff, and publish as a static demo.

Star or reuse it if you want a compact, zero-dependency example of how to ship historical diagnostics with visible assumptions, acceptance checks, structured outputs, and public-safe caveats. It is intentionally not a trading bot, signal service, forecast engine, recommendation system, broker workflow, account workflow, order workflow, position-sizing tool, or source of investment advice.

60-second path:

```bash
git clone https://github.com/SergioYin/market-signal-lab.git
cd market-signal-lab
python -m market_signal_lab.cli --validate-thesis-ledger
```

Then open the static first screen at <https://sergioyin.github.io/market-signal-lab/> or [`reports/index.html`](reports/index.html), and compare the generated acceptance output with the checked-in artifacts.

Proof artifacts:

- [Cross-Asset Thesis Ledger](reports/cross-asset-thesis-ledger.md) - deterministic QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE evidence packet from the bundled sample CSV.
- [Thesis-Ledger Acceptance Summary](reports/cross-asset-thesis-ledger-acceptance.md) - checked-in PASS/WARN/FAIL acceptance artifact for the ledger packet.
- [Static Gallery Manifest](docs/static-gallery-manifest.md) - Pages-safe artifact inventory showing local relative links, no JavaScript, and no external assets.
- [Reviewer Evidence Bundle](reports/reviewer-evidence-bundle.md) - compact cold-review handoff linking gallery, thesis-ledger acceptance, verification commands, and no-advice boundaries.
- [Beginner Backtest Reading Checklist](reports/beginner-prediction-checklist.md) - beginner-readable guardrail for reading historical backtests without treating them as predictions of future returns or advice.

For a compact cold-review handoff, use the [Quick-Tour Preview](docs/quick-tour-preview.md), [Three-Minute Review Route](docs/three-minute-review.md), [Cold User Evidence Card](docs/cold-user-evidence-card.md), [Public Share Summary](docs/public-share-summary.md), [Reviewer FAQ](docs/reviewer-faq.md), [Promotion Checklist](docs/promotion-checklist.md), [Methodology Audit](docs/methodology-audit.md), [Methodology Audit Review File Schema](docs/methodology-audit-review-schema.md), and the [Evidence Card Walkthrough](docs/evidence-card-walkthrough.svg).

The v1.22.0 beginner backtest-reading checklist increment adds a deterministic `--beginner-prediction-checklist` CLI route and checked-in [Beginner Backtest Reading Checklist](reports/beginner-prediction-checklist.md) / [JSON](reports/beginner-prediction-checklist.json) artifacts so beginners can read historical backtest outputs without treating them as predictions of future returns, recommendations, trading instructions, or investment advice. It preserves the no-live-data, no-broker/account/order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries.

The v1.21.0 reviewer evidence-bundle increment adds a deterministic `--reviewer-evidence-bundle` CLI route and checked-in [Reviewer Evidence Bundle](reports/reviewer-evidence-bundle.md) / [JSON](reports/reviewer-evidence-bundle.json) artifacts so cold reviewers can follow the static gallery -> thesis-ledger acceptance -> methodology-risk route with explicit no-live-data, no-broker/account/order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries.

The v1.20.4 quick-tour preview increment adds [Quick-Tour Preview](docs/quick-tour-preview.md) and [Quick-Tour Preview SVG](docs/quick-tour-preview.svg) so cold users can see the static gallery -> evidence card -> acceptance-check route before installing anything. It is documentation/static-demo polish only and preserves the no-live-data, no-broker/account/order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries.

The v1.20.3 reviewer decision-tree increment adds [Reviewer Decision Tree](docs/reviewer-decision-tree.md) so cold users can choose between understanding, reproducibility, methodology-risk, public-sharing, and promotion-readiness checks. It is documentation-only except version metadata and preserves the no-live-data, no-broker/account/order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries.

The v1.20.2 public-share copy increment adds [Public Share Copy](docs/public-share-copy.md) so reviewers and maintainers can describe the project without turning sample outputs into strategy, forecast, signal-service, or recommendation claims. It is documentation-only except version metadata and preserves the no-live-data, no-broker/account/order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries.

The v1.20.1 audit-command guide increment adds [Local Audit Commands](docs/local-audit-commands.md) for reviewers who want a short verification route after reading the three-minute review page. It is documentation-only except version metadata and preserves the no-live-data, no-broker/account/order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries.

The v1.20.0 cold-review route increment adds [Three-Minute Review Route](docs/three-minute-review.md) for reviewers who want to inspect the static demo, methodology caveats, and one reproducible acceptance command before deciding whether to reuse the project pattern. It is documentation-only except version metadata and preserves the no-live-data, no-broker/account/order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries.

The v1.19.0 architecture documentation increment adds [Architecture](docs/architecture.md) and [ADR 0001: Static Research Artifacts](docs/adr/0001-static-research-artifacts.md) for maintainers and public reviewers. It explains the static-first architecture, local CLI artifact pipeline, methodology audit modules, sample reports, test/selfcheck gates, and why live data, brokers, account workflows, orders, position sizing, recommendations, forecasts, and investment advice are intentionally out of scope. It is documentation-only except version metadata.

The v1.18.0 methodology-audit review-template increment adds `--methodology-audit-review-template`, a static JSON skeleton for reviewers to fill before scoring with `--score-methodology-audit`. It writes JSON to `--json-output` when supplied or stdout otherwise, and stays deterministic and stdlib-only with no JavaScript, live data, broker or account workflow, orders, position sizing, recommendations, forecasts, or investment advice.

The v1.17.0 methodology-audit validation increment documents the reviewer-filled JSON shape in [Methodology Audit Review File Schema](docs/methodology-audit-review-schema.md) and makes invalid audit check names/statuses fail with direct CLI errors. It stays deterministic and stdlib-only, with no JavaScript, live data, broker or account workflow, orders, position sizing, recommendations, forecasts, or investment advice.

The v1.16.0 methodology-audit score HTML increment lets `--score-methodology-audit PATH` write a static browser-openable score report via `--html-output PATH`, with local links to matching Markdown and JSON artifacts when those outputs are supplied. The HTML report has no JavaScript, no external assets, no live data, no broker or account workflow, no orders, no position sizing, no recommendations, no forecasts, and no investment advice.

The v1.15.0 methodology-audit scoring increment adds a static `--score-methodology-audit PATH` CLI flag that reads a reviewer-filled JSON file, then prints or writes a Markdown score summary with pass/warn/fail counts and a promotion gate suggestion. Optional compact JSON is available via `--json-output`. It reuses the `docs/methodology-audit.md` checks and does not read CSV market data, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, or provide investment advice.

The v1.14.0 methodology-audit-template increment adds a static `--methodology-audit-template` CLI flag that prints or writes a reviewer Markdown template, with optional compact JSON via `--json-output`. It reuses the `docs/methodology-audit.md` checks and does not read CSV data, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, or provide investment advice.

The v1.13.0 methodology-audit increment adds a static reviewer checklist for common sample-backtest pitfalls: look-ahead bias, survivorship bias, overfitting, fees and slippage, leveraged ETF-like daily reset risk, and no-advice/no-live-trading boundaries. It is documentation only and adds no JavaScript, live-data, broker, account, order, forecast, recommendation, position-sizing, or execution workflow.

The v1.1.0 exposure/trade review increment adds historical model-exposure metadata to single backtest Markdown and JSON artifacts, including periods in market/cash, average exposure, exposure changes, modeled entries/exits, and modeled fee drag. These fields are review metadata only, not advice, trading guidance, or a list of trades to place. For beginners, exposure changes, modeled entries, and modeled exits are historical model states, not executed trades or instructions.

The scenario/risk interpretation section adds a beginner-readable `## Scenario/Risk Interpretation` block to single backtest Markdown/HTML reports and a `scenario_risk_interpretation` object to JSON. It summarizes exposure, max drawdown, modeled fee drag, and same-period buy-and-hold comparison as historical diagnostics only. It is not advice, not a forecast, not trading guidance, and not a broker connection or execution feature.

The v1.6.0 static gallery dashboard increment makes the cold-user first screen explicit: start with the public static demo at <https://sergioyin.github.io/market-signal-lab/> or the checked-in gallery at `reports/index.html`, then use the dashboard cards to jump to the single report, regime comparison, fee sensitivity, split sweep, and manifest artifact paths. Use the static demo manifest at `docs/static-gallery-manifest.md` to confirm that the demo uses local relative links, no JavaScript, and no external assets.

The v1.8.0 scenario-card increment adds a compact, zero-dependency `--scenario-card` CLI flag that reuses the existing single-backtest path and writes Markdown/JSON artifacts at `reports/scenario-card.md` and `reports/scenario-card.json`. The card is designed for thesis-ledger or portfolio-review embedding: assumptions, key metrics, exposure/fee/drawdown diagnostics, non-advice labels, leveraged ETF-like risk language, and a next-review checklist. It does not add broker, live-data, account, order, forecast, position-sizing, or execution workflows.

The v1.9.0 cross-asset thesis-ledger increment adds checked-in `reports/cross-asset-thesis-ledger.md` and `reports/cross-asset-thesis-ledger.json` artifacts generated by selfcheck from the bundled sample CSV. The packet compares QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE with the existing backtest, exposure review, scenario-risk, and scenario-card helpers. It stays offline, zero-dependency, research-only, and does not add advice, forecasts, live data, broker, account, order, or execution workflows.

The v1.10.0 thesis-ledger acceptance increment adds a zero-dependency validator for the existing cross-asset thesis-ledger JSON packet. Use `--validate-thesis-ledger` to validate `reports/cross-asset-thesis-ledger.json` and write Markdown/JSON acceptance artifacts, or pass a local packet path. The validator checks packet shape and research boundaries only; it does not fetch live data, connect to brokers, create orders, size positions, forecast, recommend, or provide advice.

The v1.7.0 pre-trade research packet adds a zero-dependency `--pretrade-packet` CLI flag that reuses the existing single-backtest path and writes Markdown/JSON artifacts at `reports/pretrade-packet.md` and `reports/pretrade-packet.json`. The packet summarizes assumptions, historical diagnostics, a beginner checklist, and explicit non-advice plus leveraged ETF-like risk boundaries. It does not add broker, live-data, account, order, or execution workflows.

The regime-comparison artifact adds a cold-review path for the bundled synthetic bull, choppy, and drawdown-recovery fixtures. Start with `reports/regime-comparison.md`, then open `reports/regime-comparison.json` for the structured rows or `reports/regime-comparison.html` for a browser view. These files compare historical model diagnostics across deterministic synthetic regimes only; they are research-only artifacts, not investment advice, not recommendations, not forecasts, and not a guarantee of future returns.

The v1.2 fee sensitivity increment adds a research-only single-backtest comparison artifact under `reports/fee-sensitivity.md` and `reports/fee-sensitivity.json`. It reruns the bundled sample CSV with several `fee_bps` assumptions for the existing 20/50 moving-average settings and reports historical total return, buy-and-hold comparison, max drawdown, modeled exposure changes, modeled entries/exits, average exposure, and fee drag.

The v1.0.0 readiness increment adds checked static fixture provenance for the bundled sample CSV, so generated sample reports, JSON payloads, and manifests label the data as synthetic, static, and research-only without performing live downloads.

The v0.9.0 demo increment adds a beginner-readable split-sweep walkthrough and checked-in sample gallery, so a new reader can review the output shape before installing anything:

- [Artifact Gallery](docs/artifact-gallery.md) - what each checked-in report, sweep, JSON file, HTML page, and manifest is for.
- [Architecture](docs/architecture.md) - static-first architecture, CLI artifact pipeline, methodology audit modules, sample reports, selfcheck gates, and out-of-scope boundaries.
- [ADR 0001: Static Research Artifacts](docs/adr/0001-static-research-artifacts.md) - maintainer decision record for keeping the project as static research artifacts.
- [Public Share Summary](docs/public-share-summary.md) - compact public-safe summary of target users, the 60-second demo route, and research-only boundaries.
- [Reviewer FAQ](docs/reviewer-faq.md) - concise answers for cold reviewers about bot scope, live data, validation, leveraged ETF-like examples, and first-open artifacts.
- [Promotion Checklist](docs/promotion-checklist.md) - public-safe gates, evidence items, runnable checks, and copy boundaries before sharing or reusing the repo.
- [Methodology Audit](docs/methodology-audit.md) - PASS/WARN/FAIL checklist for common backtest methodology risks and public-safe scope boundaries.
- [Methodology Audit Review File Schema](docs/methodology-audit-review-schema.md) - JSON schema-like reference for reviewer-filled audit files and CLI validation errors.
- [Static Gallery Walkthrough](docs/static-gallery-walkthrough.svg) - visual reading path for the public static gallery and scenario-card artifacts.
- [Static Sample Gallery](reports/index.html) - browser-openable guide to the generated sample artifacts.
- [Static Demo Manifest](docs/static-gallery-manifest.md) - Pages-safe link and asset contract for the checked-in gallery.
- [Single Backtest Report](reports/sample-report.md) - includes `## Scenario/Risk Interpretation` and modeled exposure review sections for the bundled research-only sample.
- [Single Backtest JSON](reports/sample-report.json) - includes `scenario_risk_interpretation` and `exposure_trade_review` objects for the same run.
- [Pre-Trade Research Packet](reports/pretrade-packet.md) - assumptions, historical diagnostics, checklist, and risk boundaries generated from the existing single-backtest path.
- [Beginner Backtest Reading Checklist](reports/beginner-prediction-checklist.md) - static beginner checklist for reading historical backtest artifacts without treating them as predictions of future returns, recommendations, or advice.
- [Scenario Card](reports/scenario-card.md) - compact research-only assumptions, key metrics, diagnostics, risk labels, and artifact-inspection checklist from the existing single-backtest path.
- [Methodology Audit Score HTML](reports/methodology-audit-score.html) - static browser-openable PASS/WARN/FAIL methodology-audit score summary generated from reviewer-entered JSON.
- [Cross-Asset Thesis Ledger](reports/cross-asset-thesis-ledger.md) - deterministic QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE evidence packet generated from the bundled sample CSV by selfcheck.
- [Regime Comparison](reports/regime-comparison.md) - side-by-side research-only comparison of the bundled synthetic bull, choppy, and drawdown-recovery fixtures.
- [Regime Comparison JSON](reports/regime-comparison.json) - structured version of the same synthetic regime comparison.
- [Fee Sensitivity Comparison](reports/fee-sensitivity.md) - research-only fee assumption comparison for the bundled single backtest.
- [Split Sweep Walkthrough](docs/split-sweep-walkthrough.md) - how to read train/test ranks, return gaps, and `robustness_flag` labels as review diagnostics only.

This is not a trading bot, signal service, forecast engine, or recommendation system.

Worth saving if you want a compact reference for how to package research outputs with visible assumptions, static artifacts, and no execution surface.

## First inspection path

Before installing anything, open the public static demo at <https://sergioyin.github.io/market-signal-lab/> or [`reports/index.html`](reports/index.html) from the checkout. That static gallery is the first screen for cold review: open the single backtest report first for the Scenario/Risk Interpretation section, then open the [cold user evidence card](docs/cold-user-evidence-card.md), [public share summary](docs/public-share-summary.md), [reviewer FAQ](docs/reviewer-faq.md), [promotion checklist](docs/promotion-checklist.md), [methodology audit](docs/methodology-audit.md), [methodology audit review schema](docs/methodology-audit-review-schema.md), the [scenario card](reports/scenario-card.md), or the [static gallery walkthrough](docs/static-gallery-walkthrough.svg) for the compact card path, then open the [regime comparison](reports/regime-comparison.md) to see how the synthetic bull, choppy, and drawdown-recovery fixtures differ, then use the manifest and caveat docs to verify the checked-in artifact trail. All linked results are historical research diagnostics only, use synthetic/static sample data, and use local relative paths only. They are not investment advice, recommendations, forecasts, or a guarantee of future returns. Use [`docs/static-gallery-manifest.md`](docs/static-gallery-manifest.md) to verify the gallery contract and artifact inventory.

For maintainer context, read [Architecture](docs/architecture.md) and [ADR 0001: Static Research Artifacts](docs/adr/0001-static-research-artifacts.md) before changing artifact generation or public scope.

The v1.6.0 first-screen dashboard cards show the artifact paths directly: `reports/sample-report.html`, `reports/regime-comparison.html`, `reports/fee-sensitivity.md`, `reports/sample-sweep-split.html`, and `reports/sample-manifest.md`.

The v1.22.0 beginner backtest-reading checklist adds `reports/beginner-prediction-checklist.md` and `reports/beginner-prediction-checklist.json` to that first inspection path. The v1.9.0 cross-asset thesis ledger adds `reports/cross-asset-thesis-ledger.md` and `reports/cross-asset-thesis-ledger.json`. The v1.8.0 scenario card adds `reports/scenario-card.md` and `reports/scenario-card.json`. The v1.7.0 packet card adds `reports/pretrade-packet.md` and `reports/pretrade-packet.json`.

Validate the checked-in thesis-ledger JSON packet and write acceptance artifacts before installing the package:

```bash
python -m market_signal_lab.cli --validate-thesis-ledger
```

Validate a specific local packet while printing Markdown to stdout:

```bash
python -m market_signal_lab.cli --validate-thesis-ledger path/to/cross-asset-thesis-ledger.json \
  --json-output reports/my-ledger-acceptance.json
```

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

Pre-trade research packet:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --fee-bps 10.0 \
  --pretrade-packet \
  --output reports/pretrade-packet.md \
  --json-output reports/pretrade-packet.json
```

This packet is built from the same historical backtest diagnostics as the single
report. It includes assumptions, source metadata, historical metrics, modeled
exposure review, scenario/risk summaries, a beginner checklist, and non-advice
plus leveraged ETF-like risk boundaries.

Scenario card:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --fee-bps 10.0 \
  --scenario-card
```

By default this writes `reports/scenario-card.md` and
`reports/scenario-card.json`. The card is a compact research-only summary of
the same historical single-backtest diagnostics; it is not advice, a forecast,
trading guidance, or an execution workflow.

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

Regime comparison artifact:

```bash
market-signal-lab --regime-comparison
```

This writes `reports/regime-comparison.md`, `reports/regime-comparison.json`,
and `reports/regime-comparison.html` from the bundled synthetic multi-regime
fixture and checked configs. It compares bull, choppy, and drawdown-recovery
placeholder regimes using historical strategy return, buy-and-hold return,
drawdown, exposure, cash-time, exposure-change, and whipsaw diagnostics. The
regime labels are fixture scenarios for review and tests, not market
classifications, not recommendations, not forecasts, and not a guarantee of
future returns.

Single backtest reports include `buy_and_hold_total_return` and
`strategy_minus_buy_and_hold_return` metrics. These compare the strategy result
with a simple same-period buy-and-hold baseline over the supplied CSV. They are
historical research diagnostics only, not advice to buy, hold, sell, or follow
the strategy.

Single backtest Markdown and HTML reports also include
`## Scenario/Risk Interpretation`. The matching JSON export includes
`scenario_risk_interpretation`. This generated section is a plain-language
summary of historical exposure, drawdown, modeled fee drag, and the same-period
buy-and-hold comparison so cold readers can understand the report shape. It does
not recommend an action, predict performance, connect to a broker, or provide a
real-time execution cue.

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
python -m pip install -e ".[test]"
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
- Scenario/risk interpretation fields are historical diagnostics, not advice, forecasts, broker guidance, or real-time execution cues.
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
- [Cold Review Checklist](docs/cold-review-checklist.md)
- [Risk Boundaries](docs/risk-boundaries.md)
- [Scenario/Risk Glossary](docs/scenario-risk-glossary.md)
- [Metric Guide](docs/metric-guide.md)
- [Split Sweep Walkthrough](docs/split-sweep-walkthrough.md)
- [Example Data and Synthetic Data Caveats](docs/example-data.md)
- [Data Provenance](docs/data-provenance.md)
- [Config Files](docs/config-files.md)
- [Artifact Gallery](docs/artifact-gallery.md)
- [Architecture](docs/architecture.md)
- [ADR 0001: Static Research Artifacts](docs/adr/0001-static-research-artifacts.md)
- [Static Gallery Walkthrough](docs/static-gallery-walkthrough.svg)
- [Static Demo Manifest](docs/static-gallery-manifest.md)
- [Methodology Audit](docs/methodology-audit.md)
- [Three-Minute Review Route](docs/three-minute-review.md)
- [Local Audit Commands](docs/local-audit-commands.md)
- [Public Share Copy](docs/public-share-copy.md)
- [Reviewer Decision Tree](docs/reviewer-decision-tree.md)
- [v1.22.0 Release Notes](docs/release-notes-v1.22.0.md)
- [v1.22.0 Release Checklist](docs/release-v1.22.0.md)
- [v1.21.0 Release Notes](docs/release-notes-v1.21.0.md)
- [v1.21.0 Release Checklist](docs/release-v1.21.0.md)
- [v1.20.4 Release Notes](docs/release-notes-v1.20.4.md)
- [v1.20.4 Release Checklist](docs/release-v1.20.4.md)
- [v1.20.3 Release Notes](docs/release-notes-v1.20.3.md)
- [v1.20.3 Release Checklist](docs/release-v1.20.3.md)
- [v1.20.2 Release Notes](docs/release-notes-v1.20.2.md)
- [v1.20.2 Release Checklist](docs/release-v1.20.2.md)
- [v1.20.1 Release Notes](docs/release-notes-v1.20.1.md)
- [v1.20.1 Release Checklist](docs/release-v1.20.1.md)
- [v1.20.0 Release Notes](docs/release-notes-v1.20.0.md)
- [v1.20.0 Release Checklist](docs/release-v1.20.0.md)
- [v1.19.0 Release Notes](docs/release-notes-v1.19.0.md)
- [v1.19.0 Release Checklist](docs/release-v1.19.0.md)
- [v1.18.0 Release Notes](docs/release-notes-v1.18.0.md)
- [v1.18.0 Release Checklist](docs/release-v1.18.0.md)
- [v1.17.0 Release Notes](docs/release-notes-v1.17.0.md)
- [v1.17.0 Release Checklist](docs/release-v1.17.0.md)
- [v1.16.0 Release Notes](docs/release-notes-v1.16.0.md)
- [v1.16.0 Release Checklist](docs/release-v1.16.0.md)
- [v1.15.0 Release Notes](docs/release-notes-v1.15.0.md)
- [v1.15.0 Release Checklist](docs/release-v1.15.0.md)
- [v1.14.0 Release Notes](docs/release-notes-v1.14.0.md)
- [v1.14.0 Release Checklist](docs/release-v1.14.0.md)
- [v1.13.0 Release Notes](docs/release-notes-v1.13.0.md)
- [v1.13.0 Release Checklist](docs/release-v1.13.0.md)
- [v1.12.0 Release Notes](docs/release-notes-v1.12.0.md)
- [v1.12.0 Release Checklist](docs/release-v1.12.0.md)
- [v1.11.0 Release Notes](docs/release-notes-v1.11.0.md)
- [v1.11.0 Release Checklist](docs/release-v1.11.0.md)
- [v1.10.0 Release Notes](docs/release-notes-v1.10.0.md)
- [v1.10.0 Release Checklist](docs/release-v1.10.0.md)
- [v1.9.1 Release Notes](docs/release-notes-v1.9.1.md)
- [v1.9.1 Release Checklist](docs/release-v1.9.1.md)
- [v1.9.0 Release Notes](docs/release-notes-v1.9.0.md)
- [v1.9.0 Release Checklist](docs/release-v1.9.0.md)
- [v1.8.0 Release Notes](docs/release-notes-v1.8.0.md)
- [v1.8.0 Release Checklist](docs/release-v1.8.0.md)
- [v1.7.0 Release Notes](docs/release-notes-v1.7.0.md)
- [v1.7.0 Release Checklist](docs/release-v1.7.0.md)
- [v1.6.0 Release Notes](docs/release-notes-v1.6.0.md)
- [v1.6.0 Release Checklist](docs/release-v1.6.0.md)
- [v1.5.0 Release Notes](docs/release-notes-v1.5.0.md)
- [v1.5.0 Release Checklist](docs/release-v1.5.0.md)
- [v1.4.0 Release Notes](docs/release-notes-v1.4.0.md)
- [v1.4.0 Release Checklist](docs/release-v1.4.0.md)
- [v1.3.5 Release Notes](docs/release-notes-v1.3.5.md)
- [v1.3.5 Release Checklist](docs/release-v1.3.5.md)
- [v1.3.4 Release Notes](docs/release-notes-v1.3.4.md)
- [v1.3.4 Release Checklist](docs/release-v1.3.4.md)
- [v1.3.3 Release Notes](docs/release-notes-v1.3.3.md)
- [v1.3.3 Release Checklist](docs/release-v1.3.3.md)
- [v1.3.2 Release Notes](docs/release-notes-v1.3.2.md)
- [v1.3.2 Release Checklist](docs/release-v1.3.2.md)
- [v1.3.1 Release Notes](docs/release-notes-v1.3.1.md)
- [v1.3.1 Release Checklist](docs/release-v1.3.1.md)
- [v1.3.0 Release Notes](docs/release-notes-v1.3.0.md)
- [v1.3.0 Release Checklist](docs/release-v1.3.0.md)
- [v1.2.1 Release Notes](docs/release-notes-v1.2.1.md)
- [v1.2.1 Release Checklist](docs/release-v1.2.1.md)
- [v1.2.0 Release Notes](docs/release-notes-v1.2.0.md)
- [v1.2.0 Release Checklist](docs/release-v1.2.0.md)
- [v1.1.0 Release Notes](docs/release-notes-v1.1.0.md)
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
