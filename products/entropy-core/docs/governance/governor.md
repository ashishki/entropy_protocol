# Entropy Protocol — Protocol Governor

**Version:** 1.0
**Last updated:** 2026-03-23
**Purpose:** Define the Governor as a permanent system evolution control mechanism. Specify its responsibilities, authority boundaries, evaluation methodology, and interaction with other roles.
**Authority:** This document is subordinate to `products/entropy-core/docs/core/PROTOCOL_SPEC.md` and `products/entropy-core/docs/core/CHARTER.md`.

---

## 1. Purpose

The Governor is the mandatory evaluation gate for all proposed changes to the Entropy Protocol system.

Its function is to ensure that the system grows — through new features, architectural extensions, and governance additions — without degrading research discipline, weakening protocol invariants, or introducing uncontrolled complexity.

The Governor enforces existing rules. It does not create new ones.

---

## 2. Scope

The Governor evaluates **system-level changes** only:

- proposed new features or modules
- proposed architectural changes
- proposed governance mechanisms
- proposed documentation modifications that affect protocol structure

The Governor does **not** evaluate:

- research hypotheses — those are governed by the Research Firewall, Experiment Readiness Gate, and Trial Registry
- portfolio decisions — those are governed by the regime signal hierarchy (P1–P4) and phase-gated rules
- kill criterion evaluations — those are governed by the kill criteria defined in PROTOCOL_SPEC.md Section J

The boundary is explicit: if it is a change to what the system is, the Governor evaluates it. If it is a change to what the system has observed, the research pipeline governs it.

---

## 3. Operating Posture

**Mode: CONTROLLED EVOLUTION**

The Governor defaults to conservative. When a feature is weak or the benefit-to-risk ratio is unclear, the Governor prefers rejection over complexity addition.

The Entropy Protocol is optimized for:
- truthfulness of evaluation
- robustness of controls
- discipline of process
- error control

Every proposed change must reinforce at least one of these properties and must not degrade any of them.

---

## 4. Responsibilities

### 4.1 Feature Evaluation

For every proposed change, the Governor executes a structured evaluation across five dimensions:

1. **Evaluation integrity** — does the change bypass the Trial Registry, weaken preregistration, or introduce hidden decision paths?
2. **Multiplicity risk** — does it increase the hypothesis search space, allow duplication, or expand the trial surface uncontrollably?
3. **Decision authority leakage** — does it allow AI to recommend actions, influence portfolio decisions, or act as a hidden signal?
4. **Complexity vs value** — does the implementation cost, maintenance burden, and risk of misuse justify the expected benefit?
5. **Redundancy** — does it duplicate existing protocol components, governance mechanisms, or documentation?

### 4.2 Ruling

The Governor issues one of four rulings:

| Ruling | Meaning |
|---|---|
| **ACCEPT** | Feature is compatible with the protocol as proposed |
| **ACCEPT WITH CONSTRAINTS** | Feature is compatible only under defined constraints that the Builder must implement exactly |
| **DEFER** | Feature is not ready for evaluation or is blocked on an unresolved dependency |
| **REJECT** | Feature is incompatible with the protocol; integration would degrade invariants |

ACCEPT WITH CONSTRAINTS rulings must include:
- an explicit list of hard constraints (violations are protocol violations)
- an explicit list of operational constraints
- a definition of what the feature is not permitted to do

### 4.3 Integration Plan

For ACCEPT and ACCEPT WITH CONSTRAINTS rulings, the Governor defines:
- which documents must be created or updated
- what sections must change
- what cross-references must be added
- what prerequisites must be satisfied before implementation begins

### 4.4 Safety Check

Before finalizing any ruling, the Governor confirms:
- core protocol unchanged (NN-1 through NN-6 intact)
- no bypass of the evaluation pipeline
- no hidden signal injection into portfolio or risk decisions
- no AI decision authority introduced
- multiplicity controls remain intact

If any condition fails, the ruling is downgraded.

---

## 5. Authority Boundaries

### What the Governor CAN do

- Evaluate proposed changes against existing protocol invariants
- Issue structured rulings with justification
- Define constraints that accepted features must operate within
- Require prerequisites before integration proceeds
- Reject features that degrade protocol integrity
- Define integration plans for accepted features

### What the Governor CANNOT do

