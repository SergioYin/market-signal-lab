# Static Demo Manifest

This manifest defines the public static demo surface for Market Signal Lab v1.7.0. It exists so a cold reviewer can open one first screen, follow local links, and verify the artifact trail without installing the package.

Start at the [Root Landing](../index.html), then open the [Static Sample Gallery](../reports/index.html). Both are plain HTML pages with no JavaScript, no remote assets, no live market data calls, no broker connection, and no account flow. Every link is repository-local and relative, so the same files can be opened from a checkout or served from a static host such as GitHub Pages.

## First-Screen Links

- [Root landing](../index.html)
- [Cold review checklist](cold-review-checklist.md)
- [Static gallery entry page](../reports/index.html)
- [Static demo manifest](static-gallery-manifest.md)
- [Artifact gallery notes](artifact-gallery.md)
- [Split-sweep walkthrough](split-sweep-walkthrough.md)
- [Sample manifest](../reports/sample-manifest.md)

## Dashboard Cards

The checked-in [Static Sample Gallery](../reports/index.html) starts with a compact no-JavaScript dashboard. Each card shows the repository artifact path as visible text and links only to local relative targets:

- Single report: `reports/sample-report.html`, with links to [HTML](../reports/sample-report.html), [Markdown](../reports/sample-report.md), and [JSON](../reports/sample-report.json).
- Pre-trade packet: `reports/pretrade-packet.md`, with links to [Markdown](../reports/pretrade-packet.md) and [JSON](../reports/pretrade-packet.json).
- Regime comparison: `reports/regime-comparison.html`, with links to [HTML](../reports/regime-comparison.html), [Markdown](../reports/regime-comparison.md), and [JSON](../reports/regime-comparison.json).
- Fee sensitivity: `reports/fee-sensitivity.md`, with links to [Markdown](../reports/fee-sensitivity.md) and [JSON](../reports/fee-sensitivity.json).
- Split sweep: `reports/sample-sweep-split.html`, with links to [HTML](../reports/sample-sweep-split.html), [Markdown](../reports/sample-sweep-split.md), [JSON](../reports/sample-sweep-split.json), and the [walkthrough](split-sweep-walkthrough.md).
- Manifest: `reports/sample-manifest.md`, with links to [Sample manifest](../reports/sample-manifest.md) and this static demo manifest.

## Demo Artifacts

- [Single backtest HTML](../reports/sample-report.html)
- [Single backtest Markdown](../reports/sample-report.md)
- [Single backtest JSON](../reports/sample-report.json)
- Single backtest interpretation inventory: the Markdown/HTML reports include `## Scenario/Risk Interpretation`, and the JSON report includes `scenario_risk_interpretation`.
- [Pre-trade research packet Markdown](../reports/pretrade-packet.md)
- [Pre-trade research packet JSON](../reports/pretrade-packet.json)
- [Fee sensitivity Markdown](../reports/fee-sensitivity.md)
- [Fee sensitivity JSON](../reports/fee-sensitivity.json)
- [Regime comparison HTML](../reports/regime-comparison.html)
- [Regime comparison Markdown](../reports/regime-comparison.md)
- [Regime comparison JSON](../reports/regime-comparison.json)
- [Parameter sweep HTML](../reports/sample-sweep.html)
- [Parameter sweep Markdown](../reports/sample-sweep.md)
- [Parameter sweep JSON](../reports/sample-sweep.json)
- [Split-sweep HTML](../reports/sample-sweep-split.html)
- [Split-sweep Markdown](../reports/sample-sweep-split.md)
- [Split-sweep JSON](../reports/sample-sweep-split.json)

## Boundaries

These files are research-only review artifacts. They are not investment advice, recommendations, forecasts, live trading signals, or instructions to buy, sell, hold, trade, or size a position.

The bundled leveraged ETF-like sample is synthetic and simplified. Real leveraged ETF products commonly reset exposure daily, so multi-day results are path-dependent and cannot be estimated by multiplying an underlying index's start-to-end return. Leverage can magnify losses quickly, and real products include expenses, financing costs, tracking differences, taxes, liquidity, and market impact that these sample artifacts do not model.

The bundled multi-regime sample is also synthetic and deterministic. Its bull, choppy, and drawdown-recovery labels are fixture scenarios for research review and tests; they are not market classifications, recommendations, forecasts, or a guarantee of future returns.
