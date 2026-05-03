# CODEX_PROMPT.md

Version: 1.1
Date: 2026-05-03
Phase: 1

<!--
This file is the single source of truth for session state.
Every Codex agent reads this file before starting work.
Every Codex agent updates this file before committing at a phase boundary.
The orchestrator reads this file at the start of every session.

Never delete history from this file. Append; do not replace.
-->

---

## Current State

- **Phase:** 1
- **Baseline:** 9 passing tests (1 skipped — postgres, requires CI)
- **Ruff:** configured (pyproject.toml)
- **Last CI run:** not yet configured (ci.yml created)
- **Last updated:** 2026-05-03 (v1.1 — Cycle 2 review patch: Fix Queue, Open Findings, version bump)
- **Session tokens (approx):** not yet tracked
- **Cumulative phase tokens (approx):** not yet tracked

---

## Continuity Pointers

- **Decision log:** `docs/DECISION_LOG.md`
- **Implementation journal:** `docs/IMPLEMENTATION_JOURNAL.md`
- **Evidence index:** `docs/EVIDENCE_INDEX.md`
- **Task-scoped context:** read `Context-Refs` in `docs/tasks.md` before broad searching

---

## Next Task

**T04: Market Data Models**

Before implementation, the orchestrator should hand Codex a narrow task digest inline:

- assignment and acceptance criteria
- file scope
- applicable contract rules only
- dependency facts from prior tasks
- immediate pipeline / flow if one matters

Only send Codex to full documents when the task is architecture-shaping, security-sensitive, ambiguous, or otherwise too risky to compress safely.

---

## Fix Queue

─── Fix Queue (resolve before Phase 1 queue proceeds past T-GOV-1) ────────────────────────

FIX-1 [P1] — ARCH-3: Phase Gate Inconsistency — Spec Owner Disposition Required
  File: docs/DECISION_LOG.md · Change: add disposition entry choosing scope-separation (a) or resolution-gate (b) for protocol-level P0 findings · Test: grep 'ARCH-3' docs/DECISION_LOG.md non-empty; grep 'ARCH-3' docs/CODEX_PROMPT.md non-empty

<!--
The Fix Queue contains items that must be addressed before the next phase gate,
but that were deferred from the current task. Format:

- FQ-01: [T-NN] Description of what must be fixed. Added: YYYY-MM-DD.
- FQ-02: [T-NN] Description. Added: YYYY-MM-DD.
-->

---

## Open Findings

### P1 Findings (block next phase gate)

- P1-01: [CYCLE-2] ARCH-3 — Phase gate inconsistency: Phase 1 implementation active while protocol-level P0 findings (F-1, F-2, F-4, F-5, F-30, F-31) remain Inherited-Open or Partial-Mitigation from Cycle 1 REVIEW_REPORT. No formal scope-separation decision or Spec Owner waiver documented. File: docs/DECISION_LOG.md (entry required). Must be resolved (Spec Owner disposition written) before T04 proceeds. Opened: 2026-05-03. Task: T-GOV-1.

### P2 Findings (must resolve within 3 cycles)

