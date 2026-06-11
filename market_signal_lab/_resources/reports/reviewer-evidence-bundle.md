# Reviewer Evidence Bundle

This bundle is a compact cold-review handoff for Market Signal Lab. It points a reviewer to the static first screen, the thesis-ledger acceptance artifact, the deterministic rerun command, and the methodology-risk caveats without adding live data, broker/account access, orders, forecasts, recommendations, or investment advice.

## First-screen route

1. Open `reports/index.html` to inspect checked-in sample artifacts before installing anything.
2. Read `reports/stress-kit-quickstart-card.md` as the two-minute static/no-advice route into stress-kit review.
3. Read `reports/cross-asset-thesis-ledger-acceptance.md` for the current cross-asset thesis-ledger acceptance summary.
4. Rerun `python -m market_signal_lab.cli --validate-thesis-ledger` to regenerate the acceptance artifacts from the checked-in JSON packet.
5. Review `docs/methodology-audit.md` before citing any historical diagnostic as review context.

## Verification commands

- `python -m market_signal_lab.cli --reviewer-evidence-bundle`
- `python -m market_signal_lab.cli --validate-thesis-ledger`
- `python scripts/selfcheck.py`
- `python -m pytest`

## Artifact hash summary

- Integrity status: `PASS`
- Interpretation: PASS: All expected static reviewer artifacts were present and hashed at generation time.
- Caveat: This is artifact-integrity evidence only; it confirms local file bytes at generation time and does not validate financial correctness, future performance, recommendations, or investment suitability.
- Algorithm: `sha256`
- Scope: local static reviewer evidence artifacts only; hashes are artifact-integrity provenance at generation time, not financial validation
- Present artifacts: `7` of `7`

| Path | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| reports/index.html | present | 8918 | a00e35fc1a737f0145743250267ade6f5e6904b993597835f73e1dc2cf07069a |
| reports/cross-asset-thesis-ledger.json | present | 37420 | ce5efe33b26e3e800f61978594513fb12baa922ab51e1fc01b41ea0d27b7f495 |
| reports/cross-asset-thesis-ledger-acceptance.md | present | 4965 | 351100a40f6e76c9fb28b40234cd6e7a824c11a022235223e5501a86d49b2a14 |
| reports/cross-asset-thesis-ledger-acceptance.json | present | 6008 | 8ac3de4bc1bc71a96f77feeb86796ae0bd103a92a2523b11b5c58f165a5057dc |
| reports/stress-kit-quickstart-card.md | present | 3274 | 36dcaefb9bd916df344d3803d844d2257f2a2549e90630d56988aff93cdb67e0 |
| reports/stress-kit-quickstart-card.json | present | 3724 | 735109bcab80d26e79e975c913a21a0bc9ac6b758398292da4c84e5896f5ac3a |
| docs/methodology-audit.md | present | 4970 | 8913048eb92849915d844090f56d908e744aa84c9d0248c37adade3e13189e3a |

## Beginner risk boundaries

- All metrics are historical diagnostics from bundled static/synthetic sample data.
- QLD_LIKE and TQQQ_LIKE examples model daily-reset leveraged ETF-like behavior; path dependency, volatility drag, and extreme drawdowns can make multi-day results differ sharply from simple 2x/3x expectations.
- The bundle is not a trading bot, signal service, broker workflow, order workflow, position-sizing workflow, forecast engine, recommendation, or investment advice.

## Boundary flags

- research_only: `True`
- static_only: `True`
- no_live_data: `True`
- no_broker_or_account: `True`
- no_orders_or_position_sizing: `True`
- no_recommendations_or_forecasts: `True`
