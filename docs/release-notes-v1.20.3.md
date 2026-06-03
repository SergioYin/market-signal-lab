# v1.20.3 Release Notes

Market Signal Lab v1.20.3 adds a reviewer decision tree that routes cold users to understanding, reproducibility, methodology-risk, public-sharing, and promotion-readiness checks.

## Added

- Adds [Reviewer Decision Tree](reviewer-decision-tree.md) as a compact review-routing document.
- Links the decision tree from the README, docs map, static manifest, and root landing page.

## Boundaries

This increment is documentation and release metadata only. It adds no live data access, broker/account/order workflow, position sizing, recommendation engine, forecast, or investment advice.

## Verification

- `python scripts/selfcheck.py`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`
