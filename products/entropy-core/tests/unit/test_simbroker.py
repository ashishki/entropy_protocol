"""Unit tests for SimBroker cost model."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, cast

import pytest
from pydantic import ValidationError

from entropy.models.market import OHLCVBar
from entropy.models.registry import FillSide
from entropy.simbroker.calibration import (
    NO_GATE_CLAIM,
    BidAskProvider,
    BidAskQuote,
    CalibrationRow,
    NoOpBidAskProvider,
    build_calibration_row_from_fill,
    build_calibration_summary,
    read_calibration_rows_jsonl,
    render_calibration_summary,
    write_calibration_rows_jsonl,
)
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


def test_calibration_row_validates_buy_reference_and_deviation() -> None:
    row = make_calibration_row(
        side=FillSide.BUY,
        bid=Decimal("99"),
        ask=Decimal("100"),
        mid=Decimal("99.5"),
        spread=Decimal("1"),
        simbroker_fill_price=Decimal("102"),
        reference_price=Decimal("100"),
        absolute_deviation=Decimal("2"),
        pct_deviation=Decimal("0.02"),
        pass_15pct=True,
    )

    assert row.reference_price == Decimal("100")
    assert row.pass_15pct is True
    assert row.evidence_claim == NO_GATE_CLAIM

    with pytest.raises(ValidationError, match="reference_price"):
        make_calibration_row(side=FillSide.BUY, reference_price=Decimal("99"))
    with pytest.raises(ValidationError, match="pct_deviation"):
        make_calibration_row(pct_deviation=Decimal("0.01"))
    with pytest.raises(ValidationError, match="pass_15pct"):
        make_calibration_row(pass_15pct=False)


def test_calibration_row_validates_sell_reference() -> None:
    row = make_calibration_row(
        side=FillSide.SELL,
        bid=Decimal("99"),
        ask=Decimal("100"),
        mid=Decimal("99.5"),
        spread=Decimal("1"),
        simbroker_fill_price=Decimal("98"),
        reference_price=Decimal("99"),
        absolute_deviation=Decimal("1"),
        pct_deviation=Decimal("0.01010101010101010101010101010"),
        pass_15pct=True,
    )

    assert row.reference_price == Decimal("99")


def test_calibration_row_rejects_invalid_schema_fields() -> None:
    with pytest.raises(ValidationError, match="mid"):
        make_calibration_row(mid=Decimal("99.4"))
    with pytest.raises(ValidationError, match="spread"):
        make_calibration_row(spread=Decimal("2"))
    with pytest.raises(ValidationError, match="quote_source_hash"):
        make_calibration_row(quote_source_hash="")
    with pytest.raises(ValidationError, match="timezone-aware UTC"):
        make_calibration_row(fill_ts=datetime(2026, 5, 3, 12, 0))


def test_calibration_summary_counts_and_renders_packet_boundary() -> None:
    rows = (
        make_calibration_row(
            calibration_id="cal-1", symbol="BTC-USD", pct_deviation=Decimal("0.02")
        ),
        make_calibration_row(
            calibration_id="cal-2",
            symbol="BTC-USD",
            simbroker_fill_price=Decimal("104"),
            absolute_deviation=Decimal("4"),
            pct_deviation=Decimal("0.04"),
        ),
        make_calibration_row(
            calibration_id="cal-3",
            symbol="ETH-USD",
            simbroker_fill_price=Decimal("110"),
            absolute_deviation=Decimal("10"),
            pct_deviation=Decimal("0.10"),
        ),
        make_calibration_row(
            calibration_id="cal-4",
            symbol="ETH-USD",
            exclusion_reason="quote_outside_tolerance",
        ),
    )

    summary = build_calibration_summary(rows, min_included_rows=3)
    rendered = render_calibration_summary(summary)

    assert summary.total_rows == 4
    assert summary.included_rows == 3
    assert summary.excluded_rows == 1
    assert summary.pass_count == 3
    assert summary.packet_status == "PACKET_READY_FOR_REVIEW"
    assert summary.evidence_claim == NO_GATE_CLAIM
    assert summary.asset_summaries[0].symbol == "BTC-USD"
    assert summary.asset_summaries[0].median_pct_deviation == Decimal("0.030")
    assert "not_phase_gate_approval" in rendered
    assert "does not approve Phase 0" in rendered


def test_calibration_summary_reports_incomplete_and_failure_states() -> None:
    passing_row = make_calibration_row(calibration_id="pass")
    failing_row = make_calibration_row(
        calibration_id="fail",
        simbroker_fill_price=Decimal("120"),
        absolute_deviation=Decimal("20"),
        pct_deviation=Decimal("0.20"),
        pass_15pct=False,
    )

    incomplete = build_calibration_summary((passing_row,), min_included_rows=2)
    failed = build_calibration_summary((passing_row, failing_row), min_included_rows=2)

    assert incomplete.packet_status == "INCOMPLETE"
    assert failed.packet_status == "FAIL"
    assert failed.failure_count == 1


def test_calibration_rows_jsonl_round_trip(tmp_path) -> None:
    rows = (
        make_calibration_row(calibration_id="cal-1"),
        make_calibration_row(calibration_id="cal-2", symbol="ETH-USD"),
    )
    path = tmp_path / "calibration_rows.jsonl"

    write_calibration_rows_jsonl(rows, path)
    loaded = read_calibration_rows_jsonl(path)

    assert loaded == rows

    with pytest.raises(ValueError, match="duplicate"):
        write_calibration_rows_jsonl((rows[0], rows[0]), tmp_path / "duplicate.jsonl")


def test_build_calibration_row_from_fill_uses_side_reference_and_cost_fields() -> None:
    fill = process_fill(
        signal=make_signal(side=FillSide.SELL, proposed_price=99.5),
        bar=make_bar(),
        cost_config=make_cost_config(),
    )
    quote = BidAskQuote(
        symbol="BTC-USD",
        timestamp=UTC_TS,
        bid=99.0,
        ask=100.0,
    )

    row = build_calibration_row_from_fill(
        calibration_id="cal-fill-1",
        fill=fill,
        quote=quote,
        quote_source="kraken_public_api",
        quote_source_hash="source-hash",
        manual_verifier="reviewer",
        manual_verification_ts=UTC_TS,
        bar_open=Decimal("100"),
        bar_high=Decimal("105"),
        bar_low=Decimal("99"),
        bar_close=Decimal("103"),
    )

    assert row.side is FillSide.SELL
    assert row.reference_price == Decimal("99.0")
    assert row.simbroker_fill_price == fill.fill_price
    assert row.quantity == fill.quantity
    assert row.total_cost == fill.total_cost
    assert row.exclusion_reason is None
    assert row.evidence_claim == NO_GATE_CLAIM


def test_build_calibration_row_from_fill_excludes_stale_quote_without_failing() -> None:
    fill = process_fill(
        signal=make_signal(),
        bar=make_bar(),
        cost_config=make_cost_config(),
    )
    quote = BidAskQuote(
        symbol="BTC-USD",
        timestamp=UTC_TS - timedelta(minutes=10),
        bid=99.0,
        ask=100.0,
    )

    row = build_calibration_row_from_fill(
        calibration_id="cal-stale",
        fill=fill,
        quote=quote,
        quote_source="coinbase_exchange_public_api",
        quote_source_hash="source-hash",
        manual_verifier="reviewer",
        manual_verification_ts=UTC_TS,
        quote_tolerance=timedelta(minutes=5),
    )

    assert row.exclusion_reason == "quote_timestamp_outside_tolerance"


def test_build_calibration_row_from_fill_rejects_symbol_mismatch() -> None:
    fill = process_fill(
        signal=make_signal(symbol="BTC-USD"),
        bar=make_bar(),
        cost_config=make_cost_config(),
    )
    quote = BidAskQuote(
        symbol="ETH-USD",
        timestamp=UTC_TS,
        bid=99.0,
        ask=100.0,
    )

    with pytest.raises(ValueError, match="fill and quote symbols must match"):
        build_calibration_row_from_fill(
            calibration_id="cal-mismatch",
            fill=fill,
            quote=quote,
            quote_source="coinbase_exchange_public_api",
            quote_source_hash="source-hash",
            manual_verifier="reviewer",
            manual_verification_ts=UTC_TS,
        )


def make_calibration_row(**overrides: object) -> CalibrationRow:
    data = {
        "calibration_id": "cal-1",
        "symbol": "BTC-USD",
        "asset_class": "crypto",
        "side": FillSide.BUY,
        "fill_ts": UTC_TS,
        "quote_ts": UTC_TS,
        "quote_source": "manual-fixture",
        "quote_source_hash": "source-hash",
        "bid": Decimal("99"),
        "ask": Decimal("100"),
        "mid": Decimal("99.5"),
        "spread": Decimal("1"),
        "simbroker_fill_price": Decimal("102"),
        "bar_open": Decimal("100"),
        "bar_high": Decimal("105"),
        "bar_low": Decimal("99"),
        "bar_close": Decimal("103"),
        "quantity": Decimal("10"),
        "commission": Decimal("1.8"),
        "slippage": Decimal("0.2"),
        "market_impact": Decimal("0.2"),
        "borrow_rate": Decimal("0"),
        "funding_rate": Decimal("0"),
        "total_cost": Decimal("2.2"),
        "reference_price": Decimal("100"),
        "absolute_deviation": Decimal("2"),
        "pct_deviation": Decimal("0.02"),
        "pass_15pct": True,
        "manual_verifier": "manual-reviewer",
        "manual_verification_ts": UTC_TS,
        "exclusion_reason": None,
    }
    data.update(overrides)
    return CalibrationRow(**data)
