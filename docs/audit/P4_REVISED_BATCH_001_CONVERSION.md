# P4 Revised Batch 001 Conversion

Date: 2026-05-05
Status: COMPLETE_AS_PARTIAL_CONVERSION

## Scope

Convert the first revised BTCUSDT source batch into a partial local dataset,
compute dataset hash, run data-quality checks, and generate partial P4 output
before additional revised batches are collected.

## Inputs

| Field | Value |
|---|---|
| Collection ID | `P4-BINANCE-BATCH-COLLECT-v1` |
| Conversion ID | `P4-BINANCE-BATCH-CONVERT-v1` |
| Plan ID | `P4-BINANCE-REVISED-SCALE-PLAN-v1` |
| Plan hash | `f8902894d1b712c19784c7fd8b2ffb6dcaa52a34100b8e64815fe19a9692ee2f` |
| Batch manifest | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_001/P4_BATCH_001_MANIFEST.json` |
| Source files | 20 |
| Source range | `BTCUSDT` monthly `1d` archives, 2020-01 through 2021-08 |

## Output Artifacts

| Artifact | Path |
|---|---|
| Conversion manifest | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/batch_001/P4_BATCH_001_CONVERSION_MANIFEST.json` |
| Conversion summary | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/batch_001/P4_REVISED_BATCH_001_CONVERSION_SUMMARY.md` |
| Merged Parquet dataset | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/batch_001/datasets/BTCUSDT-1d-batch_001.parquet` |
| P4 coverage summary | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/batch_001/p4/P4_COVERAGE_SUMMARY.md` |
| P4 labels | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/batch_001/p4/labels/BTCUSDT_p4_labels.jsonl` |

## Conversion Result

| Metric | Value |
|---|---|
| Source bytes | 43858 |
| Combined source SHA-256 | `46208d6e821d093ba4bafe3fcfe2678e9f80b9f6f71e81f6ef82466a6aeaf81a` |
| Dataset hash | `e7e26e022c849317f5266333d3dd3a40570bf0e4e2919ee1850c55f3296af354` |
| Daily bars | 609 |
| First bar | `2020-01-01T00:00:00+00:00` |
| Last bar | `2021-08-31T00:00:00+00:00` |
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

This is partial revised-batch conversion only. It does not close P4 coverage,
approve Phase 0, start Phase 1, or make performance claims.

## Next Step

Start P0.7-014: Revised P4 Batch 002 Collection. Continue controlled BTCUSDT
collection under the revised plan before attempting full-window conversion.
