# v1.27.0 Release Notes

Market Signal Lab v1.27.0 adds the reviewer decision matrix route for a deterministic PASS/WARN/FAIL publication and promotion check on the checked-in static sample artifacts.

## Added

- Added the new CLI flag:

```bash
python -m market_signal_lab.cli --reviewer-decision-matrix
```

- Added generated artifacts:
  - `reports/reviewer-decision-matrix.md`
  - `reports/reviewer-decision-matrix.json`

- Integrated the matrix guide and generated artifacts into the public documentation surface (artifact gallery flow, gallery walkthrough docs, and release-links surface).

## Tests

- Added/updated checks in `tests/test_reviewer_decision_matrix.py` for schema-key order, gate semantics (`release_gate` and `promotion_gate`), markdown render assertions, and CLI conflict/restriction behavior.
- Added the v1.27.0 release-note link to docs-link registration coverage in `scripts/selfcheck.py` and `tests/test_selfcheck.py`.

## Research-Only Boundaries

This route writes static review metadata only. It does not fetch live data, route orders, size positions, connect to brokers, inspect accounts, forecast returns, recommend actions, or provide investment advice.

## Verification

Regenerate the matrix:

```bash
python -m market_signal_lab.cli --reviewer-decision-matrix
```

Run focused checks (and then broader selfcheck before any release):

```bash
python -m pytest tests/test_reviewer_decision_matrix.py tests/test_selfcheck.py
python scripts/selfcheck.py
```
