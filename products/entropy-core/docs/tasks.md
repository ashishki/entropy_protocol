# Task Graph - Entropy Core

Version: 1.0
Last updated: 2026-05-08
Status: active roadmap task graph

---

## Phase Plan

| Phase | Name | Tasks | Delivery | Gate criteria |
|-------|------|-------|----------|---------------|
| 1 | Reset Foundation | T01-T03 | Existing package baseline, Python 3.12 tooling, product-local CI, and smoke tests. | Phase 1 audit passes; local baseline recorded; ruff/format/pyright commands known. |
| 2 | Governance Integrity | T04-T07 | Registry, governance, evidence index, and no-claim report boundaries synchronized with current code. | Append-only, human-gate, no-claim, and evidence-index checks pass. |
| 3 | Evaluation Safety | T08-T11 | Data/leakage/holdout, SimBroker, attribution, and phase-gate evidence hardening. | Heavy evidence tasks have executable tests and indexed proof. |
| 4 | Product Bridges | T12-T14 | Trader Risk Audit primitives and hypothesis/backtest bridge contracts. | Bridge tests prove no live/no-claim boundaries are preserved. |
| 5 | First Research Evidence Packet | T15-T19 | One registered, hash-bound, archive-only, leakage-checked research packet from a narrow baseline hypothesis. | Packet and review prove reproducible evidence without OOS/performance, holdout, live, production, or capital-ready claims. |
| 6 | Archive Evidence Expansion | T20-T24 | Additional archive-only, hash-bound evidence packets from distinct narrow baseline hypotheses. | Packet set demonstrates repeatable archive evidence generation without OOS/performance, holdout, live, production, or capital-ready claims. |
| 7 | Archive Reproducibility Hardening | T25-T29 | Replay and consistency checks for existing archive-only evidence packets plus roadmap evaluation rules. | Replays prove deterministic packet generation, stable hashes, no hidden holdout/live/OOS/performance surfaces, and a documented roadmap evaluation after phase close. |
| 8 | Phase-Gate Readiness Review | T30-T34 | Gap matrix and readiness packet for deciding whether the archive evidence base is sufficient to discuss holdout access. | Review identifies evidence sufficiency, missing controls, and required human approvals without opening holdout. |
| 9 | Holdout Access Protocol | T35-T39 | Design and approval protocol for controlled holdout unlock, leakage guards, and audit logging. | Holdout remains unread until explicit approval; protocol proves access can be gated, logged, and blocked by default. |
| 10 | Approved Holdout Evaluation Packet | T40-T45 | If explicitly approved, run a bounded holdout/OOS evaluation packet with no production or capital-ready claims. | OOS packet is hash-bound, leakage-checked, and reviewed; performance claims remain scoped and non-production. |
| 11 | Live-Feed Dry Run Readiness | T46-T50 | Prepare live market data ingestion checks without broker orders, exchange execution, or live capital. | Live-feed path is observable and gated; no order placement, broker integration, or capital deployment is enabled. |
| 12 | Broker Sandbox and Execution Risk Audit | T51-T56 | Sandbox-only broker/exchange integration, execution risk controls, and kill-switch audit. | Sandbox execution is isolated; live capital remains blocked; risk controls and audit logs are mandatory. |
| 13 | Production and Capital Gate | T57-T64 | Final human-governed production/capital readiness review. | Production/capital-ready labels require explicit gate approval, full evidence packet, risk signoff, and rollback plan. |

## Roadmap Governance

The roadmap sets direction for autonomous AI development. The current active task is open for execution, and future phases are planned until roadmap evaluation promotes or rewrites them.

Phase boundaries are autonomous rollover points, not stop points. After every active phase closes, run deep review, fix actionable findings, validate, evaluate the roadmap, rewrite future phases/tasks when useful, open the next logical active phase, and continue automatically. The evaluation must:

