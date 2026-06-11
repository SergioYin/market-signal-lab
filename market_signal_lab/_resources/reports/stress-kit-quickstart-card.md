# Stress Kit Quickstart Card

Use this deterministic two-minute card to review the Strategy Assumption Stress Kit boundary before promoting a static research artifact.

## Source

- Source artifact: Strategy Assumption Stress Kit
- Markdown: `reports/strategy-assumption-stress-kit.md`
- JSON: `reports/strategy-assumption-stress-kit.json`

## Two-Minute Reviewer Checklist

| time box | step | check | pass condition |
|---|---|---|---|
| 0:00-0:20 | scope | Confirm the artifact names a fixed static review scope. Does the writeup limit every conclusion to the supplied artifact and sample window? | The text says the review is static, historical, and bounded to the artifact. |
| 0:20-0:45 | assumptions | Find the strategy rule, data-window, benchmark, and cost assumptions. Can a reviewer see what assumptions would need stress testing before reading results? | Key assumptions are explicit and are not phrased as action instructions. |
| 0:45-1:15 | stress_language | Scan for overclaiming around drawdown, fees, benchmarks, and robustness. Would the wording still be accurate if another static window or fee assumption looked worse? | Claims stay diagnostic and avoid guarantees, forecasts, or product rankings. |
| 1:15-1:40 | leveraged_etf_like_caveats | Verify daily reset, path dependency, volatility drag, and extreme drawdown caveats are visible when leveraged ETF-like examples appear. Does the artifact avoid implying a simple fixed multiple over multiple days? | Leveraged ETF-like caveats are framed as simplified historical diagnostics, not advice. |
| 1:40-2:00 | boundaries | Confirm no live data, broker, account, order, position-sizing, recommendation, forecast, or advice surface is present. Could a cold reviewer mistake this artifact for something to act on? | The artifact stays a documentation review checklist only. |

## Stop Conditions

- **A claim reads like a prediction, recommendation, suitability view, or trading instruction.** Mark WARN or FAIL and request boundary wording before promotion.
- **Live data, broker, account, order, or position-sizing behavior appears in the artifact path.** Stop using this quickstart card; it is scoped only to static review artifacts.

## Completion Receipt

- Source command: `python -m market_signal_lab.cli --stress-kit-quickstart-card`
- Generated output paths: `reports/stress-kit-quickstart-card.md`, `reports/stress-kit-quickstart-card.json`
- Review boundary: Completion means the checklist was reviewed for static documentation boundaries only; it does not validate financial correctness, robustness, suitability, or future performance.

## Boundaries

- research_only: `True`
- static_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`

## Boundary Claims

- This card is generated from static definitions only and does not fetch, stream, refresh, or inspect live market data.
- This card is a reviewer checklist only, not a forecast, recommendation, trading instruction, suitability view, or investment advice.

## Do Not Use This For

- live data workflow
- broker, account, or order workflow
- position sizing
- forecast or recommendation surface
- investment-advice surface