- P2-01: [CYCLE-2] ARCH-1 / CODE-3 — `entropy health` CLI command absent; OBS-3 contract unmet. File: entropy/cli.py. Opened: 2026-05-03. Age: 0 cycles. Task: T-OBS-1.
- P2-02: [CYCLE-2] CODE-1 — No unit tests for entropy/tracing.py and entropy/metrics.py; get_tracer(), increment_counter(), record_histogram() have zero test coverage. File: entropy/tracing.py:8-10, entropy/metrics.py:7-21. Opened: 2026-05-03. Age: 0 cycles. Task: T-OBS-2.
- P2-03: [CYCLE-2] CODE-2 — get_tracer() annotated as -> NoOpTracer instead of -> opentelemetry.trace.Tracer; type drift risk when OBS profile activated. File: entropy/tracing.py:8. Opened: 2026-05-03. Age: 0 cycles. Task: T-OBS-2.
- P2-04: [CYCLE-2] CODE-4 — postgres_connection fixture lacks transaction rollback; future INSERT tests will contaminate DB state across runs. File: tests/conftest.py:13-27. Opened: 2026-05-03. Age: 0 cycles. Task: T-DB-1.
- P2-05: [CYCLE-2] ARCH-2 — docs/adr/ directory absent; ADR governance path declared but not bootstrapped. Opened: 2026-05-03. Age: 0 cycles.
- P2-06: [CYCLE-2] ARCH-4 — docs/ARCHITECTURE.md Component Table omits RDL, Research Firewall, ERG, RPM, Governor; enforcement mapping to implementation modules missing. File: docs/ARCHITECTURE.md:113-128. Opened: 2026-05-03. Age: 0 cycles.
- P2-07: [CYCLE-2] ARCH-5 — docs/core/ERA0_SPEC.md authority status undefined; not referenced in any canonical document. Spec Owner disposition required. Opened: 2026-05-03. Age: 0 cycles.
- P2-08: [CYCLE-2] ARCH-6 — docs/README.md states "Phase 0 (active)"; docs/ARCHITECTURE.md and docs/spec.md absent from Documentation Map. File: docs/README.md. Opened: 2026-05-03. Age: 0 cycles.

<!--
Open findings from review cycles. Format:

### P1 Findings (block next phase gate)
- P1-01: [CYCLE-N] Finding description. File: path/to/file.py, line N. Must be resolved before Phase {N+1}.

### P2 Findings (must resolve within 3 cycles)
- P2-01: [CYCLE-N] Finding description. File: path/to/file.py. Opened: YYYY-MM-DD. Age: 0 cycles.

### P3 Findings (optional)
- P3-01: [CYCLE-N] Finding description.

P2 Age Cap: any P2 open for more than 3 review cycles must be resolved, escalated to P1,
or formally deferred to v2 (with ADR) before the next phase gate.
-->

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

---

## Tool-Use State

- Tool-Use Profile: OFF
- Registered tool schemas: n/a
- Unsafe-action guardrails: n/a
- Open tool findings: none

---

## Agentic State

- Agentic Profile: OFF
- Active agent roles: n/a
- Loop termination contract version: n/a
- Cross-iteration state mechanism: n/a
- Open agent findings: none

---

## Planning State

- Planning Profile: OFF
- Plan schema version: n/a
- Plan validation method: n/a
- Open plan findings: none

---

## Compliance State

- Compliance Status: OFF
- Active frameworks: n/a
- Controls implemented: n/a
- Controls partial: n/a
- Controls not started: n/a
- Evidence artifact: n/a
- Open compliance findings: none

---

## NFR Baseline

- API p99 latency: not yet measured
- Error rate: not yet measured
- Throughput: not yet measured
- Last measured: —
- NFR regression open: No

---

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

| Date | Task | Profile | Key metric | Score | Baseline | Delta | Regression? |
|------|------|---------|------------|-------|----------|-------|-------------|

---

## Completed Tasks

- T01: Project Skeleton — completed 2026-05-03. Baseline after: 4 tests.
- T02: CI Setup — completed 2026-05-03. Baseline after: 8 tests.
- T03: Smoke Tests — completed 2026-05-03. Baseline after: 9 pass, 1 skip.

<!--
Append completed tasks here. Format:

- T01: Project Skeleton — completed YYYY-MM-DD. Baseline after: N tests.
- T02: CI Setup — completed YYYY-MM-DD. Baseline after: N tests.
-->

---

## Phase History

<!--
Append phase summaries here at each phase gate. Format:

### Phase 1 — Foundation
Closed: YYYY-MM-DD
Baseline at gate: N passing tests
Tasks: T01, T02, T03
Review cycle: CYCLE-1 (see docs/audit/CYCLE1_REVIEW.md)
P1s resolved: N
P2s open: N
Gate approved by: {human name or "auto"}
-->

---

## Compaction Protocol

### Compaction triggers

Compact when EITHER condition is true:
- `## Completed Tasks` contains more than 20 entries, OR
- `## Phase History` contains more than 5 phase summaries

### How to compact

