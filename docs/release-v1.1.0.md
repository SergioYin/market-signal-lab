# v1.1.0 Release Checklist

This checklist covers the v1.1.0 readiness increment for exposure/trade review metadata in single backtest artifacts. It is intended for a reviewer confirming that the checked-in samples expose the new fields while staying research-only and public-safe.

See [v1.1.0 Release Notes](release-notes-v1.1.0.md) for the concise public summary.

## Feature Summary

- Markdown single backtest reports include a `Modeled Exposure Review` section.
- JSON single backtest reports include an `exposure_trade_review` object.
- The review summarizes period counts, in-market/cash percentages, average exposure, exposure changes, modeled entries/exits, and modeled fee drag.
- The wording frames entries and exits as historical model states, not executed trades, instructions, advice, recommendations, or forecasts.
- Package metadata and CLI version output identify this release as v1.1.0.

## Verification Commands

Run every command from the repository root.

Confirm the source-tree version:

```bash
python -m market_signal_lab.cli --version
```

Expected output:

```text
market-signal-lab 1.1.0
```

Run the test suite:

```bash
pytest
```

Run the project selfcheck, which validates documentation links, public wording boundaries, static fixture provenance, and regenerated sample artifacts:

```bash
python scripts/selfcheck.py
```

Expected selfcheck pass labels:

```text
PASS: compileall
PASS: pytest
PASS: sample artifact generation
PASS: documentation/gallery link check
PASS: v0.9.0 static demo acceptance check
PASS: public claim boundary check
PASS: static fixture provenance check
Selfcheck completed.
```

Review the resulting workspace diff before publishing:

```bash
git status --short
git diff -- market_signal_lab/report.py market_signal_lab/cli.py docs/artifact-gallery.md docs/index.md docs/release-notes-v1.1.0.md docs/release-v1.1.0.md reports/sample-report.md reports/sample-report.json reports/sample-report.html
```

## Exposure Review Artifact Paths

Review generated single backtest surfaces that should include `Modeled Exposure Review` or `exposure_trade_review`:

- `reports/sample-report.md`
- `reports/sample-report.json`
- `reports/sample-report.html`

Confirm that `reports/sample-report.json` includes these `exposure_trade_review` keys:

- `period_count`
- `periods_in_market`
- `periods_in_cash`
- `percent_periods_in_market`
- `percent_periods_in_cash`
- `average_exposure`
- `exposure_changes`
- `entries_to_market`
- `exits_to_cash`
- `total_fee_drag`
- `research_only`
- `note`

## Release Engineer Notes

- Run `python -m market_signal_lab.cli --version` before publishing and confirm `market-signal-lab 1.1.0`.
- Run `pytest` before publishing.
- Run `python scripts/selfcheck.py` before publishing.
- Confirm package metadata in `pyproject.toml` and `market_signal_lab/__init__.py` both say `1.1.0`.
- Confirm the runtime dependency list remains empty.

## No-Advice And Exposure Boundaries

- Market Signal Lab remains research-only software. It does not provide investment advice, trading recommendations, forecasts, live execution signals, or broker execution.
- Exposure/trade review metadata summarizes historical model states inside the supplied dataset.
- Modeled entries and modeled exits are not executed trades, trade instructions, or instructions to buy, sell, hold, or size a position.
- The bundled sample CSV remains synthetic example data with placeholder `_LIKE` symbols.
