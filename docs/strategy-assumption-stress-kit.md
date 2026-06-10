# Strategy Assumption Stress Kit Guide

The Strategy Assumption Stress Kit is a static reviewer aid for checking whether a strategy writeup keeps assumptions, caveats, and public boundaries visible. It is research-only documentation support, not investment advice, a trading recommendation, a forecast, or a live execution workflow.

Open the generated [HTML](../reports/strategy-assumption-stress-kit.html), [Markdown](../reports/strategy-assumption-stress-kit.md), or [JSON](../reports/strategy-assumption-stress-kit.json) artifact when reviewing a public sample.

## Reviewer Workflow

1. Start with the strategy artifact being reviewed, such as the sample report, scenario card, pre-trade research packet, or thesis ledger.
2. Open the stress kit and compare each assumption group against the artifact wording.
3. Mark any unclear claim as a review follow-up instead of filling in missing context.
4. Check that fees, friction limits, drawdown language, benchmark comparisons, and leveraged ETF-like caveats remain close to the performance discussion.
5. Finish by confirming the [Risk Boundaries](risk-boundaries.md) and [Methodology Audit](methodology-audit.md) still match the claim being shared.

A clean review means the public artifact is easier to inspect. It does not mean the strategy is profitable, robust, suitable, or ready for trading.

## Release-Readiness Receipt

The generated Markdown and JSON include a focused release-readiness receipt for the stress kit. It records the exact rerun commands, the expected generated output paths, and PASS boundary claims for no live data, no broker or account workflow, no orders or position sizing, no recommendations or forecasts, and no investment advice.

Use the receipt as a reproducibility handoff before release review. It is a static receipt only; it does not prove financial correctness, future performance, robustness, suitability, or trading readiness.

## What The Stress Checks Do

The stress checks ask whether the artifact stays bounded when a reviewer changes the question:

- Would the wording still be careful if the sample window, symbol mix, or missing rows changed?
- Are modeled entries, exits, and exposure labels clearly historical diagnostics rather than action instructions?
- Are fees, spreads, liquidity, taxes, tracking difference, and market impact named as limitations?
- Are benchmark comparisons framed as context rather than future product rankings?
- For leveraged ETF-like examples, are daily reset, path dependency, volatility drag, and severe drawdown risk visible?

These checks are documentation and review checks. A `PASS` means the boundary is visible enough for public review.

## What The Stress Checks Do Not Prove

The stress kit does not prove:

- future returns or future risk
- strategy quality or market robustness
- correctness of input data outside the checked-in files
- complete implementation cost, tax, liquidity, or execution modeling
- account suitability, position sizing, or whether to buy, sell, hold, or trade

Use the result as a prompt for clearer documentation, not as approval for market action.

## Beginner Leveraged ETF-Like Caveats

Leveraged ETF-like examples need extra caution because multi-day outcomes are not a simple fixed multiple of the underlying asset's start-to-end return. Daily reset and compounding make the path of daily moves matter.

High volatility can reduce compounded returns even when the simple average move looks favorable. Losses are amplified as well as gains, and adverse paths can create severe or near-total drawdowns. Real products can also differ from simplified examples because of fund expenses, financing, tracking difference, spreads, taxes, liquidity, and market impact.

Beginners should treat any leveraged ETF-like output in this repository as a historical scenario review with visible caveats, not as evidence that any product is suitable to buy, hold, or trade.
