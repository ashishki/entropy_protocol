# Entropy Protocol — Documentation

**Last updated:** 2026-03-16
**Status:** Active

---

## What Is This Project

Entropy Protocol is a **systematic capital allocation and research governance architecture**.

It is NOT a trading bot, signal generator, or alpha discovery tool.

It provides:
- Walk-forward evaluation infrastructure with strict IS/OOS separation
- Trial registry and multiplicity control
- SimBroker cost and slippage modeling
- Regime governance and portfolio allocation logic
- Structured risk escalation rules

Current classification: **Research Lab** (Era 0–2).
Conditional destination: **Capital Allocation Framework** (Era 3+, after Phase 1 exit criteria met).

---

## Documentation Map

- [`core/`](./core/) -> protocol and system principles
- [`architecture/`](./architecture/) -> engineering architecture
- [`governance/`](./governance/) -> research discipline
- [`research/`](./research/) -> research reports
- [`audit/`](./audit/) -> protocol audits
- [`audience/`](./audience/) -> external briefs
- [`archive/`](./archive/) -> historical materials

## Core Documents (start here)

| Document | Purpose | Audience |
|---|---|---|
| [`core/CHARTER.md`](./core/CHARTER.md) | Project intent, non-negotiables, phase roadmap | All |
| [`core/PROTOCOL_SPEC.md`](./core/PROTOCOL_SPEC.md) | Engineering specification: rules, thresholds, exit criteria | Developers, AI models |
| [`core/GLOSSARY.md`](./core/GLOSSARY.md) | Terms, formulas, abbreviations | AI models, new team members |
| [`core/EVOLUTION.md`](./core/EVOLUTION.md) | Design decision history: why constraints exist (v1->v5) | Architects, AI models |

## Architecture

| Document | Purpose | Audience |
|---|---|---|
| [`architecture/AI_ENGINEERING_FRAMEWORK.md`](./architecture/AI_ENGINEERING_FRAMEWORK.md) | How AI-assisted development works in this project | Developers, AI models |
| [`architecture/workflow_ai_development.md`](./architecture/workflow_ai_development.md) | Development workflow and audit governance | Developers, spec owner |
| [`architecture/system_architecture.md`](./architecture/system_architecture.md) | Layered system overview and authority boundaries | Architects, developers |
| [`architecture/research_discovery_layer.md`](./architecture/research_discovery_layer.md) | AI-assisted research discovery boundary and allowed outputs | Architects, developers |
| [`architecture/research_knowledge_graph.md`](./architecture/research_knowledge_graph.md) | Minimal structured research memory model | Architects, developers |

## Governance

| Document | Purpose | Audience |
|---|---|---|
| [`governance/research_firewall.md`](./governance/research_firewall.md) | Separation between discovery and admissible evaluation | Developers, AI models |
| [`governance/experiment_readiness_gate.md`](./governance/experiment_readiness_gate.md) | Checklist for experiment admission to the Trial Registry | Developers, researchers |
| [`governance/hypothesis_families.md`](./governance/hypothesis_families.md) | Canonical family tags for experiment classification | Developers, researchers |

## Research

| Document | Purpose | Audience |
|---|---|---|
| [`research/deep-research-report_v2.md`](./research/deep-research-report_v2.md) | Current literature-backed research synthesis | Architects, spec owner |

## Audit

| Document | Purpose | Audience |
|---|---|---|
| [`audit/AUDIT_v1.md`](./audit/AUDIT_v1.md) | Baseline quantitative integrity audit | Architects, spec owner |
| [`audit/AUDIT_INDEX.md`](./audit/AUDIT_INDEX.md) | Current audit artifact register | Spec owner, developers |
| [`audit/REVIEW_REPORT.md`](./audit/REVIEW_REPORT.md) | Consolidated current-cycle audit status | Spec owner, developers |

## Audience-Specific Briefs

| Document | Purpose | Audience |
|---|---|---|
| [`audience/ARCHITECT_BRIEF.md`](./audience/ARCHITECT_BRIEF.md) | System architecture stress-test brief | Senior architects |
| [`audience/TRADER_BRIEF.md`](./audience/TRADER_BRIEF.md) | Framework explanation for practitioners contributing hypotheses | External contributors |

---

## Reading Order

**For a new developer or AI model context-loading:**
1. This README (orientation)
2. `core/GLOSSARY.md` (terminology)
3. `core/PROTOCOL_SPEC.md` Section B (frozen non-negotiables)
4. `core/PROTOCOL_SPEC.md` Section C-D (phase structure and exit criteria)
5. `core/CHARTER.md` Section D (regime signal governance)
6. `architecture/AI_ENGINEERING_FRAMEWORK.md` (development workflow)

**For a senior architect joining the team:**
1. This README
2. `audience/ARCHITECT_BRIEF.md`
3. `core/CHARTER.md` (full)
4. `core/EVOLUTION.md` (design history)

**For an external practitioner:**
1. `audience/TRADER_BRIEF.md`

---

## Document Governance

**Frozen documents:** `core/CHARTER.md` Section B (Non-Negotiables), all kill criteria, all phase exit criteria thresholds. These require a written justification document and explicit version increment. Inline edits are not permitted.

**Evolvable documents:** `core/PROTOCOL_SPEC.md` implementation sections, `architecture/AI_ENGINEERING_FRAMEWORK.md`, architecture docs, governance docs, and audience briefs. These can be updated as the system evolves.

**Archived documents:** historical reasoning in `archive/`. Never modified after archiving. Referenced by date and version label.

**Version naming convention:**
- Core documents use `UPPERCASE_NAME.md` with no version in the filename. Version is tracked in the document header and git log.
- Audience documents: same convention.
- Archive: original filenames preserved.

---

## Current Phase

**Phase 0 (active):** Evaluation engine + SimBroker construction.
**Parallel:** Hypothesis Acceleration Track (paper-only).

No signal receives an OOS evaluation label until Phase 0 exit criteria are met. See `core/PROTOCOL_SPEC.md` Phase 0 for criteria.

---

## Current Stabilization Plan (What and Why)

The system is intentionally large. Current work is focused on reducing ambiguity, not adding new complexity.

What we are doing now:
1. Make regime control deterministic (`P3/P4`): same inputs must produce same risk action.
2. Lock RDL boundaries: Phase 0-1 scaffolding only; Phase 2 enables research operations; routing influence only after Phase 2 exit.
3. Make audit evidence machine-checkable: add mode flags, attestation queries, and structured transition logs.
4. Normalize core metrics language: net Sharpe is always `(a+b+c)` in every table and report.
5. Close governance loopholes: persistent near-zero skill weight is treated as strategy modification (GE-3), not discretionary reweighting.
6. Formalize RBE approval artifact: "charter-level review" now maps to a required packet schema.

Why this matters:
- Phase gates become auditable and reproducible.
- Fewer "interpretation" paths during stress periods.
- Lower risk of accidental policy bypass.
- Better operator confidence: clear rules before adding new modules.

Tracking sources:
- `docs/audit/REVIEW_REPORT.md` (Cycle 1 findings F-22..F-32)
- `docs/tasks.md` (Audit Findings Backlog + Implementation Notes)
