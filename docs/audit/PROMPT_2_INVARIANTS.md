# Entropy Protocol — Audit Step 3: Invariant Extraction (Agent Prompt)

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/PROMPT_2_INVARIANTS.md`
**Pipeline Step:** Step 3 — Invariant Extraction
**Cycle:** 5 (Phase 1D-K Archive-Only Baseline Deep Review)
**Date:** 2026-05-06
**Output artifact:** `docs/audit/INVARIANTS.md`

---

## Agent Instructions

You are a Staff-Level Quantitative Risk Analyst performing Step 3 (Invariant Extraction) of the Entropy Protocol audit pipeline. This is a research-and-analysis session. You do NOT implement code, fix issues, or modify specifications.

### Mandatory reads (load in order)

1. `docs/audit/PROMPT_0_META.md` — Cycle context and hard constraints
2. `docs/audit/review_pipeline.md` — Pipeline definition
3. `docs/audit/ARCH_MODEL.md` — **Step 2 required input**

**BLOCKED MODE CHECK:** If `docs/audit/ARCH_MODEL.md` does not exist or is labeled as incomplete, output:
```
BLOCKED: Step 2 artifact (ARCH_MODEL.md) is required before Step 3 can run.
Complete Step 2 and commit ARCH_MODEL.md before resuming.
```

Continue loading:

4. `docs/core/PROTOCOL_SPEC.md` — especially Sections B, D, F, J, J1, J2
5. `docs/core/CHARTER.md` — especially Sections B, D, Kill Criteria Appendix, Phase exit criteria
6. `docs/core/GLOSSARY.md`
7. `docs/audit/REVIEW_REPORT.md` (current consolidated status)

Archived Phase1A packets live under `docs/audit/archive/phase1a/`; open them
only if a current invariant requires historical boundary evidence.

---

## Task Definition

Produce `docs/audit/INVARIANTS.md` — an exhaustive, structured list of every formal invariant that must hold during system operation. This becomes the machine-checkable reference for Steps 4 and 5.

An **invariant** is any rule, threshold, condition, or constraint that:
- Is stated as mandatory ("must," "required," "non-negotiable," "always," "never"), OR
- Serves as a kill criterion, phase gate condition, or exit criterion, OR
- Constrains a metric, formula, or measurement procedure, OR
- Defines a governance or preregistration obligation

### Required invariant categories

#### Category A — Frozen Non-Negotiables (NN-1 through NN-6)

For each NN, record verbatim from PROTOCOL_SPEC.md Section B, then add:
- Applies from: Phase (first active phase)
- Check mechanism: How would a third party verify this holds?
- Known audit gap (if any): Reference RS-ID from PROMPT_0_META.md

#### Category B — Kill Criteria

For each kill criterion (K1–K6, P2K1–P2K2, P4K1–P4K2), record as a structured row:

| Kill ID | Condition formula / threshold | Measurement period | Active from phase | Action | Recovery condition | Formula complete? (Y/N/partial) | Open finding (if any) |
|---|---|---|---|---|---|---|---|

Criteria to cover:
- K1: Net OOS Sharpe < 0.28 after 15mo / ≥2 regimes → project kill
- K2: Costs > 50% gross simulated return for 2Q → cost kill
- K3: N_eff ≤ 2 for 2 consecutive months → factor collapse kill
- K4: Short t-stat < 0.5 after 18mo / ≥90 trades → retire shorts
- K5: Treasury > 60% total return in any 12-month period → strategic review
- K6: SimBroker short cost > 20% deviation 2 consecutive months → halt short development
- P2K1: Turnover increases with 1W overlay → retire overlay
- P2K2: False-trigger reduction < 10% after 6 months → retire overlay
- P4K1: Crypto funding drag > 2.5% NAV annualized trailing 3 months → pause crypto shorts
- P4K2: Combined short book Sharpe delta < 0 for 2 consecutive 6-month windows → retire crypto shorts

For each criterion: derive the false-kill and missed-kill rates at the stated threshold (show derivation, even if approximate). Flag if either rate exceeds 30%.

#### Category C — Phase Exit Criteria

For each phase gate (Phase 0→1, Phase 1→2, Phase 2→3, Phase 3→4, Phase 4→5), extract every stated exit condition and record:

| Phase Gate | Condition | Verifiable by third party? (Y/N) | Open finding blocking this gate (if any) |
|---|---|---|---|

For the Phase 0 exit criteria specifically, cover:
- Walk-forward harness completion + leakage audit
- SimBroker fill accuracy (within 15% on ≥100 fills)
- P4 historical label series (≥3 years, pre-registered algorithm)
- P1 circuit breaker test suite (minimum scenarios)
- Regime signal hierarchy implementation

#### Category D — Regime Signal Governance Invariants

For each regime signal (P1–P4):
- Trigger condition (exact formula / threshold)
- Action (exact, with magnitude if applicable)
- Recovery condition (exact formula / threshold)
- Conflict resolution rule (with precedence priority)
- Hysteresis requirement (explicit hysteresis window or "none")

Flag any rule that:
- Refers to a population that is not fully defined (RS-04)
- Depends on an algorithm that is not fully specified (RS-03)
- Has concurrent-firing states that produce undefined behavior (RS-06)

#### Category E — Metric and Formula Invariants

For each metric used in a kill criterion or phase gate decision, extract:
- Metric name (exact as in spec)
- Formula (verbatim from spec, or "not specified" if absent)
- Input data requirements
- Annualization convention (if applicable)
- Confidence interval formula and parameters
- Whether the formula is complete and implementable by a third party

Metrics to cover (minimum):
- Net Sharpe (formula, CI, annualization, streams included/excluded)
- Harvey-Liu Deflated Sharpe (formula variant, trial count input, haircut computation, cross-phase aggregation)
- IC_long and IC_short (with suspect thresholds and haircut rules)
- N_eff (formula variant: equicorrelation vs. eigenvalue-based; which is specified for K3?)
- FLAM gross Sharpe (BR_eff, IC, formula with N_eff correction)
- K4 t-statistic (formula variant; three candidates — which is specified?)
- P3 ρ (correlation metric: population, return interval, rolling window)
- K5 measurement window (rolling vs. calendar year)

#### Category F — Governance and Preregistration Invariants

- Trial Registry: rules for what must be pre-registered (GE-1, GE-2, GE-3 as defined in spec Section J1)
- Harvey-Liu trial budget: cross-phase aggregation rule, AT trial counting, RDL trial counting (from submission vs. promotion)
- GE-2/GE-3 boundary: bright-line rules for zero-weight, near-zero-weight, and cluster-cap edge cases
- RDL dormancy: constraints on Phase 0–1 RDL operation
- Growth Layer lock: monitoring-only status until RBE activation; RBE activation prerequisites
- Four-stream P&L separation: what constitutes streams (a), (b), (c), (d); what can and cannot be blended
- Behavioral integrity: solo-developer rules for self-certification, finding closure, spec changes

#### Category G — Dormant And Governed Module Invariants

**Growth Layer invariants:**
- Locked by default: what conditions allow unlock?
- RBE activation prerequisites: formula, conditions, governance requirements
- RBE interaction with kill criteria: which kill criteria apply during/after an RBE step?
- Monitoring output constraints: what can Growth Layer outputs influence in monitoring mode?

**RDL invariants:**
- Phase boundary: what is and is not permitted before Phase 2
- Trial Registry counting rule: when does the trial count begin for RDL-* hypotheses?
- RBE non-interaction: "RDL outputs must never feed into RBE step activation" — what does this mean concretely?
- FeatureSpec versioning: what triggers a new version? Does a new version require a new GE-3 registration?

---

## Flagging Rules

For every extracted invariant, assess:

1. **Formula completeness:** Is the formula or decision rule fully specified? If not, mark `FORMULA_MISSING` and reference the open finding (F-N) and task (TASK-AF-N) from REVIEW_REPORT.md.

2. **Ambiguous boundary condition:** Is there any threshold, population, or edge case that would produce different outcomes depending on implementation choice? Mark `AMBIGUOUS` and describe the ambiguity.

3. **Phase coverage gap:** Is the invariant specified for one phase but silent for another where it should logically apply? Mark `COVERAGE_GAP` with the specific phase range.

4. **Interaction risk:** Does this invariant interact with another invariant in a way that could produce contradictory requirements? Mark `INTERACTION_RISK` and identify both invariants.

---

## Output Requirements

Write the complete output to `docs/audit/INVARIANTS.md`. The file must:
- Begin with a header: `# Entropy Protocol — Invariant Registry` with cycle, date, and step status
- Organize invariants by category (A through G above)
- Number every invariant with a stable ID: `INV-[Category]-[N]` (e.g., `INV-B-K1`, `INV-D-P3`)
- Include every kill criterion and phase exit criterion as a structured row
- Flag every `FORMULA_MISSING`, `AMBIGUOUS`, `COVERAGE_GAP`, or `INTERACTION_RISK` item explicitly
- End with a summary count: total invariants extracted, count by flag type

Do NOT:
- Modify any specification document
- Resolve ambiguities by choosing an interpretation — state the ambiguity
- Assert a formula is correct without derivation
- Omit any kill criterion or phase exit criterion

---

*Cycle: 5 | Step: 3 (Invariant Extraction) | Pipeline: v1.0 | Date: 2026-05-06*
*Prior step required: Step 2 (ARCH_MODEL.md)*
*Next step: PROMPT_3_DRIFT_GUARD.md (reads INVARIANTS.md)*