- summarize what the completed phase changed;
- list evidence that strengthened or weakened the current roadmap;
- keep real external side effects, live capital actions, live broker/exchange execution, and credentialed production deployment blocked unless a future local protocol explicitly replaces them with safe dry-run/sandbox behavior;
- either keep the next planned phase, modify future planned phases, or open a better next active phase;
- update `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, and the evidence/audit indexes when applicable.

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
Status:     done 2026-05-07

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
Status:     done 2026-05-07

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

## T15: First Research Candidate Registration Packet

Owner:      codex
Phase:      5
Type:       none
Depends-On: T13, T14
Status:     done 2026-05-07

Objective: |
  Select one narrow, falsifiable archive-only baseline hypothesis and encode a preregistration packet that can become a registered evaluation object only through explicit human approval and hash binding.

Acceptance-Criteria:
  - id: AC-1
    description: "The first research candidate packet records hypothesis text, hypothesis family, scope, frozen parameters, no-claim labels, and required human registration gate."
    test: "tests/integration/test_first_research_packet.py::test_candidate_packet_records_registration_requirements"
  - id: AC-2
    description: "Candidate packet serialization is deterministic and includes dataset/code/policy/parameter hash placeholders before evaluation."
    test: "tests/integration/test_first_research_packet.py::test_candidate_packet_serializes_deterministically"
  - id: AC-3
    description: "Candidate packet cannot request holdout, OOS/performance, production, capital-ready, live-feed, or broker/exchange surfaces."
    test: "tests/integration/test_first_research_packet.py::test_candidate_packet_rejects_claim_and_live_surfaces"

Files:
  - src/entropy/research/
  - docs/research/first-packet/CANDIDATE_PACKET.md
  - tests/integration/test_first_research_packet.py

Context-Refs:
  - docs/governance/research_firewall.md
  - docs/governance/experiment_readiness_gate.md
  - docs/governance/hypothesis_families.md
  - docs/bridges/hypothesis-backtest.md

Notes: |
  This task creates a candidate packet only. It does not run evaluation, inspect holdout, or claim performance.

## T16: Archive Dataset Manifest and Hash Binding

Owner:      codex
Phase:      5
Type:       none
Depends-On: T08, T15
Status:     done 2026-05-07

Objective: |
  Bind the first research candidate to an archive-only dataset manifest with deterministic dataset hashes and explicit holdout exclusion.

Acceptance-Criteria:
  - id: AC-1
    description: "Dataset manifest hash is deterministic across row order and path ordering."
    test: "tests/integration/test_first_research_packet.py::test_archive_dataset_manifest_hash_is_deterministic"
  - id: AC-2
    description: "Manifest records formation/evaluation scope and explicitly excludes holdout reads."
    test: "tests/integration/test_first_research_packet.py::test_archive_dataset_manifest_excludes_holdout"
  - id: AC-3
    description: "Dataset binding updates the candidate packet without changing hypothesis text, family, or frozen parameters."
    test: "tests/integration/test_first_research_packet.py::test_dataset_binding_preserves_registered_candidate_fields"

Files:
  - src/entropy/research/
  - src/entropy/data/
  - src/entropy/hashing/
  - docs/research/first-packet/DATASET_MANIFEST.md
  - tests/integration/test_first_research_packet.py

Context-Refs:
  - docs/core/PROTOCOL_SPEC.md
  - docs/IMPLEMENTATION_CONTRACT.md#leakage-and-holdout-boundary

Notes: |
  Use archive/local fixtures only. Do not add provider activation, live feeds, or holdout access.

## T17: Archive Evaluation Harness Wiring

Owner:      codex
Phase:      5
Type:       none
Depends-On: T09, T10, T15, T16
Status:     done 2026-05-07

Objective: |
  Wire the first candidate through an archive-only evaluation path that records leakage checks, SimBroker fills/costs, and attribution streams without opening OOS/performance claims.

Acceptance-Criteria:
  - id: AC-1
    description: "Evaluation harness refuses to run unless candidate, dataset hash, code hash, policy hash, and parameter hash are present."
    test: "tests/integration/test_first_research_packet.py::test_archive_evaluation_requires_all_hash_bindings"
  - id: AC-2
    description: "Evaluation output includes leakage status, SimBroker fill log identifiers, and separated attribution streams."
    test: "tests/integration/test_first_research_packet.py::test_archive_evaluation_outputs_required_evidence_surfaces"
  - id: AC-3
    description: "Evaluation output serializes no-claim labels and no OOS/performance conclusion."
    test: "tests/integration/test_first_research_packet.py::test_archive_evaluation_output_remains_no_claim"

Execution-Mode: heavy
Evidence:
  - tests/integration/test_first_research_packet.py::test_archive_evaluation_output_remains_no_claim
  - docs/EVIDENCE_INDEX.md row for first archive evaluation harness proof
Verifier-Focus: |
  Confirm the first archive evaluation path cannot silently become OOS/performance evidence.

Files:
  - src/entropy/research/
  - src/entropy/walkforward/
  - src/entropy/simbroker/
  - src/entropy/attribution/
  - tests/integration/test_first_research_packet.py
  - docs/EVIDENCE_INDEX.md

Context-Refs:
  - docs/core/PROTOCOL_SPEC.md
  - docs/audit/PHASE3_REVIEW.md

Notes: |
  Heavy task because this is the first end-to-end research evidence path after reset.

## T18: First Research Evidence Packet

Owner:      codex
Phase:      5
Type:       none
Depends-On: T11, T17
Status:     done 2026-05-07

Objective: |
  Generate the first deterministic archive-only research evidence packet with candidate, hashes, leakage, SimBroker, attribution, no-claim labels, and evidence-index proof.

Acceptance-Criteria:
  - id: AC-1
    description: "Evidence packet contains candidate id, dataset/code/policy/parameter hashes, leakage status, SimBroker evidence, attribution streams, and no-claim labels."
    test: "tests/integration/test_first_research_packet.py::test_research_packet_contains_required_sections"
  - id: AC-2
    description: "Evidence packet generation fails when any referenced artifact or required hash is missing."
    test: "tests/integration/test_first_research_packet.py::test_research_packet_fails_missing_artifact_or_hash"
  - id: AC-3
    description: "Evidence packet contains no holdout unlock, OOS/performance approval, production approval, or capital-ready approval."
    test: "tests/integration/test_first_research_packet.py::test_research_packet_blocks_claim_approvals"

Execution-Mode: heavy
Evidence:
  - tests/integration/test_first_research_packet.py::test_research_packet_contains_required_sections
  - docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md
  - docs/EVIDENCE_INDEX.md row for first research packet proof
Verifier-Focus: |
  Confirm the packet is a concrete research artifact but remains no-claim and archive-only.

Files:
  - src/entropy/evidence/
  - src/entropy/research/
  - docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md
  - docs/EVIDENCE_INDEX.md
  - tests/integration/test_first_research_packet.py

Context-Refs:
  - docs/audit/RESET_REVIEW.md
  - docs/EVIDENCE_INDEX.md

Notes: |
  The packet may be useful research evidence, but it does not approve phase exit, live use, or performance claims.

## T19: First Research Packet Review

Owner:      codex
Phase:      5
Type:       none
Depends-On: T18
Status:     done 2026-05-07

Objective: |
  Review the first research evidence packet, record open findings, and recommend the next human decision without escalating claims.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md` summarizes candidate, evidence, validation, limitations, open findings, and next recommendation."
    test: "tests/reset/test_first_research_packet_review.py::test_first_research_packet_review_contains_required_sections"
  - id: AC-2
    description: "Review records that holdout, live feeds, broker integration, production, capital-ready, and OOS/performance claims remain unapproved."
    test: "tests/reset/test_first_research_packet_review.py::test_first_research_packet_review_preserves_boundaries"
  - id: AC-3
    description: "`docs/CODEX_PROMPT.md` records the completed first research packet state and next human decision point."
    test: "tests/reset/test_first_research_packet_review.py::test_codex_prompt_records_first_packet_review_state"

