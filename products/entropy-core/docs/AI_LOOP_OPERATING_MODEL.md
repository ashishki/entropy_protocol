# Entropy Core AI Loop Operating Model

Status: Active
Date: 2026-05-12
Scope: Entropy Core development loop

This document defines how AI agents should keep Entropy Core moving through the
12 month roadmap without requiring human approval for every implementation
step.

## Loop Contract

For each task, the AI agent should:

1. read `docs/IMPLEMENTATION_CONTRACT.md`;
2. read `docs/tasks.md` for the active task and dependencies;
3. read task `Context-Refs`;
4. capture the relevant baseline;
5. implement code/tests/docs in the task file scope;
6. run task verification;
7. update evidence and compact state docs;
8. run the phase review task when the phase is complete;
9. auto-open the next phase if no human gate is triggered.

The loop should not stop after analysis when the task is implementable inside
the approved roadmap and boundaries.

## Auto-Continue Allowed

Agents may continue without human approval for:

- Python schemas, validators, serializers, loaders, and CLI commands;
- tests and fixtures using synthetic or redacted data;
- local artifact registry code;
- append-only metadata logic;
- evidence packet builders;
- reproducibility runners over local fixtures;
- docs synchronization;
- internal examples;
- refactors that preserve public behavior;
- phase reviews that do not expand scope.

## Human Gate Required

Agents must stop and ask for explicit human approval before:

- reading or unlocking holdout;
- creating OOS/performance conclusions;
- enabling live feeds by default;
- adding broker/exchange execution;
- placing, blocking, or emitting orders;
- using live capital;
- loading production credentials;
- creating production, capital-ready, investment-advice, or external-compliance
  claims;
- creating a public SDK or hosted Core service;
- adding multi-tenant SaaS behavior;
- adding Rust, Go, Java, C/C++, FFI, native extensions, or another runtime
  service;
- using real customer/private data in fixtures, logs, prompts, or committed
  artifacts;
- modifying charter-level non-negotiables.

## Phase Template

Each active phase should have:

```yaml
Phase: NN
Name: short phase name
Auto-continue: true
Goal: one executable Core capability
Allowed:
  - Python code
  - tests
  - fixtures
  - CLI
  - docs sync
Blocked:
  - holdout/live/capital/order/production surfaces
  - public SDK/hosted service unless explicitly in scope
  - new runtime without ADR and approval
Exit:
  - tests pass
  - evidence or review artifact exists
  - no P0/P1 open finding
Next:
  - next phase id
```

## Required State Documents

Keep these compact and current:

- `docs/CODEX_PROMPT.md`: active phase, next task, baseline, guardrails.
- `PHASE_HANDOFF.md`: restart instructions and next action.
- `AGENT_NOTES.md`: short current decision and key links.
- `docs/tasks.md`: authoritative task graph.
- `docs/EVIDENCE_INDEX.md`: durable proof pointers.
- `docs/IMPLEMENTATION_JOURNAL.md`: append-only handoff history.

Do not turn active state files into long historical logs. Long history belongs
in the journal, evidence index, audit reports, or archives.

## Phase Review Rule

The last task of every phase is a review task. It must answer:

- what executable capability was added;
- what evidence proves it;
- which restricted surfaces remain blocked;
- whether any P0/P1 finding blocks continuation;
- whether the next phase can open automatically.

If the review passes and no human gate is triggered, the next phase opens in the
same development loop.

