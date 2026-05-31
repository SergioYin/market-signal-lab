# ADR 0001: Static Research Artifacts

## Status

Accepted.

## Context

Market Signal Lab is public-facing and research-only. The repository needs to show historical market-signal review artifacts that are easy to inspect, rerun, diff, and publish without private data, service credentials, browser scripts, or live trading infrastructure.

Adding live data, broker connections, account workflows, order placement, position sizing, recommendations, forecasts, or advice would change the risk profile of the project and make the sample artifacts harder to review as deterministic examples.

## Decision

Market Signal Lab will remain a static research artifact pipeline.

The CLI may read local CSV/config files and write deterministic Markdown, JSON, HTML, and manifest artifacts. The public demo may link those artifacts through local relative links. Maintainer docs, release notes, and selfcheck gates should keep the no-JavaScript, no-external-assets, no-live-data, no-broker, no-order, no-position-sizing, no-recommendation, no-forecast, and no-advice boundaries explicit.

## Consequences

- Public reviewers can inspect the repository from a checkout or static host.
- Sample artifacts remain reproducible and diffable.
- Test and selfcheck gates can validate public docs and reports without network access.
- The project does not become a trading bot, signal service, broker workflow, account workflow, or advice product.
- Future increments should prefer documentation, local fixtures, deterministic artifact generation, and reviewer-facing validation over live integrations.

Related overview: [Architecture](../architecture.md).
