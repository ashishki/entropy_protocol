# PHASE_HANDOFF

Use this file at phase boundary, context rollover, limit recovery, or after a
manual restart.

## Current State

- Product: entropy-core
- Branch: codex/entropy-core-work
- Active task: T08 Data and Leakage Gate Verification
- Phase: 3 Evaluation Safety
- Last validation: 2026-05-07 Phase 2 boundary: `302 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright 0 errors; `git diff --check` clean.
- Git status summary: Phase 2 local changes pending commit at handoff update time.

## Completed In This Phase

- T01 Existing Project Baseline Skeleton verified against current files.
- T02 Product-Local CI Setup completed with reset CI contract tests.
- T03 Reset Baseline Smoke Tests completed with reset smoke coverage.
- Phase 1 boundary review completed with no findings.
- T04 Registry Append-Only Audit completed with no findings.
- T05 Evidence Index and Journal Sync completed with no findings.
- T06 No-Claim Report Boundary completed with no findings.
- T07 Governance Approval Gate Audit completed with no findings.
- Phase 2 boundary review completed with no findings.

## Remaining Work

- T08 Data and Leakage Gate Verification
- T09 SimBroker and Cost Surface Regression
- T10 Attribution Stream Boundary Audit
- T11 Phase Gate Evidence Packet

## Blockers Or Human Decisions

- None.

## Resume Instruction

Continue entropy-core from `RUNBOOK.md`, `AGENT_NOTES.md`,
`PHASE_HANDOFF.md`, `CODEX_LOOP.md`, `docs/CODEX_PROMPT.md`, and
`docs/tasks.md`.

Do not spawn nested Codex. Do not use `codex exec` for the normal loop. Continue
the orchestration loop from the next pending task in the current product tmux
window.
