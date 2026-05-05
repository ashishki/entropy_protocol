# P4 Batch 002 Collection

Date: 2026-05-05
Status: COMPLETE_AS_COLLECTION

## Scope

Download the second resumable batch from `P4-BINANCE-SCALE-PLAN-v1`, record
source hashes and terminal statuses, and stop before conversion or gate claims.

## Result

| Field | Value |
|---|---|
| Collection ID | `P4-BINANCE-BATCH-COLLECT-v1` |
| Plan ID | `P4-BINANCE-SCALE-PLAN-v1` |
| Plan hash | `0e6f1e9908a88372dd47c8792c7ea01d6a5a0a8c16382510a5bc6aa8b483d457` |
| Batch index | 2 |
| Sequence range | 21-40 |
| Requested items | 20 |
| Done | 20 |
| Failed | 0 |
| First item | `BTCUSDT` 2024-09 |
| Last item | `ETHUSDT` 2023-04 |
| Gate claim allowed | `false` |

## Artifacts

| Artifact | Path |
|---|---|
| Batch manifest | `artifacts/evidence/p4_binance_scale/batches/batch_002/P4_BATCH_002_MANIFEST.json` |
| Batch summary | `artifacts/evidence/p4_binance_scale/batches/batch_002/P4_BATCH_002_SUMMARY.md` |
| Source archives | `artifacts/evidence/p4_binance_scale/batches/batch_002/` |

## Collected Items

| Sequence | Symbol | Month | Status |
|---:|---|---|---|
| 21 | BTCUSDT | 2024-09 | DONE |
| 22 | BTCUSDT | 2024-10 | DONE |
| 23 | BTCUSDT | 2024-11 | DONE |
| 24 | BTCUSDT | 2024-12 | DONE |
| 25 | BTCUSDT | 2025-01 | DONE |
| 26 | BTCUSDT | 2025-02 | DONE |
| 27 | BTCUSDT | 2025-03 | DONE |
| 28 | BTCUSDT | 2025-04 | DONE |
| 29 | BTCUSDT | 2025-05 | DONE |
| 30 | BTCUSDT | 2025-06 | DONE |
| 31 | BTCUSDT | 2025-07 | DONE |
| 32 | BTCUSDT | 2025-08 | DONE |
| 33 | BTCUSDT | 2025-09 | DONE |
| 34 | BTCUSDT | 2025-10 | DONE |
| 35 | BTCUSDT | 2025-11 | DONE |
| 36 | BTCUSDT | 2025-12 | DONE |
| 37 | ETHUSDT | 2023-01 | DONE |
| 38 | ETHUSDT | 2023-02 | DONE |
| 39 | ETHUSDT | 2023-03 | DONE |
| 40 | ETHUSDT | 2023-04 | DONE |

## Boundary

This is controlled batch collection only. It does not close P4 coverage, approve
Phase 0, start Phase 1, or make performance claims.

## Next Step

Start P0.7-007: BTCUSDT Full-Window Conversion. Batch 002 completes the planned
BTCUSDT 2023-01 through 2025-12 source window across batch 001 and batch 002, so
the next control point is a full BTCUSDT dataset hash, quality report, and P4
output before collecting more assets.
