# Task Graph - Entropy Core

Version: 1.0
Last updated: 2026-05-07
Status: reset task graph

---

## Phase Plan

| Phase | Name | Tasks | Delivery | Gate criteria |
|-------|------|-------|----------|---------------|
| 1 | Reset Foundation | T01-T03 | Existing package baseline, Python 3.12 tooling, product-local CI, and smoke tests. | Phase 1 audit passes; local baseline recorded; ruff/format/pyright commands known. |
| 2 | Governance Integrity | T04-T07 | Registry, governance, evidence index, and no-claim report boundaries synchronized with current code. | Append-only, human-gate, no-claim, and evidence-index checks pass. |
| 3 | Evaluation Safety | T08-T11 | Data/leakage/holdout, SimBroker, attribution, and phase-gate evidence hardening. | Heavy evidence tasks have executable tests and indexed proof. |
| 4 | Product Bridges | T12-T14 | Trader Risk Audit primitives and hypothesis/backtest bridge contracts. | Bridge tests prove no live/no-claim boundaries are preserved. |

## T01: Existing Project Baseline Skeleton

Owner:      codex
Phase:      1
Type:       none
Depends-On: none
Status:     done 2026-05-07

Objective: |
  Align the existing Entropy Core package skeleton with the reset governance loop: Python 3.12 tooling, package import surface, CLI health/version command surface, and baseline verification commands.

Acceptance-Criteria:
  - id: AC-1
    description: "`pyproject.toml` requires Python 3.12 and sets ruff target version to py312."
    test: "tests/reset/test_reset_tooling.py::test_pyproject_requires_python_312"
  - id: AC-2
    description: "Importing `entropy` exposes a non-empty package version or package metadata fallback."
    test: "tests/reset/test_reset_skeleton.py::test_entropy_package_import_surface"
  - id: AC-3
    description: "`entropy --help` exits with code 0 and includes the local operator command surface."
    test: "tests/reset/test_reset_skeleton.py::test_entropy_cli_help_runs"

Files:
  - pyproject.toml
  - src/entropy/__init__.py
  - src/entropy/cli.py
  - tests/reset/test_reset_tooling.py
  - tests/reset/test_reset_skeleton.py

Context-Refs:
  - docs/legacy/CORE_LEGACY_SUMMARY.md
  - docs/DECISION_LOG.md#D-RESET-001

Notes: |
  Do not restructure `src/entropy/`. This task establishes current truth over the existing codebase.

## T02: Product-Local CI Setup

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01
Status:     done 2026-05-07

Objective: |
  Add or update the product-local CI workflow that installs Entropy Core on Python 3.12 and runs pytest, ruff check, ruff format check, and pyright from `products/entropy-core/`.

Acceptance-Criteria:
  - id: AC-1
    description: "`.github/workflows/ci.yml` uses Python 3.12 and installs the package with development dependencies."
    test: "tests/reset/test_ci_contract.py::test_ci_uses_python_312_and_dev_install"
  - id: AC-2
    description: "CI has separate commands for pytest, ruff check, ruff format check, and pyright."
    test: "tests/reset/test_ci_contract.py::test_ci_runs_required_quality_commands"
  - id: AC-3
    description: "CI defines PostgreSQL 16 only as a test service and does not define broker, exchange, or live data credentials."
    test: "tests/reset/test_ci_contract.py::test_ci_has_no_live_trading_credentials"

Files:
  - .github/workflows/ci.yml
  - tests/reset/test_ci_contract.py

Context-Refs:
  - docs/ARCHITECTURE.md#runtime-and-isolation-model

Notes: |
  Product-local CI is the reset contract even if repository-level CI later delegates into it.

## T03: Reset Baseline Smoke Tests

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01, T02
Status:     done 2026-05-07

Objective: |
  Record the first reset baseline and add smoke tests for shared tracing, metrics stubs, CLI health, and documentation state.

