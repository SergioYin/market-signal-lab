# v1.7.0 Release Checklist

## Goal

Ship a minimal pre-trade research packet MVP that reuses the existing local sample/backtest data path and writes Markdown plus JSON artifacts.

## Checklist

- Add a zero-dependency `--pretrade-packet` CLI flag.
- Reuse the existing single-backtest diagnostics instead of adding a separate market-data or execution workflow.
- Include assumptions, historical diagnostics, beginner checklist, and explicit non-advice plus leveraged ETF-like risk boundaries.
- Add tests for packet rendering through the CLI.
- Add selfcheck generation for `reports/pretrade-packet.md` and `reports/pretrade-packet.json`.
- Update docs and example artifacts.
- Confirm package metadata and CLI version output are `1.7.0`.

## Verification

```bash
python -m pytest
python scripts/selfcheck.py
```

## Boundary Check

The packet is an offline research artifact. It must not include broker features, live-data features, account workflows, order workflows, private names, or external dependencies.

See [v1.7.0 Release Notes](release-notes-v1.7.0.md).
