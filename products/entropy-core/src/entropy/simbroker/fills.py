"""Deterministic SimBroker fill engine."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Protocol

from pydantic import BaseModel, Field, field_validator

from entropy.models.registry import FillLog, FillSide
from entropy.simbroker.costs import CostModelConfig, compute_cost


class BarLike(Protocol):
    """Minimal OHLCV bar surface used by the fill engine."""

    timestamp: datetime
    high: float
    low: float


class FillSignal(BaseModel):
    """Strategy fill request consumed by SimBroker."""

    symbol: str = Field(min_length=1)
    side: FillSide
    quantity: float = Field(gt=0.0)
    proposed_price: float = Field(gt=0.0)

    @field_validator("symbol")
    @classmethod
    def symbol_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only symbols."""
        if not value.strip():
            raise ValueError("symbol must not be blank")
        return value


def process_fill(*, signal: FillSignal, bar: BarLike, cost_config: CostModelConfig) -> FillLog:
    """Produce a deterministic fill log using only the provided bar."""
    fill_price = _constrain_price(signal.proposed_price, low=bar.low, high=bar.high)
    constrained = fill_price != signal.proposed_price
    cost = compute_cost(
        fill_price=fill_price,
        quantity=signal.quantity,
        fixed_commission=cost_config.fixed_commission,
        pct_commission=cost_config.pct_commission,
        slippage_linear=cost_config.slippage_linear,
        sqrt_impact_coef=cost_config.sqrt_impact_coef,
        borrow_rate=cost_config.borrow_rate,
        funding_rate=cost_config.funding_rate,
    )

    return FillLog(
        timestamp=bar.timestamp,
        symbol=signal.symbol,
        side=signal.side,
        quantity=_decimal(signal.quantity),
        fill_price=_decimal(fill_price),
        commission=_decimal(cost.fixed_commission + cost.pct_commission),
        slippage=_decimal(cost.slippage),
        market_impact=_decimal(cost.market_impact),
        borrow_rate=_decimal(cost.borrow),
        funding_rate=_decimal(cost.funding),
        total_cost=_decimal(cost.total_cost),
        constrained=constrained,
    )


def _constrain_price(proposed_price: float, *, low: float, high: float) -> float:
    if low > high:
        raise ValueError("bar low must be <= high")
    return min(max(proposed_price, low), high)


def _decimal(value: float) -> Decimal:
    return Decimal(str(value))
