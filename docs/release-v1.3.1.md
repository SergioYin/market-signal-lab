# v1.3.1 Release Checklist

## Scope

- Add a minimal root landing page for GitHub Pages.
- Link locally to the static sample gallery and key project docs.
- Keep the landing and gallery static with no scripts, no remote assets, no broker surfaces, and no live data.
- Preserve research-only and no-advice boundaries.

## Verification

Run before release:

- `python -m pytest tests/test_selfcheck.py tests/test_packaging.py tests/test_cli.py`
- `python scripts/selfcheck.py`
- `git diff --check`

## Release Notes

See [v1.3.1 Release Notes](release-notes-v1.3.1.md).
