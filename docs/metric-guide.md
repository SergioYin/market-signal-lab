# Metric Guide

Market Signal Lab reports use a small set of metrics to describe one historical backtest or one row in a parameter sweep. These metrics are educational diagnostics only. They are not investment advice, trading recommendations, forecasts, or instructions to buy, sell, hold, or use a strategy.

The numbers describe what happened inside the supplied dataset, with the report's chosen settings, fees, and date range. They do not say what will happen in future markets.

## Strategy Total Return

Strategy total return is the percentage change in the strategy's modeled equity from the start of the backtest to the end.

If the report starts at `1.0000` and ends at `1.1000`, the strategy total return is `10.00%`. If it ends at `0.9000`, the strategy total return is `-10.00%`.

This metric is simple and useful, but it does not show how rough the path was. Two runs can end with the same total return while one had much larger losses along the way.

## Buy-And-Hold Total Return

Buy-and-hold total return is the same-period return from holding the input asset for the whole report range.

It is included as a baseline. A beginner can read it as, "What would the supplied price series have done if the model stayed invested from the first row to the last row?"

This is not a recommendation to buy or hold the asset. It is only a comparison point for the same historical data window.

## Strategy Minus Buy-And-Hold Return

Strategy-minus-buy-and-hold return subtracts the buy-and-hold return from the strategy total return.

For example:

- Strategy total return: `8.00%`
- Buy-and-hold total return: `5.00%`
- Strategy minus buy-and-hold return: `3.00%`

A positive value means the strategy finished above the buy-and-hold baseline in that historical run. A negative value means it finished below that baseline. It does not prove that one approach is better for the future.

## Annualized Return

Annualized return converts the backtest return into a yearly-style rate based on the length of the sample.

This can make runs with different date ranges easier to compare, but it can also exaggerate short samples. A very short backtest with a large move can produce an annualized number that looks dramatic because the math assumes a similar pace for a full year.

## Max Drawdown

Max drawdown is the largest peak-to-trough drop in the modeled equity curve during the backtest.

For a beginner, this answers, "How far did the report fall from a previous high before recovering or ending?"

A max drawdown of `-25.00%` means the modeled equity was down 25% from an earlier high at its worst point. Lower drawdowns are usually easier to tolerate, but this metric is still historical and can be worse outside the tested data.

## Volatility

Volatility measures how much the modeled returns varied during the backtest. Higher volatility means the path moved around more.

Volatility is not the same as loss. A high-volatility run can finish positive or negative. It mainly describes unevenness: large day-to-day changes produce a higher volatility number than small, steady changes.

## Sharpe-Like Score

The Sharpe-like score is a simple return-versus-variation diagnostic. It compares annualized return with volatility using the report's simplified assumptions.

Higher values generally mean more return per unit of reported volatility inside the tested sample. A low or negative value means the run produced little return, negative return, or a rough path relative to its return.

The word "like" matters. This project's score is a lightweight diagnostic, not a full institutional Sharpe ratio. It does not include a risk-free rate, taxes, all real-world costs, liquidity effects, or a guarantee that the same risk profile will repeat.

## Win Rate

Win rate is the share of modeled return periods that were positive.

A high win rate does not guarantee a good result. A strategy can win often but lose a lot on a few bad periods. A lower win rate can still finish positive if winning periods are much larger than losing periods.

## Sweep Ranking Metrics

Sweep reports show metrics for several moving-average window combinations. The ranking tells you which settings sorted highest within the tested historical data and ranking rule.

Sweep rankings are not predictions. Testing many parameter combinations can accidentally reward settings that fit noise in one sample. Train/test fields, when present, are diagnostics for comparing two historical partitions, not evidence of future performance or stable behavior.

Split sweep reports also compare each parameter set's train rank with its test
rank. `rank_delta` is test rank minus train rank, and
`train_test_return_gap` is train total return minus test total return. A
`robustness_flag` of `fragile` means the row crossed deterministic review
thresholds for rank movement or return gap inside the supplied sample.
`not_flagged` only means those thresholds were not crossed in that sample; it
does not predict future behavior, claim stability, or advise any trade.

## Leveraged ETF Path-Dependency Caveats

Leveraged ETF-like examples need extra care because daily reset mechanics make returns path-dependent. The final result depends not only on the start and end prices, but also on the sequence of daily moves between them.

In choppy markets, repeated up-and-down moves can reduce long-horizon returns even when the underlying index ends near where it started. This is often called volatility drag. Large drawdowns can also happen quickly because leverage amplifies daily moves.

The bundled leveraged ETF-like sample data is synthetic. It is useful for checking report structure and reproducibility, not for estimating real fund behavior. Real leveraged ETFs can also include tracking error, financing costs, expense ratios, liquidity effects, taxes, and other details that are outside this project's simple reports.

## Reading Metrics Together

No single metric tells the whole story. A beginner-friendly reading order is:

1. Check the date range and input data.
2. Compare strategy total return with buy-and-hold total return.
3. Look at strategy-minus-buy-and-hold return for same-period context.
4. Check max drawdown to understand the largest historical drop.
5. Use volatility and Sharpe-like score to understand how uneven the path was.
6. Read the caveats before drawing any research conclusion.

All of these steps are for historical analysis only. They do not turn a report into advice, a forecast, or a live trading signal.
