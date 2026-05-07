# SOURCE_MANIFEST_BOOTSTRAP
_Date: 2026-05-05 · Scope: P0.7-001 free crypto source manifest canary_

## Decision

Decision: `CANARY_PASS_SOURCE_MANIFEST_READY`.

The first no-budget crypto source manifest is ready for limited evidence
bootstrap. The canary checked only domains approved in
`FREE-CRYPTO-SOURCES-v1`.

## Source Manifest

| Source | Domain | Role | Canary | Notes |
|--------|--------|------|--------|-------|
| Binance public archive | `data.binance.vision` | Primary OHLCV archive | PASS | `BTCUSDT` 1d monthly archive returned HTTP 200 and `application/zip` |
| Kraken public API | `api.kraken.com` | Bid/ask and monitoring cross-check | PASS | Public `Ticker?pair=XBTUSD` returned bid/ask fields |
| Coinbase Exchange public API | `api.exchange.coinbase.com` | Bid/ask and candle cross-check | PASS | Public `products/BTC-USD/ticker` returned bid/ask fields |

## Crypto Universe Snapshot

| Field | Value |
|-------|-------|
| Universe ID | `PHASE0-CRYPTO-20-v1` |
| Universe hash | `6d4287839640086728536ab5b40f4592e924f1b22e18c6c1c8e3190bf7d4d4cd` |
| Snapshot file | `products/entropy-core/docs/audit/CRYPTO_UNIVERSE_SNAPSHOT.md` |
| Source selection | `FREE-CRYPTO-SOURCES-v1` |
| Calendar profile | `continuous` |
| Primary timeframe | `1d` |

## Canary Commands

```bash
curl -L -sS -I --max-time 15 \
  https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1d/BTCUSDT-1d-2024-01.zip
curl -sS --max-time 15 \
  'https://api.kraken.com/0/public/Ticker?pair=XBTUSD'
curl -sS --max-time 15 \
  'https://api.exchange.coinbase.com/products/BTC-USD/ticker'
```

## Boundary

This manifest does not close P4 coverage, SimBroker calibration, or 90-day
data-stability evidence. It only confirms that the approved free public source
paths are reachable for small bootstrap checks.

Next evidence work should collect a tiny, hash-recorded canary dataset before
attempting full 3-year P4 coverage or 90-day monitoring.
