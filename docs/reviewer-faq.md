# Reviewer FAQ

Concise answers for cold reviewers. This page is for research review only. It does not provide investment advice, trading recommendations, forecasts, live signals, broker guidance, account setup steps, order instructions, or instructions to buy, sell, hold, or trade.

## Is this a trading bot?

No. Market Signal Lab is a static research artifact and backtesting sandbox. It has no broker or exchange connection, no account flow, no order routing, no position sizing workflow, and no execution surface. Start with the [Cold Review Checklist](cold-review-checklist.md) and [Risk Boundaries](risk-boundaries.md) for the public scope.

## Does it use live data?

No live data is used by the checked-in examples. The bundled CSVs are deterministic synthetic fixtures, and their provenance files label them as static sample data. The project reads local CSV files; it does not download, refresh, or validate live market data. See [Data Provenance](data-provenance.md), [Example Data and Synthetic Data Caveats](example-data.md), and the [Static Demo Manifest](static-gallery-manifest.md).

## What does validation mean?

Validation checks artifact shape and public research boundaries for the checked-in thesis-ledger packet. A PASS means the packet matched deterministic acceptance checks; it is not a profitability finding, forecast, suitability review, or trading safety approval. Read the [Thesis-Ledger Acceptance Summary](../reports/cross-asset-thesis-ledger-acceptance.md) with the [Thesis-Ledger 60-Second Walkthrough](thesis-ledger-60-second-walkthrough.md).

## Does this make the backtest tradable?

No. The assumption ledger summary and related backtest artifacts are static review aids for checked-in sample evidence. They do not make a strategy tradable and do not provide live data, broker/account access, order routing, position sizing, forecasts, recommendations, suitability review, or investment advice.

## What should a reviewer verify first?

First verify the boundary claims: static-only data, no live-data workflow, no broker/account workflow, no orders, no position sizing, no forecasts, no recommendations, and no investment advice. Then confirm the linked evidence paths in the [Assumption Ledger Summary](../reports/assumption-ledger-summary.md) resolve to checked-in local artifacts before reading any historical metrics.

## How are leveraged ETF-like examples bounded?

The `_LIKE` symbols are placeholder examples, not real QQQ, QLD, or TQQQ data. Leveraged ETF-like examples are simplified synthetic fixtures, not fund-return simulations, and do not model complete fund mechanics, daily reset effects, financing, tracking error, taxes, liquidity, market impact, or investor suitability. Treat any `QLD_LIKE` or `TQQQ_LIKE` output as high-risk historical scenario review only. See [Risk Boundaries](risk-boundaries.md) and [Data Provenance](data-provenance.md).

## What should a reviewer open first?

Open the [Cold User Evidence Card](cold-user-evidence-card.md) first for the shortest handoff. Then open the [Static Sample Gallery](../reports/index.html), [Scenario Card](../reports/scenario-card.md), [Cross-Asset Thesis Ledger](../reports/cross-asset-thesis-ledger.md), and [Thesis-Ledger Acceptance Summary](../reports/cross-asset-thesis-ledger-acceptance.md). Finish with [Risk Boundaries](risk-boundaries.md) and [Data Provenance](data-provenance.md) before drawing any research conclusion.
