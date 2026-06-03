# Reviewer Decision Tree

Use this decision tree to review Market Signal Lab as a static research-artifact package. It is not a live trading system and does not produce investment advice.

## 1. Do you only want to understand the project?

Start with [Three-Minute Review Route](three-minute-review.md), then open the static demo. Stop there if you only need a cold-read impression.

## 2. Do you want to verify reproducibility?

Run the commands in [Local Audit Commands](local-audit-commands.md): version, thesis-ledger acceptance, selfcheck, compileall, and diff hygiene.

## 3. Do you want to evaluate methodology risk?

Read [Methodology Audit](methodology-audit.md), [Risk Boundaries](risk-boundaries.md), and the generated methodology-audit template. Focus on assumptions, sample-data status, costs, path-dependency caveats, and look-ahead/survivorship limits.

## 4. Do you want to share the project publicly?

Use [Public Share Copy](public-share-copy.md). Avoid claiming that sample outputs are profitable strategies, forecasts, live signals, or recommendations.

## 5. Promotion decision

Promote only if the reviewer can answer yes to all four questions:

- Is the repo purpose understandable without a private explanation?
- Can the static demo and local audit route be verified from a fresh checkout?
- Are research-only and no-advice boundaries visible before any sample return output?
- Is there a concrete reuse reason beyond the existence of a small tool?
