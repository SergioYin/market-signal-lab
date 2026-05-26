# v1.6.0 Release Checklist

## Scope

- Improve the checked-in `reports/index.html` first screen with compact dashboard cards.
- Show visible artifact paths for the single report, regime comparison, fee sensitivity, split sweep, and manifest.
- Keep the gallery no-JavaScript, local-relative, and free of external assets.
- Update static gallery docs, artifact gallery notes, README, and release documentation.
- Add selfcheck and test coverage for the v1.6.0 dashboard contract.
- Update package metadata and CLI version output to `1.6.0`.
- Preserve research-only, synthetic-data, no-advice, no-forecast, no-live-data, and no-broker boundaries.

## Verification

Run before release:

- `python -m pytest tests/test_selfcheck.py tests/test_html.py tests/test_manifest.py tests/test_packaging.py`
- `python scripts/selfcheck.py`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`

## Reviewer Note

The dashboard increment changes navigation and documentation only. Reviewers
should verify that the first screen points to checked artifacts with relative
local links and does not add JavaScript, remote assets, live data, broker
integration, forecasts, or trading instructions.

## Risk Boundaries

- Dashboard cards are artifact links, not trading signals.
- Synthetic sample data remains the only checked demo data source.
- Scenario, regime, fee, and split-sweep fields remain historical diagnostics only.
- No broker connection, live market data, recommendations, or execution cues are introduced.

## Release Notes

See [v1.6.0 Release Notes](release-notes-v1.6.0.md).
