# Evidence Index - Entropy Core

Version: 1.0
Last updated: 2026-05-07

This file indexes proof artifacts. It is not authority by itself.

## Evidence Table

| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |
|------------------------|---------------|----------|---------------|---------------|------------|
| T01 Existing Project Baseline Skeleton | Test result | `tests/reset/test_reset_tooling.py`; `tests/reset/test_reset_skeleton.py` | Python 3.12 tooling, package import/version surface, CLI help surface | 2026-05-07: `3 passed`; full baseline `280 passed, 20 skipped` | Yes |
| T02 Product-Local CI Setup | Test result | `tests/reset/test_ci_contract.py`; `.github/workflows/ci.yml` | Python 3.12 CI setup, dev install, pytest/ruff/format/pyright commands, PostgreSQL 16 test service, no live trading credentials | 2026-05-07: `3 passed`; full baseline `283 passed, 20 skipped` | Yes |
| T03 Reset Baseline Smoke Tests | Test result | `tests/reset/test_reset_smoke.py`; `docs/CODEX_PROMPT.md` | Shared tracing boundary, metrics stubs, CLI health, reset baseline documentation, legacy context scoping | 2026-05-07: `5 passed`; full baseline `288 passed, 20 skipped` | Yes |
| Phase 1 Reset Foundation Review | Review report | `docs/audit/PHASE1_REVIEW.md` | Phase 1 boundary review for T01-T03 reset foundation | 2026-05-07: PASS; Stop-Ship 0, P0 0, P1 0, P2 0 | Yes |
| T04 Registry Append-Only Audit | Test result | `tests/unit/test_registry_append_only_reset.py`; `tests/integration/test_registry_append_only_reset.py` | Registry/governance no UPDATE/DELETE app paths, missing-hash-before-DB guard, migration append-only table checks | 2026-05-07: `3 passed`; full baseline `291 passed, 20 skipped` | Yes |
| T05 Evidence Index and Journal Sync | Test result | `tests/reset/test_evidence_index_contract.py` | Evidence rows point to existing artifacts, reset journal entry is retrievable, legacy references remain scoped | 2026-05-07: `3 passed`; full baseline `294 passed, 20 skipped` | Yes |
| T06 No-Claim Report Boundary | Test result | `tests/unit/test_no_claim_report_boundary.py`; `src/entropy/baseline/report.py`; `src/entropy/baseline/decision.py` | Archive-only stat status, no production/capital-ready/OOS claim flags without gates, D-K closure no-claim boundary | 2026-05-07: `5 passed`; full baseline `299 passed, 20 skipped` | Yes |
| T07 Governance Approval Gate Audit | Test result | `tests/unit/test_governance_gate_reset.py`; `src/entropy/governance/approval.py` | Human approval gates for phase gate reports, holdout access, and provider activation | 2026-05-07: `3 passed`; full baseline `302 passed, 20 skipped` | Yes |
| Phase 2 Governance Integrity Review | Review report | `docs/audit/PHASE2_REVIEW.md` | Phase 2 boundary review for T04-T07 governance integrity | 2026-05-07: PASS; Stop-Ship 0, P0 0, P1 0, P2 0 | Yes |
| T08 Data and Leakage Gate Verification | Test result | `tests/unit/test_data_leakage_reset.py::test_leakage_failure_blocks_oos_label`; `tests/unit/test_data_leakage_reset.py::test_holdout_lock_checked_before_path_open`; `src/entropy/walkforward/leakage.py`; `src/entropy/data/holdout.py` | OOS labels blocked by leakage failures with failing check ids; holdout lock checked before path read; dataset hash order independence | 2026-05-07: `3 passed`; full baseline `305 passed, 20 skipped` | Yes |
| T09 SimBroker and Cost Surface Regression | Test result | `tests/unit/test_simbroker_reset.py` | Deterministic fill logs, separated SimBroker cost fields, no live broker/exchange client imports | 2026-05-07: `3 passed`; full baseline `308 passed, 20 skipped` | Yes |

T08 and T10 must add heavy-task evidence rows when implemented.

## Pending Evidence

| Topic | Expected artifact | Owning task |
|-------|-------------------|-------------|
| Attribution stream proof | `tests/unit/test_attribution_reset.py::test_net_sharpe_excludes_stream_d` | T10 |
| Phase-gate packet proof | `tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_contains_required_sections` | T11 |
| Product bridge proof | `tests/integration/test_trader_risk_bridge_contract.py::test_bridge_rejects_live_and_claim_surfaces` | T12 |

## Retrieval Rules

- Add rows only after the referenced artifact exists.
- Prefer executable tests, review reports, fixtures, and generated packets over summary prose.
- Legacy summaries are context, not proof.
