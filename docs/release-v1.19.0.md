# v1.19.0 Release Checklist

Release v1.19.0 packages the public-safe architecture and maintainer documentation increment.

## Confirm

- Package metadata and CLI version report `1.19.0`.
- `docs/architecture.md` explains the static-first architecture, CLI artifact pipeline, methodology audit modules, sample reports, test/selfcheck gates, and intentionally excluded live-data, broker, trading, recommendation, forecast, and advice workflows.
- `docs/adr/0001-static-research-artifacts.md` records the static research artifact decision.
- README, documentation map, root landing page, static demo manifest, release docs, and selfcheck link sources include the architecture docs.
- The increment is documentation-only except version metadata.
- Research-only, no-advice, no-live-data, no-broker, no-account, no-order, no-position-sizing, no-recommendation, and no-forecast boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python scripts/selfcheck.py
pytest tests/test_packaging.py tests/test_cli.py tests/test_selfcheck.py
```

See [v1.19.0 Release Notes](release-notes-v1.19.0.md).
