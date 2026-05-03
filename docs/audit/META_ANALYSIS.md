# Entropy Protocol — Meta Investigation

**Classification:** Confidential — Internal Audit Document
**Filename:** `docs/audit/META_ANALYSIS.md`
**Audit Cycle:** Cycle 2 — Phase 1 (Implementation in Progress)
**Pipeline Step:** Step 1 — Meta Investigation
**Pipeline Version:** v1.0
**Date:** 2026-05-03
**Status:** Draft — Awaiting Spec Owner Acceptance
**Prior cycle META_ANALYSIS:** Cycle 1, 2026-03-04 (against PROTOCOL_SPEC v1.2, CHARTER v5.0)
**Full run / Partial run:** Full run (Cycle 2 entrypoint)

---

## Purpose

This artifact is the output of Step 1 (Meta Investigation) of the audit pipeline. It establishes the document inventory, version history, supersedes chains, cross-reference consistency, and vocabulary status across all active specification documents as of 2026-05-03. It is the required input for Step 2 (Architecture Review).

This cycle supersedes the prior META_ANALYSIS.md (Cycle 1, 2026-03-04). The primary delta since that run: PROTOCOL_SPEC advanced from v1.2 to v1.6 (four additional change sets); five new governance documents were added; three new architecture documents were added; the implementation document layer (ARCHITECTURE.md, spec.md, IMPLEMENTATION_CONTRACT.md, CODEX_PROMPT.md) was introduced; and Phase 1 software implementation has begun (T01–T03 complete, T04 next).

---

## 1. Document Inventory

### 1.1 Active Core Documents

| Document | Version | Date | Status | Supersedes | Author / Source |
|---|---|---|---|---|---|
| `docs/README.md` | — (no version header) | 2026-03-23 | Active | — | Internal |
| `docs/core/CHARTER.md` | 5.1 | 2026-03-04 | Active | `strategic_charter_v5.md` (claimed archived) | Internal |
| `docs/core/PROTOCOL_SPEC.md` | 1.6 | 2026-03-23 | Active | `entropy_protocol_master_spec_v1.md` (claimed archived) | Internal |
| `docs/core/GLOSSARY.md` | 1.2 | 2026-03-04 | Active | — | Internal |
| `docs/core/EVOLUTION.md` | 1.0 | 2026-03-04 | Active | — | Internal |

### 1.2 Active Architecture Documents

| Document | Version | Date | Status | Notes |
|---|---|---|---|---|
| `docs/architecture/AI_ENGINEERING_FRAMEWORK.md` | 1.0 | 2026-03-04 | Active | — |
| `docs/architecture/workflow_ai_development.md` | 1.0 (header) / 1.1 (changelog) | 2026-03-04 | Active | Header/changelog version mismatch (MG-04, carried forward) |
| `docs/architecture/system_architecture.md` | — | 2026-03-04 | Active | New since Cycle 1 META_ANALYSIS |
| `docs/architecture/research_discovery_layer.md` | — | 2026-03-04 | Active | New since Cycle 1 META_ANALYSIS |
| `docs/architecture/research_knowledge_graph.md` | — | 2026-03-04 | Active | New since Cycle 1 META_ANALYSIS |

### 1.3 Active Governance Documents

| Document | Version | Date | Status | Notes |
|---|---|---|---|---|
| `docs/governance/research_firewall.md` | — | 2026-03-04 | Active | New since Cycle 1 META_ANALYSIS; referenced by PROTOCOL_SPEC v1.5 |
| `docs/governance/experiment_readiness_gate.md` | — | 2026-03-04 | Active | New since Cycle 1 META_ANALYSIS; referenced by PROTOCOL_SPEC v1.5 |
| `docs/governance/hypothesis_families.md` | — | 2026-03-04 | Active | New since Cycle 1 META_ANALYSIS; referenced by PROTOCOL_SPEC v1.5 and GLOSSARY v1.2 |
| `docs/governance/governor.md` | — | 2026-03-04 | Active | New since Cycle 1 META_ANALYSIS |
| `docs/governance/research_portfolio_monitor.md` | — | 2026-03-23 | Active | New since Cycle 1 META_ANALYSIS; introduced by PROTOCOL_SPEC v1.6 |

### 1.4 Active Implementation Documents

| Document | Version | Date | Status | Notes |
|---|---|---|---|---|
| `docs/ARCHITECTURE.md` | — | 2026-05-01 | Active | New since Cycle 1 META_ANALYSIS; defines file layout and tech stack |
| `docs/spec.md` | 1.0 | 2026-05-01 | Active | New since Cycle 1 META_ANALYSIS; feature specification |
| `docs/IMPLEMENTATION_CONTRACT.md` | — | 2026-05-01 | Active | New since Cycle 1 META_ANALYSIS; contracts for Codex agents |
| `docs/CODEX_PROMPT.md` | 1.0 | 2026-05-03 | Active | Phase 1 state tracker; Phase: 1, T01–T03 complete |
| `docs/tasks.md` | 1.0 | 2026-05-01 | Active | Implementation task graph; Phase 1 + Phase 2 tasks |
| `docs/DECISION_LOG.md` | — | 2026-05-01 | Active | New since Cycle 1 META_ANALYSIS |
| `docs/IMPLEMENTATION_JOURNAL.md` | — | 2026-05-01 | Active | New since Cycle 1 META_ANALYSIS |
| `docs/EVIDENCE_INDEX.md` | — | 2026-05-01 | Active | New since Cycle 1 META_ANALYSIS |

