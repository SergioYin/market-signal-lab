# Reviewer Evidence Bundle

This bundle is a compact cold-review handoff for Market Signal Lab. It points a reviewer to the static first screen, the thesis-ledger acceptance artifact, the deterministic rerun command, and the methodology-risk caveats without adding live data, broker/account access, orders, forecasts, recommendations, or investment advice.

## First-screen route

1. Open `reports/index.html` to inspect checked-in sample artifacts before installing anything.
2. Read `reports/cross-asset-thesis-ledger-acceptance.md` for the current cross-asset thesis-ledger acceptance summary.
3. Rerun `python -m market_signal_lab.cli --validate-thesis-ledger` to regenerate the acceptance artifacts from the checked-in JSON packet.
4. Review `docs/methodology-audit.md` before treating any historical diagnostic as reusable evidence.

## Verification commands

- `python -m market_signal_lab.cli --reviewer-evidence-bundle`
- `python -m market_signal_lab.cli --validate-thesis-ledger`
- `python scripts/selfcheck.py`
- `python -m pytest`

## Beginner risk boundaries

- All metrics are historical diagnostics from bundled static/synthetic sample data.
- QLD_LIKE and TQQQ_LIKE examples model daily-reset leveraged ETF-like behavior; path dependency, volatility drag, and extreme drawdowns can make multi-day results differ sharply from simple 2x/3x expectations.
- The bundle is not a trading bot, signal service, broker workflow, order workflow, position-sizing workflow, forecast engine, recommendation, or investment advice.

## Boundary flags

- research_only: `True`
- static_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
