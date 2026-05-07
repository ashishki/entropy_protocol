# CODEX_PROMPT.md

Version: 1.3
Date: 2026-05-07
Phase: 5

This file is the single source of truth for implementation session state. Every Codex agent reads this file before starting work and updates it at phase boundaries or when the orchestrator records findings.

---

## Current Phase

- Phase: 5
- Name: Concierge Pilot Workflow
- Business goal: wire a complete local pilot workflow that produces reproducible audit artifacts, delivery-ready text, retention controls, and regression fixtures.
- Phase gate: T17-T20 complete; a local operator can run a complete anonymized audit and reproduce the same artifact hashes; pytest baseline recorded; ruff clean.

## Current State

- Phase: 5
- Baseline: 61 passing tests
- Ruff: clean (`ruff check` and `ruff format --check`)
- Last CI: workflow configured; remote run not observed from this clone
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

none - Phase 5 complete

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

- T01: Project Skeleton
- T02: CI Setup
- T03: Baseline Smoke Tests
- T04: Canonical Trade Schema
- T05: Trade Export Importer
- T06: Risk Policy Schema
- T07: Policy Review Packet
- T08: Session Calendar and Aggregates
- T09: Position and Asset Rule Evaluators
- T10: Loss, Drawdown, and Cooldown Evaluators
- T11: Violation Record Determinism
- T12: Violation P&L Attribution
- T13: Report Model and Summaries
- T14: Markdown Report Generator
- T15: Claim Guard and Disclaimers
- T16: Artifact Manifest and Reproducible Hashes
- T17: End-to-End Audit CLI
- T18: Telegram-Ready Delivery Packet
- T19: Local Retention and Deletion Workflow
- T20: Pilot Regression Fixture Pack

## Phase History

- Phase 1 Foundation complete: T01-T03 delivered package skeleton, CI contract, and baseline smoke tests. Baseline moved from 6 to 9 passing tests. Deep review Cycle 1 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 2 Input Contracts complete: T04-T07 delivered canonical trade records, CSV import normalization, risk policy schema, and policy review packets. Baseline moved from 9 to 21 passing tests. Deep review Cycle 2 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 3 Rule Evaluation complete: T08-T12 delivered session aggregation, deterministic evaluators, violation determinism, and reconciled P&L attribution with golden evidence. Baseline moved from 21 to 37 passing tests. Deep review Cycle 3 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 4 Reporting and Artifacts complete: T13-T16 delivered deterministic report data, Markdown output, claim guard validation, and reproducible artifact manifests. Baseline moved from 37 to 49 passing tests. Deep review Cycle 4 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 5 Concierge Pilot Workflow complete: T17-T20 delivered end-to-end local audit CLI, Telegram-ready copy packet, retention/delete controls, and anonymized pilot regression fixtures. Baseline moved from 49 to 61 passing tests. Deep review Cycle 5 found P0:0, P1:0, P2:0; Stop-Ship: No.

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

Phase 1 validation was not run before T01 in this workspace, and `docs/audit/PHASE1_AUDIT.md` is absent. Cycle 1 review recorded this as a non-blocking governance warning because the workspace had already advanced to T03 when the orchestrator resumed.
