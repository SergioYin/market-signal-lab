# v1.5.0 Release Notes

Market Signal Lab v1.5.0 is a multi-regime comparison increment for the checked static demo and research artifact trail.

## Changed

- Adds a `--regime-comparison` workflow that writes checked Markdown, JSON, and HTML artifacts for the bundled synthetic multi-regime fixture.
- Adds deterministic bull, choppy, and drawdown-recovery sample regimes with explicit provenance, generation assumptions, and synthetic-only trust flags.
- Adds per-regime config examples so each fixture scenario can also be rendered as an ordinary single-backtest report.
- Compares strategy return, buy-and-hold return, strategy-minus-buy-and-hold return, max drawdown, exposure, cash-time, exposure changes, and whipsaw rate side by side.
- Adds static-gallery, documentation-map, artifact-gallery, example-data, and selfcheck coverage for the regime-comparison artifacts.
- Updates package and CLI version metadata to `1.5.0`.

## Verification Expectations

- Regenerate the static artifact trail with `python scripts/selfcheck.py`.
- Run focused coverage for CLI, report rendering, HTML rendering, example data, and selfcheck behavior.
- Run the full unittest discovery and compile checks before tagging.
- Confirm `git diff --check` is clean.

## Boundaries

- The bull, choppy, and drawdown-recovery labels are deterministic fixture scenarios only; they are not market classifications.
- Regime comparison artifacts are historical diagnostics over synthetic sample data only.
- Strategy return, buy-and-hold return, drawdown, exposure, cash-time, exposure-change, and whipsaw fields are not advice, forecasts, trading instructions, or evidence of future performance.
- No broker connection, live market data, recommendations, or execution cues are added.
