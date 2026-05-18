# v0.5.0 Release Notes

- Buy-and-hold benchmark: single backtest reports now include `buy_and_hold_total_return`, a plain baseline showing the return from holding the supplied price series over the same backtest window.
- Strategy comparison metric: reports also include `strategy_minus_buy_and_hold_return`, which shows the strategy return minus the buy-and-hold return for the same historical sample.
- Beginner-friendly report labels: Markdown and HTML reports render these fields as "Buy-and-hold total return" and "Strategy minus buy-and-hold return" instead of jargon-heavy metric names.
- Sample artifacts: the checked-in single-report Markdown, JSON, and HTML samples have been regenerated with the new benchmark fields.
- Research boundary: the benchmark comparison is a historical diagnostic only. It is not investment advice, not a recommendation to buy and hold, and not evidence of future performance.
