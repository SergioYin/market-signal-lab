# v1.1.0 Release Notes

v1.1.0 adds exposure/trade review metadata to single backtest artifacts. The release does not add forecasting, live data, broker execution, investment advice, trading recommendations, or trade instructions.

## What Changed

- Added a `Modeled Exposure Review` section to Markdown reports for single backtests.
- Added `exposure_trade_review` to JSON reports with period counts, in-market/cash percentages, average exposure, exposure changes, modeled entries/exits, and modeled fee drag.
- Kept the review labels research-only: the fields describe historical model exposure inside the supplied dataset and are not a list of trades to place. For beginners, exposure changes, modeled entries, and modeled exits are historical model states, not executed trades or instructions.

## Research-Only Boundary

Exposure/trade review metadata summarizes what the model did in a historical backtest. It is not investment advice, not a recommendation, not trading guidance, not a forecast, and not evidence of future performance. Beginners should not read exposure changes, modeled entries, or modeled exits as executed trades or instructions to buy, sell, hold, or size a position.
