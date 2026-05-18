# v0.5.0 Release Checklist

This checklist covers the public release readiness items for the v0.5.0 buy-and-hold benchmark release.

See [v0.5.0 Release Notes](release-notes-v0.5.0.md) for the concise public summary.

## Feature Summary

- Single backtest metrics include a same-period buy-and-hold baseline.
- Single backtest metrics include the strategy return minus that buy-and-hold baseline.
- Human-readable reports use beginner-friendly labels for the new benchmark fields.
- JSON output uses explicit research metric keys: `buy_and_hold_total_return` and `strategy_minus_buy_and_hold_return`.

## Commands To Verify

Run the test suite:

```bash
pytest
```

Run the project selfcheck, which also regenerates sample artifacts:

```bash
python scripts/selfcheck.py
```

Run the sample single backtest:

```bash
market-signal-lab examples/data/sample_tqqq_qld_like.csv \
  --symbol QQQ_LIKE \
  --short-window 20 \
  --long-window 50 \
  --fee-bps 10.0
```

Confirm the Markdown output includes:

- `Buy-and-hold total return`
- `Strategy minus buy-and-hold return`

## Public Artifacts

Expected public sample artifacts updated for this release:

- `reports/sample-report.md`
- `reports/sample-report.json`
- `reports/sample-report.html`

Review generated diffs before publishing to confirm that artifact changes are intentional and reproducible.

## No-Advice And Data-Provenance Boundaries

- Market Signal Lab remains research-only software. It does not provide investment advice, trading recommendations, forecasts, or live execution signals.
- Buy-and-hold benchmark fields are historical comparisons over the supplied CSV only; they are not advice to buy, hold, sell, or follow the strategy.
- The bundled sample CSV is synthetic example data with placeholder `_LIKE` symbols.
- The new benchmark fields do not fetch live data, connect to brokers, or make market predictions.

## Future Work

- Add clearer report grouping for strategy, benchmark, and risk metrics.
- Expand transaction cost, slippage, and risk modeling controls.
- Improve batch-run ergonomics for comparing multiple symbols.
