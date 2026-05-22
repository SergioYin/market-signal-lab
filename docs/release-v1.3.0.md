# v1.3.0 Release Checklist

## Scope

- Improve cold-user first-screen clarity for the checked-in static gallery.
- Add a small static demo manifest for local relative artifact links.
- Keep the gallery GitHub Pages-safe with no scripts, no remote assets, and no live data or broker surfaces.
- Preserve research-only, no-advice, and leveraged ETF daily reset/path dependency warnings.

## Verification

Completed on 2026-05-23 before release:

- `python -m pytest` -> 154 passed.
- `python scripts/selfcheck.py` -> PASS for compileall, pytest, sample artifact generation, documentation/gallery links, static demo acceptance, public no-advice boundary, and static fixture provenance.
- `python -m unittest discover -s tests` -> OK; project tests are pytest-style, so unittest discovers 0 tests.
- `python -m compileall market_signal_lab tests scripts` -> PASS.
- `git diff --check` -> PASS.
- Diff hygiene scan for conflict/debug markers and secret-like patterns -> PASS.
- Public privacy scan for private/local context and credential-shaped strings -> PASS.

## Release Notes

See [v1.3.0 Release Notes](release-notes-v1.3.0.md).
