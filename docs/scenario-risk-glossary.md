# Scenario/Risk Glossary

This glossary explains the beginner-facing diagnostics shown in single backtest
reports. These fields are research-only historical review aids. They are not investment advice, trading recommendations, forecasts, broker guidance, or
instructions to buy, sell, hold, or size a position.

## Terms

- **Exposure**: How much of each reviewed period the model treated as in the
  market instead of cash. Higher exposure means the historical result depended
  more on market moves; lower exposure means more periods were modeled as cash.
- **Modeled entry**: A historical model state change from cash exposure to
  market exposure. It is not an executed trade, order, alert, or instruction to
  buy.
- **Modeled exit**: A historical model state change from market exposure to
  cash exposure. It is not an executed trade, order, alert, or instruction to
  sell.
- **Fee drag**: The simplified cost impact charged by the model when exposure
  changes. It helps compare assumptions, but it is not a complete estimate of
  spreads, taxes, slippage, liquidity, market impact, or real broker execution.
- **Drawdown**: The largest historical peak-to-trough decline in the modeled
  equity curve. A larger negative drawdown means the sample path had a deeper
  temporary loss before any later recovery.
- **Buy-and-hold gap**: The strategy return minus the same-period buy-and-hold
  return over the supplied CSV rows. A positive gap means the model beat that
  baseline in this historical sample; a negative gap means it lagged. It is not evidence of future performance.

## Reading Order

Start with exposure and drawdown to understand how much market participation
and downside appeared in the historical path. Then compare fee drag and the
buy-and-hold gap to see how much the modeled assumptions changed the result
relative to a simple same-period baseline.

For project-wide boundaries, see [Risk Boundaries](risk-boundaries.md) and the
[Metric Guide](metric-guide.md).
