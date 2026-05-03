"""OHLCV data quality validation helpers."""

from __future__ import annotations

from dataclasses import dataclass

from entropy.data.provider import GapDetectionError, OHLCVSanityError, TimestampNormalizationError
from entropy.models.market import OHLCVBar


@dataclass(frozen=True)
class DataQualityCheckResult:
    """Result for one data quality check."""

    check_name: str
    status: str
    affected_bar_count: int = 0
    message: str | None = None


@dataclass(frozen=True)
class DataQualityReport:
    """Aggregate data quality report."""

    status: str
    per_check_results: list[DataQualityCheckResult]


def validate_timestamps(bars: list[OHLCVBar]) -> None:
    """Require all bar timestamps to be timezone-aware UTC."""
    failures = _timestamp_failures(bars)
    if failures:
        raise TimestampNormalizationError(failures[0])


def detect_gaps(bars: list[OHLCVBar], *, max_gap_seconds: int) -> None:
    """Raise when consecutive bars are separated by more than max_gap_seconds."""
    failures = _gap_failures(bars, max_gap_seconds=max_gap_seconds)
    if failures:
        raise GapDetectionError(failures[0])


def check_ohlcv_sanity(bars: list[OHLCVBar]) -> None:
    """Validate OHLCV price and volume sanity."""
    failures = _ohlcv_failures(bars)
    if failures:
        raise OHLCVSanityError(failures[0])


def run_all_checks(bars: list[OHLCVBar], *, max_gap_seconds: int) -> DataQualityReport:
    """Return a per-check data quality report without raising."""
    check_failures = {
        "timestamps": _timestamp_failures(bars),
        "gaps": _gap_failures(bars, max_gap_seconds=max_gap_seconds),
        "ohlcv_sanity": _ohlcv_failures(bars),
    }
    results = [
        DataQualityCheckResult(
            check_name=check_name,
            status="FAIL" if failures else "PASS",
            affected_bar_count=len(failures),
            message=failures[0] if failures else None,
        )
        for check_name, failures in check_failures.items()
    ]
    status = "FAIL" if any(result.status == "FAIL" for result in results) else "PASS"
    return DataQualityReport(status=status, per_check_results=results)


def _timestamp_failures(bars: list[OHLCVBar]) -> list[str]:
    failures: list[str] = []
    for index, bar in enumerate(bars):
        timestamp = bar.timestamp
        if timestamp.tzinfo is None:
            failures.append("bar index " + str(index) + " has naive timestamp")
            continue

        offset = timestamp.utcoffset()
        if offset is None or offset.total_seconds() != 0:
            failures.append("bar index " + str(index) + " has non-UTC timestamp")
    return failures


def _gap_failures(bars: list[OHLCVBar], *, max_gap_seconds: int) -> list[str]:
    failures: list[str] = []
    sorted_bars = sorted(bars, key=lambda bar: bar.timestamp)
    for previous, current in zip(sorted_bars, sorted_bars[1:], strict=False):
        gap_seconds = (current.timestamp - previous.timestamp).total_seconds()
        if gap_seconds > max_gap_seconds:
            failures.append(
                "gap from "
                + previous.timestamp.isoformat()
                + " to "
                + current.timestamp.isoformat()
                + " exceeds "
                + str(max_gap_seconds)
                + " seconds"
            )
    return failures


def _ohlcv_failures(bars: list[OHLCVBar]) -> list[str]:
    failures: list[str] = []
    for index, bar in enumerate(bars):
        prefix = "bar index " + str(index) + ": "
        if bar.open <= 0:
            failures.append(prefix + "open must be positive")
        if bar.high <= 0:
            failures.append(prefix + "high must be positive")
        if bar.low <= 0:
            failures.append(prefix + "low must be positive")
        if bar.close <= 0:
            failures.append(prefix + "close must be positive")
        if bar.volume < 0:
            failures.append(prefix + "volume must be non-negative")
        if bar.high < max(bar.open, bar.close):
            failures.append(prefix + "high must be greater than or equal to open and close")
        if bar.low > min(bar.open, bar.close):
            failures.append(prefix + "low must be less than or equal to open and close")
    return failures
