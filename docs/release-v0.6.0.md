# v0.6.0 Release Checklist

This checklist covers the public release readiness items for the v0.6.0 packaging and CLI polish release.

See [v0.6.0 Release Notes](release-notes-v0.6.0.md) for the concise public summary.

## Feature Summary

- CLI supports `market-signal-lab --version` without requiring a CSV path.
- Project metadata declares a minimal setuptools build backend.
- Project metadata and the public `LICENSE` file identify the package as MIT licensed.
- Existing report generation, config loading, and no-advice boundaries are unchanged.

## Commands To Verify

Run the test suite:

```bash
pytest
```

Run the project selfcheck, which also regenerates sample artifacts:

```bash
python scripts/selfcheck.py
```

Confirm the CLI version output:

```bash
market-signal-lab --version
```

Expected output:

```text
market-signal-lab 0.6.0
```

## Public Artifacts

No report artifact changes are expected for this release. Review generated diffs before publishing to confirm that sample reports remain behaviorally unchanged.

## No-Advice And Data-Provenance Boundaries

- Market Signal Lab remains research-only software. It does not provide investment advice, trading recommendations, forecasts, or live execution signals.
- The new version flag and packaging metadata do not alter calculations, fetch live data, connect to brokers, or make market predictions.
- The bundled sample CSV remains synthetic example data with placeholder `_LIKE` symbols.

## Future Work

- Add packaging checks to release automation.
- Publish source and wheel artifacts from a clean release tag.
- Continue improving CLI ergonomics without expanding into advice or execution workflows.
