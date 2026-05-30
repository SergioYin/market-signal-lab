"""Pre-trade research packet rendering for single backtest outputs."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

PRETRADE_PACKET_NOTE = (
    "Research-only packet built from historical sample/backtest data; not "
    "investment advice, not trading guidance, not a recommendation, not a "
    "prediction, and not a broker connection or execution feature."
)

LEVERAGED_ETF_RISK_BOUNDARY = (
    "Leveraged ETF-like examples require extra caution. Daily reset mechanics "
    "make multi-day outcomes path-dependent; losses can grow quickly; and real "
    "fund results can differ because of expenses, financing costs, tracking "
    "differences, taxes, liquidity, spreads, and market impact that this packet "
    "does not model."
)

SAMPLE_BACKTEST_LIMITATION = (
    "Backtest and sample results are limited to the supplied historical rows and "
    "simplified assumptions. They are examples for review only, not evidence of "
    "future returns."
)

BEGINNER_CHECKLIST = (
    "Confirm the CSV path, symbol filter, row count, and date range match the review.",
    "Read static fixture provenance before interpreting any metric.",
    "Compare strategy return with same-period buy-and-hold return.",
    "Review exposure, cash time, exposure changes, and modeled fee drag.",
    "Check max drawdown as an interim-loss diagnostic, not a forecast.",
    "Treat all modeled states as historical diagnostics, not instructions.",
    "For leveraged ETF-like labels, read the daily-reset and path-dependency boundary.",
)


def build_pretrade_research_packet(
    backtest_payload: Mapping[str, Any],
    input_path: Path,
) -> dict[str, Any]:
    """Build a compact research packet from an existing backtest JSON payload."""

    strategy_config = dict(backtest_payload.get("strategy_config", {}))
    metrics = dict(backtest_payload.get("metrics", {}))
    exposure = dict(backtest_payload.get("exposure_trade_review", {}))
    scenario = dict(backtest_payload.get("scenario_risk_interpretation", {}))
    provenance = backtest_payload.get("data_provenance")

    assumptions = [
        "Uses the existing single-backtest moving-average workflow.",
        "Uses only the supplied local CSV path and optional symbol filter.",
        "Uses historical close-to-close sample rows; no live data is requested.",
        "Uses configured fee_bps as a simplified historical cost assumption.",
        "Does not connect to brokers, create orders, or provide execution steps.",
    ]
    if isinstance(provenance, Mapping):
        assumptions.append(
            "Adjacent static fixture provenance is included when available."
        )

    return {
        "packet_type": "pretrade_research_packet",
        "schema_version": "1.0",
        "research_only": True,
        "historical_diagnostics_only": True,
        "no_broker_or_live_data": True,
        "note": PRETRADE_PACKET_NOTE,
        "source": {
            "input_path": str(input_path),
            "first_date": backtest_payload.get("first_date"),
            "last_date": backtest_payload.get("last_date"),
            "row_count": backtest_payload.get("row_count"),
        },
        "strategy_config": strategy_config,
        "assumptions": assumptions,
        "historical_diagnostics": {
            "metrics": metrics,
            "exposure_trade_review": exposure,
            "scenario_risk_interpretation": scenario,
        },
        "beginner_checklist": [
            {"item": item, "status": "review_required"}
            for item in BEGINNER_CHECKLIST
        ],
        "risk_boundaries": {
            "non_advice": PRETRADE_PACKET_NOTE,
            "sample_backtest_limits": SAMPLE_BACKTEST_LIMITATION,
            "leveraged_etf_like": LEVERAGED_ETF_RISK_BOUNDARY,
            "scope_limits": (
                "Local artifact only. No broker workflow, live-data workflow, "
                "private account fields, order routing, position sizing "
                "instruction, or recommendation engine."
            ),
        },
    }


def render_pretrade_research_packet(packet: Mapping[str, Any]) -> str:
    """Render a pre-trade research packet as Markdown."""

    source = _mapping(packet.get("source"))
    metrics = _mapping(_diagnostics(packet).get("metrics"))
    exposure = _mapping(_diagnostics(packet).get("exposure_trade_review"))
    scenario = _mapping(_diagnostics(packet).get("scenario_risk_interpretation"))
    boundaries = _mapping(packet.get("risk_boundaries"))

    lines = [
        "# Pre-Trade Research Packet",
        "",
        f"- {packet['note']}",
        "- Built from the existing single-backtest path.",
        "",
        "## Source",
        "",
        f"- **Input path**: {_format_value(source.get('input_path'))}",
        f"- **Date range**: {_format_value(source.get('first_date'))} to "
        f"{_format_value(source.get('last_date'))}",
        f"- **Rows reviewed**: {_format_value(source.get('row_count'))}",
        "",
        "## Assumptions",
        "",
        *_render_list(packet.get("assumptions", ())),
        "",
        "## Historical Diagnostics",
        "",
        f"- **Strategy total return**: {_format_percent_metric(metrics, 'total_return')}",
        (
            "- **Buy-and-hold total return**: "
            f"{_format_percent_metric(metrics, 'buy_and_hold_total_return')}"
        ),
        (
            "- **Strategy minus buy-and-hold return**: "
            f"{_format_percent_metric(metrics, 'strategy_minus_buy_and_hold_return')}"
        ),
        f"- **Max drawdown**: {_format_percent_metric(metrics, 'max_drawdown')}",
        f"- **Average exposure**: {_format_percent_metric(exposure, 'average_exposure')}",
        f"- **Periods in market**: {_format_percent_metric(exposure, 'percent_periods_in_market')}",
        f"- **Exposure changes**: {_format_value(exposure.get('exposure_changes'))}",
        f"- **Modeled entries**: {_format_value(exposure.get('entries_to_market'))}",
        f"- **Modeled exits**: {_format_value(exposure.get('exits_to_cash'))}",
        f"- **Modeled fee drag**: {_format_percent_metric(exposure, 'total_fee_drag')}",
        "",
        "## Scenario/Risk Interpretation",
        "",
        *_render_scenario_summaries(scenario),
        "",
        "## Beginner Checklist",
        "",
        *_render_checklist(packet.get("beginner_checklist", ())),
        "",
        "## Risk Boundaries",
        "",
        f"- **Non-advice boundary**: {boundaries['non_advice']}",
        f"- **Sample/backtest limits**: {boundaries['sample_backtest_limits']}",
        f"- **Leveraged ETF-like boundary**: {boundaries['leveraged_etf_like']}",
        f"- **Scope limits**: {boundaries['scope_limits']}",
    ]

    return "\n".join(lines) + "\n"


def _diagnostics(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    diagnostics = packet.get("historical_diagnostics")
    if isinstance(diagnostics, Mapping):
        return diagnostics
    return {}


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _render_list(values: Any) -> list[str]:
    if not _is_non_text_sequence(values):
        return ["- No assumptions supplied."]
    return [f"- {value}" for value in values]


def _render_checklist(values: Any) -> list[str]:
    if not _is_non_text_sequence(values):
        return ["- [ ] No checklist supplied."]

    lines: list[str] = []
    for value in values:
        if isinstance(value, Mapping):
            lines.append(f"- [ ] {value.get('item', '')}")
        else:
            lines.append(f"- [ ] {value}")
    return lines


def _render_scenario_summaries(scenario: Mapping[str, Any]) -> list[str]:
    if not scenario:
        return ["- No scenario/risk interpretation was available."]

    lines = [f"- {scenario.get('note', '')}"]
    for label, key in (
        ("Exposure", "exposure"),
        ("Drawdown", "drawdown"),
        ("Fee drag", "fee_drag"),
        ("Buy-and-hold comparison", "buy_and_hold_comparison"),
    ):
        value = scenario.get(key)
        if isinstance(value, Mapping) and value.get("summary"):
            lines.append(f"- **{label}**: {value['summary']}")
    return lines


def _format_percent_metric(values: Mapping[str, Any], key: str) -> str:
    value = values.get(key)
    if isinstance(value, int | float) and not isinstance(value, bool):
        return f"{value * 100:.2f}%"
    return "n/a"


def _format_value(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _is_non_text_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    )
