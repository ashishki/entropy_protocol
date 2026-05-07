# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-07
Phase: 1

Reset state for Entropy Core after archiving the old active workflow. Historical files are available under `docs/legacy/old-workflow/2026-05-07/` but are not read by default.

---

## Current Phase

- Phase: 1
- Name: Reset Foundation
- Business goal: establish the new AI Workflow Playbook loop over the existing Core codebase with Python 3.12 tooling, product-local CI, and a recorded baseline.
- Phase gate: Phase 1 validation passes, T01-T03 complete, pytest baseline recorded, ruff and pyright clean, and CI workflow present.

## Current State

- Phase: 1
- Baseline: 0 passing tests (reset governance pre-implementation; manual sanity check 2026-05-07: 277 passed, 20 skipped)
- Ruff: clean on manual sanity check 2026-05-07
- Pyright: clean on manual sanity check 2026-05-07
- Last CI: not yet configured after reset
- Holdout: locked
- Live capital: not approved
- Broker/exchange integration: not approved
- OOS/performance claims: not approved
- Last updated: 2026-05-07

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Legacy summary: `docs/legacy/CORE_LEGACY_SUMMARY.md`
- Old active workflow archive: `docs/legacy/old-workflow/2026-05-07/`
- Protocol docs: `docs/core/`
- Governance docs: `docs/governance/`

## Next Task

T01: Existing Project Baseline Skeleton

## Fix Queue

empty

## Open Findings

none after reset. Legacy D-K findings were closed in the prior workflow, but old findings are not active unless re-opened by a reset task or review.

## Completed Tasks

none in the reset task graph.

## Phase History

none in the reset task graph.

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

## Verification Defaults

Run from `products/entropy-core/`:

- `.venv/bin/python -m pytest -q tests/`
- `.venv/bin/python -m ruff check src/entropy tests`
- `.venv/bin/python -m ruff format --check src/entropy tests`
- `.venv/bin/python -m pyright src/entropy`
- `git diff --check`

## Instructions for Codex

1. Read `docs/IMPLEMENTATION_CONTRACT.md` before starting any task.
2. Read the full task definition in `docs/tasks.md` before writing code.
3. Read all Depends-On tasks to understand interface contracts.
4. Read task `Context-Refs` and relevant continuity artifacts when the task depends on prior decisions, evidence, findings, registry, governance, leakage, holdout, attribution, product bridges, migrations, or runtime/language boundaries.
5. Run the verification defaults needed for the task and capture the pre-task baseline.
6. Write tests before or alongside implementation. Every acceptance criterion has a passing test.
7. Update this file at every phase boundary with baseline, next task, and open findings.
8. Commit with format `type(scope): description` - one logical change per commit.
9. When done, return `IMPLEMENTATION_RESULT: DONE` with tests run, baseline, and files changed.
10. When blocked, return `IMPLEMENTATION_RESULT: BLOCKED` with the exact blocker.

## Phase 1 Validation

Phase 1 validation has not run in the reset loop. The orchestrator should run the Phase 1 Validator before starting T01 and write `docs/audit/PHASE1_AUDIT.md`.
