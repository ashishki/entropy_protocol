# Entropy Protocol — Final Research Question Pool

**Classification:** Confidential — Internal Audit Document
**Filename:** `docs/audit/QUESTION_POOL.md`
**Audit Cycle:** Cycle 1 — Phase 0 (Pre-Development)
**Date:** 2026-03-04
**Source Basis:** `ARCH_MODEL.md`, `INVARIANTS.md`, `DRIFT_REPORT.md`, `ADVERSARIAL_REVIEW.md`, `REVIEW_REPORT.md`

This pool is deduplicated and prioritized for impact on Phase 0/1 certification integrity.

## A. Critical Architecture Questions

### Q-ID: A-01
**Question:** What is the complete, reproducible P4 algorithm specification (inputs, features, thresholds/model class, calibration protocol, versioning, and label immutability rules)?
**Why it matters:** P4 is gate-critical for Phase 0->1 and Phase 1->2 and is also required by RDL-2; currently undefined and non-reproducible.
**Missing evidence:** No canonical algorithm artifact; only references to a future prereg spec.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/INVARIANTS.md`, `docs/audit/DRIFT_REPORT.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`, `docs/core/CHARTER.md`
**Suggested method:** design comparison
**Expected deliverable:** Versioned P4 spec annex with deterministic label-generation procedure and verification checklist.

### Q-ID: A-02
**Question:** What is the canonical P3 trigger definition (asset population, return interval, inclusion/exclusion rules), and what deterministic rule selects 35% vs 50% gross reduction?
**Why it matters:** P3 can materially change exposure and risk, but current wording allows implementation divergence.
**Missing evidence:** Population and reduction-selection function are not locked; metric protocol is ambiguous.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/INVARIANTS.md`, `docs/audit/DRIFT_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** invariant proof
**Expected deliverable:** Canonical P3 formula block with deterministic trigger/action pseudocode.

### Q-ID: A-03
**Question:** What is the deterministic state-machine behavior for concurrent and recovery cases across P1/P3/P4 (U1-U4 and ramp interruptions)?
**Why it matters:** Undefined concurrency rules create evaluation-vs-execution divergence during stress periods.
**Missing evidence:** No closed transition table for known unresolved states.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/INVARIANTS.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** threat model
**Expected deliverable:** Complete state-transition matrix with precedence, hysteresis, and recovery semantics.

### Q-ID: A-04
**Question:** How are P4 calibration windows and label vintages constrained to prevent contamination of Phase 1 OOS regime-span evidence?
**Why it matters:** Gate evidence can become invalid if label generation overlaps fitted windows without explicit exclusion rules.
**Missing evidence:** No vintage exclusion protocol tied to phase-gate certification.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/DRIFT_REPORT.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** invariant proof
**Expected deliverable:** Formal vintage-control policy for regime labels used in gate decisions.

## B. Governance & Protocol Integrity

### Q-ID: B-01
**Question:** Which Harvey-Liu/deflation variant is canonical, and how are trial counts aggregated across Main, AT, and `RDL-*` submission-time entries?
**Why it matters:** Deflation is mandatory and gate-affecting, but formula and aggregation scope are currently non-auditable.
**Missing evidence:** No canonical formula variant; no unambiguous cross-namespace aggregation rule.
**Recommended files for deep research:** `docs/audit/INVARIANTS.md`, `docs/audit/DRIFT_REPORT.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`, `docs/core/GLOSSARY.md`
**Suggested method:** literature check
**Expected deliverable:** Normative deflation specification with worked examples and registry-to-haircut reproducibility test.

### Q-ID: B-02
**Question:** What is the single canonical RDL operational boundary ("Phase 2+" vs "after Phase 2 exit") and how is pre-Phase-2 dormancy externally attested?
**Why it matters:** Conflicting boundary semantics create governance bypass risk and unverifiable claims.
**Missing evidence:** No machine-checkable dormancy artifact or unified boundary statement.
**Recommended files for deep research:** `docs/audit/DRIFT_REPORT.md`, `docs/audit/REVIEW_REPORT.md`, `docs/audit/ARCH_MODEL.md`, `docs/core/PROTOCOL_SPEC.md`, `docs/audit/review_pipeline.md`
**Suggested method:** threat model
**Expected deliverable:** Boundary rule + attestation schema (state flag, log contract, audit query).

### Q-ID: B-03
**Question:** What is the operational definition of "charter-level review" for RBE activation (authority, required artifact, storage, approval criteria)?
**Why it matters:** RBE transitions can alter live risk budget; undefined review process undermines auditability.
**Missing evidence:** No role/authority map and no required approval artifact schema.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/DRIFT_REPORT.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`, `docs/core/CHARTER.md`
**Suggested method:** design comparison
**Expected deliverable:** Governance control procedure and mandatory activation packet template.

