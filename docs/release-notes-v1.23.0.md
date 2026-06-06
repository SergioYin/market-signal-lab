# v1.23.0 Release Notes

Market Signal Lab v1.23.0 adds the static `prediction-readiness-audit` artifact for checking documentation boundaries in the checked-in thesis ledger. It keeps the project research-only and does not add live data, broker/account/order workflows, position sizing, forecasts, recommendations, trading instructions, or investment advice.

## Added

- Added `market-signal-lab --prediction-readiness-audit` to generate deterministic Markdown and JSON review artifacts from a static thesis-ledger JSON file.
- Added checked-in `reports/prediction-readiness-audit.md` and `reports/prediction-readiness-audit.json` artifacts with PASS/WARN/FAIL labels for static data, non-advice boundaries, benchmark fields, fee/drawdown/exposure diagnostics, train/test diagnostics, and leveraged ETF-like caveats.
- Added CLI and packaging coverage for the default audit path, including empty-cwd use of the bundled thesis-ledger JSON resource.

## Changed

- Updated the static gallery, documentation map, README quickstart, and selfcheck sample generation so the prediction-readiness audit is linked alongside the reviewer evidence bundle and beginner checklist.
- Package metadata and CLI version output identify this release as `1.23.0`.

## Verification Commands

```bash
python -m pytest
python scripts/selfcheck.py
git diff --check
```

Wheel empty-cwd smoke coverage remains exercised by:

```bash
python -m pytest tests/test_packaging.py -m wheel_smoke
```

## Release Gate Note

Before tagging v1.23.0, the release gate is a clean `python -m pytest`, a clean `python scripts/selfcheck.py`, a clean `git diff --check`, and explicit wheel-installed empty-cwd coverage via `python -m pytest tests/test_packaging.py -m wheel_smoke`; the expected result is that version metadata reports `1.23.0`, bundled static resources are included in the wheel, `market-signal-lab --prediction-readiness-audit` runs from an empty current directory, generated/static gallery links remain local, and public copy preserves the research-only/no-live-data/no-broker/no-account/no-order/no-position-sizing/no-forecast/no-recommendation/no-trading-instruction/no-investment-advice boundaries.
