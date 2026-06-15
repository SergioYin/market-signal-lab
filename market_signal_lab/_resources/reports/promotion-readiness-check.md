# Public-Promotion Readiness Check

Focused static check for whether the cross-asset thesis ledger has enough public-facing evidence and boundary language for broader promotion. It is not trading readiness, a forecast, a recommendation, or investment advice.

## Gate Labels

- **Source artifact**: reports/cross-asset-thesis-ledger.json (Repo-relative static thesis-ledger JSON path read by this check.)
- **Source content SHA-256**: ce5efe33b26e3e800f61978594513fb12baa922ab51e1fc01b41ea0d27b7f495
- **Default outputs**: reports/promotion-readiness-check.md, reports/promotion-readiness-check.json (Repo-relative paths written by --promotion-readiness-check when output overrides are not supplied.)
- **Release Gate**: PASS
- **Promotion Gate**: WARN
- **PASS/WARN/FAIL counts (checks array)**: 6 / 1 / 0
- **Count scope**: Counts cover the checks array and are ordered PASS/WARN/FAIL.
- **Label meanings**: PASS = Expected documentation evidence and boundary wording are visible.; WARN = Public review/release can continue, but broader promotion or citation stays on hold until resolved or explicitly disclosed.; FAIL = Hold release or broader promotion until the listed fix is addressed.
- **Interpretation**: Release Gate checks whether the static artifact can be shared for review. Promotion Gate checks whether broader public promotion has enough visible evidence and boundary wording. Neither gate is trading readiness, forecast validation, recommendation approval, suitability review, or investment advice.

## Checks

| check | label | release gate impact | promotion gate impact |
|---|---|---|---|
| no_live_data_boundary | PASS | No release blocker found. | No promotion blocker found. |
| no_advice_boundary | PASS | No release blocker found. | No promotion blocker found. |
| benchmark_evidence | PASS | No release blocker found. | No promotion blocker found. |
| fee_evidence | PASS | No release blocker found. | No promotion blocker found. |
| drawdown_evidence | PASS | No release blocker found. | No promotion blocker found. |
| train_test_evidence | WARN | Public review/release can continue; keep the WARN visible. | Broader promotion/citation stays on hold until resolved or explicitly disclosed. |
| leveraged_caveat_evidence | PASS | No release blocker found. | No promotion blocker found. |

## Evidence and Follow-Up

### no_live_data_boundary

- **Label**: PASS
- **Evidence**: input_path=examples/data/sample_tqqq_qld_like.csv; static_source=True; flags=offline_only=True, no_broker_or_live_data=True, historical_diagnostics_only=True
- **Review note**: No fix is listed for this PASS check; keep the evidence visible in public review materials.

### no_advice_boundary

- **Label**: PASS
- **Evidence**: research_only=True; required_terms=not investment advice, not a recommendation, not a prediction
- **Review note**: No fix is listed for this PASS check; keep the evidence visible in public review materials.

### benchmark_evidence

- **Label**: PASS
- **Evidence**: asset_count=3; missing_symbols=none
- **Review note**: No fix is listed for this PASS check; keep the evidence visible in public review materials.

### fee_evidence

- **Label**: PASS
- **Evidence**: missing=none
- **Review note**: No fix is listed for this PASS check; keep the evidence visible in public review materials.

### drawdown_evidence

- **Label**: PASS
- **Evidence**: missing=none
- **Review note**: No fix is listed for this PASS check; keep the evidence visible in public review materials.

### train_test_evidence

- **Label**: WARN
- **Evidence**: validation_split=False; ranked_train_test=False
- **Next fix**: Before broader promotion or citation, attach a split-sweep or train/test artifact that shows train metrics, test metrics, and any return-gap or robustness labels, or explicitly disclose that the evidence is not yet present.

### leveraged_caveat_evidence

- **Label**: PASS
- **Evidence**: leveraged_symbols=QLD_LIKE, TQQQ_LIKE; required_terms=leveraged, daily reset, path-dependent, losses
- **Review note**: No fix is listed for this PASS check; keep the evidence visible in public review materials.

## Actionable Next Fixes

- Before broader promotion or citation, attach a split-sweep or train/test artifact that shows train metrics, test metrics, and any return-gap or robustness labels, or explicitly disclose that the evidence is not yet present.

## Public Boundaries

- This check reads a static thesis-ledger JSON artifact only; it does not fetch live market data, connect to brokers, inspect accounts, route orders, or size positions.
- PASS/WARN/FAIL labels are documentation readiness labels only, not market outlooks, buy/sell/hold signals, forecasts, recommendations, suitability conclusions, or investment advice.
- Leveraged ETF-like examples require extra caution. Daily reset mechanics make multi-day outcomes path-dependent; losses can grow quickly; and real fund results can differ because of expenses, financing costs, tracking differences, taxes, liquidity, spreads, and market impact that this packet does not model.

## Verification Commands

- `python -m market_signal_lab.cli --promotion-readiness-check`
- `python -m market_signal_lab.cli --prediction-readiness-audit`
- `python -m market_signal_lab.cli --validate-thesis-ledger`
- `python -m pytest`
