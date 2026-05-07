"""Unit tests for approved free evidence source selection."""

from __future__ import annotations

import pytest

from entropy.evidence.source_selection import (
    REJECTED_FREE_SOURCES,
    SOURCE_SELECTION_ID,
    build_binance_monthly_klines_urls,
    get_approved_free_crypto_sources,
    source_ids,
    validate_source_use,
)


def test_free_crypto_sources_are_approved_for_expected_roles() -> None:
    sources = get_approved_free_crypto_sources()

    assert SOURCE_SELECTION_ID == "FREE-CRYPTO-SOURCES-v1"
    assert source_ids(sources) == (
        "binance_public_archive",
        "kraken_public_api",
        "coinbase_exchange_public_api",
    )
    assert all(source.asset_class == "crypto" for source in sources)
    assert all(not source.requires_api_key for source in sources)
    assert all(source.egress_allowed for source in sources)
    assert "alpha_vantage_free" in REJECTED_FREE_SOURCES
    assert "stooq_equity_daily" in REJECTED_FREE_SOURCES


def test_validate_source_use_accepts_only_approved_domain_and_use_case() -> None:
    source = validate_source_use(
        source_id="binance_public_archive",
        use_case="p4_label_coverage",
        domain="data.binance.vision",
    )

    assert source.source_id == "binance_public_archive"

    with pytest.raises(ValueError, match="not approved for"):
        validate_source_use(
            source_id="binance_public_archive",
            use_case="simbroker_calibration",
            domain="data.binance.vision",
        )
    with pytest.raises(ValueError, match="domain"):
        validate_source_use(
            source_id="kraken_public_api",
            use_case="simbroker_calibration",
            domain="api.exchange.coinbase.com",
        )
    with pytest.raises(ValueError, match="not approved"):
        validate_source_use(
            source_id="alpha_vantage_free",
            use_case="data_stability",
            domain="www.alphavantage.co",
        )


def test_build_binance_monthly_klines_urls_is_deterministic() -> None:
    urls = build_binance_monthly_klines_urls(
        symbol="BTCUSDT",
        interval="1d",
        start_year=2023,
        start_month=12,
        end_year=2024,
        end_month=2,
    )

    assert urls == (
        "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1d/BTCUSDT-1d-2023-12.zip",
        "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1d/BTCUSDT-1d-2024-01.zip",
        "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1d/BTCUSDT-1d-2024-02.zip",
    )


def test_build_binance_monthly_klines_urls_validates_inputs() -> None:
    with pytest.raises(ValueError, match="uppercase"):
        build_binance_monthly_klines_urls(
            symbol="btcusdt",
            interval="1d",
            start_year=2024,
            start_month=1,
            end_year=2024,
            end_month=1,
        )
    with pytest.raises(ValueError, match="interval"):
        build_binance_monthly_klines_urls(
            symbol="BTCUSDT",
            interval="2h",
            start_year=2024,
            start_month=1,
            end_year=2024,
            end_month=1,
        )
    with pytest.raises(ValueError, match="after"):
        build_binance_monthly_klines_urls(
            symbol="BTCUSDT",
            interval="1d",
            start_year=2024,
            start_month=2,
            end_year=2024,
            end_month=1,
        )
