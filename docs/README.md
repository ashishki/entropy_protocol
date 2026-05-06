# Entropy Protocol — Documentation

**Last updated:** 2026-05-06
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

Current development status: Phase 1D-K archive-only baseline path completed and
deep-reviewed. Review fixes are applied; holdout, production/capital-ready
labels, live feeds, broker integration, Growth/RDL/RBE activation, and
OOS/performance claims remain blocked.

---

## Documentation Map

- [`core/`](./core/) -> protocol and system principles
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) -> active implementation architecture
- [`spec.md`](./spec.md) -> active implementation feature specification
- [`tasks.md`](./tasks.md) -> implementation task graph and remediation tasks
- [`architecture/`](./architecture/) -> engineering architecture
- [`governance/`](./governance/) -> research discipline
- [`research/`](./research/) -> research reports
- [`audit/`](./audit/) -> current protocol audit surface
- [`audience/`](./audience/) -> external briefs
- [`archive/`](./archive/) -> historical materials

## Core Documents (start here)

| Document | Purpose | Audience |
|---|---|---|
| [`core/CHARTER.md`](./core/CHARTER.md) | Project intent, non-negotiables, phase roadmap | All |
| [`core/PROTOCOL_SPEC.md`](./core/PROTOCOL_SPEC.md) | Engineering specification: rules, thresholds, exit criteria | Developers, AI models |
| [`core/GLOSSARY.md`](./core/GLOSSARY.md) | Terms, formulas, abbreviations | AI models, new team members |
| [`core/EVOLUTION.md`](./core/EVOLUTION.md) | Design decision history: why constraints exist (v1->v5) | Architects, AI models |
| [`core/ERA0_SPEC.md`](./core/ERA0_SPEC.md) | Proposed hardening package for unresolved protocol blockers; non-canonical until approved and merged | Spec owner, architects |

## Architecture

| Document | Purpose | Audience |
|---|---|---|
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Active implementation architecture for the Python package and CI/runtime boundaries | Developers, AI models |
| [`spec.md`](./spec.md) | Active implementation feature specification for Phase 0 infrastructure | Developers, AI models |
| [`tasks.md`](./tasks.md) | Task graph, acceptance criteria, and remediation queue | Developers, orchestrator |
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
| [`governance/research_portfolio_monitor.md`](./governance/research_portfolio_monitor.md) | Read-only dashboard: factual state of research portfolio by family | Developers, researchers |
| [`governance/governor.md`](./governance/governor.md) | Protocol Governor: mandatory gate for all system-level changes | Architects, spec owner |

## Research

| Document | Purpose | Audience |
|---|---|---|
| [`research/deep-research-report_v2.md`](./research/deep-research-report_v2.md) | Current literature-backed research synthesis | Architects, spec owner |

## Audit

| Document | Purpose | Audience |
|---|---|---|
| [`audit/README.md`](./audit/README.md) | Audit loading rules and current boundary | Spec owner, developers |
| [`audit/AUDIT_INDEX.md`](./audit/AUDIT_INDEX.md) | Compact current audit artifact register | Spec owner, developers |
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
2. `CODEX_PROMPT.md` (current handoff and next task)
3. `tasks.md` current task section
4. Relevant code/tests for the task

Load core protocol documents only when the task changes architecture, phase
gates, formula/statistical logic, Growth/RDL/RBE, live data, or report/claim
semantics.

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

**Current work:** Spec Owner next decision after D-K fix closure.

**Last completed task:** DK-REVIEW-001 Full D-K Deep Review And Fix Closure.

**Review cadence:** light review after each phase; deep review after the full
D-K block.

**Approved scope:** Review and decision work over the completed Phase 1D-K
archive-only baseline block. No live, production, capital-ready, or
holdout-opening work is approved by default.

**Visible roadmap:** Phase 1 D-K is now recorded in `docs/tasks.md`: P1D
implementation contract, P1E bounded baseline implementation, P1F registration
integration, P1G evaluation run contract, P1H first governed evaluation, P1I
report/audit packet, P1J research decision/holdout gate, and optional P1K final
research closure.

**Not approved:** full Phase 1 evaluation/trading, live/streaming feeds, broker
integration, live capital, archive holdout reads, portfolio/backtest evaluation,
Growth/RDL/RBE activation, strategy performance metrics, non-Python
runtime/toolchain introduction without the escalation gate, OOS/performance
claims, production labels, or capital-ready labels.

The compact session handoff is `docs/CODEX_PROMPT.md`. Historical handoff state
is available through git history and the implementation journal.

---

## Archive Discipline

Default context stays compact. Historical task graph, decision, evidence, and
implementation logs are archived under `docs/archive/session_state/`. Phase 1A
and post-Phase1A audit packets are archived under `docs/audit/archive/phase1a/`.

Load archived files only when a current task explicitly needs old acceptance
criteria, evidence, or rationale.
