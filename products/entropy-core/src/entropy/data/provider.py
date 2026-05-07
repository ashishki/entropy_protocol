"""Data provider interface and registry."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar

from entropy.models.market import OHLCVBar, Timeframe


class DataIngestionError(Exception):
    """Base error for data ingestion failures."""


class DataProviderError(DataIngestionError):
    """Raised when a provider cannot fetch or enumerate data."""


class DataQualityError(DataIngestionError):
    """Raised when ingested data fails quality checks."""


class TimestampNormalizationError(DataQualityError):
    """Raised when timestamps cannot be normalized to UTC."""


class GapDetectionError(DataQualityError):
    """Raised when bar gaps exceed the configured tolerance."""


class OHLCVSanityError(DataQualityError):
    """Raised when OHLCV values violate price/volume sanity rules."""


class ProviderNotFoundError(DataProviderError):
    """Raised when a named provider is not registered."""


@dataclass(frozen=True)
class HealthStatus:
    """Provider health check result."""

    ok: bool
    reason: str | None = None


class DataProvider(ABC):
    """Abstract interface for OHLCV providers."""

    @abstractmethod
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
    ) -> list[OHLCVBar]:
        """Fetch OHLCV bars for a symbol/timeframe/date range."""

    @abstractmethod
    def list_symbols(self) -> list[str]:
        """List symbols available from this provider."""

    @abstractmethod
    def check_health(self) -> HealthStatus:
        """Return provider health status."""


ProviderT = TypeVar("ProviderT", bound=type[DataProvider])


class ProviderRegistry:
    """Mapping from provider names to provider classes."""

    def __init__(self) -> None:
        self._providers: dict[str, type[DataProvider]] = {}

    def register(self, name: str, provider_class: ProviderT) -> ProviderT:
        """Register and return a provider class."""
        self._providers[name] = provider_class
        return provider_class

    def get(self, name: str) -> type[DataProvider]:
        """Return a provider class by name."""
        try:
            return self._providers[name]
        except KeyError as exc:
            raise ProviderNotFoundError("Provider not found: " + name) from exc


provider_registry = ProviderRegistry()
