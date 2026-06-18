# Public Demo Evidence Receipt

Give cold public reviewers one deterministic receipt for checking the static gallery/backtest report artifacts, source fixture boundaries, and no-advice/no-live-data claims.

## Reviewer Steps

1. Open docs/static-gallery-walkthrough.svg.
2. Open reports/visual-walkthrough-evidence-receipt.md and compare it with reports/visual-walkthrough-evidence-receipt.json.
3. Open reports/index.html.
4. Open reports/public-demo-evidence-receipt.md and compare it with reports/public-demo-evidence-receipt.json.
5. Check fixture provenance files next to examples/data/*.csv before reading reported metrics.
6. Use the SHA-256 table as file-byte evidence for checked-in public artifacts only.
7. Run python scripts/selfcheck.py for local regeneration and link/boundary checks.

## Generated Artifact Groups

- **Visual cold-review walkthrough**: Check the static SVG route and matching receipt before opening generated metrics.
  - Paths: `docs/static-gallery-walkthrough.svg`, `reports/visual-walkthrough-evidence-receipt.md`, `reports/visual-walkthrough-evidence-receipt.json`
- **Static gallery**: Open locally or from GitHub Pages; it contains no JavaScript or remote assets.
  - Paths: `reports/index.html`
- **Single backtest report**: Compare Markdown, JSON, HTML, and manifest paths for the same fixture-backed run.
  - Paths: `reports/sample-report.md`, `reports/sample-report.json`, `reports/sample-report.html`, `reports/sample-manifest.md`
- **Parameter sweep reports**: Check ranked historical fixture diagnostics and split robustness fields without treating rankings as predictions.
  - Paths: `reports/sample-sweep.md`, `reports/sample-sweep.json`, `reports/sample-sweep.html`, `reports/sample-sweep-split.md`, `reports/sample-sweep-split.json`, `reports/sample-sweep-split.html`
- **Regime comparison reports**: Check synthetic bull, choppy, and drawdown-recovery fixture scenarios only.
  - Paths: `reports/regime-comparison.md`, `reports/regime-comparison.json`, `reports/regime-comparison.html`

## Source Fixture Boundaries

- `examples/data/sample_tqqq_qld_like.csv` with `examples/data/sample_tqqq_qld_like.csv.provenance.json`: Synthetic static OHLC fixture for deterministic report and sweep examples.
- `examples/data/sample_multi_regime.csv` with `examples/data/sample_multi_regime.csv.provenance.json`: Synthetic static multi-regime fixture for deterministic regime-comparison examples.

## Artifact Integrity Summary

- Integrity status: `PASS`
- Interpretation: PASS: All expected static reviewer artifacts were present and hashed at generation time.
- Caveat: This is artifact-integrity evidence only; it confirms local file bytes at generation time and does not validate financial correctness, future performance, recommendations, or investment suitability.
- Algorithm: `sha256`
- Scope: local static reviewer evidence artifacts only; hashes are artifact-integrity provenance at generation time, not financial validation
- Present artifacts: `22` of `22`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| docs/static-gallery-walkthrough.svg | present | 5721 | 5ecbd181bd380ee4afba13f866615b942e79b6700d891549cee361a9557bed63 |
| reports/index.html | present | 11855 | f16a40b51a361613816dfbebb7d290e162c0dc0fea7112248451b5151b887d31 |
| reports/sample-report.md | present | 3543 | 20ba4fb3f9b1bc739f2e4ccf039e478ac41ddf570a199b6e075b783b54a48ebc |
| reports/sample-report.json | present | 3015 | 4b69d8391304c7642fce4394ce7b8648fdd664bc5f11762cb9c1d618ec24dd81 |
| reports/sample-report.html | present | 5575 | bcd9cff8ebf339ff54e0cd43df183179288659c3e9b86957f7cb524ef4b663a6 |
| reports/sample-manifest.md | present | 1275 | 8b65cf5afcf1519f8a954709f9bda563f9d0debb3e6825b1554e6d12fc58c0cc |
| reports/sample-sweep.md | present | 1484 | e224677470ece1241da80001fae24cf0cae2afdaaa8be2bc29e122fb68183daf |
| reports/sample-sweep.json | present | 1515 | fda47bf13e882df3da0b508561907a25809c4782e2f77aee285dd7cde4e710d9 |
| reports/sample-sweep.html | present | 3394 | 8813d84f637bde560d3956cde33be2b7c20e5e17a768c94f7764ac745e59fc95 |
| reports/sample-sweep-split.md | present | 2426 | 136eace686e27108c327c907aba9006ffcaf928bcaa7948184bc7201a1b0e01d |
| reports/sample-sweep-split.json | present | 3697 | cf4c7ed1a097f8c07a28309e8e464605265746a95c1403694f22e0288d46b40f |
| reports/sample-sweep-split.html | present | 4883 | eb06502662be962bad4eedac45c225f45739113cba3347edae5d106c32287bf7 |
| reports/regime-comparison.md | present | 5085 | 43ae6641ea4ac295855552c239d431fd768f00981c7333b67283fd2c1a24f027 |
| reports/regime-comparison.json | present | 18705 | 7f9b476dfde111397d16a3c7eea10f79a25edb9a00e1a132ed5b604fa464ece8 |
| reports/regime-comparison.html | present | 7954 | a999d54f3d2bb1da849a3d87fd6340051a33a6d3997a4d9f5825573935527aae |
| examples/data/sample_tqqq_qld_like.csv | present | 1125 | 4ca9451f8a391a90530d8199375387bfa233282aa1845e5a64074142c62c1e90 |
| examples/data/sample_tqqq_qld_like.csv.provenance.json | present | 798 | c7bfe5cc08727e8ba19445c47103f380975be648cc6c74b595060649abd38a68 |
| examples/data/sample_multi_regime.csv | present | 1984 | 448940642e8eac3a97ca4af9a10aa7272fb68fd31e69b6628bef0ab7ff31a015 |
| examples/data/sample_multi_regime.csv.provenance.json | present | 2419 | df6c4da0c88250d340c378a076b3fbc35adf060ab6129851985d91e232844e32 |
| docs/data-provenance.md | present | 3324 | 2f54077d55203210371f331269d1f51fc6faa95583eb407f9be89b1a19d7366b |
| docs/artifact-gallery.md | present | 25258 | 6486b09be3991ce1632f7f56d58c829d7f73357c4225c863e7ad0d309bb187f7 |
| docs/static-gallery-manifest.md | present | 14378 | 3587015ef4f4437c4352cc8d566861e73ecdf72f5062237d279a91d6a76b50c1 |

## Not Claimed

- No live market data was fetched by this receipt.
- No broker, account, order-routing, or position-sizing workflow is included.
- No report row is a recommendation, forecast, trading signal, or investment advice.
- Hashes prove local file-byte identity at generation time, not financial correctness or future performance.

## Boundary Flags

- research_only: `True`
- static_only: `True`
- fixture_or_static_data_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`
