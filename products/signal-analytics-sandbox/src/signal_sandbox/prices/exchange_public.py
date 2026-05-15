"""Public exchange OHLCV price provider."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from signal_sandbox.prices.base import (
    PriceDataError,
    PriceDataProvider,
    PriceSnapshot,
    make_price_snapshot,
)
from signal_sandbox.prices.snapshot import load_snapshot, save_snapshot


class PriceProviderUnavailable(PriceDataError):
    """Raised when a public exchange provider cannot fetch OHLCV data."""


class ExchangeClient(Protocol):
    enableRateLimit: bool

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        since: int | None = None,
        limit: int | None = None,
    ) -> list[list[float | int]]: ...


class ExchangePublicOHLCVProvider(PriceDataProvider):
    provider_status = "public_exchange"

    def __init__(
        self,
        workspace: Path,
        *,
        exchange: str,
        timeframe: str,
        client: ExchangeClient | None = None,
    ) -> None:
        self.workspace = workspace
        self.exchange = exchange
        self.timeframe = timeframe
        self.provider_id = f"exchange-public/{exchange}/{timeframe}"
        self.client = client or _build_ccxt_client(exchange)

    def snapshot(
        self,
        assets: list[str],
        range_start_utc: datetime,
        range_end_utc: datetime,
        as_of_utc: datetime,
    ) -> PriceSnapshot:
        snapshot_id = _snapshot_id(
            provider_id=self.provider_id,
            assets=assets,
            range_start_utc=range_start_utc,
            range_end_utc=range_end_utc,
            as_of_utc=as_of_utc,
        )
        try:
            return load_snapshot(self.workspace, snapshot_id)
        except FileNotFoundError:
            pass

        try:
            rows = self._fetch_rows(assets, range_start_utc, range_end_utc)
        except Exception as exc:
            raise PriceProviderUnavailable("public exchange OHLCV unavailable") from exc

        snapshot = make_price_snapshot(
            provider_id=self.provider_id,
            provider_status=self.provider_status,
            as_of_utc=as_of_utc,
            range_start_utc=range_start_utc,
            range_end_utc=range_end_utc,
            assets=assets,
            rows=rows,
        )
        save_snapshot(snapshot, self.workspace, snapshot_id=snapshot_id)
        return snapshot

    def _fetch_rows(
        self,
        assets: list[str],
        range_start_utc: datetime,
        range_end_utc: datetime,
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        since = _timestamp_ms(range_start_utc)
        for asset in assets:
            symbol = _asset_symbol(asset)
            for row in self.client.fetch_ohlcv(symbol, self.timeframe, since=since):
                timestamp_utc = datetime.fromtimestamp(row[0] / 1000, tz=UTC)
                if range_start_utc <= timestamp_utc <= range_end_utc:
                    rows.append(
                        {
                            "asset": asset,
                            "timestamp_utc": timestamp_utc.isoformat(),
                            "open": row[1],
                            "high": row[2],
                            "low": row[3],
                            "close": row[4],
                            "volume": row[5],
                        }
                    )
        return rows


def _build_ccxt_client(exchange: str) -> ExchangeClient:
    import ccxt  # type: ignore[import-untyped]

    exchange_cls = getattr(ccxt, exchange)
    return exchange_cls({"enableRateLimit": True})


def _asset_symbol(asset: str) -> str:
    return asset if "/" in asset else f"{asset}/USDT"


def _timestamp_ms(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def _snapshot_id(
    *,
    provider_id: str,
    assets: list[str],
    range_start_utc: datetime,
    range_end_utc: datetime,
    as_of_utc: datetime,
) -> str:
    payload = {
        "as_of_utc": as_of_utc.isoformat(),
        "assets": sorted(assets),
        "provider_id": provider_id,
        "range_end_utc": range_end_utc.isoformat(),
        "range_start_utc": range_start_utc.isoformat(),
    }
    digest = hashlib.sha256(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()
    return f"exchange-public-{digest}"