### 1.5 Active Audience Documents

| Document | Version | Date | Status | Notes |
|---|---|---|---|---|
| `docs/audience/ARCHITECT_BRIEF.md` | 1.0 | 2026-03-02 | Active | Stale footer (MS-01, carried forward) |
| `docs/audience/TRADER_BRIEF.md` | 1.0 | 2026-03-02 | Active | — |

### 1.6 Active Audit Documents

| Document | Version | Date | Status | Notes |
|---|---|---|---|---|
| `docs/audit/review_pipeline.md` | 1.0 | 2026-03-04 | Active | — |
| `docs/audit/AUDIT_INDEX.md` | 1.4 | 2026-03-04 | Active | Last updated after Cycle 1 partial rerun |
| `docs/audit/AUDIT_v1.md` | 1.0 | 2026-03-04 | Accepted (external audit) | — |
| `docs/audit/REVIEW_REPORT.md` | — | 2026-03-04 | Draft | Cycle 1 partial rerun; 32 findings; P0 blockers remain open |
| `docs/audit/ARCH_MODEL.md` | — | 2026-03-04 | Draft | Cycle 1 Step 2 |
| `docs/audit/INVARIANTS.md` | — | 2026-03-04 | Draft | Cycle 1 Step 3 |
| `docs/audit/DRIFT_ASSERTIONS.md` | — | 2026-03-04 | Draft | Cycle 1 Step 4 |
| `docs/audit/DRIFT_REPORT.md` | — | 2026-03-04 | Draft | Cycle 1 Step 4 |
| `docs/audit/ADVERSARIAL_REVIEW.md` | — | 2026-03-04 | Draft | Cycle 1 Step 5 |
| `docs/audit/audit_task_registry.md` (at `docs/audit_task_registry.md`) | 1.3 | 2026-03-04 | Active | Protocol remediation task registry |
| `docs/audit/PHASE1_AUDIT.md` | — | 2026-05-01 | Active (PASS) | Phase 1 pre-implementation audit; 99/99 checks passed |
| `docs/audit/STRATEGY_NOTE.md` | — | 2026-05-03 | Active | Phase 2 strategy review; recommends Proceed |
| `docs/audit/PROMPT_0_META.md` | — | 2026-03-04 | Draft | Cycle 1 orchestration entrypoint |
| `docs/audit/PROMPT_1_ARCH_REVIEW.md` | — | 2026-03-04 | Draft | — |
| `docs/audit/PROMPT_2_INVARIANTS.md` | — | 2026-03-04 | Draft | — |
| `docs/audit/PROMPT_3_DRIFT_GUARD.md` | — | 2026-03-04 | Draft | — |
| `docs/audit/PROMPT_4_ADVERSARIAL.md` | — | 2026-03-04 | Draft | — |
| `docs/audit/PROMPT_5_CONSOLIDATED.md` | — | 2026-03-04 | Draft | — |
| `docs/audit/QUESTION_POOL.md` | — | 2026-03-04 | Draft | — |

### 1.7 Active Prompt Documents

| Document | Notes |
|---|---|
| `docs/prompts/ORCHESTRATOR.md` | New since Cycle 1 META_ANALYSIS |
| `docs/prompts/PROMPT_S_STRATEGY.md` | New since Cycle 1 META_ANALYSIS |

### 1.8 Archive Documents (NOT active; for reference only)

| Document | Notes |
|---|---|
| `docs/archive/strategic_architecture_review_v1.md` | Historical reasoning v1 |
| `docs/archive/strategic_architecture_review_v2.md` | Historical reasoning v2 |
| `docs/archive/strategic_architecture_review_v3.md` | Historical reasoning v3 |
| `docs/archive/strategic_architecture_review_v4.md` | Historical reasoning v4 — source of v4 corrections |
| `docs/archive/deep-research-report.md` | Literature validation |
| `docs/archive/README.md` | Archive index |

### 1.9 Research Documents

| Document | Notes |
|---|---|
| `docs/research/deep-research-report_v2.md` | Current literature-backed research synthesis |
| `docs/core/ERA0_SPEC.md` | Era 0 specification (present; role unclear relative to current spec set) |

---

## 2. Supersedes Chains

| Current Document | Supersedes | Superseded Document Location | Gap Status |
|---|---|---|---|
| `CHARTER.md` v5.1 | `strategic_charter_v5.md` | Claimed archived; not found in `docs/archive/` | **GAP: superseded file not located** (MG-03, carried forward) |
| `PROTOCOL_SPEC.md` v1.6 | `entropy_protocol_master_spec_v1.md` | Claimed archived; not found in `docs/archive/` | **GAP: superseded file not located** (MG-03, carried forward) |
| `CHARTER.md` v5.1 | v4.0 audit findings | `docs/archive/strategic_architecture_review_v4.md` | Confirmed present |
| All other documents | No prior versions in archive | — | N/A |

