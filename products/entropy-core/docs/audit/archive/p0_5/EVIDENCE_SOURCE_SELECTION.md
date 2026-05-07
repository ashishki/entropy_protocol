# EVIDENCE_SOURCE_SELECTION
_Date: 2026-05-05 · Scope: free no-budget source selection_

## Decision

Decision: `FREE_CRYPTO_FIRST`.

Use free crypto exchange-origin data for the first evidence bootstrap:

1. Binance public archive as the primary OHLCV source.
2. Kraken public API as a bid/ask and short-window monitoring cross-check.
3. Coinbase Exchange public API as a second bid/ask and candle cross-check.

This choice is encoded in `entropy/evidence/source_selection.py` as
`FREE-CRYPTO-SOURCES-v1`.

## Rationale

The immediate Phase 0 evidence gaps need OHLCV history, bid/ask calibration, and
feed monitoring. Free equity sources are weaker for this purpose because reliable
US equity bid/ask data is licensing-sensitive and free tiers are too constrained
for multi-asset evidence collection.

Crypto exchange-origin public data is the best no-budget bootstrap because it
offers:

- continuous calendar profile;
- free historical OHLCV archive for P4 and stability bootstrap;
- public bid/ask endpoints for prospective SimBroker calibration snapshots;
- no API key requirement for the selected first sources;
- enough liquidity in major pairs to build representative early evidence.

## Approved First Universe Class

Asset class: `crypto`.

Calendar profile: `continuous`.

Initial target universe should use liquid USD/USDT majors only. The concrete
20-asset universe snapshot remains pending and must be hash-recorded before
full gate evidence generation.

## Rejected Alternatives For First Bootstrap

| Source | Decision | Reason |
|--------|----------|--------|
| Alpha Vantage free | Rejected for first bootstrap | Free request limits are too tight and free US equity bid/ask evidence is not suitable for SimBroker calibration |
| Stooq daily equities | Rejected for first bootstrap | Useful for exploratory EOD OHLCV but not for bid/ask calibration or 90-day feed evidence |
| Yahoo/unofficial wrappers | Rejected | Not stable enough for protocol evidence and licensing/terms are less clean |

## Boundary

This is not a Phase 0 gate pass. It authorizes only limited public-source
bootstrap work. Final evidence still needs source manifests, dataset hashes,
manual review, and packet acceptance.
