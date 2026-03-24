# Entropy Protocol — Meta Investigation

**Classification:** Confidential — Internal Audit Document
**Filename:** `docs/audit/META_ANALYSIS.md`
**Audit Cycle:** Cycle 1 — Phase 0, Pre-Development
**Pipeline Step:** Step 1 — Meta Investigation
**Pipeline Version:** v1.0
**Date:** 2026-03-04
**Status:** Draft — Awaiting Spec Owner Acceptance
**Prior cycle META_ANALYSIS:** None (first formal pipeline run)
**Full run / Partial run:** Full run

---

## Purpose

This artifact is the output of Step 1 (Meta Investigation) of the audit pipeline. It establishes the document inventory, version history, supersedes chains, cross-reference consistency, and vocabulary status across all active specification documents. It is the required input for Step 2 (Architecture Review).

---

## 1. Document Inventory

### 1.1 Active Core Documents

| Document | Version | Date | Status | Supersedes | Author / Source |
|---|---|---|---|---|---|
| `docs/README.md` | — (no version header) | 2026-03-04 | Active | — | Internal |
| `docs/core/CHARTER.md` | 5.0 | 2026-03-02 | Active | `strategic_charter_v5.md` (claimed archived) | Internal |
| `docs/core/PROTOCOL_SPEC.md` | 1.2 | 2026-03-04 | Active | `entropy_protocol_master_spec_v1.md` (claimed archived) | Internal |
| `docs/core/GLOSSARY.md` | 1.0 | 2026-03-04 | Active | — | Internal |
| `docs/core/EVOLUTION.md` | 1.0 | 2026-03-04 | Active | — | Internal |
| `docs/architecture/AI_ENGINEERING_FRAMEWORK.md` | 1.0 | 2026-03-04 | Active | — | Internal |
| `docs/architecture/workflow_ai_development.md` | 1.0 (header) / 1.1 (change log) | 2026-03-04 | Active | — | Internal |
| `docs/tasks.md` | 1.0 | 2026-03-04 | Active | — | Internal |
| `docs/audience/ARCHITECT_BRIEF.md` | 1.0 | 2026-03-02 | Active | — | Internal |
| `docs/audience/TRADER_BRIEF.md` | 1.0 | 2026-03-02 | Active | — | Internal |
| `docs/audit/AUDIT_v1.md` | 1.0 | 2026-03-04 | Accepted (external audit) | — | External auditor |

### 1.2 Active Audit Documents

| Document | Version | Date | Status |
|---|---|---|---|
| `docs/audit/review_pipeline.md` | 1.0 | 2026-03-04 | Active |
| `docs/audit/AUDIT_INDEX.md` | 1.1 | 2026-03-04 | Active |
| `docs/audit/REVIEW_REPORT.md` | — (Cycle 0 baseline) | 2026-03-04 | Draft |
| `docs/audit/PROMPT_0_META.md` | — (Cycle 1) | 2026-03-04 | Draft |
| `docs/audit/PROMPT_1_ARCH_REVIEW.md` | — (Cycle 1) | 2026-03-04 | Draft |
| `docs/audit/PROMPT_2_INVARIANTS.md` | — (Cycle 1) | 2026-03-04 | Draft |
| `docs/audit/PROMPT_3_DRIFT_GUARD.md` | — (Cycle 1) | 2026-03-04 | Draft |
| `docs/audit/PROMPT_4_ADVERSARIAL.md` | — (Cycle 1) | 2026-03-04 | Draft |
| `docs/audit/PROMPT_5_CONSOLIDATED.md` | — (Cycle 1) | 2026-03-04 | Draft |
| `docs/audit/QUESTION_POOL.md` | — (Cycle 1) | 2026-03-04 | Draft |

### 1.3 Archive Documents (NOT active; for reference only)

| Document | Notes |
|---|---|
| `docs/archive/strategic_architecture_review_v1.md` | Historical reasoning v1 |
| `docs/archive/strategic_architecture_review_v2.md` | Historical reasoning v2 |
| `docs/archive/strategic_architecture_review_v3.md` | Historical reasoning v3 |
| `docs/archive/strategic_architecture_review_v4.md` | Historical reasoning v4 — source of v4 corrections |
| `docs/archive/deep-research-report.md` | Literature validation |
| `docs/archive/README.md` | Archive index |

