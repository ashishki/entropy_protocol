"""Deterministic asset universe and alias resolution."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InstrumentType(StrEnum):
    CRYPTO = "crypto"
    EQUITY = "equity"
    FUND = "fund"
    INDEX = "index"
    MACRO_PROXY = "macro_proxy"
    UNRESOLVED = "unresolved"


class ResolutionStatus(StrEnum):
    EXACT = "exact"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"


class AssetAlias(BaseModel):
    model_config = ConfigDict(strict=True)

    alias: str = Field(min_length=1)
    canonical_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    provenance: str = Field(min_length=1)


class Asset(BaseModel):
    model_config = ConfigDict(strict=True)

    canonical_id: str = Field(min_length=1)
    instrument_type: InstrumentType
    display_symbol: str = Field(min_length=1)
    provider_symbols: dict[str, str] = Field(default_factory=dict)
    aliases: list[str] = Field(default_factory=list)
    exchange: str | None = None
    venue: str | None = None
    provenance: str = Field(min_length=1)

    @field_validator("instrument_type", mode="before")
    @classmethod
    def _coerce_instrument_type(cls, value: object) -> InstrumentType:
        if isinstance(value, InstrumentType):
            return value
        if isinstance(value, str):
            return InstrumentType(value)
        raise ValueError("instrument_type must be an InstrumentType or string")


class AliasResolution(BaseModel):
    model_config = ConfigDict(strict=True)

    query: str
    normalized_query: str
    status: ResolutionStatus
    matches: list[Asset] = Field(default_factory=list)
    evidence: str = Field(min_length=1)

    @field_validator("status", mode="before")
    @classmethod
    def _coerce_status(cls, value: object) -> ResolutionStatus:
        if isinstance(value, ResolutionStatus):
            return value
        if isinstance(value, str):
            return ResolutionStatus(value)
        raise ValueError("status must be a ResolutionStatus or string")


class AssetRegistry:
    def __init__(self, assets: list[Asset], aliases: list[AssetAlias] | None = None):
        self._assets = {asset.canonical_id: asset for asset in assets}
        self._alias_index: dict[str, set[str]] = {}

        for asset in assets:
            for alias in [asset.display_symbol, *asset.aliases]:
                self._add_alias(alias, asset.canonical_id)
        for alias in aliases or []:
            if alias.canonical_id in self._assets:
                self._add_alias(alias.alias, alias.canonical_id)

    @property
    def assets(self) -> list[Asset]:
        return sorted(self._assets.values(), key=lambda asset: asset.canonical_id)

    def get(self, canonical_id: str) -> Asset | None:
        return self._assets.get(canonical_id)

    def resolve_alias(self, query: str, *, evidence: str) -> AliasResolution:
        normalized = normalize_alias(query)
        canonical_ids = sorted(self._alias_index.get(normalized, set()))
        matches = [self._assets[canonical_id] for canonical_id in canonical_ids]

        if len(matches) == 1:
            status = ResolutionStatus.EXACT
        elif matches:
            status = ResolutionStatus.AMBIGUOUS
        else:
            status = ResolutionStatus.UNRESOLVED

        return AliasResolution(
            query=query,
            normalized_query=normalized,
            status=status,
            matches=matches,
            evidence=evidence,
        )

    def _add_alias(self, alias: str, canonical_id: str) -> None:
        normalized = normalize_alias(alias)
        self._alias_index.setdefault(normalized, set()).add(canonical_id)


def normalize_alias(alias: str) -> str:
    return alias.strip().removeprefix("#").removeprefix("$").upper()


def seed_asset_registry() -> AssetRegistry:
    return AssetRegistry(
        assets=[
            Asset(
                canonical_id="CRYPTO:BTC",
                instrument_type=InstrumentType.CRYPTO,
                display_symbol="BTC",
                provider_symbols={"binance": "BTC/USDT", "yfinance": "BTC-USD"},
                aliases=["#BTC", "$BTC", "Bitcoin"],
                venue="crypto",
                provenance="Phase 12 seed registry requirement",
            ),
            Asset(
                canonical_id="CRYPTO:ETH",
                instrument_type=InstrumentType.CRYPTO,
                display_symbol="ETH",
                provider_symbols={"binance": "ETH/USDT", "yfinance": "ETH-USD"},
                aliases=["#ETH", "$ETH", "Ethereum"],
                venue="crypto",
                provenance="Phase 12 seed registry requirement",
            ),
            Asset(
                canonical_id="CRYPTO:SOL",
                instrument_type=InstrumentType.CRYPTO,
                display_symbol="SOL",
                provider_symbols={"binance": "SOL/USDT", "yfinance": "SOL-USD"},
                aliases=["#SOL", "$SOL", "Solana"],
                venue="crypto",
                provenance="Phase 12 seed registry requirement",
            ),
            Asset(
                canonical_id="US:SPY",
                instrument_type=InstrumentType.FUND,
                display_symbol="SPY",
                provider_symbols={"yfinance": "SPY"},
                aliases=["#SPY", "$SPY"],
                exchange="NYSEARCA",
                venue="us_equity",
                provenance="Phase 12 seed registry requirement",
            ),
            Asset(
                canonical_id="US:QQQ",
                instrument_type=InstrumentType.FUND,
                display_symbol="QQQ",
                provider_symbols={"yfinance": "QQQ"},
                aliases=["#QQQ", "$QQQ"],
                exchange="NASDAQ",
                venue="us_equity",
                provenance="Phase 12 seed registry requirement",
            ),
            *_pilot_equity_assets(),
            Asset(
                canonical_id="UNRESOLVED",
                instrument_type=InstrumentType.UNRESOLVED,
                display_symbol="UNRESOLVED",
                provider_symbols={},
                aliases=[],
                provenance=(
                    "Fallback marker; resolution still returns "
                    "status=unresolved instead of guessing"
                ),
            ),
        ]
    )


def _pilot_equity_assets() -> list[Asset]:
    observed_symbols = {
        "AMD": ("US:AMD", "NASDAQ"),
        "CHMF": ("MOEX:CHMF", "MOEX"),
        "GAZP": ("MOEX:GAZP", "MOEX"),
        "MAGN": ("MOEX:MAGN", "MOEX"),
        "SBER": ("MOEX:SBER", "MOEX"),
        "SFIN": ("MOEX:SFIN", "MOEX"),
        "VKCO": ("MOEX:VKCO", "MOEX"),
        "VTBR": ("MOEX:VTBR", "MOEX"),
        "X5": ("MOEX:X5", "MOEX"),
    }
    return [
        Asset(
            canonical_id=canonical_id,
            instrument_type=InstrumentType.EQUITY,
            display_symbol=symbol,
            provider_symbols={
                "yfinance": symbol if exchange != "MOEX" else f"{symbol}.ME"
            },
            aliases=[f"#{symbol}", f"${symbol}"],
            exchange=exchange,
            venue="equity",
            provenance="Observed in Phase 10 bablos79 captures",
        )
        for symbol, (canonical_id, exchange) in observed_symbols.items()
    ]
