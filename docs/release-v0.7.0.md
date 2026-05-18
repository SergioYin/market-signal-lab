# v0.7.0 Release Checklist

This checklist covers the public release readiness items for the v0.7.0 documentation navigation release.

See [v0.7.0 Release Notes](release-notes-v0.7.0.md) for the concise public summary.

## Feature Summary

- `docs/index.md` is the canonical documentation map.
- README links readers to the docs map before individual high-priority risk and workflow pages.
- The project selfcheck validates local Markdown links in README and docs without adding dependencies.
- Package metadata and CLI version output identify this release as v0.7.0.
- Existing backtest calculations, generated report schemas, config behavior, sample reports, and no-advice boundaries are unchanged.

## Commands To Verify

Run the test suite:

```bash
pytest
```

Run the project selfcheck, which now checks documentation links before regenerating sample artifacts:

```bash
python scripts/selfcheck.py
```

Confirm the CLI version output:

```bash
market-signal-lab --version
```

Expected output:

```text
market-signal-lab 0.7.0
```

## Public Artifacts

No report artifact schema changes are expected for this release. Review generated diffs before publishing to confirm sample reports remain behaviorally unchanged.

## No-Advice And Data-Provenance Boundaries

- Market Signal Lab remains research-only software. It does not provide investment advice, trading recommendations, forecasts, or live execution signals.
- Documentation navigation and link validation do not alter calculations, fetch live data, connect to brokers, place trades, or make market predictions.
- The bundled sample CSV remains synthetic example data with placeholder `_LIKE` symbols.

## Future Work

- Keep release-specific docs linked from `docs/index.md`.
- Consider deeper anchor validation if documentation grows enough to need section-level link checks.
