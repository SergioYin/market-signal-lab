"""Research-only parameter sweep helpers for moving-average strategies."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any, Literal, TypedDict

from market_signal_lab.backtest import backtest_long_cash
from market_signal_lab.data import PriceBar
from market_signal_lab.metrics import (
    annualized_return,
    max_drawdown,
    sharpe_like,
    total_return,
    volatility,
    win_rate_from_returns,
)
from market_signal_lab.report import render_validation_split_note
from market_signal_lab.strategies import moving_average_crossover_strategy


SWEEP_REPORT_CAVEAT = (
    "Research-only: this sweep is a historical parameter screen, not investment "
    "advice, not a recommendation, and not evidence of future performance."
)

SWEEP_REPORT_COLUMNS = (
    "rank",
    "short_window",
    "long_window",
    "total_return",
    "annualized_return",
    "max_drawdown",
    "volatility",
    "sharpe_like",
    "win_rate",
)

SWEEP_REPORT_SPLIT_COLUMNS = (
    "rank",
    "short_window",
    "long_window",
    "total_return",
    "train_rank",
    "test_rank",
    "rank_delta",
    "train_total_return",
    "test_total_return",
    "train_test_return_gap",
    "robustness_flag",
    "annualized_return",
    "max_drawdown",
    "volatility",
    "sharpe_like",
    "win_rate",
)

SWEEP_OVERFIT_CAVEAT = (
    "Train/test columns are a comparison aid for historical research only; a "
    "large train/test gap can prompt review for possible parameter overfitting "
    "and is not a trading recommendation."
)

SWEEP_ROBUSTNESS_CAVEAT = (
    "The robustness_flag label compares historical train/test ranks and return "
    "gaps inside this sample only. 'not_flagged' only means the deterministic "
    "review thresholds were not crossed; it is not a prediction, a stability "
    "claim, or a recommendation to buy, sell, or hold."
)

ROBUSTNESS_RANK_DELTA_THRESHOLD = 2
ROBUSTNESS_RETURN_GAP_THRESHOLD = 0.10

ResultKey = tuple[int, int]
RobustnessFlag = Literal["fragile", "not_flagged"]
SplitMetricsGetter = Callable[["SweepResult"], Mapping[str, float] | None]


class RobustnessDiagnostics(TypedDict):
    train_rank: int
    test_rank: int
    rank_delta: int
    train_test_return_gap: float
    robustness_flag: RobustnessFlag


RobustnessDisplayKey = Literal[
    "train_rank",
    "test_rank",
    "rank_delta",
    "robustness_flag",
]


@dataclass(frozen=True)
class SweepResult:
    """One evaluated short/long moving-average configuration."""

    short_window: int
    long_window: int
    metrics: dict[str, float]
    train_metrics: dict[str, float] | None = None
    test_metrics: dict[str, float] | None = None
    robustness: RobustnessDiagnostics | None = field(
        default=None,
        compare=False,
        repr=False,
    )

    @property
    def total_return(self) -> float:
        return self.metrics["total_return"]

    @property
    def max_drawdown(self) -> float:
        return self.metrics["max_drawdown"]


def moving_average_parameter_grid(
    short_windows: Sequence[int],
    long_windows: Sequence[int],
) -> list[tuple[int, int]]:
    """Return all valid (short, long) pairs preserving input order."""

    short_values = _normalize_window_values(short_windows)
    long_values = _normalize_window_values(long_windows)

    pairs: list[tuple[int, int]] = []
    for short_window in short_values:
        for long_window in long_values:
            if short_window < long_window:
                pairs.append((short_window, long_window))

    return pairs


def run_moving_average_sweep(
    bars: Sequence[PriceBar],
    short_windows: Sequence[int],
    long_windows: Sequence[int],
    fee_bps: float = 0.0,
    initial_equity: float = 1.0,
    top_n: int | None = None,
    train_bars: Sequence[PriceBar] | None = None,
    test_bars: Sequence[PriceBar] | None = None,
) -> list[SweepResult]:
    """Evaluate moving-average configurations and return ranked research results."""

    if top_n is not None and top_n < 1:
        raise ValueError("top_n must be at least 1 when set")
    if (train_bars is None) != (test_bars is None):
        raise ValueError("train_bars and test_bars must be provided together")

    grid = moving_average_parameter_grid(short_windows, long_windows)
    if not grid:
        return []
    if train_bars is not None and test_bars is not None:
        _validate_split_partitions_for_grid(train_bars, test_bars, grid)

    results = [
        _evaluate_pair(
            bars=bars,
            short_window=short_window,
            long_window=long_window,
            fee_bps=fee_bps,
            initial_equity=initial_equity,
            train_bars=train_bars,
            test_bars=test_bars,
        )
        for short_window, long_window in grid
    ]

    if train_bars is not None:
        results = annotate_split_robustness(results)

    ranked = rank_sweep_results(results)
    return ranked[:top_n] if top_n is not None else ranked


def rank_sweep_results(results: Sequence[SweepResult]) -> list[SweepResult]:
    """Order results by total return then max drawdown, preserving metric ties."""

    return sorted(results, key=lambda result: _metrics_rank_key(result.metrics))


def annotate_split_robustness(results: Sequence[SweepResult]) -> list[SweepResult]:
    """Attach deterministic train/test rank comparison diagnostics to results."""

    if not results:
        return []
    if len({_result_key(result) for result in results}) != len(results):
        raise ValueError("results must have unique short_window/long_window pairs")

    train_positions = _rank_positions(results, lambda result: result.train_metrics)
    test_positions = _rank_positions(results, lambda result: result.test_metrics)

    annotated: list[SweepResult] = []
    for result in results:
        train_metrics, test_metrics = _split_metrics(result)
        train_rank = train_positions[_result_key(result)]
        test_rank = test_positions[_result_key(result)]
        rank_delta = test_rank - train_rank
        train_total_return = train_metrics["total_return"]
        test_total_return = test_metrics["total_return"]
        return_gap = train_total_return - test_total_return
        robustness_flag: RobustnessFlag = (
            "fragile"
            if _is_fragile_split_result(
                rank_delta=rank_delta,
                train_total_return=train_total_return,
                test_total_return=test_total_return,
                return_gap=return_gap,
            )
            else "not_flagged"
        )
        annotated.append(
            replace(
                result,
                robustness={
                    "train_rank": train_rank,
                    "test_rank": test_rank,
                    "rank_delta": rank_delta,
                    "train_test_return_gap": return_gap,
                    "robustness_flag": robustness_flag,
                },
            )
        )

    return annotated


def format_sweep_percentage(value: float) -> str:
    """Format a decimal metric as a percentage for sweep reports."""

    return f"{value * 100:.2f}%"


def format_sweep_number(value: float) -> str:
    """Format a plain numeric metric for sweep reports."""

    return f"{value:.4f}"


def render_sweep_report(
    results: Sequence[SweepResult],
    validation_split: Mapping[str, Any] | None = None,
) -> str:
    """Render ranked moving-average sweep results as a Markdown report."""

    lines = [
        "# Moving Average Sweep Report",
        "",
        f"> {SWEEP_REPORT_CAVEAT}",
        "",
        *render_validation_split_note(validation_split),
    ]
    if validation_split is not None:
        lines.extend(
            [
                f"> {SWEEP_OVERFIT_CAVEAT}",
                f"> {SWEEP_ROBUSTNESS_CAVEAT}",
                "",
            ]
        )

    columns = _sweep_report_columns(validation_split)
    lines.extend(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
        ]
    )

    for rank, result in enumerate(results, start=1):
        lines.append(
            _render_sweep_result_row(
                rank,
                result,
                include_split_columns=validation_split is not None,
            )
        )

    if not results:
        lines.append("| " + " | ".join("-" for _ in columns) + " |")

    return "\n".join(lines) + "\n"


def _evaluate_pair(
    bars: Sequence[PriceBar],
    short_window: int,
    long_window: int,
    fee_bps: float,
    initial_equity: float,
    train_bars: Sequence[PriceBar] | None = None,
    test_bars: Sequence[PriceBar] | None = None,
) -> SweepResult:
    return SweepResult(
        short_window=short_window,
        long_window=long_window,
        metrics=_evaluate_metrics(
            bars=bars,
            short_window=short_window,
            long_window=long_window,
            fee_bps=fee_bps,
            initial_equity=initial_equity,
        ),
        train_metrics=(
            _evaluate_metrics(
                bars=train_bars,
                short_window=short_window,
                long_window=long_window,
                fee_bps=fee_bps,
                initial_equity=initial_equity,
            )
            if train_bars is not None
            else None
        ),
        test_metrics=(
            _evaluate_metrics(
                bars=test_bars,
                short_window=short_window,
                long_window=long_window,
                fee_bps=fee_bps,
                initial_equity=initial_equity,
            )
            if test_bars is not None
            else None
        ),
    )


def _evaluate_metrics(
    bars: Sequence[PriceBar],
    short_window: int,
    long_window: int,
    fee_bps: float,
    initial_equity: float,
) -> dict[str, float]:
    signals = moving_average_crossover_strategy(
        bars,
        short_window=short_window,
        long_window=long_window,
    )
    target_exposures = [signal.target_exposure for signal in signals]
    curve = backtest_long_cash(
        bars=bars,
        target_exposures=target_exposures,
        fee_bps=fee_bps,
        initial_equity=initial_equity,
    )
    strategy_returns = [record.strategy_return for record in curve[1:]]
    return {
        "total_return": total_return(strategy_returns),
        "max_drawdown": max_drawdown(strategy_returns),
        "annualized_return": annualized_return(strategy_returns),
        "volatility": volatility(strategy_returns),
        "sharpe_like": sharpe_like(strategy_returns),
        "win_rate": win_rate_from_returns(strategy_returns),
    }


def _rank_positions(
    results: Sequence[SweepResult],
    metrics_for_result: SplitMetricsGetter,
) -> dict[ResultKey, int]:
    ranked = sorted(
        results,
        key=lambda result: _result_metrics_rank_key(result, metrics_for_result),
    )
    return {_result_key(result): rank for rank, result in enumerate(ranked, start=1)}


def _result_metrics_rank_key(
    result: SweepResult,
    metrics_for_result: SplitMetricsGetter,
) -> tuple[float, float, int, int]:
    metrics = metrics_for_result(result)
    if metrics is None:
        raise ValueError("all results must include train_metrics and test_metrics")
    return (*_metrics_rank_key(metrics), result.short_window, result.long_window)


def _metrics_rank_key(metrics: Mapping[str, float]) -> tuple[float, float]:
    return (-metrics["total_return"], -metrics["max_drawdown"])


def _result_key(result: SweepResult) -> ResultKey:
    return (result.short_window, result.long_window)


def _split_metrics(
    result: SweepResult,
) -> tuple[Mapping[str, float], Mapping[str, float]]:
    if result.train_metrics is None or result.test_metrics is None:
        raise ValueError("all results must include train_metrics and test_metrics")
    return result.train_metrics, result.test_metrics


def _validate_split_partitions_for_grid(
    train_bars: Sequence[PriceBar],
    test_bars: Sequence[PriceBar],
    grid: Sequence[tuple[int, int]],
) -> None:
    if not train_bars:
        raise ValueError("validation split training partition must not be empty")
    if not test_bars:
        raise ValueError("validation split test partition must not be empty")

    required_bars = max(long_window for _, long_window in grid)
    if len(train_bars) < required_bars or len(test_bars) < required_bars:
        raise ValueError(
            "validation split partitions must each contain at least "
            f"{required_bars} rows to evaluate the largest long window; "
            "adjust the split or use smaller long-window values"
        )


def _is_fragile_split_result(
    *,
    rank_delta: int,
    train_total_return: float,
    test_total_return: float,
    return_gap: float,
) -> bool:
    return (
        abs(rank_delta) >= ROBUSTNESS_RANK_DELTA_THRESHOLD
        or abs(return_gap) >= ROBUSTNESS_RETURN_GAP_THRESHOLD
        or (train_total_return > 0 and test_total_return <= 0)
    )


def _sweep_report_columns(
    validation_split: Mapping[str, Any] | None,
) -> tuple[str, ...]:
    if validation_split is None:
        return SWEEP_REPORT_COLUMNS
    return SWEEP_REPORT_SPLIT_COLUMNS


def _render_sweep_result_row(
    rank: int,
    result: SweepResult,
    *,
    include_split_columns: bool,
) -> str:
    values: tuple[str, ...]
    if not include_split_columns:
        values = (
            str(rank),
            str(result.short_window),
            str(result.long_window),
            format_sweep_percentage(result.metrics["total_return"]),
            format_sweep_percentage(result.metrics["annualized_return"]),
            format_sweep_percentage(result.metrics["max_drawdown"]),
            format_sweep_percentage(result.metrics["volatility"]),
            format_sweep_number(result.metrics["sharpe_like"]),
            format_sweep_percentage(result.metrics["win_rate"]),
        )
    else:
        values = (
            str(rank),
            str(result.short_window),
            str(result.long_window),
            format_sweep_percentage(result.metrics["total_return"]),
            _format_optional_robustness_value(result, "train_rank"),
            _format_optional_robustness_value(result, "test_rank"),
            _format_optional_robustness_value(result, "rank_delta"),
            _format_optional_total_return(result.train_metrics),
            _format_optional_total_return(result.test_metrics),
            _format_optional_robustness_gap(result),
            _format_optional_robustness_value(result, "robustness_flag"),
            format_sweep_percentage(result.metrics["annualized_return"]),
            format_sweep_percentage(result.metrics["max_drawdown"]),
            format_sweep_percentage(result.metrics["volatility"]),
            format_sweep_number(result.metrics["sharpe_like"]),
            format_sweep_percentage(result.metrics["win_rate"]),
        )

    return "| " + " | ".join(values) + " |"


def _format_optional_total_return(metrics: Mapping[str, float] | None) -> str:
    if metrics is None:
        return "-"
    return format_sweep_percentage(metrics["total_return"])


def _format_optional_robustness_value(
    result: SweepResult,
    key: RobustnessDisplayKey,
) -> str:
    if result.robustness is None:
        return "-"
    return str(result.robustness[key])


def _format_optional_robustness_gap(result: SweepResult) -> str:
    if result.robustness is None:
        return "-"
    return format_sweep_percentage(float(result.robustness["train_test_return_gap"]))


def _normalize_window_values(values: Sequence[int]) -> list[int]:
    if not values:
        raise ValueError("window sequence cannot be empty")

    normalized: list[int] = []
    seen: set[int] = set()
    for value in values:
        if not isinstance(value, int):
            raise TypeError("window values must be integers")
        if value < 1:
            raise ValueError("window values must be at least 1")
        if value in seen:
            continue
        seen.add(value)
        normalized.append(value)

    return normalized
