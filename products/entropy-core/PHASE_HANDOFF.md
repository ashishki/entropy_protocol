# PHASE_HANDOFF

Use this file at phase boundary, context rollover, limit recovery, or after a
manual restart.

## Current State

- Product: entropy-core
- Branch: codex/entropy-core-work
- Active task: T41 Holdout Approval Evidence Intake Contract
- Phase: 10 Holdout Approval Decision Packet
- Last validation: 2026-05-09 T40: `423 passed, 20 skipped`; ruff check clean; ruff format clean; pyright 0 errors; `git diff --check` clean.
- Git status summary: T40 holdout approval request packet changes pending commit at handoff update time.

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
- T20 Second Research Candidate Registration Packet completed with no findings.
- T21 Second Archive Dataset Manifest and Hash Binding completed with no findings.
- T22 Second Archive Evaluation Harness Wiring completed with no findings.
- T23 Second Research Evidence Packet completed with no findings.
- T24 Archive Evidence Expansion Review completed with no findings.
- T25 Roadmap Governance Contract completed with no findings.
- T26 Archive Packet Replay Contract completed with no findings.
- T27 Evidence Hash Reproducibility Matrix completed with no findings.
- T28 No-Claim Surface Regression Sweep completed with no findings.
- T29 Archive Reproducibility Hardening Review completed with no findings.
- T30 Archive Evidence Sufficiency Gap Matrix completed with no findings.
- T31 Phase-Gate Readiness Packet Scaffold completed with no findings.
- T32 Approval Boundary Checklist completed with no findings.
- T33 Readiness No-Holdout Dry Run completed with no findings.
- T34 Phase-Gate Readiness Review completed with no findings.
- T35 Holdout Access Protocol Deny-By-Default Contract completed with no findings.
- T36 Holdout Approval Event Schema Contract completed with no findings.
- T37 Holdout Access Audit Logging Contract completed with no findings.
- T38 Holdout Leakage Guard Protocol Fixture completed with no findings.
- T39 Holdout Access Protocol Review completed with no findings.
- T40 Holdout Approval Request Packet Scaffold completed with no findings.

## Remaining Work

- T41 Holdout Approval Evidence Intake Contract is active.
- T42 Holdout Approval Absence Denial Packet is pending.
- T43 Holdout Non-Approval Source Regression is pending.
- T44 Holdout Decision No-Read Dry Run is pending.
- T45 Holdout Approval Decision Review is pending.
- After T45, run deep review, fix findings, validate, evaluate the roadmap, rewrite future phases/tasks if useful, open the next logical active phase, and continue automatically.

## Blockers Or Human Decisions

- Human decision after T14 recorded: open the first research evidence packet block.
- Human decision required after T19 was satisfied by opening Phase 6 archive-only evidence expansion.
- Human decision after T19 recorded: open archive-only evidence expansion for more proof. No holdout, live feed, broker/exchange, production, capital-ready, phase-gate, or OOS/performance claim path is approved.
- Human decision required after T24 was satisfied on 2026-05-08 by opening Phase 7 only.
- Human decision after T24 recorded on 2026-05-08: record roadmap phases 7 through 13, open Phase 7, and allow autonomous phase rollover after deep review, fixes, validation, and roadmap evaluation.
- Phase 8 roadmap evaluation opened Phase 9 as protocol-only holdout access design. No holdout read, holdout unlock, phase-gate approval, or OOS/performance claim is approved.
- T35 created a denied-by-default local protocol scaffold. Phase 9 is protocol-only with holdout read/unlock still blocked, and no approval event currently exists.
- T36 defined the approval event schema and invalid fixture classes without creating any approval event.
- T37 defined audit logging requirements for denied and future approved attempts without exposing raw holdout paths or opening holdout data.
- T38 defined leakage guard inputs and fail-closed fixtures without executing holdout access.
- T39 closed Phase 9 and rewrote Phase 10 into no-read approval decision work. No approval event currently exists; holdout read/unlock remain blocked.
- T40 created a no-read approval request packet scaffold. No approval event currently exists; holdout read/unlock remain blocked.
- Real external side effects, holdout reads, holdout unlocks, live capital actions, live broker/exchange execution, and credentialed production deployment remain blocked; implement local dry-run/sandbox/protocol work instead unless a future local contract explicitly permits otherwise.

## Resume Instruction

Continue entropy-core from `RUNBOOK.md`, `AGENT_NOTES.md`,
`PHASE_HANDOFF.md`, `CODEX_LOOP.md`, `docs/CODEX_PROMPT.md`, and
`docs/tasks.md`.

Do not spawn nested Codex. Do not use `codex exec` for the normal loop. Continue
the orchestration loop from the next pending task in the current product tmux
window.
