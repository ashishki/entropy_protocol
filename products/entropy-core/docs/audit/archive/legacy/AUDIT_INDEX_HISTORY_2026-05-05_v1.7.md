# Entropy Protocol — Audit Index

**Classification:** Confidential — Internal Governance Document
**Filename:** `products/entropy-core/docs/audit/AUDIT_INDEX.md`
**Version:** 1.7
**Date:** 2026-05-05
**Owner:** Spec Owner / Staff-Level Systems Architect

---

## Purpose

This index is the authoritative register of all audit artifacts for the Entropy Protocol. It defines naming conventions, tracks artifact status, and provides a permanent history of audit cycles. Every audit step output must be registered here.

---

## Artifact Naming Convention

### Canonical filenames (current cycle)

Canonical filenames are always overwritten with the latest output from the most recent full-pipeline run. They are the **single source of truth for the current state** of each artifact:

| Artifact | Canonical Filename | Pipeline Step |
|---|---|---|
| Meta Investigation | `products/entropy-core/docs/audit/META_ANALYSIS.md` | Step 1 |
| Architecture Review | `products/entropy-core/docs/audit/ARCH_MODEL.md` | Step 2 |
| Invariant Extraction | `products/entropy-core/docs/audit/INVARIANTS.md` | Step 3 |
| Drift Assertions | `products/entropy-core/docs/audit/DRIFT_ASSERTIONS.md` | Step 4 |
| Drift Report | `products/entropy-core/docs/audit/DRIFT_REPORT.md` | Step 4 |
| Adversarial Review | `products/entropy-core/docs/audit/ADVERSARIAL_REVIEW.md` | Step 5 |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Step 6 |

### Orchestration artifacts (current cycle)

These files are produced by the Meta Orchestration step and provide stable entrypoints for each pipeline run:

| Artifact | Canonical Filename | Role |
|---|---|---|
| Cycle Entrypoint | `products/entropy-core/docs/audit/PROMPT_0_META.md` | State snapshot + risk surface register; load first each cycle |
| Step 2 Prompt | `products/entropy-core/docs/audit/PROMPT_1_ARCH_REVIEW.md` | Agent prompt for Architecture Review |
| Step 3 Prompt | `products/entropy-core/docs/audit/PROMPT_2_INVARIANTS.md` | Agent prompt for Invariant Extraction |
| Step 4 Prompt | `products/entropy-core/docs/audit/PROMPT_3_DRIFT_GUARD.md` | Agent prompt for Drift Guard |
| Step 5 Prompt | `products/entropy-core/docs/audit/PROMPT_4_ADVERSARIAL.md` | Agent prompt for Adversarial Review |
| Step 6 Prompt | `products/entropy-core/docs/audit/PROMPT_5_CONSOLIDATED.md` | Agent prompt for Consolidated Review |
| Research Questions | `products/entropy-core/docs/audit/QUESTION_POOL.md` | Deep research question pool for spec development |

### Versioned snapshot filenames

When a full-pipeline run completes, the Step 6 agent creates versioned snapshots of all artifacts before overwriting canonical files. Versioned snapshots are **permanent** and must never be deleted.

**Format:** `YYYY-MM-DD_phase<N>_<ARTIFACT>_v<N>.md`

**Examples:**
- `2026-03-04_phase0_REVIEW_REPORT_v1.md`
- `2026-06-15_phase1_ARCH_MODEL_v2.md`
- `2026-09-01_phase2_INVARIANTS_v3.md`

**Rules:**
- `YYYY-MM-DD` = date the full-pipeline run was completed (not started)
- `phase<N>` = current phase at time of audit (phase0, phase1, phase2, phase3, phase4, phase5)
- `<ARTIFACT>` = canonical artifact name in UPPER_SNAKE_CASE (matches canonical filename stem)
- `v<N>` = artifact version within this phase; starts at v1 for each new phase entry, increments for each additional full run in the same phase

**Partial-run artifacts:** Use suffix `_partial_<step>` to distinguish. Example: `2026-04-10_phase0_ADVERSARIAL_REVIEW_partial_step5_v1.md`.

---

## Artifact Status Definitions

Every artifact in the History section carries one of three statuses:

| Status | Meaning |
|---|---|
| **Draft** | Artifact produced but not yet reviewed by the human Spec Owner. Not authoritative. |
| **Accepted** | Reviewed and approved by the Spec Owner. Authoritative for its cycle. |
| **Superseded** | A newer full-pipeline artifact has replaced this one. Retained for historical reference. |

Status transitions:
- `Draft → Accepted`: requires explicit Spec Owner sign-off (written comment in this file or an ADR)
- `Accepted → Superseded`: automatically applied when the next full-pipeline run completes and is accepted

---

## Latest Artifacts

The following canonical files represent the **current accepted state** of each audit artifact:

### Pipeline Execution Artifacts

