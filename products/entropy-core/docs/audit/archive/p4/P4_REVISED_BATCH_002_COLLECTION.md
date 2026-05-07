# P4 Revised Batch 002 Collection

Date: 2026-05-05
Status: COMPLETE_AS_COLLECTION

## Scope

Download the second resumable 20-file batch from
`P4-BINANCE-REVISED-SCALE-PLAN-v1`, record source hashes and terminal statuses,
and stop before conversion or gate claims.

## Result

| Field | Value |
|---|---|
| Collection ID | `P4-BINANCE-BATCH-COLLECT-v1` |
| Plan ID | `P4-BINANCE-REVISED-SCALE-PLAN-v1` |
| Plan hash | `f8902894d1b712c19784c7fd8b2ffb6dcaa52a34100b8e64815fe19a9692ee2f` |
| Batch index | 2 |
| Sequence range | 21-40 |
| Requested items | 20 |
| Done | 20 |
| Failed | 0 |
| First item | `BTCUSDT` 2021-09 |
| Last item | `BTCUSDT` 2023-04 |
| Gate claim allowed | `false` |

## Artifacts

| Artifact | Path |
|---|---|
| Batch manifest | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_002/P4_BATCH_002_MANIFEST.json` |
| Batch summary | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_002/P4_REVISED_BATCH_002_SUMMARY.md` |
| Source archives | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_002/` |

## Boundary

This is controlled batch collection only. It does not close P4 coverage, approve
Phase 0, start Phase 1, or make performance claims.

## Next Step

Start P0.7-015: Revised P4 BTCUSDT Batch 002 Conversion. Convert this second
revised batch and inspect the cumulative BTCUSDT coverage trajectory before
collecting more revised batches.
