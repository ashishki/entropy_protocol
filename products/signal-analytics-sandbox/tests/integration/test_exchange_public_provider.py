from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from signal_sandbox.prices.exchange_public import (
    ExchangePublicOHLCVProvider,
    PriceProviderUnavailable,
)


class FakeExchangeClient:
    enableRateLimit = True

    def __init__(self, rows: list[list[float | int]] | None = None) -> None:
        self.rows = rows or [
            [
                int(datetime(2026, 5, 7, 10, tzinfo=UTC).timestamp() * 1000),
                100,
                110,
                95,
                105,
                12.5,
            ]
        ]
        self.calls = 0

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        since: int | None = None,
        limit: int | None = None,
    ) -> list[list[float | int]]:
        self.calls += 1
        assert symbol == "BTC/USDT"
        assert timeframe == "1m"
        assert since == int(datetime(2026, 5, 7, 10, tzinfo=UTC).timestamp() * 1000)
        return self.rows


class FailingExchangeClient(FakeExchangeClient):
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        since: int | None = None,
        limit: int | None = None,
    ) -> list[list[float | int]]:
        self.calls += 1
        raise RuntimeError("network unavailable")


def snapshot(provider: ExchangePublicOHLCVProvider):
    return provider.snapshot(
        assets=["BTC"],
        range_start_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        range_end_utc=datetime(2026, 5, 7, 11, tzinfo=UTC),
        as_of_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
    )


def test_basic_snapshot(tmp_path: Path) -> None:
    client = FakeExchangeClient()
    provider = ExchangePublicOHLCVProvider(
        tmp_path,
        exchange="binance",
        timeframe="1m",
        client=client,
    )

    result = snapshot(provider)

    assert provider.client.enableRateLimit is True
    assert result.provider_id == "exchange-public/binance/1m"
    assert result.provider_status == "public_exchange"
    assert result.assets == ["BTC"]
    assert client.calls == 1


def test_cache_hit_no_network(tmp_path: Path) -> None:
    client = FakeExchangeClient()
    provider = ExchangePublicOHLCVProvider(
        tmp_path,
        exchange="binance",
        timeframe="1m",
        client=client,
    )

    first = snapshot(provider)
    second = snapshot(provider)

    assert first == second
    assert client.calls == 1


def test_failure_no_partial_snapshot(tmp_path: Path) -> None:
    provider = ExchangePublicOHLCVProvider(
        tmp_path,
        exchange="binance",
        timeframe="1m",
        client=FailingExchangeClient(),
    )

    with pytest.raises(PriceProviderUnavailable):
        snapshot(provider)

    snapshots_dir = tmp_path / "snapshots"
    assert not snapshots_dir.exists() or list(snapshots_dir.iterdir()) == []
