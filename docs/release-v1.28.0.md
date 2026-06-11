# v1.28.0 Release Notes

Market Signal Lab v1.28.0 adds the Strategy Assumption Stress Kit for public, research-only review of strategy assumptions, stress-check wording, beginner risk boundaries, and leveraged ETF-like caveats. The kit is a static documentation review aid; it is not financial validation, a trading-readiness approval, a forecast, a recommendation, or investment advice.

## Added

- Added [Strategy assumption stress kit HTML](../reports/strategy-assumption-stress-kit.html) for browser-openable static review.
- Added [Strategy assumption stress kit Markdown](../reports/strategy-assumption-stress-kit.md) with the same deterministic kit and a release-readiness receipt.
- Added [Strategy assumption stress kit JSON](../reports/strategy-assumption-stress-kit.json) with boundary flags, stress-check fields, generated output paths, and exact rerun commands.
- Added the public guide: [Strategy Assumption Stress Kit Guide](strategy-assumption-stress-kit.md).
- Added the CLI route:

```bash
python -m market_signal_lab.cli --strategy-assumption-stress-kit
```

## Verification

Regenerate the stress-kit artifacts:

```bash
python -m market_signal_lab.cli --strategy-assumption-stress-kit
git diff -- reports/strategy-assumption-stress-kit.html reports/strategy-assumption-stress-kit.md reports/strategy-assumption-stress-kit.json
```

Run focused checks:

```bash
python -m pytest tests/test_strategy_assumption_stress_kit.py tests/test_selfcheck.py
python scripts/selfcheck.py
```

Run the broader local release hygiene gate before tagging:

```bash
python -m pytest
python -m compileall market_signal_lab tests scripts
git diff --check
```

## Finance-Risk Boundaries

The Strategy Assumption Stress Kit uses deterministic static artifact generation only. It does not read live market data, call network APIs, connect to brokers, inspect accounts, route orders, size positions, forecast returns, rank products for future use, recommend buy/sell/hold/trade actions, or provide investment advice.

PASS/WARN labels in the kit are documentation-review labels for boundary visibility. They do not prove profitability, robustness, financial correctness, implementation cost completeness, suitability, or future performance.
