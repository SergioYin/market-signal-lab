# v1.9.1 Release Checklist

## Scope

Release v1.9.1 packages a static-demo and manifest hygiene pass after the v1.9 cross-asset thesis-ledger increment.

## Artifact contract

- `docs/static-gallery-manifest.md` identifies the current static demo surface and includes the cross-asset thesis-ledger Markdown/JSON artifacts.
- `index.html` links to v1.9.x release notes and checklists from the root static landing page.
- Package metadata and CLI version report `1.9.1`.

## Verification

Run before tag/release:

```bash
python -m pytest
python scripts/selfcheck.py
python -m compileall market_signal_lab tests scripts
python -c 'import market_signal_lab; print("market-signal-lab", market_signal_lab.__version__)'
git diff --check
```

Fresh-clone validation should repeat the same checks and verify the v1.9.1 GitHub release metadata.

## Boundaries

- No live data, broker connection, account flow, order routing, position sizing, forecast, recommendation, or execution feature.
- Public privacy scan passes before push/release.

See [v1.9.1 Release Notes](release-notes-v1.9.1.md).
