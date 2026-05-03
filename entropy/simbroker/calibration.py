"""Bid/ask calibration interface for future SimBroker provider work."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, field_validator, model_validator


class BidAskQuote(BaseModel):
    """One bid/ask observation from an external or recorded market-data source."""

    symbol: str = Field(min_length=1)
    timestamp: datetime
    bid: float = Field(gt=0.0)
    ask: float = Field(gt=0.0)

    @field_validator("symbol")
    @classmethod
    def symbol_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only symbols."""
        if not value.strip():
            raise ValueError("symbol must not be blank")
        return value

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC quote timestamps."""
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("timestamp must be timezone-aware UTC")
        return value

    @model_validator(mode="after")
    def validate_spread(self) -> "BidAskQuote":
        """Require a non-inverted spread."""
        if self.ask < self.bid:
            raise ValueError("ask must be greater than or equal to bid")
        return self


class BidAskProvider(ABC):
    """Abstract bid/ask lookup boundary for Phase 1+ broker calibration work."""

    @abstractmethod
    def get_bid_ask(self, symbol: str, timestamp: datetime) -> BidAskQuote | None:
        """Return a bid/ask quote for the symbol and timestamp, or None if unavailable."""
        raise NotImplementedError


class NoOpBidAskProvider(BidAskProvider):
    """Phase 0 placeholder provider that never returns broker calibration data."""

    def get_bid_ask(self, symbol: str, timestamp: datetime) -> None:
        """Return no quote without contacting external systems."""
        return None