### Q-ID: B-04
**Question:** How is the RDL->RBE non-interaction rule enforced, and how do RBE transitions preserve K1-K6 evaluation-window continuity?
**Why it matters:** Without strict segregation and window rules, risk-budget changes can distort kill-criteria outcomes.
**Missing evidence:** Non-interaction is not consistently propagated; window continuity under RBE is unspecified.
**Recommended files for deep research:** `docs/audit/DRIFT_REPORT.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** threat model
**Expected deliverable:** Enforceable segregation control plus K-window continuity policy across RBE events.

### Q-ID: B-05
**Question:** What bright-line rule classifies zero/near-zero persistent weighting as GE-2 allocation tuning vs GE-3 strategy modification?
**Why it matters:** Ambiguity can suppress trial counting and understate multiplicity.
**Missing evidence:** No deterministic threshold/duration rule for classification.
**Recommended files for deep research:** `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** invariant proof
**Expected deliverable:** Governance rule with examples and automated classification test cases.

## C. Research Methodology Risks

### Q-ID: C-01
**Question:** What is the correct Sharpe CI methodology at 15 months, and how should K1/Phase-1 thresholds be recalibrated given observed low discriminative power?
**Why it matters:** Existing CI arithmetic is wrong and makes K1 statistically weak.
**Missing evidence:** No canonical estimator protocol or power analysis in spec.
**Recommended files for deep research:** `docs/audit/DRIFT_REPORT.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`, `docs/core/CHARTER.md`
**Suggested method:** literature check
**Expected deliverable:** Recomputed CI standard, power table, and threshold-calibration note.

### Q-ID: C-02
**Question:** Which `N_eff` estimator is authoritative for K3 decisions, and how should boundary decisions be handled when estimator variance is high near threshold?
**Why it matters:** Different estimators can flip K3 decisions for the same portfolio.
**Missing evidence:** Conflicting formula references and no boundary-sensitivity policy.
**Recommended files for deep research:** `docs/audit/INVARIANTS.md`, `docs/audit/DRIFT_REPORT.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** design comparison
**Expected deliverable:** Locked K3 estimator spec + boundary adjudication rule.

### Q-ID: C-03
**Question:** What exact K4 t-statistic formula and error-control target (false-kill vs missed-kill) are normative?
**Why it matters:** K4 is currently a screening rule with high misclassification risk and formula ambiguity.
**Missing evidence:** No canonical t-stat definition, df/autocorrelation handling, or calibrated error target.
**Recommended files for deep research:** `docs/audit/INVARIANTS.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/CHARTER.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** invariant proof
**Expected deliverable:** Exact K4 computation protocol and calibration rationale.

### Q-ID: C-04
**Question:** What are canonical purge/embargo and timestamp-normalization standards for evaluation joins, event labels, and feature/version transitions?
**Why it matters:** Leakage controls remain under-specified, especially for RDL-3/RDL-4 integration.
**Missing evidence:** No explicit embargo function by timeframe and no timestamp convention standard.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/REVIEW_REPORT.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** threat model
**Expected deliverable:** Leakage-control appendix with embargo equations and timestamp contract.

## D. RDL Activation Risks

### Q-ID: D-01
**Question:** What is the deterministic Phase-2 activation policy for scaffolded RDL hypotheses (promotion queue, batch limits, and trial-count shock controls)?
**Why it matters:** Simultaneous promotion can cause multiplicity spikes and unstable gate interpretation.
**Missing evidence:** No transition policy from scaffolding backlog to operational evaluation.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** design comparison
**Expected deliverable:** Phase-boundary promotion policy with queueing and rate-limit rules.

### Q-ID: D-02
**Question:** How is RDL-2 prevented from producing semantically unstable `RegimeTag` outputs before and after P4 spec finalization/version changes?
**Why it matters:** RDL-2 semantics are coupled to unresolved P4; instability can invalidate downstream studies.
**Missing evidence:** No compatibility/versioning contract linking P4 versions to RDL-2 outputs.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/INVARIANTS.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** invariant proof
**Expected deliverable:** P4-to-RDL-2 compatibility matrix and migration protocol.