| Artifact | File | Status | Date | Cycle |
|---|---|---|---|---|
| Meta Investigation | `products/entropy-core/docs/audit/META_ANALYSIS.md` | Draft | 2026-05-05 | Cycle 3, Post-Phase0 Archive-Only |
| Architecture Review | `products/entropy-core/docs/audit/ARCH_MODEL.md` | Draft | 2026-05-05 | Cycle 3, Post-Phase0 Archive-Only |
| Invariant Extraction | `products/entropy-core/docs/audit/INVARIANTS.md` | Draft | 2026-05-05 | Cycle 3, Post-Phase0 Archive-Only |
| Drift Assertions | `products/entropy-core/docs/audit/DRIFT_ASSERTIONS.md` | Draft | 2026-05-05 | Cycle 3, Post-Phase0 Archive-Only |
| Drift Report | `products/entropy-core/docs/audit/DRIFT_REPORT.md` | Draft | 2026-05-05 | Cycle 3, Post-Phase0 Archive-Only |
| Adversarial Review | `products/entropy-core/docs/audit/ADVERSARIAL_REVIEW.md` | Draft | 2026-05-05 | Cycle 3, Post-Phase0 Archive-Only |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | 2026-05-05 | Cycle 3, Post-Phase0 Archive-Only |
| Phase 2 Boundary Review | `products/entropy-core/docs/audit/PHASE2_REVIEW.md` | Draft | 2026-05-03 | Phase 2 Boundary |
| Phase 3 Boundary Review | `products/entropy-core/docs/audit/PHASE3_REVIEW.md` | Draft | 2026-05-03 | Phase 3 Boundary |
| Phase 4 Boundary Review | `products/entropy-core/docs/audit/PHASE4_REVIEW.md` | Draft | 2026-05-03 | Phase 4 Boundary |
| Phase 5 Boundary Review | `products/entropy-core/docs/audit/PHASE5_REVIEW.md` | Draft | 2026-05-03 | Phase 5 Boundary |
| Phase 6 Boundary Review | `products/entropy-core/docs/audit/PHASE6_REVIEW.md` | Draft | 2026-05-03 | Phase 6 Boundary |
| Phase 7 Boundary Review | `products/entropy-core/docs/audit/PHASE7_REVIEW.md` | Draft | 2026-05-03 | Phase 7 Boundary |
| T21 Formula-Governance Disposition | `products/entropy-core/docs/audit/T21_FORMULA_GOVERNANCE_DISPOSITION.md` | Draft | 2026-05-03 | Phase 8 Entry |
| T22 Governance Disposition | `products/entropy-core/docs/audit/T22_GOVERNANCE_DISPOSITION.md` | Draft | 2026-05-05 | Phase 8 |
| Phase 8 Boundary Review | `products/entropy-core/docs/audit/PHASE8_REVIEW.md` | Draft | 2026-05-05 | Phase 8 Boundary |
| T23 Formula-Governance Disposition | `products/entropy-core/docs/audit/T23_FORMULA_GOVERNANCE_DISPOSITION.md` | Draft | 2026-05-05 | Phase 9 |
| T24 Exit-Artifacts Disposition | `products/entropy-core/docs/audit/T24_EXIT_ARTIFACTS_DISPOSITION.md` | Draft | 2026-05-05 | Phase 9 |
| Phase 0 Foundation Review | `products/entropy-core/docs/audit/PHASE0_FOUNDATION_REVIEW.md` | Draft | 2026-05-05 | Post-T24 |
| Post-Phase Strategy Review | `products/entropy-core/docs/audit/POST_PHASE_STRATEGY_REVIEW.md` | Draft | 2026-05-05 | Post-T24 |
| Phase 0 Strategic Decision | `products/entropy-core/docs/audit/PHASE0_STRATEGIC_DECISION.md` | Draft | 2026-05-05 | PSR-002 |
| Phase 0 Exit Gap Register | `products/entropy-core/docs/audit/PHASE0_EXIT_GAP_REGISTER.md` | Draft | 2026-05-05 | P0.5-001 |
| Formula Evidence Debt Register | `products/entropy-core/docs/audit/FORMULA_EVIDENCE_DEBT.md` | Draft | 2026-05-05 | P0.5-002 |
| Sharpe CI Review | `products/entropy-core/docs/audit/SHARPE_CI_REVIEW.md` | Draft | 2026-05-05 | P0.5-003 |
| Harvey-Liu Review | `products/entropy-core/docs/audit/HARVEY_LIU_REVIEW.md` | Draft | 2026-05-05 | P0.6-005 |
| Purge Embargo Decision | `products/entropy-core/docs/audit/PURGE_EMBARGO_DECISION.md` | Draft | 2026-05-05 | P0.5-004 |
| P4 Gate Decision | `products/entropy-core/docs/audit/P4_GATE_DECISION.md` | Draft | 2026-05-05 | P0.5-005 |
| SimBroker Calibration Plan | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_PLAN.md` | Draft | 2026-05-05 | P0.6-006 |
| Data Stability Plan | `products/entropy-core/docs/audit/DATA_STABILITY_PLAN.md` | Draft | 2026-05-05 | P0.6-007 |
| Architecture And Spec Reality Sync | `products/entropy-core/docs/ARCHITECTURE.md`; `products/entropy-core/docs/spec.md`; `products/entropy-core/docs/tasks.md`; `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | 2026-05-05 | P0.5-008 |
| Phase 0 Gate Packet | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | 2026-05-05 | P0.5-009 |
| Next Phase Plan | `products/entropy-core/docs/audit/NEXT_PHASE_PLAN.md` | Draft | 2026-05-05 | Post-T24 |
| Evidence Collection Authorization | `products/entropy-core/docs/audit/EVIDENCE_COLLECTION_AUTHORIZATION.md` | Draft | 2026-05-05 | P0.6-008 |
| Evidence Source Selection | `products/entropy-core/docs/audit/EVIDENCE_SOURCE_SELECTION.md` | Draft | 2026-05-05 | P0.6-HUMAN-001 |
| Crypto Universe Snapshot | `products/entropy-core/docs/audit/CRYPTO_UNIVERSE_SNAPSHOT.md` | Draft | 2026-05-05 | P0.7-001 |
| Source Manifest Bootstrap | `products/entropy-core/docs/audit/SOURCE_MANIFEST_BOOTSTRAP.md` | Draft | 2026-05-05 | P0.7-001 |
| Binance P4 Canary | `products/entropy-core/docs/audit/BINANCE_P4_CANARY.md` | Draft | 2026-05-05 | P0.7-002 |
| P4 Coverage Scale Plan | `products/entropy-core/docs/audit/P4_COVERAGE_SCALE_PLAN.md` | Draft | 2026-05-05 | P0.7-003 |
| P4 Coverage Scale Manifest | `products/entropy-core/docs/audit/P4_COVERAGE_SCALE_MANIFEST.json` | Draft | 2026-05-05 | P0.7-003 |
| P4 First Batch Collection | `products/entropy-core/docs/audit/P4_FIRST_BATCH_COLLECTION.md` | Draft | 2026-05-05 | P0.7-004 |
| P4 Coverage Packet Review | `products/entropy-core/docs/audit/P4_COVERAGE_PACKET_REVIEW.md` | Draft | 2026-05-05 | P0.7-016 |
| Phase 0 Gate Packet Sync | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | 2026-05-05 | P0.7-017 |
| SimBroker Calibration Bootstrap | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_BOOTSTRAP.md` | Draft | 2026-05-05 | P0.7-018 |
| SimBroker Calibration Candidate Row Plan | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_CANDIDATE_ROW_PLAN.md` | Draft | 2026-05-05 | P0.7-019 |
| SimBroker Calibration Dry Run | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_DRY_RUN.md` | Draft | 2026-05-05 | P0.7-020 |
| Data Stability Bootstrap | `products/entropy-core/docs/audit/DATA_STABILITY_BOOTSTRAP.md` | Draft | 2026-05-05 | P0.7-021 |
| Data Stability Simulation | `products/entropy-core/docs/audit/DATA_STABILITY_SIMULATION.md` | Draft | 2026-05-05 | P0.7-022 |
| Daily Stability Append Procedure | `products/entropy-core/docs/audit/DAILY_STABILITY_APPEND_PROCEDURE.md` | Draft | 2026-05-05 | P0.7-022 |
| SimBroker Agent-Assisted Verification Decision | `products/entropy-core/docs/audit/SIMBROKER_AGENT_ASSISTED_VERIFICATION_DECISION.md` | Draft | 2026-05-05 | P0.7-022 |
| SimBroker Agent-Verified Calibration Packet | `products/entropy-core/docs/audit/SIMBROKER_AGENT_VERIFIED_CALIBRATION_PACKET.md` | Draft | 2026-05-05 | P0.7-023 |
| Data Stability Live Append Tooling | `products/entropy-core/docs/audit/DATA_STABILITY_LIVE_APPEND_TOOLING.md` | Draft | 2026-05-05 | P0.7-024 |
| Registered Leakage Gate Packet | `products/entropy-core/docs/audit/REGISTERED_LEAKAGE_GATE_PACKET.md` | Draft | 2026-05-05 | P0.7-025 |
| Statistical Report Gate Packet | `products/entropy-core/docs/audit/STATISTICAL_REPORT_GATE_PACKET.md` | Draft | 2026-05-05 | P0.7-026 |
| Archive-Only Evidence Mode Decision | `products/entropy-core/docs/audit/ARCHIVE_ONLY_EVIDENCE_MODE_DECISION.md` | Draft | 2026-05-05 | P0.7-028 |
| Data Stability Archive Packet | `products/entropy-core/docs/audit/DATA_STABILITY_ARCHIVE_PACKET.md` | Draft | 2026-05-05 | P0.7-028 |
| Phase 0 Final Sync | `products/entropy-core/docs/audit/PHASE0_FINAL_SYNC.md` | Draft | 2026-05-05 | P0.7-028 |
| Archive-Only Continuation Decision | `products/entropy-core/docs/audit/ARCHIVE_ONLY_CONTINUATION_DECISION.md` | Draft | 2026-05-05 | PSR-003 |
| Phase 1A Archive Entry Contract | `products/entropy-core/docs/audit/PHASE1A_ARCHIVE_ENTRY_CONTRACT.md` | Draft | 2026-05-05 | P1A-001 |
| Phase 1A Archive Freeze Packet | `products/entropy-core/docs/audit/PHASE1A_ARCHIVE_FREEZE_PACKET.md` | Draft | 2026-05-05 | P1A-002 |
| Phase 1A Registration Boundary Packet | `products/entropy-core/docs/audit/PHASE1A_REGISTRATION_BOUNDARY_PACKET.md` | Draft | 2026-05-05 | P1A-003 |
| Phase 1A Baseline Registration Packet | `products/entropy-core/docs/audit/PHASE1A_BASELINE_REGISTRATION_PACKET.md` | Draft | 2026-05-05 | P1A-004 |
| Phase 1A Fix Closure Review | `products/entropy-core/docs/audit/PHASE1A_FIX_CLOSURE_REVIEW.md` | Draft | 2026-05-05 | P1A-005 |

### Orchestration Artifacts (current)

| Artifact | File | Status | Date | Cycle |
|---|---|---|---|---|
| Cycle Entrypoint | `products/entropy-core/docs/audit/PROMPT_0_META.md` | Draft | 2026-03-04 | Cycle 1 |
| Step 2 Prompt | `products/entropy-core/docs/audit/PROMPT_1_ARCH_REVIEW.md` | Draft | 2026-03-04 | Cycle 1 |
| Step 3 Prompt | `products/entropy-core/docs/audit/PROMPT_2_INVARIANTS.md` | Draft | 2026-03-04 | Cycle 1 |
| Step 4 Prompt | `products/entropy-core/docs/audit/PROMPT_3_DRIFT_GUARD.md` | Draft | 2026-03-04 | Cycle 1 |
| Step 5 Prompt | `products/entropy-core/docs/audit/PROMPT_4_ADVERSARIAL.md` | Draft | 2026-03-04 | Cycle 1 |
| Step 6 Prompt | `products/entropy-core/docs/audit/PROMPT_5_CONSOLIDATED.md` | Draft | 2026-03-04 | Cycle 1 |
| Research Questions | `products/entropy-core/docs/audit/QUESTION_POOL.md` | Draft | 2026-03-04 | Cycle 1 |

Note: Cycle 1 full pipeline artifacts are now generated in canonical form and remain Draft pending Spec Owner acceptance.

---

## History

### P1A-005 — Phase 1A Fix Closure Review (2026-05-05)

**Trigger:** P1A-001 through P1A-004 completed the contract/read-gate fix
chain and required a decision before executable scaffold work.
**Type:** Closure review and next-scope decision.
**Pipeline version:** Phase 1A archive-only planning.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Phase 1A Fix Closure Review | `products/entropy-core/docs/audit/PHASE1A_FIX_CLOSURE_REVIEW.md` | Draft | D-033 |

**Outcome summary:**
- P1A-001 through P1A-004 close the required contract/read-gate fixes.
- A narrow executable archive baseline scaffold is approved as the next scope.
- Holdout remains locked.
- Live, Growth/RDL/RBE, portfolio/backtest evaluation, and OOS/performance
  claims remain forbidden.
- F-C3-007 remains a non-blocking P2 audit-maintenance item.
- Next task is P1A-006: Archive Baseline Executable Scaffold.

### P1A-004 — Archive Baseline Specification Registration (2026-05-05)

**Trigger:** P1A-003 created the read gate, but no baseline specification hash
or validation registration metadata existed yet.
**Type:** Archive-only non-executable baseline specification registration.
**Pipeline version:** Phase 1A archive-only planning.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Phase 1A Baseline Registration Packet | `products/entropy-core/docs/audit/PHASE1A_BASELINE_REGISTRATION_PACKET.md` | Draft | D-032 |
| Baseline Registration Manifest | `artifacts/evidence/phase1a_baseline_registration/registration_001/PHASE1A_BASELINE_SPEC_REGISTRATION_MANIFEST.json` | Draft | Hash `1b968c53607729fd3a67a9a3a4264f93e9f0a1ad60044e5614baa596a8a0ba01` |
| Baseline Registration Summary | `artifacts/evidence/phase1a_baseline_registration/registration_001/PHASE1A_BASELINE_SPEC_REGISTRATION_SUMMARY.md` | Draft | Holdout locked |

**Outcome summary:**
- Non-executable long-only baseline specification shape is registered.
- Baseline spec hash:
  `a94c0441e0ff5b38bd0bafe83e445fe2041eb19e936dac19526ef417c39d3646`.
- Validation registration hash:
  `7a23273630350704809be291da57c06e23e15537a16eaf3950d5e0da599816b4`.
- Holdout remains locked.
- No strategy, portfolio evaluation, Growth, RDL, live, OOS, or performance
  claim is authorized.
- Next task is P1A-005: Phase 1A Fix Closure Review.

### P1A-003 — Archive Split Registration Boundary (2026-05-05)

**Trigger:** P1A-002 froze datasets and split labels but future code still
needed a machine-readable read gate before any dataset-consuming implementation.
**Type:** Archive-only registration/read-gate manifest.
**Pipeline version:** Phase 1A archive-only planning.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Phase 1A Registration Boundary Packet | `products/entropy-core/docs/audit/PHASE1A_REGISTRATION_BOUNDARY_PACKET.md` | Draft | D-031 |
| Boundary Manifest | `artifacts/evidence/phase1a_registration_boundary/boundary_001/PHASE1A_ARCHIVE_REGISTRATION_BOUNDARY_MANIFEST.json` | Draft | Hash `2759fad18037361412f504384f22b411b4283b00e7764150f8c660f4375620df` |
| Boundary Summary | `artifacts/evidence/phase1a_registration_boundary/boundary_001/PHASE1A_ARCHIVE_REGISTRATION_BOUNDARY_SUMMARY.md` | Draft | Holdout locked |

**Outcome summary:**
- Formation reads are allowed for formation/instrumentation purposes.
- Validation reads require registration metadata.
- Holdout reads are locked with
  `HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION`.
- No strategy, portfolio, Growth, RDL, live, OOS, or performance claim is
  authorized.
- Next task is P1A-004: Archive Baseline Specification Registration.

### P1A-002 — Archive Dataset Freeze Manifest (2026-05-05)

**Trigger:** P1A-001 required a machine-readable dataset freeze before any
dataset-consuming implementation.
**Type:** Archive-only freeze manifest.
**Pipeline version:** Phase 1A archive-only planning.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Phase 1A Archive Freeze Packet | `products/entropy-core/docs/audit/PHASE1A_ARCHIVE_FREEZE_PACKET.md` | Draft | D-030 |
| Freeze Manifest | `artifacts/evidence/phase1a_archive_freeze/freeze_001/PHASE1A_ARCHIVE_FREEZE_MANIFEST.json` | Draft | Hash `54a820dbb07557294e821356168db4dbc6ba70fda4464a519442c4b20faea35e` |
| Freeze Summary | `artifacts/evidence/phase1a_archive_freeze/freeze_001/PHASE1A_ARCHIVE_FREEZE_SUMMARY.md` | Draft | 15 datasets, 15 symbols |

**Outcome summary:**
- Frozen universe: 15 approved `1d` archive datasets.
- Frozen window: `2020-01-01` through `2025-12-31`.
- Split labels encoded for formation, validation, and holdout.
- Holdout is forbidden before registration boundary.
- No strategy, portfolio, Growth, RDL, live, OOS, or performance claim is
  authorized.
- Next task is P1A-003: Archive Split Registration Boundary.

### P1A-001 — Phase 1 Archive Entry Contract (2026-05-05)

**Trigger:** Cycle 3 audit found six P1 contract gaps blocking any
dataset-consuming implementation.
**Type:** Archive-only entry contract.
**Pipeline version:** Phase 1A archive-only planning.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Phase 1A Archive Entry Contract | `products/entropy-core/docs/audit/PHASE1A_ARCHIVE_ENTRY_CONTRACT.md` | Draft | D-029 |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | F-C3-001 through F-C3-006 closed by contract |

**Outcome summary:**
- Closed Cycle 3 P1 findings F-C3-001 through F-C3-006 by contract.
- Defined dataset freeze rules, archive split labels, skill boundaries,
  portfolio constraints, Growth monitoring-only scope, and RDL dormancy
  attestation.
- Phase 1 implementation remains blocked.
- Next task is P1A-002: Archive Dataset Freeze Manifest.

### Cycle 3 — Post-Phase0 Archive-Only Gate Audit (2026-05-05)

**Trigger:** Archive-only Phase 0 foundation closure and PSR-003 selection of
Phase 1A Archive-Only Baseline Planning and Instrumentation.
**Type:** Full pipeline run.
**Pipeline version:** v1.0.
**Spec context:** Archive-only Phase 0 closure; D-027/D-028.

| Artifact | Canonical file | Versioned snapshot name | Status |
|---|---|---|---|
| Meta Investigation | `products/entropy-core/docs/audit/META_ANALYSIS.md` | `2026-05-05_phase0_archive_META_ANALYSIS_v3.md` | Draft |
| Architecture Review | `products/entropy-core/docs/audit/ARCH_MODEL.md` | `2026-05-05_phase0_archive_ARCH_MODEL_v3.md` | Draft |
| Invariant Extraction | `products/entropy-core/docs/audit/INVARIANTS.md` | `2026-05-05_phase0_archive_INVARIANTS_v3.md` | Draft |
| Drift Assertions | `products/entropy-core/docs/audit/DRIFT_ASSERTIONS.md` | `2026-05-05_phase0_archive_DRIFT_ASSERTIONS_v3.md` | Draft |
| Drift Report | `products/entropy-core/docs/audit/DRIFT_REPORT.md` | `2026-05-05_phase0_archive_DRIFT_REPORT_v3.md` | Draft |
| Adversarial Review | `products/entropy-core/docs/audit/ADVERSARIAL_REVIEW.md` | `2026-05-05_phase0_archive_ADVERSARIAL_REVIEW_v3.md` | Draft |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | `2026-05-05_phase0_archive_REVIEW_REPORT_v3.md` | Draft |

**Outcome summary:**
- Confirmed archive-only Phase 0 foundation closure is not invalidated.
- Confirmed live/streaming Phase 0 remains not approved.
- Verdict: `GO_FOR_P1A-001`; `NO_GO_FOR_PHASE_1_IMPLEMENTATION`.
- Cycle 3 P1 findings were later closed by P1A-001; 1 P2 audit-maintenance
  item remains open.
- Spec Owner sign-off: Pending.

### PSR-003 — Archive-Only Continuation Decision (2026-05-05)

**Trigger:** P0.7-028 closed the archive-only Phase 0 foundation and required a
strategic next-stage decision before adding new implementation surface.
**Type:** Strategy decision.
**Pipeline version:** Post-Phase-0 archive-only strategist review.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Archive-Only Continuation Decision | `products/entropy-core/docs/audit/ARCHIVE_ONLY_CONTINUATION_DECISION.md` | Draft | D-028 |

**Outcome summary:**
- Selected Phase 1A Archive-Only Baseline Planning and Instrumentation.
- Rejected live monitoring, live trading, streaming provider work, RDL
  hypothesis generation, Growth Layer escalation, and OOS/performance claims.
- First next task is P1A-001: Phase 1 Archive Entry Contract.

### P0.7-028 — Archive-Mode Data Stability Packet (2026-05-05)

**Trigger:** Owner clarified that current work should not run live monitoring
and must continue with archive-only evidence.
**Type:** Archive-only evidence decision and data-stability packet.
**Pipeline version:** Phase 0.7 archive-only evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Archive-Only Evidence Mode Decision | `products/entropy-core/docs/audit/ARCHIVE_ONLY_EVIDENCE_MODE_DECISION.md` | Draft | D-027 scope decision |
| Data Stability Archive Packet | `products/entropy-core/docs/audit/DATA_STABILITY_ARCHIVE_PACKET.md` | Draft | Archive data-stability acceptance |
| Archive Manifest | `artifacts/evidence/data_stability/archive_2020_2025/DATA_STABILITY_ARCHIVE_MANIFEST.json` | Draft | Machine-readable packet manifest |
| Phase 0 Final Sync | `products/entropy-core/docs/audit/PHASE0_FINAL_SYNC.md` | Draft | Archive-only final gate disposition |

**Outcome summary:**
- D-027 restricts current evidence work to archive-only datasets.
- Built `DATA-STABILITY-ARCHIVE-90D-v1` from 15 approved source manifests.
- Monitored archive days: 2192.
- Rows: 32880.
- Missing symbol-days: 0.
- Unexplained gaps: 0.
- Archive-only Phase 0 research foundation is ready for strategist review.
- Live/streaming data-stability remains a future hard gate.

### P0.7-027 — Phase 0 Gate Packet Final Sync (2026-05-05)

**Trigger:** P0.7-026 closed the statistical report-boundary blocker, leaving
the Phase 0 gate packet ready for final blocker reconciliation.
**Type:** Gate packet final sync.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Phase 0 Final Sync | `products/entropy-core/docs/audit/PHASE0_FINAL_SYNC.md` | Draft | Final blocker state |
| Phase 0 Gate Packet | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | Updated gate state |

**Outcome summary:**
- Phase 0 remains `NOT_APPROVED`.
- All currently closable evidence blockers are closed.
- Remaining blocker: >=90 continuous monitored days of data-stability evidence.
- Current live monitored day count: 1.
- Superseded by P0.7-028 after D-027 restricted current work to archive-only
  evidence.

### P0.7-026 — Statistical Report Gate Packets (2026-05-05)

**Trigger:** P0.7-025 closed leakage evidence, leaving Sharpe CI and Harvey-Liu
report-boundary packets as the next closable blocker.
**Type:** Statistical report-boundary evidence packet.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Statistical Report Gate Packet | `products/entropy-core/docs/audit/STATISTICAL_REPORT_GATE_PACKET.md` | Draft | Packet acceptance |
| Statistical Report Gate Manifest | `artifacts/evidence/statistical_gate/STATISTICAL_REPORT_GATE_MANIFEST.json` | Draft | Machine-readable packet manifest |

**Outcome summary:**
- Accepted `CI-SR-ACF-v1` as report-boundary tooling.
- Accepted `HL-HB-v1` family workflow as report-boundary tooling.
- Legacy single-trial Harvey-Liu scaffold remains rejected for gate/report
  proof.
- No strategy validation or OOS/performance claim is made.
- Statistical report-boundary blocker is closed.
- Next task is P0.7-027: Phase 0 Gate Packet Final Sync.

### P0.7-025 — Registered Leakage Gate Packet (2026-05-05)

**Trigger:** P0.7-024 left registered leakage/temporal-shuffling evidence as the
next closable Phase 0 blocker.
**Type:** Leakage evidence packet and temporal-shuffling implementation.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Registered Leakage Gate Packet | `products/entropy-core/docs/audit/REGISTERED_LEAKAGE_GATE_PACKET.md` | Draft | Packet acceptance |
| Leakage Gate Manifest | `artifacts/evidence/leakage_gate/REGISTERED_LEAKAGE_GATE_MANIFEST.json` | Draft | Machine-readable packet manifest |
| Temporal Shuffle Audit | `entropy/walkforward/temporal_shuffle.py` | Draft | `TS-OOS-SHUFFLE-v1` implementation |

**Outcome summary:**
- Added `TS-OOS-SHUFFLE-v1`.
- Temporal shuffle passes only when IS feature hash is invariant to deterministic
  OOS reversal.
- Packet combines T19 checklist, T20 OOS block, omitted-detector FAIL policy,
  `PE-MAX-HORIZON-v1`, and `TS-OOS-SHUFFLE-v1`.
- Leakage/temporal-shuffling evidence blocker is closed.
- Next task is P0.7-026: Statistical Report Gate Packets.

### P0.7-024 — Live Data Stability Append Tooling (2026-05-05)

**Trigger:** P0.7-022 defined the append procedure; reusable tooling was needed
to avoid manual daily row assembly.
**Type:** Evidence append tooling and first live append.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Data Stability Live Append Tooling | `products/entropy-core/docs/audit/DATA_STABILITY_LIVE_APPEND_TOOLING.md` | Draft | Tooling result and first append |
| Cumulative Rows | `artifacts/evidence/data_stability/live_monitor/DATA_STABILITY_ROWS.jsonl` | Draft | Append-only monitor rows |
| Cumulative Summary | `artifacts/evidence/data_stability/live_monitor/DATA_STABILITY_SUMMARY.md` | Draft | Current status INCOMPLETE |
| Daily Raw Manifest | `artifacts/evidence/data_stability/live_monitor/raw/2026-05-05/SIMBROKER_CALIBRATION_BOOTSTRAP_MANIFEST.json` | Draft | Daily approved-source raw snapshot manifest |

**Outcome summary:**
- Added append-only live data-stability helper and tests.
- First real append wrote 10 rows for 2026-05-05.
- Monitored day count: 1.
- Missing symbol-days: 0.
- Unexplained gaps: 0.
- Packet status: `INCOMPLETE`.
- The 90-day gate remains open until elapsed monitoring reaches >=90 days.
- Next task is P0.7-025: Registered Leakage Gate Packet.

### P0.7-023 — SimBroker Agent Verification Approval And Calibration Packet (2026-05-05)

**Trigger:** Owner approved agent-assisted deterministic verification as
equivalent to manual verification for Phase 0 SimBroker calibration evidence.
**Type:** Verification-policy decision and calibration evidence packet.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Agent-Assisted Verification Decision | `products/entropy-core/docs/audit/SIMBROKER_AGENT_ASSISTED_VERIFICATION_DECISION.md` | Draft | D-026 owner approval |
| Agent-Verified Calibration Packet | `products/entropy-core/docs/audit/SIMBROKER_AGENT_VERIFIED_CALIBRATION_PACKET.md` | Draft | 100-row packet acceptance |
| Agent-Verified Rows | `artifacts/evidence/simbroker_calibration/agent_verified_001/SIMBROKER_AGENT_VERIFIED_CALIBRATION_ROWS.jsonl` | Draft | 100 included rows |
| Agent-Verified Summary | `artifacts/evidence/simbroker_calibration/agent_verified_001/SIMBROKER_AGENT_VERIFIED_CALIBRATION_SUMMARY.md` | Draft | Packet-ready summary |

**Outcome summary:**
- D-026 records owner approval.
- Built 100 included calibration rows from approved public quote snapshots and
  deterministic SimBroker fill logs.
- Included rows: 100.
- Pass count: 100.
- Failure count: 0.
- Assets: 5.
- Packet status: `PACKET_READY_FOR_REVIEW`.
- SimBroker calibration evidence blocker is closed.
- Next task is P0.7-024: Live Data Stability Append Tooling.

### P0.7-022 — Daily Stability Append Procedure (2026-05-05)

**Trigger:** User asked to simulate monitoring now and later switch to real data
and stream, and asked whether Codex can handle row selection.
**Type:** Fixture simulation, procedure, and verification-policy proposal.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Data Stability Simulation | `products/entropy-core/docs/audit/DATA_STABILITY_SIMULATION.md` | Draft | 90-day fixture simulation |
| Daily Stability Append Procedure | `products/entropy-core/docs/audit/DAILY_STABILITY_APPEND_PROCEDURE.md` | Draft | Real append procedure |
| Agent-Assisted Verification Decision | `products/entropy-core/docs/audit/SIMBROKER_AGENT_ASSISTED_VERIFICATION_DECISION.md` | Draft | Requires owner approval |
| Simulation Rows | `artifacts/evidence/data_stability/simulation_90d_001/DATA_STABILITY_SIMULATION_ROWS.jsonl` | Draft | 450 fixture rows |
| Simulation Summary | `artifacts/evidence/data_stability/simulation_90d_001/DATA_STABILITY_SIMULATION_SUMMARY.md` | Draft | Mechanical packet-ready state |

**Outcome summary:**
- Added fixture-only data-stability simulation helper and tests.
- Generated 450 rows across 90 simulated days and 5 assets.
- Mechanical packet status reaches `PACKET_READY_FOR_REVIEW`.
- Gate claim remains disabled because the evidence is simulated.
- Defined the real daily append procedure.
- Recorded that Codex can automate SimBroker row selection/candidate assembly,
  but replacing manual verification with agent-assisted verification requires
  explicit owner approval.
- Next task is P0.7-023: SimBroker Agent Verification Approval And Calibration
  Packet.

### P0.7-021 — Data Stability Bootstrap (2026-05-05)

**Trigger:** SimBroker calibration could not be fully closed without real manual
verification, so the next feasible hard blocker was starting the elapsed-time
data-stability trail.
**Type:** Evidence bootstrap.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Data Stability Bootstrap | `products/entropy-core/docs/audit/DATA_STABILITY_BOOTSTRAP.md` | Draft | Day-1 bootstrap and boundary |
| Bootstrap Rows | `artifacts/evidence/data_stability/bootstrap_001/DATA_STABILITY_BOOTSTRAP_ROWS.jsonl` | Draft | 10 monitor rows |
| Bootstrap Summary | `artifacts/evidence/data_stability/bootstrap_001/DATA_STABILITY_BOOTSTRAP_SUMMARY.md` | Draft | Summary status INCOMPLETE |

**Outcome summary:**
- Wrote 10 monitor rows from approved public quote snapshots.
- Monitored day count: 1.
- Missing symbol-days: 0.
- Unexplained gaps: 0.
- Packet status: `INCOMPLETE`.
- Data-stability gate remains open until >=90 continuous monitored days.
- Next task is P0.7-022: Daily Stability Append Procedure.

### P0.7-020 — SimBroker Calibration Packet Assembly Dry Run (2026-05-05)

**Trigger:** P0.7-019 implemented row construction; packet assembly mechanics
needed a fixture-only end-to-end check.
**Type:** Fixture dry run.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| SimBroker Calibration Dry Run | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_DRY_RUN.md` | Draft | Dry-run result and boundary |
| Fixture Rows | `artifacts/evidence/simbroker_calibration/dry_run_001/SIMBROKER_CALIBRATION_DRY_RUN_ROWS.jsonl` | Draft | 100 excluded fixture rows |
| Fixture Summary | `artifacts/evidence/simbroker_calibration/dry_run_001/SIMBROKER_CALIBRATION_DRY_RUN_SUMMARY.md` | Draft | Summary status INCOMPLETE |

