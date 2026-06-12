# Market Signal Lab

Market Signal Lab packages bundled static backtest samples as reproducible, research-only artifacts: Markdown reports, JSON, browser-openable HTML, manifests, checklists, and PASS/WARN/FAIL validation outputs.

Use it to inspect how a historical backtest artifact explains its data, assumptions, metrics, caveats, and reproducibility while keeping the output limited to review evidence.

## Who it is for

- Beginners learning how to read backtest outputs without treating them as predictions.
- Product, research, and engineering teams evaluating a static artifact pattern for historical diagnostics.
- Maintainers who need deterministic Markdown, JSON, HTML, manifest, scenario-card, checklist, and thesis-ledger outputs from local sample data.

## What it is not

This is a research-only static backtest artifact sandbox. It has no live data, recommendations, forecasts, broker connection, account workflow, order workflow, position sizing, or investment-advice surface.

Every output is a historical research diagnostic built from synthetic/static sample data. Treat the examples as a way to check artifact shape, assumptions, caveats, and reproducibility, not as evidence beyond the artifact period.

## 30-second online demo

Open the public static demo:

- <https://sergioyin.github.io/market-signal-lab/>

If you are reading this on GitHub, open that hosted demo first. The relative
artifact links below point to checked-in files for review, not to a live trading
or prediction app.

Then use one of these static review routes:

- [Static Sample Gallery](reports/index.html) - open the browser-readable artifact dashboard.
- [Cold-User Review Route](reports/cold-user-review-route.md) - follow the compact first-time review path.
- [Assumption Ledger Summary](reports/assumption-ledger-summary.md) - scan assumptions, risk boundaries, evidence paths, and non-claims.
- [Stress Kit Quickstart Card](reports/stress-kit-quickstart-card.md) - read the two-minute static/no-advice checklist before the full stress kit.

