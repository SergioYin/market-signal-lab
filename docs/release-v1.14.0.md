# v1.14.0 Release Checklist

Release v1.14.0 packages the static methodology-audit template CLI increment for public-safe reviewer workflows.

## Confirm

- Package metadata and CLI version report `1.14.0`.
- `market-signal-lab --methodology-audit-template` prints Markdown without requiring a CSV path.
- `market-signal-lab --methodology-audit-template --json-output PATH` writes compact JSON using the same static checks.
- The template wording tracks `docs/methodology-audit.md` checks for look-ahead bias, survivorship bias, overfitting, fees and slippage, leveraged ETF-like daily reset risk, and no-advice/no-live-trading boundaries.
- Selfcheck regenerates `reports/methodology-audit-template.md` and `reports/methodology-audit-template.json`.
- Runnable checks remain local and offline.
- Research-only, no-advice, no-live-data, no-broker, no-account, no-order, no-position-sizing, no-recommendation, and no-forecast boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli --methodology-audit-template
python scripts/selfcheck.py
pytest tests/test_cli.py tests/test_packaging.py tests/test_selfcheck.py
```

See [v1.14.0 Release Notes](release-notes-v1.14.0.md).
