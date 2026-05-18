# Artifact Gallery

Market Signal Lab includes generated sample artifacts in `reports/` so new users can inspect the outputs before running their own data. These files are research artifacts only. They are not trading advice, recommendations, forecasts, or instructions to buy or sell anything.

The bundled sample data is synthetic and intentionally small. The generated numbers are useful for checking report structure and reproducibility, not for making market claims. See [Data Provenance](data-provenance.md) for the source and placeholder-symbol details.

For plain-language definitions of report metrics, including buy-and-hold comparisons, max drawdown, volatility, Sharpe-like score, and leveraged ETF path-dependency caveats, see the [Metric Guide](metric-guide.md).

`reports/index.html` is a static no-JavaScript gallery that links to the checked-in sample HTML reports and their related Markdown, JSON, and manifest artifacts. It uses only relative links and no external assets, so it can be opened directly from a local checkout or served as a public static page.

## Report Artifacts

`reports/sample-report.md` is the human-readable Markdown backtest report. It shows the moving-average strategy configuration, backtest date range, starting and ending equity, exposure changes, summary metrics, same-period buy-and-hold comparison fields, risk notes, and backtest caveats.

`reports/sample-report.json` is the machine-readable version of the same single backtest. It includes the strategy configuration, metrics, first and last dates, and row count. The single-backtest metric keys include `buy_and_hold_total_return` and `strategy_minus_buy_and_hold_return` as historical comparison diagnostics only. Use this format when another script, notebook, or test needs structured output.

`reports/sample-report.html` is an HTML wrapper around the Markdown report content. It is useful for opening the sample report in a browser or attaching it to workflows that expect an HTML artifact.

## Sweep Artifacts

`reports/sample-sweep.md` is the human-readable parameter sweep report. It ranks several moving-average window pairs from the bundled sample data and prints the top rows as a Markdown table.

`reports/sample-sweep.json` is the machine-readable sweep output. It records the sweep configuration and an ordered `ranked_results` list with each window pair and its metrics.

`reports/sample-sweep.html` is an HTML wrapper around the Markdown sweep report. It provides a browser-viewable version of the same ranked table.

Sweep runs can also include train/test comparison metadata by passing `--split-ratio` or `--split-cutoff`. In that mode, the ranked table and JSON results include `train_total_return` and `test_total_return` diagnostics for each window pair when those partitions can be evaluated. These values compare historical partitions inside the supplied dataset; they are not forecasts, recommendations, or evidence of future performance.

`reports/sample-sweep-split.md`, `reports/sample-sweep-split.json`, and `reports/sample-sweep-split.html` are generated from the bundled sample CSV with `--sweep --short-windows 1,2 --long-windows 2,3 --split-ratio 0.5`. The small windows and even split are intentional for the eight-row fixture so the train/test comparison columns show non-zero diagnostics in the checked-in sample artifact set.

### Why Sweep Rankings Are Not Predictions

A sweep ranking says, "within this historical sample, using these settings, this row sorted higher by the ranking rule." It does not say the same settings will work tomorrow.

For beginners, think of a sweep like checking which shoes were fastest on one short practice route. The result can describe that route, on that day, under those conditions. It does not prove those shoes will be fastest on every route or in future weather. In market research, this gap is larger because prices change, regimes shift, costs vary, and testing many parameter combinations can accidentally reward settings that fit noise.

Use sweep rankings and train/test comparison fields as a starting point for questioning a strategy, not as a prediction engine.

## Manifest Artifact

`reports/sample-manifest.md` records how the single-report artifact set was produced. It includes the input path, symbol, run mode, strategy configuration, output paths, fee setting, and `research_only: true`.

The manifest is intended to make reproduction easier: if a report is shared without context, the manifest gives reviewers a compact record of the inputs and outputs behind it.

## Regenerating The Samples

Run the project selfcheck from the repository root:

```bash
python scripts/selfcheck.py
```

The selfcheck performs four checks:

1. Compiles the package and tests to catch syntax issues.
2. Runs the test suite with `pytest`.
3. Validates local Markdown links in README and docs.
4. Regenerates the sample report, manifest, sweep, JSON, and HTML artifacts under `reports/`.

After it finishes, the expected generated files are:

- `reports/sample-report.md`
- `reports/sample-report.json`
- `reports/sample-report.html`
- `reports/index.html`
- `reports/sample-sweep.md`
- `reports/sample-sweep.json`
- `reports/sample-sweep.html`
- `reports/sample-sweep-split.md`
- `reports/sample-sweep-split.json`
- `reports/sample-sweep-split.html`
- `reports/sample-manifest.md`

Because selfcheck rewrites these files, review the generated diff before committing changes.
