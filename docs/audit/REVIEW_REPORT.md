# Entropy Protocol — Consolidated Review Report

**Classification:** Confidential — Internal Audit Document  
**Filename:** `docs/audit/REVIEW_REPORT.md`  
**Audit Cycle:** Cycle 1 — Phase 0 (Partial Rerun: Steps 3+4+5+6 after Spec v1.4)  
**Pipeline Version:** v1.0  
**Date:** 2026-03-04  
**Status:** Draft — Awaiting Spec Owner Acceptance  
**Spec-of-record:** `docs/core/PROTOCOL_SPEC.md` v1.4, `docs/core/CHARTER.md` v5.1  
**Step completion:** Partial rerun of Step 3/4/5/6 against v1.4 remediation set

---

## Executive Summary

Total tracked findings: **32**
- Severity split: **P0: 10 / P1: 10 / P2: 12**
- Source split: **Inherited from Cycle 0: 21 / New from Cycle 1 pipeline: 11**

Dominant risk theme:
- The system's gating evidence can appear complete while remaining statistically invalid (CI/K1), structurally non-reproducible (P4), or governance-fragile (RDL/RBE boundary controls).

Phase-block statement:
- **Phase 0 exit certification remains blocked** by unresolved P0 findings (F-1, F-2, F-4, F-5) and open P0 items pending implementation evidence (F-30, F-31).
- `F-3`, `F-23`, `F-24`, `F-25` remediation text is now synchronized and assertion-level checks are passing in this partial rerun.
- **Phase 1 entry and later phases remain blocked** until all P0 are remediated and re-verified by pipeline rerun.

## Partial Rerun Delta (2026-03-04, post-v1.4)

Remediation evidence integrated in canonical docs:
- Deterministic P3 protocol + concurrent P1/P3/P4 semantics added to `PROTOCOL_SPEC.md`.
- RDL boundary matrix, attestation (`RDL_MODE`), and machine-checkable evidence requirements added to `PROTOCOL_SPEC.md`, `workflow_ai_development.md`, and `review_pipeline.md`.
- Net Sharpe stream composition normalized in Phase 1 metrics table to `(a+b+c)`.
- GE-2/GE-3 zero-weight bright-line added (`GE-7`).
- RBE charter-level review artifact schema (`RBE Activation Packet`) added.
- Phase 2 matched-pair protocol baseline added.

Still open after partial rerun:
- F-1: Harvey-Liu canonical method is declared (`HL-HB-v1`) and scope is propagated, but full reproducibility package/examples remain incomplete.
- F-4/F-7: Full P4 algorithmic annex and vintage-exclusion rigor still incomplete for independent reproduction.
- F-29: K3 estimator lock across all authority docs is improved but still not fully formula-complete.
- F-30: policy baseline added; implementation evidence and queue telemetry verification still pending.
- F-31: freeze-safe reporting-only epoch tagging added; any logic-changing window semantics remain deferred under freeze constraints.

---

## Finding Inventory

### Inherited Findings (Cycle 0: F-1..F-21)