**Archive gap noted:** CHARTER.md states it supersedes `strategic_charter_v5.md` (archived). PROTOCOL_SPEC.md states it supersedes `entropy_protocol_master_spec_v1.md` (archived). Neither of these filenames appears in the `docs/archive/` directory. The archive folder contains `strategic_architecture_review_v*.md` documents (reviews, not charter documents). Whether the claimed superseded files exist under different names or were not preserved cannot be confirmed from the filesystem alone.

---

## 2. Supersedes Chains

| Current Document | Supersedes | Superseded Document Location | Gap Status |
|---|---|---|---|
| `CHARTER.md` v5.0 | `strategic_charter_v5.md` | Claimed archived; not found in `docs/archive/` | **GAP: superseded file not located** |
| `PROTOCOL_SPEC.md` v1.2 | `entropy_protocol_master_spec_v1.md` | Claimed archived; not found in `docs/archive/` | **GAP: superseded file not located** |
| `CHARTER.md` v5.0 | v4.0 audit findings | `docs/archive/strategic_architecture_review_v4.md` | Confirmed present |
| All other documents | No prior versions in archive | — | N/A |

**CHARTER.md v5.0 basis chain:**
CHARTER.md v5.0 states: "Basis: v2.0 findings, v3.0 extensions, v4.0 audit (authoritative corrections applied)." The v4.0 audit source is `docs/archive/strategic_architecture_review_v4.md` — present. v2.0 and v3.0 sources correspond to `strategic_architecture_review_v2.md` and `v3.md` respectively — both present.

**PROTOCOL_SPEC.md basis chain:**
PROTOCOL_SPEC.md v1.2 states: "Basis: CHARTER.md v5.0 (strategic constraints) + v4 audit (authoritative corrections applied)." Both CHARTER.md v5.0 and the v4 audit source are present.

---

## 3. Version State Summary and Deltas

### 3.1 PROTOCOL_SPEC.md Version History (from header)

| Version | Date | Change Summary | Scope impact |
|---|---|---|---|
| v1.0 | Pre-2026-03-04 | Original spec; not explicitly dated; superseded | Baseline |
| v1.1 | 2026-03-04 | Added Growth Layer module (Section E), Growth Layer & Efficiency Metrics (Section J1), Risk Budget Escalation Protocol (Section J2) | **New module, new metrics, new governance pathway** |
| v1.2 | 2026-03-04 | Added Research Discovery Layer (RDL) module (Section E) with four submodules | **New module, new trial registry namespace, new Phase 2 gate** |

**Critical observation:** Both v1.1 and v1.2 state: "Section B (Frozen Non-Negotiables), all kill criteria, all phase exit criteria, and all metric thresholds are unchanged." However, v1.1 adds Section J2 (RBE protocol) and v1.2 adds RDL trial counting rules — both introduce new governance mechanisms that interact with kill criteria and phase gates. The header assertion that "all kill criteria are unchanged" is narrowly accurate but does not address the new interactions.

### 3.2 CHARTER.md: Not Updated Post-v1.1/v1.2

CHARTER.md v5.0 is dated 2026-03-02 — two days before PROTOCOL_SPEC.md v1.2 (2026-03-04). Neither the Growth Layer, the RBE protocol, nor the RDL module appears anywhere in CHARTER.md v5.0. The charter is the strategic authority for the project; additions to PROTOCOL_SPEC.md that are not reflected in CHARTER.md operate outside the documented strategic mandate.

This is the most significant structural gap in the document set.

---

## 4. Cross-Reference Consistency Check

### 4.1 Inter-Document References Verified

