# v1.19.0 Release Notes

Market Signal Lab v1.19.0 adds a public-safe architecture and maintainer documentation increment. It documents the static-first artifact pipeline, methodology audit modules, sample report surface, selfcheck gates, and the intentional exclusion of live data, broker workflows, trading workflows, recommendations, forecasts, and investment advice.

## Added

- `docs/architecture.md`, a maintainer-oriented overview of the static-first architecture and artifact pipeline.
- `docs/adr/0001-static-research-artifacts.md`, a small ADR recording the decision to keep the project as a static research artifact pipeline.
- Public links from README, documentation map, root landing page, and static demo manifest.
- Selfcheck/test assertions so the new docs remain covered by local link and public-claim checks.

## Changed

- Updates package and CLI version metadata to `1.19.0`.
- Updates the static demo manifest version label to `v1.19.0`.

## Boundaries

This release is documentation-only except version metadata. It adds no runtime behavior, JavaScript, external assets, live data, broker or account workflow, orders, position sizing, recommendations, forecasts, or investment advice.
