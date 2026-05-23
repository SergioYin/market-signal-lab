# v1.4.0 Release Checklist

## Scope

- Add plain-language scenario/risk interpretation to single backtest Markdown and HTML reports.
- Add structured `scenario_risk_interpretation` JSON output for the same historical diagnostics.
- Document beginner-facing terms in the scenario/risk glossary and link them from public docs.
- Update package metadata and CLI version output to `1.4.0`.
- Preserve research-only, no-advice, no-forecast, no-live-data, and no-broker boundaries.

## Verification

Run before release:

- `python -m pytest tests/test_report.py tests/test_cli.py tests/test_selfcheck.py`
- `python scripts/selfcheck.py`
- `python -m unittest discover -s tests`
- `python -m compileall market_signal_lab tests scripts`
- `git diff --check`

## Reviewer Note

Independent product/engineering review found no blocking issue in the
scenario/risk increment. The generated Markdown, HTML, and JSON fields keep the
interpretation framed as historical diagnostics only, not advice, forecasts,
broker guidance, or execution cues.

## Release Notes

See [v1.4.0 Release Notes](release-notes-v1.4.0.md).
