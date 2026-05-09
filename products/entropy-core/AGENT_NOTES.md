# Agent Notes

## 2026-05-07 Workflow Recovery

The entropy-core workspace was reset close to repository state after a Codex
failure. Product-specific loop guidance has been restored locally.

Current operating model:

- The product agent is already running in tmux window `entropy-core`.
- Do not call `codex` or `codex exec` from inside the normal development loop.
- Do not spawn nested Codex or another AI coding process.
- Follow `CODEX_LOOP.md` as the local override for older Claude Code and
  `codex exec` references in legacy workflow docs.
- The only unplanned stop condition is account/model limits until reset.
- At phase boundary or context rollover, update `PHASE_HANDOFF.md`, validation
  results, and git status before stopping/restarting.

Known local status after recovery:

- Branch: `codex/entropy-core-work`
- Remaining untracked file observed before this note: `docs/audit/PHASE1_AUDIT.md`
- Other product workspaces are intentionally inaccessible and must not be used
  as context.

## 2026-05-07 Phase 1 Boundary

Phase 1 Reset Foundation is complete in the reset task graph.

- Completed tasks: T01, T02, T03.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `288 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright 0 errors; `entropy --help` exited 0; `git diff --check` clean.
- Review artifact: `docs/audit/PHASE1_REVIEW.md`.
- Audit index updated: `docs/audit/AUDIT_INDEX.md`.
- Next task: T04 Registry Append-Only Audit.
- No open findings or blockers.

## 2026-05-07 Phase 2 Boundary

Phase 2 Governance Integrity is complete in the reset task graph.

- Completed tasks: T04, T05, T06, T07.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `302 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright 0 errors; `git diff --check` clean.
- Review artifact: `docs/audit/PHASE2_REVIEW.md`.
- Audit index updated: `docs/audit/AUDIT_INDEX.md`.
- Next task: T08 Data and Leakage Gate Verification.
- No open findings or blockers.

## 2026-05-07 Phase 3 Boundary

Phase 3 Evaluation Safety is complete in the reset task graph.

- Completed tasks: T08, T09, T10, T11.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `314 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright 0 errors; `git diff --check` clean.
- Review artifact: `docs/audit/PHASE3_REVIEW.md`.
- Audit index updated: `docs/audit/AUDIT_INDEX.md`.
- Next task: T12 Trader Risk Audit Bridge Contracts.
- No open findings or blockers.

## 2026-05-07 Reset Closure

The reset implementation block is complete through T14.

- Completed tasks: T01 through T14.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `328 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright 0 errors; `git diff --check` clean.
- Review artifact: `docs/audit/RESET_REVIEW.md`.
- Audit index updated: `docs/audit/AUDIT_INDEX.md`.
- Next state: reset implementation awaits human decision after T14.
- No open findings or blockers.

## 2026-05-07 First Research Packet Block

Human decision after T14 opened a new research-result block.

- Active phase: Phase 5 First Research Evidence Packet.
- Planned tasks: T15 through T19.
- Target result: one registered, hash-bound, archive-only, leakage-checked research evidence packet.
- Latest validation remains reset closure baseline: `.venv/bin/python -m pytest -q tests/` -> `328 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright 0 errors; `git diff --check` clean.
- Next task: T15 First Research Candidate Registration Packet.
- Boundaries remain unchanged: no holdout, live feed, broker/exchange, production, capital-ready, or OOS/performance approval.

## 2026-05-07 First Packet Evidence Progress

Phase 5 is complete through T19.

- Completed tasks: T15 First Research Candidate Registration Packet, T16 Archive Dataset Manifest and Hash Binding, T17 Archive Evaluation Harness Wiring, T18 First Research Evidence Packet, T19 First Research Packet Review.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `351 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index rows added for T15, T16, T17, and T18; review artifact `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md` added for T19.
- Next state: human decision required after T19.
- Boundaries remain unchanged: first packet block is archive-only and complete; holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, and OOS/performance remain unapproved.

## 2026-05-07 Archive Evidence Expansion Opened

Human decision after T19 opened a new archive-only evidence expansion block.

- Active phase: Phase 6 Archive Evidence Expansion.
- Planned tasks: T20 through T24.
- Target result: additional hash-bound, archive-only, leakage-checked research evidence from a second distinct narrow baseline hypothesis.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `374 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- Completed tasks: T20 Second Research Candidate Registration Packet, T21 Second Archive Dataset Manifest and Hash Binding, T22 Second Archive Evaluation Harness Wiring, T23 Second Research Evidence Packet, T24 Archive Evidence Expansion Review.
- Next state: human decision required after T24.
- Boundaries remain unchanged: no holdout, live feed, broker/exchange, production, capital-ready, phase-gate, or OOS/performance approval.

## 2026-05-08 Roadmap Governance and Phase 7 Opened

Human decision after T24 recorded a forward roadmap and opened only the first active roadmap phase.

- Active phase: Phase 7 Archive Reproducibility Hardening.
- Completed task: T25 Roadmap Governance Contract.
- Active task: T26 Archive Packet Replay Contract.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `377 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Planned roadmap phases: Phase 7 Archive Reproducibility Hardening; Phase 8 Phase-Gate Readiness Review; Phase 9 Holdout Access Protocol; Phase 10 Approved Holdout Evaluation Packet; Phase 11 Live-Feed Dry Run Readiness; Phase 12 Broker Sandbox and Execution Risk Audit; Phase 13 Production and Capital Gate.
- Roadmap governance: after every active phase closes, run deep review, fix findings, validate, evaluate the roadmap, rewrite future phases/tasks if useful, open the next logical active phase, and continue automatically. Future phases may change based on completed evidence.
- Boundaries: real external side effects, live capital actions, live broker/exchange execution, and credentialed production deployment remain blocked. Use local dry-run/sandbox/protocol work instead unless a future local contract explicitly permits otherwise.

