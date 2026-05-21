# Fee Sensitivity Comparison

Research-only comparison for the bundled static sample CSV. This artifact does not use broker connections, live market data, or execution data.

## Setup

- **Input CSV**: examples/data/sample_tqqq_qld_like.csv
- **Symbol**: QQQ_LIKE
- **Short window**: 20
- **Long window**: 50
- **Date range**: 2024-01-02 to 2024-01-11
- **Rows**: 8

## Comparison

| fee_bps | total_return | buy_and_hold_total_return | strategy_minus_buy_and_hold_return | max_drawdown | modeled_exposure_changes | modeled_entries | modeled_exits | average_exposure | total_fee_drag |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0 | 0.00% | 1.69% | -1.69% | 0.00% | 0 | 0 | 0 | 0.00% | 0.00% |
| 5.0 | 0.00% | 1.69% | -1.69% | 0.00% | 0 | 0 | 0 | 0.00% | 0.00% |
| 10.0 | 0.00% | 1.69% | -1.69% | 0.00% | 0 | 0 | 0 | 0.00% | 0.00% |
| 25.0 | 0.00% | 1.69% | -1.69% | 0.00% | 0 | 0 | 0 | 0.00% | 0.00% |
| 50.0 | 0.00% | 1.69% | -1.69% | 0.00% | 0 | 0 | 0 | 0.00% | 0.00% |

## Beginner Caveats

- Fee sensitivity here means rerunning the same historical model with different basis-point assumptions; it is not an estimate of real broker costs, spreads, taxes, liquidity, or market impact.
- The bundled sample is intentionally tiny and synthetic. Its numbers are useful for checking artifact shape and reproducibility, not for making market claims.
- The TQQQ/QLD-like fixture labels do not make this a real leveraged ETF model. Daily-reset path dependency, fund expenses, financing costs, tracking differences, taxes, liquidity, and market impact are outside this fee_bps comparison.
- The existing 20/50 moving-average setup has no modeled exposure changes on this eight-row sample, so changing fee_bps does not change the reported return in this artifact.
- Modeled exposure changes, entries, exits, and fee drag are historical model metadata only. They are not executed trades or instructions.
- Buy-and-hold comparison fields are same-period historical context only; they are not recommendations or evidence of future performance.

## Data Provenance

- Research-only static fixture metadata; not live data, not investment advice, and not a prediction.
- **Dataset label**: sample_tqqq_qld_like
- **Data kind**: synthetic_static_fixture
- **Source**: Hand-authored deterministic OHLC sample bundled with Market Signal Lab for offline examples and tests.
- **As-of date**: 2026-05-18
