"""Deterministic synthetic sample data generators."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any


@dataclass(frozen=True)
class SyntheticRegimeSpec:
    """Specification for one deterministic synthetic regime series."""

    symbol: str
    regime: str
    description: str
    assumptions: tuple[str, ...]
    closes: tuple[float, ...]


MULTI_REGIME_START_DATE = date(2024, 2, 1)
MULTI_REGIME_SPECS = (
    SyntheticRegimeSpec(
        symbol="BULL_REGIME",
        regime="bull",
        description="Monotonic upward path used to exercise trend-following examples.",
        assumptions=(
            "Close prices increase every sample period by construction.",
            "Open prices equal the prior close after the first row.",
            "High and low prices are synthetic padding around open and close.",
        ),
        closes=(
            100.0,
            101.2,
            102.5,
            104.1,
            105.7,
            107.4,
            109.1,
            111.0,
            112.8,
            114.7,
            116.9,
            119.2,
        ),
    ),
    SyntheticRegimeSpec(
        symbol="CHOPPY_REGIME",
        regime="choppy",
        description="Alternating path that ends near flat after repeated reversals.",
        assumptions=(
            "Close prices alternate around the starting level by construction.",
            "Open prices equal the prior close after the first row.",
            "High and low prices are synthetic padding around open and close.",
        ),
        closes=(
            100.0,
            102.0,
            99.5,
            101.5,
            98.8,
            100.7,
            99.1,
            101.1,
            99.6,
            100.4,
            99.8,
            100.2,
        ),
    ),
    SyntheticRegimeSpec(
        symbol="DRAWDOWN_RECOVERY_REGIME",
        regime="drawdown_recovery",
        description="Decline followed by recovery for drawdown diagnostics.",
        assumptions=(
            "Close prices fall first and then recover by construction.",
            "Open prices equal the prior close after the first row.",
            "High and low prices are synthetic padding around open and close.",
        ),
        closes=(
            100.0,
            98.0,
            94.0,
            89.0,
            84.0,
            80.0,
            83.0,
            87.0,
            91.0,
            95.0,
            99.0,
            103.0,
        ),
    ),
)


def multi_regime_fixture_metadata() -> list[dict[str, Any]]:
    """Return deterministic metadata for the bundled multi-regime fixture."""

    return [
        {
            "symbol": spec.symbol,
            "regime": spec.regime,
            "description": spec.description,
            "assumptions": list(spec.assumptions),
            "synthetic_only": True,
            "not_predictive": True,
            "not_live_trading": True,
            "row_count": len(spec.closes),
        }
        for spec in MULTI_REGIME_SPECS
    ]


def generate_multi_regime_sample_rows() -> list[dict[str, str]]:
    """Generate interleaved deterministic OHLC rows for several regimes."""

    dates = tuple(_trading_dates(MULTI_REGIME_START_DATE, _sample_length()))
    rows: list[dict[str, str]] = []
    for index, row_date in enumerate(dates):
        for spec in MULTI_REGIME_SPECS:
            close_price = spec.closes[index]
            open_price = spec.closes[index - 1] if index else close_price
            high_price, low_price = _synthetic_high_low(open_price, close_price)
            rows.append(
                {
                    "symbol": spec.symbol,
                    "date": row_date.isoformat(),
                    "open": f"{open_price:.2f}",
                    "high": f"{high_price:.2f}",
                    "low": f"{low_price:.2f}",
                    "close": f"{close_price:.2f}",
                }
            )

    return rows


def render_multi_regime_sample_csv() -> str:
    """Render the deterministic multi-regime fixture as CSV text."""

    fieldnames = ("symbol", "date", "open", "high", "low", "close")
    lines = [",".join(fieldnames)]
    for row in generate_multi_regime_sample_rows():
        lines.append(",".join(row[field] for field in fieldnames))

    return "\n".join(lines) + "\n"


def _sample_length() -> int:
    lengths = {len(spec.closes) for spec in MULTI_REGIME_SPECS}
    if len(lengths) != 1:
        raise ValueError("Synthetic multi-regime close paths must have equal length")
    return lengths.pop()


def _trading_dates(start: date, count: int) -> Iterable[date]:
    current = start
    emitted = 0
    while emitted < count:
        if current.weekday() < 5:
            yield current
            emitted += 1
        current += timedelta(days=1)


def _synthetic_high_low(open_price: float, close_price: float) -> tuple[float, float]:
    pad = max(abs(close_price - open_price) * 0.45, open_price * 0.004)
    high_price = max(open_price, close_price) + pad
    low_price = min(open_price, close_price) - pad
    return high_price, low_price
