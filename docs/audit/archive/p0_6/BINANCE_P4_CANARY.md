# BINANCE_P4_CANARY
_Date: 2026-05-05 · Scope: P0.7-002 Binance P4 canary dataset_

## Decision

Decision: `CANARY_PASS_NOT_GATE_EVIDENCE`.

The approved Binance public archive source can be downloaded, hashed, converted
to local Parquet, checked with data-quality tooling, and passed through P4 label
artifact generation. This canary does not close P4 coverage because it covers
only one month of one asset.

## Canary Input

| Field | Value |
|-------|-------|
| Canary ID | `BINANCE-P4-CANARY-v1` |
| Source URL | `https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1d/BTCUSDT-1d-2024-01.zip` |
| Source SHA-256 | `474c1ce6fbb09e42cfc7231fee249aecc58af2fb5918570ffeba37998926b4a4` |
| Symbol | `BTCUSDT` |
| Interval | `1d` |
| Calendar profile | `continuous` |
| Daily bars | 31 |
| Dataset hash | `042b0b99abc857e59f4a165d66bb3a7e56abaeb9de7b08c4b224b6f1c3bb3770` |
| Data quality status | `PASS` |

## Artifact Paths

| Artifact | Path |
|----------|------|
| Raw source zip | `artifacts/evidence/binance_p4_canary/BTCUSDT_1d_2024_01/BTCUSDT-1d-2024-01.zip` |
| Local Parquet dataset | `artifacts/evidence/binance_p4_canary/BTCUSDT_1d_2024_01/BTCUSDT-1d-2024-01.parquet` |
| Canary manifest | `artifacts/evidence/binance_p4_canary/BTCUSDT_1d_2024_01/BINANCE_P4_CANARY_MANIFEST.json` |
| Canary summary | `artifacts/evidence/binance_p4_canary/BTCUSDT_1d_2024_01/BINANCE_P4_CANARY_SUMMARY.md` |
| P4 coverage summary | `artifacts/evidence/binance_p4_canary/BTCUSDT_1d_2024_01/p4/P4_COVERAGE_SUMMARY.md` |
| P4 labels JSONL | `artifacts/evidence/binance_p4_canary/BTCUSDT_1d_2024_01/p4/labels/BTCUSDT_p4_labels.jsonl` |

## P4 Result

| Metric | Value |
|--------|-------|
| Generated weekly labels | 4 |
| Valid labeled weeks after warmup | 0 |
| Required valid labeled weeks | 156 |
| P4 gate evidence complete | `false` |
| Reason | `insufficient_labeled_weeks` |

## Boundary

This is canary evidence only. It does not close P4 coverage, approve Phase 0,
start Phase 1, or make OOS/performance claims. The next step is scaled coverage
planning across `PHASE0-CRYPTO-20-v1`, with artifact size controls and
intermediate manifests before any full gate packet.
