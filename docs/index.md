# Documentation Map

This is the canonical map for Market Signal Lab documentation. The project is a research-only backtesting sandbox; these documents do not provide investment advice, trading recommendations, forecasts, or live execution signals.

## Start Here

- [README](../README.md) - project overview, quickstart commands, and scope boundaries.
- [Public static demo](https://sergioyin.github.io/market-signal-lab/) - GitHub Pages entry point for the checked-in local gallery.
- [Cold Review Checklist](cold-review-checklist.md) - 2-5 minute research-only review path for first-time visitors.
- [Root Landing](../index.html) - GitHub Pages entry point for the local static demo and key docs.
- [Single backtest sample](../reports/sample-report.md) - fastest way to inspect `## Scenario/Risk Interpretation` and the modeled exposure review in the checked-in single backtest report.
- [Static Sample Gallery](../reports/index.html) - no-JavaScript dashboard first screen for the checked-in demo artifacts, including visible paths for the single report, pre-trade packet, regime comparison, fee sensitivity, split sweep, and manifest.
- [Static Demo Manifest](static-gallery-manifest.md) - Pages-safe gallery contract and local artifact inventory.
- [Single backtest JSON](../reports/sample-report.json) - machine-readable `scenario_risk_interpretation` and `exposure_trade_review` samples for the same research-only run.
- [Pre-trade research packet](../reports/pretrade-packet.md) - assumptions, historical diagnostics, beginner checklist, and risk boundaries generated from the existing single-backtest path.
- [Pre-trade research packet JSON](../reports/pretrade-packet.json) - structured version of the same packet.
- [Scenario card](../reports/scenario-card.md) - compact research-only card for embedding assumptions, key metrics, exposure/fee/drawdown diagnostics, risk labels, and next-review checklist in thesis-ledger or portfolio-review notes.
- [Scenario card JSON](../reports/scenario-card.json) - structured version of the same scenario card.
- [Regime comparison sample](../reports/regime-comparison.md) - first artifact to open for the side-by-side synthetic bull/choppy/drawdown-recovery comparison; regenerate it with `market-signal-lab --regime-comparison`.
- [Regime comparison JSON](../reports/regime-comparison.json) - machine-readable version of the same synthetic regime comparison.
- [Regime comparison HTML](../reports/regime-comparison.html) - browser-openable view of the same checked-in artifact.
- [Fee sensitivity sample](../reports/fee-sensitivity.md) - research-only fee assumption comparison for the bundled single backtest.
- [Fee sensitivity JSON](../reports/fee-sensitivity.json) - structured output for the same fee sensitivity artifact.
- [Risk Boundaries](risk-boundaries.md) - public no-advice and no-execution boundaries.
- [Scenario/Risk Glossary](scenario-risk-glossary.md) - beginner definitions for exposure, modeled entry/exit, fee drag, drawdown, and buy-and-hold gap diagnostics.
- [Metric Guide](metric-guide.md) - definitions and caveats for reported metrics.
- [Split Sweep Walkthrough](split-sweep-walkthrough.md) - beginner reading guide for split-sweep robustness reports.
- [Example Data and Synthetic Data Caveats](example-data.md) - bundled sample-data limits.
- [Data Provenance](data-provenance.md) - how local CSV input and placeholder symbols are handled.

## Regime Comparison Boundary

The regime-comparison artifacts use deterministic synthetic sample data and placeholder regime labels. Run `market-signal-lab --regime-comparison` from the repository root to write `reports/regime-comparison.md`, `reports/regime-comparison.json`, and `reports/regime-comparison.html`. Open the Markdown file first for review. These artifacts are research-only aids for comparing historical diagnostics across fixture scenarios; they are not investment advice, recommendations, forecasts, market classifications, or a guarantee of future returns.

## Workflows

- [Config Files](config-files.md) - JSON config shape, precedence, and repeatable run examples.
- [Artifact Gallery](artifact-gallery.md) - checked-in sample report, sweep, split-sweep, manifest, JSON, and HTML artifacts.

## Release Notes

- [v1.8.0 Release Notes](release-notes-v1.8.0.md)
- [v1.8.0 Release Checklist](release-v1.8.0.md)
- [v1.7.0 Release Notes](release-notes-v1.7.0.md)
- [v1.7.0 Release Checklist](release-v1.7.0.md)
- [v1.6.0 Release Notes](release-notes-v1.6.0.md)
- [v1.6.0 Release Checklist](release-v1.6.0.md)
- [v1.5.0 Release Notes](release-notes-v1.5.0.md)
- [v1.5.0 Release Checklist](release-v1.5.0.md)
- [v1.4.0 Release Notes](release-notes-v1.4.0.md)
- [v1.4.0 Release Checklist](release-v1.4.0.md)
- [v1.3.5 Release Notes](release-notes-v1.3.5.md)
- [v1.3.5 Release Checklist](release-v1.3.5.md)
- [v1.3.4 Release Notes](release-notes-v1.3.4.md)
- [v1.3.4 Release Checklist](release-v1.3.4.md)
- [v1.3.3 Release Notes](release-notes-v1.3.3.md)
- [v1.3.3 Release Checklist](release-v1.3.3.md)
- [v1.3.2 Release Notes](release-notes-v1.3.2.md)
- [v1.3.2 Release Checklist](release-v1.3.2.md)
- [v1.3.1 Release Notes](release-notes-v1.3.1.md)
- [v1.3.1 Release Checklist](release-v1.3.1.md)
- [v1.3.0 Release Notes](release-notes-v1.3.0.md)
- [v1.3.0 Release Checklist](release-v1.3.0.md)
- [v1.2.1 Release Notes](release-notes-v1.2.1.md)
- [v1.2.1 Release Checklist](release-v1.2.1.md)
- [v1.2.0 Release Notes](release-notes-v1.2.0.md)
- [v1.2.0 Release Checklist](release-v1.2.0.md)
- [v1.1.0 Release Notes](release-notes-v1.1.0.md)
- [v1.1.0 Release Checklist](release-v1.1.0.md)
- [v1.0.0 Release Notes](release-notes-v1.0.0.md)
- [v1.0.0 Release Checklist](release-v1.0.0.md)
- [v0.9.0 Release Notes](release-notes-v0.9.0.md)
- [v0.9.0 Release Checklist](release-v0.9.0.md)
- [v0.8.0 Release Notes](release-notes-v0.8.0.md)
- [v0.8.0 Release Checklist](release-v0.8.0.md)
- [v0.7.0 Release Notes](release-notes-v0.7.0.md)
- [v0.7.0 Release Checklist](release-v0.7.0.md)
- [v0.6.0 Release Notes](release-notes-v0.6.0.md)
- [v0.6.0 Release Checklist](release-v0.6.0.md)
- [v0.5.0 Release Notes](release-notes-v0.5.0.md)
- [v0.5.0 Release Checklist](release-v0.5.0.md)
- [v0.4.0 Release Notes](release-notes-v0.4.0.md)
- [v0.4.0 Release Checklist](release-v0.4.0.md)
- [v0.3.0 Release Notes](release-notes-v0.3.0.md)
- [v0.3.0 Release Checklist](release-v0.3.0.md)