Acceptance-Criteria:
  - id: AC-1
    description: "`get_tracer()` is imported only from `src/entropy/tracing.py` by code that creates spans."
    test: "tests/reset/test_reset_smoke.py::test_shared_tracing_boundary"
  - id: AC-2
    description: "The reset baseline entry in `docs/CODEX_PROMPT.md` contains the pytest pass/skip count recorded by this task."
    test: "tests/reset/test_reset_smoke.py::test_codex_prompt_records_reset_baseline"
  - id: AC-3
    description: "No active task file points to the old workflow directory except through explicit legacy `Context-Refs`."
    test: "tests/reset/test_reset_smoke.py::test_legacy_context_is_scoped"

Files:
  - src/entropy/tracing.py
  - src/entropy/metrics.py
  - docs/CODEX_PROMPT.md
  - tests/reset/test_reset_smoke.py

Context-Refs:
  - docs/legacy/RESET_PLAN.md

Notes: |
  After this task, update baseline values in `docs/CODEX_PROMPT.md`.

## T04: Registry Append-Only Audit

Owner:      codex
Phase:      2
Type:       none
Depends-On: T03
Status:     done 2026-05-07
Status:     done 2026-05-07
Status:     done 2026-05-07

Objective: |
  Verify and harden registry/governance append-only behavior across SQLAlchemy models, migrations, and application write paths.

Acceptance-Criteria:
  - id: AC-1
    description: "Application code has no UPDATE or DELETE path for trial registry or governance events."
    test: "tests/unit/test_registry_append_only_reset.py::test_registry_governance_have_no_update_delete_paths"
  - id: AC-2
    description: "A missing hash blocks registry admission before any database write is attempted."
    test: "tests/unit/test_registry_append_only_reset.py::test_missing_hash_blocks_before_write"
  - id: AC-3
    description: "Alembic migration metadata preserves append-only tables and does not add mutation triggers."
    test: "tests/integration/test_registry_append_only_reset.py::test_migrations_preserve_append_only_tables"

Files:
  - src/entropy/registry/
  - migrations/
  - tests/unit/test_registry_append_only_reset.py
  - tests/integration/test_registry_append_only_reset.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules
  - docs/core/PROTOCOL_SPEC.md

Notes: |
  This task may read old registry tests, but should not load full legacy task history.

## T05: Evidence Index and Journal Sync

Owner:      codex
Phase:      2
Type:       none
Depends-On: T03

Objective: |
  Rebuild evidence and journal entries around real current artifacts so future tasks can retrieve proof without reading old workflow logs by default.

Acceptance-Criteria:
  - id: AC-1
    description: "Every non-pending row in `docs/EVIDENCE_INDEX.md` points to an existing file or test function."
    test: "tests/reset/test_evidence_index_contract.py::test_evidence_index_rows_point_to_existing_artifacts"
  - id: AC-2
    description: "`docs/IMPLEMENTATION_JOURNAL.md` has an append-only reset entry that names the reset scope and next task."
    test: "tests/reset/test_evidence_index_contract.py::test_journal_has_reset_entry"
  - id: AC-3
    description: "Legacy summary pointers are present in the legacy summary and absent from active task instructions except scoped `Context-Refs`."
    test: "tests/reset/test_evidence_index_contract.py::test_legacy_archive_pointers_are_scoped"

Files:
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - tests/reset/test_evidence_index_contract.py

Context-Refs:
  - docs/legacy/CORE_LEGACY_SUMMARY.md

Notes: |
  Evidence rows may remain pending only when the named future task has not created the artifact yet.

## T06: No-Claim Report Boundary

Owner:      codex
Phase:      2
Type:       none
Depends-On: T03

Objective: |
  Verify current report/evidence surfaces distinguish archive-only, scaffold-only, and admissible evaluation states without opening performance, OOS, production, or capital-ready claims.

