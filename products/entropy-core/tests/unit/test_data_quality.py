"""Unit tests for data provider interfaces."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy.exc import IntegrityError

from entropy.data import (
    DataIngestionError,
    DataProvider,
    DataProviderError,
    DataQualityError,
    GapDetectionError,
    HealthStatus,
    LocalFixtureAdapter,
    OHLCVSanityError,
    ProviderNotFoundError,
    TimestampNormalizationError,
    check_ohlcv_sanity,
    detect_gaps,
    provider_registry,
    run_all_checks,
    validate_timestamps,
)
from entropy.models.market import OHLCVBar, Timeframe


class ConcreteProvider(DataProvider):
    """Minimal concrete provider for ABC tests."""

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
    ) -> list[OHLCVBar]:
        return []

    def list_symbols(self) -> list[str]:
        return ["BTC-USD"]

    def check_health(self) -> HealthStatus:
        return HealthStatus(ok=True)


class MissingHealthProvider(DataProvider):
    """Provider intentionally missing check_health."""

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
    ) -> list[OHLCVBar]:
        return []

    def list_symbols(self) -> list[str]:
        return ["BTC-USD"]


class PlaceholderFixtureProvider(ConcreteProvider):
    """Placeholder fixture adapter class for provider registry tests."""


def test_data_provider_is_abstract() -> None:
    with pytest.raises(TypeError):
        DataProvider()  # pyright: ignore[reportAbstractUsage]


def test_concrete_provider_instantiates() -> None:
    provider = ConcreteProvider()

    assert provider.list_symbols() == ["BTC-USD"]
    assert provider.check_health() == HealthStatus(ok=True)


def test_provider_missing_method_raises_type_error() -> None:
    with pytest.raises(TypeError, match="check_health"):
        MissingHealthProvider()  # pyright: ignore[reportAbstractUsage]


def test_provider_registry_get_and_not_found() -> None:
    provider_registry.register("fixture", PlaceholderFixtureProvider)

    assert provider_registry.get("fixture") is PlaceholderFixtureProvider

    with pytest.raises(ProviderNotFoundError):
        provider_registry.get("unknown")


def test_error_hierarchy_inheritance() -> None:
    assert issubclass(DataProviderError, DataIngestionError)
    assert issubclass(DataQualityError, DataIngestionError)
    assert issubclass(TimestampNormalizationError, DataQualityError)
    assert issubclass(GapDetectionError, DataQualityError)
    assert issubclass(OHLCVSanityError, DataQualityError)
    assert issubclass(ProviderNotFoundError, DataProviderError)


def write_fixture_csv(path: Path) -> None:
    """Write a minimal valid OHLCV fixture."""
    path.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2026-05-01T00:00:00Z,100,110,95,105,12.5",
                "2026-05-01T01:00:00Z,105,112,101,108,8.0",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_fixture_adapter_parses_csv(tmp_path: Path) -> None:
    fixture_path = tmp_path / "BTC-USD_H1.csv"
    write_fixture_csv(fixture_path)
    adapter = LocalFixtureAdapter(fixture_path=fixture_path, data_dir=tmp_path / "data")

    bars = adapter.fetch_ohlcv(
        "BTC-USD",
        Timeframe.H1,
        datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc),
        datetime(2026, 5, 1, 1, 0, tzinfo=timezone.utc),
    )

    assert len(bars) == 2
    assert all(bar.timestamp.tzinfo is not None for bar in bars)
    assert bars[0].open == 100
    assert bars[0].high == 110
    assert bars[0].low == 95
    assert bars[0].close == 105
    assert bars[0].volume == 12.5


class FailingSession:
    """Session stub that fails during commit."""

    def add(self, instance: object) -> None:
        self.instance = instance

    def commit(self) -> None:
        raise IntegrityError("insert", {}, RuntimeError("duplicate"))

    def rollback(self) -> None:
        self.rolled_back = True

    def close(self) -> None:
        self.closed = True


def test_fixture_adapter_rolls_back_on_db_failure(tmp_path: Path) -> None:
    fixture_path = tmp_path / "BTC-USD_H1.csv"
    data_dir = tmp_path / "data"
    write_fixture_csv(fixture_path)
    adapter = LocalFixtureAdapter(
        fixture_path=fixture_path,
        data_dir=data_dir,
        session_factory=FailingSession,
    )

    with pytest.raises(IntegrityError):
        adapter.fetch_ohlcv(
            "BTC-USD",
            Timeframe.H1,
            datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2026, 5, 1, 1, 0, tzinfo=timezone.utc),
        )

    assert list(data_dir.rglob("*.parquet")) == []


def test_fixture_adapter_health_check(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()

    assert LocalFixtureAdapter(fixture_dir).check_health() == HealthStatus(ok=True)
    assert LocalFixtureAdapter(tmp_path / "missing").check_health() == HealthStatus(
        ok=False,
        reason="directory_missing",
    )


def valid_bar(timestamp: datetime | None = None) -> OHLCVBar:
    """Return a valid OHLCV bar for quality tests."""
    return OHLCVBar(
        timestamp=timestamp or datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=12.5,
    )


def test_validate_timestamps_raises_for_naive_datetime() -> None:
    bar = OHLCVBar.model_construct(
        timestamp=datetime(2026, 5, 1, 0, 0),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=12.5,
    )

    with pytest.raises(TimestampNormalizationError, match="bar index 0.*naive"):
        validate_timestamps([bar])


def test_validate_timestamps_raises_for_non_utc_timezone() -> None:
    bar = OHLCVBar.model_construct(
        timestamp=datetime(2026, 5, 1, 0, 0, tzinfo=ZoneInfo("America/New_York")),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=12.5,
    )

    with pytest.raises(TimestampNormalizationError, match="bar index 0.*non-UTC"):
        validate_timestamps([bar])


def test_detect_gaps_raises_at_threshold() -> None:
    first = valid_bar(datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc))
    second = valid_bar(first.timestamp + timedelta(seconds=3_601))

    with pytest.raises(GapDetectionError) as exc_info:
        detect_gaps([first, second], max_gap_seconds=3_600)

    message = str(exc_info.value)
    assert first.timestamp.isoformat() in message
    assert second.timestamp.isoformat() in message


def test_sanity_check_raises_for_zero_close() -> None:
    bar = OHLCVBar.model_construct(
        timestamp=datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc),
        open=100,
        high=110,
        low=95,
        close=0,
        volume=12.5,
    )

    with pytest.raises(OHLCVSanityError, match="bar index 0.*close"):
        check_ohlcv_sanity([bar])


def test_sanity_check_raises_for_high_below_close() -> None:
    bar = OHLCVBar.model_construct(
        timestamp=datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc),
        open=100,
        high=104,
        low=95,
        close=105,
        volume=12.5,
    )

    with pytest.raises(OHLCVSanityError, match="bar index 0.*high"):
        check_ohlcv_sanity([bar])


def test_run_all_checks_returns_report() -> None:
    passing_report = run_all_checks(
        [
            valid_bar(datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc)),
            valid_bar(datetime(2026, 5, 1, 1, 0, tzinfo=timezone.utc)),
        ],
        max_gap_seconds=3_600,
    )
    failing_bar = OHLCVBar.model_construct(
        timestamp=datetime(2026, 5, 1, 0, 0),
        open=100,
        high=104,
        low=95,
        close=105,
        volume=12.5,
    )
    failing_report = run_all_checks([failing_bar], max_gap_seconds=3_600)

    assert passing_report.status == "PASS"
    assert all(result.status == "PASS" for result in passing_report.per_check_results)
    assert failing_report.status == "FAIL"
    assert {
        result.check_name: result.affected_bar_count for result in failing_report.per_check_results
    } == {"timestamps": 1, "gaps": 0, "ohlcv_sanity": 1}
