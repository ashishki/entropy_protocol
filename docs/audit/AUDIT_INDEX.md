# Audit Index

**Version:** 2.0
**Date:** 2026-05-05
**Status:** Active compact index

This directory now keeps only the current audit surface in the root. Historical
phase packets, calibration plans, and prior review material are archived under
`docs/audit/archive/` and should not be loaded by default.

---

## Current State

**Current work:** P1D-001 Long-Only Implementation Contract.

**Next task:** define the bounded long-only implementation contract before any
transition from schema-only stubs to executable baseline logic.

**Current verdict:** `PHASE1D_PLANNING_SELECTED_NO_GO_FOR_EVALUATION`.

**Still forbidden:** Phase 1 evaluation/trading, live feeds, broker integration,
archive holdout reads, Growth/RDL/RBE activation, OOS/performance claims,
production labels, capital-ready labels, and live-capital claims.

---

## Active Audit Files

| File | Role |
|---|---|
| `REVIEW_REPORT.md` | Current consolidated audit status |
| `PHASE1A_FIX_CLOSURE_REVIEW.md` | Latest strategic/fix closure decision |
| `PHASE1A_ARCHIVE_ENTRY_CONTRACT.md` | P1A entry contract and scope boundary |
| `PHASE1A_ARCHIVE_FREEZE_PACKET.md` | Archive freeze evidence packet |
| `PHASE1A_REGISTRATION_BOUNDARY_PACKET.md` | Registration/read-gate boundary packet |
| `PHASE1A_BASELINE_REGISTRATION_PACKET.md` | Baseline spec registration packet |
| `PHASE1A_DEVELOPMENT_STRATEGY.md` | Phase 1A sequencing and runtime/workload strategy |
| `PHASE1A_WORKLOAD_BENCHMARK_CONTRACT.md` | Workload profile and benchmark contract |
| `PHASE1A_BASELINE_SCAFFOLD_PACKET.md` | Executable scaffold boundary packet |
| `PHASE1A_SCAFFOLD_PERFORMANCE_PROBE_PACKET.md` | Mechanics-only scaffold probe packet |
| `PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md` | Scaffold/probe closure decision |
| `POST_PHASE1A_STRATEGY_REVIEW.md` | Strategy decision selecting audit-readiness as the next block |
| `POST_PHASE1A_NEXT_STAGE_PLAN.md` | Task plan for prompt refresh, deep review, and consolidation |
| `PHASE1A_AUDIT_PROMPT_REFRESH_PACKET.md` | P1A-011 prompt refresh closure and F-C3-007 disposition |
| `POST_PHASE1A_OPERATIONS_PLAN.md` | Prioritized Phase 1B readiness operations plan |
| `META_ANALYSIS.md` | Cycle 4 meta-analysis output |
| `ARCH_MODEL.md` | Cycle 4 architecture review output |
| `INVARIANTS.md` | Cycle 4 invariant extraction output |
| `DRIFT_ASSERTIONS.md` | Cycle 4 drift assertion output |
| `DRIFT_REPORT.md` | Cycle 4 drift report output |
| `ADVERSARIAL_REVIEW.md` | Cycle 4 adversarial review output |

---

## Audit Pipeline Files

| File | Role |
|---|---|
| `PROMPT_0_META.md` | Meta-audit entry prompt |
| `PROMPT_1_ARCH_REVIEW.md` | Architecture review prompt |
| `PROMPT_2_INVARIANTS.md` | Invariant review prompt |
| `PROMPT_3_DRIFT_GUARD.md` | Drift guard prompt |
| `PROMPT_4_ADVERSARIAL.md` | Adversarial review prompt |
| `PROMPT_5_CONSOLIDATED.md` | Consolidated review prompt |
| `META_ANALYSIS.md` | Meta-audit output |
| `ARCH_MODEL.md` | Architecture model output |
| `INVARIANTS.md` | Invariant output |
| `DRIFT_ASSERTIONS.md` | Drift assertion output |
| `DRIFT_REPORT.md` | Drift report output |
| `ADVERSARIAL_REVIEW.md` | Adversarial review output |
| `QUESTION_POOL.md` | Review question pool |
| `review_pipeline.md` | Audit pipeline notes |

Superseded prompt files `PROMPT_1_ARCH.md`, `PROMPT_2_CODE.md`, and
`PROMPT_3_CONSOLIDATED.md` are archived under `archive/legacy_prompts/`.

---

## Archive Map

| Directory | Contents |
|---|---|
| `archive/phase_reviews/` | Historical Phase 1-8 reviews |
| `archive/phase0/` | Phase 0 gate, strategic decision, and closure records |
| `archive/p0_5/` | Phase 0.5 evidence-hardening plans and formula reviews |
| `archive/p0_6/` | Phase 0.6 source/bootstrap records |
| `archive/p0_7/` | Phase 0.7 archive-only continuation and gate packets |
| `archive/p4/` | P4 coverage and universe scaling packets |
| `archive/simbroker/` | SimBroker calibration planning and verification records |
| `archive/data_stability/` | Data stability bootstrap, append, and simulation records |
| `archive/dispositions/` | T21-T24 and D010 disposition records |
| `archive/legacy/` | Superseded audit index and legacy audit reports |
| `archive/legacy_prompts/` | Superseded prompt trio from the earlier review pipeline |

For archive details, see `archive/README.md`.