Files:
  - docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_first_research_packet_review.py

Context-Refs:
  - docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md
  - docs/audit/RESET_REVIEW.md

Notes: |
  Stop after this review unless a human explicitly opens the next research block or approves a gate discussion.

## T20: Second Research Candidate Registration Packet

Owner:      codex
Phase:      6
Type:       none
Depends-On: T19
Status:     done 2026-05-07

Objective: |
  Select a second narrow, falsifiable archive-only baseline hypothesis from a different canonical family and encode a preregistration packet with the same no-claim, human-gated, hash-placeholder boundaries as the first packet.

Acceptance-Criteria:
  - id: AC-1
    description: "The second candidate packet records candidate id, hypothesis text, distinct hypothesis family, scope, frozen parameters, no-claim labels, and required human registration gate."
    test: "tests/integration/test_second_research_packet.py::test_second_candidate_packet_records_registration_requirements"
  - id: AC-2
    description: "Second candidate packet serialization is deterministic and includes dataset/code/policy/parameter hash placeholders before evaluation."
    test: "tests/integration/test_second_research_packet.py::test_second_candidate_packet_serializes_deterministically"
  - id: AC-3
    description: "Second candidate packet cannot request holdout, OOS/performance, production, capital-ready, live-feed, or broker/exchange surfaces."
    test: "tests/integration/test_second_research_packet.py::test_second_candidate_packet_rejects_claim_and_live_surfaces"

Files:
  - src/entropy/research/
  - docs/research/second-packet/CANDIDATE_PACKET.md
  - tests/integration/test_second_research_packet.py

