# v1.8.0 Release Checklist

## Scope

Release v1.8.0 packages the scenario-card export increment for Market Signal Lab.

## Artifact contract

- `market-signal-lab ... --scenario-card` writes `reports/scenario-card.md` and `reports/scenario-card.json` by default.
- The Markdown card contains source, assumptions, key metrics, diagnostics, scenario/risk interpretation, risk labels, and next-review checklist sections.
- The JSON card includes `card_type`, `schema_version`, `research_only`, `historical_diagnostics_only`, `no_broker_or_live_data`, `source`, `strategy_config`, `key_metrics`, `diagnostics`, `risk_labels`, and `next_review_checklist`.
- Static gallery and documentation paths reference the checked-in scenario-card artifacts.

## Verification commands

```bash
python -m pytest
python scripts/selfcheck.py
python -m compileall market_signal_lab tests scripts
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --fee-bps 10.0 \
  --scenario-card \
  --output reports/scenario-card.md \
  --json-output reports/scenario-card.json
git diff --check
```

## Public boundary checklist

- No broker connection, account field, live market data, order placement, alerting, forecast, or trade instruction surface.
- Historical/sample/backtest returns are labeled as diagnostics only.
- Leveraged ETF-like examples retain daily-reset, path-dependency, volatility-loss, and drawdown warnings.
- Public privacy scan passes before push/release.

See [v1.8.0 Release Notes](release-notes-v1.8.0.md).
