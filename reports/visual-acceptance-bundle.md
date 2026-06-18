# Visual Acceptance Bundle

Give public reviewers one bounded deterministic bundle tying the static visual walkthrough, gallery first screen, visual receipt, acceptance receipt index, reviewer acceptance scorecard, cold-user route, artifact hashes, and no-live-data/no-advice boundaries together.

## Acceptance Surfaces

- **Visual walkthrough**
  - Path: `docs/static-gallery-walkthrough.svg`
  - Role: Shows the public-safe static gallery route before a reviewer opens reports or runs commands.
- **Static sample gallery**
  - Path: `reports/index.html`
  - Role: Browser-openable first screen for checked-in artifacts; no live data, external assets, broker workflow, forecasts, or advice.
- **Visual walkthrough evidence receipt**
  - Path: `reports/visual-walkthrough-evidence-receipt.md`
  - Role: Records the visual route, route artifact hashes, and explicit visual-navigation non-claims.
- **Acceptance receipt index**
  - Path: `reports/acceptance-receipt-index.md`
  - Role: Indexes public receipts, fixture provenance, artifact hashes, and no-live-data/no-advice boundaries.
- **Reviewer acceptance scorecard**
  - Path: `reports/reviewer-acceptance-scorecard.md`
  - Role: Summarizes public-review readiness, reproducibility evidence, risk boundaries, WARN items, and next actions.
- **Cold-user review route**
  - Path: `reports/cold-user-review-route.md`
  - Role: Gives first-time public reviewers a deterministic route through the static review artifacts.

## Acceptance Checks

- **Static visual entry is present**: `PASS`
  - Check: `static_visual_entry`
  - Review note: The bundle starts from checked-in SVG/HTML files rather than a live application, account, or broker route.
- **Receipt boundaries are linked**: `PASS`
  - Check: `bounded_receipts`
  - Review note: The visual receipt, acceptance index, public demo receipt, and scorecard state what they do and do not prove.
- **Artifact hashes are recorded**: `PASS`
  - Check: `artifact_hashes`
  - Review note: SHA-256 hashes identify local file bytes at generation time only, not financial correctness or trading readiness.
- **Review-only boundary is explicit**: `PASS`
  - Check: `review_only_boundary`
  - Review note: The bundle excludes live data, broker/account access, orders, position sizing, forecasts, recommendations, and investment advice.

## Reviewer Rerun Commands

- `python -m market_signal_lab.cli --visual-acceptance-bundle`
- `python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt`
- `python -m market_signal_lab.cli --acceptance-receipt-index`
- `python -m market_signal_lab.cli --reviewer-acceptance-scorecard`
- `python -m market_signal_lab.cli --cold-user-review-route`
- `python scripts/selfcheck.py`

## Artifact Integrity Summary

- Integrity status: `PASS`
- Interpretation: PASS: All expected static reviewer artifacts were present and hashed at generation time.
- Caveat: This is artifact-integrity evidence only; it confirms local file bytes at generation time and does not validate financial correctness, future performance, recommendations, or investment suitability.
- Algorithm: `sha256`
- Scope: local static reviewer evidence artifacts only; hashes are artifact-integrity provenance at generation time, not financial validation
- Present artifacts: `12` of `12`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| docs/static-gallery-walkthrough.svg | present | 5721 | 5ecbd181bd380ee4afba13f866615b942e79b6700d891549cee361a9557bed63 |
| reports/index.html | present | 11855 | f16a40b51a361613816dfbebb7d290e162c0dc0fea7112248451b5151b887d31 |
| reports/visual-walkthrough-evidence-receipt.md | present | 3854 | 9cc7c81ceb49f130915ae02970dbaa7476f5ca33b8c63d54eb655a408b9441f3 |
| reports/acceptance-receipt-index.md | present | 5487 | b36712492ddc5b0fe7fa0eeb591e380b330a63e146b5a015122ab57dcccb2216 |
| reports/reviewer-acceptance-scorecard.md | present | 5717 | 9ecd43909f25cd05c68c3b6fcf66918105184d05abb912171e7547e597ebc9db |
| reports/cold-user-review-route.md | present | 6628 | 90410a2f88d75afacb3d3291c969379cbdb1a44e93680960669ae048e23b20f5 |
| reports/visual-walkthrough-evidence-receipt.json | present | 4393 | ae8c06a1e4c2184f8c0a46050cea14e4bb9d749b163856c881102fa8ad6b6cd1 |
| reports/acceptance-receipt-index.json | present | 6319 | f1524d9546c015d5c725e131d2e48971df8877ddb49748a5ee37eee4d4c9660f |
| reports/reviewer-acceptance-scorecard.json | present | 6667 | 779e78d4dace3460976af5e8a66f38c93f22daecf334f4f8f9aceb10d33e8828 |
| reports/cold-user-review-route.json | present | 7601 | 879fb92d5ac08720184fedb84b480cce86218928dcf73a3adc6d57b50adae3ce |
| reports/public-demo-evidence-receipt.md | present | 6312 | 9f857d64aa2d98943f68e518ba4ac35946007cd6bdf8434d206833fc95d2f0e7 |
| reports/public-demo-evidence-receipt.json | present | 7497 | 20df1a742a834fa3b770e28cdc3c8f2fb8350aeac68aefbbf1a9d61e7f5befb7 |

## Not Claimed

- The bundle is a static visual acceptance handoff, not financial validation.
- PASS labels describe review-route presence and boundary visibility only.
- Hashes prove local file-byte identity at generation time only.
- No live data, broker, account, order-routing, position-sizing, forecast, recommendation, or advice workflow is included.

## Boundary Flags

- research_only: `True`
- static_only: `True`
- fixture_or_static_data_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`
