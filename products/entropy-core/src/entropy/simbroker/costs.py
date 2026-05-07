"""Deterministic SimBroker cost model."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CostModelConfig(BaseModel):
    """Configurable per-fill cost model parameters."""

    fixed_commission: float = Field(default=0.0, ge=0.0)
    pct_commission: float = Field(default=0.0, ge=0.0)
    slippage_linear: float = Field(default=0.0, ge=0.0)
    sqrt_impact_coef: float = Field(default=0.0, ge=0.0)
    borrow_rate: float = Field(default=0.0, ge=0.0)
    funding_rate: float = Field(default=0.0, ge=0.0)


class CostBreakdown(BaseModel):
    """Explicit cost decomposition for one simulated fill."""

    fixed_commission: float = Field(ge=0.0)
    pct_commission: float = Field(ge=0.0)
    slippage: float = Field(ge=0.0)
    market_impact: float = Field(ge=0.0)
    borrow: float = Field(ge=0.0)
    funding: float = Field(ge=0.0)
    total_cost: float = Field(ge=0.0)


def compute_cost(
    *,
    fill_price: float,
    quantity: float,
    fixed_commission: float = 0.0,
    pct_commission: float = 0.0,
    slippage_linear: float = 0.0,
    sqrt_impact_coef: float = 0.0,
    borrow_rate: float = 0.0,
    funding_rate: float = 0.0,
) -> CostBreakdown:
    """Compute deterministic per-fill costs from notional and configured rates.

    ``sqrt_impact_coef`` is the already-calibrated square-root impact rate for the
    fill. T15 intentionally does not introduce volume or participation inputs.
    """
    config = CostModelConfig(
        fixed_commission=fixed_commission,
        pct_commission=pct_commission,
        slippage_linear=slippage_linear,
        sqrt_impact_coef=sqrt_impact_coef,
        borrow_rate=borrow_rate,
        funding_rate=funding_rate,
    )
    if fill_price <= 0:
        raise ValueError("fill_price must be positive")
    if quantity <= 0:
        raise ValueError("quantity must be positive")

    notional = fill_price * quantity
    percentage_commission = notional * config.pct_commission
    slippage = notional * config.slippage_linear
    market_impact = notional * config.sqrt_impact_coef
    borrow = notional * config.borrow_rate
    funding = notional * config.funding_rate
    total_cost = (
        config.fixed_commission
        + percentage_commission
        + slippage
        + market_impact
        + borrow
        + funding
    )

    return CostBreakdown(
        fixed_commission=config.fixed_commission,
        pct_commission=percentage_commission,
        slippage=slippage,
        market_impact=market_impact,
        borrow=borrow,
        funding=funding,
        total_cost=total_cost,
    )
