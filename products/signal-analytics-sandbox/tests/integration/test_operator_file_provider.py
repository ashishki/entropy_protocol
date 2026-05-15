from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

import polars as pl
import pytest

from signal_sandbox.prices.operator_file import (
    OperatorFilePriceProvider,
    OperatorPriceFileMalformed,
    OperatorPriceFileMissing,
)


def write_price_input(workspace: Path, asset: str = "BTC") -> None:
    input_dir = workspace / "price_inputs"
    input_dir.mkdir(parents=True)
    pl.DataFrame(
        {
            "timestamp_utc": [
                "2026-05-07T10:00:00+00:00",
                "2026-05-07T10:01:00+00:00",
            ],
            "open": ["90", "100"],
            "high": ["101", "110"],
            "low": ["89", "95"],
            "close": ["100", "105"],
            "volume": ["10", "12.5"],
        }
    ).write_parquet(input_dir / f"{asset}.parquet")


def snapshot(provider: OperatorFilePriceProvider):
    return provider.snapshot(
        assets=["BTC"],
        range_start_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        range_end_utc=datetime(2026, 5, 7, 11, tzinfo=UTC),
        as_of_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
    )


def test_basic_snapshot(tmp_path: Path) -> None:
    write_price_input(tmp_path)
    provider = OperatorFilePriceProvider(tmp_path)

    result = snapshot(provider)

    assert result.provider_id == "operator-file"
    assert result.provider_status == "operator_supplied"
    assert result.assets == ["BTC"]
    assert result.sha256 == hashlib.sha256(result.ohlcv_bytes).hexdigest()


def test_idempotent(tmp_path: Path) -> None:
    write_price_input(tmp_path)
    provider = OperatorFilePriceProvider(tmp_path)

    first = snapshot(provider)
    second = snapshot(provider)

    assert first.sha256 == second.sha256
    assert first.canonical_bytes() == second.canonical_bytes()


def test_missing_and_malformed(tmp_path: Path) -> None:
    provider = OperatorFilePriceProvider(tmp_path)

    with pytest.raises(OperatorPriceFileMissing):
        snapshot(provider)

    input_dir = tmp_path / "price_inputs"
    input_dir.mkdir(parents=True)
    pl.DataFrame({"timestamp_utc": ["2026-05-07T10:00:00+00:00"]}).write_parquet(
        input_dir / "BTC.parquet"
    )

    with pytest.raises(OperatorPriceFileMalformed):
        snapshot(provider)