**PROTOCOL_SPEC.md basis chain:**
PROTOCOL_SPEC.md v1.6 states: "Basis: CHARTER.md v5.1 (strategic constraints) + v4 audit (authoritative corrections applied)." CHARTER.md v5.1 is confirmed present and consistent with this reference.

**CHARTER.md v5.1 basis chain:**
CHARTER.md states: "Basis: v2.0 findings, v3.0 extensions, v4.0 audit (authoritative corrections applied)." The v4.0 audit source is `docs/archive/strategic_architecture_review_v4.md` — present. v2.0 and v3.0 sources correspond to `strategic_architecture_review_v2.md` and `v3.md` — both present.

---

## 3. Version State Summary and Deltas

### 3.1 PROTOCOL_SPEC.md Version History (complete)

| Version | Date | Change Summary | Audit coverage status |
|---|---|---|---|
| v1.0 | Pre-2026-03-04 | Original spec; superseded | Baseline |
| v1.1 | 2026-03-04 | Added Growth Layer (Section E, J1, J2) | Partially audited in Cycle 1 (RS-11, RS-15 identified) |
| v1.2 | 2026-03-04 | Added RDL module (Section E) | Partially audited in Cycle 1 (RS-12, RS-13, RS-14 identified) |
| v1.3 | 2026-03-04 | Deterministic P3/P4/K3 governance; RDL attestation; GE-2/GE-3 zero-weight bright-line; RBE charter-review packet schema | Partially audited (F-3, F-10, F-23–F-26 partially mitigated) |
| v1.4 | 2026-03-04 | RDL Phase-2 promotion queue policy (FIFO, monthly cap, shock-control); freeze-safe RBE `evaluation_epoch_id` tags | Partially audited (F-30, F-31 partially mitigated) |
| v1.5 | 2026-03-04 | Added references to Research Firewall, Experiment Readiness Gate, Hypothesis Families | **Not audited in any prior cycle** |
| v1.6 | 2026-03-23 | Added Research Portfolio Monitor (RPM) to Section E; three governed signal classes (ATT, DM, SC); two forbidden output classes (F-6, F-7) | **Not audited in any prior cycle** |

**Critical observation:** v1.5 and v1.6 additions have never been reviewed in any formal pipeline step. v1.5 introduces references to five governance documents that did not exist during Cycle 1. v1.6 introduces the RPM — a new governance component that interacts with the Trial Registry (read-only) and the Governance Layer. Neither addition has been assessed against the frozen non-negotiables (NN-1 through NN-6) or the kill criterion boundary conditions.

### 3.2 CHARTER.md Version Delta

CHARTER.md advanced from v5.0 (Cycle 1) to v5.1. The date remains 2026-03-04. The v5.1 change content is referenced in PROTOCOL_SPEC.md v1.6 header ("Basis: CHARTER.md v5.1") but the specific v5.0→v5.1 delta is not documented in a changelog entry visible in CHARTER.md's opening section. The nature of the v5.0→v5.1 change is therefore not self-documented. This is a new gap.

### 3.3 GLOSSARY.md Version Delta

GLOSSARY.md advanced from v1.0 (Cycle 1) to v1.2. Thirteen missing terms were identified in Cycle 1 (MG-05). It is not confirmed whether all thirteen were added, partially added, or left absent. The GLOSSARY still claims "All terms used in PROTOCOL_SPEC.md and CHARTER.md are defined here" — this claim must be re-verified against the v1.6 additions.

### 3.4 Phase Status Delta: Pre-Development → Implementation Started

The prior META_ANALYSIS (Cycle 1, 2026-03-04) assumed Phase 0 — Pre-Development throughout. As of 2026-05-03:

- `docs/CODEX_PROMPT.md` states **Phase: 1**
- T01 (Project Skeleton), T02 (CI Setup), T03 (Smoke Tests) are marked complete
- T04 (Market Data Models) is the declared next task
- `docs/audit/PHASE1_AUDIT.md` (2026-05-01) records a pre-implementation audit with all 99 checks passing, authorizing implementation to begin

**This represents a governance-critical state change:** Phase 1 implementation is in progress while the following remains true from REVIEW_REPORT.md:
- Phase 0 exit certification remains blocked by unresolved P0 findings (F-1, F-2, F-4, F-5, F-30, F-31)
- "Phase 1 entry and later phases remain blocked until all P0 are remediated and re-verified by pipeline rerun"

The PHASE1_AUDIT.md audits the implementation documentation layer (ARCHITECTURE.md, spec.md, tasks.md, CODEX_PROMPT.md, IMPLEMENTATION_CONTRACT.md, ci.yml) — not the protocol specification audit findings. These are two distinct audit scopes. The PHASE1_AUDIT.md "PASS" result does not constitute Phase 0 exit certification under REVIEW_REPORT.md criteria.

**This discrepancy must be escalated as a new finding.** Either: (a) Phase 0 exit criteria have been formally waived or superseded (not documented anywhere visible), or (b) Phase 1 implementation has begun without formal Phase 0 exit certification, which is inconsistent with REVIEW_REPORT.md's stated Phase-block statement.

---

## 4. Cross-Reference Consistency Check

### 4.1 Inter-Document References Verified (Cycle 2 delta checks)

