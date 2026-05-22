# v1.3.4 Release Checklist

## Scope

- Fix stale public static-demo manifest version labeling.
- Make the cold-review checklist visible from the root static landing page.
- Make the cold-review checklist visible from the static sample gallery first screen.
- Preserve no-advice, no-live-data, no-broker, and static-demo boundaries.

## Verification

Run before release:

- `python -m pytest tests/test_selfcheck.py tests/test_packaging.py tests/test_cli.py`
- `python scripts/selfcheck.py`
- `python -m unittest discover -s tests`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`

## Release Notes

See [v1.3.4 Release Notes](release-notes-v1.3.4.md).