**Outcome summary:**
- Generated 100 fixture rows through `build_calibration_row_from_fill()`.
- Wrote JSONL rows and deterministic summary.
- All rows are excluded as `fixture_non_gate`.
- No real calibration evidence was created.
- SimBroker calibration gate remains open.
- Next task is P0.7-021: Data Stability Bootstrap.

### P0.7-019 — SimBroker Calibration Candidate Row Plan (2026-05-05)

**Trigger:** P0.7-018 proved approved public quote source readiness but did not
define the deterministic row-construction path from fills and quotes.
**Type:** Calibration tooling and evidence-plan implementation.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| SimBroker Calibration Candidate Row Plan | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_CANDIDATE_ROW_PLAN.md` | Draft | Builder path and no-claim boundary |

**Outcome summary:**
- Added `build_calibration_row_from_fill()`.
- Builder maps real `FillLog` plus approved `BidAskQuote` into
  `CalibrationRow`.
- Buy rows reference ask; sell rows reference bid.
- Stale quotes are excluded as `quote_timestamp_outside_tolerance`.
- Gate claim remains disabled.
- SimBroker calibration gate remains open until >=100 manually verified rows.
- Next task is P0.7-020: SimBroker Calibration Packet Assembly Dry Run.

### P0.7-018 — SimBroker Calibration Bootstrap (2026-05-05)

**Trigger:** P0.7-017 left SimBroker calibration as the next feasible Phase 0
hard blocker after P4 evidence closure.
**Type:** Evidence-source bootstrap and tooling.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| SimBroker Calibration Bootstrap | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_BOOTSTRAP.md` | Draft | Source bootstrap result and boundary |
| Bootstrap Manifest | `artifacts/evidence/simbroker_calibration/bootstrap_001/SIMBROKER_CALIBRATION_BOOTSTRAP_MANIFEST.json` | Draft | Raw quote snapshot manifest |
| Bootstrap Summary | `artifacts/evidence/simbroker_calibration/bootstrap_001/SIMBROKER_CALIBRATION_BOOTSTRAP_SUMMARY.md` | Draft | Human-readable summary |
| Raw Quote Extracts | `artifacts/evidence/simbroker_calibration/bootstrap_001/raw/` | Draft | Approved public quote extracts |

