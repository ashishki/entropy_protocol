# Entropy Protocol — Audit Step 6: Consolidated Review (Agent Prompt)

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/PROMPT_5_CONSOLIDATED.md`
**Pipeline Step:** Step 6 — Consolidated Review
**Cycle:** 1 (Phase 0, Pre-Development)
**Date:** 2026-03-04
**Output artifact:** `docs/audit/REVIEW_REPORT.md` (+ backlog proposals for `docs/tasks.md`)

---

## Agent Instructions

You are a Staff-Level Systems Architect performing Step 6 (Consolidated Review) of the Entropy Protocol audit pipeline. You synthesize findings from Steps 1–5 into a single actionable report, update the task backlog, and register this cycle in AUDIT_INDEX.md.

**This is a research-and-analysis session. You do NOT implement code, fix issues, or modify specifications.**

### Mandatory reads (load ALL — all are required inputs)

1. `docs/audit/PROMPT_0_META.md` — Cycle context and hard constraints
2. `docs/audit/review_pipeline.md` — Pipeline definition
3. `docs/audit/META_ANALYSIS.md` — Step 1 output
4. `docs/audit/ARCH_MODEL.md` — Step 2 output
5. `docs/audit/INVARIANTS.md` — Step 3 output
6. `docs/audit/DRIFT_ASSERTIONS.md` — Step 4 output
7. `docs/audit/DRIFT_REPORT.md` — Step 4 output
8. `docs/audit/ADVERSARIAL_REVIEW.md` — Step 5 output

**BLOCKED MODE CHECK:** If any of the eight files above does not exist, output:
```
BLOCKED: All Steps 1–5 artifacts are required before Step 6 can run.
Missing: [list missing files]
Complete all prior steps before resuming Step 6.
```

Continue loading:

9. `docs/audit/REVIEW_REPORT.md` — Cycle 0 baseline (current canonical file; will be OVERWRITTEN by this step)
10. `docs/tasks.md` — Task registry; current backlog (will receive NEW ENTRIES proposed by this step)
11. `docs/audit/AUDIT_INDEX.md` — Artifact registry (will be UPDATED by this step)

---

## Task Definition

### Part 1 — Produce new `docs/audit/REVIEW_REPORT.md`

Overwrite the existing REVIEW_REPORT.md with a new consolidated report for Cycle 1. The Cycle 0 baseline content should be preserved as a "Prior Cycle Summary" section (one paragraph) rather than duplicated in full.

The new REVIEW_REPORT.md must contain:

#### Header
- Audit Cycle: Cycle 1, Phase 0 (first formal full-pipeline run)
- Pipeline version, date, step status (all six steps completed)
- Spec-of-record: PROTOCOL_SPEC.md v1.2, CHARTER.md v5.0
- Status: Draft (pending Spec Owner acceptance)

#### Executive Summary
- Total findings this cycle (inherited Open + new from Steps 1–5)
- Count by severity: P0 / P1 / P2
- Count by source: Inherited from Cycle 0 / New from Cycle 1 pipeline
- Summary of the dominant risk theme (update from Cycle 0 if the new analysis changes the framing)
- Specific statement of which phases are blocked and why

#### Finding Inventory

**Deduplication rule:** If a finding appears in DRIFT_REPORT.md, ADVERSARIAL_REVIEW.md, and/or ARCH_MODEL.md, record it once with evidence pointers to all sources. Do not create duplicate finding IDs.

**Numbering:** Inherited findings retain F-1 through F-21 IDs. New findings from this cycle use F-22 onward.

For each finding, record:
- Finding ID (F-N)
- Corresponding Task ID (TASK-AF-N or "NEW — propose TASK-AF-N" for new findings)
- Severity: P0 / P1 / P2
- Status: Open / Inherited-Open / Partial-Mitigation (if spec change partially addressed but not closed)
- Source: Cycle 0 (AUDIT_v1.md) / Cycle 1 (Step N: META/ARCH/INVARIANTS/DRIFT/ADVERSARIAL)
- Location: doc(s) + section(s)
- Evidence summary (2–4 sentences max)
- Impact category: (A) invalid performance claims / (B) incorrect kill decisions / (C) state corruption / (D) behavioral integrity gap
- Next action (specific: what document, what section, what type of change)
- Acceptance criterion (verifiable by a third party)

**Mandatory finding coverage:**
- All 21 inherited Open findings (F-1 through F-21) — confirm each remains Open (or document any partial mitigation found during Cycle 1 steps)
- All new findings identified by Steps 1–5 during this cycle
- At minimum, expect new findings in these areas (from PROMPT_0_META risk surfaces):
  - RS-11 (Growth Layer RBE activation pathway)
  - RS-12 (RDL trial budget inflation)
  - RS-13 (RDL phase boundary auditability)
  - RS-14 (new modules vs. frozen non-negotiables)
  - RS-15 (RBE + kill criteria interaction)

#### Converted Backlog Items Table

| Finding ID | Task ID | Severity | Status | Cycle introduced |
|---|---|---|---|---|

For new findings, the task IDs are proposed (format: "TASK-AF-NN — proposed") and will be finalized when committed to tasks.md.

#### Missing Evidence / Ambiguous Items

- List any finding where confidence is < High
- List any assumption made in the absence of authoritative evidence
- Flag if any audit step was unable to access a required document

#### Prior Cycle Summary

One paragraph: what the Cycle 0 baseline captured, how this cycle's pipeline run extends or modifies that picture.

#### Next Actions

1. Spec Owner: review and accept this REVIEW_REPORT (changes status from Draft to Accepted)
2. Author: respond to Open Questions that remain unresolved
3. Development: re-state Phase 0 gating conditions based on updated finding inventory
4. Governance: state when the next full or partial pipeline run is required

---

### Part 2 — Backlog Proposals for `docs/tasks.md`

Do NOT directly edit `docs/tasks.md`. Instead, produce a "Proposed tasks.md additions" section at the end of REVIEW_REPORT.md with:

For each new finding (F-22 onward from this cycle):
- Proposed task ID (TASK-AF-NN)
- Finding ID reference
- Severity
- Summary (≤20 words)
- Acceptance criterion (must be verifiable by a third party)
- Dependency notes (which existing tasks must be resolved first)

For any inherited finding where the acceptance criterion needs updating (e.g., because RDL/Growth Layer additions changed the scope): note the updated criterion.

---

### Part 3 — Update `docs/audit/AUDIT_INDEX.md`

Add a new History entry for Cycle 1 using the template from AUDIT_INDEX.md Section "Cycle N — Template."

**New History entry must include:**
- Trigger: First formal full-pipeline run (pre-development Phase 0)
- Type: Full pipeline run
- Pipeline version: v1.0
- All seven canonical artifacts listed with their versioned snapshot filenames (format: `2026-03-04_phase0_<ARTIFACT>_v2.md` — v2 because v1 was Cycle 0 baseline)
- Status: Draft for all
- Open findings count: reference to REVIEW_REPORT.md finding inventory
- Spec Owner sign-off: Pending

**Update "Latest Artifacts" table** with all seven canonical files now having Cycle 1 as their source cycle.

---

## Output Requirements

### REVIEW_REPORT.md
- Complete overwrite (Cycle 0 content preserved only as "Prior Cycle Summary" paragraph)
- Header clearly marks as Cycle 1, all six steps completed
- All 21 inherited findings present with confirmed Open status or noted partial mitigation
- All new findings present with stable F-N IDs
- "Proposed tasks.md additions" section at end
- Status: Draft

### AUDIT_INDEX.md
- History section: new Cycle 1 entry added (do not modify Cycle 0 entry)
- "Latest Artifacts" table: updated with Cycle 1 date for all seven artifacts
- Versioned snapshot filenames for all seven Cycle 1 artifacts listed

### Versioned Snapshots

The Step 6 agent is responsible for noting (in AUDIT_INDEX.md) the versioned snapshot filenames for all seven artifacts. The actual snapshot files may be created by the Spec Owner or a separate process — the Step 6 agent registers their intended names. Versioned snapshot format for this cycle:
- `2026-03-04_phase0_META_ANALYSIS_v2.md`
- `2026-03-04_phase0_ARCH_MODEL_v2.md`
- `2026-03-04_phase0_INVARIANTS_v2.md`
- `2026-03-04_phase0_DRIFT_ASSERTIONS_v2.md`
- `2026-03-04_phase0_DRIFT_REPORT_v2.md`
- `2026-03-04_phase0_ADVERSARIAL_REVIEW_v2.md`
- `2026-03-04_phase0_REVIEW_REPORT_v2.md`

(v2 because Cycle 0 produced v1 for REVIEW_REPORT; all other artifacts are first-time outputs in this cycle, but use v2 for consistency within the phase numbering convention.)

Do NOT:
- Self-certify any finding as Closed
- Modify docs/tasks.md directly (propose additions only)
- Modify any specification document
- Omit any inherited finding
- Downgrade a P0 to P1/P2 without explicit derivation showing the risk is reduced

---

*Cycle: 1 | Step: 6 (Consolidated Review) | Pipeline: v1.0 | Date: 2026-03-04*
*Prior steps required: All five (META_ANALYSIS, ARCH_MODEL, INVARIANTS, DRIFT_ASSERTIONS, DRIFT_REPORT, ADVERSARIAL_REVIEW)*
*This step OVERWRITES: docs/audit/REVIEW_REPORT.md*
*This step UPDATES: docs/audit/AUDIT_INDEX.md*
*This step PROPOSES (does not directly edit): docs/tasks.md additions*
