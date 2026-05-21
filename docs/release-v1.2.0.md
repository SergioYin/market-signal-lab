# v1.2.0 Release Checklist

## Scope

- Add a research-only fee sensitivity comparison artifact for the bundled single backtest.
- Keep the increment offline and stdlib-only.
- Avoid broker integrations, live data, execution features, forecasts, and recommendations.

## Verification

- `scripts/fee_sensitivity.py` generates `reports/fee-sensitivity.md`.
- `scripts/fee_sensitivity.py` generates `reports/fee-sensitivity.json`.
- Selfcheck includes the new artifacts in reproducibility and public-claim checks.
- README, documentation map, artifact gallery, and static report gallery link the new artifacts.
- Demo polish keeps the static gallery no-JavaScript and local-only, clarifies the review path, and documents leveraged ETF-like fixture limits.

## Release Notes

See [v1.2.0 Release Notes](release-notes-v1.2.0.md).