Acceptance-Criteria:
  - id: AC-1
    description: "Archive-only reports serialize a `not_computed_no_performance_conclusion` status for performance-like fields."
    test: "tests/unit/test_no_claim_report_boundary.py::test_archive_only_reports_have_no_performance_conclusion_status"
  - id: AC-2
    description: "Report builders reject production, capital-ready, or OOS labels when required gate evidence is absent."
    test: "tests/unit/test_no_claim_report_boundary.py::test_report_builders_reject_claim_labels_without_gate_evidence"
  - id: AC-3
    description: "Current D-K baseline report surfaces remain no-claim after reset."
    test: "tests/unit/test_no_claim_report_boundary.py::test_dk_baseline_report_remains_no_claim"

Files:
  - src/entropy/evidence/
  - src/entropy/baseline/report.py
  - src/entropy/baseline/decision.py
  - tests/unit/test_no_claim_report_boundary.py

Context-Refs:
  - docs/legacy/CORE_LEGACY_SUMMARY.md#durable-boundaries
  - docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions

Notes: |
  Do not add new claim labels in this task.

## T07: Governance Approval Gate Audit

Owner:      codex
Phase:      2
Type:       none
Depends-On: T04, T06
Status:     done 2026-05-07

Objective: |
  Verify human approval gates for research object registration, evaluation execution, phase-gate acceptance, holdout access, data-provider activation, and product bridge activation.

Acceptance-Criteria:
  - id: AC-1
    description: "Phase-gate report generation returns NOT_APPROVED when matching human governance event evidence is absent."
    test: "tests/unit/test_governance_gate_reset.py::test_phase_gate_report_requires_human_approval_event"
  - id: AC-2
    description: "Holdout access attempts without an explicit approved gate return a blocked status and do not read holdout data."
    test: "tests/unit/test_governance_gate_reset.py::test_holdout_access_without_gate_is_blocked_before_read"
  - id: AC-3
    description: "Provider activation requires a declared provider contract and human approval record."
    test: "tests/unit/test_governance_gate_reset.py::test_provider_activation_requires_contract_and_approval"

Files:
  - src/entropy/governance/
  - src/entropy/evidence/
  - tests/unit/test_governance_gate_reset.py

Context-Refs:
  - docs/ARCHITECTURE.md#human-approval-boundaries
  - docs/governance/governor.md

Notes: |
  Keep provider activation design-only unless a separate task approves a real provider.

## T08: Data and Leakage Gate Verification

Owner:      codex
Phase:      3
Type:       none
Depends-On: T07
Status:     done 2026-05-07

Objective: |
  Verify local historical data contracts, deterministic hashes, purge/embargo behavior, leakage checks, and holdout locks before any evaluation result can claim OOS status.

Acceptance-Criteria:
  - id: AC-1
    description: "Dataset hash output is identical for the same rows presented in different orders."
    test: "tests/unit/test_data_leakage_reset.py::test_dataset_hash_is_order_independent"
  - id: AC-2
    description: "Leakage check failure blocks OOS label creation and records the failing check id."
    test: "tests/unit/test_data_leakage_reset.py::test_leakage_failure_blocks_oos_label"
  - id: AC-3
    description: "Holdout lock status is checked before any holdout path is opened or read."
    test: "tests/unit/test_data_leakage_reset.py::test_holdout_lock_checked_before_path_open"

Execution-Mode: heavy
Evidence:
  - tests/unit/test_data_leakage_reset.py::test_leakage_failure_blocks_oos_label
  - docs/EVIDENCE_INDEX.md row for leakage/holdout proof
Verifier-Focus: |
  Confirm no OOS/performance label can be produced when leakage evidence is absent or holdout remains locked.

Files:
  - src/entropy/data/
  - src/entropy/walkforward/
  - src/entropy/hashing/
  - tests/unit/test_data_leakage_reset.py
  - docs/EVIDENCE_INDEX.md

Context-Refs:
  - docs/core/PROTOCOL_SPEC.md
  - docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions

Notes: |
  This is heavy because leakage/holdout mistakes can invalidate downstream research claims.

## T09: SimBroker and Cost Surface Regression

Owner:      codex
Phase:      3
Type:       none
Depends-On: T08
Status:     done 2026-05-07

