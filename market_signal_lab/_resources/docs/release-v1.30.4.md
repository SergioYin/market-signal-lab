# v1.30.4 Release Notes

Market Signal Lab v1.30.4 packages the Visual Walkthrough Evidence Receipt increment for public-safe cold review.

## Start Here

- [Visual Walkthrough Evidence Receipt](../reports/visual-walkthrough-evidence-receipt.md) - deterministic cold-review route tying the static walkthrough SVG, gallery, public demo receipt, reviewer rerun receipt, and acceptance receipt index together.
- [Visual Walkthrough Evidence Receipt JSON](../reports/visual-walkthrough-evidence-receipt.json) - structured version of the same receipt, including boundary flags and artifact hashes.
- [Static Gallery Walkthrough](static-gallery-walkthrough.svg) - visual entry point for the local static gallery route.
- [Acceptance Receipt Index](../reports/acceptance-receipt-index.md) - bounded index linking public receipts, fixture provenance, hashes, and no-live-data/no-advice boundaries.

## Changed

- Added the generated Visual Walkthrough Evidence Receipt as a static reviewer handoff artifact.
- Linked the visual receipt from the README, documentation map, root landing page, static gallery, cold-user route, public demo receipt, reviewer rerun receipt, and acceptance receipt index.
- Packaged the static walkthrough SVG and visual receipt resources for installed CLI usage.
- Kept the receipt focused on visual navigation and artifact-integrity evidence, not financial correctness or trading readiness.

## Verification

```bash
python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt
python -m pytest tests/test_visual_walkthrough_evidence_receipt.py tests/test_cli.py tests/test_packaging.py
python scripts/selfcheck.py
```

## Boundaries

The Visual Walkthrough Evidence Receipt is a static research-review artifact only. It does not provide live data, broker/account access, order routing, position sizing, forecasts, recommendations, trading signals, suitability review, or investment advice. The artifact hashes confirm local file bytes at generation time only; they do not prove profitability, robustness, correctness, or public trading readiness.
