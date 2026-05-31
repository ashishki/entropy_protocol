# PHASE_HANDOFF - Entropy Core

Date: 2026-05-31

Use this file only for restart/context recovery. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/audit/`, and
`docs/tasks.md`.

## Current State

- Phase: 31 V2 Internal Kernel Review
- Active task: none - human gate required for next bounded Core V2 phase
- Baseline: `625 passed, 20 skipped`
- Latest validation: 2026-05-14 full pytest `625 passed, 20 skipped`; ruff clean; scoped artifact/db pyright `0 errors`; `git diff --check` clean
- Ruff: clean on 2026-05-14
- Pyright: `src/entropy/artifacts` and `src/entropy/cli.py` clean on 2026-05-14; full pyright still has pre-existing test import-resolution errors
- Product hypothesis status: `local_evidence_strengthened_not_confirmed`
- Artifact support status: complete through T74; Core remains hidden/internal
- Core roadmap status: Core V1 complete through T122; Core V2 start approved by D-CORE-V2-001; Phase 28 complete through T126; Phase 29 complete through T130; Phase 30 complete through T134; Phase 31 complete through T138; no active next task until a human opens a new bounded Core V2 phase

## Next Action

Read:

1. `docs/CODEX_PROMPT.md`
2. `docs/AI_LOOP_OPERATING_MODEL.md`
3. `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`
4. `docs/tasks.md` Phase 31, T135-T138
5. `docs/core/CORE_V1_SURFACE_FREEZE.md`

Do not continue beyond T138 until a human opens a new bounded Core V2 phase.
Product workspace edits, product report ownership, external delivery approval,
public SDK, hosted service, runtime RAG, live, holdout, compliance, production
credential, and capital scope remain blocked.

## Guardrails

- T66-T68 are deferred unless a human explicitly reactivates replay work.
- Core supports artifact validity; Core is not the public product now.
- Phase 15 does not approve public SDK, hosted service, product report
  rewrites, or product workspace edits from Core.
- T75-T122 are complete; T123 is complete by human decision D-CORE-V2-001.
- T124 is complete and defines the schema evolution policy.
- T125 is complete and remained library-only.
- T126 completed Phase 28 review and opened Phase 29.
- T127 is complete and preserves all restricted-surface blocks.
- T128 is complete and remained file-local/deterministic.
- T129-T130 completed evidence inspect alignment and Phase 29 review.
- T131 is complete and preserves all restricted-surface blocks.
- T132 is complete and preserved all restricted-surface blocks.
- T133 is complete and preserved all restricted-surface blocks.
- T134 is complete and preserved all restricted-surface blocks.
- T135 is complete and preserved all restricted-surface blocks.
- T136 is complete and preserved all restricted-surface blocks.
- T137 is complete and preserved all restricted-surface blocks.
- T138 is complete and preserved all restricted-surface blocks.
- No active next task is approved.
- Holdout read/unlock still blocked.
- Protocol-only holdout access design remains historical context, not active
  execution scope.
- No live orders, broker/exchange execution, production credentials, live
  capital, holdout access, external sandbox order emission, public SDK, hosted
  service, or OOS/performance claims.
- No external compliance certification, enterprise SLA, auth/RBAC, SSO, or
  tenant-isolation implementation in Phase 26.
- Core V2 start approval does not approve public SaaS, public SDK, hosted
  service, auth/RBAC/SSO, tenant isolation, external compliance certification,
  holdout access, live feeds by default, broker/exchange execution, production
  credentials, live capital, production labels, capital-ready labels, or
  unsupported OOS/performance claims.

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
- Phase 28 opened on 2026-05-29 by D-CORE-V2-001 and completed through T126.
- Phase 29 opened on 2026-05-29 and completed through T130.
- Phase 30 opened on 2026-05-29 with T131 active and completed through T134.
- Phase 31 opened on 2026-05-29 with T135 active and completed through T138.
- Full prior task history is in `docs/tasks.md`, `docs/IMPLEMENTATION_JOURNAL.md`,
  and `docs/audit/`.
