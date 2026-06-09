# Reviewer Rerun Receipt

Give public reviewers a compact deterministic receipt containing the exact rerun commands, expected artifacts, review boundaries, and PASS/WARN checks for public reproducibility review.

## Start Here

- Open the [public static demo](https://sergioyin.github.io/market-signal-lab/) or the local [static sample gallery](index.html), then use the Reviewer Rerun Receipt card.
- Run commands from the repository root after normal Python setup.
- This receipt is static; it lists commands and expected outputs but does not execute them.
- Success means the command exits 0 and the listed expected artifacts are present or updated.
- PASS means a static receipt claim about declared boundaries or artifact paths, not proof that a command has run.

## Public Verification Commands

- `python -m market_signal_lab.cli --reviewer-rerun-receipt`
  - Purpose: Regenerate this reviewer rerun receipt from stdlib-only code.
  - Expected artifacts: `reports/reviewer-rerun-receipt.md`, `reports/reviewer-rerun-receipt.json`
- `python -m market_signal_lab.cli --reviewer-evidence-bundle`
  - Purpose: Regenerate the cold-review evidence bundle and boundary flags.
  - Expected artifacts: `reports/reviewer-evidence-bundle.md`, `reports/reviewer-evidence-bundle.json`
- `python -m market_signal_lab.cli --cold-user-review-route`
  - Purpose: Regenerate the first-time public review route and integrity summary.
  - Expected artifacts: `reports/cold-user-review-route.md`, `reports/cold-user-review-route.json`
- `python -m market_signal_lab.cli --prediction-readiness-audit`
  - Purpose: Regenerate the static thesis-ledger prediction-readiness boundary audit.
  - Expected artifacts: `reports/prediction-readiness-audit.md`, `reports/prediction-readiness-audit.json`
- `python -m market_signal_lab.cli --validate-thesis-ledger`
  - Purpose: Regenerate the thesis-ledger acceptance summary from checked-in JSON.
  - Expected artifacts: `reports/cross-asset-thesis-ledger-acceptance.md`, `reports/cross-asset-thesis-ledger-acceptance.json`
- `python scripts/selfcheck.py`
  - Purpose: Regenerate and validate the full checked-in sample artifact set used by repository reviewers.
  - Expected artifacts: `checked-in sample artifacts declared by scripts/selfcheck.py::SAMPLE_ARTIFACTS`
- `python -m pytest`
  - Purpose: Run the repository test suite for reproducibility.
  - Expected artifacts: none

## Expected Artifacts

- `reports/reviewer-rerun-receipt.md` (markdown), from `python -m market_signal_lab.cli --reviewer-rerun-receipt`
- `reports/reviewer-rerun-receipt.json` (json), from `python -m market_signal_lab.cli --reviewer-rerun-receipt`
- `reports/reviewer-evidence-bundle.md` (markdown), from `python -m market_signal_lab.cli --reviewer-evidence-bundle`
- `reports/reviewer-evidence-bundle.json` (json), from `python -m market_signal_lab.cli --reviewer-evidence-bundle`
- `reports/cold-user-review-route.md` (markdown), from `python -m market_signal_lab.cli --cold-user-review-route`
- `reports/cold-user-review-route.json` (json), from `python -m market_signal_lab.cli --cold-user-review-route`
- `reports/prediction-readiness-audit.md` (markdown), from `python -m market_signal_lab.cli --prediction-readiness-audit`
- `reports/prediction-readiness-audit.json` (json), from `python -m market_signal_lab.cli --prediction-readiness-audit`
- `reports/cross-asset-thesis-ledger-acceptance.md` (markdown), from `python -m market_signal_lab.cli --validate-thesis-ledger`
- `reports/cross-asset-thesis-ledger-acceptance.json` (json), from `python -m market_signal_lab.cli --validate-thesis-ledger`

## PASS/WARN Checklist

- **PASS**: Receipt generation is deterministic - The receipt is built from fixed stdlib-only constants and does not read market data; PASS is a static receipt claim, not evidence that commands were executed.
- **PASS**: Public verification commands are explicit - Commands are listed exactly as reviewers can run them from the repository root after normal Python setup.
- **PASS**: No live-data or advice workflow is included - The receipt declares no live data, broker, account, order, position-sizing, forecast, recommendation, or investment-advice scope.
- **WARN**: Environment-dependent checks still need local execution - Self-check and pytest results depend on the current Python environment and are not claimed by this static receipt.

## No-Live-Data / No-Advice Boundaries

- This receipt lists public rerun commands only; it does not execute them.
- Run commands from the repository root after normal Python setup.
- A command rerun succeeds only when the command exits 0 and the listed expected artifacts are present or updated.
- No command fetches live market data, connects to brokers, inspects accounts, routes orders, sizes positions, forecasts returns, recommends trades, or provides investment advice.
- PASS means the static receipt claims the boundary or expected artifact is declared; WARN means the reviewer should still run the command locally.

## Boundary Flags

- research_only: `True`
- static_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
- not_investment_advice: `True`