### Q-ID: D-03
**Question:** What hard isolation controls guarantee RDL outputs cannot influence routing/sizing or RBE inputs before allowed phase conditions are satisfied?
**Why it matters:** Policy-only separation is vulnerable without technical enforcement.
**Missing evidence:** No explicit runtime/data-path segregation mechanism with audit queries.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/INVARIANTS.md`, `docs/audit/DRIFT_REPORT.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** threat model
**Expected deliverable:** Isolation architecture spec with mandatory telemetry and compliance checks.

## E. Spec Ambiguities

### Q-ID: E-01
**Question:** What is the canonical net Sharpe stream composition everywhere (`a+b+c` vs `a+c`) and how is conformance enforced in all phase tables/reports?
**Why it matters:** Inconsistent metric scope can silently exclude short-side performance.
**Missing evidence:** Drift-confirmed wording mismatch across documents.
**Recommended files for deep research:** `docs/audit/DRIFT_REPORT.md`, `docs/audit/REVIEW_REPORT.md`, `docs/audit/INVARIANTS.md`, `docs/core/PROTOCOL_SPEC.md`, `docs/core/CHARTER.md`
**Suggested method:** invariant proof
**Expected deliverable:** Unified metric definition + conformance lint checklist for docs/reports.

### Q-ID: E-02
**Question:** What is the single canonical K3 temporal trigger wording (e.g., 2 consecutive months vs >=3 months monitoring precondition), and how should conflicts be resolved?
**Why it matters:** Divergent temporal rules produce different kill outcomes.
**Missing evidence:** Cross-document inconsistency on K3 timing conditions.
**Recommended files for deep research:** `docs/audit/DRIFT_REPORT.md`, `docs/audit/INVARIANTS.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/CHARTER.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** design comparison
**Expected deliverable:** Canonical K3 temporal grammar and conflict-resolution rule.

### Q-ID: E-03
**Question:** What is the explicit lifecycle topology for Phase 5 entry when Phase 4 is optional or bypassed?
**Why it matters:** Missing 4->5 gate expression creates governance confusion in treasury activation.
**Missing evidence:** No unambiguous topology statement in current spec set.
**Recommended files for deep research:** `docs/audit/DRIFT_REPORT.md`, `docs/audit/REVIEW_REPORT.md`, `docs/audit/ARCH_MODEL.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** design comparison
**Expected deliverable:** Updated phase topology map and gate dependency rule.

## F. Secondary Questions

### Q-ID: F-01
**Question:** What IC_long suspect-threshold policy should mirror IC_short governance, and how should FLAM arithmetic/correlation assumptions be standardized?
**Why it matters:** Over-optimistic long-edge assumptions can distort feasibility expectations.
**Missing evidence:** No IC_long suspect threshold; inconsistent FLAM supporting arithmetic.
**Recommended files for deep research:** `docs/audit/REVIEW_REPORT.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/core/PROTOCOL_SPEC.md`, `docs/core/CHARTER.md`
**Suggested method:** literature check
**Expected deliverable:** IC_long governance extension and corrected FLAM assumption note.

### Q-ID: F-02
**Question:** Should a Phase-1 analogue of K6 (SimBroker drift kill/hold) be formalized, and with what thresholds/actions?
**Why it matters:** Phase-1-only flagging may allow contaminated Phase 1 certification.
**Missing evidence:** No Phase-1 kill action despite known drift risk.
**Recommended files for deep research:** `docs/audit/ARCH_MODEL.md`, `docs/audit/REVIEW_REPORT.md`, `docs/core/CHARTER.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** design comparison
**Expected deliverable:** Phase-1 cost-drift control rule with stop/recalibration semantics.

### Q-ID: F-03
**Question:** What is the canonical matched-pair construction protocol for Phase-2 overlay evaluation?
**Why it matters:** Pairing ambiguity can change measured overlay delta and decisions.
**Missing evidence:** Matching/confounding controls remain under-specified.
**Recommended files for deep research:** `docs/audit/REVIEW_REPORT.md`, `docs/audit/ADVERSARIAL_REVIEW.md`, `docs/core/PROTOCOL_SPEC.md`
**Suggested method:** invariant proof
**Expected deliverable:** Reproducible matched-pair methodology specification.
