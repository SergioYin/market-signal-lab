# v1.26.0 Release Docs

This release increments Market Signal Lab from v1.25.0 to v1.26.0 for the reviewer rerun receipt feature.

## Public Artifacts

- [Reviewer rerun receipt Markdown](../reports/reviewer-rerun-receipt.md)
- [Reviewer rerun receipt JSON](../reports/reviewer-rerun-receipt.json)
- [Static sample gallery](../reports/index.html)
- [Static demo manifest](static-gallery-manifest.md)
- [Artifact gallery notes](artifact-gallery.md)

## CLI

```bash
python -m market_signal_lab.cli --reviewer-rerun-receipt
```

Default outputs:

- `reports/reviewer-rerun-receipt.md`
- `reports/reviewer-rerun-receipt.json`

The route also supports custom `--output` and `--json-output` paths. It rejects CSV, config, HTML, manifest, strategy, sweep, split, and other artifact-mode arguments.

## Compatibility

v1.26.0 keeps the v1.25.0 public review surfaces:

- `python -m market_signal_lab.cli --cold-user-review-route`
- `python -m market_signal_lab.cli --prediction-readiness-audit`
- `python -m market_signal_lab.cli --reviewer-evidence-bundle`
- `python -m market_signal_lab.cli --validate-thesis-ledger`

## Finance Boundaries

The receipt and linked review artifacts are static research outputs. They include no live data, no broker or account workflow, no order workflow, no position sizing, no forecasts, no recommendations, and no investment advice.