| Reference point | Source document | Target | Consistent? | Notes |
|---|---|---|---|---|
| PROTOCOL_SPEC.md v1.6 "Basis: CHARTER.md v5.1" | PROTOCOL_SPEC.md header | CHARTER.md v5.1 | ✓ Yes | Charter version matches |
| PROTOCOL_SPEC.md v1.5 references to Research Firewall | PROTOCOL_SPEC.md Section E v1.5 change note | `docs/governance/research_firewall.md` | ✓ Present | File confirmed in docs/governance/ |
| PROTOCOL_SPEC.md v1.5 references to Experiment Readiness Gate | PROTOCOL_SPEC.md Section E v1.5 change note | `docs/governance/experiment_readiness_gate.md` | ✓ Present | File confirmed in docs/governance/ |
| PROTOCOL_SPEC.md v1.5 references to Hypothesis Families | PROTOCOL_SPEC.md Section E v1.5 change note | `docs/governance/hypothesis_families.md` | ✓ Present | File confirmed in docs/governance/ |
| PROTOCOL_SPEC.md v1.6 RPM addition | PROTOCOL_SPEC.md Section E v1.6 change note | `docs/governance/research_portfolio_monitor.md` | ✓ Present | File confirmed in docs/governance/ |
| README.md "Current Phase: Phase 0 (active)" | README.md Current Phase section | CODEX_PROMPT.md "Phase: 1" | **✗ INCONSISTENT** | README states Phase 0; CODEX_PROMPT states Phase 1 |
| CODEX_PROMPT.md "Phase: 1" | CODEX_PROMPT.md | REVIEW_REPORT.md Phase-block statement | **✗ INCONSISTENT** | Phase 1 implementation started; REVIEW_REPORT.md blocks Phase 1 entry |
| PROMPT_0_META.md "Phase: 0 — Pre-Development" | PROMPT_0_META.md Cycle Context | CODEX_PROMPT.md "Phase: 1" | **✗ STALE** | PROMPT_0_META reflects Cycle 1 state only |
| AUDIT_INDEX.md "Latest: Cycle 1, Phase 0" | AUDIT_INDEX.md Latest Artifacts section | Actual current phase | **✗ STALE** | AUDIT_INDEX has not been updated since Cycle 1 partial rerun |
| ARCHITECT_BRIEF.md footer companion doc reference | ARCHITECT_BRIEF.md | `entropy_protocol_master_spec_v1.md` | **✗ STALE** | Superseded (MS-01, carried forward) |
| AI_ENGINEERING_FRAMEWORK.md "PROTOCOL_SPEC.md v1.1" | AI_ENGINEERING_FRAMEWORK.md Section 3 | Current PROTOCOL_SPEC v1.6 | **✗ STALE** | Now three major versions behind (MS-02, severity increased) |
| docs/ARCHITECTURE.md existence | docs/README.md Documentation Map | Not listed in README.md Documentation Map | **✗ GAP** | ARCHITECTURE.md (implementation arch) not in README's table |
| docs/spec.md existence | docs/README.md Documentation Map | Not listed in README.md Documentation Map | **✗ GAP** | spec.md not in README's table |
| ERA0_SPEC.md role | `docs/core/ERA0_SPEC.md` | Not referenced in README.md, PROTOCOL_SPEC.md, or CHARTER.md | **AMBIGUOUS** | Purpose unclear; may be superseded or draft |

### 4.2 Intra-Document Section References (Carried Forward from Cycle 1)

| Document | Section reference | Status |
|---|---|---|
| PROTOCOL_SPEC.md Section E (RDL-2) | "P4 signal pre-registration spec (when defined per F-4 resolution)" | **✗ BROKEN** — F-4 remains Inherited-Open (REVIEW_REPORT.md); referenced spec does not exist |
| ARCHITECT_BRIEF.md Section C "Known Gap" | "nested recovery sequencing" | **✗ UNRESOLVED** — MS-03 carried forward; gap acknowledged but no spec rule added |

### 4.3 New Intra-Document Checks (v1.5/v1.6 additions)

| Document | Section reference | Status |
|---|---|---|
| PROTOCOL_SPEC.md v1.6 change header | "RPM has no write access to the Trial Registry and produces no admissible evidence" | Stated in spec header and README; not yet audited for invariant compliance |
| README.md | "PROTOCOL_SPEC.md updated to v1.6. GLOSSARY, system_architecture, and hypothesis_families updated with corresponding cross-references" | GLOSSARY is dated 2026-03-04 (before v1.6 dated 2026-03-23) — **AMBIGUOUS**: either GLOSSARY was silently updated without date bump, or README's cross-reference claim is overstated |

---

## 5. Identified Issues

### 5.1 New Structural Gaps (this cycle)