| Finding ID | Task ID | Sev | Status | Source | Location | Evidence summary | Impact | Next action | Acceptance criterion |
|---|---|---|---|---|---|---|---|---|---|
| F-1 | TASK-AF-001 | P0 | Partial-Mitigation | Cycle 0 baseline | CHARTER NN-5; PROTOCOL_SPEC B/F/J; GLOSSARY | Canonical method ID and cross-namespace counting now declared; full reproducibility package/examples still missing | A | Complete formula-level reproducibility suite and worked examples | Third party can reproduce haircut from registry inputs |
| F-2 | TASK-AF-002 | P0 | Partial-Mitigation | Cycle 0 baseline | CHARTER C; PROTOCOL_SPEC C/F; GLOSSARY | CI wording is synchronized to `CI-SR-ACF-v1`; derivation artifact and validation examples still pending | A/B | Add explicit derivation and cross-check examples | CI method and derivation explicitly documented |
| F-3 | TASK-AF-003 | P0 | Partial-Mitigation | Cycle 0 baseline | CHARTER D; PROTOCOL_SPEC D; GLOSSARY | P3 population/interval/aggregation/mapping are now defined deterministically | C | Verify implementation conformance in assertion rerun | Deterministic P3 implementation from text alone |
| F-4 | TASK-AF-004 | P0 | Inherited-Open | Cycle 0 baseline | CHARTER D; PROTOCOL_SPEC D/E/F | P4 outputs required by phase gates; no full algorithm exists | A/B/C | Add full P4 prereg algorithm + versioning/calibration protocol | Independent reproduction of label series possible |
| F-5 | TASK-AF-005 | P0 | Inherited-Open | Cycle 0 baseline | GLOSSARY IC; CHARTER correction; PROTOCOL_SPEC I | IC_long remains unvalidated load-bearing prior with no suspect threshold | A/B | Add IC_long suspect rule and correlation-aware FLAM control | IC_long governance symmetric and testable |
| F-6 | TASK-AF-006 | P1 | Partial-Mitigation | Cycle 0 baseline | CHARTER correction 2; PROTOCOL_SPEC F/J | False-kill discussion added; missed-kill still high and calibration unresolved | B | Finalize K4 error-rate policy and rationale in authoritative section | Both false/missed-kill rates documented + approved |
| F-7 | TASK-AF-007 | P1 | Partial-Mitigation | Cycle 0 baseline | Phase 0/1 gate rules; label immutability text | Label-vintage artifact added; full calibration-window exclusion policy still incomplete | A/C | Finalize calibration-window treatment for OOS spanning | Label-vintage exclusion rule is explicit and auditable |
| F-8 | TASK-AF-008 | P1 | Inherited-Open | Cycle 0 baseline | CHARTER correction 1; PROTOCOL_SPEC E/I | FLAM short-addition justification still sensitive to unresolved IC correlation | A | Add correlated long-short FLAM variant assumption and bounds | Revised delta formula and assumptions published |
| F-9 | TASK-AF-009 | P1 | Inherited-Open | Cycle 0 baseline | Phase 1 metrics, K6 scope | Phase 1 still lacks kill-level SimBroker drift control | B | Define Phase-1 cost-drift kill/hold rule | Phase-1 drift criterion blocks exits when breached |
| F-10 | TASK-AF-010 | P1 | Partial-Mitigation | Cycle 0 baseline | ARCHITECT_BRIEF known gap; PROTOCOL_SPEC D | Concurrent state semantics are now specified; runtime verification remains pending | C | Verify state-machine conformance in drift/adversarial rerun | Harness behavior is deterministic for A-D states |
| F-11 | TASK-AF-011 | P1 | Inherited-Open | Cycle 0 baseline | PROTOCOL_SPEC J1 vs other sections; GLOSSARY | N_eff estimator for K3 remains not fully locked across docs | B/C | Lock single K3 estimator and align wording | K3 verdict invariant under implementation choice |
| F-12 | TASK-AF-012 | P2 | Inherited-Open | Cycle 0 baseline | ARCHITECT_BRIEF B; PROTOCOL_SPEC open Q4 | Purge/embargo remains formula-free | C | Add timeframe-specific purge/embargo formula | Leakage checklist has explicit embargo parameter |
| F-13 | TASK-AF-013 | P2 | Partial-Mitigation | Cycle 0 baseline | CHARTER/PROTOCOL_SPEC D | P3 selection function now explicitly mapped to rho bands | C | Verify implementation conformance | Same inputs always produce same reduction target |
| F-14 | TASK-AF-014 | P2 | Inherited-Open | Cycle 0 baseline | Leakage audit references | Leakage controls remain incomplete beyond temporal shuffling | A/C | Extend checklist to remaining leakage classes | Checklist covers all named leakage modes |
| F-15 | TASK-AF-015 | P2 | Inherited-Open | Cycle 0 baseline | K4 definitions | K4 threshold exists; exact t-stat formula still absent | B | Define formula, df handling, autocorrelation treatment | Reviewer can recompute K4 exactly |
| F-16 | TASK-AF-016 | P2 | Partial-Mitigation | Cycle 0 baseline | Phase 2 matching text | Baseline matched-pair protocol now specified in PROTOCOL_SPEC; robustness details still pending | A/B | Finalize confounding controls and robustness metric details | Phase 2 delta test is reproducible |
| F-17 | TASK-AF-017 | P2 | Inherited-Open | Cycle 0 baseline | ARCHITECT_BRIEF F; Phase 0 criteria | Timestamp convention checks still not codified as gate criterion | C | Add timestamp-normalization checks to gate checklist | Timestamp consistency explicitly verified |
| F-18 | TASK-AF-018 | P2 | Partial-Mitigation | Cycle 0 baseline | PROTOCOL_SPEC J1 GE-2/GE-3 | GE-7 bright-line added for persistent near-zero weighting | D | Verify enforcement in registry and governance checks | Classification no longer developer-discretionary |
| F-19 | TASK-AF-019 | P2 | Inherited-Open | Cycle 0 baseline | GLOSSARY coverage | HWM/purge/window terms still incompletely normalized | C | Expand glossary with missing operational definitions | Missing core terms resolved |
| F-20 | TASK-AF-020 | P2 | Inherited-Open | Cycle 0 baseline | K5 text | "Any 12-month period" still lacks canonical window protocol | B/D | Lock rolling-vs-calendar convention | K5 trigger count deterministic |
| F-21 | TASK-AF-021 | P2 | Inherited-Open | Cycle 0 baseline | Phase 0 circuit-breaker criterion | P1 synthetic verification still under-specified as test suite | C | Define minimum required synthetic scenarios | P1 test suite is checklist-verifiable |

