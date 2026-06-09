# v1.26.0 Release Notes

Market Signal Lab v1.26.0 adds a deterministic reviewer rerun receipt for public reproducibility review. The release preserves the v1.25.0 cold-user review route, prediction-readiness audit, reviewer evidence bundle integrity summary, and existing static artifact gallery behavior.

## Added

- Added [Reviewer rerun receipt Markdown](../reports/reviewer-rerun-receipt.md) and [JSON](../reports/reviewer-rerun-receipt.json).
- Added the stdlib-only CLI route:

```bash
python -m market_signal_lab.cli --reviewer-rerun-receipt
```

- Added selfcheck coverage for deterministic receipt schema order, PASS/WARN checklist labels, boundary flags, required verification commands, expected artifacts, and rendered Markdown parity.
- Added gallery, manifest, landing, README, packaging, and release links for the receipt artifacts.

## Boundaries

The receipt is a static review artifact only. It lists commands and expected artifacts; it does not execute them, read market data, fetch live data, connect to brokers, inspect accounts, route orders, size positions, forecast returns, recommend trades, or provide investment advice.

## Verification

Regenerate the receipt:

```bash
python -m market_signal_lab.cli --reviewer-rerun-receipt
```

Run focused tests:

```bash
python -m pytest tests/test_cli.py tests/test_selfcheck.py tests/test_packaging.py
```

Run the broader local gate when preparing a release:

```bash
python scripts/selfcheck.py
```
