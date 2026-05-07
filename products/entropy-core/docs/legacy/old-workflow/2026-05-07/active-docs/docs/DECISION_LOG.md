# Decision Log — Entropy Protocol

Status: Active compact log
Date: 2026-05-06

Full historical decision log snapshot:
`products/entropy-core/docs/archive/session_state/DECISION_LOG_full_2026-05-06.md`.

This file is retrieval convenience only. Canonical authority remains in the
referenced specs, task graph, audit packets, and source code.

| ID | Decision | Canonical source | Date |
|---|---|---|---|
| D-027 | Current evidence mode is archive-only. Live/streaming claims, live monitoring, provider uptime claims, live capital, and OOS/performance claims are not authorized. | `products/entropy-core/docs/audit/archive/p0_7/ARCHIVE_ONLY_EVIDENCE_MODE_DECISION.md` | 2026-05-05 |
| D-028 | Proceeded to Phase 1A Archive-Only Baseline Planning and Instrumentation; no live monitoring/trading/RDL/Growth/OOS claims. | `products/entropy-core/docs/audit/archive/p0_7/ARCHIVE_ONLY_CONTINUATION_DECISION.md` | 2026-05-05 |
| D-043 | Spec Owner selected Phase 1B Long-Only Baseline Readiness Planning after Phase 1A closure. | `products/entropy-core/docs/audit/archive/phase1a/POST_PHASE1A_OPERATIONS_PLAN.md` | 2026-05-05 |
| D-049 | Phase 1C closure selected Phase 1D Bounded Long-Only Baseline Implementation Planning. | `products/entropy-core/docs/tasks.md`; archived full task graph | 2026-05-05 |
| D-050 | Phase 1 D-K sequential research roadmap recorded; not blanket approval for future phases. | `products/entropy-core/docs/tasks.md`; archived full task graph | 2026-05-05 |
| D-051 | P1D implementation contract completed and light-reviewed; D-K continuation selected with light review after each phase and deep review after the block. | `src/entropy/baseline/implementation.py`; `tests/unit/test_phase1d_implementation_contract.py` | 2026-05-06 |
| D-052 | P1E bounded formation-only baseline logic completed without evaluation/holdout/performance claims. | `src/entropy/baseline/bounded.py`; `tests/unit/test_phase1e_bounded_baseline.py` | 2026-05-06 |
| D-053 | P1F baseline hash binding and preregistration surface completed without registry writes or evaluation approval. | `src/entropy/baseline/registration.py`; `tests/unit/test_phase1f_registration.py` | 2026-05-06 |
| D-054 | P1G/P1H governed evaluation config and first archive-only run metadata completed; no holdout/performance/phase-gate/production/capital-ready claim. | `src/entropy/baseline/evaluation.py`; `src/entropy/baseline/governed.py` | 2026-05-06 |
| D-055 | P1I/P1J/P1K report, no-holdout decision, and archive-only closure packets completed pending D-K deep review. | `src/entropy/baseline/report.py`; `src/entropy/baseline/decision.py` | 2026-05-06 |
| D-056 | Full D-K deep review and fix closure completed. F-DK-001/F-DK-002/F-DK-003 fixed. This does not approve holdout, production/capital-ready labels, live feeds, broker integration, Growth/RDL/RBE, or OOS/performance claims. | `products/entropy-core/docs/audit/REVIEW_REPORT.md`; `products/entropy-core/docs/tasks.md`; D-K code/tests | 2026-05-06 |
| D-057 | Commercial product direction split into three workspaces: Entropy Core, Trader Risk Audit, and Signal Analytics Sandbox. Trader Risk Audit is the primary validation wedge; live broker/exchange control, live capital, autonomous AI trading, private-source scraping, public marketplace, and unsupported performance claims remain blocked. | `docs/PRODUCT_PORTFOLIO.md`; `docs/AI_DEVELOPMENT_OPERATING_MODEL.md`; `products/` | 2026-05-07 |
| D-058 | Entropy Core implementation was isolated into the `products/entropy-core/` workspace. Core package code now lives under `src/entropy/`, tests under `tests/`, migrations under `migrations/`, and root docs remain portfolio-level only. | `products/entropy-core/pyproject.toml`; `products/entropy-core/src/entropy/`; `products/entropy-core/tests/`; `products/entropy-core/migrations/`; `.github/workflows/ci.yml` | 2026-05-07 |
