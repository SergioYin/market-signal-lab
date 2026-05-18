"""Markdown report rendering for strategy experiments."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any

from market_signal_lab.backtest import EquityCurveRecord

LEVERAGED_ETF_SYMBOLS = frozenset({"TQQQ", "QLD"})
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
        "## Metrics",
        "",
        *_render_metrics(metrics),
        "",
        *render_validation_split_note(validation_split),
        "## Risk Notes",
        "",
        *_render_risk_notes(strategy_config, risk_notes),
        "",
        "## Backtest Caveats",
        "",
        "- Backtest results are hypothetical and do not guarantee future performance.",
        (
            "- Signals are evaluated using historical data and may be affected by "
            "data quality, survivorship bias, and parameter overfitting."
        ),
        (
            "- Reported returns are model outputs before taxes, market impact, "
            "and any costs not explicitly included in the backtest."
        ),
    ]

    return "\n".join(lines) + "\n"


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
            "- Research metadata only; this split is not a trading "
            "recommendation."
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


def _render_mapping(values: Mapping[str, Any]) -> list[str]:
    if not values:
        return ["- No strategy configuration provided."]

    return [f"- **{key}**: {_format_value(value)}" for key, value in values.items()]


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
            f"{symbol_text} seeks leveraged daily returns, can suffer volatility "
            "decay, and may diverge materially from the underlying index over "
            "longer holding periods."
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
