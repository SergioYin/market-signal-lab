# v1.20.1 Release Notes

Market Signal Lab v1.20.1 adds a local audit command guide for reviewers who want a short, reproducible verification route after reading the three-minute review page.

## Added

- Adds [Local Audit Commands](local-audit-commands.md), covering thesis-ledger acceptance, full selfcheck, release hygiene, and what those commands do not prove.
- Links the audit-command guide from the README, docs map, static manifest, and root landing page.

## Boundaries

This increment is documentation and release metadata only. It adds no live data access, no broker or account workflow, no order workflow, no position sizing, no recommendation engine, no forecasts, and no investment advice.

## Verification

- `python scripts/selfcheck.py`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`
