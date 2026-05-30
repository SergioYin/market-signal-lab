# Cross-Asset Thesis-Ledger Evidence Packet

- Research-only cross-asset thesis-ledger evidence packet built from the bundled static sample CSV; not investment advice, not trading guidance, not a recommendation, not a prediction, and not a broker connection or execution feature.
- Built from bundled static sample rows only; no live data is requested.

## Source

- **Input path**: examples/data/sample_tqqq_qld_like.csv
- **Symbols**: QQQ_LIKE, QLD_LIKE, TQQQ_LIKE
- **Date range**: 2024-01-02 to 2024-01-11
- **Rows per symbol**: QLD_LIKE=8, QQQ_LIKE=8, TQQQ_LIKE=8

## Strategy Configuration

- **Short window**: 2
- **Long window**: 3
- **Fee bps**: 10.0000

## Assumptions

- Uses only examples/data/sample_tqqq_qld_like.csv and adjacent provenance.
- Uses placeholder QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE rows from the same date range.
- Uses a deterministic 2/3 moving-average configuration so the tiny sample has reviewable exposure states.
- Uses fee_bps as a simplified historical cost assumption.
- Reuses existing single-backtest metrics, exposure review, scenario-risk, and scenario-card helpers.

## Cross-Asset Evidence

| symbol | strategy_return | buy_and_hold_return | strategy_minus_buy_hold | max_drawdown | exposure | exposure_changes | fee_drag |
|---|---|---|---|---|---|---|---|
| QQQ_LIKE | 1.51% | 1.69% | -0.18% | -1.74% | 42.86% | 5 | 0.50% |
| QLD_LIKE | 3.45% | 2.79% | 0.66% | -3.11% | 42.86% | 5 | 0.50% |
| TQQQ_LIKE | 5.06% | 4.37% | 0.68% | -4.91% | 42.86% | 5 | 0.50% |

## Evidence Notes

- Rows are ordered QQQ_LIKE, QLD_LIKE, TQQQ_LIKE for stable diffs.
- Cross-asset differences are historical sample diagnostics only, not rankings or recommendations.
- The LIKE suffix marks placeholders; these rows are not real fund prices.

## QQQ_LIKE Evidence

- **Strategy total return**: 1.51%
- **Buy-and-hold total return**: 1.69%
- **Strategy minus buy-and-hold return**: -0.18%
- **Max drawdown**: -1.74%
- **Average exposure**: 42.86%
- **Exposure changes**: 5
- **Modeled fee drag**: 0.50%
- **Scenario/risk note**: Historical diagnostics only; this scenario/risk interpretation is not investment advice, trading guidance, a prediction, or a broker connection or execution feature.

## QLD_LIKE Evidence

- **Strategy total return**: 3.45%
- **Buy-and-hold total return**: 2.79%
- **Strategy minus buy-and-hold return**: 0.66%
- **Max drawdown**: -3.11%
- **Average exposure**: 42.86%
- **Exposure changes**: 5
- **Modeled fee drag**: 0.50%
- **Scenario/risk note**: Historical diagnostics only; this scenario/risk interpretation is not investment advice, trading guidance, a prediction, or a broker connection or execution feature.

## TQQQ_LIKE Evidence

- **Strategy total return**: 5.06%
- **Buy-and-hold total return**: 4.37%
- **Strategy minus buy-and-hold return**: 0.68%
- **Max drawdown**: -4.91%
- **Average exposure**: 42.86%
- **Exposure changes**: 5
- **Modeled fee drag**: 0.50%
- **Scenario/risk note**: Historical diagnostics only; this scenario/risk interpretation is not investment advice, trading guidance, a prediction, or a broker connection or execution feature.

## Embedded Scenario Cards

- JSON includes one reusable scenario_card object and one rendered scenario_card_markdown string per symbol.
- The embedded cards reuse the existing scenario-card helper and remain historical diagnostics only.

## Risk Boundaries

- **Non-advice boundary**: Research-only cross-asset thesis-ledger evidence packet built from the bundled static sample CSV; not investment advice, not trading guidance, not a recommendation, not a prediction, and not a broker connection or execution feature.
- **Leveraged ETF-like boundary**: Leveraged ETF-like examples require extra caution. Daily reset mechanics make multi-day outcomes path-dependent; losses can grow quickly; and real fund results can differ because of expenses, financing costs, tracking differences, taxes, liquidity, spreads, and market impact that this packet does not model.
- **Scope limits**: Offline artifact only. No live data, broker workflow, account fields, order routing, position sizing instruction, forecast, or execution path.