Context-Refs:
  - docs/governance/research_firewall.md
  - docs/governance/experiment_readiness_gate.md
  - docs/governance/hypothesis_families.md
  - docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md

Notes: |
  This task opens more archive-only evidence. It does not approve holdout, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate claims.

## T21: Second Archive Dataset Manifest and Hash Binding

Owner:      codex
Phase:      6
Type:       none
Depends-On: T16, T20
Status:     done 2026-05-07

Objective: |
  Bind the second research candidate to an archive-only dataset manifest with deterministic dataset hashes and explicit holdout exclusion.

Acceptance-Criteria:
  - id: AC-1
    description: "Second dataset manifest hash is deterministic across row order and path ordering."
    test: "tests/integration/test_second_research_packet.py::test_second_archive_dataset_manifest_hash_is_deterministic"
  - id: AC-2
    description: "Second manifest records formation/evaluation scope and explicitly excludes holdout reads."
    test: "tests/integration/test_second_research_packet.py::test_second_archive_dataset_manifest_excludes_holdout"
  - id: AC-3
    description: "Second dataset binding updates the candidate packet without changing hypothesis text, family, or frozen parameters."
    test: "tests/integration/test_second_research_packet.py::test_second_dataset_binding_preserves_registered_candidate_fields"

Files:
  - src/entropy/research/
  - docs/research/second-packet/DATASET_MANIFEST.md
  - tests/integration/test_second_research_packet.py

Context-Refs:
  - docs/core/PROTOCOL_SPEC.md
  - docs/IMPLEMENTATION_CONTRACT.md#leakage-and-holdout-boundary

Notes: |
  Use archive/local fixtures only. Do not add provider activation, live feeds, or holdout access.

## T22: Second Archive Evaluation Harness Wiring

Owner:      codex
Phase:      6
Type:       none
Depends-On: T17, T20, T21
Status:     done 2026-05-07

Objective: |
  Wire the second candidate through the archive-only evaluation path and prove the reusable harness still records leakage, SimBroker, attribution, and no-claim outputs.

Acceptance-Criteria:
  - id: AC-1
    description: "Second evaluation refuses to run unless candidate, dataset hash, code hash, policy hash, and parameter hash are present."
    test: "tests/integration/test_second_research_packet.py::test_second_archive_evaluation_requires_all_hash_bindings"
  - id: AC-2
    description: "Second evaluation output includes leakage status, SimBroker fill log identifiers, and separated attribution streams."
    test: "tests/integration/test_second_research_packet.py::test_second_archive_evaluation_outputs_required_evidence_surfaces"
  - id: AC-3
    description: "Second evaluation output serializes no-claim labels and no OOS/performance conclusion."
    test: "tests/integration/test_second_research_packet.py::test_second_archive_evaluation_output_remains_no_claim"

Execution-Mode: heavy
Evidence:
  - tests/integration/test_second_research_packet.py::test_second_archive_evaluation_output_remains_no_claim
  - docs/EVIDENCE_INDEX.md row for second archive evaluation harness proof
Verifier-Focus: |
  Confirm repeat use of the archive evaluation path cannot silently become OOS/performance evidence.

Files:
  - src/entropy/research/
  - docs/EVIDENCE_INDEX.md
  - tests/integration/test_second_research_packet.py

Context-Refs:
  - docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md
  - docs/audit/PHASE3_REVIEW.md

Notes: |
  Heavy task because it expands evidence generation beyond the first candidate while preserving no-claim boundaries.

## T23: Second Research Evidence Packet

Owner:      codex
Phase:      6
Type:       none
Depends-On: T18, T22
Status:     done 2026-05-07

Objective: |
  Generate the second deterministic archive-only research evidence packet with candidate, hashes, leakage, SimBroker, attribution, no-claim labels, and evidence-index proof.

Acceptance-Criteria:
  - id: AC-1
    description: "Second evidence packet contains candidate id, dataset/code/policy/parameter hashes, leakage status, SimBroker evidence, attribution streams, and no-claim labels."
    test: "tests/integration/test_second_research_packet.py::test_second_research_packet_contains_required_sections"
  - id: AC-2
    description: "Second evidence packet generation fails when any referenced artifact or required hash is missing."
    test: "tests/integration/test_second_research_packet.py::test_second_research_packet_fails_missing_artifact_or_hash"
  - id: AC-3
    description: "Second evidence packet contains no holdout unlock, OOS/performance approval, production approval, or capital-ready approval."
    test: "tests/integration/test_second_research_packet.py::test_second_research_packet_blocks_claim_approvals"

