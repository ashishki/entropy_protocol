# Evidence Index — Entropy Protocol

Status: Active compact index
Date: 2026-05-06

Full historical evidence index snapshot:
`docs/archive/session_state/EVIDENCE_INDEX_full_2026-05-06.md`.

This file is a retrieval surface, not authority. Load archived snapshots only
when a task explicitly needs older phase evidence.

## Current Evidence

| Evidence | Artifact(s) | Status | Date |
|---|---|---|---|
| D-K deep review and fix closure | `docs/audit/REVIEW_REPORT.md`; `docs/audit/META_ANALYSIS.md`; `docs/audit/ARCH_MODEL.md`; `docs/audit/INVARIANTS.md`; `docs/audit/DRIFT_ASSERTIONS.md`; `docs/audit/DRIFT_REPORT.md`; `docs/audit/ADVERSARIAL_REVIEW.md` | Complete as draft pending Spec Owner acceptance; no claims opened | 2026-05-06 |
| P1F source-path-stable code hash | `entropy/baseline/registration.py`; `tests/unit/test_phase1f_registration.py` | Fixed F-DK-001; focused slice 6 passed | 2026-05-06 |
| P1I stat-field no-computation status | `entropy/baseline/report.py`; `tests/unit/test_phase1i_j_k_packets.py` | Fixed F-DK-002; focused slice 6 passed | 2026-05-06 |
| Active audit prompt metadata | `docs/audit/PROMPT_0_META.md` through `docs/audit/PROMPT_5_CONSOLIDATED.md` | Fixed F-DK-003; prompts identify Cycle 5 D-K context | 2026-05-06 |
| Full test baseline | `.venv/bin/python -m pytest -q tests/` | 277 passed, 20 skipped | 2026-05-06 |
| Static checks | ruff, pyright, `git diff --check` | ruff passed; pyright 0 errors; diff check passed | 2026-05-06 |

## Archive Map

| Evidence range | Location |
|---|---|
| Full historical evidence index | `docs/archive/session_state/EVIDENCE_INDEX_full_2026-05-06.md` |
| Full historical task graph | `docs/archive/session_state/tasks_full_2026-05-06.md` |
| Full historical implementation journal | `docs/archive/session_state/IMPLEMENTATION_JOURNAL_full_2026-05-06.md` |
| Full historical decision log | `docs/archive/session_state/DECISION_LOG_full_2026-05-06.md` |
| Phase 1A audit packets | `docs/audit/archive/phase1a/` |
| Phase 0.x evidence packets | `docs/audit/archive/p0_5/`, `docs/audit/archive/p0_6/`, `docs/audit/archive/p0_7/` |
| SimBroker/P4/data-stability packets | `docs/audit/archive/simbroker/`, `docs/audit/archive/p4/`, `docs/audit/archive/data_stability/` |
