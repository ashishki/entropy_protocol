# P4_FIRST_BATCH_COLLECTION
_Date: 2026-05-05 · Scope: P0.7-004 P4 first batch collection_

## Decision

Decision: `FIRST_BATCH_COLLECTED_NOT_GATE_EVIDENCE`.

The first resumable batch from `P4-BINANCE-SCALE-PLAN-v1` was downloaded from
the approved Binance public archive source. All 20 requested files completed and
each file has a recorded source SHA-256.

This is controlled collection only. It does not close P4 coverage, approve Phase
0, start Phase 1, or make OOS/performance claims.

## Batch Summary

| Field | Value |
|-------|-------|
| Collection ID | `P4-BINANCE-BATCH-COLLECT-v1` |
| Plan ID | `P4-BINANCE-SCALE-PLAN-v1` |
| Plan hash | `0e6f1e9908a88372dd47c8792c7ea01d6a5a0a8c16382510a5bc6aa8b483d457` |
| Batch index | 1 |
| Requested items | 20 |
| Done | 20 |
| Failed | 0 |
| Gate claim allowed | `false` |

## Artifact Paths

| Artifact | Path |
|----------|------|
| Batch manifest | `artifacts/evidence/p4_binance_scale/batches/batch_001/P4_BATCH_001_MANIFEST.json` |
| Batch summary | `artifacts/evidence/p4_binance_scale/batches/batch_001/P4_BATCH_001_SUMMARY.md` |
| Download directory | `artifacts/evidence/p4_binance_scale/batches/batch_001/BTCUSDT/` |

## Collected Range

| Symbol | First month | Last month | Files |
|--------|-------------|------------|-------|
| `BTCUSDT` | 2023-01 | 2024-08 | 20 |

## Boundary

The next step must convert this batch into a merged BTCUSDT local dataset,
compute dataset hash, run data-quality checks, and generate partial P4 output.
Do not continue downloading later batches until the first-batch conversion path
is verified.
