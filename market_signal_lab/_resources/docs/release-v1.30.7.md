# v1.30.7 Release Notes

Market Signal Lab v1.30.7 adds a deterministic static visual capture receipt for public review handoffs.

## Start Here

- [Static Visual Capture Receipt](../reports/static-visual-capture-receipt.md) - repo-relative static visual evidence inventory with present/missing status, byte counts, SHA-256 hashes, roles, routes, regeneration commands, and public evidence notes.
- [Static Visual Capture Receipt JSON](../reports/static-visual-capture-receipt.json) - structured version of the receipt.
- [Static Visual Capture Checklist](../reports/static-visual-capture-checklist.md) - public-safe local screenshot/GIF checklist for optional reviewer-created captures.
- [Static Sample Gallery](../reports/index.html) - local static gallery target referenced by the receipt.

## Changed

- Added `--static-visual-capture-receipt` as a deterministic stdlib-only CLI artifact mode.
- Added generated Markdown and JSON receipt artifacts under `reports/`.
- Linked the receipt from the README, documentation map, artifact gallery, static gallery manifest, root landing page, static gallery, and release docs.
- Integrated the receipt into selfcheck and packaging resource coverage.

## Verification

```bash
python -m market_signal_lab.cli --static-visual-capture-receipt
python -m pytest tests/test_static_visual_capture_receipt.py tests/test_cli.py tests/test_packaging.py
python scripts/selfcheck.py
```

## Boundaries

The Static Visual Capture Receipt is a static research-review artifact only. It scans checked-in local artifacts and does not create screenshots or GIFs, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast, recommend, or provide investment advice. It records file-byte provenance only; hashes do not validate financial correctness, future performance, suitability, profitability, or trading readiness.
