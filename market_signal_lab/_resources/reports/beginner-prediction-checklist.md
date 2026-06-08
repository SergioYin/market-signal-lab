# Beginner Backtest Reading Checklist

Use this static checklist to read historical backtest artifacts without treating sample results, labels, or checked items as predictions of future returns, recommendations, trading instructions, or investment advice.

## What This Artifact Is

- It explains how to read a historical backtest or a related review checklist without treating either one as a prediction of future returns, recommendation, or advice.
- It is deterministic and generated without live market data, broker connections, account access, orders, or position sizing.

## Why Public Reviewers Might Reference It

- Public reviewers can reference this artifact as a deterministic static review template for checking whether backtest writeups keep historical results separate from future-return predictions, recommendations, trading instructions, and investment advice.

## First-Use Route

1. Open `reports/sample-report.md`.
2. Keep this checklist beside that report and use the steps below before opening the other static sources.
3. To regenerate the checklist from the repo root, run `python -m market_signal_lab.cli --beginner-prediction-checklist`.

## How To Read A Historical Backtest

1. **Identify what file you are reading**: A backtest report is a historical review artifact. It describes how a model behaved under fixed assumptions on supplied rows.
2. **Check the source rows and date range**: Results only describe the included historical rows, symbols, fees, and strategy settings. Changing any of those inputs can change the result.
3. **Read returns, drawdown, and exposure as diagnostics**: Metrics summarize that historical run. They are not instructions and do not predict future returns or prices.
4. **Compare with same-period buy-and-hold**: The comparison is a same-window historical reference point, not guidance about what to buy, sell, or hold.
5. **Review the risk boundaries before sharing**: Do not turn sample diagnostics into advice, forecasts, position sizes, order steps, or claims about future returns.

## Open These Static Sources

- [reports/sample-report.md](sample-report.md)
- [reports/sample-report.json](sample-report.json)
- [reports/pretrade-packet.md](pretrade-packet.md)
- [reports/scenario-card.md](scenario-card.md)
- [docs/methodology-audit.md](../docs/methodology-audit.md)
- [docs/risk-boundaries.md](../docs/risk-boundaries.md)

## Risk Boundaries

- **Historical backtest limits**: Historical backtests and related checklist artifacts are limited to the supplied rows, fixed assumptions, and simplified calculations. They are examples for review only, not evidence of future returns.
- **Leveraged ETF daily-reset and path-dependency risk**: Leveraged ETF-like examples require extra caution. QLD_LIKE and TQQQ_LIKE are placeholder examples for risk review, not guidance about QLD, TQQQ, or any leveraged ETF. Daily reset mechanics make multi-day outcomes path-dependent; volatility drag and compounding can make realized paths differ sharply from simple 2x/3x expectations, and losses can grow quickly.
- **Scope limits**: Static artifact only. No live-data workflow, broker or account workflow, orders or order routing, position sizing, recommendation engine, forecast engine, or investment advice is provided.

## Do Not Use This For

- prediction of future returns
- investment advice
- trading recommendation
- live execution or signal use
- broker, account, or order workflow
- position sizing

## Boundary Flags

- research_only: `True`
- static_only: `True`
- historical_diagnostics_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`

## Verification Commands

- `python -m market_signal_lab.cli --beginner-prediction-checklist`
- `python scripts/selfcheck.py`
- `python -m pytest`
