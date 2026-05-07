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

T08 and T10 must add heavy-task evidence rows when implemented.

## Pending Evidence

| Topic | Expected artifact | Owning task |
|-------|-------------------|-------------|
| Leakage/holdout proof | `tests/unit/test_data_leakage_reset.py::test_leakage_failure_blocks_oos_label` | T08 |
| Attribution stream proof | `tests/unit/test_attribution_reset.py::test_net_sharpe_excludes_stream_d` | T10 |
| Phase-gate packet proof | `tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_contains_required_sections` | T11 |
| Product bridge proof | `tests/integration/test_trader_risk_bridge_contract.py::test_bridge_rejects_live_and_claim_surfaces` | T12 |

## Retrieval Rules

- Add rows only after the referenced artifact exists.
- Prefer executable tests, review reports, fixtures, and generated packets over summary prose.
- Legacy summaries are context, not proof.
