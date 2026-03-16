# Entropy Protocol — AI Development Workflow

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/architecture/workflow_ai_development.md`
**Version:** 1.5
**Date:** 2026-03-16
**Owner:** Spec Owner / Staff-Level Systems Architect

---

## Purpose

This document defines development workflow policies for the Entropy Protocol, with a focus on governance, audit integration, and AI-assisted development constraints. It complements `docs/architecture/AI_ENGINEERING_FRAMEWORK.md`, which covers AI model roles and context-loading protocols.

---

## AI Research Pipeline

The AI-assisted research pipeline is:

Market Observation
↓
Hypothesis Generation
↓
Adversarial Review
↓
Experiment Proposal
↓
Human Registration
↓
Trial Registry
↓
Evaluation Engine

Rules:
- AI discovery output remains research-only until human registration occurs.
- The Research Firewall blocks direct entry from AI discovery into evaluation.
- The Experiment Readiness Gate must pass before registration.
- Hypothesis family and budget rules apply before activation.

---

## Audit Governance Policy

### 1. Audit Artifact Location

All audit artifacts live in `docs/audit/`. No audit output is placed in project root, `docs/archive/`, or any other location.

Canonical artifact filenames are defined in `docs/audit/AUDIT_INDEX.md`. Versioned snapshots use the naming convention `YYYY-MM-DD_phase<N>_<ARTIFACT>_v<N>.md`.

No audit artifacts should be placed outside `docs/audit/` for any reason, including convenience or staging.

### 2. Naming and Versioning Rules

- **Canonical files** (e.g., `REVIEW_REPORT.md`): overwritten each full pipeline cycle. Represent current state.
- **Versioned snapshots** (e.g., `2026-03-04_phase0_REVIEW_REPORT_v1.md`): permanent. Never deleted.
- Version number increments per phase, not globally. Phase 1's first full run produces `v1`; its second produces `v2`.
- Partial-run artifacts are named with `_partial_step<N>` suffix.

See `docs/audit/AUDIT_INDEX.md` for the complete naming specification.

### 3. Finding Lifecycle

Every finding produced by the audit pipeline has one of four statuses:

| Status | Meaning |
|---|---|
| **Open** | Finding identified; no remediation action taken. |
| **In Progress** | Remediation underway; corresponding task exists in `docs/tasks.md`. |
| **Mitigated** | Remediation implemented; acceptance criterion met; pending final audit verification. |
| **Closed** | Verified closed by a subsequent audit pipeline run. Must cite the closing audit cycle. |

- A finding may only move to **Closed** after a formal audit step (Step 3, 4, or 5 as appropriate) confirms the invariant now passes.
- A finding may not be self-closed by the developer without a pipeline re-run. This is non-negotiable.
- Closed findings must cite: the closing pipeline cycle date, the specific step that verified closure, and the evidence pointer.

### 4. P0/P1 Finding Requirements

Every **P0** and **P1** finding must:

1. Have a corresponding entry in `docs/tasks.md` (Audit Findings Backlog section) within 48 hours of the REVIEW_REPORT being marked Draft.
2. Link to the source finding in `docs/audit/REVIEW_REPORT.md` (or the versioned snapshot that introduced it).
3. Have an objective acceptance criterion — a statement that can be verified by a third party without access to the developer's judgment.
4. Reference an ADR (Architectural Decision Record) or PR if the remediation involves a spec change. If no ADR mechanism is in place, a dated comment in `docs/core/EVOLUTION.md` serves as the ADR reference.

No P0 finding may be in status Open when a phase gate is evaluated. A phase gate evaluation with any Open P0 finding is invalid.

**Current mandatory remediation set (Cycle 1):**
- In addition to baseline findings, remediation planning must explicitly include `TASK-AF-022` through `TASK-AF-032` from `docs/tasks.md` (sourced from `docs/audit/REVIEW_REPORT.md`, Cycle 1).
- For phase-gate readiness, these items are treated under the same governance rules as other P0/P1 findings in this section.

### 5. No Spec Change Without Audit/ADR Reference

**Policy statement:** No change to `docs/core/PROTOCOL_SPEC.md`, `docs/core/CHARTER.md`, or `docs/core/GLOSSARY.md` is accepted without one of the following:

- A reference to an open audit finding (by finding ID, e.g., "Resolves F-1") that the change addresses, OR
- A new ADR entry in `docs/core/EVOLUTION.md` (for architectural decisions) or an equivalent dated record

Changes that affect frozen non-negotiables (Sections B, kill criteria, phase exit criteria, metric thresholds) additionally require:

- Explicit confirmation that the change does NOT modify any frozen non-negotiable (or, if it does, a full justification as to why a freeze override is warranted — this is an exceptional action requiring separate review)

This policy applies to all changes regardless of whether the change was AI-generated or human-authored.

### 6. RDL Operational Gating

RDL boundary is phase-sliced and machine-checkable (see `docs/core/PROTOCOL_SPEC.md` Section E):
- **Phase 0-1:** scaffolding only.
- **Phase 2 start:** pre-registered RDL hypothesis generation, Trial Registry submission, and harness evaluation permitted.
- **Before Phase 2 exit:** portfolio/routing influence remains prohibited.
- **After Phase 2 exit:** routing influence can be enabled only through explicit phase-gated policy path.
- **Multiplicity accounting:** `RDL-*` entries are counted in the Harvey-Liu trial budget at submission time, not promotion time.

Permitted in Phase 0–1:
- Defining RDL contracts (interfaces, schemas, data types)
- Creating datasets and logging infrastructure
- Writing non-routing RDL components (data ingestion, feature computation)

Not permitted in Phase 0–1:
- Any RDL-based routing decision (directing signals to portfolio layer)
- Any OOS performance claim derived through RDL evaluation paths
- Any shortcut evaluation using RDL that bypasses the walk-forward harness
- Any kill criterion evaluation using RDL outputs instead of SimBroker outputs

Any audit finding that identifies Phase 0–1 code making routing decisions or OOS claims via RDL is automatically classified **P0** and blocks Phase 1 entry.

Mandatory attestation and evidence:
- Runtime mode flag `RDL_MODE` must be present (`scaffold_only`, `eval_enabled`, `portfolio_disabled`, `portfolio_enabled`).
- Certification query `pre_phase2_rdl_portfolio_reads` must return empty for pre-Phase-2 gates.
- Any attempted RDL read from Portfolio/RBE code paths in prohibited phases must emit a structured audit event.

Phase 2 RDL promotion governance:
- Promotion order defaults to FIFO by Trial Registry submission timestamp.
- Monthly cap: max 3 new `RDL-*` promotions into active evaluation per calendar month.
- Shock-control: if `M_total` grows by >10 over rolling 30 days, pause new promotions until haircut-impact note is logged.

Research governance controls:
- The Research Firewall requires explicit human registration before any AI-generated research artifact enters evaluation.
- The Experiment Readiness Gate blocks incomplete proposals from entering the Trial Registry.
- Hypothesis family assignment is mandatory before registration.
- Baseline hypothesis budget is max 3 new hypotheses per week and max 1 active hypothesis per family.

### 7. Audit Pipeline Execution

The full audit pipeline is defined in `docs/audit/review_pipeline.md`. Key governance requirements:

- The full pipeline must run before any phase gate decision.
- Each pipeline step runs as a separate agent session (prevents context contamination).
- The `REVIEW_REPORT.md` must be accepted by the Spec Owner before a phase gate is declared.
- Partial pipeline runs are permitted for targeted re-evaluation but do not replace a full run for phase gate purposes.

### 8. AI-Generated Audit Outputs

Audit artifacts produced by AI models (Claude or equivalent) are subject to the same governance rules as human-produced artifacts.

- AI-generated audit artifacts are always status **Draft** until Spec Owner review.
- AI models must not self-certify findings as Closed. Closure requires a subsequent pipeline step.
- If an AI model identifies a contradiction with a frozen non-negotiable, it must flag the contradiction and halt — not attempt to resolve it unilaterally.

### 9. Charter-Level Review Artifact (RBE Activations)

For any RBE activation above Step 0, a mandatory `RBE Activation Packet` is required before activation:
- proposer
- approver(s)
- requested step
- preregistration ID
- metric snapshot
- expected impact
- rollback conditions
- effective date

Storage rule:
- Packet is written to append-only governance storage.
- Packet hash is referenced in the linked Trial Registry entry.
- Approver cannot be the sole proposer for the same activation.

---

## Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-03-04 | Initial creation. Audit Governance Policy (Sections 1–8). |
| 1.1 | 2026-03-04 | Section 6: added cross-reference to PROTOCOL_SPEC.md Section E for RDL dormancy definition. |
| 1.2 | 2026-03-04 | Section 4: added explicit Cycle 1 mandatory remediation set reference (`TASK-AF-022..032`). |
| 1.3 | 2026-03-04 | Section 6 boundary matrix + machine-checkable RDL attestation; Section 9 adds mandatory RBE Activation Packet policy. |
| 1.4 | 2026-03-04 | Section 6: added Phase-2 RDL promotion governance baseline (FIFO/cap/shock-control). |
| 1.5 | 2026-03-16 | Added AI research pipeline and explicit Research Firewall / readiness gate / hypothesis budget references. |

---

*Version: 1.5 | Date: 2026-03-16*
*See also: `docs/architecture/AI_ENGINEERING_FRAMEWORK.md` (AI model roles, context loading), `docs/audit/review_pipeline.md` (pipeline execution), `docs/audit/AUDIT_INDEX.md` (artifact registry)*
