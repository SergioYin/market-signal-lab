# Experiment Manifest

- **input_path**: examples/data/sample_tqqq_qld_like.csv
- **symbol**: QQQ_LIKE
- **mode**: backtest

## strategy_config

- **short_window**: 20
- **long_window**: 50

- **fee_bps**: 10.0000

## data_provenance

- **dataset_label**: sample_tqqq_qld_like
- **data_kind**: synthetic_static_fixture
- **source**: Hand-authored deterministic OHLC sample bundled with Market Signal Lab for offline examples and tests.
- **created_date**: 2026-05-18
- **as_of_date**: 2026-05-18
- **limitations**: Synthetic rows are not broker, exchange, fund-provider, vendor, or live-feed data., Placeholder symbols QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE are example-shaped labels, not real instrument histories., Leveraged ETF-like rows do not model fund mechanics, fees, tracking differences, financing costs, taxes, liquidity, or market impact., Use only for deterministic research artifact checks; do not use for advice, recommendations, predictions, or market claims.
- **metadata_path**: examples/data/sample_tqqq_qld_like.csv.provenance.json

## output_paths

- **html_report**: reports/sample-report.html
- **json_report**: reports/sample-report.json
- **manifest**: reports/sample-manifest.md
- **markdown_report**: reports/sample-report.md

- **research_only**: true
