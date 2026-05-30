"""Compact scenario-card artifacts for single backtest outputs."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from market_signal_lab.packet import SAMPLE_BACKTEST_LIMITATION

SCENARIO_CARD_NOTE = (
    "Research-only scenario card built from historical sample/backtest data; "
    "not investment advice, not trading guidance, not a recommendation, not a "
    "prediction, and not a broker connection or execution feature."
)
SCENARIO_CARD_LEVERAGED_ETF_RISK = (
    "Leveraged ETF-like examples require extra caution. Daily reset mechanics "
    "make multi-day outcomes path-dependent; losses can grow quickly; and real "
    "fund results can differ because of expenses, financing costs, tracking "
    "differences, taxes, liquidity, spreads, and market impact that this card "
    "does not model."
)
SCENARIO_CARD_SCOPE_LIMITS = (
    "Local artifact only. No broker workflow, live-data workflow, private "
    "account fields, order routing, position sizing instruction, forecast, or "
    "recommendation engine."
)

NEXT_REVIEW_CHECKLIST = (
    "Confirm input path, symbol filter, date range, and row count.",
    "Review assumptions and static fixture provenance when present.",
    "Compare key metrics with same-period buy-and-hold.",
    "Check exposure, fee drag, and max drawdown diagnostics.",
    "Re-read leveraged ETF-like daily-reset and path-dependency limits.",
)


def build_scenario_card(
    backtest_payload: Mapping[str, Any],
    input_path: Path,
) -> dict[str, Any]:
    """Build a compact research-only scenario card from a backtest payload."""

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
        assumptions.append("Includes adjacent static fixture provenance when available.")

    return {
        "card_type": "scenario_card",
        "schema_version": "1.0",
        "research_only": True,
        "historical_diagnostics_only": True,
        "no_broker_or_live_data": True,
        "note": SCENARIO_CARD_NOTE,
        "source": {
            "input_path": str(input_path),
            "first_date": backtest_payload.get("first_date"),
            "last_date": backtest_payload.get("last_date"),
            "row_count": backtest_payload.get("row_count"),
        },
        "strategy_config": dict(backtest_payload.get("strategy_config", {})),
        "assumptions": assumptions,
        "key_metrics": {
            "total_return": metrics.get("total_return"),
            "buy_and_hold_total_return": metrics.get("buy_and_hold_total_return"),
            "strategy_minus_buy_and_hold_return": metrics.get(
                "strategy_minus_buy_and_hold_return"
            ),
            "max_drawdown": metrics.get("max_drawdown"),
            "volatility": metrics.get("volatility"),
            "sharpe_like": metrics.get("sharpe_like"),
            "win_rate": metrics.get("win_rate"),
        },
        "diagnostics": {
            "exposure": {
                "average_exposure": exposure.get("average_exposure"),
                "percent_periods_in_market": exposure.get("percent_periods_in_market"),
                "exposure_changes": exposure.get("exposure_changes"),
                "entries_to_market": exposure.get("entries_to_market"),
                "exits_to_cash": exposure.get("exits_to_cash"),
            },
            "fees": {
                "total_fee_drag": exposure.get("total_fee_drag"),
            },
            "drawdown": {
                "max_drawdown": metrics.get("max_drawdown"),
            },
            "scenario_risk_interpretation": scenario,
        },
        "risk_labels": {
            "non_advice": SCENARIO_CARD_NOTE,
            "sample_backtest_limits": SAMPLE_BACKTEST_LIMITATION,
            "leveraged_etf_like": SCENARIO_CARD_LEVERAGED_ETF_RISK,
            "scope_limits": SCENARIO_CARD_SCOPE_LIMITS,
        },
        "next_review_checklist": [
            {"item": item, "status": "review_required"}
            for item in NEXT_REVIEW_CHECKLIST
        ],
    }


def render_scenario_card(card: Mapping[str, Any]) -> str:
    """Render a scenario card as compact Markdown."""

    source = _mapping(card.get("source"))
    metrics = _mapping(card.get("key_metrics"))
    diagnostics = _mapping(card.get("diagnostics"))
    exposure = _mapping(diagnostics.get("exposure"))
    fees = _mapping(diagnostics.get("fees"))
    drawdown = _mapping(diagnostics.get("drawdown"))
    scenario = _mapping(diagnostics.get("scenario_risk_interpretation"))
    labels = _mapping(card.get("risk_labels"))

    lines = [
        "# Scenario Card",
        "",
        f"- {_format_value(card.get('note', SCENARIO_CARD_NOTE))}",
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
        *_render_list(card.get("assumptions", ())),
        "",
        "## Key Metrics",
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
        f"- **Volatility**: {_format_percent_metric(metrics, 'volatility')}",
        f"- **Sharpe-like score**: {_format_value(metrics.get('sharpe_like'))}",
        f"- **Win rate**: {_format_percent_metric(metrics, 'win_rate')}",
        "",
        "## Diagnostics",
        "",
        f"- **Average exposure**: {_format_percent_metric(exposure, 'average_exposure')}",
        (
            "- **Periods in market**: "
            f"{_format_percent_metric(exposure, 'percent_periods_in_market')}"
        ),
        f"- **Exposure changes**: {_format_value(exposure.get('exposure_changes'))}",
        f"- **Modeled entries**: {_format_value(exposure.get('entries_to_market'))}",
        f"- **Modeled exits**: {_format_value(exposure.get('exits_to_cash'))}",
        f"- **Modeled fee drag**: {_format_percent_metric(fees, 'total_fee_drag')}",
        f"- **Drawdown diagnostic**: {_format_percent_metric(drawdown, 'max_drawdown')}",
        "",
        "## Scenario/Risk Interpretation",
        "",
        *_render_scenario_summaries(scenario),
        "",
        "## Risk Labels",
        "",
        f"- **Non-advice**: {_risk_label(labels, 'non_advice', SCENARIO_CARD_NOTE)}",
        (
            "- **Sample/backtest limits**: "
            f"{_risk_label(labels, 'sample_backtest_limits', SAMPLE_BACKTEST_LIMITATION)}"
        ),
        (
            "- **Leveraged ETF-like risk**: "
            f"{_risk_label(labels, 'leveraged_etf_like', SCENARIO_CARD_LEVERAGED_ETF_RISK)}"
        ),
        f"- **Scope limits**: {_risk_label(labels, 'scope_limits', SCENARIO_CARD_SCOPE_LIMITS)}",
        "",
        "## Next Review Checklist",
        "",
        *_render_checklist(card.get("next_review_checklist", ())),
    ]

    return "\n".join(lines) + "\n"


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _render_list(values: Any) -> list[str]:
    if not _is_non_text_sequence(values) or len(values) == 0:
        return ["- No assumptions supplied."]
    return [f"- {_format_value(value)}" for value in values]


def _render_checklist(values: Any) -> list[str]:
    if not _is_non_text_sequence(values) or len(values) == 0:
        return ["- [ ] No checklist supplied."]

    lines: list[str] = []
    for value in values:
        if isinstance(value, Mapping):
            lines.append(f"- [ ] {_format_value(value.get('item'))}")
        else:
            lines.append(f"- [ ] {_format_value(value)}")
    return lines


def _render_scenario_summaries(scenario: Mapping[str, Any]) -> list[str]:
    if not scenario:
        return ["- No scenario/risk interpretation was available."]

    lines: list[str] = []
    note = scenario.get("note")
    if note:
        lines.append(f"- {note}")
    for label, key in (
        ("Exposure", "exposure"),
        ("Drawdown", "drawdown"),
        ("Fee drag", "fee_drag"),
        ("Buy-and-hold comparison", "buy_and_hold_comparison"),
    ):
        value = scenario.get(key)
        if isinstance(value, Mapping) and value.get("summary"):
            lines.append(f"- **{label}**: {value['summary']}")
    if not lines:
        return ["- No scenario/risk interpretation was available."]
    return lines


def _risk_label(labels: Mapping[str, Any], key: str, fallback: str) -> str:
    value = labels.get(key)
    if value:
        return str(value)
    return fallback


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
