from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from signal_sandbox.prices.yfinance_dev import YFinanceDevProvider, YFinanceNotAllowed


class FakeYFinanceClient:
    def fetch_ohlcv(
        self,
        asset: str,
        *,
        range_start_utc: datetime,
        range_end_utc: datetime,
        interval: str,
    ) -> list[dict[str, Any]]:
        assert asset == "BTC-USD"
        assert interval == "1m"
        return [
            {
                "timestamp_utc": "2026-05-07T10:00:00+00:00",
                "open": "100",
                "high": "110",
                "low": "95",
                "close": "105",
                "volume": "12.5",
            }
        ]


def test_status_prototype() -> None:
    provider = YFinanceDevProvider(client=FakeYFinanceClient(), env=allowed_env())

    snapshot = provider.snapshot(
        assets=["BTC-USD"],
        range_start_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        range_end_utc=datetime(2026, 5, 7, 11, tzinfo=UTC),
        as_of_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
    )

    assert snapshot.provider_id == "yfinance-dev"
    assert snapshot.provider_status == "prototype"
    assert snapshot.assets == ["BTC-USD"]


def test_activation_gated() -> None:
    with pytest.raises(YFinanceNotAllowed):
        YFinanceDevProvider(client=FakeYFinanceClient(), env={})


def allowed_env() -> dict[str, str]:
    return {"SIGNAL_SANDBOX_ALLOW_YFINANCE": "1"}