**Outcome summary:**
- Added quote bootstrap tooling and tests.
- Collected 10/10 public bid/ask quote snapshots.
- Sources: Coinbase Exchange public API and Kraken public API.
- Assets: BTC-USD, ETH-USD, LTC-USD, BCH-USD, XLM-USD.
- Raw extracts and SHA-256 hashes are recorded.
- No calibration rows were created; manual verification remains incomplete.
- SimBroker calibration gate remains open.
- Next task is P0.7-019: SimBroker Calibration Candidate Row Plan.

### P0.7-017 — Phase 0 Gate Packet Sync (2026-05-05)

**Trigger:** P0.7-016 accepted the revised P4 coverage candidate, requiring the
Phase 0 gate packet to reflect P4 closure without approving the whole phase.
**Type:** Gate packet synchronization.
**Pipeline version:** Phase 0.7 free-source evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Phase 0 Gate Packet | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | P4 evidence closure and remaining blocker state |

**Outcome summary:**
- P4 label coverage is marked closed for evidence.
- Phase 0 remains `NOT_APPROVED`.
- Remaining hard blockers include SimBroker calibration, 90-day data stability,
  registered leakage/temporal-shuffling packet, and report/gate formula packets.
- Next task is P0.7-018: SimBroker Calibration Bootstrap.

### P0.7-016 — P4 Coverage Packet Review (2026-05-05)

**Trigger:** P0.7-015 produced the revised first-15 P4 coverage candidate and
required review before the P4 blocker could be treated as evidence-closed.
**Type:** Evidence review.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 Coverage Packet Review | `products/entropy-core/docs/audit/P4_COVERAGE_PACKET_REVIEW.md` | Draft | Review decision and boundary |
| Coverage Manifest | `artifacts/evidence/p4_binance_scale/revised_v2/coverage/first_15_assets_2020_2025/P4_REVISED_FIRST15_COVERAGE_MANIFEST.json` | Draft | Reviewed aggregate packet |

**Outcome summary:**
- Review findings: 0.
- Batch manifests present: 54/54.
- Source archives present: 1080/1080.
- Source SHA-256 mismatches: 0.
- Full-window symbol manifests present: 15/15.
- Dataset hash mismatches: 0.
- Label artifacts present: 15/15.
- Valid post-warmup P4 labeled weeks: 157 per asset.
- Accepted as the current P4 evidence candidate.
- Phase 0 remains `NOT_APPROVED` pending remaining gate blockers.
- Next task is P0.7-017: Phase 0 Gate Packet Sync.

### P0.7-015 — Revised P4 First 15 Coverage Build (2026-05-05)

**Trigger:** User requested continuing without stopping until the revised P4
coverage steps were complete, while minimizing per-batch documentation churn.
**Type:** Evidence collection, conversion, and aggregate coverage candidate.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Revised P4 First 15 Coverage Packet | `products/entropy-core/docs/audit/P4_REVISED_FIRST15_COVERAGE_PACKET.md` | Draft | Human-readable coverage packet candidate |
| Coverage Manifest | `artifacts/evidence/p4_binance_scale/revised_v2/coverage/first_15_assets_2020_2025/P4_REVISED_FIRST15_COVERAGE_MANIFEST.json` | Draft | Aggregate machine-readable packet |
| Coverage Summary | `artifacts/evidence/p4_binance_scale/revised_v2/coverage/first_15_assets_2020_2025/P4_REVISED_FIRST15_COVERAGE_SUMMARY.md` | Draft | Aggregate summary |
| P4 Label Artifacts | `artifacts/evidence/p4_binance_scale/revised_v2/coverage/first_15_assets_2020_2025/p4/labels/` | Draft | Label JSONL artifacts for 15 assets |
| Full-Window Datasets | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/full_windows/` | Draft | Full 2020-2025 symbol datasets |

**Outcome summary:**
- Collected revised plan sequence 1-1080 across batch 001-054.
- Batch failures: 0.
- Converted full 2020-01 through 2025-12 windows for 15 assets.
- Data quality status: `PASS` for all 15 assets.
- Daily bars: 2192 per asset.
- Valid post-warmup P4 labeled weeks: 157 per asset.
- Passing assets: 15/15.
- Aggregate P4 coverage candidate has `gate_evidence_complete=true`.
- Gate claim remains disabled pending human review.
- Next task is P0.7-016: P4 Coverage Packet Review.

### P0.7-014 — Revised P4 Batch 002 Collection (2026-05-05)

**Trigger:** P0.7-013 converted the first revised BTCUSDT batch, leaving the
second controlled revised collection batch as the next step.
**Type:** Evidence collection.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Revised P4 Batch 002 Collection | `products/entropy-core/docs/audit/P4_REVISED_BATCH_002_COLLECTION.md` | Draft | Records batch 002 result and no-claim boundary |
| Batch Manifest | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_002/P4_BATCH_002_MANIFEST.json` | Draft | Source hashes/statuses for 20 files |
| Batch Summary | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_002/P4_REVISED_BATCH_002_SUMMARY.md` | Draft | Human-readable batch summary |

**Outcome summary:**
- Downloaded revised plan sequence 21-40.
- Range: BTCUSDT 2021-09 through 2023-04.
- Requested 20, done 20, failed 0.
- Gate claim remains disabled.
- Next task is P0.7-015: Revised P4 BTCUSDT Batch 002 Conversion.

### P0.7-013 — Revised P4 BTCUSDT Batch 001 Conversion (2026-05-05)

**Trigger:** P0.7-012 collected revised batch 001, leaving conversion and
quality/P4 checks as the next control point before more collection.
**Type:** Evidence conversion.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Revised P4 Batch 001 Conversion | `products/entropy-core/docs/audit/P4_REVISED_BATCH_001_CONVERSION.md` | Draft | Records conversion result and no-claim boundary |
| Conversion Manifest | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/batch_001/P4_BATCH_001_CONVERSION_MANIFEST.json` | Draft | Dataset hash, quality status, P4 summary pointers |
| Conversion Summary | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/batch_001/P4_REVISED_BATCH_001_CONVERSION_SUMMARY.md` | Draft | Human-readable conversion summary |
| Merged Dataset | `artifacts/evidence/p4_binance_scale/revised_v2/conversions/batch_001/datasets/BTCUSDT-1d-batch_001.parquet` | Draft | 609 BTCUSDT daily bars |

**Outcome summary:**
- Converted BTCUSDT 2020-01 through 2021-08 into one partial Parquet dataset.
- Dataset hash:
  `e7e26e022c849317f5266333d3dd3a40570bf0e4e2919ee1850c55f3296af354`.
- Data quality status is `PASS`.
- Partial P4 output generated 86 weekly labels and 0 valid post-warmup labeled
  weeks.
- Gate claim remains disabled.
- Next task is P0.7-014: Revised P4 Batch 002 Collection.

### P0.7-012 — Revised P4 Batch 001 Collection (2026-05-05)

**Trigger:** P0.7-011 created the revised 1440-file scale plan, leaving the
first controlled revised collection batch as the next step.
**Type:** Evidence collection.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Revised P4 Batch 001 Collection | `products/entropy-core/docs/audit/P4_REVISED_BATCH_001_COLLECTION.md` | Draft | Records batch 001 result and no-claim boundary |
| Batch Manifest | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_001/P4_BATCH_001_MANIFEST.json` | Draft | Source hashes/statuses for 20 files |
| Batch Summary | `artifacts/evidence/p4_binance_scale/revised_v2/batches/batch_001/P4_REVISED_BATCH_001_SUMMARY.md` | Draft | Human-readable batch summary |