These artifacts are review aids only, not advice, forecasts, recommendations,
or trading instructions. Deeper reviewer links are grouped under
[Core artifacts](#core-artifacts).

## 60-second local verification

```bash
git clone https://github.com/SergioYin/market-signal-lab.git
cd market-signal-lab
python -m market_signal_lab.cli --validate-thesis-ledger
```

For the first-time public-review route, run `python -m market_signal_lab.cli --cold-user-review-route`.
For the reviewer acceptance scorecard, run `python -m market_signal_lab.cli --reviewer-acceptance-scorecard`.
For the strategy assumption stress kit, run `python -m market_signal_lab.cli --strategy-assumption-stress-kit`.
For the two-minute stress-kit quickstart card, run `python -m market_signal_lab.cli --stress-kit-quickstart-card`.
For the compact assumption ledger summary, run `python -m market_signal_lab.cli --assumption-ledger-summary`.

For the deterministic public rerun receipt, run `python -m market_signal_lab.cli --reviewer-rerun-receipt`. It writes `reports/reviewer-rerun-receipt.md` and `reports/reviewer-rerun-receipt.json` without reading market data, fetching live data, connecting to brokers, inspecting accounts, routing orders, sizing positions, forecasting, recommending, or providing investment advice.

The command validates the checked-in thesis-ledger JSON and writes acceptance artifacts. Compare its output with:

- [Cross-Asset Thesis Ledger JSON](reports/cross-asset-thesis-ledger.json)
- [Thesis-Ledger Acceptance Summary](reports/cross-asset-thesis-ledger-acceptance.md)
- [Thesis-Ledger Acceptance JSON](reports/cross-asset-thesis-ledger-acceptance.json)

Validate a specific local packet while printing Markdown to stdout:

```bash
python -m market_signal_lab.cli --validate-thesis-ledger path/to/cross-asset-thesis-ledger.json \
  --json-output reports/my-ledger-acceptance.json
```

## Beginner checklist

Before reading any output, check:

- Is the data synthetic/static, not live?
- Does the artifact show assumptions, fees, exposure, drawdown, and caveats?
- Does the report compare against a same-period buy-and-hold baseline without calling it a recommendation?
- Are modeled entries/exits clearly historical model states, not actions to take?
- Are train/test ranks and `robustness_flag` labels presented as review diagnostics, not proof that labels will hold elsewhere?
- Are leveraged ETF-like examples labeled as simplified and risky, especially across multiple days?

Use the full [Beginner Backtest Reading Checklist](reports/beginner-prediction-checklist.md) and [JSON version](reports/beginner-prediction-checklist.json) when reviewing a sample.

## Prediction-readiness audit quickstart

Generate a deterministic audit from the checked-in thesis ledger:

```bash
python -m market_signal_lab.cli --prediction-readiness-audit
```

By default this reads `reports/cross-asset-thesis-ledger.json` and writes
`reports/prediction-readiness-audit.md` plus
`reports/prediction-readiness-audit.json`. The audit labels static data,
non-advice boundaries, benchmark fields, fee/drawdown/exposure diagnostics,
train/test diagnostics, and leveraged ETF-like caveats for review only.
It is a research-boundary audit, not a readiness score for trading or forecasting.

## Strategy assumption stress kit

Generate a deterministic static stress kit for reviewing strategy assumptions:

```bash
python -m market_signal_lab.cli --strategy-assumption-stress-kit
```

By default this writes `reports/strategy-assumption-stress-kit.html`,
`reports/strategy-assumption-stress-kit.md`, and
`reports/strategy-assumption-stress-kit.json`. Use `--html-output PATH` to
write the browser-openable artifact somewhere else while preserving the
Markdown and JSON defaults. The kit names assumption groups, stress checks,
beginner risk boundaries, and leveraged ETF-like path dependency, volatility
drag, and extreme drawdown caveats. Its release-readiness receipt records exact
rerun commands, generated output paths, and no-live-data/no-advice boundary
claims. It does not use live data, brokers, orders, forecasts,
recommendations, position sizing, or advice.

Generate the focused two-minute static/no-advice reviewer route before opening the full stress kit:

```bash
python -m market_signal_lab.cli --stress-kit-quickstart-card
```

By default this writes `reports/stress-kit-quickstart-card.md` and
`reports/stress-kit-quickstart-card.json`. The card is the short route into the
full stress kit and condenses scope, assumptions, stress-language, leveraged
ETF-like caveat, and boundary checks. It is a static reviewer checklist only,
with no live-data, broker/account, order, position-sizing, forecast,
recommendation, or advice surface.

## Assumption ledger summary

Generate a deterministic static summary for cold reviewers:

```bash
python -m market_signal_lab.cli --assumption-ledger-summary
```

By default this writes `reports/assumption-ledger-summary.md` and
`reports/assumption-ledger-summary.json`. The summary lists strategy
assumptions, risk boundaries, generated evidence paths, and what is not being
claimed. It is a static review aid only, with no live-data, broker/account,
order, position-sizing, forecast, recommendation, or advice surface.

## Reviewer evidence bundle integrity

Cold reviewers can open `reports/reviewer-evidence-bundle.md` and use its artifact hash summary to confirm the listed static review files were present with recorded SHA-256 bytes at generation time. The hashes are artifact-integrity evidence only; they do not validate financial correctness, future performance, recommendations, or investment suitability. Regenerate the bundle and refresh that summary with:

```bash
python -m market_signal_lab.cli --reviewer-evidence-bundle
```

## Reviewer acceptance scorecard

Open `reports/reviewer-acceptance-scorecard.md` for a deterministic acceptance scorecard covering public-review readiness, reproducibility evidence, risk boundaries, and next actions. The scorecard uses existing static artifact paths and writes a matching structured JSON file at `reports/reviewer-acceptance-scorecard.json`; it is research-only and is not a trading-readiness, forecasting, recommendation, or investment-advice approval.

```bash
python -m market_signal_lab.cli --reviewer-acceptance-scorecard
```

After regeneration, inspect the generated diff before citing the scorecard:

```bash
git diff -- reports/reviewer-acceptance-scorecard.md reports/reviewer-acceptance-scorecard.json
```

Review the Markdown `Overall Label`, scorecard table, `Risk Boundaries`, and
`Next Actions` sections, then check the JSON fields such as `research_only`,
`static_only`, `no_live_data`, `no_broker_or_account`, and
`not_investment_advice` match the public-review boundary you expect.

## Sample output summary

The checked-in sample artifacts show:

- Historical total return, max drawdown, exposure, modeled fee drag, and same-period buy-and-hold comparison.
- Scenario and risk notes in Markdown, HTML, and JSON.
- Split-sweep train/test ranks, return gaps, and `robustness_flag` labels.
- Fee-sensitivity and regime-comparison artifacts for deterministic synthetic fixtures, not claims beyond those fixtures.
- Cross-asset thesis-ledger validation outputs.

These summaries help check reproducibility, assumptions, and caveats only. They are not predictions, forecasts, recommendations, action instructions, or investment advice.

## Core artifacts

- Start here: [Static Sample Gallery](reports/index.html), [Cold-User Review Route](reports/cold-user-review-route.md), and [Static Gallery Manifest](docs/static-gallery-manifest.md).
- Main report path: [Single Backtest Report](reports/sample-report.md), [JSON](reports/sample-report.json), [Scenario Card](reports/scenario-card.md), and [Research Packet](reports/pretrade-packet.md).
- Comparisons: [Regime Comparison](reports/regime-comparison.md), [HTML](reports/regime-comparison.html), [JSON](reports/regime-comparison.json), and [Fee Sensitivity Comparison](reports/fee-sensitivity.md).
- Reading and validation: [Beginner Checklist](reports/beginner-prediction-checklist.md), [Assumption Ledger Summary](reports/assumption-ledger-summary.md), [Strategy Assumption Stress Kit](reports/strategy-assumption-stress-kit.html), [Stress Kit Quickstart Card](reports/stress-kit-quickstart-card.md), [Strategy Assumption Stress Kit Guide](docs/strategy-assumption-stress-kit.md), [Reviewer Acceptance Scorecard](reports/reviewer-acceptance-scorecard.md), [Cross-Asset Thesis Ledger](reports/cross-asset-thesis-ledger.md), and [Thesis-Ledger Acceptance Summary](reports/cross-asset-thesis-ledger-acceptance.md).
- Review guides: [Methodology Audit](docs/methodology-audit.md), [Assumption Ledger Summary Guide](docs/assumption-ledger-summary.md), [Strategy Assumption Stress Kit Guide](docs/strategy-assumption-stress-kit.md), [Quick-Tour Preview](docs/quick-tour-preview.md), [Three-Minute Review Route](docs/three-minute-review.md), [Cold User Evidence Card](docs/cold-user-evidence-card.md), [Reviewer Acceptance Scorecard Guide](docs/reviewer-acceptance-scorecard.md), [Evidence Card Walkthrough](docs/evidence-card-walkthrough.svg), [Public Share Summary](docs/public-share-summary.md), [Reviewer FAQ](docs/reviewer-faq.md), and [Promotion Checklist](docs/promotion-checklist.md).
- Reviewer handoff: [Reviewer Evidence Bundle](reports/reviewer-evidence-bundle.md), [Reviewer Rerun Receipt](reports/reviewer-rerun-receipt.md), [Reviewer Acceptance Scorecard](reports/reviewer-acceptance-scorecard.md), [Assumption Ledger Summary](reports/assumption-ledger-summary.md), [Strategy Assumption Stress Kit](reports/strategy-assumption-stress-kit.html), [Stress Kit Quickstart Card](reports/stress-kit-quickstart-card.md), [Cold-User Review Route](reports/cold-user-review-route.md), and [Prediction-Readiness Audit](reports/prediction-readiness-audit.md).

For maintainer context, read [Architecture](docs/architecture.md) and [ADR 0001: Static Research Artifacts](docs/adr/0001-static-research-artifacts.md) before changing artifact generation or public scope.

## Generate more artifacts

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

Research packet artifact:

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
recommended action, or an execution workflow.

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
placeholder regimes using historical model return, buy-and-hold return,
drawdown, exposure, cash-time, exposure-change, and whipsaw diagnostics. The
regime labels are fixture scenarios for review and tests, not market classifications,
not recommendations, not forecasts, and not a guarantee of future returns.

Single backtest reports include `buy_and_hold_total_return` and
`strategy_minus_buy_and_hold_return` metrics. These compare the model result
with a simple same-period buy-and-hold baseline over the supplied CSV. They are
historical research diagnostics only, not advice or instructions to reuse the
model.

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

## Research-only scope

Market Signal Lab is for research and learning. It has no broker connection, account workflow, order workflow, or live instruction surface. Treat every result as a historical experiment, not a production cue.

Leveraged ETF examples such as TQQQ/QLD need extra caution, especially for beginners. Many of these products reset exposure every day, so a multi-day result depends on the order of daily moves and cannot be estimated by simply multiplying the underlying index's start-to-end return. Leverage can magnify losses quickly, choppy markets can create volatility drag, and extreme drawdowns can arrive faster than in unlevered examples. The bundled leveraged ETF-like sample data is synthetic and simplified; it is useful for checking historical diagnostic artifact shape, not for estimating real fund behavior or providing advice. It is not a full model of real fund fees, tracking differences, financing costs, taxes, liquidity, or market impact.

## Purpose

- Provide a small, explainable workflow for research-only static backtest artifact packaging.
- Keep experiments deterministic and scriptable so results can be reproduced.
- Make assumptions explicit through generated experiment reports.
- Compare historical model results with a simple buy-and-hold baseline for context.

## Target users

- Students and analysts exploring historical model diagnostics.
- Product, research, and quant teams evaluating baseline static backtest artifact behavior.
- Engineers building learning projects around market-data pipelines.
- Anyone comparing model settings against historical sample data.

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
- It currently uses a single model pattern: moving-average crossover labels.
- It is built around CSV-based OHLC input and does not fetch market data automatically.
- Performance metrics are educational and diagnostic, not investment advice.
- Buy-and-hold benchmark metrics are historical diagnostics, not recommendations.
- Fee sensitivity artifacts compare historical model assumptions only; they do not estimate real execution costs.
- Exposure review fields are historical model metadata, not advice or action instructions.
- Scenario/risk interpretation fields are historical diagnostics, not advice, forecasts, broker/order guidance, or real-time execution cues.
- Train/test sweep rankings and robustness flags are research diagnostics, not predictions or stability claims.
- Outputs are reproducible artifacts for analysis, not live-system cues.

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
- [Strategy Assumption Stress Kit Guide](docs/strategy-assumption-stress-kit.md)
- [Three-Minute Review Route](docs/three-minute-review.md)
- [Local Audit Commands](docs/local-audit-commands.md)
- [Public Share Copy](docs/public-share-copy.md)
- [Reviewer Decision Tree](docs/reviewer-decision-tree.md)
- [Reviewer Acceptance Scorecard Guide](docs/reviewer-acceptance-scorecard.md)
- [v1.30.2 Release Notes](docs/release-v1.30.2.md)
- [v1.30.1 Release Notes](docs/release-v1.30.1.md)
- [v1.30.0 Release Notes](docs/release-v1.30.0.md)
- [v1.23.0 Release Notes](docs/release-notes-v1.23.0.md)
- [v1.22.1 Release Notes](docs/release-notes-v1.22.1.md)
- [v1.22.0 Release Notes](docs/release-notes-v1.22.0.md)
- [v1.22.0 Release Checklist](docs/release-v1.22.0.md)

The full release archive lives in the [Documentation Map](docs/index.md).
