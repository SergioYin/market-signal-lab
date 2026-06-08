# v1.25.0 Release Notes

Market Signal Lab v1.25.0 adds a cold-user review route for public first-time review of checked-in static artifacts. The route is research-only and uses repo-relative public files only; it includes no private context, live market data, broker or account workflow, orders, position sizing, forecasts, recommendations, or investment advice.

## Added

- Added [Cold-user review route Markdown](../reports/cold-user-review-route.md) for a concise first-open path through the static gallery, sample report, beginner boundary checklist, reviewer evidence bundle, and methodology caveats.
- Added [Cold-user review route JSON](../reports/cold-user-review-route.json) with the same route, checklist status labels, boundary flags, verification commands, and static artifact integrity summary.
- Added the CLI route:

```bash
python -m market_signal_lab.cli --cold-user-review-route
```

## Verification

Regenerate the new Markdown and JSON outputs from the repository root:

```bash
python -m market_signal_lab.cli --cold-user-review-route
```

Run the usual local documentation gates before release:

```bash
python scripts/selfcheck.py
git diff --check
```

## Research-Only Boundary

The cold-user review route is an orientation and reproducibility aid for static historical diagnostics. It does not validate financial correctness, future performance, strategy quality, suitability, tradability, recommendations, forecasts, or investment advice.
