"""Minimal long/cash backtesting helpers."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from market_signal_lab.data import PriceBar


@dataclass(frozen=True)
class EquityCurveRecord:
    """One point on a close-to-close equity curve."""

    date: date
    equity: float
    exposure: float
    market_return: float
    strategy_return: float
    fee: float


def backtest_long_cash(
    bars: Sequence[PriceBar],
    target_exposures: Sequence[float],
    fee_bps: float = 0.0,
    initial_equity: float = 1.0,
) -> list[EquityCurveRecord]:
    """Backtest 0/1 target exposures using next-bar close-to-close returns."""

    _validate_inputs(bars, target_exposures, fee_bps, initial_equity)
    if not bars:
        return []

    equity = initial_equity
    records = [
        EquityCurveRecord(
            date=bars[0].date,
            equity=equity,
            exposure=0.0,
            market_return=0.0,
            strategy_return=0.0,
            fee=0.0,
        ),
    ]
    previous_exposure = 0.0
    fee_rate = fee_bps / 10_000

    for index in range(1, len(bars)):
        exposure = float(target_exposures[index - 1])
        market_return = bars[index].close / bars[index - 1].close - 1
        fee = abs(exposure - previous_exposure) * fee_rate
        strategy_return = exposure * market_return - fee
        equity *= 1 + strategy_return

        records.append(
            EquityCurveRecord(
                date=bars[index].date,
                equity=equity,
                exposure=exposure,
                market_return=market_return,
                strategy_return=strategy_return,
                fee=fee,
            ),
        )
        previous_exposure = exposure

    return records


def _validate_inputs(
    bars: Sequence[PriceBar],
    target_exposures: Sequence[float],
    fee_bps: float,
    initial_equity: float,
) -> None:
    if len(bars) != len(target_exposures):
        raise ValueError("bars and target_exposures must have the same length")
    if fee_bps < 0:
        raise ValueError("fee_bps must be non-negative")
    if initial_equity <= 0:
        raise ValueError("initial_equity must be positive")

    for index, exposure in enumerate(target_exposures):
        if exposure not in (0, 1, 0.0, 1.0):
            raise ValueError(f"target_exposures[{index}] must be 0 or 1")
