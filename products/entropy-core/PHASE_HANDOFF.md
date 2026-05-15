# PHASE_HANDOFF - Entropy Core

Date: 2026-05-15

Use this file only for restart/context recovery. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/audit/`, and
`docs/tasks.md`.

## Current State

- Phase: 27 Core V1 Productization
- Active task: none - Core V1 checkpoint complete
- Baseline: `625 passed, 20 skipped`
- Latest validation: 2026-05-14 full pytest `625 passed, 20 skipped`; ruff clean; scoped artifact/db pyright `0 errors`; `git diff --check` clean
- Ruff: clean on 2026-05-14
- Pyright: `src/entropy/artifacts` and `src/entropy/cli.py` clean on 2026-05-14; full pyright still has pre-existing test import-resolution errors
- Product hypothesis status: `local_evidence_strengthened_not_confirmed`
- Artifact support status: complete through T74; Core remains hidden/internal
- Core roadmap status: Core V1 complete through T122; automatic roadmap expansion stopped pending human-approved V2 roadmap
- Portfolio pause: Trader Risk Audit and Signal Analytics Sandbox are the
  active validation tracks; Core is paused unless they create a concrete Core
  dependency or a human approves Core V2.

## Next Action

Read:

1. `docs/CODEX_PROMPT.md`
2. `docs/AI_LOOP_OPERATING_MODEL.md`
3. `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`
4. `docs/tasks.md` Phase 27, T119-T122
5. `docs/core/CORE_V1_SURFACE_FREEZE.md`

Then wait for a human-approved Core V2 roadmap before starting new roadmap
tasks. Do not invent or auto-open Phase 28.
Do not reopen Core because of Product 1/2 planning unless a concrete bridge
dependency is named.

## Guardrails

- T66-T68 are deferred unless a human explicitly reactivates replay work.
- Core supports artifact validity; Core is not the public product now.
- Phase 15 does not approve public SDK, hosted service, product report
  rewrites, or product workspace edits from Core.
- T75-T122 are complete; do not auto-open new roadmap tasks until a human
  approves a Core V2 roadmap.
- Holdout read/unlock still blocked.
- Protocol-only holdout access design remains historical context, not active
  execution scope.
- No live orders, broker/exchange execution, production credentials, live
  capital, holdout access, external sandbox order emission, public SDK, hosted
  service, or OOS/performance claims.
- No external compliance certification, enterprise SLA, auth/RBAC, SSO, or
  tenant-isolation implementation in Phase 26.
- After T122, stop automatic roadmap expansion until a human approves a Core V2
  roadmap.

## Historical Pointers

- Phase 14 replay work complete through T65.
- Phase 15 opened by 2026-05-11 artifact-support override and completed
  through T74 on 2026-05-12.
- Review artifact: `docs/audit/ARTIFACT_SUPPORT_REVIEW.md`.
- Phase 16 opened on 2026-05-12 by executable Core roadmap update.
- T75-T78 completed on 2026-05-14.
- T79-T82 completed on 2026-05-14; Phase 18 opened with T83 active.
- T83-T86 completed on 2026-05-14; Phase 19 opened with T87 active.
- T87-T90 completed on 2026-05-14; Phase 20 opened with T91 active.
- T91-T94 completed on 2026-05-14; Phase 21 opened with T95 active.
- T95-T98 completed on 2026-05-14; Phase 22 opened with T99 active.
- T99-T102 completed on 2026-05-14; Phase 23 opened with T103 active.
- T103-T106 completed on 2026-05-14; Phase 24 opened with T107 active.
- T107-T110 completed on 2026-05-14; Phase 25 opened with T111 active.
- T111-T114 completed on 2026-05-14; Phase 26 opened with T115 active.
- T115-T118 completed on 2026-05-14; Phase 27 opened with T119 active.
- T119-T122 completed on 2026-05-14; Core V1 checkpoint is complete.
- Full prior task history is in `docs/tasks.md`, `docs/IMPLEMENTATION_JOURNAL.md`,
  and `docs/audit/`.