| Reference point | Source document | Target | Consistent? | Notes |
|---|---|---|---|---|
| PROTOCOL_SPEC.md "Basis: CHARTER.md v5.0" | PROTOCOL_SPEC.md header | CHARTER.md v5.0 | ✓ Yes | Charter version matches |
| PROTOCOL_SPEC.md "Supersedes: entropy_protocol_master_spec_v1.md" | PROTOCOL_SPEC.md header | Not found in archive | **✗ GAP** | Archive file absent |
| CHARTER.md "Supersedes: strategic_charter_v5.md" | CHARTER.md header | Not found in archive | **✗ GAP** | Archive file absent |
| ARCHITECT_BRIEF.md footer companion doc reference | ARCHITECT_BRIEF.md | `entropy_protocol_master_spec_v1.md` | **✗ STALE** | File superseded; PROTOCOL_SPEC.md is canonical |
| ARCHITECT_BRIEF.md footer companion doc reference | ARCHITECT_BRIEF.md | `entropy_protocol_trader_review_v1.md` | **✗ STALE** | File superseded or renamed; TRADER_BRIEF.md is canonical |
| AI_ENGINEERING_FRAMEWORK.md context loading shortcut | AI_ENGINEERING_FRAMEWORK.md Section 3 | "PROTOCOL_SPEC.md v1.1" | **✗ STALE** | Current version is v1.2 |
| EVOLUTION.md Section 1 current rule pointer | EVOLUTION.md | "PROTOCOL_SPEC.md NN-3, Phase 0 section" | ✓ Yes | NN-3 present in PROTOCOL_SPEC.md Section B |
| EVOLUTION.md Section 6 current rule pointer | EVOLUTION.md | "PROTOCOL_SPEC.md Phase 3 (IC_short assumption section)" | ✓ Yes | Present |
| EVOLUTION.md Section 7 current rule pointer | EVOLUTION.md | "PROTOCOL_SPEC.md Phase 3, K4 definition" | ✓ Yes | Present |
| GLOSSARY.md "all terms in PROTOCOL_SPEC and CHARTER are defined here" | GLOSSARY.md header | All terms in active specs | **✗ INCOMPLETE** | Multiple terms missing (see Section 5.4) |
| CHARTER.md Section D references "v2 single authoritative regime signal principle" | CHARTER.md | EVOLUTION.md Section 5 | ✓ Yes | EVOLUTION.md Section 5 documents this decision |
| AUDIT_INDEX.md references `docs/audit/AUDIT_v1.md` | AUDIT_INDEX.md | `docs/audit/AUDIT_v1.md` | ✓ Yes | File present |
| review_pipeline.md "Next full-pipeline run trigger: Phase 0 → Phase 1 gate" | review_pipeline.md | Cycle 1 pipeline (this run) | Note | Being executed now |

### 4.2 Intra-Document Section References Verified

| Document | Section reference | Target section | Consistent? |
|---|---|---|---|
| PROTOCOL_SPEC.md Section E (RDL-2) | "P4 signal pre-registration spec (when defined per F-4 resolution)" | PROTOCOL_SPEC.md Section E P4 spec | **✗ BROKEN** | Referenced spec does not exist |
| PROTOCOL_SPEC.md Section E (RDL) | "Phase 2 exit criteria met before any RDL output influences portfolio routing" | PROTOCOL_SPEC.md Phase 2 exit criteria | ✓ Yes | Criteria present |
| PROTOCOL_SPEC.md Section E (Growth Layer) | "Section J1, J2" for metrics and RBE | PROTOCOL_SPEC.md J1, J2 | ✓ Yes | Both sections present |
| CHARTER.md Phase 1 kill criteria | "K1, K2, K3" | CHARTER.md Kill Criteria Appendix | ✓ Yes | All three present in appendix |
| CHARTER.md Phase 2 exit criteria | "P2K1, P2K2" | CHARTER.md Kill Criteria Appendix | ✓ Yes | Both present |
| CHARTER.md Phase 4 kill criteria | "P4K1, P4K2, K6" | CHARTER.md Kill Criteria Appendix | ✓ Yes | All present |
| ARCHITECT_BRIEF.md Section C "Known Gap" | "nested recovery sequencing" | PROTOCOL_SPEC.md Section D | **✗ UNRESOLVED** | Gap acknowledged but no spec rule added |

### 4.3 Section Number / Letter References

| Claim | Source | Status |
|---|---|---|
| PROTOCOL_SPEC.md "especially Sections B, D, F, J" cited in pipeline | review_pipeline.md Step 2 | ✓ Sections B, D, F, J all present in PROTOCOL_SPEC.md |
| PROTOCOL_SPEC.md "Section I, Q1–Q14" (open questions) | AUDIT_v1.md | ✓ Section I with open questions present |
| PROTOCOL_SPEC.md "Section H1: N_eff ≈ 2.4" | AUDIT_v1.md F-5 | ✓ PROTOCOL_SPEC.md Section H present; N_eff reference confirmed |
| CHARTER.md "Section D" for regime governance | EVOLUTION.md Section 5 | ✓ CHARTER.md Section D (Regime Signal Governance) present |