Objective: |
  Verify deterministic SimBroker fill/cost behavior and preserve scaffold/calibration boundaries without live broker integration.

Acceptance-Criteria:
  - id: AC-1
    description: "Identical signal, bar, and cost model inputs produce byte-identical fill logs."
    test: "tests/unit/test_simbroker_reset.py::test_simbroker_fill_logs_are_deterministic"
  - id: AC-2
    description: "Cost components are serialized separately for commission, slippage, market impact, borrow, and funding."
    test: "tests/unit/test_simbroker_reset.py::test_simbroker_cost_components_are_separate"
  - id: AC-3
    description: "No SimBroker path imports broker/exchange API clients."
    test: "tests/unit/test_simbroker_reset.py::test_simbroker_has_no_live_broker_imports"

Files:
  - src/entropy/simbroker/
  - tests/unit/test_simbroker_reset.py

Context-Refs:
  - docs/ARCHITECTURE.md#non-goals-v1

Notes: |
  Do not add calibration claims or provider activation in this task.

## T10: Attribution Stream Boundary Audit

Owner:      codex
Phase:      3
Type:       none
Depends-On: T08, T09
Status:     done 2026-05-07

Objective: |
  Verify P&L streams, cost drag, and reportable attribution fields remain separated and cannot silently create unsupported performance conclusions.

Acceptance-Criteria:
  - id: AC-1
    description: "Net Sharpe calculation excludes stream d and rejects direct stream d inclusion."
    test: "tests/unit/test_attribution_reset.py::test_net_sharpe_excludes_stream_d"
  - id: AC-2
    description: "Attribution output stores streams a, b, c, and d in separate fields with no implicit merge."
    test: "tests/unit/test_attribution_reset.py::test_attribution_streams_are_separate_fields"
  - id: AC-3
    description: "Archive-only attribution output includes no performance conclusion label."
    test: "tests/unit/test_attribution_reset.py::test_archive_only_attribution_has_no_performance_conclusion"

Execution-Mode: heavy
Evidence:
  - tests/unit/test_attribution_reset.py::test_net_sharpe_excludes_stream_d
  - tests/unit/test_attribution_reset.py::test_archive_only_attribution_has_no_performance_conclusion
  - docs/EVIDENCE_INDEX.md row for attribution stream proof
Verifier-Focus: |
  Confirm stream d cannot enter primary metrics and archive-only outputs cannot imply validated performance.

Files:
  - src/entropy/attribution/
  - src/entropy/baseline/
  - tests/unit/test_attribution_reset.py
  - docs/EVIDENCE_INDEX.md

Context-Refs:
  - docs/core/PROTOCOL_SPEC.md
  - docs/legacy/CORE_LEGACY_SUMMARY.md#durable-boundaries

Notes: |
  This task is heavy because attribution errors can create false research confidence.

## T11: Phase-Gate Evidence Packet

Owner:      codex
Phase:      3
Type:       none
Depends-On: T07, T08, T10
Status:     done 2026-05-07

Objective: |
  Produce a reset-era phase-gate evidence packet that summarizes baseline, open gates, blocked claims, and proof artifacts without relying on old workflow state as authority.

Acceptance-Criteria:
  - id: AC-1
    description: "Phase-gate packet lists baseline, blocked claim surfaces, required human approvals, and evidence rows."
    test: "tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_contains_required_sections"
  - id: AC-2
    description: "Packet generation fails when a referenced evidence artifact is missing."
    test: "tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_fails_missing_evidence"
  - id: AC-3
    description: "Packet contains no OOS/performance, production, or capital-ready approval unless the matching gate evidence exists."
    test: "tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_blocks_unapproved_claim_labels"

Files:
  - src/entropy/evidence/
  - docs/EVIDENCE_INDEX.md
  - tests/integration/test_phase_gate_packet_reset.py

Context-Refs:
  - docs/ARCHITECTURE.md#minimum-viable-control-surface

Notes: |
  The packet may reference legacy summaries only as context, not proof.

