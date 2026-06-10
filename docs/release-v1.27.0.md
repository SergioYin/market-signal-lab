# v1.27.0 Release Notes

Market Signal Lab v1.27.0 adds a reviewer acceptance scorecard for public, research-only review of checked-in static backtest artifacts. The scorecard is an acceptance handoff for artifact shape, reproducibility evidence, and boundary visibility only; it is not a trading-readiness approval, forecast, recommendation, suitability review, or investment advice.

## Added

- Added [Reviewer acceptance scorecard Markdown](../reports/reviewer-acceptance-scorecard.md) with PASS/WARN review categories for public-review readiness, reproducibility evidence, risk boundaries, and next actions.
- Added [Reviewer acceptance scorecard JSON](../reports/reviewer-acceptance-scorecard.json) with deterministic boundary flags, acceptance metadata, limitations, evidence paths, and verification commands.
- Added the CLI route:

```bash
python -m market_signal_lab.cli --reviewer-acceptance-scorecard
```

## Updated

- Linked the scorecard from the README, documentation map, static gallery, packaged resources, selfcheck generator, and cold-user review route.
- Added tests for scorecard payload shape, evidence paths, CLI conflict handling, empty-cwd output generation, and installed console-script smoke coverage.

## Verification

Regenerate and inspect the scorecard:

```bash
python -m market_signal_lab.cli --reviewer-acceptance-scorecard
git diff -- reports/reviewer-acceptance-scorecard.md reports/reviewer-acceptance-scorecard.json
```

Run the local release hygiene gates:

```bash
python -m pytest -q
python scripts/selfcheck.py
python -m compileall market_signal_lab tests scripts
git diff --check
```

## Research-Only Boundary

The scorecard does not prove profitability, future robustness, financial correctness, regulatory completeness, investment suitability, or strategy quality. All linked artifacts are static historical diagnostics and examples; they do not use live market data, broker/account access, orders, position sizing, forecasts, recommendations, or investment advice.
