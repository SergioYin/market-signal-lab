# v1.6.0 Release Notes

Market Signal Lab v1.6.0 is a static gallery dashboard increment for the checked research artifact trail.

## Changed

- Updates `reports/index.html` so the first screen is a compact no-JavaScript dashboard.
- Adds dashboard cards with visible local artifact paths for the single report, regime comparison, fee sensitivity, split sweep, and manifest.
- Keeps all gallery links relative and local, with no external assets, remote data calls, broker connection, or account flow.
- Updates the static demo manifest, artifact gallery notes, documentation map, and README to describe the v1.6.0 dashboard contract.
- Adds selfcheck coverage for the v1.6.0 dashboard cards, visible artifact paths, and required local links.
- Updates package and CLI version metadata to `1.6.0`.

## Verification Expectations

- Regenerate the static artifact trail with `python scripts/selfcheck.py`.
- Run focused coverage for selfcheck, HTML, manifest, and packaging behavior.
- Confirm the checked gallery remains research-only and synthetic-data only.
- Confirm `git diff --check` is clean.

## Boundaries

- Dashboard cards are navigation aids for checked research artifacts only.
- Artifacts use bundled synthetic/static sample data and historical diagnostics only.
- The gallery does not provide investment advice, recommendations, forecasts, broker guidance, live market data, or execution cues.
