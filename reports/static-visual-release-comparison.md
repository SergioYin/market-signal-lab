# Static Visual Release Comparison

Compare the v1.30.7 static visual capture receipt baseline with the current working-tree static visual capture receipt scan, so public reviewers can see whether expected static visual receipt paths, roles, presence, hashes, and review boundaries carried forward without opening live data, broker, account, order, forecast, recommendation, or advice surfaces.

## Scope

- Previous release: v1.30.7 static visual capture receipt baseline
- Current release: working-tree static visual capture receipt candidate
- Comparison surface: existing static visual capture receipt artifacts and their current repo-relative scanned artifact inventory
- Baseline policy: baseline paths and roles are embedded from the v1.30.7 static visual capture receipt contract; current status and hashes come from the local static artifact scan
- Verification command: `python -m market_signal_lab.cli --static-visual-release-comparison`
- Source receipt rerun: `python -m market_signal_lab.cli --static-visual-capture-receipt`

## Source Receipt Artifacts

| Path | Role | Required |
| --- | --- | --- |
| reports/static-visual-capture-receipt.md | human-readable static visual capture receipt | True |
| reports/static-visual-capture-receipt.json | machine-readable static visual capture receipt | True |
| reports/static-visual-capture-checklist.md | public-safe reviewer capture checklist | True |
| reports/static-visual-capture-checklist.json | machine-readable reviewer capture checklist | True |

## Release Comparison

| Path | Previous status | Current status | Comparison | Current SHA-256 | Review note |
| --- | --- | --- | --- | --- | --- |
| reports/index.html | present | present | PASS | bab7472e9323057fbfe86025ba815ae42f81f084b6812225d60be6ee1d79f899 | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| docs/static-gallery-walkthrough.svg | present | present | PASS | 5ecbd181bd380ee4afba13f866615b942e79b6700d891549cee361a9557bed63 | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/visual-acceptance-bundle.md | present | present | PASS | ae9cf65336630fec387407cfc0c7ee9c7c4db346daac0262cd7214beb9f6ea55 | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/visual-acceptance-bundle.json | present | present | PASS | 9fded9965e05dad9bb6f729449dd002ebd2d3c87f88125f4e1921702ff91e894 | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/visual-walkthrough-evidence-receipt.md | present | present | PASS | 23a6d6deff7eb5f9c2f574cc4362faa94a24ed89d6987b83098f5a20368cc3da | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/visual-walkthrough-evidence-receipt.json | present | present | PASS | 9449b3391d52ff5e0e93fbc5aaa15db91db30f5d1dd8e916d87a84b1292efe5a | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/static-visual-capture-checklist.md | present | present | PASS | d031a77edaccfab26b31022e03f0cdbd284074b8a73e60c67dcaeed3a9d177d1 | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/static-visual-capture-checklist.json | present | present | PASS | 0771d53423301119f0af80e775aac854e998a1b3d9cd3eafe1cac1fbed08ad16 | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/cold-user-review-route.md | present | present | PASS | 90410a2f88d75afacb3d3291c969379cbdb1a44e93680960669ae048e23b20f5 | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/cold-user-review-route.json | present | present | PASS | 879fb92d5ac08720184fedb84b480cce86218928dcf73a3adc6d57b50adae3ce | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/public-demo-evidence-receipt.md | present | present | PASS | 7d258792141757308fa4eda543dd91870e35b76eac9693e58bd892e6dbd70160 | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| reports/public-demo-evidence-receipt.json | present | present | PASS | 88413ca885f79c848885f1578d8c6ece2c383031457796bbff56ab5c5aeb1a5f | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |
| docs/static-gallery-manifest.md | present | present | PASS | fdfbedd418633bf5b0639e18801b221aff133f69ffcc16ddd4371867e3f2821c | Expected path and role carried forward; current SHA-256 records local file bytes at comparison generation time only. |

## Reviewer Checklist

- **Source receipt artifacts are listed for review**: `PASS`
  - Check: `receipt_source_artifacts_present`
  - Review note: The comparison lists the existing Markdown/JSON static visual capture receipt and checklist as source receipt artifacts.
- **Compared artifact set matches the previous release baseline**: `PASS`
  - Check: `artifact_set_matches_baseline`
  - Review note: The comparison rows keep the v1.30.7 static visual capture receipt path order so release reviewers can spot additions or removals deterministically.
- **Current static visual receipt artifacts are present**: `PASS`
  - Check: `current_artifacts_present`
  - Review note: All compared paths should be present before sharing the release comparison as public static review evidence.
- **Artifact roles carried forward**: `PASS`
  - Check: `roles_carried_forward`
  - Review note: Role changes are allowed only after a reviewer confirms the visual handoff wording still describes static review evidence.
- **Research-only and no-advice boundaries are preserved**: `PASS`
  - Check: `boundaries_preserved`
  - Review note: Boundary flags must remain true: no live data, broker/account workflow, orders, position sizing, forecasts, recommendations, private data, or investment advice.
- **Hash interpretation remains limited**: `PASS`
  - Check: `hashes_are_limited`
  - Review note: SHA-256 values are file-byte receipts only; they do not prove financial correctness, performance, suitability, or trading readiness.

## Source Receipt Integrity

- Integrity status: `PASS`
- Interpretation: PASS: All expected static reviewer artifacts were present and hashed at generation time.
- Caveat: This is artifact-integrity evidence only; it confirms local file bytes at generation time and does not validate financial correctness, future performance, recommendations, or investment suitability.
- Algorithm: `sha256`
- Scope: local static reviewer evidence artifacts only; hashes are artifact-integrity provenance at generation time, not financial validation
- Present artifacts: `4` of `4`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| reports/static-visual-capture-receipt.md | present | 7357 | 48222338ae75a3340c63693ad5e3a18ee0ae611993a8b1b1e08db957dc08938e |
| reports/static-visual-capture-receipt.json | present | 10796 | a219c104f0d5901f47356e8dbaf4e5b7b16bcd740ebd159f1709e3b0de3d7962 |
| reports/static-visual-capture-checklist.md | present | 6002 | d031a77edaccfab26b31022e03f0cdbd284074b8a73e60c67dcaeed3a9d177d1 |
| reports/static-visual-capture-checklist.json | present | 6415 | 0771d53423301119f0af80e775aac854e998a1b3d9cd3eafe1cac1fbed08ad16 |

## Current Receipt Artifact Summary

- Integrity status: `PASS`
- Interpretation: PASS: All expected static reviewer artifacts were present and hashed at generation time.
- Caveat: This is artifact-integrity evidence only; it confirms local file bytes at generation time and does not validate financial correctness, future performance, recommendations, or investment suitability.
- Algorithm: `sha256`
- Scope: local static reviewer evidence artifacts only; hashes are artifact-integrity provenance at generation time, not financial validation
- Present artifacts: `13` of `13`

## Not Claimed

- This comparison is a static review checklist, not release approval or financial validation.
- It compares expected receipt inventory shape and current local file-byte hashes only.
- It does not fetch tags, releases, live market data, broker data, account data, or external services.
- PASS labels do not validate financial correctness, future performance, suitability, profitability, trading readiness, recommendations, or investment advice.
- Optional screenshots or GIFs remain reviewer-created artifacts and are not generated, captured, or validated by this command.

## Boundary Flags

- research_only: `True`
- static_only: `True`
- public_safe: `True`
- fixture_or_static_data_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`
- no_private_data: `True`
