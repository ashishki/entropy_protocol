# Entropy Protocol — Official Audit Review Pipeline

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/review_pipeline.md`
**Pipeline Version:** v1.0
**Date:** 2026-03-04
**Owner:** Spec Owner / Staff-Level Systems Architect
**Status:** Active

---

## Purpose

This document defines the **canonical, reproducible audit pipeline** for the Entropy Protocol. It specifies:

- The mandatory execution order of audit steps
- The inputs and outputs for each step
- The artifact discovery rule (reuse vs. regenerate)
- The trigger conditions for running the pipeline
- Instructions for running each step as a separate agent session

No audit is complete unless all six steps have been executed and their outputs committed to `docs/audit/`.

---

## Artifact Discovery Rule

**Before each step begins, the executing agent must scan `docs/audit/` for existing artifacts matching the step's output filename(s).**

- If a current-cycle artifact is present (same date prefix or explicitly marked `CURRENT`): **reuse it** as context input for subsequent steps; do not regenerate unless explicitly instructed.
- If only a versioned historical artifact is present: **load it as prior context**, note its version in the output, and generate a fresh artifact for the current cycle.
- If no artifact is present: generate from scratch.

This rule prevents redundant regeneration and ensures later steps build on earlier findings rather than producing disconnected analyses.

---

## Trigger Conditions

Run the full pipeline (all six steps, in order) before:

1. **Phase transitions** — any phase gate decision (Phase 0→1, Phase 1→2, etc.)
2. **Major spec revisions** — any change to PROTOCOL_SPEC.md or CHARTER.md sections B, D, F, or J
3. **New layer additions** — adding any new module, signal type, or kill criterion
4. **Annual cadence** — full pipeline run at least once per 12-month period regardless of phase status
5. **Post-kill-criterion fire** — if any kill criterion fires, run the pipeline before deciding to halt or continue

Partial runs (individual steps) are permitted for targeted re-evaluation when a specific finding has been resolved or a specific module has changed. Partial runs must note which prior full-run cycle they reference.

---

## Pipeline Steps

### Step 1 — Meta Investigation

**Purpose:** Establish the document inventory, version history, authorship, and consistency of metadata across all spec documents. Identifies structural gaps (missing sections, stale references, broken cross-links) before substantive review begins.

**Inputs:**
- All documents in `docs/` (CHARTER.md, PROTOCOL_SPEC.md, GLOSSARY.md, EVOLUTION.md, audience briefs, README.md)
- Prior `META_ANALYSIS.md` if present (for diff against current state)

**Process:**
1. List all docs, their versions, dates, and supersedes/superseded-by chains.
2. Verify all cross-references (internal links, cited section numbers) are accurate.
3. Flag any document claiming to supersede another that still exists as active.
4. Record any vocabulary inconsistencies across documents.

**Output:** `docs/audit/META_ANALYSIS.md`

**Acceptance criterion:** Document inventory complete; all structural gaps enumerated; cross-reference consistency checked.

---

### Step 2 — Architecture Review

**Purpose:** Model the system's architecture from specifications only. Produce a structured representation of components, data flows, phase dependencies, and decision points. This becomes the structural reference for all subsequent steps.

**Inputs:**
- PROTOCOL_SPEC.md
- CHARTER.md
- GLOSSARY.md
- `META_ANALYSIS.md` (Step 1 output — required)

**Process:**
1. Extract the component inventory (modules, signals, layers, kill criteria, regime signals).
2. Map data flows: from raw data → feature store → skills → portfolio layer → evaluation engine.
3. Map phase dependencies: which components are phase-gated and at which exit criterion.
4. Identify integration points between the RDL scaffolding and production routing (Phase 2+ only).
5. Note any architectural assumptions not stated in the spec.

**Output:** `docs/audit/ARCH_MODEL.md`

**Acceptance criterion:** All major components named; phase-gate dependencies mapped; integration point assumptions stated.

---

### Step 3 — Invariant Extraction

**Purpose:** Extract all formal invariants that must hold throughout system operation — kill criteria, phase exit criteria, metric thresholds, frozen non-negotiables, and regime signal governance rules. Creates a machine-checkable reference list.

**Inputs:**
- PROTOCOL_SPEC.md (especially Sections B, D, F, J)
- CHARTER.md (Sections B, D, Kill Criteria Appendix)
- GLOSSARY.md
- `ARCH_MODEL.md` (Step 2 output — required)

**Process:**
1. Extract every kill criterion (K1–K6, P2K1–P2K2, P4K1–P4K2) as a structured rule: condition, measurement period, action, active phase.
2. Extract all phase exit criteria as structured assertions.
3. Extract all metric thresholds (Sharpe, CI bounds, N_eff, K4 t-stat, P3 ρ, etc.).
4. Extract frozen non-negotiables (NN-1 through NN-6) verbatim.
5. Extract regime signal governance rules (P1–P4 hierarchy, recovery hysteresis).
6. Flag any invariant that lacks a formula or has an ambiguous boundary condition.

**Output:** `docs/audit/INVARIANTS.md`

**Acceptance criterion:** Every kill criterion and phase exit criterion appears as a structured row. Ambiguous or formula-free invariants are flagged, not silently included.

---

### Step 4 — Protocol Drift Guard

**Purpose:** Compare the current specification against the invariants established in Step 3. Detect any drift between documented rules and their implementations or formulations across documents. Produce both a structured assertion list and a human-readable drift report.

**Inputs:**
- All docs in `docs/`
- `INVARIANTS.md` (Step 3 output — required)
- Prior `DRIFT_ASSERTIONS.md` and `DRIFT_REPORT.md` if present (for regression tracking)

**Process:**
1. For each invariant in INVARIANTS.md, verify it is stated consistently across all documents that reference it.
2. Identify cases where the same rule is worded differently across CHARTER.md, PROTOCOL_SPEC.md, and GLOSSARY.md.
3. Identify cases where a document claims an invariant is met that is not yet fully specified (e.g., "P4 produces labeled series" with no algorithm defined).
4. Identify cases where a recently added module (e.g., Growth Layer) introduces implicit changes to frozen invariants without a documented override.
5. Compare against prior `DRIFT_ASSERTIONS.md` to identify regressions (previously-passing invariants now failing) vs. new drift.

**Outputs:**
- `docs/audit/DRIFT_ASSERTIONS.md` — structured list: `[invariant_id] [PASS / FAIL / AMBIGUOUS] [evidence pointer]`
- `docs/audit/DRIFT_REPORT.md` — prose analysis of failures and ambiguities, severity-ranked

**Acceptance criterion:** Every invariant from Step 3 has a PASS/FAIL/AMBIGUOUS verdict. All FAIL and AMBIGUOUS items have evidence pointers (file + section).

---

### Step 5 — Adversarial Review

**Purpose:** Stress-test the specification against failure modes that do not surface in structural review. Challenge assumptions, test boundary conditions, and identify scenarios where the system would produce invalid results or miss kill criteria without any explicit rule violation.

**Inputs:**
- PROTOCOL_SPEC.md, CHARTER.md, GLOSSARY.md, EVOLUTION.md, ARCHITECT_BRIEF.md
- `ARCH_MODEL.md` (Step 2 output — required)
- `INVARIANTS.md` (Step 3 output — required)
- `DRIFT_REPORT.md` (Step 4 output — required)
- Prior `ADVERSARIAL_REVIEW.md` if present

**Process:**
1. For each underspecified formula or parameter (flagged in Steps 3–4): derive the correct value using first principles and compare to the stated value. Flag mismatches as CRITICAL or HIGH.
2. Test state machine transitions: identify all scenarios where two or more regime signals fire simultaneously or in sequence, and verify the spec has a defined recovery path for each.
3. Test kill criterion calibration: for each kill criterion, compute the false-kill and missed-kill rates at the stated threshold using the relevant statistical distribution. Flag if either exceeds 30%.
4. Identify evaluation-vs-execution divergence points: cases where the harness and paper trading might produce different outputs from the same inputs due to specification ambiguity.
5. Identify behavioral integrity gaps: cases where a solo developer can make unilateral decisions that affect protocol outcomes without triggering a governance rule.
6. Review each open question from prior audits: are they resolved or deferred? Flag unresolved items that block phase gating.

**Output:** `docs/audit/ADVERSARIAL_REVIEW.md`

**Acceptance criterion:** All formula-level derivations shown (not asserted). All state machine transitions tested. All kill criteria assessed for calibration. Behavioral integrity gaps named, not implied.

---

### Step 6 — Consolidated Review

**Purpose:** Synthesize findings from Steps 1–5 into a single actionable report. Group by severity, map to tasks, and state next actions with objective acceptance criteria.

**Inputs:**
- All prior step outputs (Steps 1–5) — all required
- Existing `docs/tasks.md` (to map findings to existing tasks or create new ones)
- Existing `docs/audit/AUDIT_INDEX.md` (to register this cycle)

**Process:**
1. Deduplicate: if a finding appears in both the Adversarial Review and the Drift Report, record it once with both evidence pointers.
2. Assign severity: P0 (system-invalidating, blocks phase gating), P1 (high-impact, required before next phase), P2 (medium-impact, documented gap, time-bounded remediation required).
3. For each P0/P1 finding: state the acceptance criterion (what spec change or test result closes the finding). Link to `docs/tasks.md` entry.
4. Produce "Converted Backlog Items" table mapping finding IDs to task IDs.
5. Update the "Converted Backlog Items" in `docs/tasks.md`.

**Output:** `docs/audit/REVIEW_REPORT.md`

**Acceptance criterion:** Every finding has a severity, evidence pointer, next action, and acceptance criterion. Every P0/P1 finding has a corresponding `docs/tasks.md` entry.

---

## How to Run This Pipeline

Each step is run as a **separate agent session**. This prevents context window contamination across steps and ensures each step produces a self-contained artifact.

### Session initialization (every step)

Load the following context before the step-specific documents:
1. `docs/README.md`
2. `docs/core/GLOSSARY.md`
3. `docs/audit/review_pipeline.md` (this document)
4. `docs/audit/AUDIT_INDEX.md`

### Step sequencing rules

- Steps must run **in order**: Step 2 cannot begin until Step 1's output is committed to `docs/audit/`.
- Each step must explicitly acknowledge the prior step's outputs in its header.
- Steps 5 and 6 must reference Steps 2, 3, and 4 outputs respectively (by filename + date of last modification).

### Artifact naming for this cycle

See `docs/audit/AUDIT_INDEX.md` for naming conventions. Canonical filenames (e.g., `REVIEW_REPORT.md`) are overwritten each full-pipeline cycle. Versioned snapshots (e.g., `2026-03-04_phase0_REVIEW_REPORT_v1.md`) are created by the Step 6 agent and registered in the History section of `AUDIT_INDEX.md`.

### Partial-run protocol

If re-running only Step 5 (Adversarial Review) after a finding is resolved:
1. The agent must load prior outputs from Steps 2, 3, and 4 as context.
2. The agent must note in the output header: "Partial run. Referencing [full-pipeline cycle date]."
3. Step 6 must be re-run after any partial run to refresh `REVIEW_REPORT.md`.

### RDL operational boundary

RDL boundary must be verified as phase-sliced:
- Phase 0-1: scaffolding only (contracts, datasets, logging).
- Phase 2 start: preregistered RDL generation + Trial Registry submission + harness evaluation allowed.
- Before Phase 2 exit: no portfolio/routing influence.
- After Phase 2 exit: routing influence only via explicit phase-gated rule.

Audit steps must verify this boundary is respected: any audit finding that identifies Phase 0–1 code making routing decisions or OOS claims via RDL is automatically classified P0.

Machine-checkable evidence requirements:
- Runtime `RDL_MODE` flag must exist and match phase policy.
- Certification query `pre_phase2_rdl_portfolio_reads` must return empty for pre-Phase-2 gates.
- Any prohibited RDL read attempt in Portfolio/RBE paths must emit a structured audit event.
- Promotion-policy checks must verify FIFO ordering, monthly cap, and shock-control pause logging.

---

*Pipeline Version: v1.0 | Date: 2026-03-04*
*Owner: Spec Owner — Staff-Level Systems Architect*
*Next full-pipeline run trigger: Phase 0 → Phase 1 gate*
