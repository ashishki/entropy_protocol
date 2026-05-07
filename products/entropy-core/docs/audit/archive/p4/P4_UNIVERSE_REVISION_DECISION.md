# P4 Universe Revision Decision

Date: 2026-05-05
Status: DECIDED
Decision ID: P4-UNIVERSE-001

## Decision

Create a revised Phase 0 P4 evidence universe:
`PHASE0-CRYPTO-P4-20-v2`.

The revised universe keeps all 13 current assets that passed the 2020-01 through
2025-12 history eligibility probe and replaces the 7 late-listed assets with the
first 7 eligible legacy candidates from the same probe process.

## Rationale

P0.7-009 showed:

- Current universe eligible assets: 13/15.
- Ineligible current assets: SOLUSDT, AVAXUSDT, DOTUSDT, UNIUSDT, AAVEUSDT,
  NEARUSDT, FILUSDT.
- Legacy candidate eligible assets: 11/12.

The P4 label semantics should remain unchanged. The problem is the current
evidence universe composition, not the source, parser, data-quality path, or
labeler.

## Revised Universe

| Field | Value |
|---|---|
| Universe ID | `PHASE0-CRYPTO-P4-20-v2` |
| Universe hash | `298fd0d4cb59dc7f94db12f61bc9cacb9915c59ba35a9be94f470f0e5b39f594` |
| Source selection ID | `FREE-CRYPTO-SOURCES-v1` |
| Snapshot | `products/entropy-core/docs/audit/P4_REVISED_CRYPTO_UNIVERSE_SNAPSHOT.md` |

| Rank | Symbol | Binance |
|---:|---|---|
| 1 | BTC | BTCUSDT |
| 2 | ETH | ETHUSDT |
| 3 | BNB | BNBUSDT |
| 4 | XRP | XRPUSDT |
| 5 | ADA | ADAUSDT |
| 6 | DOGE | DOGEUSDT |
| 7 | TRX | TRXUSDT |
| 8 | LINK | LINKUSDT |
| 9 | LTC | LTCUSDT |
| 10 | BCH | BCHUSDT |
| 11 | ATOM | ATOMUSDT |
| 12 | ETC | ETCUSDT |
| 13 | ALGO | ALGOUSDT |
| 14 | XLM | XLMUSDT |
| 15 | VET | VETUSDT |
| 16 | IOTA | IOTAUSDT |
| 17 | NEO | NEOUSDT |
| 18 | QTUM | QTUMUSDT |
| 19 | ONT | ONTUSDT |
| 20 | XTZ | XTZUSDT |

## Replacement Map

| Removed late-listed asset | Replacement candidate |
|---|---|
| SOLUSDT | XLMUSDT |
| AVAXUSDT | VETUSDT |
| DOTUSDT | IOTAUSDT |
| UNIUSDT | NEOUSDT |
| AAVEUSDT | QTUMUSDT |
| NEARUSDT | ONTUSDT |
| FILUSDT | XTZUSDT |

## Boundary

This decision revises only the Phase 0 P4 evidence universe. It does not revise
the broader research universe, close P4 coverage, approve Phase 0, start Phase
1, or make performance claims.

## Next Step

Start P0.7-011: Revised P4 Scale Plan. Regenerate the 2020-01 through 2025-12
download matrix for `PHASE0-CRYPTO-P4-20-v2` before collecting more archives.
