# CODEX_PROMPT.md

Version: 1.35
Date: 2026-05-03
Phase: 8

<!--
This file is the single source of truth for session state.
Every Codex agent reads this file before starting work.
Every Codex agent updates this file before committing at a phase boundary.
The orchestrator reads this file at the start of every session.

Never delete history from this file. Append; do not replace.
-->

---

## Current State

- **Phase:** 8
- **Baseline:** 117 passing tests with PostgreSQL 16 Docker container
- **Ruff:** configured (pyproject.toml)
- **Last CI run:** not yet configured (ci.yml created)
- **Last updated:** 2026-05-03 (v1.35 — T21 complete; T22 governance stop before implementation)
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

**T22 governance disposition before P1/P3 State Machine implementation**

Boundary note: Phase 5 review is archived at `docs/audit/PHASE5_REVIEW.md`; Phase 6 review is archived at `docs/audit/PHASE6_REVIEW.md`; Phase 7 review is archived at `docs/audit/PHASE7_REVIEW.md`. D-017 records the T21-specific formula-governance disposition in `docs/audit/T21_FORMULA_GOVERNANCE_DISPOSITION.md`. T15, T16, T17, T18, T19, T20, and T21 are complete.

Performance note: D-012's first real language-escalation profiling gate is now reached after T20 Walk-Forward Runner. No non-Python implementation, FFI, native extension, or runtime-service escalation is allowed without measured bottleneck evidence, ADR, CI/task updates, and explicit human approval. The second profiling gate remains after formula-bearing numerical tasks are implemented or explicitly waived.

D-014/D-016 note: `docs/audit/D010_CLOSURE_PACKET.md` has been applied and focused audit is recorded in `docs/audit/D010_FOCUSED_AUDIT_F1_F2_F4_F5.md`. Canonical docs are now `docs/core/PROTOCOL_SPEC.md` v1.8, `docs/core/CHARTER.md` v5.3, and `docs/core/GLOSSARY.md` v1.4.

D-015 note: F-30 and F-31 remain In Progress and must be closed only with real generated telemetry/K-report evidence later. They are future hard gates for RDL promotion, K-report generation, phase-exit evidence, and any code path that emits those artifacts; they do not block T15. No synthetic evidence may close them.

T21 scope guard: implement only the D-017 allowed subset. T21 may implement four-stream attribution, stream (d) exclusion from Net Sharpe, raw point-estimate Net Sharpe over supplied returns, drawdown worked examples, and `PerformanceMetrics` assembly with explicit stub reason code. Do not implement Sharpe CI, bootstrap CI, Harvey-Liu, N_eff/K3, IC/BR, P4, K-report, RDL promotion, phase-exit logic, or OOS performance-claim artifacts. If a `NetSharpe` object is constructed, its confidence interval must be caller/test supplied; T21 must not derive CI internally because T23 owns that statistical helper.

D-017 note: TASK-AF-022/F-22 is closed for current canonical implementation scope. Current source-of-truth docs define Net Sharpe as streams (a)+(b)+(c) and exclude stream (d). Historical audit artifacts that mention prior drift are retained as history, not current protocol definitions.

T21 note: attribution engine lives in `entropy/attribution/engine.py`; it computes per-observation streams, enforces Net Sharpe through `PnLStreams`, treats `FillLog.borrow_rate`/`funding_rate` as realized SimBroker cost components, preserves caller-supplied CI and Calmar values, and leaves `n_eff`/`harvey_liu_deflated_sharpe` as `None` with reason code `stub_pending_formula_verification`. T21 AC-3 was corrected from final `+5%` to `+8%` because `+5%` does not recover the prior compounded peak.

T22 governance stop: do not implement `entropy/governance/state_machine.py` yet. T22 encodes P1/P3 threshold and reset rules and remains covered by D-010 unless a T22-specific disposition/waiver is recorded or the relevant D-010 blockers are explicitly closed for T22.

Review remediation note: Phase 7 deep review found WF-P1-01, where omitted T19 detector callbacks could return PASS. This was remediated during review: missing detector callbacks now FAIL, and T20 tests verify both missing and failed leakage checks block OOS before `strategy.run_oos()`.

T20 note: walk-forward runner lives in `entropy/walkforward/runner.py`. It requires a `leakage_check` callback, calls strategy `run_is()` on IS only, blocks before `run_oos()` if the leakage check is missing or non-PASS, and persists complete `RunRecord` metadata with INSERT-only ORM behavior when a SQLAlchemy session is supplied.

T19 note: leakage checklist lives in `entropy/walkforward/leakage.py` and returns `LeakageReport` with four PASS/FAIL checks: normalization leakage, regime label look-ahead, universe selection bias, and within-window optimization. T19 tests use injected synthetic violations only to verify detectors; this does not close F-30/F-31 real-evidence gates.

