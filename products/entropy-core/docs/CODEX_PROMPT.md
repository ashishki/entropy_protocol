# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-08
Phase: 7

Reset state for Entropy Core after archiving the old active workflow. Historical files are available under `docs/legacy/old-workflow/2026-05-07/` but are not read by default.

---

## Current Phase

- Phase: 7
- Name: Archive Reproducibility Hardening
- Business goal: prove existing archive-only evidence packets can be replayed, hash-checked, and governed by a dynamic roadmap evaluation rule.
- Phase gate: replay, reproducibility matrix, no-claim sweep, and review prove deterministic archive evidence without opening holdout, live, broker/exchange, production, capital-ready, phase-gate, or OOS/performance claim paths.

## Current State

- Phase: 7
- Baseline: 387 passing tests, 20 skipped (T28 local verification on 2026-05-08)
- Ruff: clean on T28 local verification 2026-05-08
- Pyright: clean on T28 local verification 2026-05-08
- Last CI: product-local workflow configured; remote CI not yet observed after reset
- Holdout: locked
- Live capital: not approved
- Broker/exchange integration: not approved
- OOS/performance claims: not approved
- Last updated: 2026-05-08

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Legacy summary: `docs/legacy/CORE_LEGACY_SUMMARY.md`
- Old active workflow archive: `docs/legacy/old-workflow/2026-05-07/`
- Protocol docs: `docs/core/`
- Governance docs: `docs/governance/`

## Next Task

T29 Archive Reproducibility Hardening Review.

Human decision after T24 opened Phase 7 Archive Reproducibility Hardening and autonomous roadmap rollover. Active scope is T25 through T29; T25 through T28 are complete. After T29, run deep review, fix findings, validate, evaluate the roadmap, rewrite future phases if useful, open the next logical active phase, and continue automatically.

Archive Evidence Expansion block complete through T24. Roadmap phases 8 through 13 are planned direction and may be rewritten by roadmap evaluation. Do not execute real external side effects, live capital actions, live broker/exchange execution, or credentialed production deployment; replace them with local dry-run/sandbox protocol work unless a future local contract explicitly permits otherwise.

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
- 2026-05-07: T15 First Research Candidate Registration Packet completed.
  - Acceptance tests: `tests/integration/test_first_research_packet.py` passed (`11 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `339 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T16 Archive Dataset Manifest and Hash Binding completed.
  - Acceptance tests: `tests/integration/test_first_research_packet.py` passed (`14 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `342 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T17 Archive Evaluation Harness Wiring completed.
  - Acceptance tests: `tests/integration/test_first_research_packet.py` passed (`17 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `345 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T18 First Research Evidence Packet completed.
  - Acceptance tests: `tests/integration/test_first_research_packet.py` passed (`20 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `348 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T19 First Research Packet Review completed.
  - Acceptance tests: `tests/reset/test_first_research_packet_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `351 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T20 Second Research Candidate Registration Packet completed.
  - Acceptance tests: `tests/integration/test_second_research_packet.py` passed (`11 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `362 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T21 Second Archive Dataset Manifest and Hash Binding completed.
  - Acceptance tests: `tests/integration/test_second_research_packet.py` passed (`14 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `365 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T22 Second Archive Evaluation Harness Wiring completed.
  - Acceptance tests: `tests/integration/test_second_research_packet.py` passed (`17 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `368 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T23 Second Research Evidence Packet completed.
  - Acceptance tests: `tests/integration/test_second_research_packet.py` passed (`20 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `371 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T24 Archive Evidence Expansion Review completed.
  - Acceptance tests: `tests/reset/test_archive_evidence_expansion_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `374 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T25 Roadmap Governance Contract completed.
  - Acceptance tests: `tests/reset/test_roadmap_governance.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `377 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T26 Archive Packet Replay Contract completed.
  - Acceptance tests: `tests/integration/test_archive_replay.py` passed (`4 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `381 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T27 Evidence Hash Reproducibility Matrix completed.
  - Acceptance tests: `tests/reset/test_reproducibility_matrix.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `384 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T28 No-Claim Surface Regression Sweep completed.
  - Acceptance tests: `tests/reset/test_no_claim_roadmap_sweep.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `387 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.

## Phase History

- 2026-05-07: Phase 1 Reset Foundation completed. Review artifact: `docs/audit/PHASE1_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Phase 2 Governance Integrity completed. Review artifact: `docs/audit/PHASE2_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Phase 3 Evaluation Safety completed. Review artifact: `docs/audit/PHASE3_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Reset implementation block completed. Review artifact: `docs/audit/RESET_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: First Research Evidence Packet block opened by human decision after T14. Scope: T15-T19.
- 2026-05-07: First Research Evidence Packet block completed. Review artifact: `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: First Research Evidence Packet block complete through T19. Human decision required after T19 was satisfied by opening archive-only evidence expansion.
- 2026-05-07: T19 boundary state preserved: holdout, live feeds, broker/exchange, production, capital-ready, and OOS/performance remain unapproved.
- 2026-05-07: Archive Evidence Expansion block opened by human decision after T19. Scope: T20-T24.
- 2026-05-07: Archive Evidence Expansion block complete through T24. Review artifact: `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-08: Human decision required after T24 was satisfied by opening Phase 7 only.
- 2026-05-08: Historical T24 boundary preserved: holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, and OOS/performance remain unapproved at the T24 boundary.
- 2026-05-08: Forward roadmap recorded for phases 7 through 13 with autonomous roadmap evaluation and rollover required after every active phase.
- 2026-05-08: Phase 7 Archive Reproducibility Hardening opened by human decision after T24. Scope: T25-T29. Phases 8 through 13 remain planned only.
- 2026-05-08: T25 Roadmap Governance Contract completed. Next task: T26 Archive Packet Replay Contract.
- 2026-05-08: T26 Archive Packet Replay Contract completed. Next task: T27 Evidence Hash Reproducibility Matrix.
- 2026-05-08: T27 Evidence Hash Reproducibility Matrix completed. Next task: T28 No-Claim Surface Regression Sweep.
- 2026-05-08: T28 No-Claim Surface Regression Sweep completed. Next task: T29 Archive Reproducibility Hardening Review.
- 2026-05-08: Phase boundaries changed from stop points to autonomous rollover points: deep review, fix findings, validate, evaluate roadmap, rewrite future phases, open the next logical active phase, and continue.

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

- Profile: No-Claim Surface Regression Sweep
- Task: T28 No-Claim Surface Regression Sweep
- Date: 2026-05-08
- Eval Source: `tests/reset/test_no_claim_roadmap_sweep.py`
- Metric(s): active-doc restricted surface scan, future-phase planned status, prompt/handoff boundary preservation
- Score: `3 passed`; current baseline `387 passed, 20 skipped`
- Baseline: T27 evidence hash reproducibility matrix `384 passed, 20 skipped`
- Delta: +3 passing tests
- Regression: none known

### Open Evaluation Issues

none

### Human Decision

Human approval after T24 opened Phase 7 Archive Reproducibility Hardening and recorded a dynamic roadmap for phases 7 through 13. Phase boundaries now roll over automatically after deep review, fixes, validation, and roadmap evaluation. Real external side effects, live capital actions, live broker/exchange execution, and credentialed production deployment remain blocked.

### Human Decision Point

Current active task is T29 Archive Reproducibility Hardening Review. Archive Evidence Expansion block is complete through T24, and Phase 7 is complete through T28. Roadmap phases 8 through 13 are planned direction and may be promoted or rewritten automatically by roadmap evaluation. Real external side effects, live capital actions, live broker/exchange execution, and credentialed production deployment remain blocked.

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
