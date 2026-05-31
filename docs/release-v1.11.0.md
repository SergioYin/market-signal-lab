# v1.11.0 Release Checklist

Release v1.11.0 packages the cold-user evidence card increment for public, static research review.

## Confirm

- Package metadata and CLI version report `1.11.0`.
- The cold-user evidence card links the static gallery, scenario card, thesis ledger, acceptance summary, risk boundaries, and data provenance.
- The evidence-card walkthrough is a static documentation artifact and does not add an execution surface.
- PASS/WARN/FAIL language stays limited to artifact-shape and boundary review.
- Research-only, no-advice, no-live-data, and no-broker boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli --validate-thesis-ledger
pytest tests/test_packaging.py tests/test_selfcheck.py tests/test_thesis_ledger.py
```

See [v1.11.0 Release Notes](release-notes-v1.11.0.md).