1. Create or update a `## Summary State` section immediately after `## Current State`:
   - Current phase and next task
   - Active capability profiles and their status
   - Open findings by severity: P1: N, P2: N
   - Current test baseline
   - Last evaluation result (if any profile is active)
   - This section must be self-sufficient: the Orchestrator must be able to resume from it alone.

2. In `## Completed Tasks`: retain the 5 most recent entries. Move all older entries to `## Archived Tasks` (create the section at the end of the file if it does not exist).

3. In `## Phase History`: retain the 2 most recent phase summaries. Move older summaries to `## Archived Phase History` (create at the end of the file if absent).

4. Rules:
   - Do NOT delete any content — only move older entries to Archive sections.
   - Archive sections are kept in this file; they are not required reading for normal operation.
   - After compaction, `## Summary State` must fit within ~50 lines.

---

## Instructions for Codex

Read these instructions every time you pick up a task. Do not skip steps.

### Pre-Task Protocol (mandatory — do not skip)

1. **Read the orchestrator's inline task digest first** — assignment, acceptance criteria, file scope, dependency facts, and applicable rules should already be summarized there.
2. **Read `docs/tasks.md` for the current task entry only** when the digest references details that must be copied exactly.
3. **Read `docs/IMPLEMENTATION_CONTRACT.md` only if the digest did not inline the applicable rules** or if the task crosses a risky boundary.
4. **Read Depends-On tasks, `Context-Refs`, and continuity artifacts only when required** — mandatory for architecture changes, risky boundaries, open findings, or tasks where prior interfaces / evidence materially constrain the implementation.
5. **Run `pytest -q`** — capture the current baseline. Record: `N passing, M failed`. If M > 0, stop and report: you cannot add failures to an already-failing baseline.
6. **Run `ruff check`** — must exit 0. If not, fix ruff issues first. Commit the ruff fix separately with message `chore(lint): resolve ruff issues`. Then re-run the pre-task protocol.
7. **Write tests before or alongside implementation.** Every acceptance criterion has exactly one corresponding test (or more, never zero).

### During Implementation

- Work on one task at a time.
- Read only the files you need. Use `grep` to find relevant sections first.
- Do not modify files outside the task's scope without documenting why.
- If you discover an interface mismatch or missing dependency, stop and report it. Do not silently patch adjacent tasks.
- If you supersede a prior decision or close a repeated finding, update `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, and `docs/EVIDENCE_INDEX.md` as applicable.

### Post-Task Protocol

1. Run `pytest -q` — baseline must be >= pre-task baseline. If lower, something broke; fix it before committing.
2. Run `ruff check entropy/ tests/` — must exit 0.
3. Run `ruff format --check entropy/ tests/` — must exit 0.
4. **If this task has a capability tag** (`rag:*`, `tool:*`, `agent:*`, `plan:*`) — evaluation is required before marking DONE. (All profiles are OFF in Entropy Protocol v1; this step is never triggered in Phase 0.)
5. Update this file (`docs/CODEX_PROMPT.md`):
   - New baseline (number of passing tests)
   - Move this task to "Completed Tasks"
   - Set "Next Task" to the next task
   - Add any new open findings discovered during this task
6. Commit with format: `type(scope): description` — one logical change per commit.
7. If the task produced multiple logical changes (migration + service + tests), use multiple commits.

### Return Format

When done, return exactly:

```
IMPLEMENTATION_RESULT: DONE
New baseline: {N} passing tests
Commits: {list of commit hashes and messages}
Notes: {anything the orchestrator should know — surprises, deviations, decisions made}
```

When blocked, return exactly:

```
IMPLEMENTATION_RESULT: BLOCKED
Blocker: {exact description of what is blocking progress}
Type: dependency | interface_mismatch | environment | ambiguity
Recommended action: {what the orchestrator or human should do}
Progress made: {what was completed before hitting the blocker}
```

### Commit Message Format

```
type(scope): short description (imperative mood, <=72 chars)

Optional body: explain why, not what. The diff shows the what.
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `security`

Do not include:
- `Co-Authored-By` lines
- Credentials or secrets
- TODO comments without a task reference (`# TODO: see T{NN}`)
- Commented-out code
- `print()` debugging statements
