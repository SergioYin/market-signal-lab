# Acceptance Receipt Index

Give public reviewers one bounded deterministic index linking the existing public demo evidence receipt, reviewer rerun receipt, reviewer evidence bundle, artifact hashes, fixture provenance, and no-live-data/no-advice boundaries.

## Indexed Receipts

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
- Present artifacts: `10` of `10`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| reports/public-demo-evidence-receipt.md | present | 5747 | b37ac21451061959e768bf1fd9fd8dea4dbda6327e53d746cba8e592a8130887 |
| reports/public-demo-evidence-receipt.json | present | 6879 | 9661076efc817ab226aad8e7d792e5dd655358683eb126deabc63ea141c78c6d |
| reports/reviewer-rerun-receipt.md | present | 5242 | 4be8a9a754436b90a5e48988d66220869b4ec2abaf91dd8ba76a5c054b24f0ae |
| reports/reviewer-rerun-receipt.json | present | 5179 | 021bd65958f2fa6b5660fb9c705ddc0e0ee7c01277660f699e6eaf317dd937a2 |
| reports/reviewer-evidence-bundle.md | present | 3350 | 5e9355d045da47a09b84593ef8d52a4dd63d63ac0d48c67e9cdd147c094d20c5 |
| reports/reviewer-evidence-bundle.json | present | 4025 | 2ad2cda05539b2c6b41e7553cf1f9c3e518f3979f1069c7ea1af55d336f9df86 |
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