---

## 5. Identified Issues

### 5.1 Structural Gaps (GAP — require tracking)

**MG-01 — CHARTER.md Not Updated for v1.1/v1.2 Additions**
- Severity: P0 (impacts governance authority of new modules)
- Detail: PROTOCOL_SPEC.md v1.1 added Growth Layer (Section E, J1, J2). v1.2 added RDL (Section E). Neither addition appears in CHARTER.md v5.0. CHARTER.md is the strategic authority — additions to PROTOCOL_SPEC that bypass charter-level treatment operate without documented strategic mandate. The Growth Layer's RBE activation pathway and RDL's trial registry counting rule both affect frozen-adjacent governance mechanisms. Requires either: (a) CHARTER.md update to acknowledge these modules and their constraints, or (b) explicit documentation that these modules are implementation-layer additions exempt from charter-level review (with justification).
- Evidence: CHARTER.md v5.0 dated 2026-03-02; PROTOCOL_SPEC.md v1.2 dated 2026-03-04; no Growth Layer or RDL text in CHARTER.md.
- RS reference: RS-11, RS-12, RS-13, RS-14

**MG-02 — EVOLUTION.md Missing Rationale for Growth Layer and RDL**
- Severity: P1 (impacts future decision-making; design history incomplete)
- Detail: EVOLUTION.md documents design decisions through Section 11 (CCA constraint, resolved in v1–v5). No section covers Growth Layer (added v1.1) or RDL (added v1.2). The stated purpose of EVOLUTION.md is to "prevent re-litigation of resolved questions." Without recorded rationale, the design intent of these modules is undocumented and cannot be defended against challenge.
- Evidence: EVOLUTION.md Section 11 is the most recent entry; no Section 12+ exists.

**MG-03 — Claimed Superseded Files Not Found in Archive**
- Severity: P2 (operational; historical record incomplete)
- Detail: CHARTER.md claims to supersede `strategic_charter_v5.md` (archived) and PROTOCOL_SPEC.md claims to supersede `entropy_protocol_master_spec_v1.md` (archived). Neither file was found in `docs/archive/`. The archive contains `strategic_architecture_review_v1.md` through `v4.md` and `deep-research-report.md`. Either the superseded files were not preserved, or they were named differently and are in the archive under a different name.
- Evidence: Glob of `docs/archive/` confirms only the five files listed above.

**MG-04 — workflow_ai_development.md Version Header Inconsistency**
- Severity: P2 (cosmetic; may cause confusion about current version)
- Detail: File header states "Version: 1.0" but the Change Log section shows v1.1 (2026-03-04) as the latest change. The canonical version should be 1.1 per the change log.
- Evidence: workflow_ai_development.md header vs. Change Log section.

### 5.2 Stale References (STALE — require updating)

**MS-01 — ARCHITECT_BRIEF.md Footer References Superseded Filenames**
- Severity: P2
- Detail: Footer states "*Companion documents: entropy_protocol_master_spec_v1.md (full spec), entropy_protocol_trader_review_v1.md (trader version)*". Both are superseded. Canonical documents are `docs/core/PROTOCOL_SPEC.md` and `docs/audience/TRADER_BRIEF.md`. An architect reading the brief and attempting to locate these companion documents will fail.
- Evidence: ARCHITECT_BRIEF.md last line.

**MS-02 — AI_ENGINEERING_FRAMEWORK.md Context Loading Shortcut References v1.1**
- Severity: P2
- Detail: Section 3 "Context Loading Shortcuts" states: "Active documents: PROTOCOL_SPEC.md v1.1, CHARTER.md v5.0". Current spec is v1.2. An AI model or developer using this loading shortcut will assume v1.1 is current and may miss RDL constraints introduced in v1.2.
- Evidence: AI_ENGINEERING_FRAMEWORK.md Section 3 example block.

