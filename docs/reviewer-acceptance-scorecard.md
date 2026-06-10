# Reviewer Acceptance Scorecard Guide

Concise guide for the generated reviewer acceptance scorecard. This page is public-safe and research-only. It does not provide investment advice, trading recommendations, forecasts, live signals, broker guidance, account setup steps, order instructions, or instructions to buy, sell, hold, or trade.

## Purpose

The reviewer acceptance scorecard summarizes whether the checked-in public review artifacts are ready for research-only handoff. It focuses on artifact readability, reproducibility evidence, visible risk boundaries, and next review actions.

Use it as a reviewer orientation aid, not as approval of strategy quality, profitability, future robustness, suitability, or financial correctness.

## Inputs

- Static checked-in Markdown, JSON, and HTML artifacts under `reports/`.
- Public documentation boundaries under `docs/`, including methodology and risk-boundary pages.
- Deterministic scorecard definitions used by `python -m market_signal_lab.cli --reviewer-acceptance-scorecard`.
- Local artifact paths only; the scorecard does not fetch market data or call external services.

## Outputs

- [Reviewer acceptance scorecard Markdown](../reports/reviewer-acceptance-scorecard.md).
- [Reviewer acceptance scorecard JSON](../reports/reviewer-acceptance-scorecard.json).
- An overall `PASS`, `WARN`, or `FAIL`-style label for reviewer handoff.
- Category labels for public-review readiness, reproducibility evidence, risk boundaries, and next actions.
- Evidence paths, review notes, boundary flags, and verification commands.

## Boundaries

- The scorecard covers static historical research diagnostics only.
- It does not use live market data, broker or account access, order routing, or position sizing.
- It does not forecast returns, recommend trades, validate investment suitability, or provide investment advice.
- A passing category means the expected public-review evidence and boundary language are present; it does not mean the underlying research is profitable, robust, complete, or correct.
- `WARN` items are reviewer follow-up prompts, not trading risk ratings or investment conclusions.

## Reviewer Acceptance Criteria

A reviewer can treat the scorecard as acceptable for public research handoff when:

1. The Markdown and JSON outputs are present at the default paths.
2. The overall label and category labels are visible and easy to compare.
3. Each category lists concrete evidence paths that exist in the repository.
4. Risk-boundary flags keep the artifact static-only, research-only, historical-diagnostics-only, no-live-data, no-broker, no-orders, no-recommendations, and not-investment-advice.
5. Next actions tell reviewers to regenerate artifacts, inspect diffs, rerun thesis-ledger acceptance, and run focused tests before citation.
6. The language stays public-safe and avoids promises about performance, future returns, trading readiness, suitability, or advice.

Regenerate the scorecard with:

```bash
python -m market_signal_lab.cli --reviewer-acceptance-scorecard
```

Then inspect the generated diff before citing it:

```bash
git diff -- reports/reviewer-acceptance-scorecard.md reports/reviewer-acceptance-scorecard.json
```
