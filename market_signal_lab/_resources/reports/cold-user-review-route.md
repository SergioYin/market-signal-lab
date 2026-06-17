# Cold-User Review Route

Use this deterministic route to review checked-in Market Signal Lab artifacts from a public, first-time-reader perspective. It is limited to static historical diagnostics with no live data, no broker/account access, no orders, no forecasts, no recommendations, no position sizing, and no investment advice.

## Route

1. **Open the static gallery visual walkthrough**
   - Path: `docs/static-gallery-walkthrough.svg`
   - Review question: Can a first-time reviewer see the static gallery path before opening reports?
   - Expected public signal: The visual walkthrough is a checked-in static SVG, not a live product flow.
2. **Open the checked-in artifact gallery**
   - Path: `reports/index.html`
   - Review question: Can a first-time reviewer find the sample artifacts without running setup?
   - Expected public signal: The first screen is a local static artifact, not a live service.
3. **Review the visual walkthrough evidence receipt**
   - Path: `reports/visual-walkthrough-evidence-receipt.md`
   - Review question: Does one receipt tie the walkthrough SVG, gallery, public demo receipt, rerun receipt, and acceptance index together?
   - Expected public signal: The receipt records repo-relative links, hashes, and no-live-data/no-advice boundaries.
4. **Review the public demo evidence receipt**
   - Path: `reports/public-demo-evidence-receipt.md`
   - Review question: Are gallery artifacts and fixture boundaries tied to hashes?
   - Expected public signal: The receipt links checked-in public artifacts without private context or live data.
5. **Check the beginner reading boundary**
   - Path: `reports/beginner-prediction-checklist.md`
   - Review question: Does the checklist keep predictions, recommendations, and advice out of scope?
   - Expected public signal: A non-expert reader gets plain scope limits before citing or sharing the artifact.
6. **Review the public evidence handoff**
   - Path: `reports/reviewer-evidence-bundle.md`
   - Review question: Does the handoff identify static files and deterministic verification commands?
   - Expected public signal: The route can be checked from local files without private context.
7. **Review the public rerun receipt**
   - Path: `reports/reviewer-rerun-receipt.md`
   - Review question: Can a reviewer see the exact public rerun commands and expected artifacts?
   - Expected public signal: The receipt lists deterministic commands, PASS/WARN checks, and no-live-data/no-advice boundaries.
8. **Review the acceptance receipt index**
   - Path: `reports/acceptance-receipt-index.md`
   - Review question: Does the index connect public receipts, fixture provenance, hashes, and boundaries?
   - Expected public signal: The acceptance index gives one bounded map of public receipt evidence without approving trading use.
9. **Inspect methodology and risk caveats**
   - Path: `docs/methodology-audit.md`
   - Review question: Are look-ahead, fees, overfitting, and leveraged ETF risks visible?
   - Expected public signal: Known research limitations are documented next to the artifacts.
10. **Finish with the reviewer acceptance scorecard**
   - Path: `reports/reviewer-acceptance-scorecard.md`
   - Review question: Does the final handoff summarize public-review readiness and remaining WARN items?
   - Expected public signal: The scorecard closes the research-only handoff without approving trading use.

## Checklist

- **Static first screen is available** (`PASS`): Start from reports/index.html and checked-in files only.
- **Route uses repo-relative public paths** (`PASS`): Paths are stable repo artifacts and exclude machine-specific locations.
- **Non-advice boundary is explicit** (`PASS`): Artifacts are historical research diagnostics, not recommendations or forecasts.
- **Deterministic verification commands are listed** (`PASS`): Commands regenerate static review artifacts without live data or broker access.
- **Artifact byte hashes are recorded** (`PASS`): Hashes identify local bytes at generation time, not financial correctness.

## Artifact Hash Summary

- Integrity status: `PASS`
- Algorithm: `sha256`
- Scope: repo-relative checked-in static artifacts only; hashes confirm local file bytes at generation time, not financial correctness
- Present artifacts: `10` of `10`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| docs/static-gallery-walkthrough.svg | present | 5721 | 5ecbd181bd380ee4afba13f866615b942e79b6700d891549cee361a9557bed63 |
| reports/index.html | present | 11190 | e547d42cd450cc0969778394e3f487df9758ea5edf57c70b9090bf228d8a2147 |
| reports/visual-walkthrough-evidence-receipt.md | present | 3854 | 0b212cd4ca48edf2335d2dcccac4b91ef08937f8c05271c6873c896dedc9a91b |
| reports/public-demo-evidence-receipt.md | present | 6312 | 89f708319e13bbd9e7209b6129aa58b6880046979ba11a1d76c875e328030845 |
| reports/beginner-prediction-checklist.md | present | 3850 | 0fd3cdc924160aebd4a9b0ffca4542d95726125200104e7f06d1f5378834b3b0 |
| reports/reviewer-evidence-bundle.md | present | 3349 | 8fd3fe3250d616c6fabe9fba17ccfeb2d0e413368482cc3cb603c433f53f6539 |
| reports/reviewer-rerun-receipt.md | present | 5868 | 3b1135d1ed5441e5ad35cbbdb1eec11aa9424aeb8a552d1eeaeb14d5c93310c5 |
| reports/acceptance-receipt-index.md | present | 5487 | a681b476c1801dba20181ac8a8be6c01012ea3532ec1b22f49827827a7a07884 |
| docs/methodology-audit.md | present | 4970 | 8913048eb92849915d844090f56d908e744aa84c9d0248c37adade3e13189e3a |
| reports/reviewer-acceptance-scorecard.md | present | 5717 | 9ecd43909f25cd05c68c3b6fcf66918105184d05abb912171e7547e597ebc9db |

## Do Not Use This For

- prediction of future returns
- investment advice
- trading recommendation
- live execution or signal use
- broker, account, or order workflow
- position sizing

## Verification Commands

- `python -m market_signal_lab.cli --cold-user-review-route`
- `python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt`
- `python -m market_signal_lab.cli --public-demo-evidence-receipt`
- `python -m market_signal_lab.cli --reviewer-rerun-receipt`
- `python -m market_signal_lab.cli --acceptance-receipt-index`
- `python -m market_signal_lab.cli --reviewer-acceptance-scorecard`
- `python -m market_signal_lab.cli --reviewer-evidence-bundle`
- `python -m market_signal_lab.cli --beginner-prediction-checklist`
- `python scripts/selfcheck.py`
- `python -m pytest`

## Boundary Flags

- research_only: `True`
- static_only: `True`
- historical_diagnostics_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
