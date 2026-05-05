# P4 Extended History Eligibility Probe

Date: 2026-05-05
Status: COMPLETE

## Scope

Probe approved Binance public archive monthly `1d` history depth without full
archive downloads. The goal is to determine whether the current Phase 0 crypto
universe can support 156 valid post-warmup P4 labels under `P4-RBL-v1`.

## Method

| Field | Value |
|---|---|
| Probe ID | `P4-BINANCE-HISTORY-PROBE-v1` |
| Source | `binance_public_archive` |
| Domain | `data.binance.vision` |
| Probe type | HTTP HEAD monthly zip availability |
| Interval | `1d` |
| Window | `2020-01` through `2025-12` |
| Required completed weeks | 312 |
| Warmup weeks | 155 |
| Required valid labeled weeks | 156 |
| Required eligible assets | 15 |
| Gate claim allowed | `false` |

## Current Universe Result

| Metric | Value |
|---|---|
| Universe ID | `PHASE0-CRYPTO-20-v1` |
| Universe hash | `6d4287839640086728536ab5b40f4592e924f1b22e18c6c1c8e3190bf7d4d4cd` |
| Eligible assets | 13/15 |
| Universe eligible | `false` |
| Manifest | `artifacts/evidence/p4_binance_scale/history_probe_2020_2025/P4_HISTORY_ELIGIBILITY_PROBE_MANIFEST.json` |
| Summary | `artifacts/evidence/p4_binance_scale/history_probe_2020_2025/P4_HISTORY_ELIGIBILITY_PROBE_SUMMARY.md` |

| Symbol | Eligible | Continuous Window | Est. Valid Labels | Reason |
|---|---|---|---:|---|
| BTCUSDT | true | 2020-01..2025-12 | 158 | pass |
| ETHUSDT | true | 2020-01..2025-12 | 158 | pass |
| BNBUSDT | true | 2020-01..2025-12 | 158 | pass |
| SOLUSDT | false | 2020-08..2025-12 | 127 | insufficient_continuous_history |
| XRPUSDT | true | 2020-01..2025-12 | 158 | pass |
| ADAUSDT | true | 2020-01..2025-12 | 158 | pass |
| DOGEUSDT | true | 2020-01..2025-12 | 158 | pass |
| TRXUSDT | true | 2020-01..2025-12 | 158 | pass |
| LINKUSDT | true | 2020-01..2025-12 | 158 | pass |
| AVAXUSDT | false | 2020-09..2025-12 | 123 | insufficient_continuous_history |
| LTCUSDT | true | 2020-01..2025-12 | 158 | pass |
| BCHUSDT | true | 2020-01..2025-12 | 158 | pass |
| DOTUSDT | false | 2020-08..2025-12 | 127 | insufficient_continuous_history |
| UNIUSDT | false | 2020-09..2025-12 | 123 | insufficient_continuous_history |
| AAVEUSDT | false | 2020-10..2025-12 | 119 | insufficient_continuous_history |
| NEARUSDT | false | 2020-10..2025-12 | 119 | insufficient_continuous_history |
| ATOMUSDT | true | 2020-01..2025-12 | 158 | pass |
| ETCUSDT | true | 2020-01..2025-12 | 158 | pass |
| FILUSDT | false | 2020-10..2025-12 | 119 | insufficient_continuous_history |
| ALGOUSDT | true | 2020-01..2025-12 | 158 | pass |

## Legacy Candidate Probe

Because the current universe has only 13 eligible assets, a small legacy-candidate
probe was run under the same source/window/method. This probe is not a universe
change by itself; it identifies candidates for a reviewed universe revision.

| Metric | Value |
|---|---|
| Candidate universe ID | `PHASE0-CRYPTO-LEGACY-CANDIDATES-v1` |
| Candidate universe hash | `c7e070f2f5ffaf54b05000838cd6cd6a742ad0ab310bf8e31eaab0408de4ed51` |
| Eligible candidates | 11/12 |
| Manifest | `artifacts/evidence/p4_binance_scale/history_probe_legacy_candidates_2020_2025/P4_HISTORY_ELIGIBILITY_PROBE_MANIFEST.json` |
| Summary | `artifacts/evidence/p4_binance_scale/history_probe_legacy_candidates_2020_2025/P4_LEGACY_CANDIDATE_HISTORY_PROBE_SUMMARY.md` |

| Symbol | Eligible | Continuous Window | Est. Valid Labels | Reason |
|---|---|---|---:|---|
| XLMUSDT | true | 2020-01..2025-12 | 158 | pass |
| EOSUSDT | false |  | 0 | insufficient_continuous_history |
| VETUSDT | true | 2020-01..2025-12 | 158 | pass |
| IOTAUSDT | true | 2020-01..2025-12 | 158 | pass |
| NEOUSDT | true | 2020-01..2025-12 | 158 | pass |
| QTUMUSDT | true | 2020-01..2025-12 | 158 | pass |
| ONTUSDT | true | 2020-01..2025-12 | 158 | pass |
| XTZUSDT | true | 2020-01..2025-12 | 158 | pass |
| ZECUSDT | true | 2020-01..2025-12 | 158 | pass |
| DASHUSDT | true | 2020-01..2025-12 | 158 | pass |
| THETAUSDT | true | 2020-01..2025-12 | 158 | pass |
| IOSTUSDT | true | 2020-01..2025-12 | 158 | pass |

## Finding

The current `PHASE0-CRYPTO-20-v1` universe cannot satisfy the encoded P4
coverage requirement because it has only 13 assets with enough continuous
history. The issue is universe composition, not source availability in general
and not the P4 labeler implementation.

The legacy-candidate probe found enough replacement candidates to preserve the
current P4 semantics. A universe revision can replace at least two late-listed
assets with eligible legacy symbols and restore the path to >=15 eligible assets.

## Boundary

This is source-history eligibility evidence only. It does not revise the
universe, close P4 coverage, approve Phase 0, start Phase 1, or make performance
claims.

## Next Step

Start P0.7-010: P4 Universe Revision Decision. The decision should select a
revised Phase 0 P4 universe or reject revision with rationale before any larger
download matrix is regenerated.
