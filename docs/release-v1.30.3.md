# v1.30.3 Release Notes

Market Signal Lab v1.30.3 packages the Promotion-Readiness Check increment for public-safe reviewer handoff.

## Start Here

- [Promotion-Readiness Check Guide](promotion-readiness-check.md) - concise reviewer guide for release and promotion gate labels.
- [Promotion-Readiness Check Markdown](../reports/promotion-readiness-check.md) - generated static checklist with evidence checks, PASS review notes, WARN/FAIL next fixes, boundaries, and verification commands.
- [Promotion-Readiness Check JSON](../reports/promotion-readiness-check.json) - structured version of the same documentation-readiness result.
- [Local Audit Commands](local-audit-commands.md) - maintainer command reference for regenerating checked-in review artifacts.

## Changed

- Added the generated Promotion-Readiness Check as a static release/promotion documentation gate for the cross-asset thesis ledger.
- Linked the reviewer guide and generated artifacts from public review surfaces.
- Added concise gate language for benchmark, fee, drawdown, train/test, leveraged-caveat, static-only, and no-advice evidence checks.
- Kept the artifact focused on documentation readiness, not trading readiness or investment validation.

## Verification

```bash
python -m market_signal_lab.cli --promotion-readiness-check
python -m pytest tests/test_promotion_readiness_check.py
python scripts/selfcheck.py
```

For a focused documentation-link check during this increment:

```bash
python - <<'PY'
from scripts.selfcheck import find_markdown_link_issues

issues = find_markdown_link_issues()
if issues:
    print("\n".join(issues))
    raise SystemExit(1)
print("Documentation link check passed.")
PY
```

## Boundaries

The Promotion-Readiness Check is a static research-review artifact only. It does not provide live data, broker/account access, order routing, position sizing, forecasts, recommendations, trading signals, suitability review, or investment advice. A passing gate means expected documentation evidence and boundary language are present; it does not prove profitability, robustness, correctness, or public trading readiness.
