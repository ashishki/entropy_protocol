# Phase 1A Archive Freeze Packet

Date: 2026-05-05
Task: P1A-002
Status: `COMPLETE`
Freeze ID: `PHASE1A-ARCHIVE-FREEZE-v1`

## Decision

P1A-002 is approved as the machine-readable archive dataset freeze for the
initial Phase 1A archive-only baseline planning surface.

The freeze converts the P1A-001 entry contract into deterministic artifacts
that enumerate the only admissible initial datasets, source conversion
manifests, dataset hashes, archive window, split labels, and no-claim boundary.
It does not start strategy implementation, portfolio implementation, archive
performance evaluation, Growth instrumentation, RDL scaffolding, live feeds, or
OOS/performance claims.

## Frozen Scope

| Field | Value |
|---|---|
| Dataset count | 15 |
| Symbol count | 15 |
| Timeframe | `1d` |
| Window | `2020-01-01` through `2025-12-31` |
| Rows per dataset | 2192 |
| Archive only | `true` |
| Gate claim allowed | `false` |
| Manifest hash | `54a820dbb07557294e821356168db4dbc6ba70fda4464a519442c4b20faea35e` |

Allowed symbols:

`ADAUSDT`, `ALGOUSDT`, `ATOMUSDT`, `BCHUSDT`, `BNBUSDT`, `BTCUSDT`,
`DOGEUSDT`, `ETCUSDT`, `ETHUSDT`, `LINKUSDT`, `LTCUSDT`, `TRXUSDT`,
`VETUSDT`, `XLMUSDT`, `XRPUSDT`.

## Split Labels

| Label | Window | Rule |
|---|---|---|
| `ARCHIVE_FORMATION` | `2020-01-01` through `2022-12-31` | Available for future registered formation work |
| `ARCHIVE_VALIDATION` | `2023-01-01` through `2024-12-31` | Available only after future registration boundary exists |
| `ARCHIVE_HOLDOUT` | `2025-01-01` through `2025-12-31` | Forbidden before registration boundary |

## Artifacts

| Artifact | Path |
|---|---|
| Freeze builder | `entropy/evidence/phase1a_freeze.py` |
| Unit tests | `tests/unit/test_phase1a_freeze.py` |
| Package export | `entropy/evidence/__init__.py` |
| Freeze manifest | `artifacts/evidence/phase1a_archive_freeze/freeze_001/PHASE1A_ARCHIVE_FREEZE_MANIFEST.json` |
| Freeze summary | `artifacts/evidence/phase1a_archive_freeze/freeze_001/PHASE1A_ARCHIVE_FREEZE_SUMMARY.md` |
| Source archive stability manifest | `artifacts/evidence/data_stability/archive_2020_2025/DATA_STABILITY_ARCHIVE_MANIFEST.json` |
| Entry contract | `docs/audit/PHASE1A_ARCHIVE_ENTRY_CONTRACT.md` |

## Validation

- Exact 15-symbol Phase 1A allowed universe required.
- Every dataset must be `1d`, `2020-01-01` through `2025-12-31`, 2192 rows,
  and data quality `PASS`.
- Archive stability packet must remain archive-only, no-claim, 15 source
  manifests, 32880 rows, 2192 monitored archive days, 0 missing symbol-days,
  0 unexplained gaps, and `PACKET_READY_FOR_REVIEW`.
- Manifest boundary is
  `manifest_only_no_strategy_no_portfolio_no_performance_claim`.

## Next Task

Proceed to P1A-003: Archive Split Registration Boundary.

P1A-003 should implement the machine-readable registration/read-gate boundary
derived from this freeze. It must still avoid strategy logic, portfolio logic,
archive performance evaluation, Growth/RDL activation, live feeds, and
OOS/performance claims.
