# v1.30.8 Release Notes

Market Signal Lab v1.30.8 adds a deterministic release-to-release static visual receipt comparison for public review handoffs.

## Start Here

- [Static Visual Release Comparison](../reports/static-visual-release-comparison.md) - compares the v1.30.7 static visual capture receipt baseline with the current static receipt scan, source receipt artifacts, hashes, and reviewer checklist.
- [Static Visual Release Comparison JSON](../reports/static-visual-release-comparison.json) - structured version of the comparison.
- [Static Visual Capture Receipt](../reports/static-visual-capture-receipt.md) - source receipt inventory used by the comparison.
- [Static Visual Capture Checklist](../reports/static-visual-capture-checklist.md) - public-safe local screenshot/GIF checklist referenced by the comparison.

## Changed

- Added `--static-visual-release-comparison` as a deterministic stdlib-only CLI artifact mode.
- Added generated Markdown and JSON comparison artifacts under `reports/`.
- Linked the comparison from the README, documentation map, artifact gallery, static gallery manifest, root landing page, static gallery, and release docs.
- Integrated the comparison into selfcheck and packaging resource coverage.

## Verification

```bash
python -m market_signal_lab.cli --static-visual-release-comparison
python -m pytest tests/test_static_visual_release_comparison.py tests/test_cli.py tests/test_packaging.py
python scripts/selfcheck.py
```

## Boundaries

The Static Visual Release Comparison is a static research-review artifact only. It compares checked-in static receipt paths, roles, status, and SHA-256 file-byte evidence; it does not fetch release tags, create screenshots or GIFs, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, or provide investment advice. PASS labels mean review-continuity checks passed; they do not validate financial correctness, future performance, suitability, profitability, or trading readiness.
