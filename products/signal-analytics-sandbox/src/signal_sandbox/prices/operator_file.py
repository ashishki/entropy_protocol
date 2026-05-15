"""Operator-supplied OHLCV price provider."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Any

import polars as pl

from signal_sandbox.observability import LOGGER_NAME, get_tracer
from signal_sandbox.prices.base import (
    PriceDataError,
    PriceDataProvider,
    PriceSnapshot,
    make_price_snapshot,
)


class OperatorFilePriceError(PriceDataError):
    """Base exception for operator-file provider failures."""


class OperatorPriceFileMissing(OperatorFilePriceError):
    """Raised when an expected operator price input file is absent."""


class OperatorPriceFileMalformed(OperatorFilePriceError):
    """Raised when an operator price input file has invalid structure."""


REQUIRED_COLUMNS = {
    "timestamp_utc",
    "open",
    "high",
    "low",
    "close",
    "volume",
}


class OperatorFilePriceProvider(PriceDataProvider):
    provider_id = "operator-file"
    provider_status = "operator_supplied"

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self._logger = logging.getLogger(LOGGER_NAME)

    def snapshot(
        self,
        assets: list[str],
        range_start_utc: datetime,
        range_end_utc: datetime,
        as_of_utc: datetime,
    ) -> PriceSnapshot:
        started = perf_counter()
        with get_tracer().start_as_current_span("price.operator_file.snapshot"):
            try:
                rows = self._load_rows(assets, range_start_utc, range_end_utc)
                snapshot = make_price_snapshot(
                    provider_id=self.provider_id,
                    provider_status=self.provider_status,
                    as_of_utc=as_of_utc,
                    range_start_utc=range_start_utc,
                    range_end_utc=range_end_utc,
                    assets=assets,
                    rows=rows,
                )
            except PriceDataError:
                self._log_result("error", started)
                raise

        self._log_result("success", started)
        return snapshot

    def _load_rows(
        self,
        assets: list[str],
        range_start_utc: datetime,
        range_end_utc: datetime,
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        range_start = range_start_utc.isoformat()
        range_end = range_end_utc.isoformat()
        for asset in assets:
            input_path = self.workspace / "price_inputs" / f"{asset}.parquet"
            if not input_path.is_file():
                raise OperatorPriceFileMissing(f"missing price input for asset {asset}")

            frame = _read_validated_frame(input_path)
            for row in frame.to_dicts():
                timestamp = str(row["timestamp_utc"])
                if range_start <= timestamp <= range_end:
                    rows.append(
                        {
                            "asset": asset,
                            "timestamp_utc": timestamp,
                            "open": row["open"],
                            "high": row["high"],
                            "low": row["low"],
                            "close": row["close"],
                            "volume": row["volume"],
                        }
                    )
        return rows

    def _log_result(self, result: str, started: float) -> None:
        latency_ms = round((perf_counter() - started) * 1000, 3)
        self._logger.info(
            "price_provider_call",
            extra={
                "event_fields": {
                    "adapter_id": self.provider_id,
                    "result": result,
                    "latency_ms": latency_ms,
                }
            },
        )


def _read_validated_frame(path: Path) -> pl.DataFrame:
    try:
        frame = pl.read_parquet(path)
    except Exception as exc:
        raise OperatorPriceFileMalformed("price input is not readable parquet") from exc

    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise OperatorPriceFileMalformed(
            f"price input missing required columns: {sorted(missing)}"
        )
    return frame.select(sorted(REQUIRED_COLUMNS))
