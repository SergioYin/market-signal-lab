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

from market_signal_lab import __version__
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
        args = _resolve_args(args, parser)
        report, json_payload, manifest_payload = (
            _run_sweep(args) if args.sweep else _run_backtest(args)
        )
        _write_outputs(args, report, json_payload, manifest_payload)
    except (OSError, ValueError, ArgumentTypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    return 0


def _write_outputs(
    args: Namespace,
    report: str,
    json_payload: dict[str, Any],
    manifest_payload: dict[str, Any],
) -> None:
    if args.output:
        _write_text(args.output, report)
    else:
        print(report, end="")

    if args.json_output:
        _write_text(args.json_output, _compact_json(json_payload))

    if args.html_output:
        _write_text(args.html_output, render_html_report(report))

    if args.manifest_output:
        _write_text(args.manifest_output, render_manifest_markdown(manifest_payload))


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="market-signal-lab",
        description="Generate a moving-average crossover report from OHLC CSV data.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        nargs="?",
        help="Path to a CSV file of OHLC data.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Optional JSON config file. CLI flags override config values.",
    )
    parser.add_argument(
        "--symbol",
        help="Filter by symbol when the input CSV contains a symbol column.",
    )
    parser.add_argument(
        "--short-window",
        type=int,
        default=None,
        help="Short moving-average window (default: 20).",
    )
    parser.add_argument(
        "--long-window",
        type=int,
        default=None,
        help="Long moving-average window (default: 50).",
    )
    parser.add_argument(
        "--fee-bps",
        type=float,
        default=None,
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
        default=None,
        help="Run a moving-average parameter sweep instead of a single report.",
    )
    parser.add_argument(
        "--short-windows",
        type=_parse_integer_list,
        default=None,
        help="Comma-separated short-window values for --sweep (default: 10,20,50).",
    )
    parser.add_argument(
        "--long-windows",
        type=_parse_integer_list,
        default=None,
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
        metavar="RATIO",
        help=(
            "Use the first RATIO share of rows for training and the rest for "
            "testing; with --sweep, adds train/test rank and return-gap "
            "diagnostics. Must be greater than 0 and less than 1."
        ),
    )
    split_group.add_argument(
        "--split-cutoff",
        metavar="YYYY-MM-DD",
        help=(
            "Use rows before this date for training and rows on or after it "
            "for testing; with --sweep, adds train/test rank and return-gap "
            "diagnostics."
        ),
    )
    return parser


def _resolve_args(args: Namespace, parser: ArgumentParser) -> Namespace:
    config_values = _load_config(args.config) if args.config else {}
    if args.split_ratio is not None:
        config_values.pop("split_cutoff", None)
    if args.split_cutoff is not None:
        config_values.pop("split_ratio", None)

    resolved = Namespace()
    for key, default in _default_args().items():
        value = getattr(args, key)
        if value is None and key in config_values:
            value = config_values[key]
        if value is None:
            value = default
        setattr(resolved, key, value)

    resolved.config = args.config
    if resolved.csv_path is None:
        parser.error("the following arguments are required: csv_path")
    if resolved.split_ratio is not None and resolved.split_cutoff is not None:
        parser.error(
            "choose only one validation split option: --split-ratio or "
            "--split-cutoff (config keys: split_ratio or split_cutoff)"
        )

    return resolved


def _default_args() -> dict[str, Any]:
    return {
        "csv_path": None,
        "symbol": None,
        "short_window": 20,
        "long_window": 50,
        "fee_bps": 0.0,
        "output": None,
        "json_output": None,
        "html_output": None,
        "manifest_output": None,
        "sweep": False,
        "short_windows": (10, 20, 50),
        "long_windows": (50, 100, 200),
        "top_n": None,
        "split_ratio": None,
        "split_cutoff": None,
    }


def _load_config(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(), parse_constant=_reject_json_constant)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON config {path}: {exc.msg}") from exc

    if not isinstance(raw, dict):
        raise ValueError("Config file must contain a JSON object")

    allowed_keys = set(_default_args())
    unknown_keys = sorted(set(raw) - allowed_keys)
    if unknown_keys:
        keys = ", ".join(unknown_keys)
        raise ValueError(f"Unknown config option(s): {keys}")

    return {
        key: _coerce_config_value(key, value)
        for key, value in raw.items()
        if value is not None
    }


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"Invalid JSON constant: {value}")


def _coerce_config_value(key: str, value: Any) -> Any:
    if key in {"csv_path", "output", "json_output", "html_output", "manifest_output"}:
        if not isinstance(value, str):
            raise ValueError(f"Config option {key!r} must be a string path")
        return Path(value)
    if key in {"symbol", "split_cutoff"}:
        if not isinstance(value, str):
            raise ValueError(f"Config option {key!r} must be a string")
        return value
    if key in {"short_window", "long_window", "top_n"}:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"Config option {key!r} must be an integer")
        return value
    if key == "fee_bps":
        if not isinstance(value, int | float) or isinstance(value, bool):
            raise ValueError("Config option 'fee_bps' must be numeric")
        return float(value)
    if key == "sweep":
        if not isinstance(value, bool):
            raise ValueError("Config option 'sweep' must be a boolean")
        return value
    if key in {"short_windows", "long_windows"}:
        return _coerce_config_integer_list(key, value)
    if key == "split_ratio":
        if not isinstance(value, int | float) or isinstance(value, bool):
            raise ValueError("Config option 'split_ratio' must be numeric")
        return _parse_split_ratio(str(value))

    raise ValueError(f"Unsupported config option: {key}")


def _coerce_config_integer_list(key: str, value: Any) -> tuple[int, ...]:
    if isinstance(value, str):
        return _parse_integer_list(value)
    if not isinstance(value, list):
        raise ValueError(f"Config option {key!r} must be a list of integers")
    if not value:
        raise ValueError(f"Config option {key!r} must not be empty")
    if not all(isinstance(item, int) and not isinstance(item, bool) for item in value):
        raise ValueError(f"Config option {key!r} must be a list of integers")

    return tuple(value)


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
    buy_and_hold_returns = [record.market_return for record in backtest_curve[1:]]
    strategy_total_return = total_return(strategy_returns)
    buy_and_hold_total_return = total_return(buy_and_hold_returns)
    metrics = {
        "total_return": strategy_total_return,
        "buy_and_hold_total_return": buy_and_hold_total_return,
        "strategy_minus_buy_and_hold_return": strategy_total_return
        - buy_and_hold_total_return,
        "annualized_return": annualized_return(strategy_returns),
        "max_drawdown": max_drawdown(strategy_returns),
        "volatility": volatility(strategy_returns),
        "sharpe_like": sharpe_like(strategy_returns),
        "win_rate": win_rate_from_returns(strategy_returns),
    }
    risk_notes = ["Model exposure states use close-price moving averages only."]
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
    if result.robustness is not None:
        row["robustness"] = result.robustness

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
        "note": "Validation split metadata is a research note, not trading guidance.",
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
