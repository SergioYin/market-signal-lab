# v1.13.0 Release Checklist

Release v1.13.0 packages the methodology-audit docs increment for static, research-only sample-backtest review.

## Confirm

- Package metadata and CLI version report `1.13.0`.
- The methodology audit is linked from the public documentation map, root landing page, README, and static demo manifest.
- The methodology audit frames PASS/WARN/FAIL rows as review evidence only, not certification, advice, recommendations, forecasts, or live trading signals.
- Public copy stays focused on checked-in artifacts, reproducibility evidence, methodology caveats, and static review boundaries.
- Runnable checks remain local and offline.
- Research-only, no-advice, no-live-data, no-broker, no-account, no-order, no-position-sizing, and no-forecast boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python scripts/selfcheck.py
pytest tests/test_packaging.py tests/test_selfcheck.py
```

See [v1.13.0 Release Notes](release-notes-v1.13.0.md).
