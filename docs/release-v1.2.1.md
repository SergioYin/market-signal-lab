# v1.2.1 Release Checklist

## Scope

- Polish the static sample gallery first screen for public review.
- Add explicit leveraged ETF-like fixture caveats to the fee sensitivity artifact.
- Guard the gallery contract against remote links/assets.

## Verification

- `python -m pytest tests/test_selfcheck.py tests/test_cli.py tests/test_report.py`
- `python scripts/selfcheck.py`
- `python -m unittest discover -s tests`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`
- Public privacy scan.

## Release Notes

See [v1.2.1 Release Notes](release-notes-v1.2.1.md).