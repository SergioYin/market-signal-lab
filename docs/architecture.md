# Architecture

Market Signal Lab is static-first by design. The package turns local, checked-in sample inputs into deterministic Markdown, JSON, HTML, and manifest artifacts that can be inspected from a checkout or a static host. The public surface is documentation and generated files, not a service, dashboard backend, broker integration, or live signal workflow.

The architecture goal is maintainability for public review: a cold reviewer should be able to open `index.html`, follow relative links, inspect sample artifacts, rerun the CLI from local files, and compare regenerated outputs without private context or network access.

## Static-First Surface

The root `index.html` and `reports/index.html` are plain HTML entry points. They use repository-relative links, no JavaScript, and no external assets. Documentation files in `docs/` describe how to read the outputs, how to review methodology assumptions, and where the project boundaries are.

Checked-in reports under `reports/` are sample artifacts, not runtime state. They are intentionally small, deterministic, and public-safe so they can be diffed in pull requests and opened directly in a browser or text editor.

## CLI Artifact Pipeline

The CLI in `market_signal_lab/cli.py` is the artifact generator. It reads local CSV/config files and writes deterministic outputs:

- Single backtest reports: Markdown, JSON, and optional static HTML.
- Parameter sweep and split-sweep reports: ranked historical diagnostics plus JSON and HTML views.
- Fee sensitivity reports: repeated runs across local fee assumptions.
- Regime comparison reports: deterministic synthetic fixture comparisons.
- Pre-trade packet and scenario card artifacts: compact research-only summaries derived from the single-backtest path.
- Cross-asset thesis ledger and acceptance artifacts: structured local evidence packets and validation summaries.
- Methodology audit templates, review templates, scores, and score HTML reports.

The pipeline is file-in, file-out. It does not fetch live market data, read brokerage accounts, send orders, size positions, or provide recommendations.

## Methodology Audit Modules

`market_signal_lab/methodology_audit.py` provides static reviewer artifacts for common sample-backtest risks:

- Look-ahead bias.
- Survivorship bias.
- Overfitting and parameter search risk.
- Fees, slippage, and omitted costs.
- Leveraged ETF-like daily reset risk.
- No-advice and no-live-trading boundaries.

The audit helpers produce templates and score reviewer-filled JSON. They are review gates for documentation quality and presentation risk; they do not certify a strategy, classify markets, forecast returns, or approve live use.

## Sample Reports

The checked-in sample reports under `reports/` are the public demonstration set. They are generated from synthetic/static fixtures in `examples/` and are intended to show artifact shape, caveats, and review flow.

The sample reports are historical diagnostics only. Placeholder symbols such as `QQQ_LIKE`, `QLD_LIKE`, and `TQQQ_LIKE` are fixture labels, not live instruments. The reports make assumptions visible so reviewers can inspect how outputs change when local inputs or config values change.

## Test And Selfcheck Gates

The test suite covers package metadata, CLI behavior, data parsing, metrics, report rendering, methodology audit validation, static HTML contracts, and generated artifact structure.

`python scripts/selfcheck.py` is the maintainer gate for public artifacts. It compiles Python files, runs pytest, regenerates sample artifacts, checks Markdown and HTML links, verifies static gallery contracts, scans public files for forbidden advice-like claims, and validates fixture provenance.

These gates are intentionally local. They provide confidence that the public artifact set is internally consistent without adding network or service dependencies.

## Out Of Scope

Live data, brokers, trading accounts, order workflows, position sizing, recommendations, forecasts, and investment advice are intentionally out of scope.

That boundary is part of the architecture, not a missing integration. Keeping the project static-first makes artifacts reproducible, inspectable, diffable, and safe to publish as examples. It also prevents the sample reports from being confused with live trading signals or instructions to act in markets.

See [ADR 0001: Static Research Artifacts](adr/0001-static-research-artifacts.md) for the maintainer decision record.