T18 note: IS/OOS splitter lives in `entropy/walkforward/splitter.py`. It uses the documented temporary embargo assumption `embargo_bars = N consecutive bars immediately preceding the first OOS bar`. The purge/embargo formula blocker remains incomplete until canonical derivation is resolved; T18 did not close that formula debt.

T13 note: LocalFixtureAdapter writes validated local fixture data to deterministic Parquet under `ENTROPY_DATA_DIR/market/{symbol}/{timeframe}/{hash}.parquet` and records provenance in `market_datasets`.

T14 note: Data quality helpers live in `entropy/data/quality.py` and export timestamp, gap, OHLCV sanity, and aggregate report checks.

Before implementation, the orchestrator should hand Codex a narrow task digest inline:

- assignment and acceptance criteria
- file scope
- applicable contract rules only
- dependency facts from prior tasks
- immediate pipeline / flow if one matters

Only send Codex to full documents when the task is architecture-shaping, security-sensitive, ambiguous, or otherwise too risky to compress safely.

---

## Fix Queue

empty

Closed FIX-1 [P1] — ARCH-3: Phase Gate Inconsistency — resolved by D-010 resolution gate on 2026-05-03. Phase 2 engineering may proceed for non-formula tasks. D-015 narrowed T15's remaining blocker scope to focused audit verification of F-1, F-2, F-4, and F-5; D-016 passed that focused audit. F-30 and F-31 remain future real-evidence gates, not T15 blockers.

<!--
The Fix Queue contains items that must be addressed before the next phase gate,
but that were deferred from the current task. Format:

- FQ-01: [T-NN] Description of what must be fixed. Added: YYYY-MM-DD.
- FQ-02: [T-NN] Description. Added: YYYY-MM-DD.
-->

---

## Open Findings

### P1 Findings (block next phase gate)

none

### Closed P1 Findings

- P1-01: [CYCLE-2] ARCH-3 — Phase gate inconsistency closed 2026-05-03 by D-010 in docs/DECISION_LOG.md. Disposition: resolution gate (b). D-015 narrowed T15's remaining blocker scope to focused audit verification of F-1, F-2, F-4, and F-5; D-016 passed that audit. F-30 and F-31 remain future real-evidence gates.
- WF-P1-01: [PHASE-7-REVIEW] T19 omitted detector callbacks returned PASS, allowing T20 to pass a formal leakage gate without detector-backed checks. Closed 2026-05-03 by making omitted detectors FAIL and adding tests `test_full_leakage_checklist_requires_all_checks` and `test_runner_blocks_oos_when_leakage_check_fails`.

### P2 Findings (must resolve within 3 cycles)

none

### Closed P2 Findings

