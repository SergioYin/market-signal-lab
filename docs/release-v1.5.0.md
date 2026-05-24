# v1.5.0 Release Checklist

## Scope

- Add the multi-regime comparison artifact for the bundled synthetic bull, choppy, and drawdown-recovery fixtures.
- Add checked Markdown, JSON, and HTML regime-comparison outputs for cold review.
- Add deterministic multi-regime sample data, provenance metadata, and per-regime config examples.
- Summarize strategy return, buy-and-hold return, strategy-minus-buy-and-hold return, drawdown, exposure, cash-time, exposure changes, and whipsaw diagnostics across fixture regimes.
- Update package metadata and CLI version output to `1.5.0`.
- Preserve research-only, synthetic-only, no-advice, no-forecast, no-live-data, and no-broker boundaries.

## Verification

Run before release:

- `python -m pytest tests/test_cli.py tests/test_report.py tests/test_html.py tests/test_selfcheck.py tests/test_example_data.py`
- `python scripts/selfcheck.py`
- `python -m unittest discover -s tests`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`

## Reviewer Note

The multi-regime comparison increment is a deterministic fixture comparison,
not a market classifier. Reviewers should verify that the Markdown, JSON, HTML,
gallery, docs, and provenance surfaces keep the bull, choppy, and
drawdown-recovery labels framed as synthetic scenarios for historical
diagnostics only.

## Risk Boundaries

- Regime labels are bundled fixture scenarios, not real-time market regimes.
- Comparison rows are historical diagnostics over deterministic synthetic data only.
- Whipsaw, exposure, cash-time, drawdown, and buy-and-hold deltas are review fields, not recommendations or stability claims.
- No broker connection, live market data, forecasts, or buy/sell recommendations are introduced.

## Release Notes

See [v1.5.0 Release Notes](release-notes-v1.5.0.md).
