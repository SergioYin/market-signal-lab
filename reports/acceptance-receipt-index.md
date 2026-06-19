# Acceptance Receipt Index

Give public reviewers one bounded deterministic index linking the visual walkthrough evidence receipt, public demo evidence receipt, reviewer rerun receipt, reviewer evidence bundle, artifact hashes, fixture provenance, and no-live-data/no-advice boundaries.

## Indexed Receipts

- **Visual walkthrough evidence receipt**
  - Markdown: `reports/visual-walkthrough-evidence-receipt.md`
  - JSON: `reports/visual-walkthrough-evidence-receipt.json`
  - Rerun: `python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt`
  - Role: Ties the static gallery walkthrough SVG, gallery first screen, public demo receipt, rerun receipt, and acceptance index into one cold-review route.
- **Public demo evidence receipt**
  - Markdown: `reports/public-demo-evidence-receipt.md`
  - JSON: `reports/public-demo-evidence-receipt.json`
  - Rerun: `python -m market_signal_lab.cli --public-demo-evidence-receipt`
  - Role: Links public gallery/backtest evidence, fixture provenance paths, artifact hashes, and no-live-data/no-advice claims.
- **Reviewer rerun receipt**
  - Markdown: `reports/reviewer-rerun-receipt.md`
  - JSON: `reports/reviewer-rerun-receipt.json`
  - Rerun: `python -m market_signal_lab.cli --reviewer-rerun-receipt`
  - Role: Lists deterministic public rerun commands, expected artifacts, PASS/WARN checks, and no-live-data/no-advice boundaries.
- **Reviewer evidence bundle**
  - Markdown: `reports/reviewer-evidence-bundle.md`
  - JSON: `reports/reviewer-evidence-bundle.json`
  - Rerun: `python -m market_signal_lab.cli --reviewer-evidence-bundle`
  - Role: Ties the gallery, thesis-ledger acceptance route, methodology risks, verification commands, and artifact hash summary together.

## Fixture Provenance

- `examples/data/sample_tqqq_qld_like.csv` with `examples/data/sample_tqqq_qld_like.csv.provenance.json`: Synthetic static OHLC fixture used by single report, sweep, fee sensitivity, and cross-asset thesis-ledger demo artifacts.
- `examples/data/sample_multi_regime.csv` with `examples/data/sample_multi_regime.csv.provenance.json`: Synthetic static multi-regime fixture used by deterministic regime-comparison demo artifacts.

## Reviewer Rerun Commands

- `python -m market_signal_lab.cli --acceptance-receipt-index`
- `python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt`
- `python -m market_signal_lab.cli --public-demo-evidence-receipt`
- `python -m market_signal_lab.cli --reviewer-rerun-receipt`
- `python -m market_signal_lab.cli --reviewer-evidence-bundle`
- `python scripts/selfcheck.py`

## Artifact Hash Index

- Integrity status: `PASS`
- Interpretation: PASS: All expected static reviewer artifacts were present and hashed at generation time.
- Caveat: This is artifact-integrity evidence only; it confirms local file bytes at generation time and does not validate financial correctness, future performance, recommendations, or investment suitability.
- Algorithm: `sha256`
- Scope: local static reviewer evidence artifacts only; hashes are artifact-integrity provenance at generation time, not financial validation
- Present artifacts: `12` of `12`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| reports/visual-walkthrough-evidence-receipt.md | present | 3854 | 10188f9fb1234e6e39ddd518e6c1cbf04a0596a537b6b5a70610b78988568834 |
| reports/visual-walkthrough-evidence-receipt.json | present | 4393 | b0379111686ae2a0d754c9c1975b40b0021e5bd9b848bbdfd26018c844d15945 |
| reports/public-demo-evidence-receipt.md | present | 6312 | a33b449439d1e22387ec22f9a22e6fc71cd05e94229a50731abc29785f451586 |
| reports/public-demo-evidence-receipt.json | present | 7497 | ec15e663ea2ccda547cd1c813d7d03fca7b70038fcd88e6e394a60c6775570aa |
| reports/reviewer-rerun-receipt.md | present | 5868 | 3b1135d1ed5441e5ad35cbbdb1eec11aa9424aeb8a552d1eeaeb14d5c93310c5 |
| reports/reviewer-rerun-receipt.json | present | 5866 | b9832c88346f88f2ca73ac7b41fb314c54d93baaa09e5f0643d4a775922326e6 |
| reports/reviewer-evidence-bundle.md | present | 3350 | 960ff28f066ab949f3213ed3b9cd8f75dfdab6cb82e3bb83eb3b572543e683b5 |
| reports/reviewer-evidence-bundle.json | present | 4025 | f5a77206ecf4fb5957959063c0346b5263f657bd61d040cc6c6339c65242658e |
| examples/data/sample_tqqq_qld_like.csv | present | 1125 | 4ca9451f8a391a90530d8199375387bfa233282aa1845e5a64074142c62c1e90 |
| examples/data/sample_tqqq_qld_like.csv.provenance.json | present | 798 | c7bfe5cc08727e8ba19445c47103f380975be648cc6c74b595060649abd38a68 |
| examples/data/sample_multi_regime.csv | present | 1984 | 448940642e8eac3a97ca4af9a10aa7272fb68fd31e69b6628bef0ab7ff31a015 |
| examples/data/sample_multi_regime.csv.provenance.json | present | 2419 | df6c4da0c88250d340c378a076b3fbc35adf060ab6129851985d91e232844e32 |

## Not Claimed

- This index does not execute rerun commands; it records deterministic public artifact links.
- SHA-256 hashes prove local file-byte identity at generation time only.
- Hashes and PASS/WARN labels do not validate financial correctness, future performance, suitability, recommendations, or investment advice.
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
