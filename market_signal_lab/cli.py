"""Command-line interface for CSV moving-average backtest reports."""

from __future__ import annotations

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from collections.abc import Sequence
from io import StringIO
from pathlib import Path
import csv
import json
import sys
from typing import Any

from market_signal_lab.backtest import backtest_long_cash
from market_signal_lab.data import REQUIRED_COLUMNS, PriceBar, load_ohlc_csv
from market_signal_lab.html import render_html_report
from market_signal_lab.metrics import (
    annualized_return,
    max_drawdown,
    sharpe_like,
    total_return,
    volatility,
    win_rate_from_returns,
)
from market_signal_lab.manifest import build_manifest, render_manifest_markdown
from market_signal_lab.report import render_experiment_report
from market_signal_lab.split import TrainTestSplit, split_train_test
from market_signal_lab.strategies import moving_average_crossover_strategy
from market_signal_lab.sweep import (
    SweepResult,
    render_sweep_report,
    run_moving_average_sweep,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        report, json_payload, manifest_payload = (
            _run_sweep(args) if args.sweep else _run_backtest(args)
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.output:
        args.output.write_text(report)
    else:
        print(report, end="")

    if args.json_output:
        args.json_output.write_text(_compact_json(json_payload))

    if args.html_output:
        args.html_output.write_text(render_html_report(report))

    if args.manifest_output:
        args.manifest_output.write_text(render_manifest_markdown(manifest_payload))

    return 0


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="market-signal-lab",
        description="Generate a moving-average crossover report from OHLC CSV data.",
    )
    parser.add_argument("csv_path", type=Path, help="Path to a CSV file of OHLC data.")
    parser.add_argument(
        "--symbol",
        help="Filter by symbol when the input CSV contains a symbol column.",
    )
    parser.add_argument(
        "--short-window",
        type=int,
        default=20,
        help="Short moving-average window (default: 20).",
    )
    parser.add_argument(
        "--long-window",
        type=int,
        default=50,
        help="Long moving-average window (default: 50).",
    )
    parser.add_argument(
        "--fee-bps",
        type=float,
        default=0.0,
        help="Round-trip fee in basis points (default: 0.0).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file path for the markdown report.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Optional output file path for a compact JSON report.",
    )
    parser.add_argument(
        "--html-output",
        type=Path,
        help="Optional output file path for a static HTML report artifact.",
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        help="Optional output file path for a Markdown experiment manifest.",
    )
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Run a moving-average parameter sweep instead of a single report.",
    )
    parser.add_argument(
        "--short-windows",
        type=_parse_integer_list,
        default=(10, 20, 50),
        help="Comma-separated short-window values for --sweep (default: 10,20,50).",
    )
    parser.add_argument(
        "--long-windows",
        type=_parse_integer_list,
        default=(50, 100, 200),
        help="Comma-separated long-window values for --sweep (default: 50,100,200).",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        help="Limit --sweep output to the top N ranked results.",
    )
    split_group = parser.add_mutually_exclusive_group()
    split_group.add_argument(
        "--split-ratio",
        type=_parse_split_ratio,
        help=(
            "Optional train/test split ratio for research metadata only; "
            "must be greater than 0 and less than 1."
        ),
    )
    split_group.add_argument(
        "--split-cutoff",
        help=(
            "Optional train/test cutoff date (YYYY-MM-DD) for research "
            "metadata only."
        ),
    )
    return parser


def _run_backtest(args: Namespace) -> tuple[str, dict[str, Any], dict[str, Any]]:
    bars = _load_bars(Path(args.csv_path), symbol=args.symbol)
    split = _build_validation_split(args, bars)
    validation_split = _build_validation_split_metadata(args, split)
    signals = moving_average_crossover_strategy(
        bars,
        short_window=args.short_window,
        long_window=args.long_window,
    )
    target_exposures = [signal.target_exposure for signal in signals]
    backtest_curve = backtest_long_cash(
        bars=bars,
        target_exposures=target_exposures,
        fee_bps=args.fee_bps,
    )

    strategy_returns = [record.strategy_return for record in backtest_curve[1:]]
    metrics = {
        "total_return": total_return(strategy_returns),
        "annualized_return": annualized_return(strategy_returns),
        "max_drawdown": max_drawdown(strategy_returns),
        "volatility": volatility(strategy_returns),
        "sharpe_like": sharpe_like(strategy_returns),
        "win_rate": win_rate_from_returns(strategy_returns),
    }
    risk_notes = ["Signals use close-price moving averages only."]
    if args.symbol:
        risk_notes.append(f"Filtered to symbol: {args.symbol}.")

    strategy_config = {"short_window": args.short_window, "long_window": args.long_window}
    if args.symbol:
        strategy_config["symbol"] = args.symbol
    if args.fee_bps:
        strategy_config["fee_bps"] = args.fee_bps

    report = render_experiment_report(
        strategy_config=strategy_config,
        backtest_curve=backtest_curve,
        metrics=metrics,
        risk_notes=tuple(risk_notes),
        validation_split=validation_split,
    )

    json_payload = {
        "strategy_config": strategy_config,
        "metrics": metrics,
        "first_date": bars[0].date.isoformat() if bars else None,
        "last_date": bars[-1].date.isoformat() if bars else None,
        "row_count": len(bars),
    }
    if validation_split is not None:
        json_payload["validation_split"] = validation_split

    manifest_payload = build_manifest(
        input_path=args.csv_path,
        symbol=args.symbol,
        mode="backtest",
        strategy_config=strategy_config,
        fee_bps=args.fee_bps,
        output_paths=_output_paths(args),
    )

    return report, json_payload, manifest_payload


