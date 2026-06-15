# Promotion-Readiness Check Guide

Concise guide for the generated Promotion-Readiness Check. This page is public-safe and research-only. It does not provide investment advice, trading recommendations, forecasts, live signals, broker guidance, account setup steps, order instructions, or instructions to buy, sell, hold, or trade.

## Purpose

The Promotion-Readiness Check summarizes whether the checked-in cross-asset thesis ledger has enough public-facing evidence and boundary language for broader public references. It separates two static documentation gates:

- **Release Gate**: whether the artifact can be shared for public research review.
- **Promotion Gate**: whether the artifact has enough visible evidence and boundary wording for broader public citation.

Use it as a documentation-readiness aid, not as approval of strategy quality, profitability, future robustness, suitability, or financial correctness.

## Inputs

- Static checked-in thesis-ledger JSON at `reports/cross-asset-thesis-ledger.json`.
- Boundary flags and evidence fields already present in the generated ledger.
- Deterministic check definitions used by `python -m market_signal_lab.cli --promotion-readiness-check`.
- Local artifact paths only; the check does not fetch market data or call external services.
- Custom ledger inputs record `source_content_sha256`, a SHA-256 of the loaded JSON content, so same-named files such as `ledger.json` remain distinguishable without exposing absolute paths.

## Outputs

- [Promotion-readiness check Markdown](../reports/promotion-readiness-check.md).
- [Promotion-readiness check JSON](../reports/promotion-readiness-check.json).
- Release Gate and Promotion Gate labels using `PASS`, `WARN`, or `FAIL`.
- Evidence checks for static/no-live-data boundaries, no-advice wording, benchmark evidence, fee evidence, drawdown evidence, train/test evidence, and leveraged ETF-like caveats.
- `source_artifact` plus `source_content_sha256` provenance; the default source artifact remains repo-relative.
- PASS review notes, actionable next fixes for WARN/FAIL items, public boundaries, and verification commands.

## Reviewer Example

When reading the generated [Markdown](../reports/promotion-readiness-check.md) or [JSON](../reports/promotion-readiness-check.json), treat labels as documentation-readiness markers:

- `PASS`: expected public-boundary evidence is visible.
- `WARN`: public review/release can continue, but broader promotion or citation stays on hold until resolved or explicitly disclosed.
- `FAIL`: hold broader public citation until the next fix is addressed.

These labels do not rank strategies, forecast outcomes, or provide trading advice.

## Boundaries

- The check covers static historical research diagnostics only.
- It does not use live market data, broker or account access, order routing, or position sizing.
- It does not forecast returns, recommend trades, validate investment suitability, or provide investment advice.
- A passing check means expected documentation evidence and boundary language are present; it does not mean the underlying research is profitable, robust, complete, or correct.
- `WARN` items are documentation follow-up prompts, not trading risk ratings or investment conclusions.

## Reviewer Acceptance Criteria

A reviewer can treat the Promotion-Readiness Check as acceptable for public research review when:

1. The Markdown and JSON outputs are present at the default paths.
2. Release Gate and Promotion Gate labels are visible and easy to compare.
3. Each check lists concrete evidence; PASS rows show a neutral no-fix/keep-evidence-visible note, and WARN/FAIL rows list the next fix.
4. The JSON includes a lowercase 64-character `source_content_sha256` for the loaded ledger content without leaking an absolute input path.
5. Public-boundary flags keep the artifact static-only, research-only, historical-diagnostics-only, no-live-data, no-broker, no-orders, no-recommendations, and not-investment-advice.
6. Any `WARN` or `FAIL` item remains visible, with broader public promotion or citation held until it is resolved or explicitly disclosed.
7. The language stays public-safe and avoids promises about performance, future returns, trading readiness, suitability, or advice.

Regenerate the check with:

```bash
python -m market_signal_lab.cli --promotion-readiness-check
```

Then inspect the generated diff before citing it:

```bash
git diff -- reports/promotion-readiness-check.md reports/promotion-readiness-check.json
```
