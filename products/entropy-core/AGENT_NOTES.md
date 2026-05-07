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
