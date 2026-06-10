# Strategy Assumption Stress Kit

Use this deterministic static kit to review strategy assumptions, stress checks, beginner risk boundaries, and leveraged ETF-like caveats without treating any item as a prediction, recommendation, trading instruction, order workflow, or investment advice.

## What This Artifact Is

- It gives reviewers a static checklist for pressure-testing how a strategy writeup explains assumptions, stress boundaries, and leveraged ETF-like caveats without turning the artifact into a forecast, recommendation, order workflow, or investment advice.
- It is generated without live market data, broker connections, account access, orders, forecasts, recommendations, or position sizing.

## Assumptions To Stress

| group | assumption | stress question |
|---|---|---|
| data_window | A result only describes the static rows included in the artifact. | Would the conclusion still be labeled carefully if the date window, symbol mix, or missing rows changed? |
| signal_rule | A strategy rule is a simplified historical model state, not an action instruction. | Does the writeup keep entries, exits, and exposure labels separate from what a reader should do? |
| costs_and_frictions | Fees, spreads, liquidity, taxes, tracking difference, and market impact can change realized outcomes. | Does the artifact avoid treating simplified modeled fees as complete implementation costs? |
| benchmark_context | Same-window benchmarks are reference points for review, not recommendations. | Does the comparison explain underperformance, drawdown, exposure, and fee drag without ranking products for future use? |

## Stress Checks

| check | review prompt | failure boundary |
|---|---|---|
| window_sensitivity | Re-read the artifact as if the start or end date moved. The claim should remain limited to the supplied static rows. | The wording implies the same result applies in another period. |
| drawdown_tolerance_language | Confirm max drawdown is presented as a historical diagnostic and not as a loss limit, guarantee, or comfort label. | The wording makes a large drawdown sound acceptable, bounded, or suitable for a reader. |
| fee_drag_visibility | Confirm fees and friction limits are visible near return and benchmark comparisons. | Return comparisons appear without cost, friction, or implementation caveats. |
| leverage_path_dependency | For leveraged ETF-like examples, confirm daily reset, path dependency, volatility drag, and extreme drawdown caveats are named. | The artifact implies multi-day returns can be read as a simple fixed multiple. |

## Hypothetical Stress Review Outcome

- Fixture: `hypothetical_static_review_001`
- Review scope: Example documentation review of one hypothetical strategy writeup; no market data, portfolio holdings, or account context is used.
- Overall label: `WARN`

| label | check | outcome | review note |
|---|---|---|---|
| PASS | window_sensitivity | The writeup states that conclusions are limited to the fixed sample rows. | PASS means the documentation boundary is visible enough for research review. |
| WARN | fee_drag_visibility | The writeup mentions modeled fees but separates other frictions into a later caveat. | WARN means reviewers should inspect whether cost and friction limits are visible near comparison text. |

- This fixture demonstrates PASS/WARN wording for a static review artifact only; it is not a forecast, suitability view, trading instruction, or investment advice.

## Beginner Risk Boundaries

- **research_scope**: This kit is a static review aid. It does not say what to buy, sell, hold, size, or trade.
- **historical_results**: Historical sample results are diagnostics from fixed assumptions and rows. They are not predictions of future returns.
- **stress_check_limits**: A passed stress check means a documentation boundary is visible; it does not prove a strategy is safe, robust, or suitable.

## Leveraged ETF-Like Caveats

- **path_dependency**: Daily reset and compounding can make multi-day outcomes depend heavily on the order of gains and losses.
- **volatility_drag**: High volatility can reduce compounded results even when the simple average move looks favorable.
- **extreme_drawdown**: Leveraged ETF-like paths can lose value quickly and may experience severe or near-total drawdowns in adverse paths.
- **implementation_gap**: Real products can differ from simplified examples because of expenses, financing, tracking difference, spreads, taxes, liquidity, and market impact.

## Do Not Use This For

- live data workflow
- broker, account, or order workflow
- position sizing
- forecasting future returns
- trading recommendation
- investment advice

## Release-Readiness Receipt

- Receipt type: `strategy_assumption_stress_kit_release_readiness`

### Exact Rerun Commands

- `python -m market_signal_lab.cli --strategy-assumption-stress-kit`
  - Purpose: Regenerate the Strategy Assumption Stress Kit Markdown, JSON, and browser-openable HTML from deterministic stdlib-only code.
  - Generated output paths: `reports/strategy-assumption-stress-kit.html`, `reports/strategy-assumption-stress-kit.md`, `reports/strategy-assumption-stress-kit.json`
- `python scripts/selfcheck.py`
  - Purpose: Regenerate checked-in sample artifacts and verify the stress-kit payload, Markdown, HTML, gallery links, and public boundaries.
  - Generated output paths: `reports/strategy-assumption-stress-kit.html`, `reports/strategy-assumption-stress-kit.md`, `reports/strategy-assumption-stress-kit.json`, `reports/index.html`
- `python -m pytest tests/test_strategy_assumption_stress_kit.py tests/test_selfcheck.py`
  - Purpose: Run the focused tests that cover the stress-kit schema, rendered release-readiness receipt, CLI defaults, and selfcheck contract.
  - Generated output paths: `none`

### Generated Output Paths

- `reports/strategy-assumption-stress-kit.html` (html), from `python -m market_signal_lab.cli --strategy-assumption-stress-kit`
- `reports/strategy-assumption-stress-kit.md` (markdown), from `python -m market_signal_lab.cli --strategy-assumption-stress-kit`
- `reports/strategy-assumption-stress-kit.json` (json), from `python -m market_signal_lab.cli --strategy-assumption-stress-kit`

### No-Live-Data / No-Advice Boundaries

- **PASS no_live_data**: The stress-kit command does not read CSV data, call network APIs, or fetch current market data.
- **PASS no_broker_or_account**: The artifact has no broker connection, account inspection, order routing, or execution workflow.
- **PASS no_orders_or_position_sizing**: The kit records documentation stress checks only and does not size positions or give buy, sell, hold, or trade instructions.
- **PASS no_recommendations_or_forecasts**: PASS/WARN labels are review labels for artifact wording, not forecasts, product rankings, or recommendations.
- **PASS not_investment_advice**: The receipt preserves the research-only, historical-diagnostics-only, non-advice boundary.

### Reviewer Notes

- Run commands from the repository root after normal Python setup.
- A generated output path is release-ready only when the command exits 0 and the checked-in path is present or updated.
- This receipt records deterministic rerun instructions and static boundaries; it does not prove financial correctness, future performance, robustness, suitability, or trading readiness.

## Boundary Flags

- research_only: `True`
- static_only: `True`
- historical_diagnostics_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`

## Verification Commands

- `python -m market_signal_lab.cli --strategy-assumption-stress-kit`
- `python scripts/selfcheck.py`
- `python -m pytest`
