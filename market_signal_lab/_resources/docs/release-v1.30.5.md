# v1.30.5 Release Notes

Market Signal Lab v1.30.5 packages the Visual Acceptance Bundle increment for bounded public visual review.

## Start Here

- [Visual Acceptance Bundle](../reports/visual-acceptance-bundle.md) - bounded visual acceptance handoff tying the static walkthrough, gallery, visual receipt, acceptance receipt index, reviewer acceptance scorecard, cold-user route, artifact hashes, and no-live-data/no-advice boundaries together.
- [Visual Acceptance Bundle JSON](../reports/visual-acceptance-bundle.json) - structured version of the same bundle, including acceptance checks, boundary flags, rerun commands, and artifact hashes.
- [Visual Walkthrough Evidence Receipt](../reports/visual-walkthrough-evidence-receipt.md) - deterministic cold-review route behind the visual acceptance bundle.
- [Reviewer Acceptance Scorecard](../reports/reviewer-acceptance-scorecard.md) - public-review readiness scorecard referenced by the bundle.

## Changed

- Added `--visual-acceptance-bundle` as a deterministic stdlib-only CLI artifact mode.
- Added generated Markdown and JSON visual acceptance bundle artifacts.
- Linked the bundle from the README, documentation map, root landing page, and static report gallery.
- Kept the bundle bounded to static visual/review evidence and artifact integrity; it does not create a trading-readiness claim.

## Verification

```bash
python -m market_signal_lab.cli --visual-acceptance-bundle
python -m pytest tests/test_visual_acceptance_bundle.py tests/test_cli.py tests/test_packaging.py
python scripts/selfcheck.py
```

## Boundaries

The Visual Acceptance Bundle is a static research-review artifact only. It does not provide live data, broker/account access, order routing, position sizing, forecasts, recommendations, trading signals, suitability review, or investment advice. PASS labels describe review-route presence and boundary visibility only; hashes confirm local file bytes at generation time only.