def _run_sweep(args: Namespace) -> tuple[str, dict[str, Any], dict[str, Any]]:
    bars = _load_bars(Path(args.csv_path), symbol=args.symbol)
    split = _build_validation_split(args, bars)
    validation_split = _build_validation_split_metadata(args, split)
    results = run_moving_average_sweep(
        bars=bars,
        short_windows=args.short_windows,
        long_windows=args.long_windows,
        fee_bps=args.fee_bps,
        top_n=args.top_n,
        train_bars=split.train if split is not None else None,
        test_bars=split.test if split is not None else None,
    )
    report = render_sweep_report(results, validation_split=validation_split)
    sweep_config: dict[str, Any] = {
        "short_windows": list(args.short_windows),
        "long_windows": list(args.long_windows),
        "fee_bps": args.fee_bps,
        "top_n": args.top_n,
    }
    if args.symbol:
        sweep_config["symbol"] = args.symbol

    json_payload = {
        "sweep_config": sweep_config,
        "ranked_results": [
            _serialize_sweep_result(rank, result)
            for rank, result in enumerate(results, start=1)
        ],
    }
    if validation_split is not None:
        json_payload["validation_split"] = validation_split

    manifest_payload = build_manifest(
        input_path=args.csv_path,
        symbol=args.symbol,
        mode="sweep",
        sweep_config=sweep_config,
        fee_bps=args.fee_bps,
        output_paths=_output_paths(args),
    )

    return report, json_payload, manifest_payload


def _compact_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, separators=(",", ":")) + "\n"


def _serialize_sweep_result(rank: int, result: SweepResult) -> dict[str, Any]:
    row: dict[str, Any] = {
        "rank": rank,
        "windows": {
            "short_window": result.short_window,
            "long_window": result.long_window,
        },
        "metrics": result.metrics,
    }
    if result.train_metrics is not None:
        row["train_metrics"] = result.train_metrics
    if result.test_metrics is not None:
        row["test_metrics"] = result.test_metrics

    return row


def _build_validation_split(
    args: Namespace,
    bars: Sequence[PriceBar],
) -> TrainTestSplit | None:
    if args.split_ratio is None and args.split_cutoff is None:
        return None

    return split_train_test(
        bars,
        train_ratio=args.split_ratio,
        cutoff_date=args.split_cutoff,
    )


def _build_validation_split_metadata(
    args: Namespace,
    split: TrainTestSplit | None,
) -> dict[str, Any] | None:
    if split is None:
        return None

    metadata: dict[str, Any] = {
        "train": _partition_metadata(split.train),
        "test": _partition_metadata(split.test),
        "research_only": True,
        "note": "Validation split metadata is not a trading recommendation.",
    }
    if args.split_ratio is not None:
        metadata["method"] = "ratio"
        metadata["split_ratio"] = args.split_ratio
    else:
        metadata["method"] = "cutoff"
        metadata["split_cutoff"] = args.split_cutoff

    return metadata


def _partition_metadata(bars: Sequence[PriceBar]) -> dict[str, Any]:
    return {
        "first_date": bars[0].date.isoformat(),
        "last_date": bars[-1].date.isoformat(),
        "row_count": len(bars),
    }


def _output_paths(args: Namespace) -> dict[str, Path | None]:
    return {
        "html_report": args.html_output,
        "json_report": args.json_output,
        "manifest": args.manifest_output,
        "markdown_report": args.output,
    }


def _load_bars(path: Path, symbol: str | None = None) -> list[PriceBar]:
    if symbol is None:
        return load_ohlc_csv(path)

    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"CSV is missing data rows: {path}")
    header = rows[0].keys()
    if "symbol" not in header:
        raise ValueError("CSV is missing required column(s): symbol")

    symbol_rows = [row for row in rows if row.get("symbol") == symbol]
    if not symbol_rows:
        raise ValueError(f"No rows found for symbol {symbol!r}")

    return _load_rows_as_csv(symbol_rows)


def _load_rows_as_csv(rows: Sequence[dict[str, str]]) -> list[PriceBar]:
    source = StringIO()
    writer = csv.DictWriter(source, fieldnames=list(REQUIRED_COLUMNS))
    writer.writeheader()
    for row in rows:
        writer.writerow({column: row[column] for column in REQUIRED_COLUMNS})

    source.seek(0)
    return load_ohlc_csv(source)


def _parse_integer_list(value: str) -> tuple[int, ...]:
    values: list[int] = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            raise ArgumentTypeError("list values must be comma-separated integers")
        try:
            values.append(int(item))
        except ValueError as exc:
            raise ArgumentTypeError(
                "list values must be comma-separated integers"
            ) from exc

    return tuple(values)


def _parse_split_ratio(value: str) -> float:
    try:
        ratio = float(value)
    except ValueError as exc:
        raise ArgumentTypeError("split ratio must be a floating point value") from exc

    if not 0 < ratio < 1:
        raise ArgumentTypeError("split ratio must be greater than 0 and less than 1")

    return ratio


if __name__ == "__main__":
    raise SystemExit(main())