## 2026-05-08 T26 Archive Replay Contract

Phase 7 is complete through T26.

- Completed task: T26 Archive Packet Replay Contract.
- Active task: T27 Evidence Hash Reproducibility Matrix.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `381 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T26 replay proof.
- Light review result: no findings.
- Boundaries remain unchanged: no holdout, live feed, broker/exchange, production, capital-ready, phase-gate, or OOS/performance approval.

## 2026-05-08 T27 Reproducibility Matrix

Phase 7 is complete through T27.

- Completed task: T27 Evidence Hash Reproducibility Matrix.
- Active task: T28 No-Claim Surface Regression Sweep.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `384 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T27 matrix proof.
- Light review result: no findings.
- Boundaries remain unchanged: the matrix is hash bookkeeping only and creates no holdout, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate approval.

## 2026-05-08 T28 No-Claim Sweep

Phase 7 is complete through T28.

- Completed task: T28 No-Claim Surface Regression Sweep.
- Active task: T29 Archive Reproducibility Hardening Review.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `387 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T28 no-claim sweep proof.
- Light review result: no findings.
- Boundaries remain unchanged: active docs and replayed packet surfaces expose no restricted approval flags, and roadmap phases 8 through 13 remain planned only.

## 2026-05-08 Phase 7 Boundary and Phase 8 Opened

Phase 7 Archive Reproducibility Hardening is complete through T29.

- Review artifact: `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`.
- Audit index row added for `ARCHIVE-REPRODUCIBILITY-HARDENING`.
- Active phase: Phase 8 Phase-Gate Readiness Review.
- Active task: T30 Archive Evidence Sufficiency Gap Matrix.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `390 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Deep review result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- Roadmap evaluation kept planned Phase 8, limited to readiness and gap analysis.
- Boundaries remain unchanged: no holdout read, live feed, broker/exchange, production, capital-ready, phase-gate, or OOS/performance approval.

## 2026-05-08 T30 Readiness Gap Matrix

Phase 8 is complete through T30.

- Completed task: T30 Archive Evidence Sufficiency Gap Matrix.
- Active task: T31 Phase-Gate Readiness Packet Scaffold.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `393 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T30 gap matrix proof.
- Light review result: no findings.
- Boundaries remain unchanged: T30 is readiness analysis only and does not approve holdout, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate surfaces.

## 2026-05-09 T31 Readiness Packet Scaffold

Phase 8 is complete through T31.

- Completed task: T31 Phase-Gate Readiness Packet Scaffold.
- Active task: T32 Approval Boundary Checklist.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `396 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T31 readiness packet proof.
- Light review result: no findings.
- Boundaries remain unchanged: readiness packet is scaffold-only and grants no holdout, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate approval.

## 2026-05-09 T32 Approval Boundary Checklist

Phase 8 is complete through T32.

- Completed task: T32 Approval Boundary Checklist.
- Active task: T33 Readiness No-Holdout Dry Run.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `399 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T32 approval checklist proof.
- Light review result: no findings.
- Boundaries remain unchanged: roadmap phases, readiness docs, archive evidence, passing tests, and review recommendations are not approval sources.

## 2026-05-09 T33 No-Holdout Dry Run

Phase 8 is complete through T33.

- Completed task: T33 Readiness No-Holdout Dry Run.
- Active task: T34 Phase-Gate Readiness Review.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `402 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T33 dry-run proof.
- Light review result: no findings.
- Boundaries remain unchanged: dry run uses archive-only artifacts and records no holdout path/read/unlock or claim conclusion.

## 2026-05-09 T34 Phase-Gate Readiness Review

Phase 8 is complete through T34. Phase 9 is open as protocol-only holdout access design.

- Completed task: T34 Phase-Gate Readiness Review.
- Active task: T35 Holdout Access Protocol Deny-By-Default Contract.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `405 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Audit index row added for Phase 8 review.
- Evidence index row added for T34 review proof.
- Light/deep review result: no findings.
- Roadmap decision: keep Phase 9, modified to local protocol-only work. Holdout read/unlock, phase-gate approval, OOS/performance claims, live, broker/exchange, production, and capital-ready paths remain blocked.

## 2026-05-09 T35 Holdout Access Protocol

Phase 9 is complete through T35.

- Completed task: T35 Holdout Access Protocol Deny-By-Default Contract.
- Active task: T36 Holdout Approval Event Schema Contract.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `408 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T35 holdout access protocol proof.
- Light review result: no findings.
- Boundaries remain unchanged: Phase 9 is protocol-only; no approval event currently exists; holdout read/unlock, phase-gate approval, OOS/performance claims, live, broker/exchange, production, and capital-ready paths remain blocked.

## 2026-05-09 T36 Holdout Approval Event Schema

Phase 9 is complete through T36.

- Completed task: T36 Holdout Approval Event Schema Contract.
- Active task: T37 Holdout Access Audit Logging Contract.
- Latest validation: `.venv/bin/python -m pytest -q tests/` -> `411 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- Evidence index row added for T36 holdout approval event schema proof.
- Light review result: no findings.
- Boundaries remain unchanged: no approval event currently exists; generated, inferred, expired, revoked, or incomplete approval fixtures are rejected; holdout read/unlock, phase-gate approval, OOS/performance claims, live, broker/exchange, production, and capital-ready paths remain blocked.
