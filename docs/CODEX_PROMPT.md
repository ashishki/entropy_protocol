# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-05
Phase: 1A archive-only baseline scaffold

This is the compact current-state handoff for new Codex sessions. Historical
handoff state remains available through git history and the implementation
journal.

## Current State

- Phase: `1A Archive-Only Baseline Planning and Instrumentation`
- Current task: `P1A-006 Archive Baseline Executable Scaffold`
- Test baseline: `205 passed, 20 skipped` without `DATABASE_URL`/live services
- Phase 0 archive-only research foundation: closed for archive-only work
- Live/streaming Phase 0 gate: not approved
- Full Phase 1 evaluation/trading: not approved
- Holdout: locked

## Read First

For a normal coding session, read only:

1. `docs/CODEX_PROMPT.md`
2. `docs/tasks.md` section `P1A-006`
3. `docs/audit/PHASE1A_FIX_CLOSURE_REVIEW.md`
4. Relevant code/tests for the touched module

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

## Key Hashes

- Freeze manifest hash:
  `54a820dbb07557294e821356168db4dbc6ba70fda4464a519442c4b20faea35e`
- Registration boundary hash:
  `2759fad18037361412f504384f22b411b4283b00e7764150f8c660f4375620df`
- Baseline spec hash:
  `a94c0441e0ff5b38bd0bafe83e445fe2041eb19e936dac19526ef417c39d3646`
- Validation registration hash:
  `7a23273630350704809be291da57c06e23e15537a16eaf3950d5e0da599816b4`

## P1A-006 Scope

Allowed:

- implement the minimum executable scaffold for the registered baseline spec;
- expose deterministic non-trading skill-family placeholders;
- enforce long-only/no-leverage constraints as validation logic;
- use P1A-003 read authorization for formation-only scaffold checks;
- prove validation reads require P1A-004 registration metadata;
- prove holdout reads remain denied.

Forbidden:

- executable alpha logic;
- portfolio allocation or backtest/evaluation;
- performance metrics;
- archive holdout read or unlock;
- Growth/RDL/RBE activation;
- live feeds, broker integration, or live capital;
- OOS/performance, validated-alpha, production, or capital-ready claims.

## Open Findings

- P0/P1 blockers for P1A-006: none.
- P2: F-C3-007 audit prompt metadata is stale. This does not block P1A-006,
  but should be fixed before the next full audit cycle.

## Verification Defaults

For P1A-006, run at minimum:

- focused pytest for new scaffold tests;
- focused ruff check/format for touched files;
- pyright for new modules;
- `git diff --check`;
- full `pytest` when feasible.

## Maintenance Rule

Keep this file compact. Append only current-state facts. Put detailed history in
`docs/IMPLEMENTATION_JOURNAL.md` or task-specific audit packets.
