# v1.3.5 Release Notes

Market Signal Lab v1.3.5 is a package metadata and manifest polish release.

## Changed

- Adds public package metadata: README long description, author, keywords, classifiers, homepage, repository, issues, and documentation URLs.
- Adds packaging regression coverage for public package metadata and CLI entrypoint declaration.
- Polishes manifest Markdown rendering so fields duplicated between nested config and top-level metadata are rendered once in the human-facing manifest.
- Updates package and CLI version metadata to `1.3.5`.

## Boundaries

- No broker connection, live market data, forecasts, or buy/sell recommendations.
- Manifest and package metadata describe research-only tooling and static demo assets only.
