# v1.18.0 Release Checklist

Release v1.18.0 packages the blank methodology-audit review JSON skeleton increment for public-safe reviewer workflows.

## Confirm

- Package metadata and CLI version report `1.18.0`.
- `market-signal-lab --methodology-audit-review-template` prints compact JSON to stdout without requiring a CSV path.
- `market-signal-lab --methodology-audit-review-template --json-output PATH` writes the same JSON skeleton and leaves stdout empty.
- The skeleton uses the accepted methodology audit check names in scoring order with blank `status` and `notes` fields for reviewers to fill.
- README, documentation map, artifact gallery, static demo manifest, release docs, and selfcheck sources include the new review-template artifact and command.
- Research-only, no-advice, no-live-data, no-broker, no-account, no-order, no-position-sizing, no-recommendation, and no-forecast boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli --methodology-audit-review-template
python -m market_signal_lab.cli --methodology-audit-review-template --json-output reports/methodology-audit-review-template.json
python scripts/selfcheck.py
pytest tests/test_cli.py tests/test_packaging.py tests/test_selfcheck.py
```

See [v1.18.0 Release Notes](release-notes-v1.18.0.md).
