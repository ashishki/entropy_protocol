# P4 Revised Batch 001 Collection

Date: 2026-05-05
Status: COMPLETE_AS_COLLECTION

## Scope

Download the first resumable 20-file batch from
`P4-BINANCE-REVISED-SCALE-PLAN-v1`, record source hashes and terminal statuses,
and stop before conversion or gate claims.

## Result

| Field | Value |
|---|---|
| Collection ID | `P4-BINANCE-BATCH-COLLECT-v1` |
| Plan ID | `P4-BINANCE-REVISED-SCALE-PLAN-v1` |
| Plan hash | `f8902894d1b712c19784c7fd8b2ffb6dcaa52a34100b8e64815fe19a9692ee2f` |
| Batch index | 1 |
| Sequence range | 1-20 |
| Requested items | 20 |
| Done | 20 |
| Failed | 0 |
| First item | `BTCUSDT` 2020-01 |
| Last item | `BTCUSDT` 2021-08 |
| Gate claim allowed | `false` |

## Artifacts

| Artifact | Path |
|---|---|
| Batch manifest | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_001/P4_BATCH_001_MANIFEST.json` |
| Batch summary | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_001/P4_REVISED_BATCH_001_SUMMARY.md` |
| Source archives | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_001/` |

## Collected Items

| Sequence | Symbol | Month | Status |
|---:|---|---|---|
| 1 | BTCUSDT | 2020-01 | DONE |
| 2 | BTCUSDT | 2020-02 | DONE |
| 3 | BTCUSDT | 2020-03 | DONE |
| 4 | BTCUSDT | 2020-04 | DONE |
| 5 | BTCUSDT | 2020-05 | DONE |
| 6 | BTCUSDT | 2020-06 | DONE |
| 7 | BTCUSDT | 2020-07 | DONE |
| 8 | BTCUSDT | 2020-08 | DONE |
| 9 | BTCUSDT | 2020-09 | DONE |
| 10 | BTCUSDT | 2020-10 | DONE |
| 11 | BTCUSDT | 2020-11 | DONE |
| 12 | BTCUSDT | 2020-12 | DONE |
| 13 | BTCUSDT | 2021-01 | DONE |
| 14 | BTCUSDT | 2021-02 | DONE |
| 15 | BTCUSDT | 2021-03 | DONE |
| 16 | BTCUSDT | 2021-04 | DONE |
| 17 | BTCUSDT | 2021-05 | DONE |
| 18 | BTCUSDT | 2021-06 | DONE |
| 19 | BTCUSDT | 2021-07 | DONE |
| 20 | BTCUSDT | 2021-08 | DONE |

## Boundary

This is controlled batch collection only. It does not close P4 coverage, approve
Phase 0, start Phase 1, or make performance claims.

## Next Step

Start P0.7-013: Revised P4 BTCUSDT Batch 001 Conversion. Convert only this first
revised batch into a partial BTCUSDT dataset and quality/P4 output before
additional revised batches are collected.
