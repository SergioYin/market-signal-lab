# v1.3.2 Release Checklist

## Scope

- Add the public GitHub Pages URL to the README first-inspection path.
- Add the public static demo URL to the docs map.
- Keep local/offline gallery links intact.
- Preserve research-only, no-advice, no-live-data, and no-broker boundaries.

## Verification

Run before release:

- `python -m pytest tests/test_selfcheck.py tests/test_packaging.py tests/test_cli.py`
- `python scripts/selfcheck.py`
- `python -m unittest discover -s tests`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`

## Release Notes

See [v1.3.2 Release Notes](release-notes-v1.3.2.md).
