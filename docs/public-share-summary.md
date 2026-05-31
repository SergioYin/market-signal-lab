# Public Share Summary

Market Signal Lab is a research-only reference repo for packaging reproducible market-signal review artifacts that can be inspected, rerun, diffed, and shared as a static demo.

## Target Users

- Builders who want a compact example of turning backtest diagnostics into Markdown, JSON, HTML, manifest, scenario-card, and thesis-ledger artifacts.
- Reviewers who need a public-safe artifact trail with visible assumptions, deterministic sample outputs, and explicit boundary language.
- Researchers who want offline sample reports for comparing historical diagnostics, fee assumptions, regime fixtures, split-sweep behavior, and acceptance checks.

## Why Review Or Reuse

- It is small and zero-dependency at runtime for the checked-in workflows.
- The public demo is a static artifact gallery, not a live trading app.
- The sample outputs are checked in, so a reviewer can inspect the artifact shape before installing anything.
- The repo shows a reusable pattern for pairing human-readable reports with structured JSON and a manifest.
- The boundary docs are explicit: outputs are labeled as research-only historical diagnostics, not forecasts or advice.

## Quick Demo Route

1. Start with the [Static Sample Gallery](../reports/index.html) for the checked-in first screen.
2. Open the [Scenario Card](../reports/scenario-card.md) for the shortest assumptions, metrics, diagnostics, risk-label, and next-review view.
3. Open the [Cross-Asset Thesis Ledger](../reports/cross-asset-thesis-ledger.md), then the [Thesis-Ledger Acceptance Summary](../reports/cross-asset-thesis-ledger-acceptance.md).
4. Use the [Thesis-Ledger Walkthrough](thesis-ledger-60-second-walkthrough.md) to interpret the validator route and PASS/WARN/FAIL fields.
5. Check the [Static Demo Manifest](static-gallery-manifest.md) and [Sample Manifest](../reports/sample-manifest.md) to confirm the relative-link artifact inventory and reproduction record.
6. Finish with [Risk Boundaries](risk-boundaries.md) and [Data Provenance](data-provenance.md).

For a compact reviewer handoff, use the [Cold User Evidence Card](cold-user-evidence-card.md). For the broader documentation map, use [Documentation Map](index.md).

## Research-Only Boundaries

Market Signal Lab is not a trading bot, signal service, forecast engine, recommendation system, broker workflow, account workflow, order workflow, position-sizing tool, or source of investment advice.

The checked-in artifacts use static sample data and placeholder symbols for reproducible review. Backtests, sweeps, fee comparisons, regime comparisons, scenario cards, thesis ledgers, and acceptance summaries are historical research diagnostics only. They do not fetch live market data, connect to brokers, access accounts, route orders, size positions, predict future returns, or tell anyone what to buy, sell, hold, or trade.
