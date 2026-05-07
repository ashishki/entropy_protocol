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
| T10 Attribution Stream Boundary Audit | Test result | `tests/unit/test_attribution_reset.py::test_net_sharpe_excludes_stream_d`; `tests/unit/test_attribution_reset.py::test_attribution_streams_are_separate_fields`; `tests/unit/test_attribution_reset.py::test_archive_only_attribution_has_no_performance_conclusion`; `src/entropy/attribution/engine.py` | Net Sharpe excludes stream d and rejects raw stream d input; archive-only attribution serializes streams a/b/c/d separately with no performance conclusion label | 2026-05-07: `3 passed`; full baseline `311 passed, 20 skipped` | Yes |
| T11 Phase-Gate Evidence Packet | Test result | `tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_contains_required_sections`; `tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_fails_missing_evidence`; `tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_blocks_unapproved_claim_labels`; `src/entropy/evidence/phase_gate_packet.py` | Reset-era phase-gate packet lists baseline, required approvals, blocked claim surfaces, canonical evidence rows, and fails missing referenced artifacts | 2026-05-07: `3 passed`; full baseline `314 passed, 20 skipped` | Yes |
| Phase 3 Evaluation Safety Review | Review report | `docs/audit/PHASE3_REVIEW.md` | Phase 3 boundary review for T08-T11 evaluation safety | 2026-05-07: PASS; Stop-Ship 0, P0 0, P1 0, P2 0 | Yes |
| T12 Trader Risk Audit Bridge Contracts | Test result | `tests/integration/test_trader_risk_bridge_contract.py::test_bridge_contract_lists_allowed_and_forbidden_surfaces`; `tests/integration/test_trader_risk_bridge_contract.py::test_bridge_schemas_are_deterministic_and_no_llm_owned_fields`; `tests/integration/test_trader_risk_bridge_contract.py::test_bridge_rejects_live_and_claim_surfaces`; `docs/bridges/trader-risk-audit.md`; `src/entropy/bridges/trader_risk_audit.py` | Bridge contract lists allowed/forbidden Core surfaces and human gates; deterministic schemas reject LLM-owned fields and live/order/claim surfaces | 2026-05-07: `8 passed`; full baseline `322 passed, 20 skipped` | Yes |
| T13 Hypothesis Backtest Bridge Design | Test result | `tests/integration/test_hypothesis_bridge_design.py::test_hypothesis_bridge_requires_human_registration`; `tests/integration/test_hypothesis_bridge_design.py::test_hypothesis_bridge_rejects_ai_owned_truth_fields`; `tests/integration/test_hypothesis_bridge_design.py::test_hypothesis_bridge_records_required_boundaries`; `docs/bridges/hypothesis-backtest.md` | Design-only hypothesis bridge requires human registration, rejects AI-owned truth fields, and records holdout/leakage/no-claim/runtime boundaries | 2026-05-07: `3 passed`; full baseline `325 passed, 20 skipped` | Yes |
| T14 Reset Strategy Closure Review | Test result | `tests/reset/test_reset_closure.py::test_reset_review_contains_required_sections`; `tests/reset/test_reset_closure.py::test_audit_index_records_reset_review`; `tests/reset/test_reset_closure.py::test_codex_prompt_records_reset_closure_state`; `docs/audit/RESET_REVIEW.md` | Reset closure review summarizes completed tasks, evidence, open findings, and next recommendation; audit index and prompt record closure state | 2026-05-07: `3 passed`; full baseline `328 passed, 20 skipped` | Yes |

T08 through T14 heavy-task, product-bridge, and reset-closure evidence rows are indexed.

## Pending Evidence

| Topic | Expected artifact | Owning task |
|-------|-------------------|-------------|

## Retrieval Rules

- Add rows only after the referenced artifact exists.
- Prefer executable tests, review reports, fixtures, and generated packets over summary prose.
- Legacy summaries are context, not proof.
