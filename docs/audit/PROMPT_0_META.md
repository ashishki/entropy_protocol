# Entropy Protocol — Meta Orchestration Prompt (Cycle Entrypoint)

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/PROMPT_0_META.md`
**Cycle:** Cycle 1 — Phase 0, Pre-Development
**Date:** 2026-03-04
**Owner:** Spec Owner / Staff-Level Systems Architect
**Pipeline Version:** v1.0
**Role:** Stable entrypoint for all future audit cycles. Read this first before running any pipeline step.

---

## How to Use This File

This file is the mandatory starting context for every audit pipeline run. It contains:
1. **Cycle Context** — delta-oriented state snapshot for this cycle
2. **Risk Surface Register** — top risk surfaces identified, with evidence pointers
3. **Downstream Prompt Index** — which prompts to run in which order

Before running any downstream prompt, load:
1. `docs/README.md`
2. `docs/core/GLOSSARY.md`
3. `docs/audit/review_pipeline.md`
4. `docs/audit/AUDIT_INDEX.md`
5. This file (`docs/audit/PROMPT_0_META.md`)

Then run downstream prompts in Step order: PROMPT_1 → PROMPT_2 → PROMPT_3 → PROMPT_4 → PROMPT_5.
Each step must complete and write its artifact before the next step begins.

---

## Cycle Context (State Snapshot — 2026-03-04)

### Spec-of-Record

| Document | Version | Date | Status |
|---|---|---|---|
| `docs/core/PROTOCOL_SPEC.md` | v1.2 | 2026-03-04 | Active; freeze period active (6mo from issue) |
| `docs/core/CHARTER.md` | v5.0 | 2026-03-04 | Active |
| `docs/core/GLOSSARY.md` | — | 2026-03-04 | Active |
| `docs/core/EVOLUTION.md` | — | 2026-03-04 | Active |
| `docs/audit/review_pipeline.md` | v1.0 | 2026-03-04 | Active |

PROTOCOL_SPEC.md v1.2 is the canonical engineering specification. It supersedes `entropy_protocol_master_spec_v1.md` (archived). The v1.1 and v1.2 changes added the Growth Layer and Research Discovery Layer (RDL) respectively. **Neither addition was included in the source audit (AUDIT_v1.md v1.0), which was authored against the pre-v1.1 spec.** These two modules represent unaudited additions to the specification.

### Existing Audit Artifacts

| Artifact | File | Status | Notes |
|---|---|---|---|
| Source Audit | `docs/audit/AUDIT_v1.md` | Accepted | 21 findings; all Open. Basis for Cycle 0. |
| Consolidated Review (baseline) | `docs/audit/REVIEW_REPORT.md` | Draft | Cycle 0 baseline; Steps 1–5 never executed. |
| Meta Investigation | `docs/audit/META_ANALYSIS.md` | Not yet run | — |
| Architecture Review | `docs/audit/ARCH_MODEL.md` | Not yet run | — |
| Invariant Extraction | `docs/audit/INVARIANTS.md` | Not yet run | — |
| Drift Assertions | `docs/audit/DRIFT_ASSERTIONS.md` | Not yet run | — |
| Drift Report | `docs/audit/DRIFT_REPORT.md` | Not yet run | — |
| Adversarial Review | `docs/audit/ADVERSARIAL_REVIEW.md` | Not yet run | — |

**Summary:** This is Cycle 1, the first formal full-pipeline run. No Step 1–5 artifacts exist. All prior findings are sourced from AUDIT_v1.md via the Cycle 0 baseline REVIEW_REPORT.

### Delta Since Cycle 0

The following changes occurred to the specification after the source audit was authored (inferred from spec version history):

1. **PROTOCOL_SPEC.md v1.1** — Added Growth Layer module (Section E), Growth Layer & Efficiency Metrics (Section J1), Risk Budget Escalation Protocol (Section J2). This is a substantive addition: the RBE mechanism creates a pathway from monitoring-only Growth Layer mode to active mode, triggered by structured conditions. The activation pathway has never been audited.

2. **PROTOCOL_SPEC.md v1.2** — Added Research Discovery Layer (RDL) module (Section E) with four submodules (RDL-1 through RDL-4). RDL introduces: (a) a new Trial Registry namespace (`RDL-*`), (b) a counting rule for Harvey-Liu trial budget that begins at submission (not promotion), (c) a new Phase 2 operational gate for signal generation, and (d) explicit constraints on RBE interaction. None of these have been audited.

3. **All 21 Cycle 0 findings remain Open.** No finding has moved to In Progress, Mitigated, or Closed. No spec change has been committed in response to any finding. Development has not started (no code exists).

**ASSUMPTION:** The project is still in the pre-development phase of Phase 0. No walk-forward harness, SimBroker, or signal code has been written yet. This is inferred from TASK-DEV-001 through TASK-DEV-004 all showing Open status with no updates.

### Current Phase Hypothesis

**Phase 0 — Pre-Development** (ASSUMPTION — no code artifacts observed)
- Primary task: Resolve P0 audit findings before any implementation begins
- Immediate blocker: 5 P0 findings (F-1 through F-5) block any valid Phase 0 exit evaluation
- Earliest permissible Phase 1 entry: After all P0 findings resolved + full pipeline re-run Accepted

---

## Risk Surface Register

The following risk surfaces are ranked by immediacy and severity. Use this list to focus effort in downstream prompts. Each risk surface should generate at least one structured finding in ARCH_MODEL.md, INVARIANTS.md, DRIFT_REPORT.md, or ADVERSARIAL_REVIEW.md.

### TIER-1: Blocking Phase Gate Evaluation (all unresolved)

**RS-01 — Harvey-Liu Formula Undefined (F-1, P0)**
- Why now: Any evaluation output (Phase 0 exit, Phase 1 OOS) citing "deflated Sharpe" is unverifiable without the formula. The formula choice also interacts with the new RDL trial counting rule (RDL trials count from submission). The Harvey-Liu trial budget is now larger and more complex than when F-1 was first identified.
- Evidence: CHARTER.md NN-5; PROTOCOL_SPEC.md NN-5, Phase 1 metrics; GLOSSARY.md; AUDIT_v1.md F-1

**RS-02 — Sharpe CI Arithmetic Error (F-2, P0)**
- Why now: The stated CI ±0.15–0.20 at 15 months OOS is wrong by factor 4–6×. With true CI ≈ ±0.89, the K1 threshold (0.28), pivot zone (0.22–0.28), and exit criterion are all statistically indistinguishable. No downstream decision using CI can be trusted until corrected.
- Evidence: PROTOCOL_SPEC.md Section C definition of Net Sharpe; CHARTER.md Section C; AUDIT_v1.md F-2

**RS-03 — P4 Algorithm Undefined (F-4, P0)**
- Why now: Phase 0 exit criterion requires "P4 produces historically labeled regime series covering ≥3 years." Phase 1 exit requires "≥2 distinct regime instances." Both are unverifiable without a P4 algorithm. RDL-2 (Market State Labeler) was added in v1.2 and explicitly depends on "P4 signal pre-registration spec (when defined per F-4 resolution)" — F-4 resolution is now a prerequisite for RDL-2 scaffolding to be meaningful.
- Evidence: PROTOCOL_SPEC.md Sections D, E; CHARTER.md Section D; AUDIT_v1.md F-4

**RS-04 — P3 Trigger Population Undefined (F-3, P0)**
- Why now: Phase 0 regime signal implementation (TASK-DEV-003) cannot begin without a locked P3 definition. Five plausible populations produce materially different trigger frequencies. Growth Layer addition in v1.1 may have added an additional candidate population (portfolio-level metrics), further expanding the ambiguity.
- Evidence: PROTOCOL_SPEC.md Section D; CHARTER.md Section D; AUDIT_v1.md F-3

**RS-05 — IC_long Unvalidated; No Suspect Threshold (F-5, P0)**
- Why now: At ρ_avg=0.40, FLAM gross ≈ 0.25 — below K1=0.28. With the corrected CI from RS-02, the system cannot distinguish a Phase 1 exit value of 0.25 from 0.28. The asymmetric treatment of IC_long vs. IC_short (IC_short has a >0.04 suspect threshold; IC_long has none) creates an undetectable false-positive Phase 1 certification path.
- Evidence: PROTOCOL_SPEC.md Section E (Equity Shorts), GLOSSARY.md; AUDIT_v1.md F-5

### TIER-2: P1 Findings — Required Before Phase 1 Entry

**RS-06 — P1+P3 Concurrent State Machine Undefined (F-10, P1)**
- Why now: Phase 0 implementation of regime signals (TASK-DEV-003) must encode all concurrent-firing states. Four specific unresolved states (A–D) have been identified. The Growth Layer (v1.1) monitoring mode during P1/P3 co-activation adds a fifth unaddressed state: what monitoring output does the Growth Layer produce when both P1 and P3 are active?
- Evidence: CHARTER.md Section D; PROTOCOL_SPEC.md Section D; ARCHITECT_BRIEF.md Section C; AUDIT_v1.md F-10

**RS-07 — Regime Label Vintage Contamination (F-7, P1)**
- Why now: P4 calibrates on ≥3 years historical data in Phase 0. RDL-2 Market State Labeler (v1.2) will produce `RegimeTag` objects using this same or related data. If P4 involves parameter fitting, the calibration window overlaps with Phase 1 IS windows. The F-4 resolution may affect the answer (a non-parametric P4 avoids this entirely; a model-based P4 does not).
- Evidence: PROTOCOL_SPEC.md Phase 0 exit criteria, Section E (RDL-2); ARCHITECT_BRIEF.md Section D; AUDIT_v1.md F-7

**RS-08 — SimBroker Cost Kill Criterion Gap in Phase 1 (F-9, P1)**
- Why now: K6 is only active from Phase 3–4. Phase 1 has a flag (>15% deviation for 2 consecutive months) but no kill action. The Growth Layer efficiency metrics (Section J1) were added in v1.1 — it is unclear whether these interact with or supplement the SimBroker cost monitoring, or create a new monitoring pathway that is also gap-covered.
- Evidence: CHARTER.md Kill Criteria Appendix, Phase 1 metrics; PROTOCOL_SPEC.md Sections F, J; AUDIT_v1.md F-9

**RS-09 — N_eff Formula Accuracy at K3 Boundary (F-11, P1)**
- Why now: Spec's own estimate N_eff≈2.4 in normal conditions is barely above K3=2.0. The equicorrelation formula gives N_eff=2.07 for the heterogeneous 3-cluster portfolio while eigenvalue-based gives 3.0 — this straddles K3. No formula choice has been documented. The Growth Layer may add a monitoring pathway that makes this more urgent by surfacing N_eff estimates without a specified formula.
- Evidence: PROTOCOL_SPEC.md Sections H, J1; GLOSSARY.md; AUDIT_v1.md F-11

**RS-10 — K4 Missed-Kill Probability Undocumented (F-6, P1)**
- Why now: K4 is miscalibrated in both directions: 60% false-kill + 31% missed-kill. The K4 t-statistic formula is also unspecified (F-15). These two unresolved items compound: the calibration claims are not even based on the correct formula.
- Evidence: CHARTER.md Correction 2, Kill Criteria Appendix; PROTOCOL_SPEC.md Phase 3, Section J; AUDIT_v1.md F-6, F-15

### TIER-3: New Risk Surfaces from v1.1/v1.2 (not in AUDIT_v1.md)

**RS-11 — Growth Layer RBE Activation Pathway Unaudited**
- Why now: PROTOCOL_SPEC.md Section J2 defines a Risk Budget Escalation (RBE) mechanism. The Growth Layer is "locked by default" — monitoring-only until an RBE step is "formally activated via charter-level review and preregistration in the trial registry." The RBE step activation criteria, the definition of "charter-level review," and the boundary conditions for Growth Layer's transition from monitoring to active mode are not audited anywhere. This is a new path from passive to active portfolio influence that was not present in the v1.0 spec.
- Evidence: PROTOCOL_SPEC.md Section E (Growth Layer), Section J1, Section J2

**RS-12 — RDL Trial Registry Counting Rule Creates Harvey-Liu Budget Inflation**
- Why now: PROTOCOL_SPEC.md Section E states "RDL hypothesis IDs are counted in the Harvey-Liu trial budget from the moment they are submitted to the Trial Registry — not from the moment they are promoted to Phase evaluation." If RDL-1 Hypothesis Generator becomes active (Phase 2+), the trial count grows during the scaffolding-to-operational transition. With F-1 unresolved (Harvey-Liu formula undefined), the trial count's effect on the haircut is doubly unverifiable. The interaction needs to be formally modeled.
- Evidence: PROTOCOL_SPEC.md Section E (RDL governance); CHARTER.md NN-5; AUDIT_v1.md F-1

**RS-13 — RDL-Phase Boundary Auditability Gap**
- Why now: The RDL "dormant until Phase 2" constraint is stated in policy (PROTOCOL_SPEC.md Section E, workflow_ai_development.md Section 6), and the audit pipeline auto-classifies Phase 0–1 RDL routing as P0. But there is no defined test or verification mechanism that a neutral third party could use to confirm that RDL submodules are operating in scaffolding-only mode during Phase 0–1. The constraint exists in specification but lacks an enforcement artifact.
- Evidence: PROTOCOL_SPEC.md Section E (RDL); docs/architecture/workflow_ai_development.md Section 6

**RS-14 — Growth Layer + RDL Interaction With Frozen Non-Negotiables**
- Why now: Both new modules introduce indirect paths to portfolio influence (Growth Layer via RBE activation; RDL via Trial Registry hypothesis promotion). Neither module's interaction with the four frozen non-negotiables (NN-1 through NN-6) has been formally reviewed. Specifically: (a) Can a Growth Layer escalation change gross leverage in ways that might approach the NN-1 limit? (b) Can RDL hypothesis promotion bypass NN-3 (Evaluation Engine First) if promoted before Phase 2 walk-forward harness integration?
- Evidence: PROTOCOL_SPEC.md Section B (NN-1 through NN-6), Section E (Growth Layer, RDL)

**RS-15 — RBE Step Interaction With Kill Criteria**
- Why now: PROTOCOL_SPEC.md Section J2 defines the RBE protocol. The kill criteria (K1–K6, P2K1–P2K2, P4K1–P4K2) were designed before the RBE existed. If an RBE step is activated (even legitimately, via charter-level review), it may change portfolio structure in ways that affect which kill criteria are active, their measurement windows, or their trigger states. No document addresses this interaction.
- Evidence: PROTOCOL_SPEC.md Section J (kill criteria), Section J2 (RBE); CHARTER.md Kill Criteria Appendix

### TIER-4: P2 Findings With Phase 0 Relevance

**RS-16 — Purge/Embargo Duration Undefined (F-12, P2)**
- Why now: A prerequisite for Phase 0 evaluation engine (TASK-DEV-004). "Proportional to maximum holding period" is not a formula. With RDL-3 Feature Library now defining versioned `FeatureSpec` objects, the purge/embargo question also applies to feature versioning — when a new feature version is introduced mid-walk-forward, what is the embargo?
- Evidence: ARCHITECT_BRIEF.md Section B; PROTOCOL_SPEC.md Phase 0 exit criteria, I Q4; AUDIT_v1.md F-12

**RS-17 — Timestamp Convention Leakage (F-17, P2)**
- Why now: Not in Phase 0 exit criteria. The RDL-4 Event Label Builder (v1.2) adds calendar and event data with potentially different timestamp conventions (UTC, exchange-local, session-relative). This expands the timestamp convention surface beyond what was evaluated in AUDIT_v1.md.
- Evidence: ARCHITECT_BRIEF.md Section F; PROTOCOL_SPEC.md Phase 0 exit criteria; AUDIT_v1.md F-17

**RS-18 — P3 Reduction Range Indeterminate (F-13, P2)**
- Why now: "Reduce gross exposure 35–50%" has no selection rule. With Growth Layer monitoring (v1.1), a P3 event will generate monitoring outputs. If Growth Layer monitors gross exposure, its output during a P3 event is indeterminate because the reduction target itself is indeterminate.
- Evidence: CHARTER.md Section D; PROTOCOL_SPEC.md Section D; AUDIT_v1.md F-13

---

## Downstream Prompt Index

| Step | Prompt File | Output Artifact | Reads (required) |
|---|---|---|---|
| Step 1 (Meta) | *(run manually; no prompt file — use review_pipeline.md Step 1 directly)* | `docs/audit/META_ANALYSIS.md` | All docs in docs/ |
| Step 2 (Arch) | `docs/audit/PROMPT_1_ARCH_REVIEW.md` | `docs/audit/ARCH_MODEL.md` | META_ANALYSIS.md + PROTOCOL_SPEC + CHARTER + GLOSSARY |
| Step 3 (Invariants) | `docs/audit/PROMPT_2_INVARIANTS.md` | `docs/audit/INVARIANTS.md` | ARCH_MODEL.md + PROTOCOL_SPEC + CHARTER + GLOSSARY |
| Step 4 (Drift) | `docs/audit/PROMPT_3_DRIFT_GUARD.md` | `DRIFT_ASSERTIONS.md` + `DRIFT_REPORT.md` | all docs + INVARIANTS.md |
| Step 5 (Adversarial) | `docs/audit/PROMPT_4_ADVERSARIAL.md` | `docs/audit/ADVERSARIAL_REVIEW.md` | ARCH_MODEL + INVARIANTS + DRIFT_REPORT + spec docs |
| Step 6 (Consolidated) | `docs/audit/PROMPT_5_CONSOLIDATED.md` | `docs/audit/REVIEW_REPORT.md` | all prior artifacts + tasks.md + AUDIT_INDEX.md |

---

## Hard Constraints (enforced in all downstream prompts)

1. No changes to frozen non-negotiables (NN-1 through NN-6), kill criteria, phase exit criteria, or metric thresholds.
2. Research-only; no live portfolio influence at any stage.
3. Trial Registry + preregistration + multiplicity rules remain mandatory; no loopholes.
4. RDL: treat as scaffolding/dormant until Phase 2 unless spec explicitly states otherwise.
5. Growth Layer: treat as monitoring-only until RBE activation is formally documented via charter-level review and preregistration.
6. All findings from this cycle are Draft until Spec Owner acceptance.
7. A finding may only move to Closed after a formal pipeline step confirms invariant passage.

---

*Cycle: 1 | Phase: 0 | Date: 2026-03-04 | Pipeline: v1.0*
*Next cycle trigger: Any P0 finding resolved (partial re-run Step 3+5) OR Phase 0→1 gate (full run)*
