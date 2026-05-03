"""Data package."""

from entropy.data.fixture_adapter import LocalFixtureAdapter
from entropy.data.provider import (
    DataIngestionError,
    DataProvider,
    DataProviderError,
    DataQualityError,
    GapDetectionError,
    HealthStatus,
    OHLCVSanityError,
    ProviderNotFoundError,
    TimestampNormalizationError,
    provider_registry,
)
from entropy.data.quality import (
    DataQualityCheckResult,
    DataQualityReport,
    check_ohlcv_sanity,
    detect_gaps,
    run_all_checks,
    validate_timestamps,
)

__all__ = [
    "DataIngestionError",
    "DataProvider",
    "DataProviderError",
    "DataQualityCheckResult",
    "DataQualityError",
    "DataQualityReport",
    "GapDetectionError",
    "HealthStatus",
    "OHLCVSanityError",
    "ProviderNotFoundError",
    "LocalFixtureAdapter",
    "TimestampNormalizationError",
    "check_ohlcv_sanity",
    "detect_gaps",
    "provider_registry",
    "run_all_checks",
    "validate_timestamps",
]
