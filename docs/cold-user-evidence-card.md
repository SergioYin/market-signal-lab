# Cold User Evidence Card

Concise reviewer handoff for the checked-in public artifacts. This page is for research review only. It does not provide investment advice, trading recommendations, forecasts, live signals, broker guidance, account setup steps, order instructions, or instructions to buy, sell, hold, or trade.

Visual path: [Evidence card walkthrough](evidence-card-walkthrough.svg).

## 60-Second Route

1. Open the [Cold Review Checklist](cold-review-checklist.md) to confirm the static-demo scope and stop conditions.
2. Open the [Static Sample Gallery](../reports/index.html) and verify it is a static artifact index, not an execution surface.
3. Read the [scenario card](../reports/scenario-card.md) for a compact assumptions, metrics, diagnostics, risk-labels, and next-review view.
4. Compare the [scenario card JSON](../reports/scenario-card.json) if structured fields are needed.
5. Open the [cross-asset thesis ledger](../reports/cross-asset-thesis-ledger.md), then the [acceptance summary](../reports/cross-asset-thesis-ledger-acceptance.md).
6. Use the [Thesis-Ledger 60-Second Walkthrough](thesis-ledger-60-second-walkthrough.md) to interpret PASS/WARN/FAIL.
7. Finish with [Risk Boundaries](risk-boundaries.md) and [Data Provenance](data-provenance.md).

## Proof Artifacts

- [Static Sample Gallery](../reports/index.html): demonstrates that the public surface is a no-JavaScript, relative-link artifact gallery, not a live trading app.
- [Static Demo Manifest](static-gallery-manifest.md): records the Pages-safe static asset contract and gallery inventory.
- [Single backtest report](../reports/sample-report.md): shows the human-readable strategy configuration, date range, metrics, caveats, scenario/risk interpretation, and modeled exposure review for one checked-in sample.
- [Single backtest JSON](../reports/sample-report.json): demonstrates that the same single-run assumptions and diagnostics are available in machine-readable form.
- [Pre-trade research packet](../reports/pretrade-packet.md): gathers assumptions, historical diagnostics, beginner checklist, and research boundaries generated from the single-backtest path.
- [Scenario card](../reports/scenario-card.md): provides the shortest human-readable evidence card for assumptions, key metrics, exposure, fee, drawdown, risk labels, and next review.
- [Scenario card JSON](../reports/scenario-card.json): gives the structured version of the scenario-card proof.
- [Cross-asset thesis ledger](../reports/cross-asset-thesis-ledger.md): demonstrates a deterministic offline evidence packet across the checked-in placeholder assets.
- [Cross-asset thesis ledger JSON](../reports/cross-asset-thesis-ledger.json): provides the structured packet that the validator reads.
- [Thesis-ledger acceptance summary](../reports/cross-asset-thesis-ledger-acceptance.md): reports deterministic shape and boundary checks for the thesis-ledger packet.
- [Regime comparison sample](../reports/regime-comparison.md): compares synthetic bull, choppy, and drawdown-recovery fixtures side by side as historical diagnostics only.
- [Fee sensitivity sample](../reports/fee-sensitivity.md): shows how the same checked-in single-backtest settings respond to several modeled fee assumptions.
- [Split sweep sample](../reports/sample-sweep-split.md): demonstrates train/test ranking diagnostics and robustness labels inside the tiny bundled fixture.
- [Sample manifest](../reports/sample-manifest.md): records the inputs and outputs behind the sample artifact set.

## PASS/WARN/FAIL

- PASS means the acceptance artifact reports `accepted: true`, `error_count: 0`, and accepted checks. Read this as "the packet shape and public research boundaries matched the validator," not as evidence of profitability, robustness, suitability, or future performance.
- WARN means `warning_count` is greater than `0`. Treat warnings as review notes that require reading the message text before relying on the artifact shape.
- FAIL means `accepted: false`, `error_count` is greater than `0`, or any required check is not accepted. Treat the packet as rejected for reviewer handoff until the failing checks are understood.

## Research-Only Boundaries

- All checked-in sample data is static and synthetic unless an artifact explicitly says otherwise.
- Placeholder symbols such as `QQQ_LIKE`, `QLD_LIKE`, and `TQQQ_LIKE` are example-shaped labels, not real market-data claims.
- Backtests, sweeps, fee comparisons, regime comparisons, scenario cards, and thesis ledgers are historical diagnostics only.
- The artifacts do not fetch live market data, connect to brokers, access accounts, route orders, size positions, forecast returns, or recommend trades.
- Leveraged ETF-like examples are simplified fixtures and do not model complete real fund mechanics, financing, tracking error, taxes, liquidity, market impact, or investor suitability.
- A valid artifact can still describe a weak, overfit, incomplete, or irrelevant research setup. Acceptance confirms shape and boundary language only.
