"""Command-line interface for CSV moving-average backtest reports."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from io import StringIO
from pathlib import Path
import csv
import sys

from market_signal_lab.backtest import backtest_long_cash
from market_signal_lab.data import REQUIRED_COLUMNS, PriceBar, load_ohlc_csv
from market_signal_lab.metrics import (
    annualized_return,
    max_drawdown,
    sharpe_like,
    total_return,
    volatility,
    win_rate_from_returns,
)
from market_signal_lab.report import render_experiment_report
from market_signal_lab.strategies import moving_average_crossover_strategy


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        report = _run_backtest(args)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.output:
        args.output.write_text(report)
    else:
        print(report, end="")

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
    return parser


def _run_backtest(args: Namespace) -> str:
    bars = _load_bars(Path(args.csv_path), symbol=args.symbol)
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

    return render_experiment_report(
        strategy_config=strategy_config,
        backtest_curve=backtest_curve,
        metrics=metrics,
        risk_notes=tuple(risk_notes),
    )


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


if __name__ == "__main__":
    raise SystemExit(main())
