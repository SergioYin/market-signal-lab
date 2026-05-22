# v1.3.3 Release Checklist

## Scope

- Add a cold-review checklist for first-time visitors.
- Link the checklist from README and the documentation map.
- Keep the checklist research-only and beginner-readable.
- Preserve no-advice, no-live-data, no-broker, and static-demo boundaries.

## Verification

Run before release:

- `python -m pytest tests/test_selfcheck.py tests/test_packaging.py tests/test_cli.py`
- `python scripts/selfcheck.py`
- `python -m unittest discover -s tests`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`

## Release Notes

See [v1.3.3 Release Notes](release-notes-v1.3.3.md).
