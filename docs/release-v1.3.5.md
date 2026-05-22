# v1.3.5 Release Checklist

## Scope

- Add release-grade package metadata for public discovery surfaces.
- Add packaging tests for README, URL, author, keyword, and CLI metadata.
- Render duplicate nested/top-level manifest fields once in Markdown output.
- Regenerate checked sample artifacts.

## Verification

Run before release:

- `python -m pytest tests/test_selfcheck.py tests/test_packaging.py tests/test_cli.py tests/test_manifest.py`
- `python scripts/selfcheck.py`
- `python -m unittest discover -s tests`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`

## Release Notes

See [v1.3.5 Release Notes](release-notes-v1.3.5.md).