- P2-03: [CYCLE-2] CODE-2 — get_tracer() return annotation corrected from NoOpTracer to opentelemetry.trace.Tracer in entropy/tracing.py on 2026-05-03. Verified by `pyright --pythonpath .venv/bin/python entropy/`.
- P2-04: [CYCLE-2] CODE-4 — postgres_connection fixture now wraps yielded connections in a rollback-only transaction; verified by tests/integration/test_fixture_isolation.py on 2026-05-03.
- P2-02: [CYCLE-2] CODE-1 — tracing and metrics helper tests added in tests/unit/test_observability.py on 2026-05-03.
- P2-01: [CYCLE-2] ARCH-1 / CODE-3 — `entropy health` CLI command implemented in entropy/cli.py; verified by tests/unit/test_cli.py and manual CLI checks on 2026-05-03.
- P2-05: [CYCLE-2] ARCH-2 — docs/adr/ bootstrapped with docs/adr/README.md on 2026-05-03.
- P2-06: [CYCLE-2] ARCH-4 — docs/ARCHITECTURE.md Component Table updated with ERG, Research Firewall, RPM, Governor, and RDL rows on 2026-05-03.
- P2-07: [CYCLE-2] ARCH-5 — docs/core/ERA0_SPEC.md authority status clarified as proposed/non-canonical until human approval and merge on 2026-05-03.
- P2-08: [CYCLE-2] ARCH-6 — docs/README.md Documentation Map and Current Phase updated on 2026-05-03.

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
- T-GOV-1: Spec Owner Phase Gate Disposition — completed 2026-05-03. Baseline after: not run locally; pytest/ruff unavailable in PATH; grep verification passed.
- T04: Market Data Models — completed 2026-05-03. Baseline after: not run locally; pytest/ruff/pydantic unavailable in PATH; py_compile passed.
- T05: Registry and Run Models — completed 2026-05-03. Baseline after: 19 pass, 1 skip; ruff and pyright pass locally.
- T06: Performance Models — completed 2026-05-03. Baseline after: 23 pass, 1 skip; ruff and pyright pass locally.
- T07: Database Schema + Alembic Migrations — completed 2026-05-03. Baseline after: 29 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T-DB-1: postgres_connection Fixture Transaction Rollback — completed 2026-05-03. Baseline after: 30 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T-OBS-2: Observability Helper Unit Tests — completed 2026-05-03. Baseline after: 34 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T-OBS-1: entropy health CLI Command — completed 2026-05-03. Baseline after: 37 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T08: Deterministic Hashing — completed 2026-05-03 under D-011 narrow waiver. Baseline after: 42 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T09: Trial Registry Write Path — completed 2026-05-03. Baseline after: 47 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T10: Experiment Readiness Gate — completed 2026-05-03. Baseline after: 52 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T11: Trial Registry Read Path — completed 2026-05-03. Baseline after: 57 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T12: Data Ingestion Interface — completed 2026-05-03. Baseline after: 52 pass, 10 skip without DATABASE_URL; ruff and pyright pass locally.
- T13: Local Fixture Adapter + Parquet Store — completed 2026-05-03. Baseline after: 68 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T14: Data Quality Checks — completed 2026-05-03. Baseline after: 74 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T-GOV-2: Focused D-010 Audit Verification — completed 2026-05-03. Baseline after: not run; documentation/governance only.
- T15: SimBroker Cost Model — completed 2026-05-03. Baseline after: 67 pass, 13 skip without DATABASE_URL; ruff and pyright pass locally.
- T16: SimBroker Fill Engine — completed 2026-05-03. Baseline after: 87 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T17: SimBroker Calibration Interface — completed 2026-05-03. Baseline after: 91 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T18: IS/OOS Splitter — completed 2026-05-03. Baseline after: 97 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T19: Leakage Detection Checklist — completed 2026-05-03. Baseline after: 106 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- T20: Walk-Forward Runner — completed 2026-05-03. Baseline after: 110 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- Phase 6/7 Deep Audit Review — completed 2026-05-03. Baseline after remediation: 112 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally.
- D-017: T21 Formula-Governance Disposition — completed 2026-05-03. T21 may proceed under the narrow D-017 scope; baseline unchanged at 112 pass.
- T21: P&L Attribution Engine — completed 2026-05-03 under D-017 narrow scope. Baseline after: 117 pass with PostgreSQL 16 Docker container; ruff and pyright pass locally. T22 remains governance-blocked before implementation.

<!--
Append completed tasks here. Format:

- T01: Project Skeleton — completed YYYY-MM-DD. Baseline after: N tests.
- T02: CI Setup — completed YYYY-MM-DD. Baseline after: N tests.
-->

---

## Phase History

### Phase 2 — Core Domain Models
Closed: 2026-05-03
Baseline at gate: 23 pass, 1 skip
Tasks: T04, T05, T06
Review cycle: Phase 2 boundary review (see docs/audit/PHASE2_REVIEW.md)
P1s resolved: 0
P2s open: 7
Gate approved by: local orchestrator review; human approval still required for formal project governance gates

### Phase 3 — Database Schema + Hashing
Closed: 2026-05-03
Baseline at gate: 42 pass
Tasks: T07, T08
Review cycle: Phase 3 boundary review (see docs/audit/PHASE3_REVIEW.md)
P1s resolved: 0
P2s open: 0
Gate approved by: local orchestrator review under D-011 for T08; human approval still required for formal project governance gates

### Phase 4 — Trial Registry
Closed: 2026-05-03
Baseline at gate: 57 pass
Tasks: T09, T10, T11
Review cycle: Phase 4 boundary review (see docs/audit/PHASE4_REVIEW.md)
P1s resolved: 0
P2s open: 0
Gate approved by: local orchestrator review; human approval still required for formal project governance gates

### Phase 5 — Data Pipeline
Closed: 2026-05-03
Baseline at gate: 74 pass
Tasks: T12, T13, T14
Review cycle: Phase 5 boundary review (see docs/audit/PHASE5_REVIEW.md)
P1s resolved: 0
P2s open: 0
Gate approved by: local orchestrator review; T15 was blocked by D-010 until D-016 focused audit passed on 2026-05-03

### T15 Waiver Disposition
Date: 2026-05-03
Decision: D-013 denies a T15-specific waiver.
Result: Superseded by D-015 and D-016 for T15 entry. T15 is now unblocked for cost-model implementation only; F-30/F-31 remain future real-evidence gates.

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
