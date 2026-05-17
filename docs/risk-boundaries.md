# Risk Boundaries

- This project is for research and analysis only; it is **not** live trading software.
- It has **no broker/exchange connection** and cannot place orders.
- Backtests are historical analyses, not forecasts. A strategy that worked in-sample can fail in live markets.
- Synthetic leveraged ETF behavior differs from cash positions and can deviate sharply from expectations.
- For **TQQQ/QLD** in particular:
  - Returns are path-dependent because of daily reset mechanics.
  - Volatility drag and rebalancing can reduce long-horizon returns even when the underlying index is flat.
  - Intraday and regime-driven swings can create **extreme drawdowns**.
  - Holding for long periods can increase risk as compounding effects accumulate.
