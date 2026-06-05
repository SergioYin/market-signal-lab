# v1.22.0 Release Checklist

Release v1.22.0 packages the beginner backtest-reading checklist increment.

## Readiness

- Package metadata and CLI version report `1.22.0`.
- `--beginner-prediction-checklist` writes `reports/beginner-prediction-checklist.md` and `reports/beginner-prediction-checklist.json` by default.
- The checklist is deterministic, zero-dependency, beginner-readable, and static.
- Public reviewers get a clear star/reuse reason: the artifact is a deterministic static review template for checking whether backtest writeups keep historical results separate from future-return predictions, recommendations, trading instructions, and investment advice.
- The checklist preserves historical-only, no-live-data, no-broker/account/order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries.
- Leveraged ETF daily-reset/path-dependency risk language is included in Markdown and JSON.
- README, docs map, root landing, static gallery, selfcheck, and tests reference the new artifacts.

## Verification

```bash
python -m pip install -e ".[test]"
python -m market_signal_lab.cli --version
python -m market_signal_lab.cli --beginner-prediction-checklist
python -m pytest
python scripts/selfcheck.py
```

See [v1.22.0 Release Notes](release-notes-v1.22.0.md).
