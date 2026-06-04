# v1.21.0 Release Checklist

Release v1.21.0 packages the reviewer evidence bundle increment.

## Included

- `--reviewer-evidence-bundle` CLI route with default Markdown and JSON outputs.
- Checked-in `reports/reviewer-evidence-bundle.md` and `reports/reviewer-evidence-bundle.json` static artifacts.
- Tests for default bundle generation and CSV rejection.
- README, docs index, root landing, and selfcheck coverage for the new static route.
- Package metadata and CLI version report `1.21.0`.

## Verification commands

```bash
python -m market_signal_lab.cli --reviewer-evidence-bundle
python -m market_signal_lab.cli --validate-thesis-ledger
python -m unittest discover -s tests
python scripts/selfcheck.py
python -m compileall market_signal_lab tests scripts
git diff --check
```

## Scope boundary

No live data, no broker/account/order workflow, no position sizing, no forecasts, no recommendations, and no investment advice. Leveraged ETF-like sample labels remain historical diagnostics only, with daily-reset/path-dependency caveats.

See [v1.21.0 Release Notes](release-notes-v1.21.0.md).
