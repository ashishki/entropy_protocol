"""Unit tests for the Phase 0 crypto universe snapshot."""

from __future__ import annotations

from entropy.evidence.crypto_universe import (
    CRYPTO_UNIVERSE_ID,
    P4_REVISED_CRYPTO_UNIVERSE_ID,
    get_default_phase0_crypto_universe,
    get_default_phase0_p4_crypto_universe,
    render_crypto_universe_snapshot,
)


def test_default_crypto_universe_has_twenty_ranked_assets() -> None:
    snapshot = get_default_phase0_crypto_universe()

    assert snapshot.universe_id == CRYPTO_UNIVERSE_ID
    assert snapshot.source_selection_id == "FREE-CRYPTO-SOURCES-v1"
    assert len(snapshot.assets) == 20
    assert tuple(asset.rank for asset in snapshot.assets) == tuple(range(1, 21))
    assert snapshot.assets[0].binance_symbol == "BTCUSDT"
    assert all(asset.calendar_profile == "continuous" for asset in snapshot.assets)
    assert len({asset.binance_symbol for asset in snapshot.assets}) == 20


def test_default_crypto_universe_hash_is_deterministic() -> None:
    first = get_default_phase0_crypto_universe()
    second = get_default_phase0_crypto_universe()

    assert first.universe_hash == second.universe_hash
    assert len(first.universe_hash) == 64


def test_revised_p4_crypto_universe_replaces_late_listed_assets() -> None:
    snapshot = get_default_phase0_p4_crypto_universe()
    symbols = tuple(asset.binance_symbol for asset in snapshot.assets)

    assert snapshot.universe_id == P4_REVISED_CRYPTO_UNIVERSE_ID
    assert len(snapshot.assets) == 20
    assert len(set(symbols)) == 20
    assert "BTCUSDT" in symbols
    assert "XLMUSDT" in symbols
    assert "XTZUSDT" in symbols
    assert "SOLUSDT" not in symbols
    assert "AVAXUSDT" not in symbols


def test_render_crypto_universe_snapshot_contains_boundary() -> None:
    snapshot = get_default_phase0_crypto_universe()
    rendered = render_crypto_universe_snapshot(snapshot)

    assert "PHASE0-CRYPTO-20-v1" in rendered
    assert snapshot.universe_hash in rendered
    assert "| 1 | BTC | BTCUSDT | XBT/USD | BTC-USD | continuous |" in rendered
    assert "does not approve Phase 0" in rendered
