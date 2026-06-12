# Assumption Ledger Summary

This deterministic static artifact gives cold reviewers one place to check strategy assumptions, risk boundaries, generated evidence paths, and what Market Signal Lab is not claiming. Read it as a map of the artifact's assumptions and limits, not as a verdict on strategy quality or suitability. It does not read live data, connect to brokers or accounts, route orders, size positions, forecast, recommend, or provide investment advice.

## Purpose

- Give cold reviewers one compact ledger of strategy assumptions, risk boundaries, generated evidence paths, and explicit non-claims without reading live data or creating any advice surface.

## Strategy Assumptions

| assumption | summary | review boundary |
|---|---|---|
| static_sample_scope | Results and labels describe deterministic checked-in sample artifacts only. | Do not extend any result to live markets, another date window, another product, or an account. |
| historical_signal_state | Entries, exits, exposure, and strategy states are historical model diagnostics. | They are not buy, sell, hold, rebalance, sizing, or timing instructions. |
| cost_and_friction_limits | Modeled fees are review inputs, while spreads, taxes, liquidity, financing, tracking difference, and market impact remain caveats. | Do not treat simplified costs as a complete implementation model. |
| same_window_benchmarking | Benchmark comparisons are same-period context for artifact review. | They are not product rankings, forward expectations, or recommendations. |

## Risk Boundaries

- **research_scope**: The ledger summarizes documentation assumptions and static evidence paths only.
- **historical_diagnostics**: Historical metrics are sample diagnostics, not forecasts, guarantees, or loss limits.
- **leveraged_etf_like_examples**: Leveraged ETF-like samples require daily reset, path dependency, volatility drag, tracking, and severe drawdown caveats.
- **review_labels**: PASS, WARN, and FAIL labels describe artifact-review boundaries, not strategy quality or suitability.

## Generated Evidence Paths

| path | format | review use |
|---|---|---|
| [`reports/index.html`](index.html) | html | First screen for checked-in static sample artifacts. |
| [`reports/strategy-assumption-stress-kit.html`](strategy-assumption-stress-kit.html) | html | Full assumption and stress-boundary review kit. |
| [`reports/stress-kit-quickstart-card.md`](stress-kit-quickstart-card.md) | markdown | Two-minute route into no-advice stress-kit review. |
| [`reports/reviewer-evidence-bundle.md`](reviewer-evidence-bundle.md) | markdown | Cold-review handoff with local artifact hash summary. |
| [`reports/assumption-ledger-summary.md`](assumption-ledger-summary.md) | markdown | This compact assumption ledger summary. |
| [`reports/assumption-ledger-summary.json`](assumption-ledger-summary.json) | json | Structured version of this compact assumption ledger summary. |

## What Is Not Being Claimed

| claim not made | reason |
|---|---|
| future_performance | Static historical diagnostics do not predict future returns or risk. |
| tradability_or_execution | The artifact has no broker, account, order, routing, fill, or execution workflow. |
| position_size_or_suitability | No portfolio, account, risk tolerance, tax, liquidity, or suitability context is used. |
| recommendation_or_advice | The ledger is a review aid and does not tell a reader what to buy, sell, hold, size, or trade. |

## Reviewer Use

- Open this after the static gallery when reviewing public maturity.
- Use it to check whether assumptions and no-advice boundaries are visible before reading deeper artifacts.
- Treat every path as generated static evidence, not as financial validation.

## Boundary Flags

- research_only: `True`
- static_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`

## Boundary Claims

- This summary is generated from deterministic static definitions only and does not fetch, stream, refresh, or inspect live market data.
- This summary is a reviewer ledger only, not a forecast, recommendation, trading instruction, suitability view, or investment advice.

## Verification Commands

- `python -m market_signal_lab.cli --assumption-ledger-summary`
- `python scripts/selfcheck.py`
- `python -m pytest`
