"""Cross-asset thesis-ledger evidence packets for bundled sample data."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from io import StringIO
import csv
from pathlib import Path
from typing import Any

from market_signal_lab.backtest import backtest_long_cash
from market_signal_lab.data import (
    REQUIRED_COLUMNS,
    PriceBar,
    load_ohlc_csv,
    load_static_fixture_provenance,
)
from market_signal_lab.metrics import (
    annualized_return,
    max_drawdown,
    sharpe_like,
    total_return,
    volatility,
    win_rate_from_returns,
)
from market_signal_lab.packet import LEVERAGED_ETF_RISK_BOUNDARY
from market_signal_lab.report import (
    build_exposure_trade_review,
    build_scenario_risk_interpretation,
)
from market_signal_lab.scenario_card import (
    build_scenario_card,
    render_scenario_card,
)
from market_signal_lab.strategies import moving_average_crossover_strategy

THESIS_LEDGER_SYMBOLS = ("QQQ_LIKE", "QLD_LIKE", "TQQQ_LIKE")
THESIS_LEDGER_NOTE = (
    "Research-only cross-asset thesis-ledger evidence packet built from the "
    "bundled static sample CSV; not investment advice, not trading guidance, "
    "not a recommendation, not a prediction, and not a broker connection or "
    "execution feature."
)
THESIS_LEDGER_SCOPE_LIMITS = (
    "Offline artifact only. No live data, broker workflow, account fields, "
    "order routing, position sizing instruction, forecast, or execution path."
)
THESIS_LEDGER_ASSUMPTIONS = (
    "Uses only examples/data/sample_tqqq_qld_like.csv and adjacent provenance.",
    "Uses placeholder QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE rows from the same date range.",
    "Uses a deterministic 2/3 moving-average configuration so the tiny sample has reviewable exposure states.",
    "Uses fee_bps as a simplified historical cost assumption.",
    "Reuses existing single-backtest metrics, exposure review, scenario-risk, and scenario-card helpers.",
)


def build_cross_asset_thesis_ledger(
    input_path: Path,
    symbols: Sequence[str] = THESIS_LEDGER_SYMBOLS,
    short_window: int = 2,
    long_window: int = 3,
    fee_bps: float = 10.0,
) -> dict[str, Any]:
    """Build a deterministic cross-asset evidence packet from a local CSV."""

    provenance = _load_provenance_payload(input_path)
    rows_by_symbol = _load_symbol_rows(input_path, symbols)
    assets: list[dict[str, Any]] = []
    for symbol in symbols:
        bars = _rows_to_bars(rows_by_symbol[symbol])
        payload = _run_symbol_backtest(
            bars=bars,
            symbol=symbol,
            short_window=short_window,
            long_window=long_window,
            fee_bps=fee_bps,
            data_provenance=provenance,
        )
        card = build_scenario_card(payload, input_path)
        assets.append(
            {
                "symbol": symbol,
                "source": {
                    "input_path": str(input_path),
                    "first_date": payload["first_date"],
                    "last_date": payload["last_date"],
                    "row_count": payload["row_count"],
                },
                "strategy_config": payload["strategy_config"],
                "metrics": payload["metrics"],
                "exposure_trade_review": payload["exposure_trade_review"],
                "scenario_risk_interpretation": payload[
                    "scenario_risk_interpretation"
                ],
                "scenario_card": card,
                "scenario_card_markdown": render_scenario_card(card),
            }
        )

    return {
        "packet_type": "cross_asset_thesis_ledger_evidence_packet",
        "schema_version": "1.0",
        "research_only": True,
        "historical_diagnostics_only": True,
        "offline_only": True,
        "no_broker_or_live_data": True,
        "note": THESIS_LEDGER_NOTE,
        "source": {
            "input_path": str(input_path),
            "symbols": list(symbols),
            "first_date": assets[0]["source"]["first_date"] if assets else None,
            "last_date": assets[0]["source"]["last_date"] if assets else None,
            "rows_per_symbol": {
                asset["symbol"]: asset["source"]["row_count"] for asset in assets
            },
        },
        "strategy_config": {
            "short_window": short_window,
            "long_window": long_window,
            "fee_bps": fee_bps,
        },
        "assumptions": list(THESIS_LEDGER_ASSUMPTIONS),
        "assets": assets,
        "cross_asset_evidence": _build_cross_asset_evidence(assets),
        "risk_boundaries": {
            "non_advice": THESIS_LEDGER_NOTE,
            "leveraged_etf_like": LEVERAGED_ETF_RISK_BOUNDARY,
            "scope_limits": THESIS_LEDGER_SCOPE_LIMITS,
        },
        "data_provenance": provenance,
    }


def render_cross_asset_thesis_ledger(packet: Mapping[str, Any]) -> str:
    """Render a cross-asset thesis-ledger packet as Markdown."""

    source = _mapping(packet.get("source"))
    config = _mapping(packet.get("strategy_config"))
    evidence = _mapping(packet.get("cross_asset_evidence"))
    boundaries = _mapping(packet.get("risk_boundaries"))
    assets = packet.get("assets", ())

    lines = [
        "# Cross-Asset Thesis-Ledger Evidence Packet",
        "",
        f"- {_format_value(packet.get('note', THESIS_LEDGER_NOTE))}",
        "- Built from bundled static sample rows only; no live data is requested.",
        "",
        "## Source",
        "",
        f"- **Input path**: {_format_value(source.get('input_path'))}",
        f"- **Symbols**: {_format_inline_list(source.get('symbols', ()))}",
        f"- **Date range**: {_format_value(source.get('first_date'))} to "
        f"{_format_value(source.get('last_date'))}",
        f"- **Rows per symbol**: {_format_mapping(source.get('rows_per_symbol'))}",
        "",
        "## Strategy Configuration",
        "",
        f"- **Short window**: {_format_value(config.get('short_window'))}",
        f"- **Long window**: {_format_value(config.get('long_window'))}",
        f"- **Fee bps**: {_format_value(config.get('fee_bps'))}",
        "",
        "## Assumptions",
        "",
        *[f"- {item}" for item in packet.get("assumptions", ())],
        "",
        "## Cross-Asset Evidence",
        "",
        (
            "| symbol | strategy_return | buy_and_hold_return | "
            "strategy_minus_buy_hold | max_drawdown | exposure | "
            "exposure_changes | fee_drag |"
        ),
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in evidence.get("rows", ()):
        metrics = _mapping(row.get("metrics"))
        exposure = _mapping(row.get("exposure_trade_review"))
        lines.append(
            "| "
            f"{_format_value(row.get('symbol'))} | "
            f"{_format_percent(metrics.get('total_return'))} | "
            f"{_format_percent(metrics.get('buy_and_hold_total_return'))} | "
            f"{_format_percent(metrics.get('strategy_minus_buy_and_hold_return'))} | "
            f"{_format_percent(metrics.get('max_drawdown'))} | "
            f"{_format_percent(exposure.get('percent_periods_in_market'))} | "
            f"{_format_value(exposure.get('exposure_changes'))} | "
            f"{_format_percent(exposure.get('total_fee_drag'))} |"
        )

    lines.extend(
        [
            "",
            "## Evidence Notes",
            "",
            *[f"- {item}" for item in evidence.get("notes", ())],
            "",
        ]
    )

    for asset in assets if _is_non_text_sequence(assets) else ():
        if not isinstance(asset, Mapping):
            continue
        metrics = _mapping(asset.get("metrics"))
        exposure = _mapping(asset.get("exposure_trade_review"))
        scenario = _mapping(asset.get("scenario_risk_interpretation"))
        lines.extend(
            [
                f"## {asset.get('symbol')} Evidence",
                "",
                f"- **Strategy total return**: {_format_percent(metrics.get('total_return'))}",
                (
                    "- **Buy-and-hold total return**: "
                    f"{_format_percent(metrics.get('buy_and_hold_total_return'))}"
                ),
                (
                    "- **Strategy minus buy-and-hold return**: "
                    f"{_format_percent(metrics.get('strategy_minus_buy_and_hold_return'))}"
                ),
                f"- **Max drawdown**: {_format_percent(metrics.get('max_drawdown'))}",
                f"- **Average exposure**: {_format_percent(exposure.get('average_exposure'))}",
                f"- **Exposure changes**: {_format_value(exposure.get('exposure_changes'))}",
                f"- **Modeled fee drag**: {_format_percent(exposure.get('total_fee_drag'))}",
                f"- **Scenario/risk note**: {_format_value(scenario.get('note'))}",
                "",
            ]
        )

    lines.extend(
        [
            "## Embedded Scenario Cards",
            "",
            "- JSON includes one reusable scenario_card object and one rendered scenario_card_markdown string per symbol.",
            "- The embedded cards reuse the existing scenario-card helper and remain historical diagnostics only.",
            "",
            "## Risk Boundaries",
            "",
            f"- **Non-advice boundary**: {_format_value(boundaries.get('non_advice'))}",
            (
                "- **Leveraged ETF-like boundary**: "
                f"{_format_value(boundaries.get('leveraged_etf_like'))}"
            ),
            f"- **Scope limits**: {_format_value(boundaries.get('scope_limits'))}",
        ]
    )

    return "\n".join(lines) + "\n"


def _run_symbol_backtest(
    bars: Sequence[PriceBar],
    symbol: str,
    short_window: int,
    long_window: int,
    fee_bps: float,
    data_provenance: Mapping[str, Any] | None,
) -> dict[str, Any]:
    signals = moving_average_crossover_strategy(
        bars,
        short_window=short_window,
        long_window=long_window,
    )
    curve = backtest_long_cash(
        bars=bars,
        target_exposures=[signal.target_exposure for signal in signals],
        fee_bps=fee_bps,
    )
    strategy_returns = [record.strategy_return for record in curve[1:]]
    buy_and_hold_returns = [record.market_return for record in curve[1:]]
    strategy_total = total_return(strategy_returns)
    buy_and_hold_total = total_return(buy_and_hold_returns)
    metrics = {
        "total_return": strategy_total,
        "buy_and_hold_total_return": buy_and_hold_total,
        "strategy_minus_buy_and_hold_return": strategy_total - buy_and_hold_total,
        "annualized_return": annualized_return(strategy_returns),
        "max_drawdown": max_drawdown(strategy_returns),
        "volatility": volatility(strategy_returns),
        "sharpe_like": sharpe_like(strategy_returns),
        "win_rate": win_rate_from_returns(strategy_returns),
    }
    payload: dict[str, Any] = {
        "strategy_config": {
            "short_window": short_window,
            "long_window": long_window,
            "symbol": symbol,
            "fee_bps": fee_bps,
        },
        "metrics": metrics,
        "exposure_trade_review": build_exposure_trade_review(curve),
        "scenario_risk_interpretation": build_scenario_risk_interpretation(
            curve,
            metrics,
        ),
        "first_date": bars[0].date.isoformat() if bars else None,
        "last_date": bars[-1].date.isoformat() if bars else None,
        "row_count": len(bars),
    }
    if data_provenance is not None:
        payload["data_provenance"] = data_provenance
    return payload


def _build_cross_asset_evidence(
    assets: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    rows = [
        {
            "symbol": asset["symbol"],
            "metrics": asset["metrics"],
            "exposure_trade_review": asset["exposure_trade_review"],
        }
        for asset in assets
    ]
    return {
        "rows": rows,
        "notes": [
            "Rows are ordered QQQ_LIKE, QLD_LIKE, TQQQ_LIKE for stable diffs.",
            "Cross-asset differences are historical sample diagnostics only, not rankings or recommendations.",
            "The LIKE suffix marks placeholders; these rows are not real fund prices.",
        ],
    }


def _load_symbol_rows(
    input_path: Path,
    symbols: Sequence[str],
) -> dict[str, list[dict[str, str]]]:
    with input_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV is missing a header row")
        if "symbol" not in reader.fieldnames:
            raise ValueError("CSV is missing required column(s): symbol")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV is missing required column(s): {', '.join(missing)}")
        rows = list(reader)

    rows_by_symbol = {
        symbol: [row for row in rows if row.get("symbol") == symbol]
        for symbol in symbols
    }
    for symbol, symbol_rows in rows_by_symbol.items():
        if not symbol_rows:
            raise ValueError(f"No rows found for symbol {symbol!r}")
    return rows_by_symbol


def _rows_to_bars(rows: Sequence[dict[str, str]]) -> list[PriceBar]:
    source = StringIO()
    writer = csv.DictWriter(source, fieldnames=list(REQUIRED_COLUMNS))
    writer.writeheader()
    for row in rows:
        writer.writerow({column: row[column] for column in REQUIRED_COLUMNS})
    source.seek(0)
    return load_ohlc_csv(source)


def _load_provenance_payload(input_path: Path) -> dict[str, Any] | None:
    provenance = load_static_fixture_provenance(input_path)
    if provenance is None:
        return None
    return provenance.as_dict()


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _format_percent(value: Any) -> str:
    if isinstance(value, int | float) and not isinstance(value, bool):
        return f"{value * 100:.2f}%"
    return "n/a"


def _format_value(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _format_inline_list(value: Any) -> str:
    if _is_non_text_sequence(value):
        return ", ".join(str(item) for item in value)
    return _format_value(value)


def _format_mapping(value: Any) -> str:
    if not isinstance(value, Mapping):
        return "n/a"
    return ", ".join(f"{key}={value[key]}" for key in sorted(value))


def _is_non_text_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    )
