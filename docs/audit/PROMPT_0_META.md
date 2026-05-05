# Entropy Protocol — Meta Orchestration Prompt (Cycle Entrypoint)

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/PROMPT_0_META.md`
**Cycle:** Cycle 4 — Post-Phase-1A Scaffold Closure
**Date:** 2026-05-05
**Owner:** Spec Owner / Staff-Level Systems Architect
**Pipeline Version:** v1.0
**Role:** Stable entrypoint for the post-Phase-1A deep protocol review. Read
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

## Cycle Context (State Snapshot — 2026-05-05)

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
| Current consolidated review | `docs/audit/REVIEW_REPORT.md` | Draft | Cycle 3 post-Phase0 archive-only audit plus Phase 1A closure updates |
| Meta Investigation | `docs/audit/META_ANALYSIS.md` | Existing | Refresh in this cycle |
| Architecture Review | `docs/audit/ARCH_MODEL.md` | Existing | Refresh in this cycle |
| Invariant Extraction | `docs/audit/INVARIANTS.md` | Existing | Refresh in this cycle |
| Drift Assertions | `docs/audit/DRIFT_ASSERTIONS.md` | Existing | Refresh in this cycle |
| Drift Report | `docs/audit/DRIFT_REPORT.md` | Existing | Refresh in this cycle |
| Adversarial Review | `docs/audit/ADVERSARIAL_REVIEW.md` | Existing | Refresh in this cycle |
| Phase 1A closure | `docs/audit/PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md` | Complete | Scaffold/probe chain closed; no evaluation approval |
| Post-Phase-1A strategy | `docs/audit/POST_PHASE1A_STRATEGY_REVIEW.md` | Complete | Selects audit-readiness and deep review as next stage |

**Summary:** This cycle runs after Phase 1A archive-only scaffold/probe
closure. Phase 0 is closed only as an archive-only research foundation. Full
Phase 1 evaluation/trading remains unapproved, live/streaming Phase 0 remains
unapproved, and holdout remains locked.

### Delta Since Prior Full Audit

1. P1A-001 through P1A-004 closed the archive contract/read-gate fix chain.
2. P1A-006 and P1A-007 established workload/runtime and benchmark boundaries:
   Python remains the control/orchestration layer, Polars/DuckDB/Arrow remain
   the data-plane default, and non-Python escalation requires benchmark
   evidence, ADR, architecture/task/CI updates, and explicit human approval.
3. P1A-008 implemented a narrow executable scaffold with non-trading
   placeholders and read-gate checks.
4. P1A-009 implemented a mechanics-only scaffold probe with synthetic/no-claim
   benchmark artifacts and no strategy metrics.
5. P1A-010 closed the scaffold/probe chain for foundation purposes only.
6. PSR-004 selected audit-readiness before any new implementation block.

### Current Phase Hypothesis

**Post-Phase-1A Audit Readiness And Deep Review**

- Current task: P1A-011 Audit Prompt Metadata Refresh
- Immediate blocker for this audit run: F-C3-007 stale prompt metadata
- Earliest permissible next implementation block: after the prompt refresh,
  deep review, and consolidated post-Phase-1A decision
- Not approved: Phase 1 evaluation/trading, holdout reads, live feeds,
  Growth/RDL/RBE activation, non-Python runtime/toolchain introduction, or
  OOS/performance claims

---

## Risk Surface Register

The following risk surfaces are ranked for the post-Phase-1A review. Downstream
prompts should create findings only when current documents or code evidence
support them.

### TIER-1: Claim And Phase-Gate Containment

**RS-01 — Phase 1 Evaluation Creep**
- Why now: Phase 1A created executable scaffold/probe artifacts. A downstream
  review must ensure these cannot be mistaken for Phase 1 evaluation, OOS
  evidence, validated alpha, or gate approval.
- Evidence: `PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md`,
  `POST_PHASE1A_STRATEGY_REVIEW.md`, `REVIEW_REPORT.md`

**RS-02 — Holdout Boundary Integrity**
- Why now: The archive freeze and registration boundary encode formation,
  validation, and holdout labels. The holdout must remain locked until a
  separate approved gate exists.
- Evidence: `PHASE1A_REGISTRATION_BOUNDARY_PACKET.md`,
  `PHASE1A_BASELINE_REGISTRATION_PACKET.md`,
  `PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md`

**RS-03 — No-Claim Benchmark Semantics**
- Why now: P1A-009 emits runtime/memory/artifact facts. These facts must remain
  implementation evidence only and must not become strategy performance
  evidence.
- Evidence: `PHASE1A_WORKLOAD_BENCHMARK_CONTRACT.md`,
  `PHASE1A_SCAFFOLD_PERFORMANCE_PROBE_PACKET.md`

### TIER-2: Architecture And Runtime Drift

**RS-04 — Runtime Escalation Drift**
- Why now: Phase 1A explicitly considered high-load simulation concerns.
  Python remains the control plane and Polars/DuckDB/Arrow remain the data
  plane unless a benchmark miss and ADR justify escalation.
- Evidence: `ARCHITECTURE.md`, `IMPLEMENTATION_CONTRACT.md`,
  `PHASE1A_DEVELOPMENT_STRATEGY.md`,
  `PHASE1A_WORKLOAD_BENCHMARK_CONTRACT.md`

**RS-05 — Storage Boundary Drift**
- Why now: Benchmarks and future evaluation planning must not move large
  intermediates into PostgreSQL or create mutable untracked data stores.
- Evidence: `ARCHITECTURE.md`, `PHASE1A_WORKLOAD_BENCHMARK_CONTRACT.md`

### TIER-3: Dormant Module And Governance Boundaries

**RS-06 — Growth/RBE Activation Leakage**
- Why now: Phase 1A documents Growth monitoring-only scope but does not approve
  Growth instrumentation, RBE activation, or portfolio influence.
- Evidence: `PROTOCOL_SPEC.md`, `PHASE1A_ARCHIVE_ENTRY_CONTRACT.md`,
  `REVIEW_REPORT.md`

**RS-07 — RDL Dormancy Leakage**
- Why now: RDL must remain dormant/scaffolding-only through Phase 0-1 unless a
  future approved phase changes the boundary.
- Evidence: `PROTOCOL_SPEC.md`, `GLOSSARY.md`,
  `PHASE1A_ARCHIVE_ENTRY_CONTRACT.md`

### TIER-4: Audit Pipeline Integrity

**RS-08 — Prompt Metadata Drift**
- Why now: F-C3-007 identified stale prompt metadata. This refresh is the
  prerequisite for a reliable deep review.
- Evidence: `POST_PHASE1A_STRATEGY_REVIEW.md`, `REVIEW_REPORT.md`

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

*Cycle: 4 | Phase: Post-Phase-1A | Date: 2026-05-05 | Pipeline: v1.0*
*Next cycle trigger: P1A-011 prompt refresh complete, then run the full post-Phase-1A deep review sequence*
