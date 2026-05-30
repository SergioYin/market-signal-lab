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
THESIS_LEDGER_ACCEPTANCE_NOTE = (
    "Research-only thesis-ledger acceptance summary for an offline JSON artifact; "
    "not investment advice, not trading guidance, not a recommendation, not a "
    "prediction, and not a broker connection or execution feature."
)
THESIS_LEDGER_REQUIRED_TOP_LEVEL_KEYS = (
    "packet_type",
    "schema_version",
    "research_only",
    "historical_diagnostics_only",
    "offline_only",
    "no_broker_or_live_data",
    "note",
    "source",
    "strategy_config",
    "assumptions",
    "assets",
    "cross_asset_evidence",
    "risk_boundaries",
)
THESIS_LEDGER_REQUIRED_ASSET_KEYS = (
    "symbol",
    "source",
    "strategy_config",
    "metrics",
    "exposure_trade_review",
    "scenario_risk_interpretation",
    "scenario_card",
    "scenario_card_markdown",
)
THESIS_LEDGER_REQUIRED_METRIC_KEYS = (
    "total_return",
    "buy_and_hold_total_return",
    "strategy_minus_buy_and_hold_return",
    "annualized_return",
    "max_drawdown",
    "volatility",
    "sharpe_like",
    "win_rate",
)
THESIS_LEDGER_REQUIRED_EXPOSURE_KEYS = (
    "period_count",
    "periods_in_market",
    "periods_in_cash",
    "percent_periods_in_market",
    "percent_periods_in_cash",
    "average_exposure",
    "exposure_changes",
    "entries_to_market",
    "exits_to_cash",
    "total_fee_drag",
    "research_only",
    "note",
)
THESIS_LEDGER_REQUIRED_RISK_BOUNDARIES = (
    "non_advice",
    "leveraged_etf_like",
    "scope_limits",
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


def validate_cross_asset_thesis_ledger_packet(packet: Any) -> dict[str, Any]:
    """Validate a cross-asset thesis-ledger packet without raising on failure."""

    checks: list[dict[str, Any]] = []

    def record(check: str, accepted: bool, message: str) -> None:
        checks.append(
            {
                "check": check,
                "accepted": accepted,
                "message": message,
            }
        )

    if not isinstance(packet, Mapping):
        record("packet_object", False, "Packet must be a JSON object.")
        return _build_acceptance_summary(packet, checks)

    missing_top = [
        key for key in THESIS_LEDGER_REQUIRED_TOP_LEVEL_KEYS if key not in packet
    ]
    record(
        "top_level_keys",
        not missing_top,
        (
            "Required top-level keys are present."
            if not missing_top
            else f"Missing top-level key(s): {', '.join(missing_top)}."
        ),
    )
    record(
        "packet_type",
        packet.get("packet_type") == "cross_asset_thesis_ledger_evidence_packet",
        "Packet type must be cross_asset_thesis_ledger_evidence_packet.",
    )
    record(
        "schema_version",
        packet.get("schema_version") == "1.0",
        "Schema version must be 1.0.",
    )
    for flag in (
        "research_only",
        "historical_diagnostics_only",
        "offline_only",
        "no_broker_or_live_data",
    ):
        record(flag, packet.get(flag) is True, f"{flag} must be true.")

    note = packet.get("note")
    record(
        "non_advice_note",
        isinstance(note, str) and _contains_all(note, ("not investment advice",)),
        "Note must preserve the non-advice boundary.",
    )

    source = packet.get("source")
    record("source_shape", isinstance(source, Mapping), "source must be an object.")
    if isinstance(source, Mapping):
        record(
            "source_symbols",
            _is_non_text_sequence(source.get("symbols")),
            "source.symbols must be a list of reviewed symbols.",
        )

    assets = packet.get("assets")
    assets_valid = _is_non_text_sequence(assets) and all(
        isinstance(asset, Mapping) for asset in assets
    )
    record(
        "assets_shape",
        assets_valid,
        "assets must be a list of asset objects.",
    )
    asset_symbols: list[str] = []
    if assets_valid:
        for index, asset in enumerate(assets):
            symbol = asset.get("symbol")
            label = str(symbol) if isinstance(symbol, str) else f"asset[{index}]"
            if isinstance(symbol, str):
                asset_symbols.append(symbol)
            _validate_asset_shape(asset, label, record)

    evidence = packet.get("cross_asset_evidence")
    record(
        "cross_asset_evidence_shape",
        isinstance(evidence, Mapping) and _is_non_text_sequence(evidence.get("rows")),
        "cross_asset_evidence.rows must be present.",
    )
    if isinstance(evidence, Mapping) and _is_non_text_sequence(evidence.get("rows")):
        evidence_symbols = [
            row.get("symbol")
            for row in evidence["rows"]
            if isinstance(row, Mapping) and isinstance(row.get("symbol"), str)
        ]
        record(
            "cross_asset_evidence_symbols",
            evidence_symbols == asset_symbols,
            "cross_asset_evidence.rows symbols must match assets order.",
        )

    risk_boundaries = packet.get("risk_boundaries")
    boundaries_ok = isinstance(risk_boundaries, Mapping) and all(
        isinstance(risk_boundaries.get(key), str)
        and risk_boundaries.get(key, "").strip()
        for key in THESIS_LEDGER_REQUIRED_RISK_BOUNDARIES
    )
    record(
        "risk_boundaries",
        boundaries_ok,
        "Risk boundaries must include non_advice, leveraged_etf_like, and scope_limits.",
    )
    if isinstance(risk_boundaries, Mapping):
        record(
            "risk_boundary_text",
            _contains_all(
                " ".join(
                    str(risk_boundaries.get(key, ""))
                    for key in THESIS_LEDGER_REQUIRED_RISK_BOUNDARIES
                ).lower(),
                ("not investment advice", "no live data", "broker"),
            ),
            "Risk boundaries must preserve non-advice, no-live-data, and broker limits.",
        )

    return _build_acceptance_summary(packet, checks, asset_symbols=asset_symbols)


def render_thesis_ledger_acceptance_summary(summary: Mapping[str, Any]) -> str:
    """Render a thesis-ledger acceptance summary as Markdown."""

    lines = [
        "# Thesis-Ledger Acceptance Summary",
        "",
        f"- {_format_value(summary.get('note', THESIS_LEDGER_ACCEPTANCE_NOTE))}",
        f"- **Accepted**: {_format_value(summary.get('accepted'))}",
        f"- **Packet type**: {_format_value(summary.get('packet_type'))}",
        f"- **Packet schema version**: {_format_value(summary.get('packet_schema_version'))}",
        f"- **Acceptance schema version**: {_format_value(summary.get('schema_version'))}",
        f"- **Assets reviewed**: {_format_inline_list(summary.get('asset_symbols', ()))}",
        f"- **Error count**: {_format_value(summary.get('error_count'))}",
        f"- **Warning count**: {_format_value(summary.get('warning_count'))}",
        "",
        "## Checks",
        "",
        "| check | accepted | message |",
        "|---|---|---|",
    ]
    for check in summary.get("checks", ()):
        if not isinstance(check, Mapping):
            continue
        lines.append(
            "| "
            f"{_escape_table_cell(_format_value(check.get('check')))} | "
            f"{_format_value(check.get('accepted'))} | "
            f"{_escape_table_cell(_format_value(check.get('message')))} |"
        )

    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "- Validation is limited to the JSON packet shape and public research boundaries.",
            "- It does not fetch live data, connect to brokers, create orders, size positions, make forecasts, or provide recommendations.",
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


def _validate_asset_shape(
    asset: Mapping[str, Any],
    label: str,
    record: Any,
) -> None:
    missing = [key for key in THESIS_LEDGER_REQUIRED_ASSET_KEYS if key not in asset]
    record(
        f"asset.{label}.keys",
        not missing,
        (
            f"{label} contains required asset keys."
            if not missing
            else f"{label} missing key(s): {', '.join(missing)}."
        ),
    )
    record(
        f"asset.{label}.symbol",
        isinstance(asset.get("symbol"), str) and bool(asset.get("symbol")),
        f"{label} symbol must be a non-empty string.",
    )
    record(
        f"asset.{label}.source",
        isinstance(asset.get("source"), Mapping),
        f"{label} source must be an object.",
    )
    record(
        f"asset.{label}.strategy_config",
        isinstance(asset.get("strategy_config"), Mapping),
        f"{label} strategy_config must be an object.",
    )

    metrics = asset.get("metrics")
    metrics_ok = isinstance(metrics, Mapping) and all(
        _is_number(metrics.get(key)) for key in THESIS_LEDGER_REQUIRED_METRIC_KEYS
    )
    record(
        f"asset.{label}.metrics",
        metrics_ok,
        f"{label} metrics must include numeric thesis-ledger metric fields.",
    )

    exposure = asset.get("exposure_trade_review")
    exposure_ok = isinstance(exposure, Mapping) and all(
        key in exposure for key in THESIS_LEDGER_REQUIRED_EXPOSURE_KEYS
    )
    record(
        f"asset.{label}.exposure_trade_review",
        exposure_ok,
        f"{label} exposure_trade_review must include review metadata fields.",
    )
    if isinstance(exposure, Mapping):
        record(
            f"asset.{label}.exposure_research_boundary",
            exposure.get("research_only") is True,
            f"{label} exposure review must remain research_only.",
        )

    scenario = asset.get("scenario_risk_interpretation")
    scenario_ok = (
        isinstance(scenario, Mapping)
        and scenario.get("research_only") is True
        and scenario.get("historical_diagnostics_only") is True
        and isinstance(scenario.get("note"), str)
        and "not investment advice" in scenario.get("note", "").lower()
    )
    record(
        f"asset.{label}.scenario_risk_interpretation",
        scenario_ok,
        f"{label} scenario risk interpretation must preserve research-only boundaries.",
    )
    card = asset.get("scenario_card")
    record(
        f"asset.{label}.scenario_card",
        isinstance(card, Mapping) and card.get("card_type") == "scenario_card",
        f"{label} scenario_card must be an embedded scenario_card object.",
    )
    record(
        f"asset.{label}.scenario_card_markdown",
        isinstance(asset.get("scenario_card_markdown"), str)
        and "# Scenario Card" in asset.get("scenario_card_markdown", ""),
        f"{label} scenario_card_markdown must contain rendered scenario card Markdown.",
    )


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


def _build_acceptance_summary(
    packet: Any,
    checks: Sequence[Mapping[str, Any]],
    asset_symbols: Sequence[str] = (),
) -> dict[str, Any]:
    error_count = sum(1 for check in checks if check.get("accepted") is not True)
    packet_mapping = packet if isinstance(packet, Mapping) else {}
    return {
        "summary_type": "cross_asset_thesis_ledger_acceptance",
        "schema_version": "1.0",
        "accepted": error_count == 0,
        "error_count": error_count,
        "warning_count": 0,
        "packet_type": packet_mapping.get("packet_type"),
        "packet_schema_version": packet_mapping.get("schema_version"),
        "asset_symbols": list(asset_symbols),
        "checks": [dict(check) for check in checks],
        "research_only": True,
        "historical_diagnostics_only": True,
        "offline_only": True,
        "no_broker_or_live_data": True,
        "note": THESIS_LEDGER_ACCEPTANCE_NOTE,
    }


def _contains_all(value: str, fragments: Sequence[str]) -> bool:
    lowered = value.lower()
    return all(fragment in lowered for fragment in fragments)


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def _escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|")


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
