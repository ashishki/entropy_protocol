# CODEX_PROMPT.md

Version: 2.8
Date: 2026-05-05
Phase: Phase 1B code closure review

This is the compact current-state handoff for new Codex sessions. Historical
handoff state remains available through git history and the implementation
journal.

## Current State

- Phase: `Phase 1B Long-Only Baseline Readiness Code Block`
- Current task: `P1B-HUMAN-001 Phase 1B Code Closure Review`
- Test baseline: `232 passed, 20 skipped` without `DATABASE_URL`/live services
- Phase 0 archive-only research foundation: closed for archive-only work
- Live/streaming Phase 0 gate: not approved
- Full Phase 1 evaluation/trading: not approved
- Holdout: locked

## Read First

For a normal coding session, read only:

1. `docs/CODEX_PROMPT.md`
2. `docs/audit/PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md`
3. `docs/audit/POST_PHASE1A_STRATEGY_REVIEW.md`
4. `docs/audit/POST_PHASE1A_NEXT_STAGE_PLAN.md`
5. `docs/audit/PHASE1A_AUDIT_PROMPT_REFRESH_PACKET.md`
6. `docs/tasks.md` current task section

Read broader protocol docs only if changing architecture, phase gates,
formula/statistical logic, Growth/RDL/RBE, live data, or claim/report semantics.

## Active Decisions

- D-027: current evidence mode is archive-only; live/streaming claims are not
  authorized.
- D-028: Phase 1A archive-only baseline planning selected.
- D-029: P1A entry contract approved.
- D-030: archive dataset freeze approved.
- D-031: archive split registration/read gate approved.
- D-032: non-executable baseline specification registration approved.
- D-033: fix chain closed for narrow executable scaffold only.
- D-034: executable scaffold deferred until workload profile and benchmark
  contract are explicit.
- D-035: workload profile and benchmark contract approved; P1A-008 may proceed
  as scaffold-only under that boundary.
- D-036: executable scaffold approved; P1A-009 may run mechanics-only scaffold
  performance probe.
- D-037: scaffold performance probe approved; P1A-010 may review scaffold/probe
  closure only.
- D-038: scaffold/probe chain closed; next step is human/strategic post-Phase-1A
  decision.
- D-039: post-Phase-1A strategy selected audit-readiness work first: refresh
  audit prompt metadata, then run the deep protocol review, then consolidate the
  next task graph.
- D-040: audit prompt metadata refresh closed F-C3-007; P1A-012 may run the
  post-Phase-1A deep protocol review.
- D-041: post-Phase-1A deep review found no P0/P1 drift in the scaffold/probe
  boundary and opened P2 F-C4-001 for current-state sync.
- D-042: current-state sync closed F-C4-001; next step requires Spec Owner
  approval of the next block.
- D-043: Spec Owner selected Phase 1B Long-Only Baseline Readiness Planning as
  the next block. Phase 1B is part of the Phase 1 workstream but is not full
  Phase 1 evaluation/trading.
- D-044: Phase taxonomy and gate map approved; P1B-002 should expand the
  operations plan into an ordered readiness task graph.
- D-045: long-only baseline implementation surface approved.
- D-046: Phase 1B readiness code block completed as implemented: formation-only
  input adapter, feature contract, schema-only skill stubs, and mechanics-only
  benchmark.

Decision log: `docs/DECISION_LOG.md`.

## Current Artifacts

- Entry contract:
  `docs/audit/PHASE1A_ARCHIVE_ENTRY_CONTRACT.md`
- Freeze manifest:
  `artifacts/evidence/phase1a_archive_freeze/freeze_001/PHASE1A_ARCHIVE_FREEZE_MANIFEST.json`
- Registration boundary manifest:
  `artifacts/evidence/phase1a_registration_boundary/boundary_001/PHASE1A_ARCHIVE_REGISTRATION_BOUNDARY_MANIFEST.json`
- Baseline registration manifest:
  `artifacts/evidence/phase1a_baseline_registration/registration_001/PHASE1A_BASELINE_SPEC_REGISTRATION_MANIFEST.json`
- Fix closure review:
  `docs/audit/PHASE1A_FIX_CLOSURE_REVIEW.md`
- Development/runtime strategy:
  `docs/audit/PHASE1A_DEVELOPMENT_STRATEGY.md`
- Workload/benchmark contract:
  `docs/audit/PHASE1A_WORKLOAD_BENCHMARK_CONTRACT.md`
- Baseline scaffold packet:
  `docs/audit/PHASE1A_BASELINE_SCAFFOLD_PACKET.md`
- Scaffold performance probe packet:
  `docs/audit/PHASE1A_SCAFFOLD_PERFORMANCE_PROBE_PACKET.md`
- Scaffold closure review:
  `docs/audit/PHASE1A_SCAFFOLD_CLOSURE_REVIEW.md`
- Post-Phase-1A strategy review:
  `docs/audit/POST_PHASE1A_STRATEGY_REVIEW.md`
- Post-Phase-1A next stage plan:
  `docs/audit/POST_PHASE1A_NEXT_STAGE_PLAN.md`
- Audit prompt refresh packet:
  `docs/audit/PHASE1A_AUDIT_PROMPT_REFRESH_PACKET.md`
- Operations plan:
  `docs/audit/POST_PHASE1A_OPERATIONS_PLAN.md`
- Phase 1B readiness code:
  `entropy/baseline/features.py`, `entropy/baseline/formation.py`,
  `entropy/baseline/skills.py`

## Key Hashes

- Freeze manifest hash:
  `54a820dbb07557294e821356168db4dbc6ba70fda4464a519442c4b20faea35e`
- Registration boundary hash:
  `2759fad18037361412f504384f22b411b4283b00e7764150f8c660f4375620df`
- Baseline spec hash:
  `a94c0441e0ff5b38bd0bafe83e445fe2041eb19e936dac19526ef417c39d3646`
- Validation registration hash:
  `7a23273630350704809be291da57c06e23e15537a16eaf3950d5e0da599816b4`

## Current Scope

Allowed:

- perform Phase 1B code closure review and decide the next bounded block;
- keep forbidden claim boundaries intact;
- update docs only for real status/evidence changes.

Forbidden:

- executable alpha logic;
- portfolio allocation or backtest/evaluation;
- strategy performance metrics;
- archive holdout read or unlock;
- Growth/RDL/RBE activation;
- live feeds, broker integration, or live capital;
- Rust, Go, C/C++, FFI, native extensions, or second runtime services without
  benchmark evidence, ADR, architecture/task/CI updates, and explicit human
  approval;
- OOS/performance, validated-alpha, production, or capital-ready claims.

## Open Findings

- P0/P1 blockers for P1B-HUMAN-001: none known.
- F-C3-007 is closed for the active audit prompt chain by P1A-011.
- F-C4-001 is closed by P1A-013 current-state sync.

## Verification Defaults

For P1B-HUMAN-001, run at minimum:

- review `entropy/baseline/long_only.py`, `features.py`, `formation.py`, and
  `skills.py`;
- run targeted Phase 1B tests;
- run ruff/pyright on touched Python files if code changes;
- `git diff --check`;

## Maintenance Rule

Keep this file compact. Append only current-state facts. Put detailed history in
`docs/IMPLEMENTATION_JOURNAL.md` or task-specific audit packets.
