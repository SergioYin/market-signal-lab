# v1.30.6 Release Notes

Market Signal Lab v1.30.6 adds a deterministic static visual capture checklist for cold reviewers.

## Start Here

- [Static Visual Capture Checklist](../reports/static-visual-capture-checklist.md) - public-safe local screenshot/GIF checklist for the static gallery route.
- [Static Visual Capture Checklist JSON](../reports/static-visual-capture-checklist.json) - structured version with boundary flags, capture options, source artifact hashes, and do-not-capture rules.
- [Static Sample Gallery](../reports/index.html) - local static gallery target for screenshot capture.
- [Visual Acceptance Bundle](../reports/visual-acceptance-bundle.md) - bounded visual review handoff referenced by the checklist.

## Changed

- Added `--static-visual-capture-checklist` as a deterministic stdlib-only CLI artifact mode.
- Added generated Markdown and JSON checklist artifacts under `reports/`.
- Linked the checklist from the README, documentation map, root landing page, static gallery, and gallery docs.
- Kept capture guidance bounded to local static files and public-safe review evidence; the CLI does not create screenshots or GIFs.

## Verification

```bash
python -m market_signal_lab.cli --static-visual-capture-checklist
python -m pytest tests/test_static_visual_capture_checklist.py tests/test_cli.py tests/test_packaging.py
python scripts/selfcheck.py
```

## Boundaries

The Static Visual Capture Checklist is a static research-review artifact only. It does not provide live data, broker/account access, order routing, position sizing, forecasts, recommendations, trading signals, suitability review, or investment advice. Screenshot and GIF guidance is for public-safe orientation evidence only and must not capture private names, absolute local paths, accounts, orders, holdings, current quotes, or action guidance.