Execution-Mode: heavy
Evidence:
  - tests/integration/test_second_research_packet.py::test_second_research_packet_contains_required_sections
  - docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md
  - docs/EVIDENCE_INDEX.md row for second research packet proof
Verifier-Focus: |
  Confirm the second packet adds evidence without approving phase exit, live use, or performance claims.

Files:
  - src/entropy/evidence/
  - src/entropy/research/
  - docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md
  - docs/EVIDENCE_INDEX.md
  - tests/integration/test_second_research_packet.py

Context-Refs:
  - docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md
  - docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md

Notes: |
  The packet may be useful archive evidence, but it does not approve phase exit, live use, or performance claims.

## T24: Archive Evidence Expansion Review

Owner:      codex
Phase:      6
Type:       none
Depends-On: T23
Status:     done 2026-05-07

Objective: |
  Review the expanded archive evidence set, record open findings, and recommend the next human decision without escalating claims.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md` summarizes packet set, evidence, validation, limitations, open findings, and next recommendation."
    test: "tests/reset/test_archive_evidence_expansion_review.py::test_archive_evidence_expansion_review_contains_required_sections"
  - id: AC-2
    description: "Review records that holdout, live feeds, broker integration, production, capital-ready, and OOS/performance claims remain unapproved."
    test: "tests/reset/test_archive_evidence_expansion_review.py::test_archive_evidence_expansion_review_preserves_boundaries"
  - id: AC-3
    description: "`docs/CODEX_PROMPT.md` records the completed archive evidence expansion state and next human decision point."
    test: "tests/reset/test_archive_evidence_expansion_review.py::test_codex_prompt_records_archive_expansion_review_state"

Files:
  - docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_archive_evidence_expansion_review.py

Context-Refs:
  - docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md
  - docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md

Notes: |
  Stop after this review unless a human explicitly opens the next research block or approves a gate discussion.

## T25: Roadmap Governance Contract

Owner:      codex
Phase:      7
Type:       none
Depends-On: T24
Status:     done 2026-05-08

Objective: |
  Record the forward roadmap and the autonomous phase rollover rule so future agents can adapt planned phases after each completed active phase, open the next logical phase, and continue without waiting for a human at every boundary.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/tasks.md` lists planned phases 7 through 13 and records that autonomous phase rollover opens the next logical active phase after roadmap evaluation."
    test: "tests/reset/test_roadmap_governance.py::test_tasks_records_planned_roadmap_and_active_phase"
  - id: AC-2
    description: "Roadmap governance requires deep review, fixes, validation, roadmap evaluation, roadmap rewrite when useful, next active phase opening, and automatic continuation after every active phase."
    test: "tests/reset/test_roadmap_governance.py::test_tasks_records_dynamic_roadmap_evaluation_rule"
  - id: AC-3
    description: "`CODEX_LOOP.md`, `docs/CODEX_PROMPT.md`, and `PHASE_HANDOFF.md` record autonomous continuation while blocking real external side effects, live capital actions, live broker/exchange execution, and credentialed production deployment."
    test: "tests/reset/test_roadmap_governance.py::test_prompt_and_handoff_record_phase7_boundaries"

Files:
  - CODEX_LOOP.md
  - docs/tasks.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md
  - tests/reset/test_roadmap_governance.py

Context-Refs:
  - docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md
  - docs/EVIDENCE_INDEX.md

Notes: |
  This opens Phase 7 only. Phases 8 through 13 are planned roadmap entries, not approvals.

## T26: Archive Packet Replay Contract

Owner:      codex
Phase:      7
Type:       none
Depends-On: T25
Status:     done 2026-05-08

Objective: |
  Add deterministic replay checks for existing archive-only evidence packets so regenerated packet content and referenced artifacts remain stable.

Acceptance-Criteria:
  - id: AC-1
    description: "Replay checks regenerate first and second archive evidence packets from current fixtures and compare deterministic content or hashes."
    test: "tests/integration/test_archive_replay.py::test_archive_packet_replay_is_deterministic"
  - id: AC-2
    description: "Replay checks fail when a required packet artifact, dataset manifest, or hash binding is missing."
    test: "tests/integration/test_archive_replay.py::test_archive_packet_replay_requires_all_artifacts"
  - id: AC-3
    description: "Replay output remains archive-only and contains no holdout, OOS/performance, live, production, or capital-ready approval."
    test: "tests/integration/test_archive_replay.py::test_archive_packet_replay_preserves_no_claim_boundary"

