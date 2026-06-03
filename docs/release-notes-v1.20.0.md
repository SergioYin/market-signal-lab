# v1.20.0 Release Notes

Market Signal Lab v1.20.0 adds a three-minute cold-review route for public reviewers who need a fast way to inspect the static demo, methodology caveats, and one reproducible acceptance command before deciding whether to reuse the project pattern.

## Added

- Adds [Three-Minute Review Route](three-minute-review.md), a concise static reviewer path covering first-screen demo links, methodology-audit evidence, thesis-ledger validation, and a non-advice reviewer checklist.
- Links the route from the README, documentation map, root landing page, and static demo manifest.

## Boundaries

This increment is documentation and release metadata only. It adds no live data access, no broker or account workflow, no order workflow, no position sizing, no recommendation engine, no forecasts, and no investment advice.

## Verification

- `python -m unittest discover -s tests`
- `python scripts/selfcheck.py`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`
