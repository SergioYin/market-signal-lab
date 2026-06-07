# v1.24.0 Release Notes

Market Signal Lab v1.24.0 adds a public-safe artifact integrity summary to the reviewer evidence bundle. The summary records local static artifact presence, byte counts, and SHA-256 hashes captured at generation time. It is integrity evidence for checked-in review files only; it does not validate financial correctness, future performance, strategy quality, recommendations, suitability, or investment advice.

## Added

- Added an `artifact_integrity_summary` section to `reports/reviewer-evidence-bundle.json`.
- Added a matching artifact hash table to `reports/reviewer-evidence-bundle.md` for cold reviewers.
- Documented that the hashes cover local static reviewer evidence artifacts only and confirm file bytes at generation time.

## Verification Commands

Regenerate the reviewer bundle and inspect the artifact hash summary:

```bash
python -m market_signal_lab.cli --reviewer-evidence-bundle
```

Run the existing local review gates when preparing a release:

```bash
python scripts/selfcheck.py
git diff --check
```

Use the full test suite only when code changes or release policy require it:

```bash
python -m pytest
```

## Research-Only Finance Boundary

This release keeps Market Signal Lab as a static research-artifact package. It adds no live market data, broker or account workflow, order routing, position sizing, forecasts, recommendations, trading instructions, or investment advice. The artifact hashes should be read as reproducibility and file-integrity metadata, not as evidence that any financial result is correct, robust, tradable, suitable, or predictive.