**Outcome summary:**
- Downloaded revised plan sequence 1-20.
- Range: BTCUSDT 2020-01 through 2021-08.
- Requested 20, done 20, failed 0.
- Gate claim remains disabled.
- Next task is P0.7-013: Revised P4 BTCUSDT Batch 001 Conversion.

### P0.7-011 — Revised P4 Scale Plan (2026-05-05)

**Trigger:** P0.7-010 created `PHASE0-CRYPTO-P4-20-v2`, leaving the revised
2020-2025 download matrix as the next step before collection resumes.
**Type:** Evidence scale plan.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Revised P4 Scale Plan Decision | `products/entropy-core/docs/audit/P4_REVISED_SCALE_PLAN_DECISION.md` | Draft | Summary of revised matrix |
| Revised P4 Coverage Scale Plan | `products/entropy-core/docs/audit/P4_REVISED_COVERAGE_SCALE_PLAN.md` | Draft | 1440 planned downloads and resume policy |
| Revised P4 Coverage Scale Manifest | `products/entropy-core/docs/audit/P4_REVISED_COVERAGE_SCALE_MANIFEST.json` | Draft | Machine-readable revised matrix |
| P4 Scale Plan Module | `entropy/evidence/p4_scale_plan.py` | Draft | Adds revised plan ID support |

**Outcome summary:**
- Created `P4-BINANCE-REVISED-SCALE-PLAN-v1`.
- Plan hash:
  `f8902894d1b712c19784c7fd8b2ffb6dcaa52a34100b8e64815fe19a9692ee2f`.
- Planned matrix is 20 revised-universe assets x 72 months, 2020-01 through
  2025-12.
- Planned downloads: 1440 monthly Binance `1d` archive files.
- Batch size: 20 files.
- Gate claim remains disabled.
- Next task is P0.7-012: Revised P4 Batch 001 Collection.

### P0.7-010 — P4 Universe Revision Decision (2026-05-05)

**Trigger:** P0.7-009 showed current universe insufficiency and enough eligible
legacy replacements.
**Type:** Strategy decision and universe snapshot.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 Universe Revision Decision | `products/entropy-core/docs/audit/P4_UNIVERSE_REVISION_DECISION.md` | Draft | Decision rationale and replacement map |
| Revised P4 Universe Snapshot | `products/entropy-core/docs/audit/P4_REVISED_CRYPTO_UNIVERSE_SNAPSHOT.md` | Draft | `PHASE0-CRYPTO-P4-20-v2` snapshot |
| Crypto Universe Module | `entropy/evidence/crypto_universe.py` | Draft | Adds revised P4 universe getter |

**Outcome summary:**
- Created `PHASE0-CRYPTO-P4-20-v2`.
- Revised universe hash:
  `298fd0d4cb59dc7f94db12f61bc9cacb9915c59ba35a9be94f470f0e5b39f594`.
- Retained 13 eligible current assets.
- Replaced 7 late-listed assets with eligible legacy candidates.
- P4 label semantics remain unchanged.
- Next task is P0.7-011: Revised P4 Scale Plan.

### P0.7-009 — P4 Extended History Eligibility Probe (2026-05-05)

**Trigger:** P0.7-008 selected an approved-source history eligibility probe
before regenerating any broad P4 download matrix.
**Type:** Evidence probe.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 Extended History Eligibility Probe | `products/entropy-core/docs/audit/P4_EXTENDED_HISTORY_ELIGIBILITY_PROBE.md` | Draft | Current universe and legacy candidate probe summary |
| Current Universe Probe Manifest | `artifacts/evidence/p4_binance_scale/history_probe_2020_2025/P4_HISTORY_ELIGIBILITY_PROBE_MANIFEST.json` | Draft | HEAD-only availability probe for `PHASE0-CRYPTO-20-v1` |
| Current Universe Probe Summary | `artifacts/evidence/p4_binance_scale/history_probe_2020_2025/P4_HISTORY_ELIGIBILITY_PROBE_SUMMARY.md` | Draft | Human-readable current universe result |
| Legacy Candidate Probe Manifest | `artifacts/evidence/p4_binance_scale/history_probe_legacy_candidates_2020_2025/P4_HISTORY_ELIGIBILITY_PROBE_MANIFEST.json` | Draft | HEAD-only availability probe for replacement candidates |
| P4 History Probe Module | `entropy/evidence/p4_history_probe.py` | Draft | Reproducible HEAD-only history probe tooling |

**Outcome summary:**
- Current `PHASE0-CRYPTO-20-v1` universe has 13/15 eligible assets.
- Ineligible current assets: SOLUSDT, AVAXUSDT, DOTUSDT, UNIUSDT, AAVEUSDT,
  NEARUSDT, FILUSDT.
- Legacy candidate probe found 11/12 eligible candidates.
- Finding: preserve P4 label semantics and revise universe composition before
  regenerating a broad download matrix.
- Next task is P0.7-010: P4 Universe Revision Decision.

### P0.7-008 — P4 Coverage Window Strategy Decision (2026-05-05)

**Trigger:** P0.7-007 showed that the clean 2023-2025 BTCUSDT data path still
produces only 1 valid post-warmup P4 label against the encoded 156-label
requirement.
**Type:** Strategy decision.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 Coverage Window Strategy Decision | `products/entropy-core/docs/audit/P4_COVERAGE_WINDOW_STRATEGY_DECISION.md` | Draft | Stops broad 3-year collection and selects eligibility probe |

**Outcome summary:**
- Rejected continuing the broad 2023-2025 matrix.
- Rejected treating 156 generated labels as gate-sufficient without an explicit
  metric revision.
- Accepted next step: approved-source extended-history eligibility probe.
- Next task is P0.7-009: P4 Extended History Eligibility Probe.

### P0.7-007 — BTCUSDT Full-Window Conversion (2026-05-05)

**Trigger:** P0.7-006 completed the source archives needed for BTCUSDT
2023-01 through 2025-12, allowing a full planned-window conversion before
collecting more assets.
**Type:** Evidence conversion.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| BTCUSDT Full-Window Conversion | `products/entropy-core/docs/audit/P4_BTCUSDT_FULL_WINDOW_CONVERSION.md` | Draft | Records conversion result and strategic finding |
| Symbol Conversion Manifest | `artifacts/evidence/p4_binance_scale/conversions/full_windows/BTCUSDT_1d_2023_01_2025_12/BTCUSDT_1d_SYMBOL_CONVERSION_MANIFEST.json` | Draft | Dataset hash, quality status, P4 summary pointers |
| Symbol Conversion Summary | `artifacts/evidence/p4_binance_scale/conversions/full_windows/BTCUSDT_1d_2023_01_2025_12/BTCUSDT_1d_SYMBOL_CONVERSION_SUMMARY.md` | Draft | Human-readable symbol conversion summary |
| Full BTCUSDT Dataset | `artifacts/evidence/p4_binance_scale/conversions/full_windows/BTCUSDT_1d_2023_01_2025_12/datasets/BTCUSDT-1d-2023_01-2025_12.parquet` | Draft | 1096 BTCUSDT daily bars |
| P4 Symbol Conversion Module | `entropy/evidence/p4_batch_conversion.py` | Draft | Adds symbol-window conversion tooling |

**Outcome summary:**
- Converted BTCUSDT source sequences 1-36 into one full 2023-2025 dataset.
- Dataset hash:
  `15dd83aa0222f764247f535fbd5ac1c8c67cdd50770870f5fc9aa66dac0f4592`.
- Data quality status is `PASS`.
- P4 generated 156 weekly labels but only 1 valid post-warmup labeled week.
- Strategic finding: the current 3-year plan cannot satisfy the encoded 156
  valid post-warmup labeled-week requirement.
- Next task is P0.7-008: P4 Coverage Window Strategy Decision.

### P0.7-006 — P4 Batch 002 Collection (2026-05-05)

**Trigger:** P0.7-005 converted the first BTCUSDT batch and left continued
controlled source collection as the next step toward full P4 coverage.
**Type:** Evidence collection.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 Batch 002 Collection | `products/entropy-core/docs/audit/P4_BATCH_002_COLLECTION.md` | Draft | Records batch 002 result and no-claim boundary |
| Batch 002 Manifest | `artifacts/evidence/p4_binance_scale/batches/batch_002/P4_BATCH_002_MANIFEST.json` | Draft | Source hashes/statuses for 20 files |
| Batch 002 Summary | `artifacts/evidence/p4_binance_scale/batches/batch_002/P4_BATCH_002_SUMMARY.md` | Draft | Human-readable batch summary |
| P4 Scale Plan Module | `entropy/evidence/p4_scale_plan.py` | Draft | Adds deterministic `batch_items()` helper |

**Outcome summary:**
- Downloaded sequence 21-40.
- Range: BTCUSDT 2024-09 through 2025-12, then ETHUSDT 2023-01 through 2023-04.
- Requested 20, done 20, failed 0.
- Gate claim remains disabled.
- Next task is P0.7-007: BTCUSDT Full-Window Conversion.

### P0.7-005 — P4 First Batch Conversion (2026-05-05)

**Trigger:** P0.7-004 collected the first 20-file BTCUSDT source batch, leaving
conversion, dataset hashing, data-quality checks, and partial P4 output as the
next control point before further downloads.
**Type:** Evidence conversion.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 First Batch Conversion | `products/entropy-core/docs/audit/P4_FIRST_BATCH_CONVERSION.md` | Draft | Records conversion result and no-claim boundary |
| Conversion Manifest | `artifacts/evidence/p4_binance_scale/conversions/batch_001/P4_BATCH_001_CONVERSION_MANIFEST.json` | Draft | Dataset hash, quality status, P4 summary pointers |
| Conversion Summary | `artifacts/evidence/p4_binance_scale/conversions/batch_001/P4_BATCH_001_CONVERSION_SUMMARY.md` | Draft | Human-readable conversion summary |
| Merged Dataset | `artifacts/evidence/p4_binance_scale/conversions/batch_001/datasets/BTCUSDT-1d-batch_001.parquet` | Draft | 609 BTCUSDT daily bars |
| P4 Batch Conversion Module | `entropy/evidence/p4_batch_conversion.py` | Draft | Batch conversion and manifest tooling |

**Outcome summary:**
- Converted first 20 BTCUSDT monthly archives into one merged Parquet dataset.
- Dataset hash:
  `75dfbf9a9a41c2a374220da43cf12930a9c663f17a4aef2523944cc742744c65`.
- Data quality status is `PASS`.
- Partial P4 output generated 86 weekly labels and 0 valid post-warmup labeled
  weeks; gate claim remains disabled.
- Next task is P0.7-006: P4 Batch 002 Collection.

### P0.7-004 — P4 First Batch Collection (2026-05-05)

**Trigger:** P0.7-003 produced the deterministic 720-file scale plan, leaving
first-batch collection as the controlled next step.
**Type:** Evidence collection.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 First Batch Collection | `products/entropy-core/docs/audit/P4_FIRST_BATCH_COLLECTION.md` | Draft | Records first batch result |
| Batch Manifest | `artifacts/evidence/p4_binance_scale/batches/batch_001/P4_BATCH_001_MANIFEST.json` | Draft | Source hashes/statuses for 20 files |
| Batch Summary | `artifacts/evidence/p4_binance_scale/batches/batch_001/P4_BATCH_001_SUMMARY.md` | Draft | Human-readable batch summary |
| P4 Batch Collection Module | `entropy/evidence/p4_batch_collection.py` | Draft | Resumable batch collector |

**Outcome summary:**
- First 20 planned BTCUSDT monthly archives were downloaded.
- All 20 files completed with source SHA-256 recorded.
- Gate claim remains disabled.
- Next task is P0.7-005: P4 First Batch Conversion.

