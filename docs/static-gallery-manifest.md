# Static Demo Manifest

This manifest defines the public static demo surface for Market Signal Lab v1.3.0. It exists so a cold reviewer can open one first screen, follow local links, and verify the artifact trail without installing the package.

Start at the [Static Sample Gallery](../reports/index.html). It is a plain HTML page with no JavaScript, no remote assets, no live market data calls, no broker connection, and no account flow. Every link is repository-local and relative, so the same file can be opened from a checkout or served from a static host such as GitHub Pages.

## First-Screen Links

- [Static gallery entry page](../reports/index.html)
- [Static demo manifest](static-gallery-manifest.md)
- [Artifact gallery notes](artifact-gallery.md)
- [Split-sweep walkthrough](split-sweep-walkthrough.md)
- [Sample manifest](../reports/sample-manifest.md)

## Demo Artifacts

- [Single backtest HTML](../reports/sample-report.html)
- [Single backtest Markdown](../reports/sample-report.md)
- [Single backtest JSON](../reports/sample-report.json)
- [Fee sensitivity Markdown](../reports/fee-sensitivity.md)
- [Fee sensitivity JSON](../reports/fee-sensitivity.json)
- [Parameter sweep HTML](../reports/sample-sweep.html)
- [Parameter sweep Markdown](../reports/sample-sweep.md)
- [Parameter sweep JSON](../reports/sample-sweep.json)
- [Split-sweep HTML](../reports/sample-sweep-split.html)
- [Split-sweep Markdown](../reports/sample-sweep-split.md)
- [Split-sweep JSON](../reports/sample-sweep-split.json)

## Boundaries

These files are research-only review artifacts. They are not investment advice, recommendations, forecasts, live trading signals, or instructions to buy, sell, hold, trade, or size a position.

The bundled leveraged ETF-like sample is synthetic and simplified. Real leveraged ETF products commonly reset exposure daily, so multi-day results are path-dependent and cannot be estimated by multiplying an underlying index's start-to-end return. Leverage can magnify losses quickly, and real products include expenses, financing costs, tracking differences, taxes, liquidity, and market impact that these sample artifacts do not model.
