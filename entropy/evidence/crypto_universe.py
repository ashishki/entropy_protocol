"""Phase 0 crypto universe snapshot helpers."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

CRYPTO_UNIVERSE_ID = "PHASE0-CRYPTO-20-v1"
P4_REVISED_CRYPTO_UNIVERSE_ID = "PHASE0-CRYPTO-P4-20-v2"


@dataclass(frozen=True)
class CryptoUniverseAsset:
    """One asset in the Phase 0 free-source crypto universe."""

    rank: int
    symbol: str
    base_asset: str
    quote_asset: str
    binance_symbol: str
    calendar_profile: str = "continuous"
    kraken_pair: str | None = None
    coinbase_product: str | None = None


@dataclass(frozen=True)
class CryptoUniverseSnapshot:
    """Deterministic crypto target universe snapshot."""

    universe_id: str
    source_selection_id: str
    assets: tuple[CryptoUniverseAsset, ...]
    rationale: str

    @property
    def universe_hash(self) -> str:
        payload = json.dumps(
            {
                "universe_id": self.universe_id,
                "source_selection_id": self.source_selection_id,
                "assets": [asdict(asset) for asset in self.assets],
                "rationale": self.rationale,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


DEFAULT_PHASE0_CRYPTO_UNIVERSE = CryptoUniverseSnapshot(
    universe_id=CRYPTO_UNIVERSE_ID,
    source_selection_id="FREE-CRYPTO-SOURCES-v1",
    rationale=(
        "Liquid crypto majors selected for no-budget Phase 0 evidence bootstrap "
        "using Binance public archive primary data and Kraken/Coinbase public "
        "cross-checks where available."
    ),
    assets=(
        CryptoUniverseAsset(
            1, "BTC", "BTC", "USDT", "BTCUSDT", kraken_pair="XBT/USD", coinbase_product="BTC-USD"
        ),
        CryptoUniverseAsset(
            2, "ETH", "ETH", "USDT", "ETHUSDT", kraken_pair="ETH/USD", coinbase_product="ETH-USD"
        ),
        CryptoUniverseAsset(3, "BNB", "BNB", "USDT", "BNBUSDT"),
        CryptoUniverseAsset(
            4, "SOL", "SOL", "USDT", "SOLUSDT", kraken_pair="SOL/USD", coinbase_product="SOL-USD"
        ),
        CryptoUniverseAsset(
            5, "XRP", "XRP", "USDT", "XRPUSDT", kraken_pair="XRP/USD", coinbase_product="XRP-USD"
        ),
        CryptoUniverseAsset(
            6, "ADA", "ADA", "USDT", "ADAUSDT", kraken_pair="ADA/USD", coinbase_product="ADA-USD"
        ),
        CryptoUniverseAsset(
            7,
            "DOGE",
            "DOGE",
            "USDT",
            "DOGEUSDT",
            kraken_pair="DOGE/USD",
            coinbase_product="DOGE-USD",
        ),
        CryptoUniverseAsset(8, "TRX", "TRX", "USDT", "TRXUSDT", kraken_pair="TRX/USD"),
        CryptoUniverseAsset(
            9,
            "LINK",
            "LINK",
            "USDT",
            "LINKUSDT",
            kraken_pair="LINK/USD",
            coinbase_product="LINK-USD",
        ),
        CryptoUniverseAsset(
            10,
            "AVAX",
            "AVAX",
            "USDT",
            "AVAXUSDT",
            kraken_pair="AVAX/USD",
            coinbase_product="AVAX-USD",
        ),
        CryptoUniverseAsset(
            11, "LTC", "LTC", "USDT", "LTCUSDT", kraken_pair="LTC/USD", coinbase_product="LTC-USD"
        ),
        CryptoUniverseAsset(
            12, "BCH", "BCH", "USDT", "BCHUSDT", kraken_pair="BCH/USD", coinbase_product="BCH-USD"
        ),
        CryptoUniverseAsset(
            13, "DOT", "DOT", "USDT", "DOTUSDT", kraken_pair="DOT/USD", coinbase_product="DOT-USD"
        ),
        CryptoUniverseAsset(
            14, "UNI", "UNI", "USDT", "UNIUSDT", kraken_pair="UNI/USD", coinbase_product="UNI-USD"
        ),
        CryptoUniverseAsset(
            15,
            "AAVE",
            "AAVE",
            "USDT",
            "AAVEUSDT",
            kraken_pair="AAVE/USD",
            coinbase_product="AAVE-USD",
        ),
        CryptoUniverseAsset(
            16,
            "NEAR",
            "NEAR",
            "USDT",
            "NEARUSDT",
            kraken_pair="NEAR/USD",
            coinbase_product="NEAR-USD",
        ),
        CryptoUniverseAsset(
            17,
            "ATOM",
            "ATOM",
            "USDT",
            "ATOMUSDT",
            kraken_pair="ATOM/USD",
            coinbase_product="ATOM-USD",
        ),
        CryptoUniverseAsset(
            18, "ETC", "ETC", "USDT", "ETCUSDT", kraken_pair="ETC/USD", coinbase_product="ETC-USD"
        ),
        CryptoUniverseAsset(
            19, "FIL", "FIL", "USDT", "FILUSDT", kraken_pair="FIL/USD", coinbase_product="FIL-USD"
        ),
        CryptoUniverseAsset(
            20,
            "ALGO",
            "ALGO",
            "USDT",
            "ALGOUSDT",
            kraken_pair="ALGO/USD",
            coinbase_product="ALGO-USD",
        ),
    ),
)

DEFAULT_PHASE0_P4_CRYPTO_UNIVERSE = CryptoUniverseSnapshot(
    universe_id=P4_REVISED_CRYPTO_UNIVERSE_ID,
    source_selection_id="FREE-CRYPTO-SOURCES-v1",
    rationale=(
        "Phase 0 P4 evidence universe revised after `P4-BINANCE-HISTORY-PROBE-v1`: "
        "retain current assets with continuous 2020-01 through 2025-12 Binance "
        "history and replace late-listed assets with eligible legacy candidates. "
        "This preserves P4 label semantics and supports >=15 eligible assets."
    ),
    assets=(
        CryptoUniverseAsset(
            1, "BTC", "BTC", "USDT", "BTCUSDT", kraken_pair="XBT/USD", coinbase_product="BTC-USD"
        ),
        CryptoUniverseAsset(
            2, "ETH", "ETH", "USDT", "ETHUSDT", kraken_pair="ETH/USD", coinbase_product="ETH-USD"
        ),
        CryptoUniverseAsset(3, "BNB", "BNB", "USDT", "BNBUSDT"),
        CryptoUniverseAsset(
            4, "XRP", "XRP", "USDT", "XRPUSDT", kraken_pair="XRP/USD", coinbase_product="XRP-USD"
        ),
        CryptoUniverseAsset(
            5, "ADA", "ADA", "USDT", "ADAUSDT", kraken_pair="ADA/USD", coinbase_product="ADA-USD"
        ),
        CryptoUniverseAsset(
            6,
            "DOGE",
            "DOGE",
            "USDT",
            "DOGEUSDT",
            kraken_pair="DOGE/USD",
            coinbase_product="DOGE-USD",
        ),
        CryptoUniverseAsset(7, "TRX", "TRX", "USDT", "TRXUSDT", kraken_pair="TRX/USD"),
        CryptoUniverseAsset(
            8,
            "LINK",
            "LINK",
            "USDT",
            "LINKUSDT",
            kraken_pair="LINK/USD",
            coinbase_product="LINK-USD",
        ),
        CryptoUniverseAsset(
            9, "LTC", "LTC", "USDT", "LTCUSDT", kraken_pair="LTC/USD", coinbase_product="LTC-USD"
        ),
        CryptoUniverseAsset(
            10, "BCH", "BCH", "USDT", "BCHUSDT", kraken_pair="BCH/USD", coinbase_product="BCH-USD"
        ),
        CryptoUniverseAsset(
            11,
            "ATOM",
            "ATOM",
            "USDT",
            "ATOMUSDT",
            kraken_pair="ATOM/USD",
            coinbase_product="ATOM-USD",
        ),
        CryptoUniverseAsset(
            12, "ETC", "ETC", "USDT", "ETCUSDT", kraken_pair="ETC/USD", coinbase_product="ETC-USD"
        ),
        CryptoUniverseAsset(
            13,
            "ALGO",
            "ALGO",
            "USDT",
            "ALGOUSDT",
            kraken_pair="ALGO/USD",
            coinbase_product="ALGO-USD",
        ),
        CryptoUniverseAsset(
            14,
            "XLM",
            "XLM",
            "USDT",
            "XLMUSDT",
            kraken_pair="XLM/USD",
            coinbase_product="XLM-USD",
        ),
        CryptoUniverseAsset(15, "VET", "VET", "USDT", "VETUSDT"),
        CryptoUniverseAsset(16, "IOTA", "IOTA", "USDT", "IOTAUSDT"),
        CryptoUniverseAsset(17, "NEO", "NEO", "USDT", "NEOUSDT"),
        CryptoUniverseAsset(18, "QTUM", "QTUM", "USDT", "QTUMUSDT"),
        CryptoUniverseAsset(19, "ONT", "ONT", "USDT", "ONTUSDT"),
        CryptoUniverseAsset(
            20,
            "XTZ",
            "XTZ",
            "USDT",
            "XTZUSDT",
            kraken_pair="XTZ/USD",
            coinbase_product="XTZ-USD",
        ),
    ),
)


def get_default_phase0_crypto_universe() -> CryptoUniverseSnapshot:
    """Return the default Phase 0 crypto universe snapshot."""
    return DEFAULT_PHASE0_CRYPTO_UNIVERSE


def get_default_phase0_p4_crypto_universe() -> CryptoUniverseSnapshot:
    """Return the revised Phase 0 P4 evidence universe snapshot."""
    return DEFAULT_PHASE0_P4_CRYPTO_UNIVERSE


def render_crypto_universe_snapshot(snapshot: CryptoUniverseSnapshot) -> str:
    """Render a deterministic Markdown crypto universe snapshot."""
    lines = [
        "# CRYPTO_UNIVERSE_SNAPSHOT",
        "",
        f"Universe ID: `{snapshot.universe_id}`",
        f"Source selection ID: `{snapshot.source_selection_id}`",
        f"Universe hash: `{snapshot.universe_hash}`",
        "",
        snapshot.rationale,
        "",
        "| Rank | Symbol | Binance | Kraken | Coinbase | Calendar |",
        "|------|--------|---------|--------|----------|----------|",
    ]
    for asset in snapshot.assets:
        lines.append(
            "| "
            f"{asset.rank} | "
            f"{asset.symbol} | "
            f"{asset.binance_symbol} | "
            f"{asset.kraken_pair or ''} | "
            f"{asset.coinbase_product or ''} | "
            f"{asset.calendar_profile} |"
        )
    lines.extend(
        [
            "",
            "Boundary: this universe is for free-source evidence bootstrap only. "
            "It does not approve Phase 0, start Phase 1, or make performance claims.",
        ]
    )
    return "\n".join(lines)
