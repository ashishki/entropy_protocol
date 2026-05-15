"""Data package."""

from entropy.data.fixture_adapter import LocalFixtureAdapter
from entropy.data.holdout import HoldoutReadDecision, HoldoutReadRequest, authorize_holdout_read
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
from entropy.data.stability import (
    NO_STABILITY_GATE_CLAIM,
    STABILITY_METHOD_ID,
    DataStabilityAssetSummary,
    DataStabilityRow,
    DataStabilitySummary,
    build_data_stability_summary,
    read_data_stability_rows_jsonl,
    render_data_stability_summary,
    write_data_stability_rows_jsonl,
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
    "HoldoutReadDecision",
    "HoldoutReadRequest",
    "OHLCVSanityError",
    "ProviderNotFoundError",
    "LocalFixtureAdapter",
    "NO_STABILITY_GATE_CLAIM",
    "TimestampNormalizationError",
    "STABILITY_METHOD_ID",
    "DataStabilityAssetSummary",
    "DataStabilityRow",
    "DataStabilitySummary",
    "build_data_stability_summary",
    "authorize_holdout_read",
    "check_ohlcv_sanity",
    "detect_gaps",
    "provider_registry",
    "read_data_stability_rows_jsonl",
    "render_data_stability_summary",
    "run_all_checks",
    "validate_timestamps",
    "write_data_stability_rows_jsonl",
]
