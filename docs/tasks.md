# Task Graph — Entropy Protocol

Version: 1.1
Date: 2026-05-06
Status: Active compact task graph

Full historical task graph snapshot:
`docs/archive/session_state/tasks_full_2026-05-06.md`.

Status legend:
- `[ ]` Not started
- `[~]` Implemented, pending review
- `[x]` Complete
- `[!]` Blocked

---

## Current State

Last completed:
`DK-REVIEW-001 Full D-K Deep Review And Fix Closure`.

Current verdict:
`DK_DEEP_REVIEW_COMPLETE_FIXES_APPLIED_NO_CLAIMS`.

Next required task:
`SO-DK-001 Spec Owner Next Decision After D-K Fix Closure`.

Still forbidden:
- Phase 1 trading or live capital;
- archive holdout reads/unlock;
- live feeds or broker integration;
- Growth/RDL/RBE activation;
- portfolio/backtest performance claims;
- production labels or capital-ready labels;
- non-Python runtime/toolchain escalation without benchmark evidence, ADR,
  task/CI updates, and explicit human approval.

---

## Recent Completed Chain

| Task | Status | Evidence |
|---|---|---|
| P1D-001 Long-Only Implementation Contract | [x] | `entropy/baseline/implementation.py`; `tests/unit/test_phase1d_implementation_contract.py`; D-051 |
| P1E-001 Bounded Long-Only Baseline Logic | [x] | `entropy/baseline/bounded.py`; `tests/unit/test_phase1e_bounded_baseline.py`; D-052 |
| P1F-001/P1F-002 Baseline Registration Integration | [x] | `entropy/baseline/registration.py`; `tests/unit/test_phase1f_registration.py`; D-053 |
| P1G-001 Evaluation Configuration Contract | [x] | `entropy/baseline/evaluation.py`; `tests/unit/test_phase1g_evaluation_config.py`; D-054 |
| P1H-001 First Archive-Only Governed Evaluation Run | [x] | `entropy/baseline/governed.py`; `tests/unit/test_phase1h_governed_evaluation.py`; D-054 |
| P1I-001 Evaluation Report Assembly | [x] | `entropy/baseline/report.py`; `tests/unit/test_phase1i_j_k_packets.py`; D-055/D-056 |
| P1J-HUMAN-001/P1J-HUMAN-002 Research Decision And Holdout Gate | [x] | `entropy/baseline/decision.py`; D-055 |
| P1K-001/P1K-HUMAN-001 Archive-Only Closure | [x] | `entropy/baseline/decision.py`; D-055 |
| DK-REVIEW-001 Full D-K Deep Review And Fix Closure | [x] | `docs/audit/REVIEW_REPORT.md`; D-056 |

---

## [x] DK-REVIEW-001: Full D-K Deep Review And Fix Closure

Objective:
Run prompts 0-5 over the completed Phase 1D-K archive-only baseline block,
consolidate findings, and apply required fixes without opening claim surfaces.

Result:
- Canonical audit outputs refreshed:
  `META_ANALYSIS.md`, `ARCH_MODEL.md`, `INVARIANTS.md`,
  `DRIFT_ASSERTIONS.md`, `DRIFT_REPORT.md`, `ADVERSARIAL_REVIEW.md`,
  `REVIEW_REPORT.md`.
- F-DK-001 fixed: Phase 1F code hash normalizes repository-local source paths
  before hash payload construction.
- F-DK-002 fixed: Phase 1I report payload records deterministic stat-field
  status `not_computed_no_performance_conclusion`.
- F-DK-003 fixed: active audit prompt headers identify Cycle 5 D-K context.
- Verification: `277 passed, 20 skipped`; ruff passed; pyright 0 errors;
  `git diff --check` passed.

Boundary:
Holdout, production/capital-ready labels, live feeds, broker integration,
Growth/RDL/RBE, and OOS/performance claims remain blocked.

---

## [ ] SO-DK-001: Spec Owner Next Decision After D-K Fix Closure

Objective:
Spec Owner decides the next bounded block after D-K deep review fix closure.

Allowed decision outputs:
- accept D-K fix closure and stop;
- accept D-K fix closure and open a new bounded planning block;
- request iteration on D-K artifacts;
- explicitly reject the D-K review/fix closure and state required remediation.

Acceptance criteria:
- Decision is recorded in `docs/DECISION_LOG.md`.
- `docs/CODEX_PROMPT.md`, `docs/audit/AUDIT_INDEX.md`, and this task graph
  state the selected next block.
- No holdout, live, production, capital-ready, broker, Growth/RDL/RBE, or
  OOS/performance surface is opened unless a separate explicit gate says so.

---

## Historical Task Graph

The full completed task history from T01 through DK-REVIEW-001 is archived at:

`docs/archive/session_state/tasks_full_2026-05-06.md`

Use the archived snapshot only when a task explicitly requires historical
acceptance criteria or old phase evidence. Default handoff should use this
compact task graph.
