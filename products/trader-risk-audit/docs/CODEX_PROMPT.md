# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-07
Phase: 1

This file is the single source of truth for implementation session state. Every Codex agent reads this file before starting work and updates it at phase boundaries or when the orchestrator records findings.

---

## Current Phase

- Phase: 1
- Name: Foundation
- Business goal: establish the local Python package skeleton, CI contract, and first smoke-test baseline for deterministic Trader Risk Audit implementation.
- Phase gate: Phase 1 validation passes, T01-T03 complete, pytest baseline recorded, ruff clean, and CI workflow present.

## Current State

- Phase: 1
- Baseline: 0 passing tests (pre-implementation)
- Ruff: not yet configured
- Last CI: not yet configured
- Last updated: 2026-05-07
- Session tokens (approx): not yet tracked
- Cumulative phase tokens (approx): not yet tracked

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Task graph: `docs/tasks.md`
- Implementation contract: `docs/IMPLEMENTATION_CONTRACT.md`
- Task-scoped context: read `Context-Refs` in `docs/tasks.md` before broad searching.

## Next Task

T01: Project Skeleton

Before implementation, the orchestrator should hand Codex a narrow task digest inline:

- assignment and acceptance criteria
- file scope
- applicable contract rules only
- dependency facts from prior tasks
- immediate pipeline or flow if one matters

Only send Codex to full documents when the task is architecture-shaping, security-sensitive, ambiguous, or too risky to compress safely.

## Fix Queue

empty

## Open Findings

none

## Completed Tasks

none

## Phase History

none

## Summary State

No compacted phase summaries yet.

## Compaction Protocol

- Trigger when `## Completed Tasks` exceeds 20 entries or `## Phase History` exceeds 5 phase summaries.
- Preserve current phase, baseline, next task, open findings, active decisions, and evidence pointers.
- Move older detail into an archive section rather than deleting it.

---

## Profile State: RAG

- RAG Status: OFF
- Active corpora: n/a
- Retrieval baseline: n/a
- Open retrieval findings: none
- Index schema version: n/a
- Pending reindex actions: none
- Retrieval-related next tasks: none
- Retrieval-driven tasks: none

## Tool-Use State

- Tool-Use Profile: OFF
- Registered tool schemas: n/a
- Unsafe-action guardrails: n/a
- Open tool findings: none

## Agentic State

- Agentic Profile: OFF
- Active agent roles: n/a
- Loop termination contract version: n/a
- Cross-iteration state mechanism: n/a
- Open agent findings: none

## Planning State

- Planning Profile: OFF
- Plan schema version: n/a
- Plan validation method: n/a
- Open plan findings: none

## Compliance State

- Compliance Status: OFF
- Active frameworks: n/a
- Controls implemented: n/a
- Controls partial: n/a
- Controls not started: n/a
- Evidence artifact: n/a
- Open compliance findings: none

## NFR Baseline

- API p99 latency: n/a (no API in v1)
- Batch audit duration: not yet measured
- Error rate: not yet measured
- Throughput: not yet measured
- Last measured: n/a
- NFR regression open: No

## Evaluation State

### Last Evaluation

- Profile: n/a
- Task: n/a
- Date: n/a
- Eval Source: n/a
- Metric(s): n/a
- Score: n/a
- Baseline: n/a
- Delta: n/a
- Regression: n/a

### Open Evaluation Issues

none

### Evaluation History

none

---

## Instructions for Codex

1. Read `docs/IMPLEMENTATION_CONTRACT.md` before starting any task.
2. Read the full task definition in `docs/tasks.md` before writing code.
3. Read all Depends-On tasks to understand interface contracts.
4. Read task `Context-Refs` and relevant continuity artifacts when the task depends on prior decisions, proof, findings, rule semantics, attribution, retention, or report claims.
5. Run `pytest -q` to capture the current baseline before making changes. If the baseline is broken, stop and report the blocker.
6. Run `ruff check`. It must exit 0 before implementation starts. Fix ruff issues first in a separate commit.
7. Write tests before or alongside implementation. Every acceptance criterion has a passing test.
8. Update this file at every phase boundary with the new baseline, next task, and open findings.
9. Commit with format `type(scope): description` - one logical change per commit.
10. When done, return `IMPLEMENTATION_RESULT: DONE` with the new baseline, tests run, and files changed.
11. When blocked, return `IMPLEMENTATION_RESULT: BLOCKED` with the exact blocker, command output summary, and affected files.

## Phase 1 Validation

Phase 1 validation has not run yet. The orchestrator should run the Phase 1 Validator before starting T01 and write `docs/audit/PHASE1_AUDIT.md`.
