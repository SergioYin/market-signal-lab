# Documentation Map

This is the canonical map for Market Signal Lab documentation. The project is a research-only backtesting sandbox; these documents do not provide investment advice, trading recommendations, forecasts, or live execution signals.

## Cold User Route

Use these first if you are opening the project cold:

- [Public static demo](https://sergioyin.github.io/market-signal-lab/) - GitHub Pages entry point for the checked-in local gallery.
- [Static Sample Gallery](../reports/index.html) - browser-openable dashboard for the checked-in artifacts.
- [Visual Acceptance Bundle](../reports/visual-acceptance-bundle.md) - bounded visual acceptance handoff tying the static walkthrough, gallery, visual receipt, acceptance index, scorecard, cold-user route, hashes, and no-live-data/no-advice boundaries together.
- [Static Visual Capture Checklist](../reports/static-visual-capture-checklist.md) - public-safe local screenshot/GIF checklist for the static gallery route.
- [Static Visual Capture Receipt](../reports/static-visual-capture-receipt.md) - deterministic scan of static visual capture evidence paths, hashes, roles, routes, commands, and public evidence notes.
- [Visual Walkthrough Evidence Receipt](../reports/visual-walkthrough-evidence-receipt.md) - deterministic cold-review route tying the static walkthrough SVG, gallery, public demo receipt, rerun receipt, and acceptance index together.
- [Cold-user review route](../reports/cold-user-review-route.md) - first-time public-review route through checked-in static artifacts.

All three routes are static research-review surfaces only. They do not provide investment advice, trading recommendations, forecasts, broker workflows, live data, account access, order routing, or execution signals.

## Start Here

- [README](../README.md) - project overview, quickstart commands, and scope boundaries.
- [Quick-Tour Preview](quick-tour-preview.md) - visual three-minute route from static gallery to evidence card to thesis-ledger acceptance.
- [Three-Minute Review Route](three-minute-review.md) - cold-review route for the static demo, methodology caveats, and one reproducible acceptance command.
- [Local Audit Commands](local-audit-commands.md) - concise local commands for artifact acceptance, selfcheck, release hygiene, and command limits.
- [Public Share Copy](public-share-copy.md) - public-safe one-liners and claim boundaries for sharing the project.
- [Reviewer Decision Tree](reviewer-decision-tree.md) - route reviewers through understanding, reproducibility, methodology-risk, sharing, and promotion-readiness decisions.
- [Reviewer Decision Matrix](reviewer-decision-matrix.md) - explains release vs promotion gates and PASS/WARN/FAIL interpretation for the generated review artifact.
- [Promotion-Readiness Check Guide](promotion-readiness-check.md) - public-safe guide to the generated release/promotion readiness check, evidence labels, boundaries, PASS review notes, and WARN/FAIL next fixes.
- [Promotion-readiness check](../reports/promotion-readiness-check.md) - generated release/promotion gate labels, no-live-data/no-advice boundaries, evidence checks, PASS review notes, and WARN/FAIL next fixes for public sharing review.
- [Architecture](architecture.md) - static-first architecture, CLI artifact pipeline, methodology audit modules, sample reports, test/selfcheck gates, and out-of-scope boundaries.
- [ADR 0001: Static Research Artifacts](adr/0001-static-research-artifacts.md) - maintainer decision record for keeping the project as static research artifacts.
- [Cold Review Checklist](cold-review-checklist.md) - 2-5 minute research-only review path for first-time visitors.
- [Cold User Evidence Card](cold-user-evidence-card.md) - concise reviewer handoff for the checked-in public artifacts, PASS/WARN/FAIL language, and research-only boundaries.
- [Reviewer Acceptance Scorecard Guide](reviewer-acceptance-scorecard.md) - public-safe guide to the scorecard purpose, inputs, outputs, boundaries, and reviewer acceptance criteria.
- [Assumption Ledger Summary Guide](assumption-ledger-summary.md) - concise cold-review workflow for reading the generated assumption summary, evidence paths, risk boundaries, and non-claims.
- [Public Share Summary](public-share-summary.md) - compact public-safe summary of target users, the 60-second demo route, and research-only boundaries.
- [Reviewer FAQ](reviewer-faq.md) - concise answers for cold reviewers about bot scope, live data, validation, leveraged ETF-like examples, and first-open artifacts.
- [Promotion Checklist](promotion-checklist.md) - public-safe gates, evidence items, runnable checks, and copy boundaries before sharing or reusing the repo.
- [Methodology Audit](methodology-audit.md) - reviewer checklist for look-ahead bias, survivorship bias, overfitting, cost assumptions, leveraged ETF daily-reset risk, and no-advice/no-live-trading boundaries.
- [Strategy Assumption Stress Kit Guide](strategy-assumption-stress-kit.md) - reviewer workflow, stress-check limits, and beginner leveraged ETF-like caveats for the generated stress kit.
- [Methodology Audit Review File Schema](methodology-audit-review-schema.md) - JSON schema-like documentation for reviewer-filled audit files, accepted check names, accepted statuses, and CLI validation errors.
- [Evidence Card Walkthrough](evidence-card-walkthrough.svg) - visual local reading path for the evidence-card handoff.
- [Quick-Tour Preview SVG](quick-tour-preview.svg) - static public-safe preview diagram for the cold-review route.
- [Root Landing](../index.html) - GitHub Pages entry point for the local static demo and key docs.
- [Single backtest sample](../reports/sample-report.md) - fastest way to inspect `## Scenario/Risk Interpretation` and the modeled exposure review in the checked-in single backtest report.
- [Static Gallery Walkthrough](static-gallery-walkthrough.svg) - visual public-safe reading path for the static gallery, scenario card, JSON fields, and research-only boundaries.
- [Static Demo Manifest](static-gallery-manifest.md) - Pages-safe gallery contract and local artifact inventory.
- [Single backtest JSON](../reports/sample-report.json) - machine-readable `scenario_risk_interpretation` and `exposure_trade_review` samples for the same research-only run.
- [Pre-trade research packet](../reports/pretrade-packet.md) - assumptions, historical diagnostics, beginner checklist, and risk boundaries generated from the existing single-backtest path.
- [Pre-trade research packet JSON](../reports/pretrade-packet.json) - structured version of the same packet.
- [Scenario card](../reports/scenario-card.md) - compact research-only card for embedding assumptions, key metrics, exposure/fee/drawdown diagnostics, risk labels, and next-review checklist in thesis-ledger or portfolio-review notes.
- [Scenario card JSON](../reports/scenario-card.json) - structured version of the same scenario card.
- [Methodology audit score HTML](../reports/methodology-audit-score.html) - static browser-openable PASS/WARN/FAIL score summary generated from reviewer-entered JSON.
- [Methodology audit review template JSON](../reports/methodology-audit-review-template.json) - blank static reviewer-fillable JSON skeleton generated by `--methodology-audit-review-template`.
- [Cross-asset thesis ledger](../reports/cross-asset-thesis-ledger.md) - deterministic QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE evidence packet generated from the bundled sample CSV by selfcheck.
- [Cross-asset thesis ledger JSON](../reports/cross-asset-thesis-ledger.json) - structured version of the same offline research-only packet.
- [Thesis-ledger 60-second walkthrough](thesis-ledger-60-second-walkthrough.md) - run `python -m market_signal_lab.cli --validate-thesis-ledger` from a fresh checkout, see the local files it reads and writes, and interpret PASS/WARN/FAIL acceptance fields without live data, broker, account, order, forecast, recommendation, or advice workflows.
- [Reviewer evidence bundle](../reports/reviewer-evidence-bundle.md) - compact static handoff tying gallery, thesis-ledger acceptance, verification commands, methodology risks, no-advice boundaries, and the [artifact hash summary](../reports/reviewer-evidence-bundle.md#artifact-hash-summary) together.
- [Reviewer evidence bundle JSON](../reports/reviewer-evidence-bundle.json) - structured version of the same public-safe handoff.
- [Visual acceptance bundle](../reports/visual-acceptance-bundle.md) - bounded public visual acceptance bundle tying the static walkthrough, gallery first screen, visual receipt, acceptance receipt index, reviewer acceptance scorecard, cold-user route, hashes, and no-live-data/no-advice boundaries together.
- [Visual acceptance bundle JSON](../reports/visual-acceptance-bundle.json) - structured version of the same visual acceptance bundle.
- [Static visual capture checklist](../reports/static-visual-capture-checklist.md) - deterministic public-safe checklist for capturing a local static gallery screenshot or GIF without private context, live data, broker/account surfaces, orders, position sizing, forecasts, recommendations, or advice.
- [Static visual capture checklist JSON](../reports/static-visual-capture-checklist.json) - structured version of the same capture checklist.
- [Visual walkthrough evidence receipt](../reports/visual-walkthrough-evidence-receipt.md) - deterministic public visual walkthrough receipt tying `docs/static-gallery-walkthrough.svg`, `reports/index.html`, the public demo evidence receipt, reviewer rerun receipt, and acceptance receipt index into a cold-review route.
- [Visual walkthrough evidence receipt JSON](../reports/visual-walkthrough-evidence-receipt.json) - structured version of the same visual walkthrough receipt.
- [Public demo evidence receipt](../reports/public-demo-evidence-receipt.md) - deterministic public demo receipt for gallery/backtest artifact hashes, fixture provenance paths, and no-live-data/no-advice claims.
- [Public demo evidence receipt JSON](../reports/public-demo-evidence-receipt.json) - structured version of the same public demo receipt.
- [Reviewer rerun receipt](../reports/reviewer-rerun-receipt.md) - deterministic stdlib-only receipt listing public rerun commands, expected artifacts, PASS/WARN checks, and no-live-data/no-advice boundaries.
- [Reviewer rerun receipt JSON](../reports/reviewer-rerun-receipt.json) - structured version of the same rerun receipt.
- [Acceptance receipt index](../reports/acceptance-receipt-index.md) - bounded public index linking the visual walkthrough evidence receipt, public demo evidence receipt, reviewer rerun receipt, reviewer evidence bundle, fixture provenance, artifact hashes, and no-live-data/no-advice boundaries.
- [Acceptance receipt index JSON](../reports/acceptance-receipt-index.json) - structured version of the same receipt index.
- [Reviewer acceptance scorecard guide](reviewer-acceptance-scorecard.md) - explains the generated scorecard purpose, inputs, outputs, boundaries, and reviewer acceptance criteria.
- [Reviewer acceptance scorecard](../reports/reviewer-acceptance-scorecard.md) - deterministic PASS/WARN public-review readiness, reproducibility evidence, risk-boundary, and next-action summary.
- [Reviewer acceptance scorecard JSON](../reports/reviewer-acceptance-scorecard.json) - structured version of the same scorecard.
- [Promotion-readiness check guide](promotion-readiness-check.md) - explains the generated promotion-readiness purpose, inputs, outputs, boundaries, and reviewer acceptance criteria.
- [Strategy assumption stress kit HTML](../reports/strategy-assumption-stress-kit.html) - browser-openable static stress kit for checking strategy assumptions, beginner boundaries, and leveraged ETF-like caveats without live data, broker workflows, forecasts, recommendations, or advice.
- [Strategy assumption stress kit guide](strategy-assumption-stress-kit.md) - concise public guide for reviewer workflow, what stress checks do and do not prove, and beginner leveraged ETF-like caveats.
- [Strategy assumption stress kit Markdown](../reports/strategy-assumption-stress-kit.md) - Markdown version of the same deterministic stress kit, including the release-readiness receipt.
- [Strategy assumption stress kit JSON](../reports/strategy-assumption-stress-kit.json) - structured version of the same deterministic stress kit, including exact rerun commands, generated output paths, and no-live-data/no-advice boundary claims.
- [Stress Kit Quickstart Card](../reports/stress-kit-quickstart-card.md) - deterministic two-minute reviewer checklist distilled from the Strategy Assumption Stress Kit.
- [Stress Kit Quickstart Card JSON](../reports/stress-kit-quickstart-card.json) - structured version of the same quickstart card.
- [Assumption Ledger Summary Guide](assumption-ledger-summary.md) - explains how cold reviewers should use the generated assumption-ledger summary without treating it as advice, forecast, recommendation, or trading-readiness approval.
- [Assumption Ledger Summary](../reports/assumption-ledger-summary.md) - compact static handoff for strategy assumptions, risk boundaries, evidence paths, and explicit non-claims.
- [Assumption Ledger Summary JSON](../reports/assumption-ledger-summary.json) - structured version of the same assumption-ledger summary.
- [Cold-user review route JSON](../reports/cold-user-review-route.json) - structured route, checklist status labels, boundary flags, verification commands, and static artifact integrity summary.
- [Prediction-readiness audit](../reports/prediction-readiness-audit.md) - static documentation-boundary audit with PASS/WARN/FAIL labels for reviewing whether the thesis-ledger artifact keeps historical diagnostics, boundaries, benchmark fields, and caveats visible.
- [Prediction-readiness audit JSON](../reports/prediction-readiness-audit.json) - structured version of the same review-only audit.
- [Promotion-readiness check JSON](../reports/promotion-readiness-check.json) - structured release/promotion gate labels and actionable WARN/FAIL next fixes for public promotion review.
- [Beginner backtest-reading checklist](../reports/beginner-prediction-checklist.md) - static beginner-readable checklist for reading historical backtest and related checklist artifacts without treating them as predictions of future returns, recommendations, or advice.
- [Beginner backtest-reading checklist JSON](../reports/beginner-prediction-checklist.json) - structured version of the same public-safe checklist.
- [Regime comparison sample](../reports/regime-comparison.md) - first artifact to open for the side-by-side synthetic bull/choppy/drawdown-recovery comparison; regenerate it with `market-signal-lab --regime-comparison`.
- [Regime comparison JSON](../reports/regime-comparison.json) - machine-readable version of the same synthetic regime comparison.
- [Regime comparison HTML](../reports/regime-comparison.html) - browser-openable view of the same checked-in artifact.
- [Fee sensitivity sample](../reports/fee-sensitivity.md) - research-only fee assumption comparison for the bundled single backtest.
- [Fee sensitivity JSON](../reports/fee-sensitivity.json) - structured output for the same fee sensitivity artifact.
- [Risk Boundaries](risk-boundaries.md) - public no-advice and no-execution boundaries.
- [Scenario/Risk Glossary](scenario-risk-glossary.md) - beginner definitions for exposure, modeled entry/exit, fee drag, drawdown, and buy-and-hold gap diagnostics.
- [Metric Guide](metric-guide.md) - definitions and caveats for reported metrics.
- [Methodology Audit](methodology-audit.md) - static review checklist for common backtest methodology risks and public-safe scope boundaries.
- [Methodology Audit Review File Schema](methodology-audit-review-schema.md) - reviewer JSON file shape for `--score-methodology-audit`.
- [Split Sweep Walkthrough](split-sweep-walkthrough.md) - beginner reading guide for split-sweep robustness reports.
- [Example Data and Synthetic Data Caveats](example-data.md) - bundled sample-data limits.
- [Data Provenance](data-provenance.md) - how local CSV input and placeholder symbols are handled.

## Regime Comparison Boundary

The regime-comparison artifacts use deterministic synthetic sample data and placeholder regime labels. Run `market-signal-lab --regime-comparison` from the repository root to write `reports/regime-comparison.md`, `reports/regime-comparison.json`, and `reports/regime-comparison.html`. Open the Markdown file first for review. These artifacts are research-only aids for comparing historical diagnostics across fixture scenarios; they are not investment advice, recommendations, forecasts, market classifications, or a guarantee of future returns.

## Workflows

- [Config Files](config-files.md) - JSON config shape, precedence, and repeatable run examples.
- [Architecture](architecture.md) - maintainer overview for the static artifact pipeline and public-safe scope.
- [ADR 0001: Static Research Artifacts](adr/0001-static-research-artifacts.md) - accepted decision record for the static-first boundary.
- [Artifact Gallery](artifact-gallery.md) - checked-in sample report, sweep, split-sweep, manifest, JSON, and HTML artifacts.
- [Public Share Summary](public-share-summary.md) - public-safe summary route for sharing the static artifact workflow.
- [Promotion Checklist](promotion-checklist.md) - pre-share checklist for evidence links, runnable checks, and public copy boundaries.
- [Methodology Audit](methodology-audit.md) - checklist for reviewing sample backtests without treating them as advice, forecasts, or live-trading systems.
- [Strategy Assumption Stress Kit Guide](strategy-assumption-stress-kit.md) - public guide for reviewing assumption stress checks without treating them as robustness proof.
- [Methodology Audit Review File Schema](methodology-audit-review-schema.md) - allowed review-file fields, check order, status values, and scoring output fields.

## Release Notes

- [v1.30.7 Release Notes](release-v1.30.7.md)
- [v1.30.6 Release Notes](release-v1.30.6.md)
- [v1.30.5 Release Notes](release-v1.30.5.md)
- [v1.30.4 Release Notes](release-v1.30.4.md)
- [v1.30.3 Release Notes](release-v1.30.3.md)
- [v1.30.2 Release Notes](release-v1.30.2.md)
- [v1.30.1 Release Notes](release-v1.30.1.md)
- [v1.30.0 Release Notes](release-v1.30.0.md)
- [v1.29.0 Release Notes](release-v1.29.0.md)
- [v1.28.0 Release Notes](release-v1.28.0.md)
- [v1.27.0 Release Notes](release-v1.27.0.md)
- [v1.27.0 Release Notes](release-notes-v1.27.0.md)
- [v1.26.0 Release Notes](release-v1.26.0.md)
- [v1.26.0 Release Docs](release-notes-v1.26.0.md)
- [v1.25.0 Release Notes](release-v1.25.0.md)
- [v1.24.0 Release Notes](release-notes-v1.24.0.md)
- [v1.23.0 Release Notes](release-notes-v1.23.0.md)
- [v1.22.1 Release Notes](release-notes-v1.22.1.md)
- [v1.22.0 Release Notes](release-notes-v1.22.0.md)
- [v1.22.0 Release Checklist](release-v1.22.0.md)
- [v1.21.0 Release Notes](release-notes-v1.21.0.md)
- [v1.21.0 Release Checklist](release-v1.21.0.md)
- [v1.20.4 Release Notes](release-notes-v1.20.4.md)
- [v1.20.4 Release Checklist](release-v1.20.4.md)
- [v1.20.3 Release Notes](release-notes-v1.20.3.md)
- [v1.20.3 Release Checklist](release-v1.20.3.md)
- [v1.20.2 Release Notes](release-notes-v1.20.2.md)
- [v1.20.2 Release Checklist](release-v1.20.2.md)
- [v1.20.1 Release Notes](release-notes-v1.20.1.md)
- [v1.20.1 Release Checklist](release-v1.20.1.md)
- [v1.20.0 Release Notes](release-notes-v1.20.0.md)
- [v1.20.0 Release Checklist](release-v1.20.0.md)
- [v1.19.0 Release Notes](release-notes-v1.19.0.md)
- [v1.19.0 Release Checklist](release-v1.19.0.md)
- [v1.18.0 Release Notes](release-notes-v1.18.0.md)
- [v1.18.0 Release Checklist](release-v1.18.0.md)
- [v1.17.0 Release Notes](release-notes-v1.17.0.md)
- [v1.17.0 Release Checklist](release-v1.17.0.md)
- [v1.16.0 Release Notes](release-notes-v1.16.0.md)
- [v1.16.0 Release Checklist](release-v1.16.0.md)
- [v1.15.0 Release Notes](release-notes-v1.15.0.md)
- [v1.15.0 Release Checklist](release-v1.15.0.md)
- [v1.14.0 Release Notes](release-notes-v1.14.0.md)
- [v1.14.0 Release Checklist](release-v1.14.0.md)
- [v1.13.0 Release Notes](release-notes-v1.13.0.md)
- [v1.13.0 Release Checklist](release-v1.13.0.md)
- [v1.12.0 Release Notes](release-notes-v1.12.0.md)
- [v1.12.0 Release Checklist](release-v1.12.0.md)
- [v1.11.0 Release Notes](release-notes-v1.11.0.md)
- [v1.11.0 Release Checklist](release-v1.11.0.md)
- [v1.10.0 Release Notes](release-notes-v1.10.0.md)
- [v1.10.0 Release Checklist](release-v1.10.0.md)
- [v1.9.1 Release Notes](release-notes-v1.9.1.md)
- [v1.9.1 Release Checklist](release-v1.9.1.md)
- [v1.9.0 Release Notes](release-notes-v1.9.0.md)
- [v1.9.0 Release Checklist](release-v1.9.0.md)
- [v1.8.0 Release Notes](release-notes-v1.8.0.md)
- [v1.8.0 Release Checklist](release-v1.8.0.md)
- [v1.7.0 Release Notes](release-notes-v1.7.0.md)
- [v1.7.0 Release Checklist](release-v1.7.0.md)
- [v1.6.0 Release Notes](release-notes-v1.6.0.md)
- [v1.6.0 Release Checklist](release-v1.6.0.md)
- [v1.5.0 Release Notes](release-notes-v1.5.0.md)
- [v1.5.0 Release Checklist](release-v1.5.0.md)
- [v1.4.0 Release Notes](release-notes-v1.4.0.md)
- [v1.4.0 Release Checklist](release-v1.4.0.md)
- [v1.3.5 Release Notes](release-notes-v1.3.5.md)
- [v1.3.5 Release Checklist](release-v1.3.5.md)
- [v1.3.4 Release Notes](release-notes-v1.3.4.md)
- [v1.3.4 Release Checklist](release-v1.3.4.md)
- [v1.3.3 Release Notes](release-notes-v1.3.3.md)
- [v1.3.3 Release Checklist](release-v1.3.3.md)
- [v1.3.2 Release Notes](release-notes-v1.3.2.md)
- [v1.3.2 Release Checklist](release-v1.3.2.md)
- [v1.3.1 Release Notes](release-notes-v1.3.1.md)
- [v1.3.1 Release Checklist](release-v1.3.1.md)
- [v1.3.0 Release Notes](release-notes-v1.3.0.md)
- [v1.3.0 Release Checklist](release-v1.3.0.md)
- [v1.2.1 Release Notes](release-notes-v1.2.1.md)
- [v1.2.1 Release Checklist](release-v1.2.1.md)
- [v1.2.0 Release Notes](release-notes-v1.2.0.md)
- [v1.2.0 Release Checklist](release-v1.2.0.md)
- [v1.1.0 Release Notes](release-notes-v1.1.0.md)
- [v1.1.0 Release Checklist](release-v1.1.0.md)
- [v1.0.0 Release Notes](release-notes-v1.0.0.md)
- [v1.0.0 Release Checklist](release-v1.0.0.md)
- [v0.9.0 Release Notes](release-notes-v0.9.0.md)
- [v0.9.0 Release Checklist](release-v0.9.0.md)
- [v0.8.0 Release Notes](release-notes-v0.8.0.md)
- [v0.8.0 Release Checklist](release-v0.8.0.md)
- [v0.7.0 Release Notes](release-notes-v0.7.0.md)
- [v0.7.0 Release Checklist](release-v0.7.0.md)
- [v0.6.0 Release Notes](release-notes-v0.6.0.md)
- [v0.6.0 Release Checklist](release-v0.6.0.md)
- [v0.5.0 Release Notes](release-notes-v0.5.0.md)
- [v0.5.0 Release Checklist](release-v0.5.0.md)
- [v0.4.0 Release Notes](release-notes-v0.4.0.md)
- [v0.4.0 Release Checklist](release-v0.4.0.md)
- [v0.3.0 Release Notes](release-notes-v0.3.0.md)
- [v0.3.0 Release Checklist](release-v0.3.0.md)