**MG-06 — Phase Gate Inconsistency: Implementation Phase 1 Started Without Protocol-Level Phase 0 Exit Certification**
- Severity: P0 (governance violation — the system's own phase-gate rules are in a contradictory state)
- Detail: REVIEW_REPORT.md (Cycle 1 partial rerun, 2026-03-04) states: "Phase 0 exit certification remains blocked" and "Phase 1 entry and later phases remain blocked until all P0 are remediated and re-verified by pipeline rerun." CODEX_PROMPT.md (2026-05-03) states Phase: 1 with T01–T03 complete. PHASE1_AUDIT.md (2026-05-01) records a pre-implementation audit pass that covers the implementation documentation layer (ARCHITECTURE.md, spec.md, tasks.md, CODEX_PROMPT.md, IMPLEMENTATION_CONTRACT.md, ci.yml) but does not constitute protocol-level Phase 0 exit certification. The two audit scopes are distinct:
  - **PHASE1_AUDIT.md scope:** Implementation readiness (is the engineering scaffolding correct and consistent?). PASS.
  - **REVIEW_REPORT.md scope:** Protocol specification validity (are the rules, formulas, and thresholds correct and auditable?). BLOCKED on P0 findings F-1, F-2, F-4, F-5, F-30, F-31.
  No document records a formal waiver, scope separation decision, or Spec Owner approval to proceed with Phase 1 implementation while protocol-level P0 findings remain open.
- Evidence: REVIEW_REPORT.md Phase-block statement; CODEX_PROMPT.md Phase field; PHASE1_AUDIT.md scope; AUDIT_v1.md and REVIEW_REPORT.md P0 finding list.
- Required action: Spec Owner must either (a) formally document that PHASE1_AUDIT.md scope is sufficient for Phase 1 engineering start and that protocol-level Phase 0 exit certification is a separate milestone (with explicit acceptance that F-1/F-2/F-4/F-5 remain unresolved), or (b) halt Phase 1 implementation until protocol-level P0 findings are resolved.

**MG-07 — CHARTER.md v5.0→v5.1 Delta Not Self-Documented**
- Severity: P1 (charter version change without visible changelog)
- Detail: PROTOCOL_SPEC.md v1.6 references "CHARTER.md v5.1" but CHARTER.md contains no visible version-change log or entry explaining what changed between v5.0 and v5.1. Under the project's document governance rules, the CHARTER is a frozen-adjacent document — changes to it require explicit version increment (per README Document Governance section). The delta is silent, making it unauditable.
- Evidence: CHARTER.md version header (v5.1, date 2026-03-04); PROTOCOL_SPEC.md v1.6 header; REVIEW_REPORT.md references "CHARTER.md v5.1" (suggesting v5.1 was current during Cycle 1 partial rerun, same date).
- Note: AUDIT_INDEX.md Cycle 1 partial rerun entry states "Spec context: PROTOCOL_SPEC.md v1.4; CHARTER.md v5.1", meaning the v5.0→v5.1 transition occurred between Cycle 1 full run (2026-03-04, CHARTER v5.0) and Cycle 1 partial rerun (2026-03-04, CHARTER v5.1) — on the same calendar date. The change set is unknown.

**MG-08 — v1.5/v1.6 Additions Not Audited Against Frozen Non-Negotiables or Kill Criteria**
- Severity: P1 (new modules added to production spec without formal invariant review)
- Detail: PROTOCOL_SPEC v1.5 added references to five governance documents (Research Firewall, Experiment Readiness Gate, Hypothesis Families, Governor, RPM predecessor context). v1.6 added the Research Portfolio Monitor (RPM) with three governed signal classes and two forbidden output classes. Neither addition has been reviewed in any formal pipeline step (Steps 2–5). The RPM is declared read-only and non-admissible, but its interaction with the Trial Registry, governance state machine, and Hypothesis Families (which are used for trial classification) has not been formally assessed. Any v1.5/v1.6 component that interacts with trial classification or multiplicity budget is adjacent to NN-5 (Trial Registry + multiplicity correction).
- Evidence: PROTOCOL_SPEC.md v1.5/v1.6 change summaries; AUDIT_INDEX.md showing no Cycle 2 pipeline steps completed.

**MG-09 — ERA0_SPEC.md: Undocumented File With Unclear Authority Status**
- Severity: P2 (ambiguous document with unknown role)
- Detail: `docs/core/ERA0_SPEC.md` exists in the core/ directory alongside CHARTER.md, PROTOCOL_SPEC.md, GLOSSARY.md, and EVOLUTION.md. It is not referenced in README.md, PROTOCOL_SPEC.md, CHARTER.md, or any audit document. Its version, date, authority level, and relationship to the other core documents are unknown. A document in the core/ directory is presumed authoritative unless explicitly marked otherwise. If ERA0_SPEC.md contains rules or constraints that conflict with or extend PROTOCOL_SPEC.md, those rules would be operating outside the audit pipeline.
- Evidence: Glob of docs/core/ confirms file presence; no reference to it found in README, PROTOCOL_SPEC, CHARTER, AUDIT_INDEX, or REVIEW_REPORT.

**MG-10 — Implementation Documents (ARCHITECTURE.md, spec.md) Not in README.md Documentation Map**
- Severity: P2 (navigation gap; may cause agents or developers to miss authoritative implementation constraints)
- Detail: `docs/ARCHITECTURE.md` and `docs/spec.md` are active implementation documents (v1.0, 2026-05-01). PHASE1_AUDIT.md audited both as authoritative. Neither appears in the README.md Documentation Map table or Reading Order sections. An AI model or developer loading context via README.md will not discover these documents.
- Evidence: README.md Documentation Map; Glob confirming docs/ARCHITECTURE.md and docs/spec.md exist; PHASE1_AUDIT.md references both.

### 5.2 Structural Gaps Carried Forward from Cycle 1

**MG-01 — CHARTER.md Not Updated for Growth Layer / RDL (carried forward)**
- Severity: P0 (status: Partial-Mitigation per REVIEW_REPORT.md F-22 through F-25)
- Detail: CHARTER.md v5.1 does not contain explicit sections for Growth Layer, RBE protocol, or RDL. These modules operate via PROTOCOL_SPEC.md only. Charter-level mandate is still absent.
- Status update: Cycle 1 pipeline identified this as new findings F-22 through F-25 (Partial-Mitigation). No full resolution confirmed.

**MG-02 — EVOLUTION.md Missing Rationale for Growth Layer and RDL (carried forward)**
- Severity: P1
- Detail: EVOLUTION.md has not been updated since Cycle 1 (last entry Section 11; no section for Growth Layer, RDL, RBE, RPM, or governance layer additions). Four major feature additions have occurred since the last EVOLUTION.md entry.
- Status update: No change since Cycle 1.

**MG-03 — Claimed Superseded Files Not Found in Archive (carried forward)**
- Severity: P2
- Detail: `strategic_charter_v5.md` and `entropy_protocol_master_spec_v1.md` remain absent from `docs/archive/`.

**MG-04 — workflow_ai_development.md Version Header Inconsistency (carried forward)**
- Severity: P2
- Detail: Header states v1.0; changelog section shows v1.1 as latest.

### 5.3 Stale References

**MS-01 — ARCHITECT_BRIEF.md Footer References Superseded Filenames (carried forward)**
- Severity: P2
- Detail: Footer references `entropy_protocol_master_spec_v1.md` and `entropy_protocol_trader_review_v1.md`; both superseded.

**MS-02 — AI_ENGINEERING_FRAMEWORK.md Context Loading Shortcut References v1.1 (severity increased)**
- Severity: P1 (upgraded from P2: now three major versions behind; v1.5/v1.6 governance additions are substantial)
- Detail: Section 3 "Context Loading Shortcuts" states "Active documents: PROTOCOL_SPEC.md v1.1". Current spec is v1.6. An AI model loading context via this shortcut will operate without awareness of: RDL attestation rules (v1.3), RDL promotion queue policy (v1.4), Research Firewall/ERG/HF references (v1.5), and RPM (v1.6).
- Evidence: AI_ENGINEERING_FRAMEWORK.md Section 3.

**MS-03 — ARCHITECT_BRIEF.md Section C "Known Gap" Never Resolved (carried forward)**
- Severity: P1 (corresponds to F-10, Partial-Mitigation)
- Detail: ARCHITECT_BRIEF.md Section C states the known gap for nested recovery sequencing. PROTOCOL_SPEC.md v1.3 added concurrent P1/P3/P4 semantics but runtime verification remains pending per REVIEW_REPORT.md F-10.

**MS-04 — README.md "Current Phase: Phase 0 (active)" Is Stale**
- Severity: P1 (new this cycle; authoritative entry point for developers and AI models)
- Detail: README.md Current Phase section states "Phase 0 (active): Evaluation engine + SimBroker construction." CODEX_PROMPT.md states Phase: 1. PHASE1_AUDIT.md (2026-05-01) authorized implementation to begin. The README is described as the reading entry point for all roles. A developer or AI model reading the README will load incorrect phase context.
- Evidence: README.md "Current Phase" section; CODEX_PROMPT.md Phase field.

**MS-05 — PROMPT_0_META.md Cycle Context Is Stale (Phase 0; pre-implementation)**
- Severity: P1 (new this cycle; this is the Cycle Entrypoint document)
- Detail: PROMPT_0_META.md is dated 2026-03-04 and reflects Phase 0 pre-development state. The document is the mandatory starting context for all audit pipeline runs. It states "No Step 1–5 artifacts exist" (now false: Steps 1–5 were completed in Cycle 1) and "Phase 0 — Pre-Development (ASSUMPTION — no code artifacts observed)" (now false: Phase 1 code is in progress). Running any downstream pipeline step from PROMPT_0_META.md as-is will produce artifacts based on stale cycle context.
- Evidence: PROMPT_0_META.md Cycle Context section; CODEX_PROMPT.md; AUDIT_INDEX.md.

### 5.4 Vocabulary Inconsistencies (carried forward where unresolved)

**MV-01 — "NNN-5" Typo in CHARTER.md (carried forward)**
- Severity: P2
- Detail: CHARTER.md Section B uses "NNN-5" (three N's). All other documents use "NN-5."

**MV-02 — BR_long Arithmetic Error: "5 × 2 × 12 ≈ 240" = 120, Not 240 (carried forward)**
- Severity: P0 (corresponds to F-5, Inherited-Open)
- Detail: CHARTER.md Correction 1 and GLOSSARY.md both state BR_long ≈ 240 bets/year (5 skills × 2 timeframes × 12 months). 5 × 2 × 12 = 120, not 240. No resolution confirmed in REVIEW_REPORT.md — F-5 remains Inherited-Open.

**MV-03 — K3 Trigger: "2 Consecutive Months" Absent from Kill Criteria Appendix (carried forward)**
- Severity: P1 (ambiguous kill criterion; corresponds to REVIEW_REPORT.md F-29 Partial-Mitigation)
- Detail: K3 duration trigger inconsistency between CHARTER.md Phase 1 metrics table and Kill Criteria Appendix remains. REVIEW_REPORT.md F-29 notes "K3 timing lock added" in v1.3 but "estimator lock remains partially unresolved."

**MV-04 — Sharpe CI Claim Consistently Wrong Across Documents (carried forward)**
- Severity: P0 (corresponds to F-2, Partial-Mitigation)
- Detail: CI ≈ ±0.15–0.20 appears in CHARTER.md, PROTOCOL_SPEC.md, GLOSSARY.md, and ARCHITECT_BRIEF.md. REVIEW_REPORT.md F-2: "CI wording is synchronized to `CI-SR-ACF-v1`; derivation artifact and validation examples still pending." The synchronization may have addressed the CI method reference but the derivation artifact is still missing.

**MV-05 — "Regime" Definition Incomplete in GLOSSARY.md and CHARTER.md (carried forward)**
- Severity: P2
- Detail: PROTOCOL_SPEC.md adds "Fragments < 8 weeks are excluded from spanning calculations" which is absent from GLOSSARY.md and CHARTER.md.

**MV-06 — GLOSSARY.md Coverage Gaps (Cycle 1 MG-05, status unknown)**
- Severity: P2 (minimum; some terms affect kill criterion auditability)
- Detail: Cycle 1 identified 13 missing terms in GLOSSARY.md (HWM, Purge/embargo, Walk-forward window parameters, GE-1/GE-2/GE-3, RDL, CandidateHypothesis, RegimeTag, FeatureSpec, EventLabel, Growth Layer, RBE, N_eff formula, Fragments < 8 weeks exclusion). GLOSSARY.md advanced to v1.2 since Cycle 1 but the completeness of the update is not confirmed. Additionally, PROTOCOL_SPEC v1.5/v1.6 introduced new terms not in the prior list: Research Firewall, Experiment Readiness Gate, Hypothesis Families, RPM, Class ATT, Class DM, Class SC, F-6 (trend inference), F-7 (denominator-collapsed ratios). These new terms must also be verified present in GLOSSARY.md.

---

## 6. Structural Issues Summary

### Priority-Ordered Findings

| ID | Issue | Severity | Corresponding Finding | Blocks Step |
|---|---|---|---|---|
| MG-06 | Phase 1 implementation started without protocol-level Phase 0 exit certification | P0 | New (no F-ID) | Blocks all steps: governance inconsistency must be resolved or formally acknowledged before audit findings can be acted upon |
| MG-01 | CHARTER.md not updated for Growth Layer / RDL | P0 | F-22–F-25 (Partial-Mitigation) | Step 2 (ARCH) |
| MV-04 | CI claim consistently wrong across all documents | P0 | F-2 (Partial-Mitigation) | Step 3 (INV) |
| MV-02 | BR_long arithmetic error (120 ≠ 240) | P0 | F-5 (Inherited-Open) | Step 3 (INV) |
| MG-07 | CHARTER.md v5.0→v5.1 delta not self-documented | P1 | New | Step 2 (ARCH) |
| MG-08 | v1.5/v1.6 additions not audited against frozen non-negotiables | P1 | New | Steps 2–5 |
| MG-02 | EVOLUTION.md missing rationale for Growth Layer, RDL, RPM, governance layer | P1 | New (MG-02 extended) | Step 5 (ADV) |
| MS-02 | AI_ENGINEERING_FRAMEWORK.md references v1.1 (now 3 versions behind) | P1 | — | Step 2 context loading risk |
| MS-03 | P1+P3 nested recovery gap acknowledged in ARCHITECT_BRIEF, runtime verify pending | P1 | F-10 (Partial-Mitigation) | Step 2 (ARCH) |
| MS-04 | README.md states Phase 0; actual phase is Phase 1 | P1 | New | All steps: misleading entry point |
| MS-05 | PROMPT_0_META.md cycle context stale (Phase 0; no artifacts) | P1 | New | All steps: stale entrypoint |
| MV-03 | K3 trigger: "2 consecutive months" absent from kill criteria appendix | P1 | F-29 (Partial-Mitigation) | Step 3 (INV) |
| MG-04 | workflow_ai_development.md version header (1.0) vs. change log (1.1) | P2 | — | None |
| MG-05/MV-06 | GLOSSARY.md: original 13 missing terms + new v1.5/v1.6 terms | P2 | F-19 related | Step 3 (INV) |
| MG-09 | ERA0_SPEC.md: undocumented file with unclear authority status | P2 | New | Step 2 (ARCH) |
| MG-10 | ARCHITECTURE.md and spec.md not in README Documentation Map | P2 | New | None |
| MV-05 | "Regime" definition incomplete in GLOSSARY.md and CHARTER.md | P2 | — | None |
| MG-03 | Claimed superseded files not found in archive | P2 | — | None |
| MS-01 | ARCHITECT_BRIEF.md footer references superseded filenames | P2 | — | None |
| MV-01 | "NNN-5" typo in CHARTER.md | P2 | — | None |

---

## 7. New Finding Candidates for Step 6 (CONSOLIDATED)

The following issues identified in this Step 1 analysis do not correspond to existing findings F-1 through F-32 and should be proposed as new findings:

**Candidate F-33 — Phase Gate Inconsistency: Phase 1 Implementation Active While Protocol P0 Findings Open (MG-06)**
- Proposed severity: P0
- Rationale: The system's own governance rules (REVIEW_REPORT.md Phase-block statement) explicitly block Phase 1 entry. Implementation has begun without documented waiver or scope separation decision. This is either a governance violation or an undocumented policy decision that must be formally recorded.
- Required action: Spec Owner to formally document the scope boundary between PHASE1_AUDIT.md (implementation readiness) and REVIEW_REPORT.md (protocol specification validity), and the conditions under which Phase 1 implementation may proceed despite open protocol-level P0 findings.

**Candidate F-34 — CHARTER.md v5.0→v5.1 Delta Not Self-Documented (MG-07)**
- Proposed severity: P1
- Rationale: Charter version incremented (v5.0→v5.1) without a visible changelog entry. The charter is the strategic authority document. Silent version changes undermine audit traceability.

**Candidate F-35 — v1.5/v1.6 Additions Not Formally Audited (MG-08)**
- Proposed severity: P1
- Rationale: Three Cycle 1 pipeline steps (Steps 2–5) have not been re-run against v1.3/v1.4/v1.5/v1.6 additions. PROTOCOL_SPEC v1.5 added governance document references; v1.6 added the RPM and two forbidden output classes. Neither has been assessed against frozen non-negotiables, kill criteria, or invariant boundary conditions.

**Candidate F-36 — README.md Phase Status Stale (MS-04)**
- Proposed severity: P1
- Rationale: README.md is the primary entry point for all roles (developers, AI models, architects). It states Phase 0 is active. Actual phase is 1. This creates context-loading errors for any agent or developer relying on README for phase-state orientation.

**Candidate F-37 — ERA0_SPEC.md Authority Status Undefined (MG-09)**
- Proposed severity: P2
- Rationale: A document in docs/core/ with no references, no audit coverage, and no declared relationship to the active spec set is an unknown authority surface.

---

## 8. Prior Cycle Finding Status Notes (Step 1 scope)

The following Cycle 1 findings are directly relevant to Step 1 scope (document structure, version consistency, cross-references). Status is as reported in REVIEW_REPORT.md Cycle 1 partial rerun:

| Finding | Status per REVIEW_REPORT | Step 1 confirmation |
|---|---|---|
| F-2 (CI arithmetic) | Partial-Mitigation | MV-04: CI method synchronized; derivation artifact still missing |
| F-3 (P3 population) | Partial-Mitigation | MG-01: Charter still lacks explicit Growth Layer/RDL |
| F-5 (IC_long/BR_long) | Inherited-Open | MV-02: BR_long formula still states 240; no resolution visible |
| F-19 (GLOSSARY coverage) | Inherited-Open | MV-06: GLOSSARY at v1.2; completeness unconfirmed |
| F-22 (Net Sharpe wording) | Partial-Mitigation | Not directly verifiable at Step 1 scope |

---

## 9. Acceptance Criterion for This Artifact

This META_ANALYSIS.md is accepted when:
1. The Spec Owner confirms the document inventory is complete (no active documents missing)
2. All new Structural Gaps (MG-06 through MG-10) are acknowledged
3. Finding candidates F-33 through F-37 are either accepted into the findings backlog or explicitly rejected with rationale
4. The governance question raised in MG-06 (Phase 1 implementation vs. protocol P0 block) receives a formal written disposition

---

## 10. Inputs for Step 2 (Architecture Review)

Step 2 (ARCH_MODEL.md) should load this artifact and note:

- **MG-06** — Phase gate inconsistency must be documented in ARCH_MODEL as a governance assumption: the ARCH_MODEL is being generated against a system in Phase 1 implementation with protocol P0 findings open
- **MG-07** — CHARTER.md v5.1 delta unknown; any architectural claim dependent on v5.1 specific content must be flagged uncertain
- **MG-08** — v1.5/v1.6 governance additions (Research Firewall, ERG, Hypothesis Families, RPM) must be included in component inventory; none were in Cycle 1 ARCH_MODEL
- **MG-09** — ERA0_SPEC.md must be opened and its content inventoried; its authority status must be determined before the ARCH_MODEL can be considered complete
- **MS-02** — Load PROTOCOL_SPEC.md directly (not via AI_ENGINEERING_FRAMEWORK.md context shortcut); v1.6 is canonical
- **MG-01** — Growth Layer and RDL carry forward as operating without charter-level mandate
- **MV-03** — K3 trigger duration ambiguity carries forward as AMBIGUOUS in invariant review
- **MS-03** — P1+P3 nested recovery gap carries forward as unresolved

---

*Cycle: 2 | Step: 1 (Meta Investigation) | Pipeline: v1.0 | Date: 2026-05-03*
*Spec-of-record: PROTOCOL_SPEC.md v1.6, CHARTER.md v5.1*
*Output: `docs/audit/META_ANALYSIS.md`*
*Next step: Step 2 — Architecture Review (PROMPT_1_ARCH_REVIEW.md → ARCH_MODEL.md)*