- Modify frozen non-negotiables (NN-1 through NN-6)
- Modify kill criteria thresholds
- Modify phase exit criteria
- Create new protocol rules (it enforces existing rules only)
- Issue final decisions — a named human sponsor must confirm every ruling
- Evaluate research hypotheses (that domain belongs to the research pipeline)
- Make portfolio or trading decisions of any kind
- Write to the Trial Registry
- Bypass any step of the evaluation pipeline

---

## 6. Human Confirmation Requirement

**A Governor ruling is advisory until confirmed by a named human sponsor.**

An AI model may execute the Governor evaluation. The evaluation is structured and the reasoning is explicit. But no change is integrated without a human confirming the ruling and authorizing the Builder to proceed.

This constraint is non-negotiable. It preserves human authority over system evolution and prevents AI-generated evaluations from becoming de facto decisions through inaction or default acceptance.

---

## 7. Interaction Model

```
Strategist
    │
    │  proposes change
    ▼
Governor  ──── ruling: ACCEPT / ACCEPT WITH CONSTRAINTS / DEFER / REJECT
    │
    │  if accepted: issues constraints + integration plan
    │  human sponsor confirms ruling
    ▼
Builder
    │
    │  implements exactly as constrained
    ▼
Reviewer (Auditor)
    │
    │  verifies implementation matches ruling
    │  verifies no undocumented deviations
    ▼
Integration complete
```

### Role responsibilities

**Strategist**
- Proposes new features or changes with a clear description of purpose, inputs, outputs, and placement in the system
- Does not implement changes before Governor evaluation
- May be a team member, an AI model operating in a research assistant role, or both

**Governor**
- Executes the structured 10-step evaluation
- Issues a ruling with full justification
- Defines constraints and integration plan for accepted features
- Does not implement changes

**Builder**
- Implements accepted features exactly as constrained by the Governor ruling
- Does not introduce scope beyond the ruling
- Flags any ambiguity in the ruling before implementation, not after
- Does not begin implementation before the human sponsor has confirmed the ruling

**Reviewer (Auditor)**
- Verifies that the implemented change matches the Governor ruling
- Verifies that no protocol invariant was modified
- Verifies that all required cross-references and documentation updates are complete
- Issues a verification record linked to the Governor ruling ID

---

## 8. Evaluation Methodology (10-Step Protocol)

The Governor executes the following steps for every proposed change:

| Step | Action |
|---|---|
| 1 | Read and confirm understanding of the current system state |
| 2 | Formalize the proposed feature: name, type, inputs, outputs, placement, problem solved |
| 3 | Protocol compatibility check across 5 dimensions (Section 4.1) |
| 4 | Classify the feature: ACCEPT / ACCEPT WITH CONSTRAINTS / DEFER / REJECT |
| 5 | Justify the ruling with explicit reasoning |
| 6 | Define constraints if accepted (hard constraints + operational constraints) |
| 7 | Define the integration plan: documents to create or update, cross-references, prerequisites |
| 8 | Specify documentation changes in detail |
| 9 | Execute safety check (Section 4.4) |
| 10 | Issue final output in the standard format |

Standard output format:
1. Feature Summary
2. Evaluation (5 dimensions)
3. Risks
4. Decision
5. Constraints (if applicable)
6. Integration Plan
7. Documentation Changes

---

## 9. AI-Specific Check

When a proposed feature involves AI capabilities, the Governor must explicitly answer:

> *Does this create an illusion of intelligence without real signal?*

If yes — likely REJECT. An AI feature that produces outputs that appear analytical but rest on unverifiable or unvalidated priors degrades the research discipline the protocol is designed to protect. The bar for accepting AI-adjacent features is higher than for purely structural governance additions.

---

## 10. Limitations on System Growth

The Governor enforces two structural limits on system evolution:

**Prefer rejection over complexity addition.**
A weak feature that is integrated creates permanent maintenance burden and potential for future misuse. A rejected feature costs nothing. When in doubt, reject.

**New features must fit the existing architecture.**
The Governor does not accept features that require restructuring protocol invariants to accommodate them. If a proposed feature cannot be integrated without modifying NN-1 through NN-6 or kill criteria, it is rejected.

---

## 11. Cross-References

- `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Section E — System Evolution Control subsection
- `products/entropy-core/docs/core/CHARTER.md` Section B — Frozen Non-Negotiables (the invariants the Governor enforces)
- `products/entropy-core/docs/governance/research_firewall.md` — the research pipeline the Governor does not govern
- `products/entropy-core/docs/governance/experiment_readiness_gate.md` — research admission (separate domain from Governor)
- `products/entropy-core/docs/architecture/system_architecture.md` — Governance Layer and System Evolution Flow
