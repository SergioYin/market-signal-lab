# v1.16.0 Release Notes

Market Signal Lab v1.16.0 adds static HTML output for the offline methodology-audit scoring utility. It keeps the scorer local and reviewer-driven while making the checked-in score summary browser-openable.

## Added

- `market-signal-lab --score-methodology-audit PATH --html-output PATH`, which writes a static HTML rendering of the methodology audit score summary.
- Related local artifact links in the HTML score report when `--output` and `--json-output` are supplied.
- Selfcheck generation for `reports/methodology-audit-score.html`.

## Changed

- Updates package and CLI version metadata to `1.16.0`.
- Registers the HTML score artifact in the static gallery, manifest, README, documentation map, release docs, and selfcheck link sources.

## Boundaries

The HTML score report is a static rendering of reviewer-entered PASS/WARN/FAIL statuses from a local JSON file. It has no JavaScript, no external assets, no live data, no broker or account workflow, no orders, no position sizing, no recommendations, no forecasts, and no investment advice.