**MS-03 — ARCHITECT_BRIEF.md Section C "Known Gap" Never Resolved in Spec**
- Severity: P1 (same as F-10, already tracked)
- Detail: ARCHITECT_BRIEF.md Section C explicitly states: "The recovery from P3 that occurs while P1 recovery criteria are also pending should be explicitly handled in the harness implementation. The current spec is silent on nested recovery sequencing." This was written as a "known gap." PROTOCOL_SPEC.md Section D was updated through v1.2 but the nested recovery gap was not addressed. The ARCHITECT_BRIEF.md "Known Gap" statement thus remains accurate — it was never closed.
- Evidence: ARCHITECT_BRIEF.md Section C; PROTOCOL_SPEC.md Section D.
- Corresponds to: F-10, TASK-AF-010.

### 5.3 Vocabulary Inconsistencies (VOCAB — require clarification)

**MV-01 — "NNN-5" Typo in CHARTER.md**
- Severity: P2 (cosmetic)
- Detail: CHARTER.md Section B labels the fifth Non-Negotiable as "**NNN-5**: Trial registry + multiplicity correction" — three N's. All other documents and all other NN labels use "NN-N" (two N's). PROTOCOL_SPEC.md correctly uses "NN-5."
- Evidence: CHARTER.md Section B ("NNN-5"); PROTOCOL_SPEC.md Section B ("NN-5").

**MV-02 — BR_long Arithmetic Error: "5 × 2 × 12 ≈ 240" = 120, Not 240**
- Severity: P0 (arithmetic error in a load-bearing formula — same as F-5)
- Detail: CHARTER.md Correction 1 states: "BR_long ≈ 240 bets/year (5 skills × 2 timeframes × 12 months, approximate)." GLOSSARY.md echoes: "BR_long ≈ 240/year (5 skills × 2 timeframes × 12 months, approximate)." 5 × 2 × 12 = 120, not 240. The value 240 appears to be the correct target (implying the formula description is wrong) or the formula is correct and the value should be 120. This ambiguity feeds directly into F-5 (FLAM BR_eff calculation) and the FLAM gross Sharpe derivation.
- Evidence: CHARTER.md Correction 1; GLOSSARY.md BR definition; AUDIT_v1.md F-5.
- Corresponds to: F-5, TASK-AF-005; RS-05.

**MV-03 — K3 Trigger Conditions Stated Inconsistently Across Documents**
- Severity: P1 (ambiguous kill criterion)
- Detail: The K3 trigger involves two temporal conditions that are not consistently stated:
  - CHARTER.md Phase 1 metrics table: "K3: N_eff ≤ 2 for 2 consecutive months" — only the 2-month condition
  - CHARTER.md Phase 1 text: "K3: N_eff ≤ 2 after 3+ months of DR monitoring + correlation clustering" — only the 3-month pre-condition
  - CHARTER.md Kill Criteria Appendix: "K3: N_eff ≤ 2 after 3+ months of DR monitoring + correlation clustering" — 3-month pre-condition only
  - GLOSSARY.md Kill Criteria: "K3: N_eff ≤ 2 after 3+ months DR + correlation clustering" — 3-month pre-condition only
  - PROTOCOL_SPEC.md Phase 1: "K3: N_eff ≤ 2 after 3+ months of DR monitoring + correlation clustering" — 3-month pre-condition only
  The "2 consecutive months" duration for the N_eff ≤ 2 condition appears only in the CHARTER.md Phase 1 metrics table. It does not appear in the kill criteria appendix or in PROTOCOL_SPEC.md. This creates ambiguity: does K3 require N_eff ≤ 2 in two consecutive months, or only requires N_eff ≤ 2 once (after the 3-month pre-condition)?
- Evidence: CHARTER.md Phase 1 metrics table vs. Kill Criteria Appendix; PROTOCOL_SPEC.md Phase 1; GLOSSARY.md Kill Criteria.

