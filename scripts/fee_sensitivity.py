#!/usr/bin/env python3
"""Generate the checked-in single-backtest fee sensitivity artifact."""

from __future__ import annotations

from argparse import ArgumentParser
from collections.abc import Sequence
from io import StringIO
from pathlib import Path
import csv
import json
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from market_signal_lab.backtest import backtest_long_cash
from market_signal_lab.data import (
    REQUIRED_COLUMNS,
    PriceBar,
    load_ohlc_csv,
    load_static_fixture_provenance,
)
from market_signal_lab.metrics import max_drawdown, total_return
from market_signal_lab.report import build_exposure_trade_review
from market_signal_lab.strategies import moving_average_crossover_strategy

CSV_PATH = Path("examples/data/sample_tqqq_qld_like.csv")
SYMBOL = "QQQ_LIKE"
SHORT_WINDOW = 20
LONG_WINDOW = 50
FEE_BPS_VALUES = (0.0, 5.0, 10.0, 25.0, 50.0)
MARKDOWN_OUTPUT = Path("reports/fee-sensitivity.md")
JSON_OUTPUT = Path("reports/fee-sensitivity.json")


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    payload = build_fee_sensitivity_payload()
    markdown = render_fee_sensitivity_markdown(payload)

    _write_text(args.markdown_output, markdown)
    _write_text(args.json_output, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


def build_fee_sensitivity_payload() -> dict[str, Any]:
    """Build a deterministic fee-sensitivity payload from the bundled CSV."""

    bars = _load_symbol_bars(REPO_ROOT / CSV_PATH, symbol=SYMBOL)
    signals = moving_average_crossover_strategy(
        bars,
        short_window=SHORT_WINDOW,
        long_window=LONG_WINDOW,
    )
    target_exposures = [signal.target_exposure for signal in signals]
    buy_and_hold_returns: list[float] = []
    for index in range(1, len(bars)):
        buy_and_hold_returns.append(bars[index].close / bars[index - 1].close - 1)

    baseline_total_return = total_return(buy_and_hold_returns)
    provenance = load_static_fixture_provenance(REPO_ROOT / CSV_PATH)
    rows = []
    for fee_bps in FEE_BPS_VALUES:
        curve = backtest_long_cash(
            bars=bars,
            target_exposures=target_exposures,
            fee_bps=fee_bps,
        )
        strategy_returns = [record.strategy_return for record in curve[1:]]
        exposure_review = build_exposure_trade_review(curve)
        strategy_total_return = total_return(strategy_returns)
        rows.append(
            {
                "fee_bps": fee_bps,
                "total_return": strategy_total_return,
                "buy_and_hold_total_return": baseline_total_return,
                "strategy_minus_buy_and_hold_return": (
                    strategy_total_return - baseline_total_return
                ),
                "max_drawdown": max_drawdown(strategy_returns),
                "modeled_exposure_changes": exposure_review["exposure_changes"],
                "modeled_entries": exposure_review["entries_to_market"],
                "modeled_exits": exposure_review["exits_to_cash"],
                "average_exposure": exposure_review["average_exposure"],
                "periods_in_market": exposure_review["periods_in_market"],
                "period_count": exposure_review["period_count"],
                "total_fee_drag": exposure_review["total_fee_drag"],
            }
        )

    payload: dict[str, Any] = {
        "artifact": "fee_sensitivity",
        "research_only": True,
        "input_csv": str(CSV_PATH),
        "symbol": SYMBOL,
        "strategy_config": {
            "short_window": SHORT_WINDOW,
            "long_window": LONG_WINDOW,
        },
        "fee_bps_values": list(FEE_BPS_VALUES),
        "first_date": bars[0].date.isoformat() if bars else None,
        "last_date": bars[-1].date.isoformat() if bars else None,
        "row_count": len(bars),
        "rows": rows,
        "caveats": _caveats(),
    }
    if provenance is not None:
        provenance_payload = provenance.as_dict()
        provenance_payload["metadata_path"] = str(
            Path(provenance_payload["metadata_path"]).relative_to(REPO_ROOT)
        )
        payload["data_provenance"] = provenance_payload

    return payload


def render_fee_sensitivity_markdown(payload: dict[str, Any]) -> str:
    """Render a beginner-readable Markdown fee-sensitivity comparison."""

    config = payload["strategy_config"]
    lines = [
        "# Fee Sensitivity Comparison",
        "",
        "Research-only comparison for the bundled static sample CSV. This artifact "
        "does not use broker connections, live market data, or execution data.",
        "",
        "## Setup",
        "",
        f"- **Input CSV**: {payload['input_csv']}",
        f"- **Symbol**: {payload['symbol']}",
        f"- **Short window**: {config['short_window']}",
        f"- **Long window**: {config['long_window']}",
        f"- **Date range**: {payload['first_date']} to {payload['last_date']}",
        f"- **Rows**: {payload['row_count']}",
        "",
        "## Comparison",
        "",
        "| fee_bps | total_return | buy_and_hold_total_return | strategy_minus_buy_and_hold_return | max_drawdown | modeled_exposure_changes | modeled_entries | modeled_exits | average_exposure | total_fee_drag |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["rows"]:
        lines.append(
            "| "
            f"{row['fee_bps']:.1f} | "
            f"{_format_percent(row['total_return'])} | "
            f"{_format_percent(row['buy_and_hold_total_return'])} | "
            f"{_format_percent(row['strategy_minus_buy_and_hold_return'])} | "
            f"{_format_percent(row['max_drawdown'])} | "
            f"{row['modeled_exposure_changes']} | "
            f"{row['modeled_entries']} | "
            f"{row['modeled_exits']} | "
            f"{_format_percent(row['average_exposure'])} | "
            f"{_format_percent(row['total_fee_drag'])} |"
        )

    lines.extend(
        [
            "",
            "## Beginner Caveats",
            "",
            *[f"- {caveat}" for caveat in payload["caveats"]],
            "",
        ]
    )

    provenance = payload.get("data_provenance")
    if provenance:
        lines.extend(
            [
                "## Data Provenance",
                "",
                "- Research-only static fixture metadata; not live data, not investment advice, and not a prediction.",
                f"- **Dataset label**: {provenance['dataset_label']}",
                f"- **Data kind**: {provenance['data_kind']}",
                f"- **Source**: {provenance['source']}",
                f"- **As-of date**: {provenance['as_of_date']}",
                "",
            ]
        )

    return "\n".join(lines)


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description=(
            "Generate reports/fee-sensitivity.md and reports/fee-sensitivity.json "
            "from the bundled sample CSV."
        )
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=MARKDOWN_OUTPUT,
        help="Markdown output path (default: reports/fee-sensitivity.md).",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=JSON_OUTPUT,
        help="JSON output path (default: reports/fee-sensitivity.json).",
    )
    return parser


def _write_text(path: Path, text: str) -> None:
    output_path = REPO_ROOT / path if not path.is_absolute() else path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def _load_symbol_bars(path: Path, symbol: str) -> list[PriceBar]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"CSV is missing data rows: {path}")
    if "symbol" not in rows[0]:
        raise ValueError("CSV is missing required column(s): symbol")

    symbol_rows = [row for row in rows if row.get("symbol") == symbol]
    if not symbol_rows:
        raise ValueError(f"No rows found for symbol {symbol!r}")

    source = StringIO()
    writer = csv.DictWriter(source, fieldnames=list(REQUIRED_COLUMNS))
    writer.writeheader()
    for row in symbol_rows:
        writer.writerow({column: row[column] for column in REQUIRED_COLUMNS})

    source.seek(0)
    return load_ohlc_csv(source)


def _caveats() -> list[str]:
    return [
        (
            "Fee sensitivity here means rerunning the same historical model with "
            "different basis-point assumptions; it is not an estimate of real "
            "broker costs, spreads, taxes, liquidity, or market impact."
        ),
        (
            "The bundled sample is intentionally tiny and synthetic. Its numbers "
            "are useful for checking artifact shape and reproducibility, not for "
            "making market claims."
        ),
        (
            "The existing 20/50 moving-average setup has no modeled exposure "
            "changes on this eight-row sample, so changing fee_bps does not change "
            "the reported return in this artifact."
        ),
        (
            "Modeled exposure changes, entries, exits, and fee drag are historical "
            "model metadata only. They are not executed trades or instructions."
        ),
        (
            "Buy-and-hold comparison fields are same-period historical context only; "
            "they are not recommendations or evidence of future performance."
        ),
    ]


def _format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


if __name__ == "__main__":
    raise SystemExit(main())
