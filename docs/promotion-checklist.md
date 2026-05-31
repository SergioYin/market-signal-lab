# Promotion Checklist

Use this public-safe checklist before sharing, starring, or reusing Market Signal Lab. The goal is to decide whether the repository is useful as a reproducible research-artifact example, not whether any strategy is profitable, suitable, or predictive.

This checklist is not investment advice, trading guidance, a forecast, a recommendation to buy, sell, hold, or trade, or a review of real fund suitability.

## Decision Gates

Share the repo only if these gates are true:

1. The thing being promoted is the artifact workflow: Markdown, JSON, HTML, manifest, scenario-card, thesis-ledger, and acceptance outputs that can be inspected and rerun.
2. The public surface is static and reviewable. Start with the [Static Sample Gallery](../reports/index.html), [Static Demo Manifest](static-gallery-manifest.md), and [Public Share Summary](public-share-summary.md).
3. The evidence path is visible before any performance claim. Use the [Cold User Evidence Card](cold-user-evidence-card.md), [Cold Review Checklist](cold-review-checklist.md), and [Artifact Gallery](artifact-gallery.md).
4. Sample data limits are stated plainly. Confirm the [Data Provenance](data-provenance.md) and [Example Data and Synthetic Data Caveats](example-data.md) describe the bundled fixtures as synthetic/static review inputs.
5. Risk boundaries are prominent. Link the [Risk Boundaries](risk-boundaries.md), [Scenario/Risk Glossary](scenario-risk-glossary.md), and [Metric Guide](metric-guide.md) when mentioning diagnostics.

Do not share, star, or reuse it as a trading signal service, investment recommendation, live-data tool, broker workflow, account workflow, order workflow, position-sizing workflow, forecast engine, or proof of future returns.

## Evidence Items

Before promotion, inspect these checked-in artifacts:

1. [README](../README.md): confirms the project scope, quickstart commands, static demo route, and research-only caveats.
2. [Single backtest report](../reports/sample-report.md): shows assumptions, date range, metrics, caveats, scenario/risk interpretation, and modeled exposure review.
3. [Single backtest JSON](../reports/sample-report.json): exposes the same run metadata, `scenario_risk_interpretation`, and `exposure_trade_review` in structured form.
4. [Scenario card](../reports/scenario-card.md): provides the compact public-safe assumptions, key metrics, diagnostics, risk labels, and next-review checklist.
5. [Pre-trade research packet](../reports/pretrade-packet.md): gathers assumptions, historical diagnostics, beginner checklist, and explicit risk boundaries without adding execution behavior.
6. [Cross-asset thesis ledger](../reports/cross-asset-thesis-ledger.md): demonstrates a deterministic offline evidence packet across placeholder assets.
7. [Thesis-ledger acceptance summary](../reports/cross-asset-thesis-ledger-acceptance.md): shows PASS/WARN/FAIL review language for packet shape and public boundary checks.
8. [Methodology audit score](../reports/methodology-audit-score.md): shows reviewer-entered PASS/WARN/FAIL counts and a promotion gate suggestion for static methodology review.
9. [Fee sensitivity sample](../reports/fee-sensitivity.md): shows fee-assumption diagnostics for the bundled single-backtest settings.
10. [Regime comparison sample](../reports/regime-comparison.md): compares synthetic fixture scenarios side by side.
11. [Split sweep sample](../reports/sample-sweep-split.md): shows train/test rank, return-gap, and robustness-label diagnostics inside the tiny fixture.
12. [Sample manifest](../reports/sample-manifest.md): records input path, output paths, configuration, fixture provenance, and `research_only` metadata.

Evidence is sufficient for public promotion when a reader can move from a claim to a checked-in artifact, then to a matching JSON or manifest record, without relying on live services or private context.

## Runnable Checks

Run these from the repository root before promoting a fresh checkout:

```bash
python -m market_signal_lab.cli --version
python scripts/selfcheck.py
python -m pytest
```

For targeted artifact regeneration, use the documented workflows:

```bash
python -m market_signal_lab.cli --config examples/configs/single-backtest-report.json
python -m market_signal_lab.cli --regime-comparison
python -m market_signal_lab.cli --validate-thesis-ledger
```

Treat a passing run as evidence that the package, docs links, and checked-in sample artifact workflow are internally consistent. Do not treat it as evidence of strategy quality, market robustness, future performance, or investment suitability.
These checks support release safety; promotion readiness still depends on the decision gates, evidence items, and public copy boundary above.

## Public Copy Boundary

Acceptable public wording:

- "Research-only artifact workflow for reproducible market-signal review."
- "Static sample reports with visible assumptions, JSON outputs, manifests, and caveats."
- "Useful pattern for packaging historical diagnostics and public-safe review evidence."
- "Checked-in synthetic fixtures and offline sample artifacts for inspection."

Avoid public wording that implies:

- Buy, sell, hold, trade, or position-sizing instructions.
- Forecasts, alpha claims, profitability claims, or evidence of future returns.
- Live market data, broker connectivity, account access, order routing, or execution.
- Real QQQ, QLD, or TQQQ performance, suitability, or fund-mechanics modeling.
- Validation, certification, endorsement, or compliance review beyond the repository's own acceptance checks.

## Reuse Boundary

Reuse is reasonable when the target project needs a small example of:

- Pairing human-readable Markdown with machine-readable JSON.
- Keeping static public demos free of JavaScript, remote assets, live data calls, and account flows.
- Recording run assumptions and artifact paths in manifests.
- Making synthetic fixture provenance and non-advice labels visible.
- Using tests and selfcheck scripts to keep docs, reports, and public claims aligned.

Reuse is not reasonable when the target project needs production trading infrastructure, broker integrations, licensed data feeds, portfolio recommendations, personalized advice, execution routing, tax modeling, compliance approval, or real fund behavior estimates.

## Stop Conditions

Stop promotion if any shared message makes the repo sound like a signal to act in the market. Stop promotion if a reader would need to infer whether the data is real, whether the outputs are advice, or whether the demo can trade. Stop promotion if the linked artifacts, runnable checks, and risk docs are not included near the claim being shared.
