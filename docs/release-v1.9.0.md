# v1.9.0 Release Checklist

## Scope

- Deterministic cross-asset thesis-ledger evidence packet for `QQQ_LIKE`, `QLD_LIKE`, and `TQQQ_LIKE`.
- Checked-in Markdown and JSON artifacts under `reports/cross-asset-thesis-ledger.*`.
- Documentation and static gallery links for the new artifacts.

## Verification

- Run `python scripts/selfcheck.py` from the repository root.
- Confirm `reports/cross-asset-thesis-ledger.md` and `reports/cross-asset-thesis-ledger.json` are regenerated.
- Confirm public artifacts remain research-only and contain no advice, forecasts, live data, broker, or execution workflow.
