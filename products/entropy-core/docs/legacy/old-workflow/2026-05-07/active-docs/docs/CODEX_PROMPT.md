# CODEX_PROMPT.md

Version: 3.8
Date: 2026-05-06
Phase: D-K deep review fix closure

Compact current-state handoff. Historical task graph, logs, evidence, and
Phase1A packets are archived and should not be loaded by default.

## Current State

- Current task: `SO-DK-001 Spec Owner Next Decision After D-K Fix Closure`
- Last completed task: `DK-REVIEW-001 Full D-K Deep Review And Fix Closure`
- Current verdict: `DK_DEEP_REVIEW_COMPLETE_FIXES_APPLIED_NO_CLAIMS`
- Test baseline: `277 passed, 20 skipped`
- Holdout: locked
- Phase 1 trading/live capital: not approved
- Production/capital-ready labels: not approved

## Read First

For a normal coding session, read only:

1. `products/entropy-core/docs/CODEX_PROMPT.md`
2. `products/entropy-core/docs/tasks.md`
3. `products/entropy-core/docs/audit/AUDIT_INDEX.md`
4. `products/entropy-core/docs/audit/REVIEW_REPORT.md`

Load archive files only when a task explicitly needs historical evidence.

## Active Decisions

| ID | Summary |
|---|---|
| D-027 | Evidence mode is archive-only; live/streaming claims are not authorized. |
| D-050 | Phase 1 D-K roadmap was recorded; it is not blanket approval. |
| D-051 | P1D implementation contract completed and light-reviewed. |
| D-052 | P1E bounded formation-only baseline logic completed. |
| D-053 | P1F baseline hash binding and preregistration surface completed. |
| D-054 | P1G/P1H governed config and archive-only run metadata completed. |
| D-055 | P1I/P1J/P1K report, decision, and no-holdout closure completed. |
| D-056 | D-K deep review and fix closure completed; F-DK-001/002/003 fixed. |

Strategy recommendation:
If SO-DK-001 accepts D-K fix closure, open proposed block
`P0C Phase 0 Exit Evidence And D-K Admission Planning`.

Full decision history:
`products/entropy-core/docs/archive/session_state/DECISION_LOG_full_2026-05-06.md`.

## Current Artifacts

| Area | Active artifact |
|---|---|
| Task graph | `products/entropy-core/docs/tasks.md` |
| Audit status | `products/entropy-core/docs/audit/REVIEW_REPORT.md` |
| Strategy recommendation | `products/entropy-core/docs/audit/POST_DK_STRATEGY_REVIEW.md`; `products/entropy-core/docs/audit/NEXT_PHASE_PLAN.md` |
| Audit index | `products/entropy-core/docs/audit/AUDIT_INDEX.md` |
| D-K code | `src/entropy/baseline/implementation.py`, `bounded.py`, `registration.py`, `evaluation.py`, `governed.py`, `report.py`, `decision.py` |
| D-K tests | `tests/unit/test_phase1d_implementation_contract.py` through `tests/unit/test_phase1i_j_k_packets.py` |
| Historical Phase1A packets | `products/entropy-core/docs/audit/archive/phase1a/` |
| Full historical logs | `products/entropy-core/docs/archive/session_state/` |

## Current Scope

Allowed:
- prepare or record the Spec Owner next decision;
- inspect or explain D-K review artifacts and fixes;
- update compact current-state docs for real status changes.

Forbidden:
- executable alpha logic;
- portfolio allocation or backtest/evaluation;
- strategy performance metrics;
- archive holdout read/unlock;
- Growth/RDL/RBE activation;
- live feeds, broker integration, or live capital;
- non-Python runtime/toolchain escalation without the approved escalation gate;
- OOS/performance, validated-alpha, production, or capital-ready claims.

## Open Findings

- No open D-K P0/P1 findings remain after fix closure.
- F-DK-001, F-DK-002, and F-DK-003 are fixed pending Spec Owner acceptance.
- Holdout remains closed; production/capital-ready labels remain blocked.

## Verification Defaults

For code changes in this scope, run:

- `.venv/bin/python -m pytest -q tests/`
- `.venv/bin/python -m ruff check src/entropy tests`
- `.venv/bin/python -m pyright src/entropy`
- `git diff --check`

## Archive Pointers

| Historical surface | Snapshot/location |
|---|---|
| Full task graph | `products/entropy-core/docs/archive/session_state/tasks_full_2026-05-06.md` |
| Full implementation journal | `products/entropy-core/docs/archive/session_state/IMPLEMENTATION_JOURNAL_full_2026-05-06.md` |
| Full evidence index | `products/entropy-core/docs/archive/session_state/EVIDENCE_INDEX_full_2026-05-06.md` |
| Full decision log | `products/entropy-core/docs/archive/session_state/DECISION_LOG_full_2026-05-06.md` |
| Command hook log | `products/entropy-core/docs/archive/session_state/hooks_log_2026-05-01_to_2026-05-06.txt` |
