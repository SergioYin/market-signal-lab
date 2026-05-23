# Risk Boundaries

- This project is for research and analysis only; it is **not** live trading software.
- It does **not** provide investment advice, trading recommendations, forecasts, or instructions to buy, sell, or hold.
- It has **no broker/exchange connection** and cannot place orders.
- Backtests are historical analyses, not forecasts. A strategy that worked in-sample can fail in live markets.
- Scenario/risk diagnostics such as exposure, modeled entries/exits, fee drag, drawdown, and buy-and-hold gap are defined in the [Scenario/Risk Glossary](scenario-risk-glossary.md). They are historical diagnostics only, not advice or execution cues.
- Synthetic leveraged ETF-like behavior differs from cash positions and can deviate sharply from expectations. The sample data and reports are simplified research fixtures, not a complete model of real fund mechanics, fees, tracking error, borrowing costs, taxes, liquidity, or market impact.
- For **TQQQ/QLD** in particular:
  - Returns are path-dependent because leveraged ETFs generally reset exposure daily. A multi-day result cannot be estimated by simply multiplying the underlying index's start-to-end return.
  - Volatility drag and rebalancing can reduce long-horizon returns even when the underlying index ends flat or only modestly changed.
  - Leverage amplifies losses as well as gains. Intraday and regime-driven swings can create **extreme drawdowns**, including losses that happen much faster than in broad unleveraged funds.
  - Holding for long periods can increase risk as compounding effects accumulate, especially in choppy or declining markets.
  - Beginners should treat any TQQQ/QLD output as a high-risk historical scenario review, not as evidence that leveraged ETFs are suitable to buy, hold, or trade.
