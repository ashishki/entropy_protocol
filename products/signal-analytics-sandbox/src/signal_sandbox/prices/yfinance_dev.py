"""Prototype-only yfinance price provider."""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Protocol

from signal_sandbox.prices.base import (
    PriceDataProvider,
    PriceSnapshot,
    make_price_snapshot,
)

ALLOW_YFINANCE_ENV = "SIGNAL_SANDBOX_ALLOW_YFINANCE"


class YFinanceNotAllowed(Exception):
    """Raised when the prototype yfinance provider is not explicitly enabled."""


class YFinanceClient(Protocol):
    def fetch_ohlcv(
        self,
        asset: str,
        *,
        range_start_utc: datetime,
        range_end_utc: datetime,
        interval: str,
    ) -> Sequence[Mapping[str, Any]]: ...


class YFinanceDevProvider(PriceDataProvider):
    provider_id = "yfinance-dev"
    provider_status = "prototype"

    def __init__(
        self,
        *,
        interval: str = "1m",
        client: YFinanceClient | None = None,
        env: Mapping[str, str] | None = None,
    ) -> None:
        effective_env = os.environ if env is None else env
        if effective_env.get(ALLOW_YFINANCE_ENV) != "1":
            raise YFinanceNotAllowed(
                f"{ALLOW_YFINANCE_ENV}=1 is required for yfinance prototype prices"
            )
        self.interval = interval
        self.client = client or _YFinanceClient()

    def snapshot(
        self,
        assets: list[str],
        range_start_utc: datetime,
        range_end_utc: datetime,
        as_of_utc: datetime,
    ) -> PriceSnapshot:
        rows: list[Mapping[str, Any]] = []
        for asset in assets:
            for row in self.client.fetch_ohlcv(
                asset,
                range_start_utc=range_start_utc,
                range_end_utc=range_end_utc,
                interval=self.interval,
            ):
                rows.append({"asset": asset, **dict(row)})

        return make_price_snapshot(
            provider_id=self.provider_id,
            provider_status=self.provider_status,
            as_of_utc=as_of_utc,
            range_start_utc=range_start_utc,
            range_end_utc=range_end_utc,
            assets=assets,
            rows=rows,
        )


class _YFinanceClient:
    def fetch_ohlcv(
        self,
        asset: str,
        *,
        range_start_utc: datetime,
        range_end_utc: datetime,
        interval: str,
    ) -> Sequence[Mapping[str, Any]]:
        import yfinance as yf  # type: ignore[import-untyped]

        frame = yf.Ticker(asset).history(
            start=range_start_utc,
            end=range_end_utc,
            interval=interval,
        )
        rows: list[Mapping[str, Any]] = []
        for timestamp, row in frame.iterrows():
            rows.append(
                {
                    "timestamp_utc": _timestamp_to_isoformat(timestamp),
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": row["Volume"],
                }
            )
        return rows


def _timestamp_to_isoformat(value: object) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    to_pydatetime = getattr(value, "to_pydatetime", None)
    if callable(to_pydatetime):
        converted = to_pydatetime()
        if isinstance(converted, datetime):
            return converted.isoformat()
    return str(value)
