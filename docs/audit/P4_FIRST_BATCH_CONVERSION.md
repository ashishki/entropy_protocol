# P4 First Batch Conversion

Date: 2026-05-05
Status: COMPLETE_AS_PARTIAL_CONVERSION

## Scope

Convert the first collected BTCUSDT Binance public archive batch into a merged
local dataset, compute dataset hash, run data-quality checks, and generate
partial P4 output before downloading additional batches.

## Inputs

| Field | Value |
|---|---|
| Collection ID | `P4-BINANCE-BATCH-COLLECT-v1` |
| Conversion ID | `P4-BINANCE-BATCH-CONVERT-v1` |
| Plan ID | `P4-BINANCE-SCALE-PLAN-v1` |
| Plan hash | `0e6f1e9908a88372dd47c8792c7ea01d6a5a0a8c16382510a5bc6aa8b483d457` |
| Batch manifest | `artifacts/evidence/p4_binance_scale/batches/batch_001/P4_BATCH_001_MANIFEST.json` |
| Source files | 20 |
| Source range | `BTCUSDT` monthly `1d` archives, 2023-01 through 2024-08 |

## Output Artifacts

| Artifact | Path |
|---|---|
| Conversion manifest | `artifacts/evidence/p4_binance_scale/conversions/batch_001/P4_BATCH_001_CONVERSION_MANIFEST.json` |
| Conversion summary | `artifacts/evidence/p4_binance_scale/conversions/batch_001/P4_BATCH_001_CONVERSION_SUMMARY.md` |
| Merged Parquet dataset | `artifacts/evidence/p4_binance_scale/conversions/batch_001/datasets/BTCUSDT-1d-batch_001.parquet` |
| P4 coverage summary | `artifacts/evidence/p4_binance_scale/conversions/batch_001/p4/P4_COVERAGE_SUMMARY.md` |
| P4 labels | `artifacts/evidence/p4_binance_scale/conversions/batch_001/p4/labels/BTCUSDT_p4_labels.jsonl` |

## Conversion Result

| Metric | Value |
|---|---|
| Source bytes | 43048 |
| Combined source SHA-256 | `2d82fba724e6c46b8595a872d14cbfafadcf059e63d97c2eac8ac6b26b9beb4f` |
| Dataset hash | `75dfbf9a9a41c2a374220da43cf12930a9c663f17a4aef2523944cc742744c65` |
| Daily bars | 609 |
| First bar | `2023-01-01T00:00:00+00:00` |
| Last bar | `2024-08-31T00:00:00+00:00` |
| Data quality status | `PASS` |
| P4 generated labels | 86 |
| P4 valid labeled weeks | 0 |
| P4 reason | `insufficient_labeled_weeks` |
| P4 gate evidence complete | `false` |
| Gate claim allowed | `false` |

## Data Quality Checks

| Check | Status | Affected Bars | Message |
|---|---|---:|---|
| timestamps | PASS | 0 |  |
| gaps | PASS | 0 |  |
| ohlcv_sanity | PASS | 0 |  |

## Boundary

This is partial first-batch conversion only. It does not close P4 coverage,
approve Phase 0, start Phase 1, or make performance claims.

## Next Step

Continue controlled collection with P0.7-006: P4 Batch 002 Collection. The goal
is to extend BTCUSDT through 2025-12 and begin the next planned asset without
changing source approvals or gate status.
