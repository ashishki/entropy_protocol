# Entropy Protocol — AI Engineering Framework

**Version:** 1.0
**Last updated:** 2026-03-16
**Purpose:** Define how AI-assisted development works in this project. Describe roles, context-loading patterns, workflow protocols, and governance for AI collaboration.

This document is for developers using AI models as collaborators and for AI models that receive this document as context.

---

## 1. Development Model

Entropy Protocol is developed by a small founding team using AI-assisted engineering workflows.

**What this means in practice:**
- AI models are collaborators, not code generators operating in isolation
- The human team holds architectural authority and final decision-making
- AI models produce proposals, analyses, and implementations — not decisions
- All AI-generated specifications affecting protocol rules require human review before adoption

**Why AI assistance:**
- The project requires deep reasoning across quantitative finance, systems architecture, and statistical methodology simultaneously
- AI collaboration extends the effective capacity of a small team without introducing operational dependencies
- AI models can maintain precise document context across long technical sessions

---

## 2. AI Model Roles

### Architecture Reasoning (Claude)

**When used:** Architectural design decisions, protocol specification review, documentation writing, technical analysis of design tradeoffs.

**Context loaded for architecture sessions:**
1. `README.md` (orientation)
2. `core/GLOSSARY.md` (terminology)
3. `core/PROTOCOL_SPEC.md` (current specification)
4. `core/CHARTER.md` (strategic constraints)
5. `core/EVOLUTION.md` (design history — prevents re-litigation of closed questions)
6. Relevant audience brief if addressing a specific role

**Operating constraints for AI architecture sessions:**
- Do NOT redesign the protocol. Work within frozen constraints (NN-1 through NN-6).
- Do NOT introduce speculative trading strategies.
- When a proposed change touches a frozen rule, flag it explicitly rather than bypassing it.
- When producing updated specifications, use the delta-first format: state what changed and why, not just the new content.

### Code Implementation (Code Models / Claude)

**When used:** Writing evaluation engine components, SimBroker, data pipeline, portfolio layer logic.

**Context loaded for implementation sessions:**
1. `core/GLOSSARY.md` (key terms)
2. Relevant `core/PROTOCOL_SPEC.md` section for the component being built
3. Component-specific specification if one exists

**Operating constraints:**
- Implementation must match the specification exactly. Do not simplify constraints for implementation convenience.
- When a specification is ambiguous, flag the ambiguity and ask for clarification rather than inferring.
- Phase-gated components (1W overlay, shorts, treasury) are NOT implemented until the prior phase's exit criteria are met, even if the code structure is otherwise ready.

### Documentation (Claude / Other models)

**When used:** Writing audience briefs, updating glossary, maintaining evolution document, producing evaluation reports.

**Operating constraints:**
- Audience briefs (ARCHITECT_BRIEF, TRADER_BRIEF) must not contradict PROTOCOL_SPEC or CHARTER.
- When documentation drifts from the specification, the specification wins. Update the documentation.
- Never introduce new protocol rules or constraints in documentation. Document rules defined in CHARTER and PROTOCOL_SPEC.

---

## 3. Context Loading Protocol

### For New Sessions

AI models do not retain memory between sessions. Every session must be initialized with the appropriate context set.

**Standard context for any technical session:**
```
1. docs/core/GLOSSARY.md
2. docs/core/PROTOCOL_SPEC.md (or relevant sections)
3. docs/core/CHARTER.md (Non-Negotiables section minimum)
```

**Extended context for design sessions:**
```
4. docs/core/EVOLUTION.md
5. docs/README.md
```

**Minimal context for implementation-only sessions:**
```
1. docs/core/GLOSSARY.md
2. Specific `docs/core/PROTOCOL_SPEC.md` section relevant to the component
```

### Context Loading Shortcuts

When loading context for an AI model, state the following explicitly at the start of the session:

```
Current phase: Phase 0 (Evaluation Engine + SimBroker)
Current date: [DATE]
Active documents: docs/core/PROTOCOL_SPEC.md, docs/core/CHARTER.md
Frozen constraints: NN-1 through NN-6 (see docs/core/PROTOCOL_SPEC.md Section B)
```

This prevents the model from assuming earlier or later phase constraints.

### What NOT to Load

Do NOT routinely load archive documents as context:
- `archive/strategic_architecture_review_v*.md` — these contain superseded claims
- `archive/deep-research-report.md` — useful for literature background but not active rules
- Loading archive documents alongside active specs creates ambiguity about which version is current

If you need to reference a specific historical decision, load `docs/core/EVOLUTION.md` instead.

---

## 4. Specification vs Implementation

### The Specification Layer

`docs/core/PROTOCOL_SPEC.md` defines what the system must do. It is the authoritative source for:
- Phase structure and exit criteria
- Kill criteria and thresholds
- Kill criterion trigger conditions
- P&L attribution rules
- Regime signal governance

**Rules in PROTOCOL_SPEC are not negotiated in implementation.** If a rule cannot be implemented as written, the implementation problem is surfaced for human review — the rule is not silently modified.

### The Implementation Layer

Implementation documents, code, and technical specifications define how the system does it. These evolve freely within the bounds set by PROTOCOL_SPEC.

Examples of implementation-layer decisions:
- Technology stack (Python vs Rust vs Go)
- Database schema details
- API design
- Specific ML library choices
- Monitoring infrastructure

**Implementation decisions do not require charter-level review.** Architecture-pattern decisions that affect module boundaries may warrant an architecture session, but not a specification change.

