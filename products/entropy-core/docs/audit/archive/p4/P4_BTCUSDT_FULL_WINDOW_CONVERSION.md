# P4 BTCUSDT Full-Window Conversion

Date: 2026-05-05
Status: COMPLETE_AS_SYMBOL_WINDOW_CONVERSION

## Scope

Merge BTCUSDT source archives across batch 001 and batch 002 into the full
planned 2023-01 through 2025-12 local dataset, compute dataset hash, run
data-quality checks, and generate BTCUSDT full-window P4 output.

## Inputs

| Field | Value |
|---|---|
| Conversion ID | `P4-BINANCE-SYMBOL-CONVERT-v1` |
| Plan ID | `P4-BINANCE-SCALE-PLAN-v1` |
| Plan hash | `0e6f1e9908a88372dd47c8792c7ea01d6a5a0a8c16382510a5bc6aa8b483d457` |
| Symbol | `BTCUSDT` |
| Interval | `1d` |
| Source manifests | 2 |
| Source sequences | 1-36 |
| Source months | `2023-01` through `2025-12` |
| Source files | 36 |

## Output Artifacts

| Artifact | Path |
|---|---|
| Symbol conversion manifest | `artifacts/evidence/p4_binance_scale/conversions/full_windows/BTCUSDT_1d_2023_01_2025_12/BTCUSDT_1d_SYMBOL_CONVERSION_MANIFEST.json` |
| Symbol conversion summary | `artifacts/evidence/p4_binance_scale/conversions/full_windows/BTCUSDT_1d_2023_01_2025_12/BTCUSDT_1d_SYMBOL_CONVERSION_SUMMARY.md` |
| Merged Parquet dataset | `artifacts/evidence/p4_binance_scale/conversions/full_windows/BTCUSDT_1d_2023_01_2025_12/datasets/BTCUSDT-1d-2023_01-2025_12.parquet` |
| P4 coverage summary | `artifacts/evidence/p4_binance_scale/conversions/full_windows/BTCUSDT_1d_2023_01_2025_12/p4/P4_COVERAGE_SUMMARY.md` |
| P4 labels | `artifacts/evidence/p4_binance_scale/conversions/full_windows/BTCUSDT_1d_2023_01_2025_12/p4/labels/BTCUSDT_p4_labels.jsonl` |

## Conversion Result

| Metric | Value |
|---|---|
| Source bytes | 78162 |
| Combined source SHA-256 | `51f03cd8807fafcf611a9757dd93b71c48e9235f9568c7ce9834051d8b5a4a16` |
| Dataset hash | `15dd83aa0222f764247f535fbd5ac1c8c67cdd50770870f5fc9aa66dac0f4592` |
| Daily bars | 1096 |
| First bar | `2023-01-01T00:00:00+00:00` |
| Last bar | `2025-12-31T00:00:00+00:00` |
| Data quality status | `PASS` |
| P4 generated labels | 156 |
| P4 valid labeled weeks | 1 |
| P4 reason | `insufficient_labeled_weeks` |
| P4 gate evidence complete | `false` |
| Gate claim allowed | `false` |

## Data Quality Checks

| Check | Status | Affected Bars | Message |
|---|---|---:|---|
| timestamps | PASS | 0 |  |
| gaps | PASS | 0 |  |
| ohlcv_sanity | PASS | 0 |  |

## Strategic Finding

The 2023-01 through 2025-12 source window is clean and reproducible, but it does
not produce enough post-warmup P4 labels under the current `P4-RBL-v1` semantics.
The labeler emits 156 completed weekly labels and only the final week is
post-warmup, leaving 1 valid labeled week against the current requirement of 156.

This means the current 3-year/20-asset scale plan cannot close the P4 gate as
currently encoded. Continuing to collect the remaining 2023-2025 assets would
likely reproduce the same insufficiency across assets.

## Boundary

This is symbol-window conversion evidence only. It does not close P4 coverage,
approve Phase 0, start Phase 1, or make performance claims.

## Next Step

Start P0.7-008: P4 Coverage Window Strategy Decision. The decision must choose
whether to expand the source window enough to satisfy 156 post-warmup labels,
revise the acceptance metric wording, or record a charter-level change request
before more broad collection.
