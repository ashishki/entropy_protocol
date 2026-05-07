"""Local fixture data adapter and versioned Parquet store."""

from __future__ import annotations

import os
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol
from uuid import uuid4

import polars as pl

from entropy.data.provider import DataProvider, DataProviderError, DataQualityError, HealthStatus
from entropy.db.models import MarketDataset
from entropy.hashing import compute_dataset_hash
from entropy.models.market import OHLCVBar, Timeframe


class SessionLike(Protocol):
    """Minimal SQLAlchemy session surface needed for provenance writes."""

    def add(self, instance: object) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...

    def close(self) -> None: ...


SessionFactory = Callable[[], SessionLike]


class LocalFixtureAdapter(DataProvider):
    """Read local OHLCV fixtures, persist deterministic Parquet, and record provenance."""

    def __init__(
        self,
        fixture_dir: str | Path | None = None,
        *,
        fixture_path: str | Path | None = None,
        data_dir: str | Path | None = None,
        session_factory: SessionFactory | None = None,
    ) -> None:
        self.fixture_dir = Path(fixture_dir) if fixture_dir is not None else None
        self.fixture_path = Path(fixture_path) if fixture_path is not None else None
        env_data_dir = os.getenv("ENTROPY_DATA_DIR")
        if data_dir is not None:
            self.data_dir = Path(data_dir)
        elif env_data_dir is not None:
            self.data_dir = Path(env_data_dir)
        else:
            self.data_dir = Path("data")
        self.session_factory = session_factory

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
    ) -> list[OHLCVBar]:
        """Fetch, validate, persist, and optionally record local OHLCV fixture data."""
        requested_timeframe = Timeframe(timeframe)
        start_utc = _require_utc(start, "start")
        end_utc = _require_utc(end, "end")
        if end_utc <= start_utc:
            raise DataQualityError("end must be after start")

        source_path = self._resolve_source_path(symbol, requested_timeframe)
        source_frame = self._read_source(source_path)
        bars = _frame_to_bars(source_frame, start_utc, end_utc)
        parquet_frame = _bars_to_frame(bars)

        final_path: Path | None = None
        temp_path: Path | None = None
        try:
            dataset_dir = (
                self.data_dir / "market" / _safe_path_part(symbol) / requested_timeframe.value
            )
            dataset_dir.mkdir(parents=True, exist_ok=True)
            temp_path = dataset_dir / (".tmp-" + uuid4().hex + ".parquet")
            parquet_frame.write_parquet(temp_path)
            dataset_hash = compute_dataset_hash(temp_path)
            final_path = dataset_dir / (dataset_hash + ".parquet")
            temp_path.replace(final_path)
            temp_path = None

            if self.session_factory is not None:
                self._record_provenance(
                    dataset_hash=dataset_hash,
                    symbol=symbol,
                    timeframe=requested_timeframe,
                    source_path=source_path,
                    parquet_path=final_path,
                    bars=bars,
                    requested_start=start_utc,
                    requested_end=end_utc,
                )
        except Exception:
            _remove_if_exists(temp_path)
            _remove_if_exists(final_path)
            raise

        return bars

    def list_symbols(self) -> list[str]:
        """List symbols discoverable from fixture filenames."""
        if self.fixture_path is not None:
            return [_symbol_from_stem(self.fixture_path.stem)]
        if self.fixture_dir is None or not self.fixture_dir.exists():
            return []

        symbols = {
            _symbol_from_stem(path.stem)
            for path in self.fixture_dir.iterdir()
            if path.suffix.lower() in {".csv", ".parquet"}
        }
        return sorted(symbols)

    def check_health(self) -> HealthStatus:
        """Return whether the configured fixture directory is readable."""
        if self.fixture_path is not None:
            if self.fixture_path.exists() and os.access(self.fixture_path, os.R_OK):
                return HealthStatus(ok=True)
            return HealthStatus(ok=False, reason="directory_missing")

        if self.fixture_dir is None or not self.fixture_dir.exists():
            return HealthStatus(ok=False, reason="directory_missing")
        if not self.fixture_dir.is_dir() or not os.access(self.fixture_dir, os.R_OK):
            return HealthStatus(ok=False, reason="directory_missing")
        return HealthStatus(ok=True)

    def _resolve_source_path(self, symbol: str, timeframe: Timeframe) -> Path:
        if self.fixture_path is not None:
            return _require_supported_file(self.fixture_path)

        symbol_path = Path(symbol)
        if symbol_path.suffix.lower() in {".csv", ".parquet"} and symbol_path.exists():
            return _require_supported_file(symbol_path)

        if self.fixture_dir is None:
            raise DataProviderError("fixture_dir is required when fixture_path is not set")

        base_name = _safe_path_part(symbol) + "_" + timeframe.value
        for suffix in (".csv", ".parquet"):
            candidate = self.fixture_dir / (base_name + suffix)
            if candidate.exists():
                return _require_supported_file(candidate)

        raise DataProviderError("fixture file not found for symbol/timeframe")

    def _read_source(self, source_path: Path) -> pl.DataFrame:
        if source_path.suffix.lower() == ".csv":
            return pl.read_csv(source_path)
        if source_path.suffix.lower() == ".parquet":
            return pl.read_parquet(source_path)
        raise DataProviderError("unsupported fixture format")

    def _record_provenance(
        self,
        *,
        dataset_hash: str,
        symbol: str,
        timeframe: Timeframe,
        source_path: Path,
        parquet_path: Path,
        bars: list[OHLCVBar],
        requested_start: datetime,
        requested_end: datetime,
    ) -> None:
        session = self.session_factory() if self.session_factory is not None else None
        if session is None:
            return

        provenance = {
            "adapter": "LocalFixtureAdapter",
            "source_format": source_path.suffix.lower().lstrip("."),
            "requested_start": requested_start.isoformat(),
            "requested_end": requested_end.isoformat(),
        }
        record = MarketDataset(
            dataset_hash=dataset_hash,
            symbol=symbol,
            timeframe=timeframe.value,
            start_ts=bars[0].timestamp,
            end_ts=bars[-1].timestamp,
            row_count=len(bars),
            source_path=str(source_path),
            parquet_path=str(parquet_path),
            provenance=provenance,
        )

        try:
            session.add(record)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def _frame_to_bars(frame: pl.DataFrame, start: datetime, end: datetime) -> list[OHLCVBar]:
    rename_map = {column: column.lower() for column in frame.columns}
    normalized = frame.rename(rename_map)
    required_columns = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required_columns.difference(normalized.columns)
    if missing:
        raise DataQualityError("missing OHLCV columns: " + ", ".join(sorted(missing)))

    bars: list[OHLCVBar] = []
    for row in normalized.select(sorted(required_columns)).to_dicts():
        timestamp = _parse_timestamp(row["timestamp"])
        if start <= timestamp <= end:
            bars.append(
                OHLCVBar(
                    timestamp=timestamp,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                )
            )

    if not bars:
        raise DataQualityError("fixture returned no bars for requested range")

    return sorted(bars, key=lambda bar: bar.timestamp)


def _bars_to_frame(bars: list[OHLCVBar]) -> pl.DataFrame:
    return pl.DataFrame(
        [
            {
                "timestamp": bar.timestamp.isoformat().replace("+00:00", "Z"),
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume,
            }
            for bar in bars
        ]
    )


def _parse_timestamp(value: object) -> datetime:
    if isinstance(value, datetime):
        return _require_utc(value, "timestamp")
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return _require_utc(parsed, "timestamp")
    raise DataQualityError("timestamp must be an ISO-8601 string or datetime")


def _require_utc(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None:
        raise DataQualityError(field_name + " must be timezone-aware UTC")
    return value.astimezone(timezone.utc)


def _require_supported_file(path: Path) -> Path:
    if path.suffix.lower() not in {".csv", ".parquet"}:
        raise DataProviderError("unsupported fixture format")
    if not path.exists():
        raise DataProviderError("fixture file not found")
    return path


def _remove_if_exists(path: Path | None) -> None:
    if path is not None and path.exists():
        path.unlink()


def _safe_path_part(value: str) -> str:
    return value.replace("/", "_").replace("\\", "_")


def _symbol_from_stem(stem: str) -> str:
    if "_" not in stem:
        return stem
    return stem.rsplit("_", maxsplit=1)[0]