Files:
  - src/entropy/research/
  - src/entropy/evidence/
  - tests/integration/test_archive_replay.py
  - docs/EVIDENCE_INDEX.md

Context-Refs:
  - docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md
  - docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md

Notes: |
  This task proves repeatability only. It does not compare profitability, unlock holdout, or create OOS/performance claims.

## T27: Evidence Hash Reproducibility Matrix

Owner:      codex
Phase:      7
Type:       none
Depends-On: T26
Status:     done 2026-05-08

Objective: |
  Build a matrix of candidate, dataset, code, policy, parameter, and artifact hashes across existing archive evidence packets.

Acceptance-Criteria:
  - id: AC-1
    description: "A reproducibility matrix lists the required hash categories for first and second archive evidence packets."
    test: "tests/reset/test_reproducibility_matrix.py::test_reproducibility_matrix_lists_required_hashes"
  - id: AC-2
    description: "Matrix validation fails when any required hash category is unresolved, duplicated incorrectly, or missing from a packet row."
    test: "tests/reset/test_reproducibility_matrix.py::test_reproducibility_matrix_rejects_missing_hashes"
  - id: AC-3
    description: "The evidence index references the reproducibility matrix and its validation tests."
    test: "tests/reset/test_reproducibility_matrix.py::test_evidence_index_records_reproducibility_matrix"

Files:
  - docs/research/REPRODUCIBILITY_MATRIX.md
  - docs/EVIDENCE_INDEX.md
  - tests/reset/test_reproducibility_matrix.py

Context-Refs:
  - docs/research/first-packet/DATASET_MANIFEST.md
  - docs/research/second-packet/DATASET_MANIFEST.md

Notes: |
  The matrix is evidence bookkeeping. It must not rank hypotheses or imply performance quality.

## T28: No-Claim Surface Regression Sweep

Owner:      codex
Phase:      7
Type:       none
Depends-On: T27
Status:     done 2026-05-08

Objective: |
  Sweep archive evidence, bridge, phase-gate, and reporting surfaces to prove no completed packet or roadmap entry silently opens restricted claim paths.

Acceptance-Criteria:
  - id: AC-1
    description: "Regression tests scan active docs and generated packet surfaces for disallowed holdout/live/broker/production/capital-ready/OOS/performance approval language."
    test: "tests/reset/test_no_claim_roadmap_sweep.py::test_active_docs_do_not_open_restricted_surfaces"
  - id: AC-2
    description: "Phase plan entries for phases 8 through 13 are marked as planned roadmap, not active approvals."
    test: "tests/reset/test_no_claim_roadmap_sweep.py::test_future_phases_are_not_approvals"
  - id: AC-3
    description: "The sweep preserves the existing explicit boundary language in `docs/CODEX_PROMPT.md` and `PHASE_HANDOFF.md`."
    test: "tests/reset/test_no_claim_roadmap_sweep.py::test_prompt_and_handoff_preserve_boundaries"

Files:
  - docs/tasks.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - tests/reset/test_no_claim_roadmap_sweep.py

Context-Refs:
  - docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md
  - docs/bridges/hypothesis-backtest.md

Notes: |
  This is a safety task before any readiness discussion.

## T29: Archive Reproducibility Hardening Review

Owner:      codex
Phase:      7
Type:       none
Depends-On: T28
Status:     active

Objective: |
  Review Phase 7 reproducibility hardening, record open findings, and run the first roadmap evaluation before any next phase is opened.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md` summarizes replay evidence, reproducibility matrix, no-claim sweep, validation, limitations, open findings, and next recommendation."
    test: "tests/reset/test_archive_reproducibility_review.py::test_archive_reproducibility_review_contains_required_sections"
  - id: AC-2
    description: "Review records a roadmap evaluation that either keeps, modifies, or blocks the planned Phase 8."
    test: "tests/reset/test_archive_reproducibility_review.py::test_archive_reproducibility_review_records_roadmap_evaluation"
  - id: AC-3
    description: "`docs/CODEX_PROMPT.md` records completion through T29 and returns to a human decision point before any next phase opens."
    test: "tests/reset/test_archive_reproducibility_review.py::test_codex_prompt_records_phase7_review_state"

Files:
  - docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_archive_reproducibility_review.py

Context-Refs:
  - docs/research/REPRODUCIBILITY_MATRIX.md
  - docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md

Notes: |
  Stop after this review. Phase 8 remains planned only until a human explicitly opens it after roadmap evaluation.
