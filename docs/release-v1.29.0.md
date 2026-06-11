# v1.29.0 Release Notes

Market Signal Lab v1.29.0 adds a focused Stress Kit Quickstart Card that condenses the v1.28 Strategy Assumption Stress Kit into a deterministic two-minute reviewer checklist.

## Start Here

- [Stress Kit Quickstart Card Markdown](../reports/stress-kit-quickstart-card.md) - shortest v1.29 reviewer route.
- [Static Sample Gallery](../reports/index.html) - browser-openable artifact dashboard.
- [Documentation Map](index.md) - broader docs navigation after the first review.

## Added

- Added [Stress Kit Quickstart Card Markdown](../reports/stress-kit-quickstart-card.md).
- Added [Stress Kit Quickstart Card JSON](../reports/stress-kit-quickstart-card.json).
- Added the CLI route:

```bash
python -m market_signal_lab.cli --stress-kit-quickstart-card
```

## Boundaries

The quickstart card is a static reviewer checklist only, with no live-data, broker/account, order, position-sizing, forecast, recommendation, or investment-advice surface.

The v1.28 [Strategy Assumption Stress Kit release note](release-v1.28.0.md), [public guide](strategy-assumption-stress-kit.md), and generated [HTML](../reports/strategy-assumption-stress-kit.html), [Markdown](../reports/strategy-assumption-stress-kit.md), and [JSON](../reports/strategy-assumption-stress-kit.json) artifacts remain available for static, research-only review.
