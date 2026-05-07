# P4 Revised Scale Plan

Date: 2026-05-05
Status: COMPLETE_AS_PLAN

## Scope

Regenerate the P4 download matrix for the revised Phase 0 P4 universe
`PHASE0-CRYPTO-P4-20-v2`, using the 2020-01 through 2025-12 window required by
the current `P4-RBL-v1` warmup and valid-label semantics.

## Plan Result

| Field | Value |
|---|---|
| Plan ID | `P4-BINANCE-REVISED-SCALE-PLAN-v1` |
| Plan hash | `f8902894d1b712c19784c7fd8b2ffb6dcaa52a34100b8e64815fe19a9692ee2f` |
| Universe ID | `PHASE0-CRYPTO-P4-20-v2` |
| Universe hash | `298fd0d4cb59dc7f94db12f61bc9cacb9915c59ba35a9be94f470f0e5b39f594` |
| Source selection ID | `FREE-CRYPTO-SOURCES-v1` |
| Interval | `1d` |
| Window | `2020-01` through `2025-12` |
| Asset count | 20 |
| Month count | 72 |
| Planned downloads | 1440 |
| Batch size | 20 |
| Required passing assets | 15 |
| Required valid labeled weeks | 156 |
| Gate claim allowed | `false` |

## Artifacts

| Artifact | Path |
|---|---|
| Revised scale plan | `products/entropy-core/docs/audit/P4_REVISED_COVERAGE_SCALE_PLAN.md` |
| Revised scale manifest | `products/entropy-core/docs/audit/P4_REVISED_COVERAGE_SCALE_MANIFEST.json` |
| Revised universe snapshot | `products/entropy-core/docs/audit/P4_REVISED_CRYPTO_UNIVERSE_SNAPSHOT.md` |

## First And Last Download Items

| Position | Sequence | Symbol | Month | URL |
|---|---:|---|---|---|
| First | 1 | BTCUSDT | 2020-01 | `https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1d/BTCUSDT-1d-2020-01.zip` |
| Last | 1440 | XTZUSDT | 2025-12 | `https://data.binance.vision/data/spot/monthly/klines/XTZUSDT/1d/XTZUSDT-1d-2025-12.zip` |

## Boundary

This is a deterministic collection plan only. It does not download archives,
close P4 coverage, approve Phase 0, start Phase 1, or make performance claims.

## Next Step

Start P0.7-012: Revised P4 Batch 001 Collection. Download only the first
resumable 20-file batch from the revised plan and record source hashes/statuses
before any broad collection.