**MV-04 — Sharpe CI Claim: Consistently Wrong Across All Documents (F-2 confirmed)**
- Severity: P0 (same as F-2)
- Detail: "CI ≈ ±0.15–0.20 for a ~0.30-Sharpe system" at 15 months OOS appears verbatim in: CHARTER.md Section C, PROTOCOL_SPEC.md Section C, GLOSSARY.md "Net Sharpe," and ARCHITECT_BRIEF.md Section B. All four documents contain the same incorrect value. The correct asymptotic SE at T=1.25 years, SR=0.30 is approximately ±0.89. The error is present uniformly — this is not a drift between documents but a consistent baseline error.
- Evidence: CHARTER.md Section C; PROTOCOL_SPEC.md Section C; GLOSSARY.md; ARCHITECT_BRIEF.md Section B.
- Corresponds to: F-2, TASK-AF-002.

**MV-05 — "Regime" Definition Slightly Different in CHARTER.md vs. PROTOCOL_SPEC.md vs. GLOSSARY.md**
- Severity: P2 (minor wording variation; same meaning)
- Detail:
  - CHARTER.md: "A market state classification produced by the authoritative signal hierarchy (Section D). A regime instance requires ≥8 consecutive weeks to count for OOS spanning requirements."
  - PROTOCOL_SPEC.md Section C: "A market state classification produced by the authoritative signal hierarchy (Section D). A regime instance requires ≥8 consecutive weeks to count toward OOS spanning requirements. Fragments < 8 weeks are excluded from spanning calculations."
  - GLOSSARY.md: "A market state classification produced by the P1–P4 hierarchy. A regime instance requires ≥8 consecutive weeks to count for OOS spanning requirements."
  PROTOCOL_SPEC.md adds "Fragments < 8 weeks are excluded" — this is not present in CHARTER.md or GLOSSARY.md. Functionally identical meaning but GLOSSARY.md and CHARTER.md are incomplete.

### 5.4 GLOSSARY.md Coverage Gaps

The GLOSSARY.md states: "All terms used in PROTOCOL_SPEC.md and CHARTER.md are defined here." The following terms are used in PROTOCOL_SPEC.md v1.2 and/or CHARTER.md v5.0 but are NOT defined in GLOSSARY.md:

| Missing Term | Used In | Impact |
|---|---|---|
| HWM (High-Water Mark) | PROTOCOL_SPEC.md Section D (P1 trigger: "DD from HWM ≥ 12%"), CHARTER.md Section D | Reset timing undefined; affects P1 trigger frequency |
| Purge/embargo | PROTOCOL_SPEC.md Phase 0 exit criteria, ARCHITECT_BRIEF.md Section B | Embargo duration formula undefined (F-12) |
| Walk-forward window parameters (4yr IS / 1yr OOS / 1yr test) | ARCHITECT_BRIEF.md Section B | Implementation ambiguity |
| GE-1, GE-2, GE-3 | PROTOCOL_SPEC.md Section J1 | Preregistration exemption boundary undefined (F-18) |
| RDL (Research Discovery Layer) | PROTOCOL_SPEC.md Section E (v1.2) | New module; no glossary entry |
| CandidateHypothesis | PROTOCOL_SPEC.md Section E (RDL-1) | New schema object; undefined |
| RegimeTag | PROTOCOL_SPEC.md Section E (RDL-2) | New schema object; undefined |
| FeatureSpec | PROTOCOL_SPEC.md Section E (RDL-3) | New schema object; undefined |
| EventLabel | PROTOCOL_SPEC.md Section E (RDL-4) | New schema object; undefined |
| Growth Layer | PROTOCOL_SPEC.md Section E (v1.1) | New module; no glossary entry |
| RBE (Risk Budget Escalation) | PROTOCOL_SPEC.md Section J2 | New mechanism; no glossary entry |
| N_eff formula | GLOSSARY.md says "computed via DR + correlation clustering" but gives no formula | K3 ambiguity (F-11) |
| Fragments < 8 weeks exclusion | Defined in PROTOCOL_SPEC.md Section C "Regime" but not in GLOSSARY.md | OOS spanning ambiguity |

Total missing terms from GLOSSARY.md: **13 identified** (some with direct impact on kill criteria or phase gate decisions).

---

## 6. Structural Issues Summary

### Priority-Ordered Findings