### New Findings (Cycle 1: F-22..F-32)

| Finding ID | Task ID | Sev | Status | Source | Location | Evidence summary | Impact | Next action | Acceptance criterion |
|---|---|---|---|---|---|---|---|---|---|
| F-22 | TASK-AF-022 (proposed) | P1 | Partial-Mitigation | Step 4 Drift | DRIFT_ASSERTIONS INV-E-01 | Net Sharpe wording normalized to `(a+b+c)` in canonical docs | A/B | Verify no residual drift in non-canonical artifacts | All references to net Sharpe stream composition are identical |
| F-23 | TASK-AF-023 (proposed) | P0 | Partial-Mitigation | Step 4 Drift | INV-F-08, INV-G-RDL-03 | RDL boundary matrix now aligned across PROTOCOL_SPEC/workflow/GLOSSARY | C/D | Verify assertion-level pass in next rerun | No cross-doc boundary contradiction remains |
| F-24 | TASK-AF-024 (proposed) | P0 | Partial-Mitigation | Step 4 Drift | INV-F-10, INV-G-RDL-02 | Submission-time trial counting propagated to workflow and GLOSSARY | A/D | Verify governance references in full rerun | Rule appears in all canonical governance references |
| F-25 | TASK-AF-025 (proposed) | P0 | Partial-Mitigation | Step 4 Drift | INV-F-11, INV-G-RDL-04 | RDL->RBE non-interaction propagated across canonical governance docs | C/D | Verify checklist/assertion linkage in rerun | Independent reviewer can verify separation without reading module internals |
| F-26 | TASK-AF-026 (proposed) | P1 | Partial-Mitigation | Step 4/5 | INV-G-GL-02; Adversarial B2/E3 | `RBE Activation Packet` schema and authority/storage rules defined | D | Validate packet flow evidence in governance log | Every RBE activation has a compliant review artifact |
| F-27 | TASK-AF-027 (proposed) | P2 | Open | Step 4 Drift | INV-C-12 | Explicit 4→5 gate topology missing; Phase 5 prerequisites skip direct dependency expression | C | Clarify phase topology rule for optional Phase 4 bypass | Phase transition map is unambiguous |
| F-28 | TASK-AF-028 (proposed) | P2 | Partial-Mitigation | Step 4/5 | INV-G-RDL-01; Adversarial D2 | RDL attestation schema (`RDL_MODE` + certification query) is now specified | D | Verify machine-checkable evidence in runtime audit outputs | Third party can verify scaffolding-only operation |
| F-29 | TASK-AF-029 (proposed) | P1 | Partial-Mitigation | Step 5 Adversarial | Adversarial A5/C | K3 timing lock added; estimator lock remains partially unresolved | B/C | Finalize single estimator contract + examples | Same portfolio yields same K3 verdict across tools |
| F-30 | TASK-AF-030 (proposed) | P0 | Partial-Mitigation | Step 5 Adversarial | Adversarial B3 | Deterministic queue/rate-limit/shock-control policy is now specified; runtime evidence pending | A/D | Verify FIFO/cap/shock-control telemetry in rerun | Phase-2 trial-count transition is deterministic |
| F-31 | TASK-AF-031 (proposed) | P0 | Partial-Mitigation | Step 5 Adversarial | Adversarial B2 + ARCH_MODEL AG-05 | Reporting-only `evaluation_epoch_id` rule added; freeze-sensitive logic changes intentionally deferred | B/C | Verify epoch-tag coverage in all K reports; keep kill logic unchanged under freeze | K1-K6 evaluation windows remain auditable through RBE events |
| F-32 | TASK-AF-032 (proposed) | P1 | Partial-Mitigation | Step 5 Adversarial | Adversarial E1 | GE-7 now defines zero-weight persistence as GE-3 | D | Verify registry classification enforcement | Trial counts include de-facto skill removals deterministically |

---

## Converted Backlog Items

