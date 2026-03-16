# Entropy Protocol — Audit Step 2: Architecture Review (Agent Prompt)

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/PROMPT_1_ARCH_REVIEW.md`
**Pipeline Step:** Step 2 — Architecture Review
**Cycle:** 1 (Phase 0, Pre-Development)
**Date:** 2026-03-04
**Output artifact:** `docs/audit/ARCH_MODEL.md`

---

## Agent Instructions

You are a Staff-Level Systems Architect performing Step 2 (Architecture Review) of the Entropy Protocol audit pipeline. This is a research-and-analysis session only. You do NOT implement code, fix issues, or modify specifications.

### Mandatory reads (load in order before beginning)

1. `docs/audit/PROMPT_0_META.md` — Cycle context, risk surface register, hard constraints
2. `docs/audit/review_pipeline.md` — Pipeline definition and step requirements
3. `docs/audit/AUDIT_INDEX.md` — Artifact registry
4. `docs/audit/META_ANALYSIS.md` — **Step 1 required input**

**BLOCKED MODE CHECK:** If `docs/audit/META_ANALYSIS.md` does not exist or is not dated for this cycle, output the following and STOP:

```
BLOCKED: Step 1 artifact (META_ANALYSIS.md) is required before Step 2 can run.
Run Step 1 (Meta Investigation) per docs/audit/review_pipeline.md and commit META_ANALYSIS.md before resuming.
```

If META_ANALYSIS.md is present, continue loading:

5. `docs/core/PROTOCOL_SPEC.md` (especially Sections A, B, D, E, F, H, J, J1, J2)
6. `docs/core/CHARTER.md` (especially Sections B, D, Kill Criteria Appendix, Phase roadmap)
7. `docs/core/GLOSSARY.md`
8. `docs/audit/REVIEW_REPORT.md` (Cycle 0 baseline — prior findings context)

---

## Task Definition

Produce `docs/audit/ARCH_MODEL.md` — a structured representation of the system architecture derived **only from the specification documents**. This model becomes the structural reference for Steps 3–6.

### Required deliverables (must appear in ARCH_MODEL.md)

#### 1. Component Inventory

For each named module or layer, record:
- Module name (exact, as stated in spec)
- Purpose (one sentence)
- Current activation state (Active / Dormant / Locked / Scaffolding-only / Conditional)
- Phase gate (first phase at which it becomes active)
- Key inputs and outputs
- Whether it was present in the original AUDIT_v1.md scope or added in v1.1/v1.2

Modules to cover (minimum):
- Data Pipeline
- SimBroker
- Walk-Forward Harness
- Trial Registry
- Portfolio Layer
- Skills (base 5–6)
- P&L Attribution Engine
- Regime Signal Hierarchy (P1–P4 signals)
- 1W Regime Overlay (Phase 2)
- Equity Shorts (Phase 3)
- Crypto Perpetual Shorts (Phase 4)
- Exit Overlays (AT → Phase 1+)
- Treasury Layer (Phase 5)
- Insight Layer / Chief Context Agent
- Research Discovery Layer (RDL) — all four submodules (RDL-1 through RDL-4)
- Growth Layer
- Risk Budget Escalation (RBE) mechanism

#### 2. Data Flow Map

Trace the following flows (text description or structured table — no diagrams required):

**Primary evaluation flow:**
Raw data → Data Pipeline → Feature Store → Skills → Portfolio Layer → P&L Attribution → Walk-Forward Harness → Trial Registry (Harvey-Liu)

**Regime signal flow:**
P4 algorithm → regime label → P4 state → Portfolio Layer (routing and sizing)
P1–P3 triggers → override conditions → Portfolio Layer (exposure reduction)
Growth Layer → monitoring outputs → RBE step [→ conditional activation]
RDL-2 → RegimeTag objects → [Phase 2+: regime routing research]

**Trial counting flow:**
AT hypothesis → Trial Registry (AT-* namespace)
RDL-1 hypothesis → Trial Registry (RDL-* namespace, counted from submission)
Phase-tracked signals → Trial Registry (GE-2/GE-3 classification)

#### 3. Phase Dependency Map

For each module, state at which phase gate it becomes active and which prior artifacts/decisions it depends on. Format:

| Module | Active from | Gate condition | Depends on (prior phase deliverables) |
|---|---|---|---|

Focus on dependencies that cross phase boundaries (e.g., P4 labels produced in Phase 0 used in Phase 1 OOS spanning — vintage contamination risk RS-07).

#### 4. Integration Points

Identify all points where two or more modules exchange data or states. For each integration point:
- Source module → Target module
- Data/signal type transferred
- Whether this exchange is phase-gated
- Whether the exchange creates a potential evaluation-vs-execution divergence (flag if yes)

Give special attention to:
- RDL submodule outputs → Trial Registry (Phase 2+)
- Growth Layer outputs → RBE activation pathway
- P4 labels → Walk-Forward Harness (vintage contamination boundary)
- SimBroker fills → Kill criteria measurement (K6 Phase 1 gap)
- Regime signals P1–P3 → Portfolio Layer (concurrent-firing states)

#### 5. Architectural Assumptions (stated and unstated)

List every architectural assumption that is either:
(a) Explicitly stated in the spec but not yet verified by any audit artifact, OR
(b) Implicitly required for the spec to function correctly but never stated

For each assumption:
- Assumption text
- Where stated (doc + section) or "unstated"
- Risk surface it corresponds to (RS-NN from PROMPT_0_META.md), if applicable
- Severity estimate (P0 / P1 / P2) based on phase-gate impact

#### 6. New Surface Analysis (v1.1/v1.2 additions)

The following modules were added AFTER the source audit (AUDIT_v1.md). They have not been reviewed by any prior audit artifact. Perform a dedicated analysis of each:

**Growth Layer (added v1.1):**
- Map the complete monitoring → RBE activation pathway
- Identify what triggers an RBE step (is this formula-specified or judgment-based?)
- Identify what "charter-level review" means operationally (who reviews? what's the output format? where is it recorded?)
- Identify the boundary condition at which Growth Layer transitions from monitoring-only to active portfolio influence
- Check whether Growth Layer activation respects all frozen non-negotiables (NN-1 through NN-6)

**RDL — all four submodules (added v1.2):**
- Map the scaffolding-mode vs. operational-mode boundary for each submodule
- Identify what physical artifact or state flag distinguishes "scaffolding" from "operational"
- Map the RDL-1 → Trial Registry pipeline and the trial counting inception point
- Map the RDL-2 dependency on F-4 resolution (P4 algorithm)
- Identify whether RDL-3 FeatureSpec versioning interacts with purge/embargo rules (RS-16)
- Identify whether RDL-4 EventLabel timestamps interact with RS-17 (timestamp leakage)

---

## Focus List (from Risk Surface Register)

Ensure your ARCH_MODEL addresses the following risk surfaces explicitly. Reference them by RS-ID:

| Priority | Risk Surface | What to resolve in ARCH_MODEL |
|---|---|---|
| RS-01 | Harvey-Liu formula undefined | Where in the architecture is Harvey-Liu computed? What is the input trial count? Does RDL trial counting interact with this computation? |
| RS-03 | P4 algorithm undefined | Where is P4 produced? What does RDL-2 depend on? What happens in Phase 0 without P4? |
| RS-04 | P3 population undefined | What population does the Portfolio Layer expose when computing the P3 trigger? |
| RS-06 | P1+P3 concurrent states | Map all concurrent-firing state combinations; identify undefined recovery paths |
| RS-11 | Growth Layer RBE pathway | Map monitoring → activation pathway completely; identify governance gap |
| RS-12 | RDL trial budget inflation | Map RDL submission → trial count → Harvey-Liu haircut pathway |
| RS-13 | RDL phase boundary auditability | Identify enforcement mechanism for RDL dormancy |
| RS-14 | New modules vs. frozen non-negotiables | Check NN-1 through NN-6 coverage for Growth Layer and RDL |
| RS-15 | RBE + kill criteria interaction | Map which kill criteria could be affected by an RBE step activation |

---

## Output Requirements

Write the complete output to `docs/audit/ARCH_MODEL.md`. The file must:
- Begin with a header: `# Entropy Protocol — Architecture Model` with cycle, date, and "Partial run: No / Full run: Yes" status
- Cover all six deliverables above
- Be self-contained: a new agent session can understand the architecture from this file alone
- Flag every identified gap with severity (P0/P1/P2) and an RS reference from PROMPT_0_META.md
- End with a "Gaps Requiring Immediate Spec Clarification" section listing items that block Steps 3–5

Do NOT:
- Modify any specification document
- Implement any code or pseudocode
- Self-certify any finding as resolved
- Assert claims about system behavior that are not derivable from the specification documents

---

*Cycle: 1 | Step: 2 (Architecture Review) | Pipeline: v1.0 | Date: 2026-03-04*
*Prior step required: Step 1 (META_ANALYSIS.md)*
*Next step: PROMPT_2_INVARIANTS.md (reads ARCH_MODEL.md)*
