# v1.16.0 Release Checklist

Release v1.16.0 packages the static methodology-audit score HTML artifact increment for public-safe reviewer workflows.

## Confirm

- Package metadata and CLI version report `1.16.0`.
- `market-signal-lab --score-methodology-audit PATH --html-output PATH` writes a static browser-openable score summary.
- The HTML score report uses local relative links for matching Markdown and JSON artifacts when those paths are supplied.
- Selfcheck regenerates `reports/methodology-audit-score.html`.
- The static gallery and manifest include the HTML score artifact.
- Research-only, no-advice, no-live-data, no-broker, no-account, no-order, no-position-sizing, no-recommendation, and no-forecast boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli --score-methodology-audit examples/configs/methodology-audit-review.json --html-output reports/methodology-audit-score.html
python scripts/selfcheck.py
pytest tests/test_cli.py tests/test_packaging.py tests/test_selfcheck.py
```

See [v1.16.0 Release Notes](release-notes-v1.16.0.md).