| ID | Issue | Severity | Corresponding Finding | Blocks Step |
|---|---|---|---|---|
| MG-01 | CHARTER.md not updated for Growth Layer / RDL | P0 | New (no F-ID) | Step 2 (ARCH must flag) |
| MV-04 | CI claim consistently wrong across all 4 documents | P0 | F-2 | Step 3 (INV must note) |
| MV-02 | BR_long arithmetic error (120 ≠ 240) in CHARTER and GLOSSARY | P0 | F-5 | Step 3 (INV must note) |
| MS-03 | P1+P3 nested recovery gap acknowledged in ARCHITECT_BRIEF, unresolved | P1 | F-10 | Step 2 (ARCH) |
| MV-03 | K3 trigger: "2 consecutive months" appears only in metrics table, not appendix | P1 | New ambiguity | Step 3 (INV must flag AMBIGUOUS) |
| MG-02 | EVOLUTION.md missing rationale for Growth Layer and RDL | P1 | New | Step 5 (ADV) |
| MG-04 | workflow_ai_development.md header version (1.0) vs. change log (1.1) | P2 | — | None |
| MV-05 | "Regime" definition incomplete in GLOSSARY.md and CHARTER.md vs. PROTOCOL_SPEC | P2 | — | None |
| MG-03 | Claimed superseded files not found in archive | P2 | — | None |
| MS-01 | ARCHITECT_BRIEF.md footer references superseded filenames | P2 | — | None |
| MS-02 | AI_ENGINEERING_FRAMEWORK.md context loading shortcut references v1.1 | P2 | — | Step 2 context loading risk |
| MV-01 | "NNN-5" typo in CHARTER.md | P2 | — | None |
| MG-05 | GLOSSARY.md missing 13 terms | P2 | F-12, F-18, F-19 related | Step 3 (INV) |

---

## 7. New Finding Candidates for Step 6 (CONSOLIDATED)

The following issues identified in this Step 1 analysis do not correspond to any F-1 through F-21 finding and should be proposed as new findings:

**Candidate F-22 — CHARTER.md Not Updated for Growth Layer / RDL (MG-01)**
- Proposed severity: P1 (or P0 if Growth Layer RBE pathway is determined to affect frozen non-negotiables)
- Rationale: Strategic document does not reflect two new modules added to the engineering specification. Charter-level governance mechanisms (NN-1 through NN-6) may interact with these modules without documented charter-level treatment.

**Candidate F-23 — EVOLUTION.md Missing Rationale for Growth Layer and RDL (MG-02)**
- Proposed severity: P1
- Rationale: Design decision history is incomplete. Future challenges to these modules cannot be addressed by reference to EVOLUTION.md.

**Candidate F-24 — K3 "2 Consecutive Months" Trigger Duration: Absent from Kill Criteria Appendix (MV-03)**
- Proposed severity: P1
- Rationale: CHARTER.md Phase 1 metrics table includes "2 consecutive months" as part of K3 trigger. Kill Criteria Appendix and PROTOCOL_SPEC.md do not. This is an ambiguous kill criterion — it may fire after 1 month of N_eff ≤ 2 (per the appendix/spec) or require 2 consecutive months (per the metrics table).

---

## 8. Acceptance Criterion for This Artifact

This META_ANALYSIS.md is accepted when:
1. The Spec Owner confirms the document inventory is complete (no active documents missing)
2. All Structural Gaps (MG-01 through MG-04) are acknowledged
3. All new finding candidates (F-22 through F-24) are either accepted into the findings backlog or explicitly rejected with rationale

---

## 9. Inputs for Step 2 (Architecture Review)

Step 2 (ARCH_MODEL.md) should load this artifact and note:
- **MG-01** — Growth Layer and RDL operate without charter-level mandate; flag in ARCH_MODEL architectural assumptions section
- **MV-03** — K3 trigger duration ambiguity; flag in component inventory for regime signal hierarchy
- **MV-02** — BR_long arithmetic error; flag in data flow map for FLAM computation
- **MS-03** — P1+P3 nested recovery gap; flag in state machine section
- **MG-05** — 13 missing GLOSSARY terms; flag any that affect component definitions in ARCH_MODEL

---

*Cycle: 1 | Step: 1 (Meta Investigation) | Pipeline: v1.0 | Date: 2026-03-04*
*Output: `docs/audit/META_ANALYSIS.md`*
*Next step: Step 2 — Architecture Review (PROMPT_1_ARCH_REVIEW.md → ARCH_MODEL.md)*
