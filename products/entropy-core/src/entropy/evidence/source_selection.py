"""Approved free evidence source selection for Phase 0 bootstrap."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

EvidenceUseCase = Literal["p4_label_coverage", "simbroker_calibration", "data_stability"]
SourceRole = Literal["primary", "cross_check"]

SOURCE_SELECTION_ID = "FREE-CRYPTO-SOURCES-v1"


@dataclass(frozen=True)
class ApprovedEvidenceSource:
    """Approved free source boundary for evidence collection."""

    source_id: str
    role: SourceRole
    use_cases: tuple[EvidenceUseCase, ...]
    domains: tuple[str, ...]
    asset_class: str
    requires_api_key: bool
    egress_allowed: bool
    notes: str


@dataclass(frozen=True)
class BinanceArchiveKlinesPath:
    """Deterministic Binance public archive klines path."""

    symbol: str
    interval: str
    year: int
    month: int
    market: Literal["spot"] = "spot"

    @property
    def url(self) -> str:
        file_name = f"{self.symbol}-{self.interval}-{self.year}-{self.month:02d}.zip"
        return (
            "https://data.binance.vision/data/"
            f"{self.market}/monthly/klines/{self.symbol}/{self.interval}/{file_name}"
        )


APPROVED_FREE_CRYPTO_SOURCES: tuple[ApprovedEvidenceSource, ...] = (
    ApprovedEvidenceSource(
        source_id="binance_public_archive",
        role="primary",
        use_cases=("p4_label_coverage", "data_stability"),
        domains=("data.binance.vision",),
        asset_class="crypto",
        requires_api_key=False,
        egress_allowed=True,
        notes="Primary bulk OHLCV source for free crypto historical coverage.",
    ),
    ApprovedEvidenceSource(
        source_id="kraken_public_api",
        role="cross_check",
        use_cases=("simbroker_calibration", "data_stability"),
        domains=("api.kraken.com",),
        asset_class="crypto",
        requires_api_key=False,
        egress_allowed=True,
        notes="Public ticker/depth and short-window OHLC cross-check source.",
    ),
    ApprovedEvidenceSource(
        source_id="coinbase_exchange_public_api",
        role="cross_check",
        use_cases=("simbroker_calibration", "data_stability"),
        domains=("api.exchange.coinbase.com",),
        asset_class="crypto",
        requires_api_key=False,
        egress_allowed=True,
        notes="Public ticker and candle cross-check source.",
    ),
)

REJECTED_FREE_SOURCES: tuple[str, ...] = (
    "alpha_vantage_free",
    "stooq_equity_daily",
)


def get_approved_free_crypto_sources() -> tuple[ApprovedEvidenceSource, ...]:
    """Return the approved free crypto source set."""
    return APPROVED_FREE_CRYPTO_SOURCES


def get_source(source_id: str) -> ApprovedEvidenceSource:
    """Return an approved source by identifier."""
    for source in APPROVED_FREE_CRYPTO_SOURCES:
        if source.source_id == source_id:
            return source
    raise ValueError(f"source is not approved: {source_id}")


def validate_source_use(
    *,
    source_id: str,
    use_case: EvidenceUseCase,
    domain: str,
) -> ApprovedEvidenceSource:
    """Validate that a source/domain is approved for a specific evidence use case."""
    source = get_source(source_id)
    if not source.egress_allowed:
        raise ValueError(f"egress is not allowed for source: {source_id}")
    if use_case not in source.use_cases:
        raise ValueError(f"source {source_id} is not approved for {use_case}")
    if domain not in source.domains:
        raise ValueError(f"domain {domain} is not approved for source {source_id}")
    return source


def build_binance_monthly_klines_urls(
    *,
    symbol: str,
    interval: str,
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
) -> tuple[str, ...]:
    """Build deterministic monthly Binance public archive klines URLs."""
    _validate_binance_symbol(symbol)
    _validate_binance_interval(interval)
    start_index = start_year * 12 + start_month
    end_index = end_year * 12 + end_month
    if start_month < 1 or start_month > 12 or end_month < 1 or end_month > 12:
        raise ValueError("months must be in [1, 12]")
    if end_index < start_index:
        raise ValueError("end month must be after or equal to start month")
    urls: list[str] = []
    for month_index in range(start_index, end_index + 1):
        year = month_index // 12
        month = month_index % 12
        if month == 0:
            year -= 1
            month = 12
        urls.append(BinanceArchiveKlinesPath(symbol, interval, year, month).url)
    return tuple(urls)


def _validate_binance_symbol(symbol: str) -> None:
    if not symbol or not symbol.isalnum() or symbol.upper() != symbol:
        raise ValueError("Binance archive symbol must be uppercase alphanumeric")


def _validate_binance_interval(interval: str) -> None:
    allowed = {"1m", "5m", "15m", "1h", "4h", "1d"}
    if interval not in allowed:
        raise ValueError("unsupported Binance archive interval")


def source_ids(sources: Sequence[ApprovedEvidenceSource]) -> tuple[str, ...]:
    """Return deterministic source identifiers."""
    return tuple(source.source_id for source in sources)
