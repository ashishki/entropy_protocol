# Entropy Protocol — Audit Step 4: Protocol Drift Guard (Agent Prompt)

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/PROMPT_3_DRIFT_GUARD.md`
**Pipeline Step:** Step 4 — Protocol Drift Guard
**Cycle:** 1 (Phase 0, Pre-Development)
**Date:** 2026-03-04
**Output artifacts:** `docs/audit/DRIFT_ASSERTIONS.md` + `docs/audit/DRIFT_REPORT.md`

---

## Agent Instructions

You are a Staff-Level Quantitative Risk Analyst performing Step 4 (Protocol Drift Guard) of the Entropy Protocol audit pipeline. Your task is to compare invariants against all documents and detect inconsistencies, missing elements, and formulation drift.

### Mandatory reads (load in order)

1. `docs/audit/PROMPT_0_META.md` — Cycle context and hard constraints
2. `docs/audit/review_pipeline.md` — Pipeline definition
3. `docs/audit/INVARIANTS.md` — **Step 3 required input**

**BLOCKED MODE CHECK:** If `docs/audit/INVARIANTS.md` does not exist, output:
```
BLOCKED: Step 3 artifact (INVARIANTS.md) is required before Step 4 can run.
Complete Step 3 and commit INVARIANTS.md before resuming.
```

Continue loading:

4. `docs/core/PROTOCOL_SPEC.md`
5. `docs/core/CHARTER.md`
6. `docs/core/GLOSSARY.md`
7. `docs/core/EVOLUTION.md`
8. `docs/audience/ARCHITECT_BRIEF.md`
9. `docs/audience/TRADER_BRIEF.md`
10. `docs/audit/ARCH_MODEL.md`
11. `docs/audit/REVIEW_REPORT.md` (Cycle 0 — prior findings)
12. Prior `docs/audit/DRIFT_ASSERTIONS.md` and `docs/audit/DRIFT_REPORT.md` if present (check; none expected for Cycle 1)

---

## Task Definition

Produce two artifacts:
1. `docs/audit/DRIFT_ASSERTIONS.md` — structured verdict list (machine-checkable)
2. `docs/audit/DRIFT_REPORT.md` — prose analysis (severity-ranked, human-readable)

For every invariant in INVARIANTS.md, determine whether it is:
- **PASS** — stated consistently and completely across all documents that reference it
- **FAIL** — stated inconsistently, incompletely, or contradictorily across documents
- **AMBIGUOUS** — stated in one document but absent, weaker, or modified in another; or stated without a formula where a formula is required

---

## Drift Check Procedure

### Check 1 — Cross-Document Consistency

For each invariant in INVARIANTS.md:
1. Find every document that mentions the invariant's subject (metric name, module, threshold, or rule)
2. Compare the formulation in each document
3. Note any difference in wording, threshold value, formula, population, or applicability scope
4. Assign verdict: PASS / FAIL / AMBIGUOUS

Pay special attention to:
- Kill criteria: K1–K6, P2K1–P2K2, P4K1–P4K2 (compare CHARTER.md vs. PROTOCOL_SPEC.md vs. GLOSSARY.md)
- Regime signal rules (P1–P4): trigger thresholds, populations, recovery conditions (compare across all five documents)
- Sharpe CI: "±0.15–0.20" claim (CHARTER.md, PROTOCOL_SPEC.md, GLOSSARY.md — must all agree; also must be arithmetically correct)
- Harvey-Liu deflation: mandatory condition (net Sharpe < 0.40), formula specification, trial count rule (CHARTER.md NN-5, PROTOCOL_SPEC.md NN-5 + Phase 1 metrics, GLOSSARY.md)
- NN-1 through NN-6: compare CHARTER.md Section B vs. PROTOCOL_SPEC.md Section B
- RDL constraints: compare PROTOCOL_SPEC.md Section E vs. docs/architecture/workflow_ai_development.md Section 6

### Check 2 — Formula Completeness

For each invariant flagged `FORMULA_MISSING` or `AMBIGUOUS` in INVARIANTS.md:
1. Confirm that no formula exists in any of the loaded documents (it's possible a formula appears in GLOSSARY.md or EVOLUTION.md but not in the primary spec)
2. If a formula is found in any document but absent from PROTOCOL_SPEC.md: this is FAIL (drift toward fragmented specification)
3. If no formula is found anywhere: retain FORMULA_MISSING flag

### Check 3 — New Module Drift (v1.1/v1.2)

The Growth Layer and RDL were added after the source audit. Check specifically:

**Growth Layer drift:**
- Does Section J1 (Growth Layer metrics) introduce any new metric that is not defined in GLOSSARY.md?
- Does Section J2 (RBE protocol) use any threshold or formula that appears nowhere else?
- Does the phrase "charter-level review" appear in any document with a concrete definition of what that means?
- Does any Growth Layer monitoring output appear in any document other than PROTOCOL_SPEC.md Section E and J?

**RDL drift:**
- Does the RDL trial counting rule ("counted from submission") appear consistently in PROTOCOL_SPEC.md Section E and GLOSSARY.md?
- Is the "RDL-* namespace" defined in GLOSSARY.md and Trial Registry section?
- Does the "RDL outputs must never feed into RBE" constraint appear in docs/architecture/workflow_ai_development.md or any governance document, or only in PROTOCOL_SPEC.md?
- Do RDL-3 FeatureSpec versioning rules cross-reference or contradict the purge/embargo rules (F-12 / TASK-AF-012)?

### Check 4 — Regression Detection (vs. Cycle 0 findings)

For each P0/P1 finding from REVIEW_REPORT.md (F-1 through F-11):
1. Check whether any document in the current spec set has been modified to partially address the finding
2. If a partial fix exists: note it as PARTIAL_MITIGATION (not PASS; partial mitigations cannot change finding status without a full pipeline step)
3. If the finding has not been addressed at all: confirm FAIL status persists
4. If the spec change introduced for another purpose inadvertently worsened the finding: mark REGRESSION

### Check 5 — Phase Coverage

For each invariant, verify it is explicitly scoped to the correct phases. Flag:
- `COVERAGE_GAP_EARLY` — invariant not active in a phase where it should logically apply
- `COVERAGE_GAP_LATE` — invariant stated as active before it can be meaningfully evaluated
- Specifically: K6 (SimBroker drift) is active Phase 3–4 but RS-08 identifies a Phase 1 gap — verify this gap is correctly coded in INVARIANTS.md and no document claims otherwise

---

## DRIFT_ASSERTIONS.md Format

Each row:
```
| INV-ID | Invariant short name | PASS / FAIL / AMBIGUOUS | Evidence pointer (doc + section) | Prior cycle verdict | Regression? |
```

Add a summary row at the end:
```
| TOTAL | — | PASS: N | FAIL: N | AMBIGUOUS: N | — | Regressions: N |
```

Where INV-ID matches the stable ID from INVARIANTS.md.

---

## DRIFT_REPORT.md Format

Structure:

### Executive Summary
- Total verdicts by type
- Most critical FAIL items
- New FAIL items vs. prior cycle (Cycle 0 had no DRIFT_ASSERTIONS; treat all as new)
- Any regressions identified

### FAIL Findings (ordered by severity)

For each FAIL verdict:
- Invariant ID and name
- What was expected (from INVARIANTS.md)
- What was found (in each document)
- Specific discrepancy (wording, value, formula, scope)
- Phase-gate impact (which phase gate is blocked or contaminated?)
- Severity: P0 / P1 / P2
- Corresponding open finding from REVIEW_REPORT.md (if any) or "New finding"

### AMBIGUOUS Findings (ordered by severity)

For each AMBIGUOUS verdict:
- Invariant ID and name
- Source of ambiguity
- Resolution required (spec clarification, formula addition, scope statement)
- Severity: P0 / P1 / P2

### New Risk Surfaces Identified (Growth Layer / RDL)

Dedicated section for drift findings arising from the v1.1/v1.2 additions. For each:
- What rule or constraint exists in PROTOCOL_SPEC.md
- Whether it appears (consistently or inconsistently) in other documents
- Whether the rule is independently enforceable or requires judgment

### Scope of Next Actions

Map each FAIL/AMBIGUOUS verdict to:
- Required spec action (document, section, type of change)
- Whether the action modifies a frozen non-negotiable (must flag if yes — this is exceptional)
- Whether the action requires an ADR entry in EVOLUTION.md

---

*Cycle: 1 | Step: 4 (Drift Guard) | Pipeline: v1.0 | Date: 2026-03-04*
*Prior steps required: Steps 2–3 (ARCH_MODEL.md, INVARIANTS.md)*
*Next step: PROMPT_4_ADVERSARIAL.md (reads DRIFT_REPORT.md)*