### P0.7-003 — P4 Coverage Scale Plan (2026-05-05)

**Trigger:** P0.7-002 proved the Binance OHLCV/P4 canary path, leaving scaled
collection planning before any full archive download.
**Type:** Evidence scale plan.
**Pipeline version:** Phase 0.7 free-source P4 evidence.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 Coverage Scale Plan | `products/entropy-core/docs/audit/P4_COVERAGE_SCALE_PLAN.md` | Draft | 720 planned downloads, resume policy, acceptance checks |
| P4 Coverage Scale Manifest | `products/entropy-core/docs/audit/P4_COVERAGE_SCALE_MANIFEST.json` | Draft | Machine-readable planned download matrix |
| P4 Scale Plan Module | `entropy/evidence/p4_scale_plan.py` | Draft | Deterministic plan builder |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.7-004 as next task |

**Outcome summary:**
- 20 assets x 36 months are planned for Binance `1d` monthly archives.
- Batch size is 20 files.
- Gate claim remains disabled.
- Next task is P0.7-004: P4 First Batch Collection.

### P0.7-002 — Binance P4 Canary Dataset (2026-05-05)

**Trigger:** P0.7-001 confirmed approved source reachability, leaving a tiny
hash-recorded OHLCV/P4 canary as the next evidence-bootstrap step.
**Type:** Evidence canary.
**Pipeline version:** Phase 0.7 free-source canary.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Binance P4 Canary | `products/entropy-core/docs/audit/BINANCE_P4_CANARY.md` | Draft | Records canary source hash, dataset hash, and P4 result |
| Canary Artifacts | `artifacts/evidence/binance_p4_canary/BTCUSDT_1d_2024_01/` | Draft | Raw zip, Parquet, manifest, summary, P4 labels |
| Binance Canary Module | `entropy/evidence/binance_canary.py` | Draft | Parser and canary runner |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.7-003 as next task |

**Outcome summary:**
- Approved Binance public archive canary downloaded and hashed.
- Data quality passed and P4 artifact tooling ran.
- Gate evidence remains incomplete by design.
- Next task is P0.7-003: P4 Coverage Scale Plan.

### P0.7-001 — Crypto Universe Snapshot And Source Manifest Bootstrap (2026-05-05)

**Trigger:** P0.6-HUMAN-001 approved limited free crypto sources, leaving a
target universe and source canary as the first evidence-bootstrap step.
**Type:** Evidence bootstrap.
**Pipeline version:** Phase 0.7 free-source canary.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Crypto Universe Snapshot | `products/entropy-core/docs/audit/CRYPTO_UNIVERSE_SNAPSHOT.md` | Draft | Records `PHASE0-CRYPTO-20-v1` and universe hash |
| Source Manifest Bootstrap | `products/entropy-core/docs/audit/SOURCE_MANIFEST_BOOTSTRAP.md` | Draft | Records canary PASS for approved public domains |
| Crypto Universe Module | `entropy/evidence/crypto_universe.py` | Draft | Machine-readable universe snapshot |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.7-002 as next task |

**Outcome summary:**
- 20-asset crypto universe snapshot recorded.
- Source canary passed for Binance public archive, Kraken public API, and
  Coinbase Exchange public API.
- No full evidence collection or gate claim was made.
- Next task is P0.7-002: Binance P4 Canary Dataset.

### P0.6-HUMAN-001 — Evidence Collection Authorization Review (2026-05-05)

**Trigger:** Human owner asked for the best no-budget reliable source set and
authorized proceeding.
**Type:** Human authorization and source-selection implementation.
**Pipeline version:** Phase 0.6 evidence authorization.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Evidence Collection Authorization | `products/entropy-core/docs/audit/EVIDENCE_COLLECTION_AUTHORIZATION.md` | Draft | Updated to `APPROVED_LIMITED_FREE_CRYPTO_SOURCES` |
| Evidence Source Selection | `products/entropy-core/docs/audit/EVIDENCE_SOURCE_SELECTION.md` | Draft | Records `FREE-CRYPTO-SOURCES-v1` rationale |
| Source Selection Module | `entropy/evidence/source_selection.py` | Draft | Machine-readable source/use-case/domain guards |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.7-001 as next task |

**Outcome summary:**
- Binance public archive selected as primary free OHLCV source.
- Kraken public API and Coinbase Exchange public API selected as free
  cross-check sources.
- Egress is limited to approved public domains.
- Paid APIs, authenticated broker APIs, trading, Phase 0 approval, Phase 1
  start, and performance claims remain blocked.
- Next task is P0.7-001: Crypto Universe Snapshot And Source Manifest
  Bootstrap.

### P0.6-008 — Evidence Collection Authorization Packet (2026-05-05)

**Trigger:** P0.6-007 completed data-stability monitoring tooling, leaving human
source/provider authorization as the blocker before real evidence collection.
**Type:** Authorization request packet.
**Pipeline version:** Phase 0.6 evidence implementation.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Evidence Collection Authorization | `products/entropy-core/docs/audit/EVIDENCE_COLLECTION_AUTHORIZATION.md` | Draft | Records `PENDING_HUMAN_APPROVAL` |
| Phase 0 Gate Packet | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | Sets P0.6-HUMAN-001 as next action |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.6-HUMAN-001 as next action |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to P0.6-008 packet |

**Outcome summary:**
- P4 coverage, SimBroker calibration, and data-stability evidence collection
  approval requirements are recorded.
- Provider activation, network egress, and real evidence collection remain
  blocked until human approval.
- Next action is P0.6-HUMAN-001: Evidence Collection Authorization Review.

### P0.6-007 — Data Stability Monitor Tooling (2026-05-05)

**Trigger:** P0.6-006 completed SimBroker calibration tooling, leaving
data-stability monitoring tooling as the next direct Phase 0 evidence-prep
blocker.
**Type:** Implementation tooling.
**Pipeline version:** Phase 0.6 evidence implementation.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Data Stability Plan | `products/entropy-core/docs/audit/DATA_STABILITY_PLAN.md` | Draft | Updated from plan-only to tooling-ready/evidence-missing |
| Phase 0 Gate Packet | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | Sets P0.6-008 as next task |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.6-008 as next task |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to P0.6-007 implementation evidence |

**Outcome summary:**
- Monitoring row validation, JSONL round-trip, and summary rendering are
  implemented without provider activation.
- Real >=90 continuous monitored days remain required before gate use.
- Next task is P0.6-008: Evidence Collection Authorization Packet.

### P0.6-006 — SimBroker Calibration Tooling (2026-05-05)

**Trigger:** P0.6-005 completed Harvey-Liu family tooling, leaving SimBroker
calibration tooling as the next direct Phase 0 evidence-prep blocker.
**Type:** Implementation tooling.
**Pipeline version:** Phase 0.6 evidence implementation.

