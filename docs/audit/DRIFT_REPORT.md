# Entropy Protocol — Drift Report

**Classification:** Confidential — Internal Audit Document  
**Filename:** `docs/audit/DRIFT_REPORT.md`  
**Audit Cycle:** Cycle 1 — Phase 0 (Pre-Development)  
**Pipeline Step:** Step 4 — Protocol Drift Guard  
**Pipeline Version:** v1.0  
**Date:** 2026-03-04  
**Status:** Draft — Awaiting Spec Owner Acceptance

---

## Executive Summary

Drift verdict totals (from `DRIFT_ASSERTIONS.md`):
- PASS: 30
- FAIL: 17
- AMBIGUOUS: 34
- Regressions: 0 (no prior Step-4 artifact exists in Cycle 0)

Most critical FAIL items (P0/P1 impact):
- **INV-E-02 (P0):** Sharpe CI claim is internally consistent across docs but arithmetically incorrect.
- **INV-C-05 / INV-D-P4 / INV-G-RDL-05 (P0):** P4 outputs are required by phase gates and RDL-2 but algorithm remains undefined.
- **INV-F-08 / INV-G-RDL-03 (P0):** RDL boundary is inconsistently scoped ("Phase 2+" vs "Phase 2 exit criteria met").
- **INV-B-K3 (P1):** K3 temporal trigger differs across documents.
- **INV-E-01 (P1):** Net Sharpe stream composition wording drifts (`a+b+c` vs `a+c`).
- **INV-D-U1..U4 (P1):** Concurrent regime-state recovery behaviors remain undefined.

All FAIL items are new in this cycle because Step 4 is first executed in Cycle 1.

---

## FAIL Findings (Severity-Ordered)

### P0

1. **INV-E-02 — Net Sharpe CI Arithmetic Drift (links: F-2 / TASK-AF-002)**
- Expected: CI definition should be correct and consistently implementable.
- Found: CHARTER, PROTOCOL_SPEC, and GLOSSARY all repeat `±0.15–0.20` at 15 months for SR~0.30, conflicting with the documented audit derivation in REVIEW_REPORT.
- Discrepancy type: formula correctness drift (shared incorrect value).
- Phase-gate impact: contaminates K1 and Phase 1 exit interpretation.

2. **INV-C-05 + INV-D-P4 + INV-G-RDL-05 — P4 Required Output Without P4 Algorithm (links: F-4 / TASK-AF-004, F-7 / TASK-AF-007)**
- Expected: P4 should be fully specified if used in Phase 0 exit and Phase 1 regime-span claims.
- Found: Phase 0/1 gates require P4 labels; RDL-2 references "P4 prereg spec"; no algorithm exists in spec set.
- Discrepancy type: missing core invariant definition.
- Phase-gate impact: invalidates third-party verifiability of Phase 0->1 and Phase 1->2 gating evidence.

3. **INV-F-08 / INV-G-RDL-03 — RDL Operational Boundary Inconsistency (new finding, RS-13)**
- Expected: single boundary for when RDL may influence routing/sizing.
- Found: PROTOCOL_SPEC states both "operational Phase 2+" and "no influence until Phase 2 exit criteria met"; workflow doc states operational starts at Phase 2+.
- Discrepancy type: scope drift across governance docs.
- Phase-gate impact: creates contradictory interpretations for legal/valid RDL outputs in Phase 2.

4. **INV-F-10 / INV-G-RDL-02 — RDL Trial Counting Rule Fragmentation (links: F-1 / TASK-AF-001, RS-12)**
- Expected: submission-time counting rule should exist in canonical glossary/governance locations.
- Found: only PROTOCOL_SPEC Section E contains the rule; GLOSSARY and workflow governance omit it.
- Discrepancy type: fragmented invariant location.
- Phase-gate impact: multiplicity accounting implementation can diverge between teams/tools.

5. **INV-F-11 / INV-G-RDL-04 — RDL->RBE Non-Interaction Rule Not Propagated (new finding, RS-15)**
- Expected: strict separation should be explicit in governance workflow, not only module narrative.
- Found: explicit in PROTOCOL_SPEC E only; absent in workflow governance policy.
- Discrepancy type: control-surface drift.
- Phase-gate impact: ambiguous authority for RBE activation inputs.

