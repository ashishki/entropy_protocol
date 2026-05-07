# Audit Index

**Version:** 2.2
**Date:** 2026-05-06
**Status:** Active compact index

This directory keeps only the current audit surface in root. Historical phase
packets, prior review material, and bulky retrieval logs are archived.

## Current State

**Current work:** Spec Owner next decision after D-K fix closure.

**Last completed task:** DK-REVIEW-001 Full D-K Deep Review And Fix Closure.

**Current verdict:** `DK_DEEP_REVIEW_COMPLETE_FIXES_APPLIED_NO_CLAIMS`.

**Still forbidden:** Phase 1 evaluation/trading, live feeds, broker integration,
archive holdout reads, Growth/RDL/RBE activation, OOS/performance claims,
production labels, capital-ready labels, and live-capital claims.

## Active Audit Files

| File | Role |
|---|---|
| `REVIEW_REPORT.md` | Current consolidated audit status |
| `POST_DK_STRATEGY_REVIEW.md` | Strategy synthesis after D-K fix closure |
| `NEXT_PHASE_PLAN.md` | Proposed next bounded block plan |
| `META_ANALYSIS.md` | Cycle 5 D-K meta-analysis output |
| `ARCH_MODEL.md` | Cycle 5 D-K architecture review output |
| `INVARIANTS.md` | Cycle 5 D-K invariant extraction output |
| `DRIFT_ASSERTIONS.md` | Cycle 5 D-K drift assertion output |
| `DRIFT_REPORT.md` | Cycle 5 D-K drift report output |
| `ADVERSARIAL_REVIEW.md` | Cycle 5 D-K adversarial review output |

## Audit Pipeline Files

| File | Role |
|---|---|
| `PROMPT_0_META.md` | Meta-audit entry prompt |
| `PROMPT_1_ARCH_REVIEW.md` | Architecture review prompt |
| `PROMPT_2_INVARIANTS.md` | Invariant review prompt |
| `PROMPT_3_DRIFT_GUARD.md` | Drift guard prompt |
| `PROMPT_4_ADVERSARIAL.md` | Adversarial review prompt |
| `PROMPT_5_CONSOLIDATED.md` | Consolidated review prompt |
| `review_pipeline.md` | Audit pipeline notes |

## Archive Map

| Directory | Contents |
|---|---|
| `archive/phase_reviews/` | Historical Phase 1-8 reviews |
| `archive/phase0/` | Phase 0 gate, strategic decision, and closure records |
| `archive/p0_5/` | Phase 0.5 evidence-hardening plans and formula reviews |
| `archive/p0_6/` | Phase 0.6 source/bootstrap records |
| `archive/p0_7/` | Archive-only continuation and gate packet records |
| `archive/phase1a/` | Phase 1A and post-Phase1A packets moved out of active root |
| `archive/p4/` | P4 coverage and universe scaling packets |
| `archive/simbroker/` | SimBroker calibration planning and verification records |
| `archive/data_stability/` | Data stability bootstrap, append, and simulation records |
| `archive/dispositions/` | T21-T24 and D010 disposition records |
| `archive/legacy/` | Superseded audit index and legacy audit reports |
| `archive/legacy/QUESTION_POOL_cycle1_2026-03-04.md` | Superseded Cycle 1 question pool |
| `archive/legacy_prompts/` | Superseded prompt trio from the earlier review pipeline |
| `../archive/session_state/` | Full compacted task/log/evidence snapshots |

For archive details, see `archive/README.md`.
