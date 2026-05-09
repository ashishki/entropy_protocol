"""Reset-era attribution stream boundary tests."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from decimal import Decimal
from math import sqrt
from typing import Any, cast

import pytest

from entropy.attribution import (
    AttributionInput,
    StreamBoundaryError,
    archive_only_attribution_payload,
    compute_net_sharpe,
    compute_streams,
)
from entropy.models.performance import PnLStreams
from entropy.models.registry import FillLog, FillSide

UTC_TS = datetime(2026, 5, 7, 12, 0, tzinfo=timezone.utc)


def test_net_sharpe_excludes_stream_d() -> None:
    """Primary Net Sharpe uses streams a+b+c and rejects raw stream d input."""
    streams = PnLStreams(
        stream_a=(
            Decimal("0.010"),
            Decimal("-0.004"),
            Decimal("0.006"),
            Decimal("0.002"),
            Decimal("-0.001"),
        ),
        stream_b=(
            Decimal("-0.001"),
            Decimal("0.003"),
            Decimal("0.000"),
            Decimal("-0.002"),
            Decimal("0.004"),
        ),
        stream_c=(
            Decimal("-0.002"),
            Decimal("-0.001"),
            Decimal("-0.001"),
            Decimal("-0.001"),
            Decimal("-0.002"),
        ),
        stream_d=(
            Decimal("100"),
            Decimal("200"),
            Decimal("300"),
            Decimal("400"),
            Decimal("500"),
        ),
    )

    net_sharpe = compute_net_sharpe(
        streams,
        confidence_interval_68=(-0.50, 0.50),
        M_total=3,
    )

    assert streams.net_sharpe_streams == (
        Decimal("0.007"),
        Decimal("-0.002"),
        Decimal("0.005"),
        Decimal("-0.001"),
        Decimal("0.001"),
    )
    assert net_sharpe.value == pytest.approx(
        _manual_sample_sharpe(streams.net_sharpe_streams),
        abs=1e-12,
    )
    assert net_sharpe.sample_length == 5
    assert net_sharpe.M_total == 3

    with pytest.raises(StreamBoundaryError, match="requires PnLStreams"):
        compute_net_sharpe(cast(Any, streams.stream_d), confidence_interval_68=(-0.50, 0.50))


def test_attribution_streams_are_separate_fields() -> None:
    """Attribution output keeps streams a, b, c, and d separate."""
    streams = compute_streams(
        (
            AttributionInput(
                fill_log=_fill_log(
                    commission=Decimal("0.08"),
                    slippage=Decimal("0.01"),
                    market_impact=Decimal("0.01"),
                    borrow_rate=Decimal("0.10"),
                    funding_rate=Decimal("0.00"),
                    total_cost=Decimal("0.20"),
                ),
                stream_a_return=Decimal("0.012"),
                stream_b_return=Decimal("-0.003"),
                stream_d_return=Decimal("0.001"),
            ),
            AttributionInput(
                fill_log=_fill_log(
                    commission=Decimal("0.04"),
                    slippage=Decimal("0.02"),
                    market_impact=Decimal("0.01"),
                    borrow_rate=Decimal("0.03"),
                    funding_rate=Decimal("0.05"),
                    total_cost=Decimal("0.15"),
                ),
                stream_a_return=Decimal("-0.004"),
                stream_b_return=Decimal("0.007"),
                stream_d_return=Decimal("0.002"),
            ),
        )
    )
    payload = archive_only_attribution_payload(streams)

    assert set(payload) == {
        "archive_only",
        "stream_a",
        "stream_b",
        "stream_c",
        "stream_d",
        "no_claim_labels",
    }
    assert payload["stream_a"] == ["0.012", "-0.004"]
    assert payload["stream_b"] == ["-0.003", "0.007"]
    assert payload["stream_c"] == ["-0.002", "-0.0015"]
    assert payload["stream_d"] == ["0.001", "0.002"]
    assert streams.net_sharpe_streams == (Decimal("0.007"), Decimal("0.0015"))


def test_archive_only_attribution_has_no_performance_conclusion() -> None:
    """Archive-only attribution payload does not serialize claim labels."""
    streams = PnLStreams(
        stream_a=(Decimal("0.003"), Decimal("-0.001")),
        stream_b=(Decimal("0.001"), Decimal("0.002")),
        stream_c=(Decimal("-0.001"), Decimal("-0.001")),
        stream_d=(Decimal("0.010"), Decimal("0.011")),
    )

    payload = archive_only_attribution_payload(streams)

    assert payload["archive_only"] is True
    assert "performance_conclusion" not in _payload_keys(payload)
    assert "oos_label" not in _payload_keys(payload)
    assert "phase_gate_evidence" not in _payload_keys(payload)
    assert "not_performance_conclusion" not in _payload_strings(payload)


def _fill_log(**overrides: object) -> FillLog:
    data = {
        "timestamp": UTC_TS,
        "symbol": "ETH-USD",
        "side": FillSide.SELL,
        "quantity": Decimal("1"),
        "fill_price": Decimal("100"),
        "commission": Decimal("0.01"),
        "slippage": Decimal("0.01"),
        "market_impact": Decimal("0.01"),
        "borrow_rate": Decimal("0.01"),
        "funding_rate": Decimal("0.00"),
        "total_cost": Decimal("0.04"),
        "constrained": False,
    }
    data.update(overrides)
    return FillLog(**data)


def _manual_sample_sharpe(returns: Sequence[Decimal]) -> float:
    values = tuple(float(value) for value in returns)
    mean_return = sum(values) / len(values)
    sample_variance = sum((value - mean_return) ** 2 for value in values) / (len(values) - 1)
    return mean_return / sqrt(sample_variance)


def _payload_keys(payload: Mapping[str, object]) -> set[str]:
    keys: set[str] = set()

    def visit(value: object) -> None:
        if isinstance(value, Mapping):
            keys.update(str(key) for key in value)
            for nested in value.values():
                visit(nested)
        elif isinstance(value, Sequence) and not isinstance(value, str):
            for nested in value:
                visit(nested)

    visit(payload)
    return keys


def _payload_strings(payload: Mapping[str, object]) -> set[str]:
    strings: set[str] = set()

    def visit(value: object) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                strings.add(str(key))
                visit(nested)
        elif isinstance(value, Sequence) and not isinstance(value, str):
            for nested in value:
                visit(nested)
        elif isinstance(value, str):
            strings.add(value)

    visit(payload)
    return strings