---

## 5. Change Governance

### Frozen Rules (Requires Charter-Level Review)

The following cannot be changed by any AI session or implementation decision:
- NN-1: Gross leverage ≤ 1.0
- NN-2: Four-stream P&L attribution structure
- NN-3: Evaluation engine first (Phase 0 prerequisite)
- NN-4: Sequential rollout
- NN-5: Trial registry + multiplicity correction
- NN-6: Asset-class-specific stop-loss parameters
- All kill criterion threshold numbers (K1–K6, P2K1–P2K2, P4K1–P4K2)
- All phase exit criteria

A "charter-level review" requires:
1. Written justification document
2. Explicit version increment in CHARTER.md
3. Update to EVOLUTION.md with reasoning

### Evolvable Rules

The following can be updated through a normal specification update:
- Implementation details within a phase
- Technology choices
- Data provider selection (if quality equivalent)
- Monitoring metrics and tooling
- AI tooling and model choices

### New Documents

Before creating a new document:
1. Check whether the content belongs in an existing document
2. If creating, determine which category it belongs to (core / architecture / governance / research / audit / audience / archive)
3. Add it to README.md document map

Do not create documents that duplicate content from `docs/core/PROTOCOL_SPEC.md` or `docs/core/CHARTER.md`. Reference those documents instead.

---

## 6. AI-Assisted Research Governance

### Trial Registry

Every signal specification tested must be pre-registered before any data is examined. This applies equally to:
- Human-designed specifications
- AI-generated specifications
- AI-suggested modifications to existing specifications

**An AI-generated signal specification that has not been pre-registered before data examination is NOT a valid OOS result.** The evaluation protocol applies regardless of who proposed the specification.

### AT Hypotheses

AI models can be used to:
- Generate AT hypothesis candidates
- Write the one-page pre-registration spec
- Compute baseline rates on historical data (pre-registration step)

AI models cannot:
- Evaluate AT results without the pre-registration being filed first
- Suggest hypothesis modifications after data examination has begun
- Combine AT results with OOS results

### Prompt Hygiene for Signal Research

When using AI to generate or evaluate signal ideas:
- **State the hypothesis explicitly before showing any data.** "I want to test whether X predicts Y" — then show the data.
- **Do not show recent price action and ask "what signal does this suggest?"** — this is a form of look-ahead bias in signal generation.
- **Log every signal idea generated by AI in the trial registry**, even if not immediately tested. The trial count accrues against the Harvey-Liu budget.

## 7. AI Research Workflow

### AI Roles

AI can participate in research as specialized assistants, including:
- Market Observer
- Hypothesis Generator
- Null Hypothesis Auditor
- Cost Analyst
- Risk Analyst
- Regime Analyst
- Multiplicity Auditor
- Experiment Designer
- Protocol Guardian
- Research Coordinator

### Workflow Rule

These agents assist research but cannot authorize protocol actions.

They can:
- observe markets
- draft hypotheses
- critique proposals
- prepare experiment specifications
- surface governance risks

They cannot:
- approve Trial Registry admission on their own
- classify evidence as protocol-valid on their own
- override frozen rules
- route outputs directly into portfolio logic

### Required Human Control

Any protocol action requires human review and formal registration in the governed workflow.

AI participation increases research throughput, but authority remains with the human owner of the protocol.

---

## 8. Future Team Additions

### Senior Software Architect

When a senior software architect joins, provide the following context:
1. `audience/ARCHITECT_BRIEF.md` (primary onboarding document)
2. `docs/core/PROTOCOL_SPEC.md` (full)
3. `docs/core/EVOLUTION.md` (design history)
4. This document (AI workflow)

The architect's role is implementation architecture, not protocol design. Protocol design decisions are made through charter-level review.

### ML Engineer (Local Models)

When an ML engineer builds local models for specialized tasks:
1. Clearly scope which components the local model handles
2. Ensure local model outputs are fed through the trial registry if they generate signal specifications
3. Local models used for infrastructure (classification, data cleaning) do not require trial registry logging
4. Local models used for signal generation or regime detection do require logging

Document the local model's role in the implementation specification for the relevant component.

---

## 9. Documentation Health Checks

### When to Update This Document

- When a new AI model role is added to the workflow
- When the context loading protocol changes
- When new governance rules for AI assistance are established
- When a new team member or AI tool joins

### When to Update PROTOCOL_SPEC

- When a phase exit criterion changes (charter-level review required if a frozen criterion)
- When a new kill criterion is added
- When a new phase is formally added
- When an implementation detail is promoted to specification-level constraint

### When to Update EVOLUTION.md

- When a design question is conclusively resolved after debate
- When a rule that was previously debated is closed
- When a correction is applied (like v4 corrections → v5 charter)

### When to Update GLOSSARY.md

- When a new technical term is introduced in PROTOCOL_SPEC or CHARTER
- When a formula is updated (update both the spec and the glossary entry)
- When a term is deprecated or renamed

---

## 9. Version and Authorship Tracking

All core documents carry:
- Version number in the document header
- Date of last update
- Basis (what document or decision it derives from)

AI-generated document sections are not labeled separately from human-authored sections — the document is the product of the team, not of any individual contributor. Version history is tracked in git.

**Exception:** If an AI model produces a significant analysis that is incorporated into a specification, note in the git commit message that the analysis was AI-assisted. This is relevant for audit purposes if the analysis turns out to be incorrect.
