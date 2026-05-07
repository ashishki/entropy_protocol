# PHASE_HANDOFF

Use this file at phase boundary, context rollover, limit recovery, or after a
manual restart.

## Current State

- Product: entropy-core
- Branch: codex/entropy-core-work
- Active task: T04 Registry Append-Only Audit
- Phase: 2 Governance Integrity
- Last validation: 2026-05-07 Phase 1 boundary: `288 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright 0 errors; `entropy --help` exited 0; `git diff --check` clean.
- Git status summary: local reset/orchestration files modified or untracked; no commit made in this segment.

## Completed In This Phase

- T01 Existing Project Baseline Skeleton verified against current files.
- T02 Product-Local CI Setup completed with reset CI contract tests.
- T03 Reset Baseline Smoke Tests completed with reset smoke coverage.
- Phase 1 boundary review completed with no findings.

## Remaining Work

- T04 Registry Append-Only Audit
- T05 Evidence Index and Journal Sync
- T06 No-Claim Report Boundary
- T07 Governance Approval Gate Audit

## Blockers Or Human Decisions

- None.

## Resume Instruction

Continue entropy-core from `RUNBOOK.md`, `AGENT_NOTES.md`,
`PHASE_HANDOFF.md`, `CODEX_LOOP.md`, `docs/CODEX_PROMPT.md`, and
`docs/tasks.md`.

Do not spawn nested Codex. Do not use `codex exec` for the normal loop. Continue
the orchestration loop from the next pending task in the current product tmux
window.