| Artifact | File | Status | Notes |
|---|---|---|---|
| SimBroker Calibration Plan | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_PLAN.md` | Draft | Updated from plan-only to tooling-ready/evidence-missing |
| Phase 0 Gate Packet | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | Sets P0.6-007 as next task |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.6-007 as next task |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to P0.6-006 implementation evidence |

**Outcome summary:**
- Calibration row validation, JSONL round-trip, and summary rendering are
  implemented without provider activation.
- Real >=100 manually verified bid/ask rows remain required before gate use.
- Next task is P0.6-007: Data Stability Monitor Tooling.

### P0.6-005 — Harvey-Liu Family Workflow (2026-05-05)

**Trigger:** P0.6-004 completed Sharpe CI revision, leaving Harvey-Liu as the
next claim-blocking statistical helper.
**Type:** Implementation review.
**Pipeline version:** Phase 0.6 evidence implementation.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Harvey-Liu Review | `products/entropy-core/docs/audit/HARVEY_LIU_REVIEW.md` | Draft | Updated from blocked helper review to implementation-revised packet-required |
| Phase 0 Gate Packet | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | Sets P0.6-006 as next task |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.6-006 as next task |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to P0.6-005 implementation evidence |

**Outcome summary:**
- `HL-HB-v1` family-table workflow is implemented with Holm-Bonferroni
  adjustment and membership/hash guards.
- Legacy single-trial deflation remains provisional.
- Report/gate packet integration remains required before phase-exit proof.
- Next task is P0.6-006: SimBroker Calibration Tooling.

### P0.5-009 — Phase 0 Gate Packet (2026-05-05)

**Trigger:** P0.5-008 synchronized implementation-facing docs, completing the
Phase 0.5 closure tasks before a gate packet.
**Type:** Gate review.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Phase 0 Gate Packet | `products/entropy-core/docs/audit/PHASE0_GATE_PACKET.md` | Draft | Records Phase 0 NOT_APPROVED and Phase 0.6 reshape |
| Decision Log | `products/entropy-core/docs/DECISION_LOG.md` | Draft | D-025 recorded |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.6-001 as next task |

**Outcome summary:**
- T01-T24 remain accepted as implementation foundation.
- Phase 0 remains `NOT_APPROVED`.
- Phase 1 remains stop-shipped.
- Next stage is Phase 0.6 Evidence Implementation and Collection Prep.
- First next task is P0.6-001: P4 Labeler Implementation.

### P0.5-008 — Architecture And Spec Reality Sync (2026-05-05)

**Trigger:** P0.5-007 completed the data-stability plan, leaving
implementation-facing docs to be synchronized before the Phase 0 gate packet.
**Type:** Documentation sync.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Architecture | `products/entropy-core/docs/ARCHITECTURE.md` | Draft | Adds Phase 0.5 reality and provisional surfaces |
| Feature Spec | `products/entropy-core/docs/spec.md` | Draft | Adds gate-missing/provisional status |
| Task Graph | `products/entropy-core/docs/tasks.md` | Draft | Adds Phase 0.5 task graph |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to P0.5-008 |

**Outcome summary:**
- Implementation-facing docs now state that T01-T24 are complete but Phase 0 is
  not gate-approved.
- Hard evidence blockers remain visible.
- Next task is P0.5-009: Phase 0 Gate Packet.

### P0.5-007 — Data Pipeline Stability Plan (2026-05-05)

**Trigger:** P0.5-006 defined the SimBroker calibration plan, leaving the
90-day data feed monitoring criterion as the next direct evidence blocker.
**Type:** Evidence plan.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Data Stability Plan | `products/entropy-core/docs/audit/DATA_STABILITY_PLAN.md` | Draft | Defines future >=90 continuous days monitoring packet |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to the stability plan |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.5-008 as next task |

**Outcome summary:**
- Future monitoring rows, gap reason codes, acceptance packet, and failure
  handling are specified.
- No provider was activated.
- No 90-day stability evidence was produced.
- Next task is P0.5-008: Architecture And Spec Reality Sync.

### P0.5-006 — SimBroker Calibration Evidence Plan (2026-05-05)

**Trigger:** P0.5-005 selected the P4 implementation/evidence path, leaving
SimBroker bid/ask calibration as the next direct Phase 0 evidence blocker.
**Type:** Evidence plan.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| SimBroker Calibration Plan | `products/entropy-core/docs/audit/SIMBROKER_CALIBRATION_PLAN.md` | Draft | Defines future >=100 manually verified bid/ask fill evidence packet |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to the calibration plan |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.5-007 as next task |

**Outcome summary:**
- Future calibration rows, source approval requirements, acceptance calculation,
  and failure handling are specified.
- No provider was activated.
- No calibration evidence was produced.
- Next task is P0.5-007: Data Pipeline Stability Plan.

### P0.5-005 — P4 Labeler Gate Decision (2026-05-05)

**Trigger:** P4 labels are a direct Phase 0 exit criterion and P0.5-004 closed
the prior purge/embargo decision.
**Type:** Gate decision.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| P4 Gate Decision | `products/entropy-core/docs/audit/P4_GATE_DECISION.md` | Draft | Selects implementation/evidence path; no charter revision yet |
| Decision Log | `products/entropy-core/docs/DECISION_LOG.md` | Draft | D-024 recorded |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.5-006 as next task |

**Outcome summary:**
- Implement/evidence deterministic `P4-RBL-v1` before Phase 1.
- Algorithm text alone cannot close the Phase 0 P4 criterion.
- Required evidence remains >=3 years of 1D labels on >=15 of 20 target assets.
- Next task is P0.5-006: SimBroker Calibration Evidence Plan.

### P0.5-004 — Purge/Embargo Design Decision (2026-05-05)

**Trigger:** P0.5-002 ranked purge/embargo as a pre-Phase-1 blocker, and P0.5-003
closed the immediate statistical-helper review packets.
**Type:** Design decision.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Purge Embargo Decision | `products/entropy-core/docs/audit/PURGE_EMBARGO_DECISION.md` | Draft | Retains T18 embargo as scaffold only; blocks Phase 1 OOS claims until derived methodology exists |
| Decision Log | `products/entropy-core/docs/DECISION_LOG.md` | Draft | D-023 recorded |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.5-005 as next task |

**Outcome summary:**
- The current N-consecutive-bar embargo remains accepted for deterministic tests.
- It is not accepted as final Phase 1 OOS-claim methodology.
- Future closure must tie embargo to feature lookback, label horizon, holding
  period, bar frequency, calendar profile, and execution assumptions.
- Next task is P0.5-005: P4 Labeler Gate Decision.

### P0.5-003 — Sharpe CI And Harvey-Liu Review Packets (2026-05-05)

**Trigger:** P0.5-002 ranked Sharpe CI and Harvey-Liu as claim blockers that
must be reviewed before later evidence packets rely on statistical helper output.
**Type:** Formula review.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Sharpe CI Review | `products/entropy-core/docs/audit/SHARPE_CI_REVIEW.md` | Draft | `CI-SR-ACF-v1` requires revision before gate/report use |
| Harvey-Liu Review | `products/entropy-core/docs/audit/HARVEY_LIU_REVIEW.md` | Draft | `HL-HB-v1` is blocked for gate use |
| Decision Log | `products/entropy-core/docs/DECISION_LOG.md` | Draft | D-022 recorded |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.5-004 as next task |

**Outcome summary:**
- T23 statistical helpers remain provisional scaffolds only.
- `CI-SR-ACF-v1` lacks required autocorrelation/report fields for gate/report use.
- `HL-HB-v1` lacks family-table Holm-Bonferroni workflow and is blocked for
  gate use.
- Next task is P0.5-004: Purge/Embargo Design Decision.

### P0.5-002 — Formula And Evidence Debt Register (2026-05-05)

**Trigger:** P0.5-001 identified formula/evidence debt that can contaminate
Phase 0 gate packets and downstream performance claims.
**Type:** Documentation/audit debt register.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Formula Evidence Debt | `products/entropy-core/docs/audit/FORMULA_EVIDENCE_DEBT.md` | Draft | Ranks unresolved formula/evidence surfaces by gate impact |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to the debt register |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.5-003 as next task |

**Outcome summary:**
- Direct gate blockers: P4 labels, SimBroker calibration evidence, data
  stability evidence, and registered leakage/temporal-shuffling packet.
- Claim blockers: Sharpe CI and Harvey-Liu.
- Pre-Phase-1 blockers: purge/embargo and N_eff/K3 operational semantics.
- Future hard gates: F-30 RDL telemetry and F-31 K-report epoch coverage.
- Next task is P0.5-003: Sharpe CI And Harvey-Liu Review Packets.

### P0.5-001 — Phase 0 Exit Criteria Gap Register (2026-05-05)

**Trigger:** PSR-002 selected Phase 0.5 and required exact mapping between the
core Phase 0 exit criteria and current evidence.
**Type:** Documentation/audit gap register.
**Pipeline version:** Phase 0.5 foundation closure.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Exit Gap Register | `products/entropy-core/docs/audit/PHASE0_EXIT_GAP_REGISTER.md` | Draft | Maps each canonical exit criterion to evidence, gaps, owner, blocker status, and closure path |
| Evidence Index | `products/entropy-core/docs/EVIDENCE_INDEX.md` | Draft | Points to the gap register |
| Codex Prompt | `products/entropy-core/docs/CODEX_PROMPT.md` | Draft | Sets P0.5-002 as next task |

**Outcome summary:**
- Phase 0 gate remains `NOT_APPROVED`.
- Hard blockers remain for SimBroker calibration, 90-day data stability, P4
  labels or charter-level revision, and registered leakage/temporal-shuffling
  gate evidence.
- Trial Registry and P1 are implemented but still require final gate-packet
  evidence.
- Next task is P0.5-002: Formula And Evidence Debt Register.

### PSR-002 — Phase 0 Strategic Decision (2026-05-05)

**Trigger:** Post-T24 foundation is complete as implementation baseline, but
formal Phase 0 gate approval remains `NOT_APPROVED`.
**Type:** Strategic phase-direction decision.
**Pipeline version:** Post-T24 strategy remediation.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Strategic Decision | `products/entropy-core/docs/audit/PHASE0_STRATEGIC_DECISION.md` | Draft | Selects Phase 0.5 Foundation Closure and Evidence Hardening |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | Synchronized next blocker to P0.5-001 |
| Next Phase Plan | `products/entropy-core/docs/audit/NEXT_PHASE_PLAN.md` | Draft | Rewritten to Phase 0.5 task plan |
| Decision Log | `products/entropy-core/docs/DECISION_LOG.md` | Draft | D-021 recorded |

**Outcome summary:**
- T01-T24 are accepted as the implementation foundation baseline.
- Phase 0 gate remains `NOT_APPROVED`.
- Phase 1 remains stop-shipped.
- Next stage is Phase 0.5 Foundation Closure and Evidence Hardening.
- Next task is P0.5-001: Phase 0 Exit Criteria Gap Register.

### PSR-001 — Phase 0 Foundation Consolidated Review (2026-05-05)

**Trigger:** Post-phase strategy review found the canonical consolidated review
still reflected the Phase 8 boundary state after T23/T24 completion.
**Type:** Documentation/state consolidation.
**Pipeline version:** Post-T24 strategy remediation.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | Updated to current post-T24 Phase 0 foundation state |
| Phase 0 Foundation Review | `products/entropy-core/docs/audit/PHASE0_FOUNDATION_REVIEW.md` | Draft | Primary foundation checkpoint reference |
| Post-Phase Strategy Review | `products/entropy-core/docs/audit/POST_PHASE_STRATEGY_REVIEW.md` | Draft | Source of PSR-001/PSR-002 blockers |
| Next Phase Plan | `products/entropy-core/docs/audit/NEXT_PHASE_PLAN.md` | Draft | Recommends Phase 0 Closure and Hardening before Phase 1 |

**Outcome summary:**
- T01-T24 are complete and baseline is 135 passed with PostgreSQL 16.
- Phase 0 implementation foundation is complete.
- Phase gate remains `NOT_APPROVED` pending human review.
- No OOS performance claims, formula-validation claims, RDL/K-report closure
  claims, live-data claims, or live-capital claims were made.
- Harvey-Liu, Sharpe CI, N_eff/K3, purge/embargo, P4, F-30, and F-31 remain
  unresolved provisional surfaces.
- Next blocker is PSR-002: human Phase 0 foundation decision.

### Phase 2 Boundary Review (2026-05-03)

**Trigger:** Completion of Phase 2 core domain model tasks T04-T06.
**Type:** Scoped phase-boundary review.
**Pipeline version:** Orchestrator v2.0 scoped review.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Strategy Review | `products/entropy-core/docs/audit/STRATEGY_NOTE.md` | Draft | Proceed to T07; D-010 blocks T08 |
| Architecture Review | `products/entropy-core/docs/audit/ARCH_REPORT.md` | Draft | No new architecture findings |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | No P0/P1; no new P2 |
| Archived Phase Review | `products/entropy-core/docs/audit/PHASE2_REVIEW.md` | Draft | Phase 2 boundary archive |

**Outcome summary:**
- Phase 2 domain models completed and verified locally.
- P2-03 closed by correcting `get_tracer()` return type.
- T07 may proceed. T08 remains blocked by D-010 until the named protocol-level P0 findings are closed or waived.

### Phase 3 Boundary Review (2026-05-03)

**Trigger:** Completion of Phase 3 database schema and hashing tasks T07-T08.
**Type:** Scoped phase-boundary review.
**Pipeline version:** Orchestrator v2.0 scoped review.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Strategy Review | `products/entropy-core/docs/audit/STRATEGY_NOTE.md` | Draft | Proceed to T09 |
| Architecture Review | `products/entropy-core/docs/audit/ARCH_REPORT.md` | Draft | No new architecture findings |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | No P0/P1; no new P2 |
| Archived Phase Review | `products/entropy-core/docs/audit/PHASE3_REVIEW.md` | Draft | Phase 3 boundary archive |

**Outcome summary:**
- Phase 3 schema and hashing infrastructure completed and verified locally.
- T08 completed under D-011 narrow waiver as non-formula infrastructure.
- T09 may proceed. D-010 remains active for formula-bearing future tasks T15, T21, T22, and T23.

### Phase 4 Boundary Review (2026-05-03)

**Trigger:** Completion of Phase 4 Trial Registry tasks T09-T11.
**Type:** Scoped phase-boundary review.
**Pipeline version:** Orchestrator v2.0 scoped review.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Strategy Review | `products/entropy-core/docs/audit/STRATEGY_NOTE.md` | Draft | Proceed to T12 |
| Architecture Review | `products/entropy-core/docs/audit/ARCH_REPORT.md` | Draft | No new architecture findings |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | No P0/P1; no new P2 |
| Archived Phase Review | `products/entropy-core/docs/audit/PHASE4_REVIEW.md` | Draft | Phase 4 boundary archive |

**Outcome summary:**
- Phase 4 registry write/read/gate paths completed and verified locally.
- T12 may proceed. D-010 remains active for formula-bearing future tasks T15, T21, T22, and T23.

### Phase 5 Boundary Review (2026-05-03)

**Trigger:** Completion of Phase 5 Data Pipeline tasks T12-T14.
**Type:** Scoped phase-boundary review.
**Pipeline version:** Orchestrator v2.0 scoped review.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Strategy Review | `products/entropy-core/docs/audit/STRATEGY_NOTE.md` | Draft | T15 blocked by D-010 |
| Architecture Review | `products/entropy-core/docs/audit/ARCH_REPORT.md` | Draft | No new architecture findings |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | No P0/P1; no new P2 |
| Archived Phase Review | `products/entropy-core/docs/audit/PHASE5_REVIEW.md` | Draft | Phase 5 boundary archive |

**Outcome summary:**
- Phase 5 provider boundary, local fixture adapter, Parquet store, provenance table, and data quality checks completed and verified locally.
- T15 is formula-bearing and remains blocked by D-010 until the named protocol-level P0 findings are closed or an explicit T15 waiver is recorded.

### Phase 6 Boundary Review (2026-05-03)

**Trigger:** Completion of Phase 6 SimBroker tasks T15-T17.
**Type:** Scoped phase-boundary review.
**Pipeline version:** Orchestrator v2.0 scoped review.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Archived Phase Review | `products/entropy-core/docs/audit/PHASE6_REVIEW.md` | Draft | Phase 6 boundary archive |

**Outcome summary:**
- Phase 6 cost model, fill engine, and calibration interface completed and verified locally.
- No new open P0/P1/P2 findings.
- F-30/F-31 remain future real-evidence gates and were not closed synthetically.

### Phase 7 Boundary Review (2026-05-03)

**Trigger:** Completion of Phase 7 walk-forward tasks T18-T20 and user-requested gap review for phases without prior deep review.
**Type:** Scoped phase-boundary review with remediation.
**Pipeline version:** Orchestrator v2.0 scoped review.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Strategy Review | `products/entropy-core/docs/audit/STRATEGY_NOTE.md` | Draft | T21 governance disposition required |
| Architecture Review | `products/entropy-core/docs/audit/ARCH_REPORT.md` | Draft | One P1 review issue remediated |
| Consolidated Review | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | Stop-ship for direct T21 implementation |
| Archived Phase Review | `products/entropy-core/docs/audit/PHASE7_REVIEW.md` | Draft | Phase 7 boundary archive |

**Outcome summary:**
- Phase 7 splitter, leakage checklist, and runner completed and verified locally.
- Review found WF-P1-01: omitted T19 detectors could return PASS and allow a formal leakage gate without detector-backed evidence.
- WF-P1-01 was remediated during review; missing detectors now FAIL and T20 blocks failed checks before OOS.
- Baseline after remediation: 112 passed with PostgreSQL 16; ruff and pyright pass.
- T21 remains stopped until a T21-specific formula-governance disposition is recorded.

### T21 Formula-Governance Disposition (2026-05-03)

**Trigger:** User approval to proceed with the next governance step after Phase 7 review stop-shipped direct T21 implementation.
**Type:** Task-specific formula-governance disposition.
**Pipeline version:** Orchestrator v2.0 scoped disposition.

| Artifact | File | Status | Notes |
|---|---|---|---|
| Formula-Governance Disposition | `products/entropy-core/docs/audit/T21_FORMULA_GOVERNANCE_DISPOSITION.md` | Draft | D-017 |

**Outcome summary:**
- T21 may proceed under D-017's narrow scope.
- T21 must not implement Sharpe CI, Harvey-Liu, N_eff/K3, IC/BR, P4, K-report, RDL promotion, phase-exit logic, or OOS performance-claim artifacts.
- TASK-AF-022/F-22 is closed for current canonical implementation scope.

### Cycle 1 — Phase 0 Partial Rerun (2026-03-04, post-spec v1.4)

**Trigger:** Partial rerun after remediation batch in `PROTOCOL_SPEC.md` v1.4 and governance doc synchronization (`workflow_ai_development.md`, `review_pipeline.md`, `tasks.md`, audience briefs, README).
**Type:** Partial pipeline run (Step 3+4+5+6 review delta; no Step 1/2 regeneration).
**Pipeline version:** v1.0
**Spec context:** PROTOCOL_SPEC.md v1.4; CHARTER.md v5.1

| Artifact | File | Status | Notes |
|---|---|---|---|
| Consolidated Review (delta) | `products/entropy-core/docs/audit/REVIEW_REPORT.md` | Draft | Updated with partial rerun delta section; blockers remain |

**Outcome summary:**
- Determinism and governance clarifications integrated in spec/workflow/pipeline docs, with CHARTER/GLOSSARY synchronized.
- Added v1.4 policy baseline for RDL promotion queue and reporting-only epoch tags for RBE transparency.
- P0 blockers remain open for unresolved formula-level artifacts and runtime evidence (HL full package, P4 annex reproducibility, queue telemetry, epoch-tag coverage).

### Cycle 1 — Phase 0 Full Pipeline Run (2026-03-04)

**Trigger:** First formal full-pipeline run in pre-development Phase 0 (after orchestration setup).
**Type:** Full pipeline run (Steps 1–6 completed).
**Pipeline version:** v1.0
**Spec context:** PROTOCOL_SPEC.md v1.2; CHARTER.md v5.0

| Artifact | Versioned File (intended) | Status |
|---|---|---|
| Meta Investigation | `2026-03-04_phase0_META_ANALYSIS_v2.md` | Draft |
| Architecture Review | `2026-03-04_phase0_ARCH_MODEL_v2.md` | Draft |
| Invariant Extraction | `2026-03-04_phase0_INVARIANTS_v2.md` | Draft |
| Drift Assertions | `2026-03-04_phase0_DRIFT_ASSERTIONS_v2.md` | Draft |
| Drift Report | `2026-03-04_phase0_DRIFT_REPORT_v2.md` | Draft |
| Adversarial Review | `2026-03-04_phase0_ADVERSARIAL_REVIEW_v2.md` | Draft |
| Consolidated Review | `2026-03-04_phase0_REVIEW_REPORT_v2.md` | Draft |

**Open findings from this cycle:** 32 total (P0: 10, P1: 10, P2: 12) — see `products/entropy-core/docs/audit/REVIEW_REPORT.md`.
**Spec Owner sign-off:** Pending.
**Next action:** Spec Owner acceptance, then targeted remediation and partial reruns (Step 3+4+5+6) after each P0/P1 clarification set.
**Mandatory remediation set linkage:** `products/entropy-core/docs/tasks.md` must include and track `TASK-AF-022` through `TASK-AF-032` (Cycle 1 additions from `REVIEW_REPORT.md`) before phase-gate readiness review.

### Cycle 1 — Phase 0, First Formal Run Setup (2026-03-04)

**Trigger:** Meta Orchestration run to prepare Cycle 1 pipeline prompts and question pool. Spec-of-record: PROTOCOL_SPEC.md v1.2 (added RDL + Growth Layer since Cycle 0 source audit). All 21 Cycle 0 findings remain Open.
**Type:** Orchestration setup (pre-execution). Steps 1–6 not yet executed.
**Pipeline version:** v1.0
**Spec context:** PROTOCOL_SPEC.md v1.2 (Growth Layer added v1.1; RDL added v1.2; both post-date AUDIT_v1.md)

| Artifact | Versioned File (intended) | Status | Notes |
|---|---|---|---|
| Cycle Entrypoint | `2026-03-04_phase0_PROMPT_0_META_v1.md` | Draft | State snapshot; 18 risk surfaces identified |
| Step 2 Prompt | `2026-03-04_phase0_PROMPT_1_ARCH_REVIEW_v1.md` | Draft | Ready for execution |
| Step 3 Prompt | `2026-03-04_phase0_PROMPT_2_INVARIANTS_v1.md` | Draft | Ready for execution |
| Step 4 Prompt | `2026-03-04_phase0_PROMPT_3_DRIFT_GUARD_v1.md` | Draft | Ready for execution |
| Step 5 Prompt | `2026-03-04_phase0_PROMPT_4_ADVERSARIAL_v1.md` | Draft | Ready for execution |
| Step 6 Prompt | `2026-03-04_phase0_PROMPT_5_CONSOLIDATED_v1.md` | Draft | Ready for execution |
| Research Questions | `2026-03-04_phase0_QUESTION_POOL_v1.md` | Draft | 25 top-priority + 25 secondary questions |

**Pipeline artifacts (pending execution):**

When Cycle 1 pipeline runs complete, the Step 6 agent will register these versioned snapshot filenames:

| Artifact | Versioned File (intended) | Status |
|---|---|---|
| Meta Investigation | `2026-03-04_phase0_META_ANALYSIS_v2.md` | Pending Step 1 execution |
| Architecture Review | `2026-03-04_phase0_ARCH_MODEL_v2.md` | Pending Step 2 execution |
| Invariant Extraction | `2026-03-04_phase0_INVARIANTS_v2.md` | Pending Step 3 execution |
| Drift Assertions | `2026-03-04_phase0_DRIFT_ASSERTIONS_v2.md` | Pending Step 4 execution |
| Drift Report | `2026-03-04_phase0_DRIFT_REPORT_v2.md` | Pending Step 4 execution |
| Adversarial Review | `2026-03-04_phase0_ADVERSARIAL_REVIEW_v2.md` | Pending Step 5 execution |
| Consolidated Review | `2026-03-04_phase0_REVIEW_REPORT_v2.md` | Pending Step 6 execution |

(v2 because Cycle 0 produced REVIEW_REPORT_v1; other artifacts are first-time outputs in this phase but use v2 for phase-consistent numbering.)

**New risk surfaces identified this cycle (not in AUDIT_v1.md):**
- RS-11: Growth Layer RBE activation pathway unaudited
- RS-12: RDL trial budget inflation (trial counting from submission)
- RS-13: RDL phase boundary auditability gap
- RS-14: New modules vs. frozen non-negotiables (NN-1 through NN-6)
- RS-15: RBE + kill criteria interaction

**Spec Owner sign-off:** Pending.

**Next action:** Execute Cycle 1 pipeline Steps 1–6 in order. Begin with Step 1 (META_ANALYSIS.md) before executing PROMPT_1_ARCH_REVIEW.md.

---

### Cycle 0 — Phase 0 Baseline (2026-03-04)

**Trigger:** Initial governance setup — baseline consolidation of `products/entropy-core/docs/audit/AUDIT_v1.md`.
**Type:** Baseline (pre-pipeline). Steps 1–5 not yet executed.
**Pipeline version:** v1.0

| Artifact | Versioned File | Status | Notes |
|---|---|---|---|
| Consolidated Review | `2026-03-04_phase0_REVIEW_REPORT_v1.md` | Draft | Baseline from AUDIT_v1.md. Steps 1–5 outputs pending. |
| Source Audit | `products/entropy-core/docs/audit/AUDIT_v1.md` | Accepted | Primary input for baseline REVIEW_REPORT. External auditor document. 21 findings, all Open. |

**Spec Owner sign-off:** Pending.

**Next full-pipeline run:** Before Phase 0 → Phase 1 gate. All six steps must run in sequence. Orchestration prompts now available in Cycle 1 artifacts.

---

### Cycle N — Template (copy for each future cycle)

**Trigger:** [phase transition / spec revision / annual cadence / kill criterion fire]
**Type:** Full pipeline run / Partial run (Step N)
**Pipeline version:** v1.0

| Artifact | Versioned File | Status |
|---|---|---|
| Meta Investigation | `YYYY-MM-DD_phaseX_META_ANALYSIS_vN.md` | Draft |
| Architecture Review | `YYYY-MM-DD_phaseX_ARCH_MODEL_vN.md` | Draft |
| Invariant Extraction | `YYYY-MM-DD_phaseX_INVARIANTS_vN.md` | Draft |
| Drift Assertions | `YYYY-MM-DD_phaseX_DRIFT_ASSERTIONS_vN.md` | Draft |
| Drift Report | `YYYY-MM-DD_phaseX_DRIFT_REPORT_vN.md` | Draft |
| Adversarial Review | `YYYY-MM-DD_phaseX_ADVERSARIAL_REVIEW_vN.md` | Draft |
| Consolidated Review | `YYYY-MM-DD_phaseX_REVIEW_REPORT_vN.md` | Draft |

**Spec Owner sign-off:** [Pending / Accepted on YYYY-MM-DD]
**Open findings from this cycle:** [link to tasks.md entries]

---

## Rules

1. Every full-pipeline cycle produces versioned snapshots of all seven artifacts before overwriting canonicals.
2. Versioned snapshots are permanent. Do not delete them.
3. Status transitions from Draft to Accepted require written Spec Owner sign-off in this file.
4. A new phase cannot begin (phase gate) until the REVIEW_REPORT for the current phase is Accepted.
5. Partial-run artifacts do not supersede canonical artifacts; they are addenda until Step 6 is re-run.
6. This index must be updated by the Step 6 agent as part of every pipeline run.
7. Orchestration prompts (PROMPT_0 through PROMPT_5, QUESTION_POOL) must be regenerated at the start of each new cycle if: (a) the spec-of-record has changed, or (b) new risk surfaces have been identified since the last orchestration run.

---

*Version: 1.7 | Date: 2026-05-05 | Updated: Registered PSR-002 strategic decision and Phase 0.5 next-stage plan.*
