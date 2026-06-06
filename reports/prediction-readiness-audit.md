# Prediction-Readiness Audit

Static research audit for checking whether the sample artifact keeps historical diagnostics separate from predictions, recommendations, trading instructions, and investment advice.

## How to Read This

- Read PASS as a documentation item found, WARN as a review question, and FAIL as a missing or incomplete boundary.
- Treat every row as a static documentation check, not as a market outlook, action cue, or position-sizing input.
- For leveraged ETF-like rows, confirm the report names daily reset, path dependency, magnified losses, and unmodeled product costs.

## Summary

- **Source artifact**: reports/cross-asset-thesis-ledger.json
- **Overall label**: WARN
- **PASS/WARN/FAIL counts**: 5 / 1 / 0
- **Boundary**: This audit checks whether required labels and supporting fields are visible in a static historical artifact for public review. It is not a prediction, forecast, recommendation, trading instruction, or investment-advice approval.

## Leveraged ETF Risk Boundary

Leveraged ETF-like examples are research fixtures only. Daily reset and compounding can make multi-day results path-dependent, losses can be magnified quickly, and real funds can differ because of expenses, financing, tracking differences, taxes, liquidity, spreads, and market impact that this audit does not model.

## Criteria

| criterion | label | status |
|---|---|---|
| static_data | PASS | Artifact is limited to static/offline historical rows. |
| non_advice_boundary | PASS | Research-only and non-advice wording is present. |
| benchmark_presence | PASS | Every asset includes same-period buy-and-hold benchmark fields. |
| fee_drawdown_exposure_presence | PASS | Fee, drawdown, and exposure diagnostics are present. |
| train_test_diagnostics | WARN | No train/test diagnostics are present in this ledger artifact. |
| leveraged_etf_caveats | PASS | Leveraged ETF-like daily-reset and path-dependency caveats are present. |

## Evidence Notes

### static_data

- **Label**: PASS
- **Status**: Artifact is limited to static/offline historical rows.
- **Evidence**: input_path=examples/data/sample_tqqq_qld_like.csv; offline_only=True
- **Review note**: Static sample rows are diagnostics only and do not update from live markets.

### non_advice_boundary

- **Label**: PASS
- **Status**: Research-only and non-advice wording is present.
- **Evidence**: research_only=True; required_terms=not investment advice, not a recommendation, not a prediction
- **Review note**: Passing this check does not change the artifact scope; it confirms the boundary label is present.

### benchmark_presence

- **Label**: PASS
- **Status**: Every asset includes same-period buy-and-hold benchmark fields.
- **Evidence**: asset_count=3; missing_symbols=none
- **Review note**: Benchmarks are comparison diagnostics only, not action guidance.

### fee_drawdown_exposure_presence

- **Label**: PASS
- **Status**: Fee, drawdown, and exposure diagnostics are present.
- **Evidence**: missing=none
- **Review note**: These diagnostics describe modeled history only and omit taxes, spreads, market impact, and execution-quality assumptions.

### train_test_diagnostics

- **Label**: WARN
- **Status**: No train/test diagnostics are present in this ledger artifact.
- **Evidence**: validation_split=False; ranked_train_test=False
- **Review note**: Absence is a review warning, not a failure of the static ledger shape; use split-sweep artifacts for historical train/test rank and return-gap documentation checks.

### leveraged_etf_caveats

- **Label**: PASS
- **Status**: Leveraged ETF-like daily-reset and path-dependency caveats are present.
- **Evidence**: leveraged_symbols=QLD_LIKE, TQQQ_LIKE; required_terms=leveraged, daily reset, path-dependent, losses
- **Review note**: Leveraged ETF-like sample rows require extra caution because multi-day outcomes can diverge sharply from simple leverage multiples.

## Verification Commands

- `python -m market_signal_lab.cli --prediction-readiness-audit`
- `python -m market_signal_lab.cli --validate-thesis-ledger`
- `python -m pytest`
