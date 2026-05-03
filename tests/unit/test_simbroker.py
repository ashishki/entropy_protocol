"""Unit tests for SimBroker cost model."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, cast

import pytest
from pydantic import ValidationError

from entropy.models.market import OHLCVBar
from entropy.models.registry import FillSide
from entropy.simbroker.calibration import BidAskProvider, BidAskQuote, NoOpBidAskProvider
from entropy.simbroker.costs import CostModelConfig, compute_cost
from entropy.simbroker.fills import FillSignal, process_fill

UTC_TS = datetime(2026, 5, 3, 12, 0, tzinfo=timezone.utc)


def make_bar(**overrides: object) -> OHLCVBar:
    data = {
        "timestamp": UTC_TS,
        "open": 100.0,
        "high": 105.0,
        "low": 99.0,
        "close": 103.0,
        "volume": 1000.0,
    }
    data.update(overrides)
    return OHLCVBar(**data)


def make_signal(**overrides: object) -> FillSignal:
    data = {
        "symbol": "BTC-USD",
        "side": FillSide.BUY,
        "quantity": 10.0,
        "proposed_price": 102.0,
    }
    data.update(overrides)
    return FillSignal(**data)


def make_cost_config(**overrides: float) -> CostModelConfig:
    data = {
        "fixed_commission": 1.0,
        "pct_commission": 0.0008,
        "slippage_linear": 0.0002,
        "sqrt_impact_coef": 0.0002,
        "borrow_rate": 0.0,
        "funding_rate": 0.0,
    }
    data.update(overrides)
    return CostModelConfig(**data)


def test_cost_model_worked_example() -> None:
    breakdown = compute_cost(
        fill_price=100.0,
        quantity=10,
        fixed_commission=1.0,
        pct_commission=0.0008,
        slippage_linear=0.0002,
        sqrt_impact_coef=0.0002,
        borrow_rate=0.0,
        funding_rate=0.0,
    )

    assert breakdown.fixed_commission == pytest.approx(1.0)
    assert breakdown.pct_commission == pytest.approx(0.8)
    assert breakdown.slippage == pytest.approx(0.2)
    assert breakdown.market_impact == pytest.approx(0.2)
    assert breakdown.borrow == pytest.approx(0.0)
    assert breakdown.funding == pytest.approx(0.0)
    assert breakdown.total_cost == pytest.approx(2.2, abs=1e-6)


def test_cost_model_is_deterministic() -> None:
    kwargs = {
        "fill_price": 250.0,
        "quantity": 4,
        "fixed_commission": 0.5,
        "pct_commission": 0.001,
        "slippage_linear": 0.0003,
        "sqrt_impact_coef": 0.0004,
        "borrow_rate": 0.0001,
        "funding_rate": 0.0002,
    }

    first = compute_cost(**kwargs)
    second = compute_cost(**kwargs)

    assert first == second
    assert first.total_cost == second.total_cost


def test_cost_model_borrow_component() -> None:
    borrow_rate = 0.015 / 365
    breakdown = compute_cost(
        fill_price=100.0,
        quantity=10,
        fixed_commission=0.0,
        pct_commission=0.0,
        slippage_linear=0.0,
        sqrt_impact_coef=0.0,
        borrow_rate=borrow_rate,
        funding_rate=0.0,
    )

    expected_borrow = 100.0 * 10 * borrow_rate
    assert breakdown.borrow == pytest.approx(expected_borrow, abs=1e-10)
    assert breakdown.total_cost == pytest.approx(expected_borrow, abs=1e-10)


def test_cost_model_zero_costs() -> None:
    breakdown = compute_cost(
        fill_price=100.0,
        quantity=10,
        fixed_commission=0.0,
        pct_commission=0.0,
        slippage_linear=0.0,
        sqrt_impact_coef=0.0,
        borrow_rate=0.0,
        funding_rate=0.0,
    )

    assert breakdown.fixed_commission == 0.0
    assert breakdown.pct_commission == 0.0
    assert breakdown.slippage == 0.0
    assert breakdown.market_impact == 0.0
    assert breakdown.borrow == 0.0
    assert breakdown.funding == 0.0
    assert breakdown.total_cost == 0.0


def test_cost_model_config_validates_nonnegative() -> None:
    config = CostModelConfig(
        fixed_commission=1.0,
        pct_commission=0.0008,
        slippage_linear=0.0002,
        sqrt_impact_coef=0.0002,
        borrow_rate=0.0,
        funding_rate=0.0,
    )

    assert config.pct_commission == pytest.approx(0.0008)

    with pytest.raises(ValidationError):
        CostModelConfig(pct_commission=-0.0001)


def test_cost_model_rejects_nonpositive_fill_inputs() -> None:
    with pytest.raises(ValueError, match="fill_price must be positive"):
        compute_cost(fill_price=0.0, quantity=1)

    with pytest.raises(ValueError, match="quantity must be positive"):
        compute_cost(fill_price=1.0, quantity=0)


def test_fill_constrained_to_bar_high() -> None:
    fill_log = process_fill(
        signal=make_signal(side=FillSide.BUY, proposed_price=110.0),
        bar=make_bar(),
        cost_config=make_cost_config(),
    )

    assert fill_log.fill_price == Decimal("105.0")
    assert fill_log.constrained is True


def test_fill_constrained_to_bar_low() -> None:
    fill_log = process_fill(
        signal=make_signal(side=FillSide.SELL, proposed_price=95.0),
        bar=make_bar(),
        cost_config=make_cost_config(),
    )

    assert fill_log.fill_price == Decimal("99.0")
    assert fill_log.constrained is True


def test_fill_unconstrained_within_bar() -> None:
    fill_log = process_fill(
        signal=make_signal(proposed_price=102.0),
        bar=make_bar(),
        cost_config=make_cost_config(),
    )

    assert fill_log.fill_price == Decimal("102.0")
    assert fill_log.constrained is False


def test_fill_engine_determinism() -> None:
    signal = make_signal(proposed_price=102.0)
    bar = make_bar()
    cost_config = make_cost_config(borrow_rate=0.015 / 365, funding_rate=0.0002)

    first = process_fill(signal=signal, bar=bar, cost_config=cost_config)
    second = process_fill(signal=signal, bar=bar, cost_config=cost_config)

    assert first == second
    assert first.model_dump_json() == second.model_dump_json()


def test_fill_log_has_all_required_fields() -> None:
    fill_log = process_fill(
        signal=make_signal(proposed_price=100.0),
        bar=make_bar(),
        cost_config=make_cost_config(borrow_rate=0.015 / 365, funding_rate=0.0002),
    )

    dumped = fill_log.model_dump()
    for field_name in (
        "timestamp",
        "symbol",
        "side",
        "quantity",
        "fill_price",
        "commission",
        "slippage",
        "market_impact",
        "borrow_rate",
        "funding_rate",
        "total_cost",
        "constrained",
    ):
        assert field_name in dumped

    assert fill_log.timestamp == UTC_TS
    assert fill_log.symbol == "BTC-USD"
    assert fill_log.side is FillSide.BUY
    assert fill_log.quantity == Decimal("10.0")
    assert fill_log.commission == Decimal("1.8")
    assert fill_log.slippage == Decimal("0.2")
    assert fill_log.market_impact == Decimal("0.2")
    assert fill_log.total_cost > Decimal("0")


def test_fill_engine_no_lookahead() -> None:
    class GuardedBar:
        timestamp = UTC_TS
        high = 105.0
        low = 99.0

        @property
        def next_bar(self) -> object:
            raise AttributeError("fill engine must not access next_bar")

    fill_log = process_fill(
        signal=make_signal(proposed_price=110.0),
        bar=GuardedBar(),
        cost_config=make_cost_config(),
    )

    assert fill_log.fill_price == Decimal("105.0")
    assert fill_log.constrained is True


def test_bid_ask_provider_is_abstract() -> None:
    with pytest.raises(TypeError):
        cast(Any, BidAskProvider)()


def test_noop_bid_ask_provider_returns_none() -> None:
    provider = NoOpBidAskProvider()

    assert provider.get_bid_ask(symbol="BTCUSDT", timestamp=UTC_TS) is None


def test_noop_is_valid_subclass() -> None:
    provider = NoOpBidAskProvider()

    assert isinstance(provider, BidAskProvider)


def test_bid_ask_quote_validates_spread_and_timestamp() -> None:
    quote = BidAskQuote(symbol="BTCUSDT", timestamp=UTC_TS, bid=100.0, ask=100.5)

    assert quote.symbol == "BTCUSDT"
    assert quote.bid == pytest.approx(100.0)
    assert quote.ask == pytest.approx(100.5)

    with pytest.raises(ValidationError):
        BidAskQuote(symbol="BTCUSDT", timestamp=UTC_TS, bid=101.0, ask=100.0)

    with pytest.raises(ValidationError):
        BidAskQuote(symbol="BTCUSDT", timestamp=datetime(2026, 5, 3, 12, 0), bid=100.0, ask=100.5)
