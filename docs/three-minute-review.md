# Three-Minute Review Route

Use this route when you want to decide quickly whether Market Signal Lab is worth cloning, starring, or reusing as a research-artifact pattern. It is a static, research-only review path. It does not fetch live market data, connect to brokers, inspect accounts, route orders, size positions, recommend trades, forecast returns, or provide investment advice.

## Minute 1: Open the public first screen

Open the [Root Landing](../index.html) or the public Pages landing, then open the [Static Sample Gallery](../reports/index.html). Confirm that the gallery is plain static HTML with local links only and visible artifact paths.

Look for these evidence anchors:

- `reports/sample-report.html` for a single historical diagnostic report.
- `reports/scenario-card.md` for a compact research-only card.
- `reports/cross-asset-thesis-ledger.md` for a multi-symbol evidence packet.
- `docs/static-gallery-manifest.md` for the no-JavaScript, no-external-asset link contract.

## Minute 2: Inspect the method and caveats

Open the [Methodology Audit](methodology-audit.md) and [Methodology Audit Score](../reports/methodology-audit-score.md). They force the sample backtest to be reviewed through common pitfalls instead of being presented as a profit claim.

Check that the artifacts explicitly label:

- look-ahead, survivorship, overfitting, fees, and slippage checks;
- leveraged ETF-like daily reset and path-dependency risk;
- synthetic/static sample-data boundaries;
- no live trading, no broker or account workflow, no orders, no position sizing, no recommendations, no forecasts, and no investment advice.

## Minute 3: Verify one command locally

From a fresh checkout, run:

```bash
python -m market_signal_lab.cli --validate-thesis-ledger
```

Expected result: the command validates the checked-in `reports/cross-asset-thesis-ledger.json` packet and writes acceptance artifacts under `reports/`. Review [Thesis-Ledger Acceptance Summary](../reports/cross-asset-thesis-ledger-acceptance.md) for PASS/WARN/FAIL fields.

## Reviewer decision checklist

After three minutes, the useful question is not "does this strategy win?" The useful question is whether the repo provides a reusable public pattern for packaging historical diagnostics with visible assumptions, caveats, generated artifacts, and acceptance checks.

Use this checklist:

- Can a stranger find the static demo before installing anything?
- Are the assumptions and sample-data boundaries visible?
- Are leveraged ETF-like risks explained as path-dependent and high drawdown, not as guaranteed multiplied returns?
- Can the reviewer reproduce at least one acceptance artifact locally?
- Is every artifact clearly research-only and non-advisory?

If any answer is "no", treat it as a documentation or methodology-review gap before sharing the project more broadly.
