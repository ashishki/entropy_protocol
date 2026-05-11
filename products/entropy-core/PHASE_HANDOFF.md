# PHASE_HANDOFF - Entropy Core

Date: 2026-05-11

Use this file only for restart/context recovery. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/audit/`, and
`docs/tasks.md`.

## Current State

- Phase: 15 Artifact Support Mode
- Active task: T69 Shared Artifact Contract Freeze
- Baseline: 501 pass / 20 skip
- Ruff: clean
- Pyright: clean
- Product hypothesis status: `local_evidence_strengthened_not_confirmed`

## Next Action

Read:

1. `docs/CODEX_PROMPT.md`
2. `docs/ARTIFACT_SUPPORT_ROADMAP.md`
3. `docs/tasks.md#t69-shared-artifact-contract-freeze`

Then define the minimal shared artifact contract for Trader and Signal reports.

## Guardrails

- T66-T68 are deferred unless a human explicitly reactivates replay work.
- Core supports artifact validity; Core is not the public product now.
- Holdout read/unlock still blocked.
- Protocol-only holdout access design remains historical context, not active
  execution scope.
- No live orders, broker/exchange execution, production credentials, live
  capital, holdout access, external sandbox order emission, public SDK, hosted
  service, or OOS/performance claims.

## Historical Pointers

- Phase 14 replay work complete through T65.
- Phase 15 opened by 2026-05-11 artifact-support override.
- Full prior task history is in `docs/tasks.md`, `docs/IMPLEMENTATION_JOURNAL.md`,
  and `docs/audit/`.