### P1

6. **INV-B-K3 — K3 Temporal Trigger Inconsistency (links: F-11 / TASK-AF-011)**
- Expected: one canonical temporal trigger definition.
- Found: CHARTER Phase 1 metrics table says "N_eff <=2 for 2 consecutive months"; CHARTER appendix/PROTOCOL_SPEC/GLOSSARY emphasize "after 3+ months monitoring" without explicit consecutive-month clause.
- Discrepancy type: threshold/temporal wording drift.
- Phase-gate impact: K3 fire decision can differ by implementation.

7. **INV-E-01 — Net Sharpe Stream Composition Drift (new finding; interacts with F-5)**
- Expected: primary metric always references streams (a)+(b)+(c) from NN-2.
- Found: multiple phase tables use `(a+c)` wording while NN-2/GLOSSARY define `(a+b+c)`.
- Discrepancy type: metric scope drift.
- Phase-gate impact: short-side performance can be silently excluded in later-phase reporting.

8. **INV-E-06 — N_eff Formula Choice Drift (links: F-11 / TASK-AF-011)**
- Expected: single formula for K3 decisions.
- Found: J1 gives explicit equicorrelation formula; other sections use DR+clustering language without locking estimator choice.
- Discrepancy type: formula location/authority drift.
- Phase-gate impact: K3 boundary is non-deterministic across implementations.

9. **INV-E-07 — FLAM Input Definition Drift (links: F-5 / TASK-AF-005, F-8 / TASK-AF-008)**
- Expected: internally consistent BR/IC assumptions.
- Found: BR_long arithmetic text inconsistent (5x2x12 stated as 240); unresolved dependency on long-short correlation remains open.
- Discrepancy type: numeric-definition drift.
- Phase-gate impact: Phase 3 expected value and prioritization may be mis-specified.

10. **INV-D-U1..INV-D-U4 — Undefined Concurrent Regime Recovery States (links: F-10 / TASK-AF-010)**
- Expected: deterministic transition rules for all identified concurrent states.
- Found: ARCHITECT_BRIEF flags the gap explicitly; PROTOCOL_SPEC/CHARTER do not close it.
- Discrepancy type: missing state-machine specification.
- Phase-gate impact: execution-vs-evaluation divergence risk in stress periods.

11. **INV-C-12 — Missing Explicit 4->5 Gate Topology (new finding)**
- Expected: phase-gate topology should be unambiguous.
- Found: no direct 4->5 criterion; Phase 5 prerequisites reference Phase 1 + live capital only.
- Discrepancy type: lifecycle topology drift.
- Phase-gate impact: governance confusion for treasury activation if Phase 4 is bypassed.

12. **INV-G-GL-02 — "Charter-Level Review" Undefined Operationally (RS-11)**
- Expected: RBE approval authority/process/output should be concretely defined.
- Found: term used in PROTOCOL_SPEC E/J2 without operational definition in CHARTER/EVOLUTION/workflow.
- Discrepancy type: governance-definition drift.
- Phase-gate impact: non-reproducible RBE activation decisions.

### P2

13. **INV-F-10 / INV-F-11 companion drift**
- Secondary impact: glossary incompleteness raises implementation risk for non-core tools.

14. **INV-E-07 arithmetic mismatch side-effect**
- Secondary impact: modeling docs and practical planning can diverge despite unchanged thresholds.

---

## AMBIGUOUS Findings (Severity-Ordered)

### P0-P1 Ambiguities

1. **INV-A-05 / INV-E-03 — Harvey-Liu formula missing**
- Ambiguity: mandatory control with no canonical formula or aggregation procedure.
- Required resolution: add formula variant, trial-count aggregation scope, and haircut computation to PROTOCOL_SPEC + GLOSSARY.

2. **INV-D-P3 / INV-E-09 — P3 rho population and return-interval undefined**
- Ambiguity: threshold is fixed but population definition is not.
- Required resolution: lock population, return interval, and handling of active/inactive assets.

3. **INV-E-08 — K4 t-stat formula undefined**
- Ambiguity: threshold exists; test statistic definition does not.
- Required resolution: define t-stat computation and variance estimator.

