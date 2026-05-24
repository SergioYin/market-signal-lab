# Regime Comparison Report

- Research-only historical comparison of deterministic bundled fixtures; not investment advice, not a recommendation, not a prediction, and not a broker connection or execution feature.
- To reproduce this checked sample from the repository root, run market-signal-lab --regime-comparison.
- Open reports/regime-comparison.md first for the readable review, reports/regime-comparison.html for a browser view, or reports/regime-comparison.json for structured data.
- Buy-and-hold values use the same close-to-close sample as each strategy run.
- Exposure and cash-time are historical model states, not trades or instructions.

## Comparison Table

| regime | symbol | strategy_return | buy_and_hold_return | strategy_minus_buy_hold | max_drawdown | exposure | cash_time | exposure_changes | whipsaw_rate |
|---|---|---|---|---|---|---|---|---|---|
| bull | BULL_REGIME | 12.66% | 19.20% | -6.54% | 0.00% | 63.64% | 36.36% | 1 | 9.09% |
| choppy | CHOPPY_REGIME | -1.48% | 0.20% | -1.68% | -1.58% | 27.27% | 72.73% | 2 | 18.18% |
| drawdown recovery | DRAWDOWN_RECOVERY_REGIME | 13.08% | 3.00% | 10.08% | 0.00% | 27.27% | 72.73% | 1 | 9.09% |

## Interpretation

- **Best strategy total return**: DRAWDOWN_RECOVERY_REGIME.
- **Best buy-and-hold total return**: BULL_REGIME.
- **Largest modeled drawdown**: CHOPPY_REGIME.
- **Highest whipsaw pressure**: CHOPPY_REGIME.
- **Most cash time**: CHOPPY_REGIME.

## bull (BULL_REGIME)

- **Synthetic-only label**: deterministic fixture scenario; not historical market data, not predictive, and not live-trading use.
- **Generation source**: Monotonic upward path used to exercise trend-following examples.
- **Generation assumptions**: Close prices increase every sample period by construction; Open prices equal the prior close after the first row; High and low prices are synthetic padding around open and close.
- **Buy-and-hold comparison**: Strategy minus buy-and-hold was -6.54% over this deterministic sample.
- **Exposure/cash-time**: The model spent 36.36% of close-to-close periods in cash, so lower exposure means more missed market movement and less time bearing market risk in this sample.
- **Drawdown**: The worst modeled peak-to-trough decline was 0.00%; more negative values show larger interim losses before recovery.
- **Whipsaw**: 1 exposure change across 11 periods produced a whipsaw rate of 9.09%. Higher values indicate more historical switching between market and cash states.

## choppy (CHOPPY_REGIME)

- **Synthetic-only label**: deterministic fixture scenario; not historical market data, not predictive, and not live-trading use.
- **Generation source**: Alternating path that ends near flat after repeated reversals.
- **Generation assumptions**: Close prices alternate around the starting level by construction; Open prices equal the prior close after the first row; High and low prices are synthetic padding around open and close.
- **Buy-and-hold comparison**: Strategy minus buy-and-hold was -1.68% over this deterministic sample.
- **Exposure/cash-time**: The model spent 72.73% of close-to-close periods in cash, so lower exposure means more missed market movement and less time bearing market risk in this sample.
- **Drawdown**: The worst modeled peak-to-trough decline was -1.58%; more negative values show larger interim losses before recovery.
- **Whipsaw**: 2 exposure changes across 11 periods produced a whipsaw rate of 18.18%. Higher values indicate more historical switching between market and cash states.

## drawdown recovery (DRAWDOWN_RECOVERY_REGIME)

- **Synthetic-only label**: deterministic fixture scenario; not historical market data, not predictive, and not live-trading use.
- **Generation source**: Decline followed by recovery for drawdown diagnostics.
- **Generation assumptions**: Close prices fall first and then recover by construction; Open prices equal the prior close after the first row; High and low prices are synthetic padding around open and close.
- **Buy-and-hold comparison**: Strategy minus buy-and-hold was 10.08% over this deterministic sample.
- **Exposure/cash-time**: The model spent 72.73% of close-to-close periods in cash, so lower exposure means more missed market movement and less time bearing market risk in this sample.
- **Drawdown**: The worst modeled peak-to-trough decline was 0.00%; more negative values show larger interim losses before recovery.
- **Whipsaw**: 1 exposure change across 11 periods produced a whipsaw rate of 9.09%. Higher values indicate more historical switching between market and cash states.

## Caveats

- This artifact uses deterministic bundled sample data for research workflows only. The prices were constructed for examples and tests; they are not real market prices.
- Results are hypothetical, historical, and sensitive to data, fees, and chosen parameters.
- A synthetic backtest can show how the software behaves, but it cannot show what will happen in live markets.
- Nothing in this report is investment advice, trading guidance, a recommendation, a prediction, or a live-trading signal.
