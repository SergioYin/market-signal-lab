# Local Audit Commands

Use these commands when reviewing Market Signal Lab from a fresh checkout. They are local, deterministic checks for the checked-in research artifacts. They do not fetch live market data, connect to brokers, inspect accounts, route orders, size positions, recommend trades, forecast returns, or provide investment advice.

## Fast artifact acceptance

```bash
python -m market_signal_lab.cli --validate-thesis-ledger
```

This validates `reports/cross-asset-thesis-ledger.json` and writes Markdown/JSON acceptance artifacts. PASS/WARN/FAIL labels describe research-boundary and artifact-shape checks only; they do not certify a strategy.

## Full project selfcheck

```bash
python scripts/selfcheck.py
```

The selfcheck compiles Python files, runs pytest, regenerates deterministic sample artifacts, checks docs/gallery links, checks static demo acceptance links, scans public claims for advice-like wording, and verifies fixture provenance metadata.

## Release hygiene commands

```bash
python -m compileall market_signal_lab tests scripts
git diff --check
```

Before publishing a public release, also run the repository privacy scan from the release checklist and confirm there are no private paths, agent deployment names, chat-platform names, local usernames, tokens, or key material.

## What these commands do not prove

These commands prove packaging and boundary hygiene for a static sample project. They do not prove that any moving-average rule will work in future markets, that leveraged ETF-like exposure is suitable for a user, or that a trade should be placed.
