# Decision Log — Entropy Protocol

Status: Active compact log
Date: 2026-05-06

Full historical decision log snapshot:
`docs/archive/session_state/DECISION_LOG_full_2026-05-06.md`.

This file is retrieval convenience only. Canonical authority remains in the
referenced specs, task graph, audit packets, and source code.

| ID | Decision | Canonical source | Date |
|---|---|---|---|
| D-027 | Current evidence mode is archive-only. Live/streaming claims, live monitoring, provider uptime claims, live capital, and OOS/performance claims are not authorized. | `docs/audit/archive/p0_7/ARCHIVE_ONLY_EVIDENCE_MODE_DECISION.md` | 2026-05-05 |
| D-028 | Proceeded to Phase 1A Archive-Only Baseline Planning and Instrumentation; no live monitoring/trading/RDL/Growth/OOS claims. | `docs/audit/archive/p0_7/ARCHIVE_ONLY_CONTINUATION_DECISION.md` | 2026-05-05 |
| D-043 | Spec Owner selected Phase 1B Long-Only Baseline Readiness Planning after Phase 1A closure. | `docs/audit/archive/phase1a/POST_PHASE1A_OPERATIONS_PLAN.md` | 2026-05-05 |
| D-049 | Phase 1C closure selected Phase 1D Bounded Long-Only Baseline Implementation Planning. | `docs/tasks.md`; archived full task graph | 2026-05-05 |
| D-050 | Phase 1 D-K sequential research roadmap recorded; not blanket approval for future phases. | `docs/tasks.md`; archived full task graph | 2026-05-05 |
| D-051 | P1D implementation contract completed and light-reviewed; D-K continuation selected with light review after each phase and deep review after the block. | `entropy/baseline/implementation.py`; `tests/unit/test_phase1d_implementation_contract.py` | 2026-05-06 |
| D-052 | P1E bounded formation-only baseline logic completed without evaluation/holdout/performance claims. | `entropy/baseline/bounded.py`; `tests/unit/test_phase1e_bounded_baseline.py` | 2026-05-06 |
| D-053 | P1F baseline hash binding and preregistration surface completed without registry writes or evaluation approval. | `entropy/baseline/registration.py`; `tests/unit/test_phase1f_registration.py` | 2026-05-06 |
| D-054 | P1G/P1H governed evaluation config and first archive-only run metadata completed; no holdout/performance/phase-gate/production/capital-ready claim. | `entropy/baseline/evaluation.py`; `entropy/baseline/governed.py` | 2026-05-06 |
| D-055 | P1I/P1J/P1K report, no-holdout decision, and archive-only closure packets completed pending D-K deep review. | `entropy/baseline/report.py`; `entropy/baseline/decision.py` | 2026-05-06 |
| D-056 | Full D-K deep review and fix closure completed. F-DK-001/F-DK-002/F-DK-003 fixed. This does not approve holdout, production/capital-ready labels, live feeds, broker integration, Growth/RDL/RBE, or OOS/performance claims. | `docs/audit/REVIEW_REPORT.md`; `docs/tasks.md`; D-K code/tests | 2026-05-06 |
