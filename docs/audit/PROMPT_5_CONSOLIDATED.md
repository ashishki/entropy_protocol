# Entropy Protocol — Audit Step 6: Consolidated Review (Agent Prompt)

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/PROMPT_5_CONSOLIDATED.md`
**Pipeline Step:** Step 6 — Consolidated Review
**Cycle:** 4 (Post-Phase-1A Scaffold Closure)
**Date:** 2026-05-05
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

9. `docs/audit/REVIEW_REPORT.md` — current consolidated status (will be OVERWRITTEN by this step)
10. `docs/tasks.md` — Task registry; current backlog (will receive NEW ENTRIES proposed by this step)
11. `docs/audit/AUDIT_INDEX.md` — Artifact registry (will be UPDATED by this step)
12. `docs/audit/PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md`
13. `docs/audit/POST_PHASE1A_STRATEGY_REVIEW.md`

---

## Task Definition

### Part 1 — Produce new `docs/audit/REVIEW_REPORT.md`

Overwrite the existing REVIEW_REPORT.md with a new consolidated report for
Cycle 4. Preserve the current report content as a "Prior Cycle Summary" section
(one paragraph) rather than duplicating it in full.

The new REVIEW_REPORT.md must contain:

#### Header
- Audit Cycle: Cycle 4, Post-Phase-1A Scaffold Closure
- Pipeline version, date, step status (all six steps completed)
- Spec-of-record: PROTOCOL_SPEC.md v1.8, CHARTER.md v5.3,
  GLOSSARY.md v1.4
- Status: Draft (pending Spec Owner acceptance)

#### Executive Summary
- Total findings this cycle (inherited Open + new from Steps 1–5)
- Count by severity: P0 / P1 / P2
- Count by source: Prior open / New from Cycle 4 pipeline
- Summary of the dominant risk theme and whether this cycle changes the current
  framing
- Specific statement of which phases are blocked and why

#### Finding Inventory

**Deduplication rule:** If a finding appears in DRIFT_REPORT.md, ADVERSARIAL_REVIEW.md, and/or ARCH_MODEL.md, record it once with evidence pointers to all sources. Do not create duplicate finding IDs.

**Numbering:** Existing findings retain their current IDs. New findings from
this cycle use the next available current-cycle ID.

For each finding, record:
- Finding ID (F-N)
- Corresponding Task ID (TASK-AF-N or "NEW — propose TASK-AF-N" for new findings)
- Severity: P0 / P1 / P2
- Status: Open / Inherited-Open / Partial-Mitigation (if spec change partially addressed but not closed)
- Source: Prior report / Cycle 4 (Step N: META/ARCH/INVARIANTS/DRIFT/ADVERSARIAL)
- Location: doc(s) + section(s)
- Evidence summary (2–4 sentences max)
- Impact category: (A) invalid performance claims / (B) incorrect kill decisions / (C) state corruption / (D) behavioral integrity gap
- Next action (specific: what document, what section, what type of change)
- Acceptance criterion (verifiable by a third party)

**Mandatory finding coverage:**
- All open findings in the current REVIEW_REPORT.md, including F-C3-007 if not
  closed before consolidation
- All new findings identified by Steps 1–5 during this cycle
- At minimum, explicitly cover the risk surfaces from PROMPT_0_META:
  - RS-01 through RS-03 claim and phase-gate containment
  - RS-04 through RS-05 architecture/runtime drift
  - RS-06 through RS-07 dormant module boundaries
  - RS-08 through RS-09 audit pipeline integrity

#### Converted Backlog Items Table

| Finding ID | Task ID | Severity | Status | Cycle introduced |
|---|---|---|---|---|

For new findings, the task IDs are proposed (format: "TASK-AF-NN — proposed") and will be finalized when committed to tasks.md.

#### Missing Evidence / Ambiguous Items

- List any finding where confidence is < High
- List any assumption made in the absence of authoritative evidence
- Flag if any audit step was unable to access a required document

#### Prior Cycle Summary

One paragraph: what the current REVIEW_REPORT captured before this run, how this
cycle's pipeline run extends or modifies that picture.

#### Next Actions

1. Spec Owner: review and accept this REVIEW_REPORT (changes status from Draft to Accepted)
2. Author: respond to Open Questions that remain unresolved
3. Development: re-state current gating conditions based on updated finding inventory
4. Governance: state when the next full or partial pipeline run is required

---

### Part 2 — Backlog Proposals for `docs/tasks.md`

Do NOT directly edit `docs/tasks.md`. Instead, produce a "Proposed tasks.md additions" section at the end of REVIEW_REPORT.md with:

For each new finding from this cycle:
- Proposed task ID (TASK-AF-NN)
- Finding ID reference
- Severity
- Summary (≤20 words)
- Acceptance criterion (must be verifiable by a third party)
- Dependency notes (which existing tasks must be resolved first)

For any existing finding where the acceptance criterion needs updating, note the
updated criterion.

---

### Part 3 — Update `docs/audit/AUDIT_INDEX.md`

Add or update the current-state entry for Cycle 4. The compact
`AUDIT_INDEX.md` may not have a historical history table; if so, update the
current-state fields and active artifact table instead of recreating archived
history.

**New History entry must include:**
- Trigger: Post-Phase-1A scaffold/probe closure and PSR-004 audit-readiness
  decision
- Type: Full pipeline run
- Pipeline version: v1.0
- All seven canonical artifacts listed with their versioned snapshot filenames
  if snapshots are used
- Status: Draft for all
- Open findings count: reference to REVIEW_REPORT.md finding inventory
- Spec Owner sign-off: Pending

**Update active artifacts/current-state tables** so they reflect Cycle 4.

---

## Output Requirements

### REVIEW_REPORT.md
- Complete overwrite (prior current content preserved only as "Prior Cycle Summary" paragraph)
- Header clearly marks as Cycle 4, all six steps completed
- All existing open findings present with confirmed status or noted partial mitigation
- All new findings present with stable F-N IDs
- "Proposed tasks.md additions" section at end
- Status: Draft

### AUDIT_INDEX.md
- Current-state fields updated for Cycle 4
- Active artifact table updated for all seven current artifacts
- Versioned snapshot filenames listed only if this cycle uses snapshots

### Versioned Snapshots

If snapshots are used, register intended filenames with a current date and
post-Phase-1A label. Do not create archive files unless the Spec Owner requests
snapshot archival.

Do NOT:
- Self-certify any finding as Closed
- Modify docs/tasks.md directly (propose additions only)
- Modify any specification document
- Omit any inherited finding
- Downgrade a P0 to P1/P2 without explicit derivation showing the risk is reduced

---

*Cycle: 4 | Step: 6 (Consolidated Review) | Pipeline: v1.0 | Date: 2026-05-05*
*Prior steps required: All five (META_ANALYSIS, ARCH_MODEL, INVARIANTS, DRIFT_ASSERTIONS, DRIFT_REPORT, ADVERSARIAL_REVIEW)*
*This step OVERWRITES: docs/audit/REVIEW_REPORT.md*
*This step UPDATES: docs/audit/AUDIT_INDEX.md*
*This step PROPOSES (does not directly edit): docs/tasks.md additions*
