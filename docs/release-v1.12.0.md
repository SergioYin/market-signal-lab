# v1.12.0 Release Checklist

Release v1.12.0 packages the public promotion kit increment for static, research-only sharing and review.

## Confirm

- Package metadata and CLI version report `1.12.0`.
- The public share summary, reviewer FAQ, and promotion checklist are linked from the public documentation map, root landing page, README, and static demo manifest.
- Public copy stays focused on the artifact workflow, checked-in evidence, reproducible sample outputs, and caveats.
- Runnable checks remain local and offline.
- Research-only, no-advice, no-live-data, no-broker, no-account, no-order, no-position-sizing, and no-forecast boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python scripts/selfcheck.py
pytest tests/test_packaging.py tests/test_selfcheck.py
```

See [v1.12.0 Release Notes](release-notes-v1.12.0.md).
