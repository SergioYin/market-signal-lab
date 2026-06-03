# v1.20.2 Release Notes

Market Signal Lab v1.20.2 adds public share copy so the project can be described consistently as a static research-artifact packaging reference without overstating sample backtest outputs.

## Added

- Adds [Public Share Copy](public-share-copy.md), with a one-line description, short share note, unsafe claims to avoid, and a safe call to action.
- Links the share-copy guide from the README, docs map, static manifest, and root landing page.

## Boundaries

This increment is documentation and release metadata only. It adds no live data access, no broker or account workflow, no order workflow, no position sizing, no recommendation engine, no forecasts, and no investment advice.

## Verification

- `python scripts/selfcheck.py`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`
