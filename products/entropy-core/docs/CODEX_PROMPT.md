# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-07
Phase: 5

Reset state for Entropy Core after archiving the old active workflow. Historical files are available under `docs/legacy/old-workflow/2026-05-07/` but are not read by default.

---

## Current Phase

- Phase: 5
- Name: First Research Evidence Packet
- Business goal: produce one registered, hash-bound, archive-only, leakage-checked research evidence packet from a narrow baseline hypothesis.
- Phase gate: packet and review prove reproducible evidence without OOS/performance, holdout, live, production, or capital-ready claims.

## Current State

- Phase: 5
- Baseline: 328 passing tests, 20 skipped (T14 local verification on 2026-05-07)
- Ruff: clean on Phase 1 boundary verification 2026-05-07
- Pyright: clean on Phase 1 boundary verification 2026-05-07
- Last CI: product-local workflow configured; remote CI not yet observed after reset
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

T15: First Research Candidate Registration Packet

Human decision recorded: Reset implementation awaits human decision after T14; this instruction opens the next research packet block.

## Fix Queue

empty

## Open Findings

none after reset. Legacy D-K findings were closed in the prior workflow, but old findings are not active unless re-opened by a reset task or review.

## Completed Tasks

- 2026-05-07: T01 Existing Project Baseline Skeleton completed.
  - Acceptance tests: `tests/reset/test_reset_tooling.py` and `tests/reset/test_reset_skeleton.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `280 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean.
- 2026-05-07: T02 Product-Local CI Setup completed.
  - Acceptance tests: `tests/reset/test_ci_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `283 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T03 Reset Baseline Smoke Tests completed.
  - Acceptance tests: `tests/reset/test_reset_smoke.py` passed (`5 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `288 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean.
- 2026-05-07: T04 Registry Append-Only Audit completed.
  - Acceptance tests: `tests/unit/test_registry_append_only_reset.py` and `tests/integration/test_registry_append_only_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `291 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T05 Evidence Index and Journal Sync completed.
  - Acceptance tests: `tests/reset/test_evidence_index_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `294 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T06 No-Claim Report Boundary completed.
  - Acceptance tests: `tests/unit/test_no_claim_report_boundary.py` passed (`5 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `299 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T07 Governance Approval Gate Audit completed.
  - Acceptance tests: `tests/unit/test_governance_gate_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `302 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T08 Data and Leakage Gate Verification completed.
  - Acceptance tests: `tests/unit/test_data_leakage_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `305 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T09 SimBroker and Cost Surface Regression completed.
  - Acceptance tests: `tests/unit/test_simbroker_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `308 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T10 Attribution Stream Boundary Audit completed.
  - Acceptance tests: `tests/unit/test_attribution_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `311 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T11 Phase-Gate Evidence Packet completed.
  - Acceptance tests: `tests/integration/test_phase_gate_packet_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `314 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T12 Trader Risk Audit Bridge Contracts completed.
  - Acceptance tests: `tests/integration/test_trader_risk_bridge_contract.py` passed (`8 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `322 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T13 Hypothesis Backtest Bridge Design completed.
  - Acceptance tests: `tests/integration/test_hypothesis_bridge_design.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `325 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T14 Reset Strategy Closure Review completed.
  - Acceptance tests: `tests/reset/test_reset_closure.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `328 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.

## Phase History

- 2026-05-07: Phase 1 Reset Foundation completed. Review artifact: `docs/audit/PHASE1_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Phase 2 Governance Integrity completed. Review artifact: `docs/audit/PHASE2_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Phase 3 Evaluation Safety completed. Review artifact: `docs/audit/PHASE3_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Reset implementation block completed. Review artifact: `docs/audit/RESET_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: First Research Evidence Packet block opened by human decision after T14. Scope: T15-T19.

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

- Profile: First Research Evidence Packet
- Task: T15 First Research Candidate Registration Packet
- Date: 2026-05-07
- Eval Source: pending
- Metric(s): pending first research candidate contract tests
- Score: pending; current baseline `328 passed, 20 skipped`
- Baseline: reset closure `328 passed, 20 skipped`
- Delta: pending
- Regression: none known

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

Phase 1 validation ran in the reset loop and wrote `docs/audit/PHASE1_AUDIT.md`.
Result: PASS, 100 checks passed, 0 blockers, 0 warnings.
