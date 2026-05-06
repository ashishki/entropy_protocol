# Entropy Protocol — Meta Orchestration Prompt (Cycle Entrypoint)

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/PROMPT_0_META.md`
**Cycle:** Cycle 5 — Phase 1D-K Archive-Only Baseline Deep Review
**Date:** 2026-05-06
**Owner:** Spec Owner / Staff-Level Systems Architect
**Pipeline Version:** v1.0
**Role:** Stable entrypoint for the Phase 1D-K deep protocol review. Read
this first before running any pipeline step.

---

## How to Use This File

This file is the mandatory starting context for the current audit pipeline run.
It contains:

1. **Cycle Context** — current state snapshot and deltas
2. **Risk Surface Register** — current review focus areas
3. **Downstream Prompt Index** — which prompts to run in which order

Before running any downstream prompt, load:

1. `docs/README.md`
2. `docs/core/GLOSSARY.md`
3. `docs/audit/review_pipeline.md`
4. `docs/audit/AUDIT_INDEX.md`
5. This file (`docs/audit/PROMPT_0_META.md`)

Then run downstream prompts in step order:

1. `PROMPT_1_ARCH_REVIEW.md`
2. `PROMPT_2_INVARIANTS.md`
3. `PROMPT_3_DRIFT_GUARD.md`
4. `PROMPT_4_ADVERSARIAL.md`
5. `PROMPT_5_CONSOLIDATED.md`

Each step must complete and write its artifact before the next step begins.

---

## Cycle Context (State Snapshot — 2026-05-06)

### Spec-of-Record

| Document | Version | Date | Status |
|---|---|---|---|
| `docs/core/PROTOCOL_SPEC.md` | v1.8 | 2026-05-03 | Active |
| `docs/core/CHARTER.md` | v5.3 | 2026-05-03 | Active |
| `docs/core/GLOSSARY.md` | v1.4 | 2026-05-03 | Active |
| `docs/ARCHITECTURE.md` | v1.0 | 2026-05-01 | Active |
| `docs/spec.md` | v1.0 | 2026-05-01 | Active |
| `docs/IMPLEMENTATION_CONTRACT.md` | v1.0 | 2026-05-01 | Immutable without ADR |
| `docs/audit/review_pipeline.md` | v1.0 | current | Active pipeline mechanics |

Canonical authority comes from the protocol, architecture, feature spec, and
implementation contract files above. `DECISION_LOG.md`,
`IMPLEMENTATION_JOURNAL.md`, and `EVIDENCE_INDEX.md` are retrieval surfaces, not
authorities.

### Existing Audit Artifacts

| Artifact | File | Status | Notes |
|---|---|---|---|
| Current consolidated review | `docs/audit/REVIEW_REPORT.md` | Draft | Cycle 5 D-K deep review status |
| Meta Investigation | `docs/audit/META_ANALYSIS.md` | Existing | Refresh in this cycle |
| Architecture Review | `docs/audit/ARCH_MODEL.md` | Existing | Refresh in this cycle |
| Invariant Extraction | `docs/audit/INVARIANTS.md` | Existing | Refresh in this cycle |
| Drift Assertions | `docs/audit/DRIFT_ASSERTIONS.md` | Existing | Refresh in this cycle |
| Drift Report | `docs/audit/DRIFT_REPORT.md` | Existing | Refresh in this cycle |
| Adversarial Review | `docs/audit/ADVERSARIAL_REVIEW.md` | Existing | Refresh in this cycle |
| Phase 1A closure | `docs/audit/archive/phase1a/PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md` | Complete | Scaffold/probe chain closed; no evaluation approval |
| Post-Phase-1A strategy | `docs/audit/archive/phase1a/POST_PHASE1A_STRATEGY_REVIEW.md` | Complete | Selects audit-readiness and deep review as next stage |

**Summary:** This cycle runs after the Phase 1D-K archive-only baseline path was
implemented and light-reviewed phase by phase. The D-K block is not production,
capital-ready, or phase-gate evidence. Phase 1 trading, live feeds, broker
integration, Growth/RDL/RBE activation, performance/OOS claims, and holdout
reads remain unapproved.

### Delta Since Prior Full Audit

1. P1D defined the long-only implementation contract and separate P1E approval
   guard.
2. P1E implemented bounded formation-only baseline observations for registered
   skill families.
3. P1F added deterministic hash binding and preregistration payload surfaces.
4. P1G added the governed evaluation configuration contract and approval guard.
5. P1H emitted first archive-only governed run metadata with no performance
   conclusion.
6. P1I/P1J/P1K packaged the report, no-holdout research decision, and
   archive-only closure packet.

### Current Phase Hypothesis

**Phase 1D-K Archive-Only Baseline Deep Review**

- Current task: full D-K deep review
- Last completed task: `P1K-HUMAN-001 Research Phase Closure Decision`
- Immediate review focus: P1F reproducibility, P1I report semantics, and prompt
  current-state metadata
- Not approved: Phase 1 evaluation/trading, holdout reads, live feeds,
  Growth/RDL/RBE activation, non-Python runtime/toolchain introduction, or
  OOS/performance claims

---

## Risk Surface Register

The following risk surfaces are ranked for the D-K review. Downstream
prompts should create findings only when current documents or code evidence
support them.

### TIER-1: Claim And Phase-Gate Containment

**RS-01 — Evaluation/Claim Creep**
- Why now: P1H and P1I create evaluation-run metadata and report packets. A
  downstream review must ensure these cannot be mistaken for OOS evidence,
  validated alpha, phase-gate evidence, production status, or capital readiness.
- Evidence: `entropy/baseline/governed.py`, `entropy/baseline/report.py`,
  `docs/tasks.md`, `REVIEW_REPORT.md`

**RS-02 — Holdout Boundary Integrity**
- Why now: The archive freeze and registration boundary encode formation,
  validation, and holdout labels. The holdout must remain locked until a
  separate approved gate exists.
- Evidence: `archive/phase1a/PHASE1A_REGISTRATION_BOUNDARY_PACKET.md`,
  `archive/phase1a/PHASE1A_BASELINE_REGISTRATION_PACKET.md`,
  `archive/phase1a/PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md`

**RS-03 — No-Claim Report Semantics**
- Why now: P1I emits report metadata. Field inventory must not be read as
  computed performance statistics or phase-gate evidence.
- Evidence: `entropy/baseline/report.py`, `tests/unit/test_phase1i_j_k_packets.py`

### TIER-2: Architecture And Runtime Drift

**RS-04 — Runtime Escalation Drift**
- Why now: Phase 1A explicitly considered high-load simulation concerns.
  Python remains the control plane and Polars/DuckDB/Arrow remain the data
  plane unless a benchmark miss and ADR justify escalation.
- Evidence: `ARCHITECTURE.md`, `IMPLEMENTATION_CONTRACT.md`,
  `archive/phase1a/PHASE1A_DEVELOPMENT_STRATEGY.md`,
  `archive/phase1a/PHASE1A_WORKLOAD_BENCHMARK_CONTRACT.md`

**RS-05 — Storage Boundary Drift**
- Why now: Benchmarks and future evaluation planning must not move large
  intermediates into PostgreSQL or create mutable untracked data stores.
- Evidence: `ARCHITECTURE.md`,
  `archive/phase1a/PHASE1A_WORKLOAD_BENCHMARK_CONTRACT.md`

### TIER-3: Dormant Module And Governance Boundaries

**RS-06 — Growth/RBE Activation Leakage**
- Why now: Phase 1A documents Growth monitoring-only scope but does not approve
  Growth instrumentation, RBE activation, or portfolio influence.
- Evidence: `PROTOCOL_SPEC.md`, `archive/phase1a/PHASE1A_ARCHIVE_ENTRY_CONTRACT.md`,
  `REVIEW_REPORT.md`

**RS-07 — RDL Dormancy Leakage**
- Why now: RDL must remain dormant/scaffolding-only through Phase 0-1 unless a
  future approved phase changes the boundary.
- Evidence: `PROTOCOL_SPEC.md`, `GLOSSARY.md`,
  `archive/phase1a/PHASE1A_ARCHIVE_ENTRY_CONTRACT.md`

### TIER-4: Audit Pipeline Integrity

**RS-08 — Prompt Metadata Drift**
- Why now: D-K became the current review state after P1K closure. Prompt headers
  and current-cycle context must match that state.
- Evidence: `AUDIT_INDEX.md`, `REVIEW_REPORT.md`

**RS-09 — Archive Loading Discipline**
- Why now: Historical audit files are archived. The next review should load
  compact indexes first and open archive files only when evidence requires it.
- Evidence: `AUDIT_INDEX.md`, `docs/audit/README.md`

---

## Downstream Prompt Index

| Step | Prompt File | Output Artifact | Reads (required) |
|---|---|---|---|
| Step 1 (Meta) | `docs/audit/PROMPT_0_META.md` + `review_pipeline.md` | `docs/audit/META_ANALYSIS.md` | Current docs, audit index, review report, Phase 1A packets |
| Step 2 (Architecture) | `docs/audit/PROMPT_1_ARCH_REVIEW.md` | `docs/audit/ARCH_MODEL.md` | META_ANALYSIS.md + canonical docs |
| Step 3 (Invariants) | `docs/audit/PROMPT_2_INVARIANTS.md` | `docs/audit/INVARIANTS.md` | ARCH_MODEL.md + canonical docs |
| Step 4 (Drift) | `docs/audit/PROMPT_3_DRIFT_GUARD.md` | `DRIFT_ASSERTIONS.md` + `DRIFT_REPORT.md` | INVARIANTS.md + current docs |
| Step 5 (Adversarial) | `docs/audit/PROMPT_4_ADVERSARIAL.md` | `docs/audit/ADVERSARIAL_REVIEW.md` | ARCH_MODEL + INVARIANTS + DRIFT_REPORT + canonical docs |
| Step 6 (Consolidated) | `docs/audit/PROMPT_5_CONSOLIDATED.md` | `docs/audit/REVIEW_REPORT.md` | all prior artifacts + tasks.md + AUDIT_INDEX.md |

---

## Hard Constraints (enforced in all downstream prompts)

1. No changes to frozen non-negotiables, kill criteria, phase exit criteria, or
   metric thresholds.
2. Research-only; no live portfolio influence at any stage.
3. Trial Registry, preregistration, and multiplicity rules remain mandatory.
4. Holdout remains locked unless a later explicit human gate approves access.
5. RDL remains dormant/scaffolding-only through Phase 0-1 unless a future
   approved phase changes the boundary.
6. Growth/RBE remains inactive unless a charter-level review and preregistration
   path explicitly approve activation.
7. Python remains the Phase 0/1 control plane; non-Python runtime/toolchain
   additions require benchmark evidence, ADR, architecture/task/CI updates, and
   explicit human approval.
8. This audit does not approve Phase 1 evaluation/trading, OOS/performance
   claims, production labels, capital-ready labels, live feeds, broker
   integration, or live capital.
9. Findings remain Draft until Spec Owner acceptance.
10. Archive files are not loaded by default. Use compact indexes first, then
   open archived evidence only when required.

---

*Cycle: 5 | Phase: Phase 1D-K Archive-Only Baseline Deep Review | Date: 2026-05-06 | Pipeline: v1.0*
*Next cycle trigger: Spec Owner selects the next bounded block, a phase gate is proposed, or D-K evidence semantics change*
