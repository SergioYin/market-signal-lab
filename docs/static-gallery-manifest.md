# Static Demo Manifest

This manifest defines the public static demo surface for Market Signal Lab v1.20.0. It exists so a cold reviewer can open one first screen, follow local links, and verify the artifact trail without installing the package.

Start at the [Root Landing](../index.html), then open the [Static Sample Gallery](../reports/index.html). Both are plain HTML pages with no JavaScript, no remote assets, no live market data calls, no broker connection, and no account flow. Every link is repository-local and relative, so the same files can be opened from a checkout or served from a static host such as GitHub Pages.

## First-Screen Links

- [Root landing](../index.html)
- [Three-minute review route](three-minute-review.md)
- [Cold review checklist](cold-review-checklist.md)
- [Cold user evidence card](cold-user-evidence-card.md)
- [Public share summary](public-share-summary.md)
- [Reviewer FAQ](reviewer-faq.md)
- [Promotion checklist](promotion-checklist.md)
- [Architecture](architecture.md)
- [ADR 0001: Static Research Artifacts](adr/0001-static-research-artifacts.md)
- [Methodology audit](methodology-audit.md)
- [Methodology audit review file schema](methodology-audit-review-schema.md)
- [Evidence card walkthrough](evidence-card-walkthrough.svg)
- [Static gallery entry page](../reports/index.html)
- [Static gallery walkthrough](static-gallery-walkthrough.svg)
- [Static demo manifest](static-gallery-manifest.md)
- [Artifact gallery notes](artifact-gallery.md)
- [Split-sweep walkthrough](split-sweep-walkthrough.md)
- [Sample manifest](../reports/sample-manifest.md)

## Dashboard Cards

The checked-in [Static Sample Gallery](../reports/index.html) starts with a compact no-JavaScript dashboard. Each card shows the repository artifact path as visible text and links only to local relative targets:

- Single report: `reports/sample-report.html`, with links to [HTML](../reports/sample-report.html), [Markdown](../reports/sample-report.md), and [JSON](../reports/sample-report.json).
- Pre-trade packet: `reports/pretrade-packet.md`, with links to [Markdown](../reports/pretrade-packet.md) and [JSON](../reports/pretrade-packet.json).
- Scenario card: `reports/scenario-card.md`, with links to [Markdown](../reports/scenario-card.md) and [JSON](../reports/scenario-card.json).
- Methodology audit score: `reports/methodology-audit-score.html`, with links to [HTML](../reports/methodology-audit-score.html), [Markdown](../reports/methodology-audit-score.md), and [JSON](../reports/methodology-audit-score.json).
- Cross-asset thesis ledger: `reports/cross-asset-thesis-ledger.md`, with links to [Markdown](../reports/cross-asset-thesis-ledger.md) and [JSON](../reports/cross-asset-thesis-ledger.json).
- Regime comparison: `reports/regime-comparison.html`, with links to [HTML](../reports/regime-comparison.html), [Markdown](../reports/regime-comparison.md), and [JSON](../reports/regime-comparison.json).
- Fee sensitivity: `reports/fee-sensitivity.md`, with links to [Markdown](../reports/fee-sensitivity.md) and [JSON](../reports/fee-sensitivity.json).
- Split sweep: `reports/sample-sweep-split.html`, with links to [HTML](../reports/sample-sweep-split.html), [Markdown](../reports/sample-sweep-split.md), [JSON](../reports/sample-sweep-split.json), and the [walkthrough](split-sweep-walkthrough.md).
- Manifest: `reports/sample-manifest.md`, with links to [Sample manifest](../reports/sample-manifest.md) and this static demo manifest.

## Pages-Safe Artifact Inventory

The Pages-safe artifact inventory uses repository-relative links only. The checked-in SVG walkthroughs are static SVG files with no external assets or scripts.

- [Single backtest HTML](../reports/sample-report.html)
- [Single backtest Markdown](../reports/sample-report.md)
- [Single backtest JSON](../reports/sample-report.json)
- Single backtest interpretation inventory: the Markdown/HTML reports include `## Scenario/Risk Interpretation`, and the JSON report includes `scenario_risk_interpretation`.
- [Pre-trade research packet Markdown](../reports/pretrade-packet.md)
- [Pre-trade research packet JSON](../reports/pretrade-packet.json)
- [Scenario card Markdown](../reports/scenario-card.md)
- [Scenario card JSON](../reports/scenario-card.json)
- [Methodology audit template Markdown](../reports/methodology-audit-template.md)
- [Methodology audit template JSON](../reports/methodology-audit-template.json)
- [Methodology audit review template JSON](../reports/methodology-audit-review-template.json)
- [Example methodology audit score Markdown](../reports/methodology-audit-score.md)
- [Example methodology audit score JSON](../reports/methodology-audit-score.json)
- [Example methodology audit score HTML](../reports/methodology-audit-score.html)
- [Cross-asset thesis ledger Markdown](../reports/cross-asset-thesis-ledger.md)
- [Cross-asset thesis ledger JSON](../reports/cross-asset-thesis-ledger.json)
- [Thesis-ledger acceptance Markdown](../reports/cross-asset-thesis-ledger-acceptance.md)
- [Thesis-ledger acceptance JSON](../reports/cross-asset-thesis-ledger-acceptance.json)
- [Three-minute review route](three-minute-review.md)
- [Cold user evidence card](cold-user-evidence-card.md)
- [Public share summary](public-share-summary.md)
- [Reviewer FAQ](reviewer-faq.md)
- [Promotion checklist](promotion-checklist.md)
- [Architecture](architecture.md)
- [ADR 0001: Static Research Artifacts](adr/0001-static-research-artifacts.md)
- [Methodology audit](methodology-audit.md)
- [Methodology audit review file schema](methodology-audit-review-schema.md)
- [Evidence card walkthrough SVG](evidence-card-walkthrough.svg)
- [Static gallery walkthrough SVG](static-gallery-walkthrough.svg)
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

The public share summary, reviewer FAQ, and promotion checklist are static documentation artifacts only. They add no JavaScript, no live data access, no broker workflow, no account workflow, and no order workflow.

The architecture overview and ADR document the same static-first boundary for maintainers. They add no runtime behavior, JavaScript, external assets, live data, broker or account workflow, orders, position sizing, recommendations, forecasts, or investment advice.

The methodology audit, methodology audit review file schema, generated methodology audit template, blank methodology audit review JSON skeleton, and example methodology audit score are also static reviewer artifacts only. They help reviewers check for common sample-backtest presentation risks such as look-ahead bias, survivorship bias, overfitting, cost omissions, leveraged ETF-like daily reset risk, and no-advice/no-live-trading boundaries; they do not read CSV market data, certify a strategy, or add execution functionality.

The bundled leveraged ETF-like sample is synthetic and simplified. Real leveraged ETF products commonly reset exposure daily, so multi-day results are path-dependent and cannot be estimated by multiplying an underlying index's start-to-end return. Leverage can magnify losses quickly, and real products include expenses, financing costs, tracking differences, taxes, liquidity, and market impact that these sample artifacts do not model.

The bundled multi-regime sample is also synthetic and deterministic. Its bull, choppy, and drawdown-recovery labels are fixture scenarios for research review and tests; they are not market classifications, recommendations, forecasts, or a guarantee of future returns.
