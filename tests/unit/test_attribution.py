"""Unit tests for P&L attribution."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from math import sqrt
from typing import Any, cast

import pytest

from entropy.attribution import (
    STUB_REASON_CODE,
    AttributionInput,
    StreamBoundaryError,
    compute_drawdown_records,
    compute_net_sharpe,
    compute_performance_metrics,
    compute_streams,
)
from entropy.models.performance import PnLStreams
from entropy.models.registry import FillLog, FillSide

UTC_TS = datetime(2026, 5, 3, 12, 0, tzinfo=timezone.utc)


def make_fill_log(**overrides: object) -> FillLog:
    data = {
        "timestamp": UTC_TS,
        "symbol": "BTC-USD",
        "side": FillSide.BUY,
        "quantity": Decimal("1"),
        "fill_price": Decimal("100"),
        "commission": Decimal("0.10"),
        "slippage": Decimal("0.05"),
        "market_impact": Decimal("0.02"),
        "borrow_rate": Decimal("0.01"),
        "funding_rate": Decimal("0.00"),
        "total_cost": Decimal("0.18"),
        "constrained": False,
    }
    data.update(overrides)
    return FillLog(**data)


def test_four_stream_worked_example() -> None:
    entries = (
        AttributionInput(fill_log=make_fill_log(), stream_a_return=Decimal("0.01")),
        AttributionInput(
            fill_log=make_fill_log(
                commission=Decimal("0.11"),
                borrow_rate=Decimal("0.02"),
                total_cost=Decimal("0.20"),
            ),
            stream_a_return=Decimal("0.02"),
        ),
        AttributionInput(
            fill_log=make_fill_log(
                commission=Decimal("0.05"),
                slippage=Decimal("0.03"),
                borrow_rate=Decimal("0.02"),
                total_cost=Decimal("0.12"),
            ),
            stream_a_return=Decimal("-0.005"),
        ),
    )

    streams = compute_streams(entries)

    assert streams.stream_a == (Decimal("0.01"), Decimal("0.02"), Decimal("-0.005"))
    assert streams.stream_b == (Decimal("0"), Decimal("0"), Decimal("0"))
    assert streams.stream_c == (Decimal("-0.0018"), Decimal("-0.002"), Decimal("-0.0012"))
    assert streams.stream_d == (Decimal("0"), Decimal("0"), Decimal("0"))
    assert streams.net_sharpe_streams == (Decimal("0.0082"), Decimal("0.018"), Decimal("-0.0062"))

    net_sharpe = compute_net_sharpe(streams, confidence_interval_68=(-1.0, 1.0))
    assert net_sharpe.sample_length == 3
    assert net_sharpe.confidence_interval_68 == (-1.0, 1.0)


def test_net_sharpe_excludes_stream_d() -> None:
    active_returns = (
        Decimal("0.005"),
        Decimal("0.003"),
        Decimal("-0.002"),
        Decimal("0.004"),
        Decimal("0.001"),
    )
    streams = PnLStreams(
        stream_a=active_returns,
        stream_b=(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
        stream_c=(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
        stream_d=(Decimal("999"), Decimal("999"), Decimal("999"), Decimal("999"), Decimal("999")),
    )

    net_sharpe = compute_net_sharpe(streams, confidence_interval_68=(-0.25, 0.75), M_total=2)

    assert net_sharpe.value == pytest.approx(_manual_sample_sharpe(active_returns), abs=1e-12)
    assert net_sharpe.sample_length == len(active_returns)
    assert net_sharpe.M_total == 2
    with pytest.raises(StreamBoundaryError):
        compute_net_sharpe(cast(Any, streams.stream_d), confidence_interval_68=(-0.25, 0.75))


def test_drawdown_record_worked_example() -> None:
    timestamps = _timestamps(5)
    records = compute_drawdown_records(
        (
            Decimal("0.01"),
            Decimal("0.02"),
            Decimal("-0.04"),
            Decimal("-0.03"),
            Decimal("0.08"),
        ),
        timestamps,
    )

    assert len(records) == 1
    record = records[0]
    assert record.start_ts == timestamps[1]
    assert record.end_ts == timestamps[3]
    assert record.peak_value == Decimal("1.0302")
    assert record.trough_value == Decimal("0.95932224")
    assert record.drawdown_pct == pytest.approx(0.0688, abs=1e-12)
    assert record.recovery_ts == timestamps[4]


def test_net_sharpe_numerical_accuracy() -> None:
    active_returns = (
        Decimal("0.005"),
        Decimal("0.003"),
        Decimal("-0.002"),
        Decimal("0.004"),
        Decimal("0.001"),
    )
    streams = PnLStreams(
        stream_a=active_returns,
        stream_b=(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
        stream_c=(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
        stream_d=(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
    )

    net_sharpe = compute_net_sharpe(streams, confidence_interval_68=(-0.25, 0.75))

    assert net_sharpe.value == pytest.approx(_manual_sample_sharpe(active_returns), abs=1e-6)


def test_performance_metrics_stub_fields() -> None:
    streams = PnLStreams(
        stream_a=(
            Decimal("0.005"),
            Decimal("0.003"),
            Decimal("-0.002"),
            Decimal("0.004"),
            Decimal("0.001"),
        ),
        stream_b=(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
        stream_c=(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
        stream_d=(Decimal("100"), Decimal("100"), Decimal("100"), Decimal("100"), Decimal("100")),
    )

    metrics = compute_performance_metrics(
        streams,
        (
            Decimal("0.01"),
            Decimal("0.02"),
            Decimal("-0.04"),
            Decimal("-0.03"),
            Decimal("0.08"),
        ),
        _timestamps(5),
        confidence_interval_68=(-0.25, 0.75),
        calmar_ratio=1.7,
    )

    assert metrics.n_eff is None
    assert metrics.harvey_liu_deflated_sharpe is None
    assert metrics.reason_code == STUB_REASON_CODE
    assert metrics.calmar_ratio == 1.7
    assert metrics.max_drawdown.drawdown_pct == pytest.approx(0.0688, abs=1e-12)


def _timestamps(count: int) -> tuple[datetime, ...]:
    return tuple(UTC_TS + timedelta(days=offset) for offset in range(count))


def _manual_sample_sharpe(returns: tuple[Decimal, ...]) -> float:
    values = tuple(float(value) for value in returns)
    mean_return = sum(values) / len(values)
    sample_variance = sum((value - mean_return) ** 2 for value in values) / (len(values) - 1)
    return mean_return / sqrt(sample_variance)
