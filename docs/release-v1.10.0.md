# v1.10.0 Release Checklist

Release v1.10.0 packages the thesis-ledger acceptance validator without adding dependencies or execution workflows.

## Confirm

- Package metadata and CLI version report `1.10.0`.
- Valid thesis-ledger packets return an accepted structured summary.
- Invalid but loaded packets return rejected summaries without raising for normal shape failures.
- CLI validation defaults to `reports/cross-asset-thesis-ledger.json` and can write Markdown/JSON acceptance artifacts.
- Research-only, no-advice, no-live-data, and no-broker boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli --validate-thesis-ledger
pytest tests/test_thesis_ledger.py tests/test_cli.py tests/test_packaging.py
```

See [v1.10.0 Release Notes](release-notes-v1.10.0.md).

