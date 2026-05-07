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
