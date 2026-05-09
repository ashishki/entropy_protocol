"""Deterministic horizon metrics over local market-data snapshots."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal
from enum import StrEnum
from io import BytesIO
from typing import Any

import polars as pl
from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.market_data.store import MarketDataSnapshot

ROUNDING_QUANT = Decimal("0.000001")
DEFAULT_HORIZONS = {"1d": 1, "3d": 3, "7d": 7, "30d": 30}


class Direction(StrEnum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class HorizonStatus(StrEnum):
    EVALUATED = "evaluated"
    INSUFFICIENT_DATA = "insufficient_data"
    UNRESOLVED_ASSET = "unresolved_asset"
    NON_DIRECTIONAL = "non_directional"


class HorizonMetric(BaseModel):
    model_config = ConfigDict(strict=True)

    horizon: str = Field(min_length=1)
    status: HorizonStatus
    canonical_asset_id: str = Field(min_length=1)
    entry_timestamp_utc: datetime | None = None
    horizon_end_utc: datetime | None = None
    return_pct: Decimal | None = None
    max_favorable_excursion_pct: Decimal | None = None
    max_adverse_excursion_pct: Decimal | None = None

    @field_validator("status", mode="before")
    @classmethod
    def _coerce_status(cls, value: object) -> HorizonStatus:
        if isinstance(value, HorizonStatus):
            return value
        if isinstance(value, str):
            return HorizonStatus(value)
        raise ValueError("status must be a HorizonStatus or string")

    @field_validator("entry_timestamp_utc", "horizon_end_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime | None:
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")


def evaluate_horizon_metrics(
    snapshot: MarketDataSnapshot,
    *,
    canonical_asset_id: str,
    post_timestamp_utc: datetime,
    direction: Direction,
) -> list[HorizonMetric]:
    if canonical_asset_id != snapshot.metadata.canonical_asset_id:
        return [
            _status_metric(horizon, canonical_asset_id, HorizonStatus.UNRESOLVED_ASSET)
            for horizon in DEFAULT_HORIZONS
        ]
    if direction not in {Direction.LONG, Direction.SHORT}:
        return [
            _status_metric(horizon, canonical_asset_id, HorizonStatus.NON_DIRECTIONAL)
            for horizon in DEFAULT_HORIZONS
        ]

    rows = _snapshot_rows(snapshot)
    return [
        _evaluate_one_horizon(
            rows=rows,
            canonical_asset_id=canonical_asset_id,
            post_timestamp_utc=post_timestamp_utc,
            direction=direction,
            horizon=horizon,
            days=days,
        )
        for horizon, days in DEFAULT_HORIZONS.items()
    ]


def _evaluate_one_horizon(
    *,
    rows: list[dict[str, Any]],
    canonical_asset_id: str,
    post_timestamp_utc: datetime,
    direction: Direction,
    horizon: str,
    days: int,
) -> HorizonMetric:
    horizon_end = post_timestamp_utc + timedelta(days=days)
    window = [
        row
        for row in rows
        if post_timestamp_utc <= row["timestamp_utc"] <= horizon_end
    ]
    if not window:
        return _status_metric(
            horizon,
            canonical_asset_id,
            HorizonStatus.INSUFFICIENT_DATA,
            horizon_end_utc=horizon_end,
        )

    entry = window[0]
    exit_row = window[-1]
    entry_close = entry["close"]
    exit_close = exit_row["close"]
    highs = [row["high"] for row in window]
    lows = [row["low"] for row in window]

    return_pct = _pct_change(exit_close, entry_close)
    if direction == Direction.SHORT:
        favorable = ((entry_close - min(lows)) / entry_close) * Decimal("100")
        adverse = ((entry_close - max(highs)) / entry_close) * Decimal("100")
    else:
        favorable = _pct_change(max(highs), entry_close)
        adverse = _pct_change(min(lows), entry_close)

    return HorizonMetric(
        horizon=horizon,
        status=HorizonStatus.EVALUATED,
        canonical_asset_id=canonical_asset_id,
        entry_timestamp_utc=entry["timestamp_utc"],
        horizon_end_utc=horizon_end,
        return_pct=_round(return_pct),
        max_favorable_excursion_pct=_round(favorable),
        max_adverse_excursion_pct=_round(adverse),
    )


def _snapshot_rows(snapshot: MarketDataSnapshot) -> list[dict[str, Any]]:
    frame = pl.read_parquet(BytesIO(snapshot.data_bytes))
    rows = []
    for row in frame.to_dicts():
        rows.append(
            {
                "timestamp_utc": datetime.fromisoformat(
                    str(row["timestamp_utc"]).replace("Z", "+00:00")
                ),
                "open": Decimal(str(row["open"])),
                "high": Decimal(str(row["high"])),
                "low": Decimal(str(row["low"])),
                "close": Decimal(str(row["close"])),
            }
        )
    return sorted(rows, key=lambda row: row["timestamp_utc"])


def _pct_change(later: Decimal, earlier: Decimal) -> Decimal:
    return ((later - earlier) / earlier) * Decimal("100")


def _round(value: Decimal) -> Decimal:
    return value.quantize(ROUNDING_QUANT, rounding=ROUND_HALF_EVEN)


def _status_metric(
    horizon: str,
    canonical_asset_id: str,
    status: HorizonStatus,
    *,
    horizon_end_utc: datetime | None = None,
) -> HorizonMetric:
    return HorizonMetric(
        horizon=horizon,
        status=status,
        canonical_asset_id=canonical_asset_id,
        horizon_end_utc=horizon_end_utc,
    )
