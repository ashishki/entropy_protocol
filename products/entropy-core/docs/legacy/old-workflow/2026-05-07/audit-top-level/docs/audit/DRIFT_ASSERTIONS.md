# DRIFT_ASSERTIONS — D-K Deep Review

**Audit cycle:** Cycle 5 — Phase 1D-K archive-only baseline deep review
**Date:** 2026-05-06
**Prior artifact:** `INVARIANTS.md`
**Status:** Draft — pending Spec Owner acceptance

| INV-ID | Invariant short name | Verdict | Evidence pointer | Prior cycle verdict | Regression? |
|---|---|---|---|---|---|
| DK-INV-001 | D-K no unlock | PASS | `products/entropy-core/docs/audit/AUDIT_INDEX.md` Current State; D-K task boundaries | New | No |
| DK-INV-002 | P1D contract gate | PASS | `implementation.py`; `products/entropy-core/docs/tasks.md` P1D | New | No |
| DK-INV-003 | P1E forbidden outputs | PASS | `bounded.py`; `test_phase1e_bounded_baseline.py` | New | No |
| DK-INV-004 | P1F all-family binding | PASS | `registration.py` `_validate_outputs` | New | No |
| DK-INV-005 | P1F reproducible code hash | PASS | `registration.py` `_hash_source_files` normalizes repo-local source identity | New | No |
| DK-INV-006 | P1F no registry write | PASS | `registration.py` dataclasses and tests | New | No |
| DK-INV-007 | P1G denied requests | PASS | `evaluation.py` `validate_phase1g_evaluation_request` | New | No |
| DK-INV-008 | P1H approval gate | PASS | `governed.py` `run_phase1h_governed_evaluation` | New | No |
| DK-INV-009 | P1H no performance conclusion | PASS | `governed.py` result flags | New | No |
| DK-INV-010 | P1I stat status clarity | PASS | `report.py` `stat_field_statuses` records no-computation status | New | No |
| DK-INV-011 | P1J/P1K holdout closed | PASS | `decision.py` no-holdout guard | New | No |
| DK-INV-012 | Prompt current metadata | PASS | `PROMPT_0_META.md` through `PROMPT_5_CONSOLIDATED.md` headers | Prior F-C3-007/F-C4-001 class | No |
| TOTAL | - | PASS: 12 | FAIL: 0 | AMBIGUOUS: 0 | Regressions: 0 |
