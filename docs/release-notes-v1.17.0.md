# v1.17.0 Release Notes

Market Signal Lab v1.17.0 adds a small public-safe methodology-audit documentation and validation increment. It documents reviewer-filled audit JSON files and makes malformed check names or statuses fail with clear CLI errors.

## Added

- `docs/methodology-audit-review-schema.md`, a JSON schema-like reference for methodology audit review files.
- Lightweight validation helper coverage for methodology audit review `checks` rows, including exact check-name order and allowed status values.
- CLI tests for invalid methodology audit check names and statuses.

## Changed

- Updates package and CLI version metadata to `1.17.0`.
- Registers the schema page in the README, documentation map, root landing page, static demo manifest, release docs, and selfcheck link sources.
- Improves invalid methodology-audit status errors to show the accepted values.

## Boundaries

This release remains deterministic and stdlib-only. It adds no JavaScript, no broker or account workflow, no live data, no orders, no position sizing, no recommendations, no forecasts, and no investment advice.
