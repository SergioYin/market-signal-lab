# v1.17.0 Release Checklist

Release v1.17.0 packages the methodology-audit review schema and validation-message increment for public-safe reviewer workflows.

## Confirm

- Package metadata and CLI version report `1.17.0`.
- `docs/methodology-audit-review-schema.md` documents the reviewer JSON object, check rows, accepted statuses, and score output shape.
- Invalid methodology audit check names produce row-specific CLI errors.
- Invalid methodology audit statuses produce check-specific CLI errors with accepted values.
- README, documentation map, root landing page, static demo manifest, release docs, and selfcheck link sources include the schema page.
- Research-only, no-advice, no-live-data, no-broker, no-account, no-order, no-position-sizing, no-recommendation, and no-forecast boundaries remain explicit.

## Suggested Checks

```bash
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli --score-methodology-audit examples/configs/methodology-audit-review.json
python scripts/selfcheck.py
pytest tests/test_cli.py tests/test_packaging.py tests/test_selfcheck.py
```

See [v1.17.0 Release Notes](release-notes-v1.17.0.md).