4. **INV-C-07 / INV-D-CR-03 — Regime label immutability vs vintage contamination**
- Ambiguity: immutability exists, but calibration-vintage rules for phase gating remain unspecified.
- Required resolution: define allowed calibration windows and OOS spanning accounting rules.

5. **INV-F-09 / INV-G-GL-01..07 — Growth/RBE enforcement artifacts incomplete**
- Ambiguity: policy text exists without external attestations/mechanized controls.
- Required resolution: define activation artifact schema and verifier checklist.

### P2 Ambiguities

6. **INV-E-10 / INV-E-11 / INV-E-12**
- Ambiguity: windowing, annualization, and uncertainty protocol not locked for several secondary metrics.
- Required resolution: add canonical computation appendix.

7. **INV-G-RDL-01 / INV-G-RDL-07**
- Ambiguity: dormancy is policy-stated; timestamp conventions and attestation controls absent.
- Required resolution: add phase-boundary compliance test and timestamp standard.

---

## New Risk Surfaces (Growth Layer / RDL Drift)

1. **GL-DRIFT-01 (RS-11): Governance-token without governance object**
- Rule exists: RBE activation requires charter-level review.
- Drift: no doc defines the review artifact or decision authority.
- Enforceability: judgment-based, not independently testable.

2. **RDL-DRIFT-01 (RS-13): Dual boundary semantics for Phase 2**
- Rule exists: RDL is dormant pre-Phase-2.
- Drift: routing influence boundary described as both Phase 2+ and post-Phase-2-exit.
- Enforceability: ambiguous without explicit mode/state field.

3. **RDL-DRIFT-02 (RS-12): Counting rule orphaned outside module text**
- Rule exists: `RDL-*` counted at submission.
- Drift: absent from glossary/governance docs.
- Enforceability: high risk of partial implementations.

4. **GL/RDL-DRIFT-03 (RS-15): Non-interaction rule not propagated**
- Rule exists: RDL must never feed RBE.
- Drift: not mirrored in workflow governance.
- Enforceability: relies on reader memory of one section.

---

## Regression Detection vs Cycle 0 Findings (F-1..F-11)

- **No full mitigations detected.**
- **No documented regressions relative to prior accepted drift artifacts** (none existed).
- **Partial-mitigation signals only:**
  - F-6 acknowledged calibration tradeoff language remains present (K4 known limitation documented).
  - F-10 explicitly acknowledged in ARCHITECT_BRIEF but not resolved in canonical spec.
  - F-9 remains open; K6 still Phase 3-4 only.

---

## Scope of Next Actions

| Drift item(s) | Required spec action | Frozen non-negotiable impact? | ADR/EVOLUTION entry required? |
|---|---|---|---|
| INV-E-02 | Correct CI methodology and dependent wording in PROTOCOL_SPEC C/F, CHARTER C, GLOSSARY Net Sharpe | No threshold change required unless recalibrating K1 policy | Yes |
| INV-C-05 / INV-D-P4 / INV-G-RDL-05 | Add formal P4 algorithm prereg spec with versioning and calibration protocol | No | Yes |
| INV-B-K3 / INV-E-06 | Harmonize K3 temporal wording and lock N_eff estimator used for K3 | No | Yes |
| INV-E-01 | Normalize net Sharpe stream composition wording to `(a+b+c)` in all phase tables | No | Yes |
| INV-F-08 / INV-G-RDL-03 | Unify RDL operational boundary language across PROTOCOL_SPEC and workflow governance | No | Yes |
| INV-F-10 | Add RDL submission-count rule to GLOSSARY and governance workflow doc | No | Yes |
| INV-F-11 | Mirror RDL->RBE non-interaction in workflow governance and checklist artifacts | No | Yes |
| INV-G-GL-02 | Define charter-level review authority, output artifact, and storage location | No | Yes |
| INV-D-U1..U4 | Add explicit concurrent recovery state-machine rules | No | Yes |
| INV-C-12 | Clarify phase-topology rule for Phase 5 entry when Phase 4 is bypassed | No | Yes |

No identified next action requires direct modification of frozen NN-1..NN-6 thresholds. All required actions are clarifications/formalizations of currently underspecified rules.

---

Prepared for Step 5 input (`docs/audit/PROMPT_4_ADVERSARIAL.md`).
