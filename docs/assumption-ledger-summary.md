# Assumption Ledger Summary Guide

The assumption ledger summary is a compact cold-review entry point for the generated static artifacts at [`reports/assumption-ledger-summary.md`](../reports/assumption-ledger-summary.md) and [`reports/assumption-ledger-summary.json`](../reports/assumption-ledger-summary.json).

Use it to identify what assumptions the sample artifacts expose, where supporting evidence lives, and which claims are explicitly out of scope. It is a research-review guide only. It does not provide investment advice, trading recommendations, forecasts, live market data, broker/account workflows, order routing, position sizing, or execution signals.

## Cold Review Flow

1. Open [`reports/assumption-ledger-summary.md`](../reports/assumption-ledger-summary.md) before the larger stress kit.
2. Read the strategy assumptions as review prompts, not as validated truths or instructions to act.
3. Check each evidence path against the linked static artifact, especially the gallery, stress kit, quickstart card, and reviewer evidence bundle.
4. Compare the risk boundaries and non-claims with the README and documentation map before quoting the project publicly.
5. Use the JSON only when you need deterministic field names for automation or diff review.

## What To Verify

- The summary names assumptions, evidence paths, risk boundaries, and non-claims without implying future performance.
- The evidence paths resolve to checked-in static files and do not require live data, accounts, brokers, or network access.
- Boundary flags remain consistent with the rest of the project: research-only, static-only, no recommendations, no forecasts, and no investment advice.
- Any public mention describes the summary as a reviewer handoff, not as a model approval, trading-readiness score, or suitability review.

## Regeneration

Regenerate the checked-in summary with:

```bash
python -m market_signal_lab.cli --assumption-ledger-summary
```

Then inspect the generated Markdown and JSON diff:

```bash
git diff -- reports/assumption-ledger-summary.md reports/assumption-ledger-summary.json
```

Do not treat a clean regeneration or matching JSON schema as evidence that any strategy is correct, profitable, suitable, or safe to trade.
