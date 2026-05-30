# Thesis-Ledger 60-Second Walkthrough

Market Signal Lab v1.10.0 includes a zero-dependency validator for the checked-in cross-asset thesis-ledger JSON packet. The validator is for public review of artifact shape and research boundaries only.

## Run

From the repository root, validate the default checked-in packet:

```bash
python -m market_signal_lab.cli --validate-thesis-ledger
```

If the package is installed, the equivalent command is:

```bash
market-signal-lab --validate-thesis-ledger
```

To validate a specific local packet, pass its path:

```bash
python -m market_signal_lab.cli --validate-thesis-ledger path/to/cross-asset-thesis-ledger.json
```

## Files

Default input:

- `reports/cross-asset-thesis-ledger.json`

Default outputs, when no output paths are supplied:

- `reports/cross-asset-thesis-ledger-acceptance.md`
- `reports/cross-asset-thesis-ledger-acceptance.json`

Optional output paths:

```bash
python -m market_signal_lab.cli --validate-thesis-ledger \
  --output reports/my-ledger-acceptance.md \
  --json-output reports/my-ledger-acceptance.json
```

The validator reads only a local JSON packet and writes only local acceptance artifacts. It does not fetch market data.

## Read The Result

Use the Markdown summary first, then inspect JSON if you need structured fields.

- PASS: `accepted` is `true`, `error_count` is `0`, and each row in `checks` has `accepted: true`.
- WARN: `warning_count` is greater than `0`. In v1.10.0 the validator emits `warning_count: 0`; future warnings should be read as review notes, not approval or rejection by themselves.
- FAIL: `accepted` is `false`, `error_count` is greater than `0`, or one or more rows in `checks` has `accepted: false`.

Important fields:

- `summary_type`: acceptance artifact type.
- `schema_version`: acceptance schema version.
- `packet_type` and `packet_schema_version`: identity of the packet being validated.
- `asset_symbols`: symbols reviewed in the packet.
- `checks`: deterministic shape and boundary checks with a short message for each row.

## Boundaries

The validator checks that the thesis-ledger packet preserves public research-only boundaries: offline-only input, historical diagnostics only, no live data, no broker connection, no account access, no orders, no position sizing, no forecasts, no recommendations, and no investment advice.

Passing validation means the artifact matches the expected v1.10.0 packet shape and boundary language. It does not mean a strategy is profitable, robust, suitable for trading, or likely to perform in the future.
