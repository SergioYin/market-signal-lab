"""Markdown report rendering for strategy experiments."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any

from market_signal_lab.backtest import EquityCurveRecord

LEVERAGED_ETF_SYMBOLS = frozenset({"TQQQ", "QLD"})
EXPOSURE_TRADE_REVIEW_NOTE = (
    "Historical exposure metadata only; these model states are not "
    "investment advice, trading guidance, executed trades, or instructions "
    "to buy, sell, hold, or size a position."
)
SCENARIO_RISK_INTERPRETATION_NOTE = (
    "Historical diagnostics only; this scenario/risk interpretation is not "
    "investment advice, trading guidance, a prediction, or a broker connection "
    "or execution feature."
)
REGIME_COMPARISON_NOTE = (
    "Research-only historical comparison of deterministic bundled fixtures; "
    "not investment advice, not a recommendation, not a prediction, and not "
    "a broker connection or execution feature."
)
SCENARIO_RISK_INTERPRETATION_KEYS = frozenset(
    {
        "research_only",
        "historical_diagnostics_only",
        "note",
        "exposure",
        "drawdown",
        "fee_drag",
        "buy_and_hold_comparison",
    }
)
SCENARIO_RISK_EXPOSURE_KEYS = frozenset(
    {
        "period_count",
        "average_exposure",
        "percent_periods_in_market",
        "summary",
    }
)
SCENARIO_RISK_DRAWDOWN_KEYS = frozenset({"max_drawdown", "summary"})
SCENARIO_RISK_FEE_DRAG_KEYS = frozenset({"total_fee_drag", "summary"})
SCENARIO_RISK_COMPARISON_KEYS = frozenset(
    {
        "strategy_total_return",
        "buy_and_hold_total_return",
        "strategy_minus_buy_and_hold_return",
        "summary",
    }
)
METRIC_LABELS = {
    "total_return": "Strategy total return",
    "buy_and_hold_total_return": "Buy-and-hold total return",
    "strategy_minus_buy_and_hold_return": "Strategy minus buy-and-hold return",
    "annualized_return": "Annualized return",
    "max_drawdown": "Max drawdown",
    "volatility": "Volatility",
    "sharpe_like": "Sharpe-like score",
    "win_rate": "Win rate",
}


def render_experiment_report(
    strategy_config: Mapping[str, Any],
    backtest_curve: Sequence[EquityCurveRecord],
    metrics: Mapping[str, float],
    risk_notes: Sequence[str] = (),
    validation_split: Mapping[str, Any] | None = None,
    data_provenance: Mapping[str, Any] | None = None,
) -> str:
    """Render a Markdown report for one strategy/backtest experiment."""

    lines = [
        "# Market Signal Experiment Report",
        "",
        "## Strategy Config",
        "",
        *_render_mapping(strategy_config),
        "",
        "## Backtest Summary",
        "",
        *_render_backtest_summary(backtest_curve),
        "",
        "## Modeled Exposure Review",
        "",
        *_render_exposure_trade_review(build_exposure_trade_review(backtest_curve)),
        "",
        "## Scenario/Risk Interpretation",
        "",
        *_render_scenario_risk_interpretation(
            build_scenario_risk_interpretation(backtest_curve, metrics)
        ),
        "",
        "## Metrics",
        "",
        *_render_metrics(metrics),
        "",
        *render_validation_split_note(validation_split),
        *render_data_provenance_note(data_provenance),
        "## Risk Notes",
        "",
        *_render_risk_notes(strategy_config, risk_notes),
        "",
        "## Backtest Caveats",
        "",
        "- Backtest results are hypothetical and do not guarantee future performance.",
        (
            "- Model exposure states are calculated from historical data only. "
            "They can be affected by data quality, survivorship bias, and "
            "parameter overfitting, and they are not trading instructions."
        ),
        (
            "- Reported returns are model outputs before taxes, market impact, "
            "and any costs not explicitly included in the backtest."
        ),
    ]

    return "\n".join(lines) + "\n"


def render_regime_comparison_report(
    regimes: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> str:
    """Render a Markdown comparison across deterministic bundled regimes."""

    lines = [
        "# Regime Comparison Report",
        "",
        f"- {REGIME_COMPARISON_NOTE}",
        (
            "- To reproduce this checked sample from the repository root, run "
            "market-signal-lab --regime-comparison."
        ),
        (
            "- Open reports/regime-comparison.md first for the readable "
            "review, reports/regime-comparison.html for a browser view, or "
            "reports/regime-comparison.json for structured data."
        ),
        "- Buy-and-hold values use the same close-to-close sample as each strategy run.",
        "- Exposure and cash-time are historical model states, not trades or instructions.",
        "",
        "## Comparison Table",
        "",
        (
            "| regime | symbol | strategy_return | buy_and_hold_return | "
            "strategy_minus_buy_hold | max_drawdown | exposure | cash_time | "
            "exposure_changes | whipsaw_rate |"
        ),
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for regime in regimes:
        metrics = regime["metrics"]
        exposure = regime["exposure_trade_review"]
        lines.append(
            "| "
            f"{regime['regime_label']} | "
            f"{regime['symbol']} | "
            f"{_format_percent(metrics['total_return'])} | "
            f"{_format_percent(metrics['buy_and_hold_total_return'])} | "
            f"{_format_percent(metrics['strategy_minus_buy_and_hold_return'])} | "
            f"{_format_percent(metrics['max_drawdown'])} | "
            f"{_format_percent(exposure['percent_periods_in_market'])} | "
            f"{_format_percent(exposure['percent_periods_in_cash'])} | "
            f"{exposure['exposure_changes']} | "
            f"{_format_percent(regime['interpretation']['whipsaw_rate'])} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- **Best strategy total return**: {summary['best_strategy_total_return_symbol']}.",
            (
                "- **Best buy-and-hold total return**: "
                f"{summary['best_buy_and_hold_total_return_symbol']}."
            ),
            f"- **Largest modeled drawdown**: {summary['largest_drawdown_symbol']}.",
            f"- **Highest whipsaw pressure**: {summary['highest_whipsaw_symbol']}.",
            f"- **Most cash time**: {summary['most_cash_time_symbol']}.",
            "",
        ]
    )
    for regime in regimes:
        interpretation = regime["interpretation"]
        assumptions = regime.get("generation_assumptions", {})
        if not isinstance(assumptions, Mapping):
            assumptions = {}
        assumption_text = _format_inline_list(assumptions.get("assumptions", ()))
        lines.extend(
            [
                f"## {regime['regime_label']} ({regime['symbol']})",
                "",
                "- **Synthetic-only label**: deterministic fixture scenario; "
                "not historical market data, not predictive, and not live-trading use.",
                f"- **Generation source**: {_format_value(assumptions.get('source'))}",
                f"- **Generation assumptions**: {assumption_text}",
                f"- **Buy-and-hold comparison**: {interpretation['buy_and_hold_summary']}",
                f"- **Exposure/cash-time**: {interpretation['cash_time_summary']}",
                f"- **Drawdown**: {interpretation['drawdown_summary']}",
                f"- **Whipsaw**: {interpretation['whipsaw_summary']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Caveats",
            "",
            (
                "- This artifact uses deterministic bundled sample data for "
                "research workflows only. The prices were constructed for "
                "examples and tests; they are not real market prices."
            ),
            (
                "- Results are hypothetical, historical, and sensitive to data, "
                "fees, and chosen parameters."
            ),
            (
                "- A synthetic backtest can show how the software behaves, but "
                "it cannot show what will happen in live markets."
            ),
            (
                "- Nothing in this report is investment advice, trading guidance, "
                "a recommendation, a prediction, or a live-trading signal."
            ),
        ]
    )

    return "\n".join(lines) + "\n"


def build_exposure_trade_review(
    backtest_curve: Sequence[EquityCurveRecord],
) -> dict[str, Any]:
    """Summarize historical exposure changes for report and JSON artifacts."""

    if not backtest_curve:
        return {
            "period_count": 0,
            "periods_in_market": 0,
            "periods_in_cash": 0,
            "percent_periods_in_market": 0.0,
            "percent_periods_in_cash": 0.0,
            "average_exposure": 0.0,
            "exposure_changes": 0,
            "entries_to_market": 0,
            "exits_to_cash": 0,
            "total_fee_drag": 0.0,
            "research_only": True,
            "note": EXPOSURE_TRADE_REVIEW_NOTE,
        }

    period_records = backtest_curve[1:]
    period_count = len(period_records)
    periods_in_market = sum(1 for record in period_records if record.exposure > 0.0)
    periods_in_cash = period_count - periods_in_market
    exposure_changes = sum(
        1
        for previous, current in zip(backtest_curve, backtest_curve[1:])
        if previous.exposure != current.exposure
    )
    entries_to_market = sum(
        1
        for previous, current in zip(backtest_curve, backtest_curve[1:])
        if previous.exposure == 0.0 and current.exposure > 0.0
    )
    exits_to_cash = sum(
        1
        for previous, current in zip(backtest_curve, backtest_curve[1:])
        if previous.exposure > 0.0 and current.exposure == 0.0
    )
    average_exposure = (
        sum(record.exposure for record in period_records) / period_count
        if period_count
        else 0.0
    )

    return {
        "period_count": period_count,
        "periods_in_market": periods_in_market,
        "periods_in_cash": periods_in_cash,
        "percent_periods_in_market": _ratio(periods_in_market, period_count),
        "percent_periods_in_cash": _ratio(periods_in_cash, period_count),
        "average_exposure": average_exposure,
        "exposure_changes": exposure_changes,
        "entries_to_market": entries_to_market,
        "exits_to_cash": exits_to_cash,
        "total_fee_drag": sum(record.fee for record in period_records),
        "research_only": True,
        "note": EXPOSURE_TRADE_REVIEW_NOTE,
    }


def build_scenario_risk_interpretation(
    backtest_curve: Sequence[EquityCurveRecord],
    metrics: Mapping[str, float],
) -> dict[str, Any]:
    """Build beginner-readable historical diagnostics for one backtest output."""

    exposure_review = build_exposure_trade_review(backtest_curve)
    strategy_total_return = float(
        metrics.get("total_return", _curve_total_return(backtest_curve))
    )
    buy_and_hold_total = float(metrics.get("buy_and_hold_total_return", 0.0))
    return_gap = float(
        metrics.get(
            "strategy_minus_buy_and_hold_return",
            strategy_total_return - buy_and_hold_total,
        )
    )
    max_drawdown_value = float(metrics.get("max_drawdown", 0.0))
    total_fee_drag = float(exposure_review["total_fee_drag"])

    exposure_summary = (
        "No close-to-close periods were available, so exposure could not be "
        "interpreted."
        if exposure_review["period_count"] == 0
        else (
            "The model was exposed to the market for "
            f"{_format_percent(exposure_review['percent_periods_in_market'])} "
            "of reviewed periods. Higher exposure means the historical result "
            "depended more on market moves; lower exposure means more periods "
            "were modeled as cash."
        )
    )
    drawdown_summary = (
        "The worst modeled peak-to-trough decline was "
        f"{_format_percent(max_drawdown_value)}. Larger negative drawdowns "
        "mean the historical equity curve had larger interim losses."
    )
    fee_drag_summary = (
        "Modeled fee drag summed to "
        f"{_format_percent(total_fee_drag)} across reviewed periods. This is "
        "a simplified historical cost assumption, not a complete estimate of taxes, "
        "spreads, market impact, or broker execution."
    )
    comparison_summary = (
        "Strategy minus buy-and-hold was "
        f"{_format_percent(return_gap)} over the same period. "
        "A positive gap means the model finished above buy-and-hold in this "
        "historical sample; a negative gap means it finished below it."
    )

    return {
        "research_only": True,
        "historical_diagnostics_only": True,
        "note": SCENARIO_RISK_INTERPRETATION_NOTE,
        "exposure": {
            "period_count": exposure_review["period_count"],
            "average_exposure": exposure_review["average_exposure"],
            "percent_periods_in_market": exposure_review[
                "percent_periods_in_market"
            ],
            "summary": exposure_summary,
        },
        "drawdown": {
            "max_drawdown": max_drawdown_value,
            "summary": drawdown_summary,
        },
        "fee_drag": {
            "total_fee_drag": total_fee_drag,
            "summary": fee_drag_summary,
        },
        "buy_and_hold_comparison": {
            "strategy_total_return": strategy_total_return,
            "buy_and_hold_total_return": buy_and_hold_total,
            "strategy_minus_buy_and_hold_return": return_gap,
            "summary": comparison_summary,
        },
    }


def render_validation_split_note(
    validation_split: Mapping[str, Any] | None,
) -> list[str]:
    """Render a concise Markdown validation split note."""

    if validation_split is None:
        return []

    train = validation_split["train"]
    test = validation_split["test"]
    return [
        "## Validation split",
        "",
        (
            "- Research metadata only; this split is not trading guidance."
        ),
        (
            f"- Train: {train['first_date']} to {train['last_date']} "
            f"({train['row_count']} rows)."
        ),
        (
            f"- Test: {test['first_date']} to {test['last_date']} "
            f"({test['row_count']} rows)."
        ),
        "",
    ]


def render_data_provenance_note(
    data_provenance: Mapping[str, Any] | None,
) -> list[str]:
    """Render concise research-only static fixture provenance metadata."""

    if data_provenance is None:
        return []

    lines = [
        "## Data Provenance",
        "",
        "- Research-only fixture metadata; not live data, not investment advice, "
        "and not a prediction.",
        f"- **Dataset label**: {_format_value(data_provenance['dataset_label'])}",
        f"- **Data kind**: {_format_value(data_provenance['data_kind'])}",
        f"- **Source**: {_format_value(data_provenance['source'])}",
        f"- **Created date**: {_format_value(data_provenance['created_date'])}",
        f"- **As-of date**: {_format_value(data_provenance['as_of_date'])}",
    ]
    metadata_path = data_provenance.get("metadata_path")
    if metadata_path:
        lines.append(f"- **Metadata path**: {_format_value(metadata_path)}")

    limitations = data_provenance.get("limitations", ())
    if limitations:
        lines.append(f"- **Limitations**: {_format_limitations(limitations)}")

    regimes = data_provenance.get("regimes", ())
    if regimes:
        lines.append(f"- **Synthetic regimes**: {_format_regimes(regimes)}")

    return [*lines, ""]


def _render_mapping(values: Mapping[str, Any]) -> list[str]:
    if not values:
        return ["- No strategy configuration provided."]

    return [f"- **{key}**: {_format_value(value)}" for key, value in values.items()]


def _format_limitations(limitations: Any) -> str:
    if _is_non_text_sequence(limitations):
        return "; ".join(str(item) for item in limitations)
    return _format_value(limitations)


def _format_inline_list(values: Any) -> str:
    if _is_non_text_sequence(values):
        parts = [str(item).strip().rstrip(".") for item in values]
        return "; ".join(parts) + "."
    return _format_value(values)


def _format_regimes(regimes: Any) -> str:
    if not _is_non_text_sequence(regimes):
        return _format_value(regimes)

    labels: list[str] = []
    for regime in regimes:
        if isinstance(regime, Mapping):
            symbol = regime.get("symbol", "unknown")
            regime_name = regime.get("regime", "unknown")
            row_count = regime.get("row_count", "?")
            labels.append(f"{symbol} ({regime_name}, {row_count} rows)")
        else:
            labels.append(str(regime))

    return "; ".join(labels)


def _is_non_text_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    )


def _render_backtest_summary(
    backtest_curve: Sequence[EquityCurveRecord],
) -> list[str]:
    if not backtest_curve:
        return ["- No backtest curve records provided."]

    first = backtest_curve[0]
    last = backtest_curve[-1]
    total_return = last.equity / first.equity - 1
    trades = sum(
        1
        for previous, current in zip(backtest_curve, backtest_curve[1:])
        if previous.exposure != current.exposure
    )

    return [
        f"- **Start date**: {_format_date(first.date)}",
        f"- **End date**: {_format_date(last.date)}",
        f"- **Starting equity**: {first.equity:.4f}",
        f"- **Ending equity**: {last.equity:.4f}",
        f"- **Backtest total return**: {_format_percent(total_return)}",
        f"- **Exposure changes**: {trades}",
    ]


def _render_exposure_trade_review(review: Mapping[str, Any]) -> list[str]:
    if not review:
        return ["- No exposure review available."]

    period_count = int(review["period_count"])
    if period_count == 0:
        return [
            f"- {review['note']}",
            "- No close-to-close periods were available to review.",
        ]

    return [
        f"- {review['note']}",
        (
            f"- **Periods in market**: {review['periods_in_market']} of "
            f"{period_count} close-to-close periods "
            f"({_format_percent(review['percent_periods_in_market'])})."
        ),
        (
            f"- **Periods in cash**: {review['periods_in_cash']} of "
            f"{period_count} close-to-close periods "
            f"({_format_percent(review['percent_periods_in_cash'])})."
        ),
        f"- **Average exposure**: {_format_percent(review['average_exposure'])}.",
        f"- **Exposure changes**: {review['exposure_changes']}.",
        f"- **Modeled entries**: {review['entries_to_market']}.",
        f"- **Modeled exits**: {review['exits_to_cash']}.",
        (
            "- **Total fee drag**: "
            f"{_format_percent(review['total_fee_drag'])} summed across periods."
        ),
    ]


def _render_scenario_risk_interpretation(review: Mapping[str, Any]) -> list[str]:
    if not review:
        return ["- No scenario/risk interpretation available."]

    return [
        f"- {review['note']}",
        f"- **Exposure**: {review['exposure']['summary']}",
        f"- **Drawdown**: {review['drawdown']['summary']}",
        f"- **Fee drag**: {review['fee_drag']['summary']}",
        (
            "- **Buy-and-hold comparison**: "
            f"{review['buy_and_hold_comparison']['summary']}"
        ),
    ]


def _render_metrics(metrics: Mapping[str, float]) -> list[str]:
    if not metrics:
        return ["- No metrics provided."]

    return [
        f"- **{_metric_label(key)}**: {_format_metric(key, value)}"
        for key, value in metrics.items()
    ]


def _render_risk_notes(
    strategy_config: Mapping[str, Any],
    risk_notes: Sequence[str],
) -> list[str]:
    notes = [f"- {note}" for note in risk_notes]
    symbols = _extract_symbols(strategy_config)
    leveraged_symbols = sorted(
        symbol for symbol in symbols if symbol in LEVERAGED_ETF_SYMBOLS
    )
    if leveraged_symbols:
        symbol_text = ", ".join(leveraged_symbols)
        notes.append(
            "- Leveraged ETF warning: "
            f"{symbol_text} seeks leveraged daily returns. Multi-day results "
            "depend on the path of daily moves, losses can grow quickly, and "
            "choppy markets can reduce returns through volatility decay even "
            "when the underlying index ends near flat, especially over longer "
            "holding periods."
        )

    if not notes:
        return ["- No additional risk notes provided."]

    return notes


def _extract_symbols(strategy_config: Mapping[str, Any]) -> set[str]:
    candidates: list[Any] = []
    for key in ("symbol", "symbols", "ticker", "tickers"):
        if key in strategy_config:
            candidates.append(strategy_config[key])

    symbols: set[str] = set()
    for candidate in candidates:
        if isinstance(candidate, str):
            symbols.add(candidate.upper())
        elif isinstance(candidate, Sequence):
            symbols.update(
                item.upper()
                for item in candidate
                if isinstance(item, str)
            )

    return symbols


def _format_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, date):
        return _format_date(value)
    if isinstance(value, str):
        return value
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return ", ".join(str(item) for item in value)
    return str(value)


def _format_metric(key: str, value: float) -> str:
    metric_name = key.lower()
    percent_metric_terms = ("return", "drawdown", "volatility", "rate")
    if any(term in metric_name for term in percent_metric_terms):
        return _format_percent(value)

    return f"{value:.4f}"


def _metric_label(key: str) -> str:
    return METRIC_LABELS.get(key, key)


def _format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def _format_date(value: date) -> str:
    return value.isoformat()


def _curve_total_return(backtest_curve: Sequence[EquityCurveRecord]) -> float:
    if not backtest_curve:
        return 0.0

    first = backtest_curve[0]
    last = backtest_curve[-1]
    return last.equity / first.equity - 1


def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator
