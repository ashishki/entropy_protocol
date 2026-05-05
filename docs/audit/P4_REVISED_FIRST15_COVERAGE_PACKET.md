# P4 Revised First 15 Coverage Packet

Date: 2026-05-05
Status: COVERAGE_PACKET_CANDIDATE_COMPLETE

## Scope

Build the revised P4 evidence candidate for the first 15 assets in
`PHASE0-CRYPTO-P4-20-v2` using approved Binance public archive data for
2020-01 through 2025-12.

This packet consolidates revised batch collection, full-window symbol
conversion, data-quality checks, dataset hashes, and aggregate P4 label coverage.

## Inputs

| Field | Value |
|---|---|
| Packet ID | `P4-REVISED-FIRST15-COVERAGE-v1` |
| Plan ID | `P4-BINANCE-REVISED-SCALE-PLAN-v1` |
| Plan hash | `f8902894d1b712c19784c7fd8b2ffb6dcaa52a34100b8e64815fe19a9692ee2f` |
| Universe ID | `PHASE0-CRYPTO-P4-20-v2` |
| Universe hash | `298fd0d4cb59dc7f94db12f61bc9cacb9915c59ba35a9be94f470f0e5b39f594` |
| Source selection ID | `FREE-CRYPTO-SOURCES-v1` |
| Source domain | `data.binance.vision` |
| Window | `2020-01` through `2025-12` |
| Batch range | `001-054` |
| Sequence range | `1-1080` |
| Symbols | 15 |

## Artifacts

| Artifact | Path |
|---|---|
| Coverage manifest | `artifacts/evidence/p4_binance_scale/revised_v2/coverage/first_15_assets_2020_2025/P4_REVISED_FIRST15_COVERAGE_MANIFEST.json` |
| Coverage summary | `artifacts/evidence/p4_binance_scale/revised_v2/coverage/first_15_assets_2020_2025/P4_REVISED_FIRST15_COVERAGE_SUMMARY.md` |
| P4 aggregate summary | `artifacts/evidence/p4_binance_scale/revised_v2/coverage/first_15_assets_2020_2025/p4/P4_COVERAGE_SUMMARY.md` |
| P4 label artifacts | `artifacts/evidence/p4_binance_scale/revised_v2/coverage/first_15_assets_2020_2025/p4/labels/` |
| Full-window symbol datasets | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/full_windows/` |
| Source batches | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_001/` through `batch_054/` |

## Coverage Result

| Metric | Value |
|---|---|
| Passing assets | 15/15 |
| Required passing assets | 15 |
| Required valid labeled weeks | 156 |
| Actual valid labeled weeks per asset | 157 |
| Daily bars per asset | 2192 |
| Data quality status | `PASS` for all 15 assets |
| Gate evidence complete | `true` |
| Gate claim allowed | `false` |

## Asset Rows

| Symbol | Quality | Daily Bars | Dataset Hash | Valid Labels | Pass |
|---|---|---:|---|---:|---|
| BTCUSDT | PASS | 2192 | `6b0bfb2c1a8520e08b917db2b9d16172eaae7a5da2f85cbb7afa54054b674530` | 157 | true |
| ETHUSDT | PASS | 2192 | `8c2eb38ed7d16896249bd281ec3fca5adc34571d6c79c711b4236669c3cd7866` | 157 | true |
| BNBUSDT | PASS | 2192 | `f4ee9a9067508fd64190fbdac106e7a33d70791864c76d554506606305e406b1` | 157 | true |
| XRPUSDT | PASS | 2192 | `3711ddf233a5e481b88465774ea6f4f3960656b1afe4b43006e0176f19f92de6` | 157 | true |
| ADAUSDT | PASS | 2192 | `dad613a083896dfb9d5434fcfa0cf810b686b279673cebc45df42acfab6c899f` | 157 | true |
| DOGEUSDT | PASS | 2192 | `81aa076e9f2e3c84f0368b2c60da24fd73267c20c1d8e96a51bd2140af679a2f` | 157 | true |
| TRXUSDT | PASS | 2192 | `bf46799256617a79f4d4bbb269b2720319c2955a0b8e07ae10d010dfd0ae32d5` | 157 | true |
| LINKUSDT | PASS | 2192 | `08b1206a2a867df52b57f4929fd5821e936d28add80c3d9551ac3617a19ed5eb` | 157 | true |
| LTCUSDT | PASS | 2192 | `c4c24245a9eb7d2737b113e49e6dbd0d0e3a3b88cfe6ec7b7b68ff647bef58fb` | 157 | true |
| BCHUSDT | PASS | 2192 | `5043398211f91e6d6a4873eacd9dea80e00cfb8d7d3b02d275d29ed1c24cd1dd` | 157 | true |
| ATOMUSDT | PASS | 2192 | `b532daf6ffb33505574549843667bf2451a3cfb6abf1e16ac2ae94f9998abb13` | 157 | true |
| ETCUSDT | PASS | 2192 | `c9fcd30d4cd7ce492eaaeb7d167b400d06825ae4ece64b97fae91040b74c7c5c` | 157 | true |
| ALGOUSDT | PASS | 2192 | `c2d5b35fb15d6561cb5d0730782736407b2df7ee5ccbd6826bc6e434c7331fb9` | 157 | true |
| XLMUSDT | PASS | 2192 | `2300f9e83cd453cd11054a7331ef5b448f93a72943c7e31b41be15a6e5850cdb` | 157 | true |
| VETUSDT | PASS | 2192 | `4f868cdc62c7ab631ec11db5c68fb15ee0fb95c02ea44126bcf873d45d02f9bc` | 157 | true |

## Boundary

This is a P4 coverage packet candidate. It does not approve Phase 0, start Phase
1, authorize live capital, or make performance claims. Human review is still
required before the Phase 0 gate packet can treat this as accepted P4 evidence.

## Next Step

Start P0.7-016: P4 Coverage Packet Review. Review the generated labels,
manifests, hashes, and source boundaries before marking the P4 blocker as
closed in the Phase 0 gate packet.
