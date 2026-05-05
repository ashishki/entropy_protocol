# Entropy Protocol — Documentation

**Last updated:** 2026-05-05
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

**Current work:** P1D-001 Long-Only Implementation Contract.

**Next task:** define the bounded long-only implementation contract before any
transition from schema-only stubs to executable baseline logic.

**Approved scope:** Phase 1D implementation planning only. This is part of the
Phase 1 workstream, but no executable baseline logic or Phase 1
evaluation/trading step is approved by default.

**Not approved:** full Phase 1 evaluation/trading, live/streaming feeds, broker
integration, live capital, archive holdout reads, portfolio/backtest evaluation,
Growth/RDL/RBE activation, strategy performance metrics, non-Python
runtime/toolchain introduction without the escalation gate, OOS/performance
claims, production labels, or capital-ready labels.

The compact session handoff is `docs/CODEX_PROMPT.md`. Historical handoff state
is available through git history and the implementation journal.

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

---

## Recent Addition — Research Portfolio Monitor (2026-03-23)

### What was added

`governance/research_portfolio_monitor.md` — a new governance document defining the **Research Portfolio Monitor (RPM)**: a read-only dashboard that displays the factual state of the research portfolio by hypothesis family.

The RPM introduces three governed signal classes:

- **Class ATT (Attention Signals)** — human-preregistered conditions evaluated mechanically against Trial Registry data. When a condition is met, the system reports: "The state of [X] is [Y]." No inference is added. The human defines the condition; the system checks it.
- **Class DM (Derived Metrics)** — factual metrics computed from registry data with all inputs visible: X-of-Y counts, means with mandatory basis counts, budget headroom. Percentages without visible denominators are prohibited.
- **Class SC (Session Comparison)** — a manual point-in-time diff between the current state and one named, timestamped snapshot. Output is a signed integer delta. No directional framing, no trend inference, no accumulated history.

Two output types are newly formally prohibited (F-6, F-7):

- **F-6: trend inference** — moving averages, rate-of-change indicators, "improving/declining" language
- **F-7: denominator-collapsed ratios** — any percentage without a visible denominator

`PROTOCOL_SPEC.md` updated to v1.7. `CHARTER.md` updated to v5.2 and `GLOSSARY.md` updated to v1.3 for D-010 formula-bearing implementation mitigations. The v1.6 RPM update remains active.

### Why it was added

Two gaps existed that the existing governance controls did not address:

1. **No cross-family evidence review.** The hypothesis budget (max 3/week, 1 active/family) controls the rate of new experiments but provides no view of what has actually been learned across families. A researcher has no structured way to see which families have accumulated results, which are stale, and where the multiplicity budget is being consumed.

2. **No redundancy detection.** Nothing in the existing pipeline detects when a candidate hypothesis is semantically near-duplicate to an already-registered trial. Redundant hypotheses consume multiplicity budget without producing new information.

### What the RPM explicitly does not do

The RPM produces no recommendations, no priority rankings, no composite quality scores, and no AI-generated assessments. It has no write access to the Trial Registry. Its outputs cannot be cited as admissible evidence in phase gates or kill criterion evaluations. All decisions informed by RPM output require a named human sponsor. The human interprets the data; the system only surfaces it.
