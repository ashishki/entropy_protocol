"""Market data domain models."""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class Timeframe(str, Enum):
    """Supported OHLCV bar timeframes."""

    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"


class OHLCVBar(BaseModel):
    """One validated UTC OHLCV market data bar."""

    timestamp: datetime
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float = Field(ge=0)

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC timestamps."""
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("timestamp must be timezone-aware UTC")
        return value

    @model_validator(mode="after")
    def validate_price_sanity(self) -> "OHLCVBar":
        """Validate OHLC consistency against open and close."""
        if self.high < max(self.open, self.close):
            raise ValueError("high must be greater than or equal to max(open, close)")
        if self.low > min(self.open, self.close):
            raise ValueError("low must be less than or equal to min(open, close)")
        return self


class Dataset(BaseModel):
    """A non-empty OHLCV dataset plus provenance metadata."""

    bars: list[OHLCVBar] = Field(min_length=1)
    provenance: dict[str, Any] = Field(default_factory=dict)


class DatasetKey(BaseModel):
    """Stable identifier for a symbol/timeframe/date-range dataset."""

    symbol: str = Field(min_length=1)
    timeframe: Timeframe
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def validate_date_range(self) -> "DatasetKey":
        """Require a strictly increasing date range."""
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self
