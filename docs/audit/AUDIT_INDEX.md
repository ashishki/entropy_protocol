# Entropy Protocol — Audit Index

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/AUDIT_INDEX.md`
**Version:** 1.0
**Date:** 2026-03-04
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
| Meta Investigation | `docs/audit/META_ANALYSIS.md` | Step 1 |
| Architecture Review | `docs/audit/ARCH_MODEL.md` | Step 2 |
| Invariant Extraction | `docs/audit/INVARIANTS.md` | Step 3 |
| Drift Assertions | `docs/audit/DRIFT_ASSERTIONS.md` | Step 4 |
| Drift Report | `docs/audit/DRIFT_REPORT.md` | Step 4 |
| Adversarial Review | `docs/audit/ADVERSARIAL_REVIEW.md` | Step 5 |
| Consolidated Review | `docs/audit/REVIEW_REPORT.md` | Step 6 |

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

| Artifact | File | Status | Date | Cycle |
|---|---|---|---|---|
| Meta Investigation | `docs/audit/META_ANALYSIS.md` | — | Not yet run | — |
| Architecture Review | `docs/audit/ARCH_MODEL.md` | — | Not yet run | — |
| Invariant Extraction | `docs/audit/INVARIANTS.md` | — | Not yet run | — |
| Drift Assertions | `docs/audit/DRIFT_ASSERTIONS.md` | — | Not yet run | — |
| Drift Report | `docs/audit/DRIFT_REPORT.md` | — | Not yet run | — |
| Adversarial Review | `docs/audit/ADVERSARIAL_REVIEW.md` | — | Not yet run | — |
| Consolidated Review | `docs/audit/REVIEW_REPORT.md` | **Draft** | 2026-03-04 | Phase 0 baseline |

Note: `REVIEW_REPORT.md` was produced as a baseline consolidation from `docs/AUDIT_v1.md` before the pipeline's Step 1–5 artifacts were generated. Steps 1–5 artifacts are pending the first full formal pipeline run. See History section.

---

## History

### Cycle 0 — Phase 0 Baseline (2026-03-04)

**Trigger:** Initial governance setup — baseline consolidation of `docs/AUDIT_v1.md`.
**Type:** Baseline (pre-pipeline). Steps 1–5 not yet executed.
**Pipeline version:** v1.0

| Artifact | Versioned File | Status | Notes |
|---|---|---|---|
| Consolidated Review | `2026-03-04_phase0_REVIEW_REPORT_v1.md` | Draft | Baseline from AUDIT_v1.md. Steps 1–5 outputs pending. |
| Source Audit | `docs/AUDIT_v1.md` | Accepted | Primary input for baseline REVIEW_REPORT. External auditor document. |

**Spec Owner sign-off:** Pending.

**Next full-pipeline run:** Before Phase 0 → Phase 1 gate. All six steps must run in sequence.

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

---

*Version: 1.0 | Date: 2026-03-04*
