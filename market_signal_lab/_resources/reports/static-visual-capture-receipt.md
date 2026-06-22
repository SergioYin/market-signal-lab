# Static Visual Capture Receipt

Scan the existing static visual, gallery, walkthrough, route, and checklist artifacts that support a public-safe local visual capture handoff, recording relative paths, presence, byte counts, SHA-256 hashes, roles, routes, known regeneration commands, and public evidence notes.

## Scope

- Scan surface: checked-in static visual/gallery/walkthrough/checklist artifacts only
- Source policy: repo-relative public artifacts; no private paths, secrets, live data, or external services
- Capture asset policy: optional reviewer-created screenshots or GIFs are not generated or hashed by this receipt; no live data is captured
- Verification command: `python -m market_signal_lab.cli --static-visual-capture-receipt`

## Scanned Artifacts

| Path | Status | Bytes | SHA-256 | Role | Route | Regeneration command | Public evidence note |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| reports/index.html | present | 13121 | 370cc9c2ca7b865f2c4332cc880163858afb4dac3a60acce852bc613f33b9c25 | static_gallery_first_screen | open local static gallery before inspecting review artifacts | `python scripts/selfcheck.py` | Browser-openable static gallery with no JavaScript, external assets, live data, broker/account workflow, orders, forecasts, recommendations, or advice. |
| docs/static-gallery-walkthrough.svg | present | 5721 | 5ecbd181bd380ee4afba13f866615b942e79b6700d891549cee361a9557bed63 | visual_walkthrough_map | start with walkthrough, then open reports/index.html | `python scripts/selfcheck.py` | Static SVG route map for public orientation only; it is not a live signal surface or execution workflow. |
| reports/visual-acceptance-bundle.md | present | 5503 | 3dfbe1b0f1d6e3c55094b14170e32d9e4b8c67d1a931e2be28cc290b9f6ecb6d | visual_acceptance_handoff | gallery -> visual bundle -> linked receipts | `python -m market_signal_lab.cli --visual-acceptance-bundle` | Markdown handoff tying static visual artifacts, hashes, reviewer checks, and no-live-data/no-advice boundaries together. |
| reports/visual-acceptance-bundle.json | present | 6280 | d734d2d3ffe5230082793fc3c24a05f901d13e145d4ff7a3351ece078ac47911 | visual_acceptance_handoff_json | machine-readable pair for reports/visual-acceptance-bundle.md | `python -m market_signal_lab.cli --visual-acceptance-bundle` | Structured visual acceptance evidence for deterministic review. |
| reports/visual-walkthrough-evidence-receipt.md | present | 3854 | 5b2180f4ca63b592fce85dea6ba8673a25d84e0dfa1aa175f18f18260105d530 | walkthrough_route_receipt | walkthrough SVG -> gallery -> demo receipt -> rerun receipt -> acceptance index | `python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt` | Receipt for the static visual walkthrough route and linked public review evidence. |
| reports/visual-walkthrough-evidence-receipt.json | present | 4393 | 7af91623b705aed3aba758fc8eacadd7be018a232937ae9124ef346f36fdbd8f | walkthrough_route_receipt_json | machine-readable pair for reports/visual-walkthrough-evidence-receipt.md | `python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt` | Structured receipt for deterministic walkthrough-route review. |
| reports/static-visual-capture-checklist.md | present | 6002 | 86ec8ce1e7eb9d561951c157695fa19ab0c5828320e3943d522c31811f59f894 | capture_safety_checklist | read before creating any local screenshot or GIF | `python -m market_signal_lab.cli --static-visual-capture-checklist` | Checklist for keeping optional reviewer-created captures public safe and bounded to static local artifacts. |
| reports/static-visual-capture-checklist.json | present | 6415 | 70cd97edef19e6ca869d00c60c90e6f4b9abe71c6e80ac39b9f3af177f100882 | capture_safety_checklist_json | machine-readable pair for reports/static-visual-capture-checklist.md | `python -m market_signal_lab.cli --static-visual-capture-checklist` | Structured checklist with source hashes and do-not-capture rules. |
| reports/cold-user-review-route.md | present | 6628 | 90410a2f88d75afacb3d3291c969379cbdb1a44e93680960669ae048e23b20f5 | cold_reviewer_route | first-time public reviewer orientation path | `python -m market_signal_lab.cli --cold-user-review-route` | Static orientation route only; it does not approve financial correctness, execution readiness, forecasts, recommendations, or advice. |
| reports/cold-user-review-route.json | present | 7601 | 879fb92d5ac08720184fedb84b480cce86218928dcf73a3adc6d57b50adae3ce | cold_reviewer_route_json | machine-readable pair for reports/cold-user-review-route.md | `python -m market_signal_lab.cli --cold-user-review-route` | Structured cold-review route evidence. |
| reports/public-demo-evidence-receipt.md | present | 6312 | b57b1f3e862e8f525fbc510c00426d34f1a5b897bc83b0539b18da42974cd7c0 | public_demo_receipt | gallery and fixture-boundary evidence receipt | `python -m market_signal_lab.cli --public-demo-evidence-receipt` | Public receipt for static sample artifacts, fixture boundaries, hashes, and non-advice claims. |
| reports/public-demo-evidence-receipt.json | present | 7497 | a2d34d24316645c290cb5c95347d6748d211aa201c7e5200f800d18e1a75814e | public_demo_receipt_json | machine-readable pair for reports/public-demo-evidence-receipt.md | `python -m market_signal_lab.cli --public-demo-evidence-receipt` | Structured public demo evidence receipt. |
| docs/static-gallery-manifest.md | present | 15402 | e726465cb12fad9fd1150b13d8bb36d9163604e9720cb06d82be25ed96e576cd | static_gallery_manifest_doc | documentation map for the static gallery link contract | `python scripts/selfcheck.py` | Documentation for the static gallery contract using repo-relative paths only. |

## Artifact Integrity Summary

- Integrity status: `PASS`
- Interpretation: PASS: All expected static reviewer artifacts were present and hashed at generation time.
- Caveat: This is artifact-integrity evidence only; it confirms local file bytes at generation time and does not validate financial correctness, future performance, recommendations, or investment suitability.
- Algorithm: `sha256`
- Scope: local static reviewer evidence artifacts only; hashes are artifact-integrity provenance at generation time, not financial validation
- Present artifacts: `13` of `13`

## Public Evidence Notes

- All paths are repo-relative and intended for public static review.
- SHA-256 values identify local file bytes at generation time only.
- The receipt records existing static artifacts; it does not create screenshots or GIFs.
- Optional captures must follow the static visual capture checklist before sharing.

## Not Claimed

- No live market data, broker, account, order, portfolio, holdings, or position-sizing surface is scanned.
- No forecast, recommendation, buy/sell/hold advice, suitability review, or investment advice is provided.
- Hashes do not validate financial correctness, future performance, robustness, profitability, or trading readiness.
- The receipt does not inspect private files, private paths, browser profiles, terminals, editors, notifications, or secrets.

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
