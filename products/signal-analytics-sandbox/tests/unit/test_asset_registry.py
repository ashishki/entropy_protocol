from __future__ import annotations

from signal_sandbox.assets import (
    Asset,
    AssetAlias,
    AssetRegistry,
    InstrumentType,
    ResolutionStatus,
    seed_asset_registry,
)


def test_asset_alias_schema_round_trip() -> None:
    asset = Asset(
        canonical_id="CRYPTO:BTC",
        instrument_type=InstrumentType.CRYPTO,
        display_symbol="BTC",
        provider_symbols={"binance": "BTC/USDT", "yfinance": "BTC-USD"},
        aliases=["#BTC", "$BTC", "Bitcoin"],
        venue="crypto",
        provenance="unit test",
    )
    alias = AssetAlias(
        alias="#BTC",
        canonical_id=asset.canonical_id,
        source="unit",
        provenance="unit test",
    )

    loaded_asset = Asset.model_validate_json(asset.model_dump_json())
    loaded_alias = AssetAlias.model_validate_json(alias.model_dump_json())

    assert loaded_asset == asset
    assert loaded_alias == alias
    assert loaded_asset.instrument_type == InstrumentType.CRYPTO
    assert loaded_asset.provider_symbols["binance"] == "BTC/USDT"
    assert "#BTC" in loaded_asset.aliases
    assert loaded_asset.venue == "crypto"
    assert loaded_asset.provenance == "unit test"


def test_alias_resolution_never_guesses() -> None:
    registry = AssetRegistry(
        assets=[
            Asset(
                canonical_id="US:ABC",
                instrument_type=InstrumentType.EQUITY,
                display_symbol="ABC",
                provider_symbols={"yfinance": "ABC"},
                aliases=["#ABC"],
                exchange="NYSE",
                provenance="unit test",
            ),
            Asset(
                canonical_id="MOEX:ABC",
                instrument_type=InstrumentType.EQUITY,
                display_symbol="ABC.ME",
                provider_symbols={"yfinance": "ABC.ME"},
                aliases=["ABC", "#ABC"],
                exchange="MOEX",
                provenance="unit test",
            ),
        ]
    )

    ambiguous = registry.resolve_alias("#ABC", evidence="capture-1")
    unresolved = registry.resolve_alias("#DOESNOTEXIST", evidence="capture-2")

    assert ambiguous.status == ResolutionStatus.AMBIGUOUS
    assert {asset.canonical_id for asset in ambiguous.matches} == {
        "MOEX:ABC",
        "US:ABC",
    }
    assert ambiguous.evidence == "capture-1"
    assert unresolved.status == ResolutionStatus.UNRESOLVED
    assert unresolved.matches == []
    assert unresolved.evidence == "capture-2"


def test_seed_registry_contains_required_assets() -> None:
    registry = seed_asset_registry()

    required = {
        "CRYPTO:BTC",
        "CRYPTO:ETH",
        "CRYPTO:SOL",
        "US:SPY",
        "US:QQQ",
        "US:AMD",
        "MOEX:CHMF",
        "MOEX:GAZP",
        "MOEX:MAGN",
        "MOEX:SBER",
        "MOEX:SFIN",
        "MOEX:VKCO",
        "MOEX:VTBR",
        "MOEX:X5",
        "UNRESOLVED",
    }

    assert {asset.canonical_id for asset in registry.assets} >= required
    assert (
        registry.resolve_alias("#BTC", evidence="seed").status
        == ResolutionStatus.EXACT
    )
    assert (
        registry.resolve_alias("btc", evidence="seed").matches[0].canonical_id
        == "CRYPTO:BTC"
    )
    assert (
        registry.resolve_alias("#MAGN", evidence="seed").matches[0].canonical_id
        == "MOEX:MAGN"
    )
    assert (
        registry.resolve_alias("#UNKNOWN", evidence="seed").status
        == ResolutionStatus.UNRESOLVED
    )