| Finding ID | Task ID | Severity | Status | Cycle introduced |
|---|---|---|---|---|
| F-1..F-21 | TASK-AF-001..TASK-AF-021 | Mixed | Open / Partial-Mitigation | Cycle 0 |
| F-22 | TASK-AF-022 (proposed) | P1 | Partial-Mitigation | Cycle 1 |
| F-23 | TASK-AF-023 (proposed) | P0 | Partial-Mitigation | Cycle 1 |
| F-24 | TASK-AF-024 (proposed) | P0 | Partial-Mitigation | Cycle 1 |
| F-25 | TASK-AF-025 (proposed) | P0 | Partial-Mitigation | Cycle 1 |
| F-26 | TASK-AF-026 (proposed) | P1 | Partial-Mitigation | Cycle 1 |
| F-27 | TASK-AF-027 (proposed) | P2 | Open | Cycle 1 |
| F-28 | TASK-AF-028 (proposed) | P2 | Partial-Mitigation | Cycle 1 |
| F-29 | TASK-AF-029 (proposed) | P1 | Partial-Mitigation | Cycle 1 |
| F-30 | TASK-AF-030 (proposed) | P0 | Partial-Mitigation | Cycle 1 |
| F-31 | TASK-AF-031 (proposed) | P0 | Partial-Mitigation | Cycle 1 |
| F-32 | TASK-AF-032 (proposed) | P1 | Partial-Mitigation | Cycle 1 |

---

## Missing Evidence / Ambiguous Items

- Confidence below High:
  - Quantified K2/K5/K6 error rates (missing estimator-noise models).
  - Exact haircut magnitude by Harvey-Liu variant (variant not specified in spec).
- Assumptions made due missing authority:
  - K3-equivalent estimator uncertainty modeled from available formulas only.
  - RDL promotion behavior inferred from boundary language, not explicit operational spec.
- Access issues:
  - None. All required Step 1–5 artifacts were available.

---

## Prior Cycle Summary

Cycle 0 provided a baseline consolidation of `AUDIT_v1.md` with 21 open findings but no full pipeline artifacts. Cycle 1 executed Steps 1–5 formally and extends the baseline by adding architecture/invariant/drift/adversarial evidence, confirming all inherited issues remain open while introducing 11 new cross-module governance and consistency findings centered on Growth Layer/RBE and RDL integration boundaries.

---

## Next Actions

1. Finalize unresolved P0 formula-level artifacts: HL method package and P4 annex reproducibility contract.
2. Implement runtime telemetry evidence for F-30/F-31 policies (queue behavior + epoch-tag coverage in K reports).
3. Run next partial rerun (Step 3+4+5+6) with telemetry evidence.
4. Run full rerun before any Phase 0→1 gate decision.

---

## Proposed tasks.md additions (historical reference)

Status update (2026-03-04): `docs/tasks.md` has been synchronized and now includes `TASK-AF-022` through `TASK-AF-032` (version 1.1).

| Proposed Task ID | Finding | Sev | Summary | Acceptance criterion | Dependencies |
|---|---|---|---|---|---|
| TASK-AF-022 | F-22 | P1 | Normalize net Sharpe stream wording across docs | All net Sharpe references use identical stream definition `(a+b+c)` | None |
| TASK-AF-023 | F-23 | P0 | Unify RDL operational boundary semantics | PROTOCOL_SPEC/workflow/GLOSSARY express same boundary rule | TASK-AF-004 |
| TASK-AF-024 | F-24 | P0 | Propagate RDL submission-count rule to governance docs | Rule present in GLOSSARY and workflow governance section | TASK-AF-001 |
| TASK-AF-025 | F-25 | P0 | Add explicit RDL->RBE separation governance control | Governance checklist includes non-interaction verifier | TASK-AF-023 |
| TASK-AF-026 | F-26 | P1 | Define charter-level review process for RBE | RBE activation includes required review artifact schema | None |
| TASK-AF-027 | F-27 | P2 | Clarify phase topology for Phase 5 entry | Explicit gate dependency text for optional Phase 4 bypass | None |
| TASK-AF-028 | F-28 | P2 | Add RDL dormancy attestation artifact | Pre-Phase-2 mode attestation is machine-checkable | TASK-AF-023 |
| TASK-AF-029 | F-29 | P1 | Lock K3 estimator and boundary procedure | K3 formula and boundary behavior deterministic | TASK-AF-011 |
| TASK-AF-030 | F-30 | P0 | Define Phase-2 RDL promotion queue policy | Promotion/activation trial-count behavior is deterministic | TASK-AF-023, TASK-AF-024 |
| TASK-AF-031 | F-31 | P0 | Define kill-window continuity under RBE transitions | K1-K6 evaluation windows survive RBE changes consistently | TASK-AF-026 |
| TASK-AF-032 | F-32 | P1 | Close zero-weight GE-2/GE-3 governance loophole | Zero-weight persistence is explicitly GE-3 and trial-counted | TASK-AF-018 |

---
