# Cold Review Checklist

Use this checklist to evaluate the public static demo in 2-5 minutes. It is for research review only. It does not provide investment advice, trading recommendations, forecasts, live trading signals, broker guidance, account setup steps, or instructions to buy, sell, hold, or trade.

## Quick Pass

1. Open the [public static demo](https://sergioyin.github.io/market-signal-lab/) and confirm it presents a static artifact gallery, not an execution tool.
2. Open the [Static Demo Manifest](static-gallery-manifest.md) and check that the demo surface is described as no JavaScript, no remote assets, no live market data calls, no broker connection, and no account flow.
3. Open one human-readable artifact, such as the [single backtest report](../reports/sample-report.md) or [split-sweep report](../reports/sample-sweep-split.md), and identify the input assumptions, date range, metrics, and caveats before reading any result.
4. Open the matching JSON artifact, such as the [single backtest JSON](../reports/sample-report.json) or [split-sweep JSON](../reports/sample-sweep-split.json), and confirm the same run metadata is available in structured form.
5. Read the [Risk Boundaries](risk-boundaries.md) and [Example Data and Synthetic Data Caveats](example-data.md) before drawing any research conclusion.

## What To Look For

- The sample data is synthetic and static, not a live feed or licensed market dataset.
- Reported returns, drawdowns, fee drag, exposure fields, sweep ranks, and robustness labels are historical diagnostics only.
- Buy-and-hold comparisons are context fields for the same sample period, not recommendations.
- The demo should make caveats visible near the artifacts, not hide them in release history.
- A useful review outcome is understanding what the artifacts claim, what they do not claim, and whether the links make that boundary easy to verify.

## Stop Conditions

Stop the review if you are looking for investment advice, a trading recommendation, a forecast, live execution, broker integration, account instructions, or real-time market data. Market Signal Lab is a research-only static demo and backtesting sandbox.
