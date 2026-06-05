# v1.22.1 Release Notes

Market Signal Lab v1.22.1 is an audit-driven patch for the static demo and installed-package review path. It keeps the project research-only and does not add live data, broker/account/order workflows, position sizing, forecasts, recommendations, or investment advice.

## Fixed

- Wheel-installed demo routes now work from an empty current working directory by reading bundled static resources for `--validate-thesis-ledger` and `--regime-comparison`.
- Added wheel smoke coverage for empty-cwd console-script usage, including the beginner checklist, thesis-ledger validation, and regime-comparison demo routes.

## Changed

- Reworked the static gallery landing into a simpler three-CTA first screen: view the sample report, open the beginner backtest checklist, or run one verification command.
- Tightened beginner-risk wording across the README and landing copy so backtest outputs are framed as historical diagnostics, not predictions, recommendations, action instructions, or advice.
- Package metadata and CLI version output identify this audit-driven patch as `1.22.1`.

## Verification Commands

```bash
python -m pip install -e ".[test]"
python -m pytest
python scripts/selfcheck.py
git diff --check
```

Wheel empty-cwd smoke coverage is exercised by:

```bash
python -m pytest tests/test_packaging.py
```

Routine `python scripts/selfcheck.py` excludes that wheel smoke so local selfcheck
does not spend extra time creating venvs, building a wheel, and reinstalling it.

## Release Gate Note

Before tagging v1.22.1, the release gate is a clean `python -m pytest`, a clean `python scripts/selfcheck.py`, a clean `git diff --check`, and explicit wheel-installed empty-cwd coverage via `python -m pytest tests/test_packaging.py -m wheel_smoke`; the expected result is that version metadata reports `1.22.1`, bundled static resources are included in the wheel, `market-signal-lab --validate-thesis-ledger` and `market-signal-lab --regime-comparison` run from an empty current directory, generated/static gallery links remain local, and public copy preserves the research-only/no-live-data/no-broker/no-account/no-order/no-position-sizing/no-forecast/no-recommendation/no-investment-advice boundaries.
