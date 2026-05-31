# v1.15.0 Release Checklist

Release v1.15.0 packages the offline methodology-audit scoring CLI increment for public-safe reviewer workflows.

## Confirm

- Package metadata and CLI version report `1.15.0`.
- `market-signal-lab --score-methodology-audit examples/configs/methodology-audit-review.json` prints Markdown without requiring a CSV path.
- `market-signal-lab --score-methodology-audit PATH --json-output PATH` writes compact JSON with pass/warn/fail counts and a promotion gate suggestion.
- Invalid audit statuses are rejected.
- The scoring schema tracks `docs/methodology-audit.md` checks for look-ahead bias, survivorship bias, overfitting, fees and slippage, leveraged ETF-like daily reset risk, and no-advice/no-live-trading boundaries.
- Runnable checks remain local, deterministic, offline, and stdlib-only.
- Research-only, no-advice, no-live-data, no-broker, no-account, no-order, no-position-sizing, no-recommendation, and no-forecast boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli --score-methodology-audit examples/configs/methodology-audit-review.json
python scripts/selfcheck.py
pytest tests/test_cli.py tests/test_packaging.py tests/test_selfcheck.py
```

See [v1.15.0 Release Notes](release-notes-v1.15.0.md).
