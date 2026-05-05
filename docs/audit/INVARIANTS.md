# Entropy Protocol — Invariant Registry

**Audit Cycle:** Cycle 3 — Post-Phase0 Archive-Only Gate Audit
**Pipeline Step:** Step 3 — Invariant Extraction
**Pipeline Version:** v1.0
**Date:** 2026-05-05
**Status:** Draft — Awaiting Spec Owner Acceptance
**Prior step input:** `docs/audit/ARCH_MODEL.md`

## Category A — Frozen / Global Invariants

| ID | Invariant | Applies from | Flag |
|---|---|---|---|
| INV-C3-A01 | No live capital or live trading is authorized by archive-only Phase 0 closure | Now | PASS_REQUIRED |
| INV-C3-A02 | No OOS/performance claim may be made from foundation/evidence packets alone | Now | PASS_REQUIRED |
| INV-C3-A03 | Live/streaming Phase 0 gate remains distinct from archive-only foundation closure | Now | PASS_REQUIRED |
| INV-C3-A04 | Trial Registry and governance event writes remain append-only | Phase 0+ | PASS_REQUIRED |
| INV-C3-A05 | Four-stream P&L boundary remains intact; treasury stream is excluded from Net Sharpe | Phase 1+ | PASS_REQUIRED |
| INV-C3-A06 | RDL is dormant/scaffolding-only before Phase 2 | Phase 0-1 | PHASE_BOUNDARY |
| INV-C3-A07 | Growth/RBE active influence remains locked until explicit review and preregistration | Phase 0-1A | PHASE_BOUNDARY |

## Category B — Archive Phase 0 Closure Invariants

| ID | Invariant | Required evidence | Verdict |
|---|---|---|---|
| INV-C3-B01 | P4 labels cover >=3 years / >=15 assets for archive foundation | `P4_COVERAGE_PACKET_REVIEW.md` | PASS |
| INV-C3-B02 | SimBroker calibration has >=100 accepted rows within criterion | `SIMBROKER_AGENT_VERIFIED_CALIBRATION_PACKET.md` | PASS |
| INV-C3-B03 | Archive data stability has >=90 days, no missing symbol-days, no unexplained gaps | `DATA_STABILITY_ARCHIVE_PACKET.md` | PASS |
| INV-C3-B04 | Leakage/temporal-shuffling packet is accepted | `REGISTERED_LEAKAGE_GATE_PACKET.md` | PASS |
| INV-C3-B05 | Statistical helpers are report-boundary only, not performance validation | `STATISTICAL_REPORT_GATE_PACKET.md` | PASS |
| INV-C3-B06 | Live data stability is not claimed | D-027 / Phase 0 final sync | PASS |

## Category C — Phase 1A Entry Invariants

| ID | Invariant | Status before P1A-001 | Flag |
|---|---|---|---|
| INV-C3-C01 | Archive datasets must be frozen before strategy implementation | Contract defined in P1A-001; manifest next | BLOCKER_FOR_DATASET_USE |
| INV-C3-C02 | IS/OOS boundaries must be defined before archive evaluation | Contract defined in P1A-001 | BLOCKER_FOR_EVALUATION |
| INV-C3-C03 | Long-only baseline skill boundaries must be defined before skill code | Contract defined in P1A-001 | BLOCKER_FOR_SKILL_CODE |
| INV-C3-C04 | Portfolio constraints must be defined before portfolio implementation | Contract defined in P1A-001 | BLOCKER_FOR_PORTFOLIO_CODE |
| INV-C3-C05 | Growth Layer monitoring-only outputs must be defined before instrumentation | Contract defined in P1A-001 | BLOCKER_FOR_GROWTH_CODE |
| INV-C3-C06 | RDL dormancy attestation must be defined before any RDL-adjacent scaffolding | Contract defined in P1A-001 | BLOCKER_FOR_RDL_CODE |

## Category D — No-Claim Invariants

| ID | Forbidden claim/action | Status |
|---|---|---|
| INV-C3-D01 | Live feed stability claim | Forbidden |
| INV-C3-D02 | Live capital readiness claim | Forbidden |
| INV-C3-D03 | OOS performance claim | Forbidden |
| INV-C3-D04 | RDL telemetry closure claim | Forbidden |
| INV-C3-D05 | K-report closure claim | Forbidden |
| INV-C3-D06 | RBE activation or Growth Layer escalation | Forbidden |

## Summary Counts

| Type | Count |
|---|---:|
| Total invariants | 25 |
| PASS / currently satisfied | 13 |
| Phase-boundary invariants | 2 |
| Contract-defined blockers for later code tasks | 6 |
| Forbidden claims/actions | 6 |