## T12: Trader Risk Audit Bridge Contracts

Owner:      codex
Phase:      4
Type:       none
Depends-On: T05, T06, T10
Status:     done 2026-05-07

Objective: |
  Define deterministic bridge contracts for Trader Risk Audit risk policy, violation record, attribution, and report primitives that can reuse Core without opening live trading or research-claim surfaces.

Acceptance-Criteria:
  - id: AC-1
    description: "Bridge contract document lists allowed Core primitives, forbidden Core calls, schema version, and human approval boundaries."
    test: "tests/integration/test_trader_risk_bridge_contract.py::test_bridge_contract_lists_allowed_and_forbidden_surfaces"
  - id: AC-2
    description: "Risk policy and violation record bridge schemas serialize deterministically and contain no runtime LLM-owned fields."
    test: "tests/integration/test_trader_risk_bridge_contract.py::test_bridge_schemas_are_deterministic_and_no_llm_owned_fields"
  - id: AC-3
    description: "Bridge tests reject live broker, order-blocking, production, capital-ready, and OOS/performance labels."
    test: "tests/integration/test_trader_risk_bridge_contract.py::test_bridge_rejects_live_and_claim_surfaces"

Files:
  - docs/bridges/trader-risk-audit.md
  - src/entropy/bridges/
  - tests/integration/test_trader_risk_bridge_contract.py

Context-Refs:
  - ../../products/trader-risk-audit/docs/ARCHITECTURE.md
  - docs/ARCHITECTURE.md#human-approval-boundaries

Notes: |
  This is a bridge contract, not a direct product integration task.

## T13: Hypothesis Backtest Bridge Design

Owner:      codex
Phase:      4
Type:       none
Depends-On: T07, T08, T11

Objective: |
  Design the human-gated bridge from research-assist hypothesis drafts to registered, hash-bound, leakage-safe evaluation objects without enabling autonomous strategy execution.

Acceptance-Criteria:
  - id: AC-1
    description: "Bridge design requires human registration before any draft hypothesis can become an evaluation object."
    test: "tests/integration/test_hypothesis_bridge_design.py::test_hypothesis_bridge_requires_human_registration"
  - id: AC-2
    description: "Bridge design rejects AI-authored registry truth, gate decisions, metric computation, and evidence truth generation."
    test: "tests/integration/test_hypothesis_bridge_design.py::test_hypothesis_bridge_rejects_ai_owned_truth_fields"
  - id: AC-3
    description: "Bridge design records holdout, leakage, no-claim, and runtime escalation boundaries."
    test: "tests/integration/test_hypothesis_bridge_design.py::test_hypothesis_bridge_records_required_boundaries"

Files:
  - docs/bridges/hypothesis-backtest.md
  - tests/integration/test_hypothesis_bridge_design.py

Context-Refs:
  - docs/governance/research_firewall.md
  - docs/core/CHARTER.md

Notes: |
  Keep this design-only unless a later phase explicitly implements the bridge.

## T14: Reset Strategy Closure Review

Owner:      codex
Phase:      4
Type:       none
Depends-On: T11, T12, T13

Objective: |
  Close the reset implementation block with a strategy review, audit index update, and next-block recommendation grounded in current evidence.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/audit/RESET_REVIEW.md` summarizes completed reset tasks, evidence, open findings, and next recommendation."
    test: "tests/reset/test_reset_closure.py::test_reset_review_contains_required_sections"
  - id: AC-2
    description: "`docs/audit/AUDIT_INDEX.md` contains an archive row for the reset review."
    test: "tests/reset/test_reset_closure.py::test_audit_index_records_reset_review"
  - id: AC-3
    description: "`docs/CODEX_PROMPT.md` points to the next task or states reset implementation awaits human decision after T14."
    test: "tests/reset/test_reset_closure.py::test_codex_prompt_records_reset_closure_state"

Files:
  - docs/audit/RESET_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_reset_closure.py

Context-Refs:
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task does not approve holdout, live feeds, broker integration, or performance claims.
