# v1.20.4 Release Checklist

Release v1.20.4 packages the quick-tour preview documentation increment.

## Included

- Static quick-tour Markdown and SVG preview.
- Public first-screen links from README, docs index, root landing, and gallery manifest.
- Package metadata and CLI version report `1.20.4`.
- Selfcheck/test coverage for the new static route.

## Verification commands

```bash
python -m unittest discover -s tests
python scripts/selfcheck.py
python -m compileall market_signal_lab tests scripts
git diff --check
```

## Scope boundary

No live data, no broker/account/order workflow, no position sizing, no forecasts, no recommendations, and no investment advice.

See [v1.20.4 Release Notes](release-notes-v1.20.4.md).
