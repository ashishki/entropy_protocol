# PHASE_HANDOFF

Use this file at phase boundary, context rollover, limit recovery, or after a
manual restart.

## Current State

- Product: entropy-core
- Branch: codex/entropy-core-work
- Active task: Human decision required after T19
- Phase: 5 First Research Evidence Packet
- Last validation: 2026-05-07 T19: `351 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright 0 errors; `git diff --check` clean.
- Git status summary: T15-T19 first research packet local changes pending commit at handoff update time.

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
- T08 Data and Leakage Gate Verification completed with no findings.
- T09 SimBroker and Cost Surface Regression completed with no findings.
- T10 Attribution Stream Boundary Audit completed with no findings.
- T11 Phase-Gate Evidence Packet completed with no findings.
- Phase 3 boundary review completed with no findings.
- T12 Trader Risk Audit Bridge Contracts completed with no findings.
- T13 Hypothesis Backtest Bridge Design completed with no findings.
- T14 Reset Strategy Closure Review completed with no findings.
- T15 First Research Candidate Registration Packet completed with no findings.
- T16 Archive Dataset Manifest and Hash Binding completed with no findings.
- T17 Archive Evaluation Harness Wiring completed with no findings.
- T18 First Research Evidence Packet completed with no findings.
- T19 First Research Packet Review completed with no findings.

## Remaining Work

- Human decision required before any new research block, phase-gate discussion, holdout access, live-feed path, broker/exchange path, production/capital-ready path, or OOS/performance claim path.

## Blockers Or Human Decisions

- Human decision after T14 recorded: open the first research evidence packet block.
- Human decision required after T19: first packet block is complete; no next block is open.

## Resume Instruction

Continue entropy-core from `RUNBOOK.md`, `AGENT_NOTES.md`,
`PHASE_HANDOFF.md`, `CODEX_LOOP.md`, `docs/CODEX_PROMPT.md`, and
`docs/tasks.md`.

Do not spawn nested Codex. Do not use `codex exec` for the normal loop. Continue
the orchestration loop from the next pending task in the current product tmux
window.
