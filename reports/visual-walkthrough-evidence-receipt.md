# Visual Walkthrough Evidence Receipt

Give cold public reviewers one deterministic receipt tying the static gallery walkthrough SVG, public gallery, public demo evidence receipt, reviewer rerun receipt, and acceptance receipt index into a review-only route.

## Reviewer Steps

1. Open docs/static-gallery-walkthrough.svg to see the intended static gallery path.
2. Open reports/index.html from local checked-in files, not from a live app or broker workflow.
3. Compare reports/public-demo-evidence-receipt.md with its JSON output for artifact hashes and source boundaries.
4. Read reports/reviewer-rerun-receipt.md for deterministic commands and expected artifacts.
5. Finish with reports/acceptance-receipt-index.md before treating any artifact as public-review evidence.

## Walkthrough Links

- **Static gallery walkthrough**
  - Path: `docs/static-gallery-walkthrough.svg`
  - Role: Visual entry point showing the static gallery path a cold reviewer can inspect before running commands.
- **Static sample gallery**
  - Path: `reports/index.html`
  - Role: Browser-openable public first screen with no JavaScript, external assets, live data, broker workflow, orders, forecasts, or advice.
- **Public demo evidence receipt**
  - Path: `reports/public-demo-evidence-receipt.md`
  - Role: Receipt for gallery/backtest artifacts, fixture boundaries, hashes, and no-live-data/no-advice claims.
- **Reviewer rerun receipt**
  - Path: `reports/reviewer-rerun-receipt.md`
  - Role: Receipt for deterministic public rerun commands and expected review artifacts.
- **Acceptance receipt index**
  - Path: `reports/acceptance-receipt-index.md`
  - Role: Index tying public receipts, fixture provenance, artifact hashes, and non-advice boundaries together.

## Artifact Integrity Summary

- Integrity status: `PASS`
- Interpretation: PASS: All expected static reviewer artifacts were present and hashed at generation time.
- Caveat: This is artifact-integrity evidence only; it confirms local file bytes at generation time and does not validate financial correctness, future performance, recommendations, or investment suitability.
- Algorithm: `sha256`
- Scope: local static reviewer evidence artifacts only; hashes are artifact-integrity provenance at generation time, not financial validation
- Present artifacts: `6` of `6`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| docs/static-gallery-walkthrough.svg | present | 5721 | 5ecbd181bd380ee4afba13f866615b942e79b6700d891549cee361a9557bed63 |
| reports/index.html | present | 13766 | bab7472e9323057fbfe86025ba815ae42f81f084b6812225d60be6ee1d79f899 |
| reports/public-demo-evidence-receipt.md | present | 6312 | 7d258792141757308fa4eda543dd91870e35b76eac9693e58bd892e6dbd70160 |
| reports/public-demo-evidence-receipt.json | present | 7497 | 88413ca885f79c848885f1578d8c6ece2c383031457796bbff56ab5c5aeb1a5f |
| reports/reviewer-rerun-receipt.md | present | 5868 | 3b1135d1ed5441e5ad35cbbdb1eec11aa9424aeb8a552d1eeaeb14d5c93310c5 |
| reports/reviewer-rerun-receipt.json | present | 5866 | b9832c88346f88f2ca73ac7b41fb314c54d93baaa09e5f0643d4a775922326e6 |

## Not Claimed

- The SVG is visual navigation evidence only; it does not prove financial correctness.
- This receipt does not execute commands or fetch live market data.
- The acceptance receipt index is linked as a route step, but not hashed here because it indexes this receipt.
- No broker, account, order-routing, position-sizing, forecast, recommendation, or advice workflow is included.
- SHA-256 hashes identify local file bytes at generation time only.

## Boundary Flags

- research_only: `True`
- static_only: `True`
- fixture_or_static_data_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`
