# v1.2.0 Release Notes

Market Signal Lab v1.2.0 adds a focused, research-only fee sensitivity artifact for the bundled single backtest.

## Added

- `scripts/fee_sensitivity.py` reads `examples/data/sample_tqqq_qld_like.csv` and writes `reports/fee-sensitivity.md` plus `reports/fee-sensitivity.json`.
- The artifact compares several `fee_bps` assumptions for the existing 20/50 moving-average settings.
- Each row reports historical total return, buy-and-hold total return, strategy-minus-buy-and-hold return, max drawdown, modeled exposure changes, modeled entries/exits, average exposure, periods in market, and modeled fee drag.
- Beginner caveats explain that the fixture is tiny and synthetic, fee assumptions are not real execution-cost estimates, and the bundled 20/50 sample has no modeled exposure changes.

## Documentation

- README, documentation map, artifact gallery, and static report gallery now link the fee sensitivity Markdown and JSON artifacts.
- Selfcheck regenerates the new artifacts and includes them in public-safe claim checks.

## Boundaries

- No broker integrations, live market data, trading execution, forecasts, or recommendations were added.
- The fee sensitivity output is historical research metadata only.
