# Cold-User Review Route

Use this deterministic route to review checked-in Market Signal Lab artifacts from a public, first-time-reader perspective. It is limited to static historical diagnostics with no live data, no broker/account access, no orders, no forecasts, no recommendations, no position sizing, and no investment advice.

## Route

1. **Open the checked-in artifact gallery**
   - Path: `reports/index.html`
   - Review question: Can a first-time reviewer find the sample artifacts without running setup?
   - Expected public signal: The first screen is a local static artifact, not a live service.
2. **Read the sample Markdown report**
   - Path: `reports/sample-report.md`
   - Review question: Are metrics framed as historical diagnostics rather than forecasts?
   - Expected public signal: The report describes a fixed historical sample and its assumptions.
3. **Check the beginner reading boundary**
   - Path: `reports/beginner-prediction-checklist.md`
   - Review question: Does the checklist keep predictions, recommendations, and advice out of scope?
   - Expected public signal: A non-expert reader gets plain scope limits before citing or sharing the artifact.
4. **Review the public evidence handoff**
   - Path: `reports/reviewer-evidence-bundle.md`
   - Review question: Does the handoff identify static files and deterministic verification commands?
   - Expected public signal: The route can be checked from local files without private context.
5. **Inspect methodology and risk caveats**
   - Path: `docs/methodology-audit.md`
   - Review question: Are look-ahead, fees, overfitting, and leveraged ETF risks visible?
   - Expected public signal: Known research limitations are documented next to the artifacts.

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
- Present artifacts: `5` of `5`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| reports/index.html | present | 7679 | 208bc2c8559ae749f90ce8c08b0e39eea4da4c213e7ec7af1726520d42584c69 |
| reports/sample-report.md | present | 3543 | 20ba4fb3f9b1bc739f2e4ccf039e478ac41ddf570a199b6e075b783b54a48ebc |
| reports/beginner-prediction-checklist.md | present | 3850 | 0fd3cdc924160aebd4a9b0ffca4542d95726125200104e7f06d1f5378834b3b0 |
| reports/reviewer-evidence-bundle.md | present | 2925 | 95c996bdca95b10cd2becea77be6adc43af83449e2d778bd6ac6124c8ca0ecbc |
| docs/methodology-audit.md | present | 4970 | 8913048eb92849915d844090f56d908e744aa84c9d0248c37adade3e13189e3a |

## Do Not Use This For

- prediction of future returns
- investment advice
- trading recommendation
- live execution or signal use
- broker, account, or order workflow
- position sizing

## Verification Commands

- `python -m market_signal_lab.cli --cold-user-review-route`
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
