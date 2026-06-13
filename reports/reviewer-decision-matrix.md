# Reviewer Decision Matrix

Use this static review matrix to decide whether a public-facing static backtest artifact can be released and whether any barriers remain before promotion. It does not generate trading signals, predictions, recommendations, or investment advice.

## Source and Scope
- **Source artifact**: reports/sample-report.json
- **Purpose**: Help cold reviewers decide whether a checked static backtest artifact is safe for release and what must be completed before broader promotion.

## Decision Gates
- **Release Gate**: WARN
- **Promotion Gate**: FAIL
- **Score counts**: pass=7 / warn=1 / fail=0
- PASS means static evidence does not block release.
- WARN means release may proceed only for review but requires additional run-time checks before promotion.
- FAIL means the artifact should not be released or promoted.

## How to Read the Gates
- Release Gate is about whether this static review artifact is safe to release for people to inspect; PASS is clear, WARN means release is okay for review but still needs follow-up before promotion.
- Promotion Gate is about whether the artifact is ready for broader public sharing, documentation, and demo quality. It only turns PASS when all categories are suitable for public presentation.

- A Release Gate PASS/WARN result is not a buy/sell signal.
- Promotion Gate is about public demo quality, not proof of strategy profitability.

## Decision Criteria
| criterion | label | evidence | review note |
|---|---|---|---|
| data_provenance | PASS | Checked-in artifacts are generated from bundled historical CSV files and checked into provenance sidecar metadata in examples/data. | PASS means provenance is explicit and static; reviewers should still confirm source paths before promoting. |
| benchmark_comparison | PASS | Static backtest summaries include same-period buy-and-hold comparison for each configured asset and a strategy-minus-buy-and-hold delta. | The benchmark is a historical reference and does not imply future superiority. |
| fee_drawdown_disclosure | PASS | Fee drag and max drawdown fields are present in historical metrics, with explicit notes about modeled fee assumptions. | PASS means baseline fee/drawdown exposure is disclosed; promote only after confirming fee model assumptions in the exact artifact build path. |
| train_test_robustness | WARN | Train/test metadata is generated only when split options are used and should be checked on a split run before deciding. | WARN means this artifact should be reviewed with train/test run outputs before any promotion-grade approval. |
| beginner_risk_language | PASS | Beginner-facing documentation includes no-prediction, no-advice, and path-dependent risk wording for leveraged examples. | PASS indicates suitable language for first-time reviewers and non-specialist audiences. |
| leveraged_etf_caveat | PASS | Leveraged ETF-like fixtures are explicitly flagged as simplified examples with path-dependent daily reset and volatility drag caveats. | PASS means the caveat appears in artifact-facing documentation and risk text. |
| reproducibility_evidence | PASS | This matrix is generated with reproducible static CLI commands that output markdown and JSON without live market inputs. | PASS means a reviewer can rerun generation locally to validate consistency before promotion. |
| no_advice_boundary | PASS | Static artifact flags explicitly disallow live data, broker/account, order, recommendations, forecasts, and investment-advice workflows. | PASS confirms the primary non-advice boundary is stated and preserved in this artifact package. |

## Public Boundaries
- This matrix is a static historical research review aid only; it does not provide investment advice, trading guidance, recommendations, forecasts, buy/sell/hold signals, order steps, or position sizing.
- No generated field, PASS/WARN/FAIL label, or gate result validates financial correctness, profitability, suitability, or future performance.
- Leveraged ETF-like examples require extra caution. Daily reset mechanics make multi-day outcomes path-dependent; losses can grow quickly; and real fund results can differ because of expenses, financing costs, tracking differences, taxes, liquidity, spreads, and market impact that this packet does not model.

## Verification Commands
- `python -m market_signal_lab.cli --reviewer-decision-matrix`
- `python -m market_signal_lab.cli --prediction-readiness-audit`
- `python -m market_signal_lab.cli --reviewer-rerun-receipt`
- `python -m pytest`

## Boundary Flags
- research_only: `True`
- static_only: `True`
- historical_diagnostics_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`
