# Task Graph - Entropy Core

Version: 1.2
Last updated: 2026-05-12
Status: Core V1 checkpoint complete through T122. Automatic roadmap expansion is stopped until a human approves a Core V2 roadmap. Phase 14 replay tasks T66-T68 remain deferred unless explicitly reactivated by a human decision.

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
| 10 | Holdout Approval Decision Packet | T40-T45 | Assemble no-read approval request and decision evidence before any future holdout access approval could be considered. | Packet proves explicit approval is absent or bounded, non-approval sources are rejected, and holdout remains unread unless a future human approval event and controls exist. |
| 11 | Live-Feed Dry Run Readiness | T46-T50 | Prepare live market data ingestion checks without broker orders, exchange execution, or live capital. | Live-feed path is observable and gated; no order placement, broker integration, or capital deployment is enabled. |
| 12 | Broker Sandbox and Execution Risk Audit | T51-T56 | Sandbox-only broker/exchange integration, execution risk controls, and kill-switch audit. | Sandbox execution is isolated; live capital remains blocked; risk controls and audit logs are mandatory. |
| 13 | Product Hypothesis Confirmation Decision | T57-T62 | Local-only approval decision work for defining the safest next validation step toward product hypothesis confirmation. | No production, capital, live order, broker/exchange execution, production credential, or holdout access path opens without explicit future human approval and a bounded task contract. |
| 14 | Local Broker Sandbox No-Capital Replay Extension | T63-T68 | Execute the approved local/no-effect replay extension against deterministic SimBroker fixture scenarios and record evidence deltas. | Replay evidence is hash-bound, deterministic, no-effect, and cannot be interpreted as production, capital-ready, live, holdout, or OOS/performance confirmation. |
| 15 | Artifact Support Mode | T69-T74 | Define shared artifact contracts, report validity checklist, reproducibility checklist, product bridge notes, internal review templates, and Core freeze/platformization gate. | Core improves Trader/Signal artifact trust without becoming the public product or opening live, holdout, OOS, SDK, hosted service, or execution scope. |
| 16 | Executable Artifact Validation | T75-T78 | Turn the Phase 15 artifact contract into Pydantic schemas, loaders, CLI validation, fixtures, and review evidence. | `entropy artifact validate` deterministically accepts valid artifacts and rejects invalid claim/state/hash/field combinations. |
| 17 | Artifact Registry | T79-T82 | Register validated artifacts as append-only governed records. | Artifacts have stable ids, validation status, metadata, history, and corrections without mutation. |
| 18 | Reproducibility Runner | T83-T86 | Compare reruns, hashes, and declared nondeterminism. | Core classifies exact, materially equivalent, partial, declared non-reproducible, and failed reproduction states. |
| 19 | Evidence Pipeline | T87-T90 | Build machine-readable evidence packets from validation, registry, and reproducibility outputs. | Core emits inspectable evidence packets without requiring long-form docs. |
| 20 | Product Bridge Profiles | T91-T94 | Add narrow validation overlays for product-shaped artifacts while keeping product logic outside Core. | Core validates product profiles without owning Trader or Signal runtime behavior. |
| 21 | Governance State Machine | T95-T98 | Add deterministic artifact state transitions and approval events. | Unsafe transitions are blocked and state history is append-only. |
| 22 | Research Evaluation Integration | T99-T102 | Bind research/evaluation outputs into the artifact governance model. | Research packets can be validated as no-claim governed artifacts without opening holdout/OOS/live scope. |
| 23 | Storage And Audit Backend | T103-T106 | Add durable metadata and artifact-store abstractions. | Postgres metadata and filesystem/object-store boundaries are ready without SaaS scope. |
| 24 | Internal API And Job Boundary | T107-T110 | Define optional internal API and job abstractions after CLI behavior is stable. | Validation can run as idempotent internal jobs without public service claims. |
| 25 | CAF Decision Primitives | T111-T114 | Add Capital Allocation Framework decision, risk, and rationale artifact schemas. | Core can represent allocation decisions as governed evidence without executing capital. |
| 26 | Enterprise Audit Readiness | T115-T118 | Add exportable lineage, audit bundles, data classification, and review-role models. | Core can produce serious audit packages without claiming external certification. |
| 27 | Core V1 Productization | T119-T122 | Stabilize CLI, schemas, docs, examples, runbooks, and migration notes. | Core is a documented, tested internal product kernel ready for v2 planning. |

## Roadmap Governance

The roadmap sets direction for autonomous AI development. The current active task is open for execution, and future phases are planned until roadmap evaluation promotes or rewrites them.

Phase boundaries are autonomous rollover points, not stop points. After every active phase closes, run deep review, fix actionable findings, validate, evaluate the roadmap, rewrite future phases/tasks when useful, open the next logical active phase, and continue automatically. The evaluation must:

- summarize what the completed phase changed;
- list evidence that strengthened or weakened the current roadmap;
- keep real external side effects, live capital actions, live broker/exchange execution, and credentialed production deployment blocked unless a future local protocol explicitly replaces them with safe dry-run/sandbox behavior;
- either keep the next planned phase, modify future planned phases, or open a better next active phase;
- update `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, and the evidence/audit indexes when applicable.

## Artifact Support Priority Override

As of 2026-05-11, the operator confirmed the next portfolio need is real
artifact validation for Trader Risk Audit and Signal Analytics Sandbox. Core's
active role is now internal support for artifact validity, reproducibility, and
claim safety.

T66-T68 remain in the graph for the old local replay extension but are deferred.
Do not continue replay, live, broker/exchange, holdout, OOS, public SDK, hosted
service, or generic platform work unless a later explicit human decision
reactivates that path. During Phase 15 the active Core task was T69; that mode
is now closed through T74 and superseded by the executable Core roadmap override
below.

## Executable Core Roadmap Override

As of 2026-05-12, the operator clarified that Entropy Core is the long-lived
protocol kernel, while Trader Risk Audit and Signal Analytics Sandbox remain
separate commercial product workspaces. Core may use adjacent product artifacts
as external use-case shapes, but must not absorb product-specific report logic.

The next Core priority is not more artifact-support prose. The next priority is
an executable trust layer:

```text
artifact -> validation -> registry -> reproducibility -> evidence -> governance
```

The 12 month roadmap lives in `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`. The AI
development loop rules live in `docs/AI_LOOP_OPERATING_MODEL.md`.

The current active Core task is none. T75-T122 are complete. Automatic roadmap
expansion is stopped until a human approves a Core V2 roadmap.

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
Status:     done 2026-05-08

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
    description: "`docs/CODEX_PROMPT.md` records completion through T29 and opens Phase 8 with T30 active while preserving all blocked approval boundaries."
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
  This review is a phase boundary. Continue automatically after roadmap evaluation unless a blocker is found.

## T30: Archive Evidence Sufficiency Gap Matrix

Owner:      codex
Phase:      8
Type:       none
Depends-On: T29
Status:     done 2026-05-08

Objective: |
  Build a readiness gap matrix that maps the current archive evidence base to the controls required before any human-approved phase-gate discussion.

Acceptance-Criteria:
  - id: AC-1
    description: "Gap matrix lists replay, reproducibility, no-claim, governance, leakage, holdout, and review controls with evidence status."
    test: "tests/reset/test_phase_gate_readiness_gap_matrix.py::test_gap_matrix_lists_required_controls"
  - id: AC-2
    description: "Matrix marks holdout, OOS/performance, live, broker/exchange, production, capital-ready, and phase-gate approvals as blocked."
    test: "tests/reset/test_phase_gate_readiness_gap_matrix.py::test_gap_matrix_preserves_blocked_boundaries"
  - id: AC-3
    description: "Evidence index references the gap matrix and validation tests."
    test: "tests/reset/test_phase_gate_readiness_gap_matrix.py::test_evidence_index_records_gap_matrix"

Files:
  - docs/readiness/PHASE_GATE_GAP_MATRIX.md
  - docs/EVIDENCE_INDEX.md
  - tests/reset/test_phase_gate_readiness_gap_matrix.py

Context-Refs:
  - docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md
  - docs/research/REPRODUCIBILITY_MATRIX.md

Notes: |
  This task is readiness analysis only. It must not request holdout access or approve any claim surface.

## T31: Phase-Gate Readiness Packet Scaffold

Owner:      codex
Phase:      8
Type:       none
Depends-On: T30
Status:     done 2026-05-09

Objective: |
  Create a readiness packet scaffold that assembles current evidence, missing controls, limitations, and explicit non-approval boundaries for a future human phase-gate discussion.

Acceptance-Criteria:
  - id: AC-1
    description: "Readiness packet scaffold includes evidence summary, missing controls, limitations, and required human approvals."
    test: "tests/reset/test_phase_gate_readiness_packet.py::test_readiness_packet_contains_required_sections"
  - id: AC-2
    description: "Readiness packet rejects any holdout unlock, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate approval label."
    test: "tests/reset/test_phase_gate_readiness_packet.py::test_readiness_packet_rejects_approval_labels"
  - id: AC-3
    description: "Packet references the Phase 8 gap matrix and Phase 7 review."
    test: "tests/reset/test_phase_gate_readiness_packet.py::test_readiness_packet_references_gap_matrix_and_review"

Files:
  - docs/readiness/PHASE_GATE_READINESS_PACKET.md
  - tests/reset/test_phase_gate_readiness_packet.py

Context-Refs:
  - docs/readiness/PHASE_GATE_GAP_MATRIX.md
  - docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md

Notes: |
  Scaffold means no approval. The packet is input to a future review only.

## T32: Approval Boundary Checklist

Owner:      codex
Phase:      8
Type:       none
Depends-On: T31
Status:     done 2026-05-09

Objective: |
  Record a checklist of explicit human approvals and evidence prerequisites that would be required before holdout, phase-gate, or claim-surface work could be considered.

Acceptance-Criteria:
  - id: AC-1
    description: "Checklist lists every required approval boundary and the current blocked status."
    test: "tests/reset/test_approval_boundary_checklist.py::test_checklist_lists_required_boundaries"
  - id: AC-2
    description: "Checklist forbids treating roadmap phases, readiness docs, or archive evidence as approval."
    test: "tests/reset/test_approval_boundary_checklist.py::test_checklist_rejects_implicit_approval_sources"
  - id: AC-3
    description: "`docs/CODEX_PROMPT.md` and `PHASE_HANDOFF.md` preserve the same blocked boundary language."
    test: "tests/reset/test_approval_boundary_checklist.py::test_prompt_and_handoff_match_boundary_checklist"

Files:
  - docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - tests/reset/test_approval_boundary_checklist.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions
  - docs/ARCHITECTURE.md#human-approval-boundaries

Notes: |
  The checklist may identify prerequisites only. It must not grant approval.

## T33: Readiness No-Holdout Dry Run

Owner:      codex
Phase:      8
Type:       none
Depends-On: T32
Status:     done 2026-05-09

Objective: |
  Add a local dry-run proof that readiness review can assemble evidence without reading or unlocking holdout data.

Acceptance-Criteria:
  - id: AC-1
    description: "Dry-run test assembles readiness evidence from archive artifacts without opening a holdout path."
    test: "tests/reset/test_readiness_no_holdout_dry_run.py::test_readiness_dry_run_uses_archive_only_artifacts"
  - id: AC-2
    description: "Dry-run fails if any holdout, live, broker/exchange, production, capital-ready, phase-gate, or OOS/performance approval flag is present."
    test: "tests/reset/test_readiness_no_holdout_dry_run.py::test_readiness_dry_run_rejects_restricted_flags"
  - id: AC-3
    description: "Dry-run output records limitations and missing prerequisites instead of claim conclusions."
    test: "tests/reset/test_readiness_no_holdout_dry_run.py::test_readiness_dry_run_records_limitations"

Files:
  - tests/reset/test_readiness_no_holdout_dry_run.py
  - docs/readiness/PHASE_GATE_READINESS_PACKET.md

Context-Refs:
  - docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md
  - docs/readiness/PHASE_GATE_READINESS_PACKET.md

Notes: |
  This is local dry-run validation only. No holdout path may be read.

## T34: Phase-Gate Readiness Review

Owner:      codex
Phase:      8
Type:       none
Depends-On: T33
Status:     done 2026-05-09

Objective: |
  Review Phase 8 readiness artifacts, record findings, evaluate whether the roadmap should proceed to a holdout access protocol, and preserve blocked boundaries unless the roadmap evaluation identifies a safer next phase.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/audit/PHASE_GATE_READINESS_REVIEW.md` summarizes gap matrix, readiness packet, approval checklist, dry-run evidence, validation, limitations, findings, and roadmap evaluation."
    test: "tests/reset/test_phase_gate_readiness_review.py::test_phase_gate_readiness_review_contains_required_sections"
  - id: AC-2
    description: "Review either keeps, modifies, or blocks the planned Holdout Access Protocol phase."
    test: "tests/reset/test_phase_gate_readiness_review.py::test_phase_gate_readiness_review_records_roadmap_evaluation"
  - id: AC-3
    description: "Audit index and prompt record Phase 8 completion and the next active task selected by roadmap evaluation."
    test: "tests/reset/test_phase_gate_readiness_review.py::test_phase_gate_readiness_review_updates_state"

Files:
  - docs/audit/PHASE_GATE_READINESS_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_phase_gate_readiness_review.py

Context-Refs:
  - docs/readiness/PHASE_GATE_GAP_MATRIX.md
  - docs/readiness/PHASE_GATE_READINESS_PACKET.md
  - docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md

Notes: |
  This is a phase-boundary review. Continue automatically after roadmap evaluation unless a blocker is found.

## T35: Holdout Access Protocol Deny-By-Default Contract

Owner:      codex
Phase:      9
Type:       none
Depends-On: T34
Status:     done 2026-05-09

Objective: |
  Define a local holdout access protocol scaffold that is denied by default and cannot open or read holdout paths without explicit future human approval records.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md` records denied-by-default states, required approvals, allowed local-only operations, and forbidden holdout read/unlock actions."
    test: "tests/reset/test_holdout_access_protocol.py::test_holdout_protocol_records_denied_by_default_contract"
  - id: AC-2
    description: "The protocol rejects treating roadmap phases, review recommendations, passing tests, or readiness artifacts as holdout approval."
    test: "tests/reset/test_holdout_access_protocol.py::test_holdout_protocol_rejects_implicit_approval_sources"
  - id: AC-3
    description: "Prompt and handoff record Phase 9 as protocol-only with holdout read/unlock still blocked."
    test: "tests/reset/test_holdout_access_protocol.py::test_prompt_and_handoff_record_protocol_only_phase"

Files:
  - docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - tests/reset/test_holdout_access_protocol.py

Context-Refs:
  - docs/audit/PHASE_GATE_READINESS_REVIEW.md
  - docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md
  - docs/readiness/PHASE_GATE_READINESS_PACKET.md

Notes: |
  No holdout path may be opened or read. This task defines protocol scaffolding only.

## T36: Holdout Approval Event Schema Contract

Owner:      codex
Phase:      9
Type:       none
Depends-On: T35
Status:     done 2026-05-09

Objective: |
  Define the local schema for explicit human holdout approval events without creating or implying any approval.

Acceptance-Criteria:
  - id: AC-1
    description: "Schema requires approver identity, approval scope, candidate/evidence hashes, expiry, revocation state, and audit metadata."
    test: "tests/reset/test_holdout_approval_event_schema.py::test_holdout_approval_event_schema_requires_governance_fields"
  - id: AC-2
    description: "Schema fixtures reject generated, inferred, expired, revoked, or incomplete approval events."
    test: "tests/reset/test_holdout_approval_event_schema.py::test_holdout_approval_event_schema_rejects_invalid_approval_events"
  - id: AC-3
    description: "State docs preserve that no approval event currently exists."
    test: "tests/reset/test_holdout_approval_event_schema.py::test_state_docs_record_no_current_holdout_approval_event"

Files:
  - docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - tests/reset/test_holdout_approval_event_schema.py

Context-Refs:
  - docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md
  - docs/governance/

Notes: |
  Schema work only. Do not create a real approval event.

## T37: Holdout Access Audit Logging Contract

Owner:      codex
Phase:      9
Type:       none
Depends-On: T36
Status:     done 2026-05-09

Objective: |
  Define audit logging requirements for any future approved holdout access attempt while preserving blocked default behavior.

Acceptance-Criteria:
  - id: AC-1
    description: "Audit log contract records request, approval reference, candidate/evidence hashes, access decision, path fingerprint, denial reason, and immutable timestamp metadata."
    test: "tests/reset/test_holdout_audit_logging_contract.py::test_holdout_audit_logging_contract_lists_required_fields"
  - id: AC-2
    description: "Contract records denied attempts without exposing holdout path contents or opening holdout data."
    test: "tests/reset/test_holdout_audit_logging_contract.py::test_holdout_audit_logging_contract_preserves_no_read_boundary"
  - id: AC-3
    description: "Evidence index records the audit logging contract proof."
    test: "tests/reset/test_holdout_audit_logging_contract.py::test_evidence_index_records_holdout_audit_logging_contract"

Files:
  - docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md
  - docs/EVIDENCE_INDEX.md
  - tests/reset/test_holdout_audit_logging_contract.py

Context-Refs:
  - docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md
  - docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md

Notes: |
  Audit logging design must not reveal or read holdout contents.

## T38: Holdout Leakage Guard Protocol Fixture

Owner:      codex
Phase:      9
Type:       none
Depends-On: T37
Status:     done 2026-05-09

Objective: |
  Define local leakage guard checks that any future approved holdout access would need to pass before a holdout read could be considered.

Acceptance-Criteria:
  - id: AC-1
    description: "Guard fixture lists candidate binding, dataset partition proof, code/policy/parameter hashes, training-window proof, and no-prior-holdout-read evidence."
    test: "tests/reset/test_holdout_leakage_guard_protocol.py::test_holdout_leakage_guard_lists_required_inputs"
  - id: AC-2
    description: "Guard fixture records fail-closed behavior for missing approval, stale hashes, partition overlap, prior holdout read, or unresolved evidence."
    test: "tests/reset/test_holdout_leakage_guard_protocol.py::test_holdout_leakage_guard_records_fail_closed_behavior"
  - id: AC-3
    description: "Prompt and handoff preserve no holdout read/unlock while guard protocol is incomplete."
    test: "tests/reset/test_holdout_leakage_guard_protocol.py::test_state_docs_preserve_holdout_lock_during_guard_protocol"

Files:
  - docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - tests/reset/test_holdout_leakage_guard_protocol.py

Context-Refs:
  - src/entropy/walkforward/leakage.py
  - src/entropy/data/holdout.py
  - docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md

Notes: |
  This is fixture/protocol work only. Do not execute holdout access.

## T39: Holdout Access Protocol Review

Owner:      codex
Phase:      9
Type:       none
Depends-On: T38
Status:     done 2026-05-09

Objective: |
  Review Phase 9 protocol artifacts, record findings, and evaluate whether any future phase may request explicit human holdout approval.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md` summarizes protocol, approval schema, audit logging, leakage guard evidence, validation, limitations, findings, and roadmap evaluation."
    test: "tests/reset/test_holdout_access_protocol_review.py::test_holdout_access_protocol_review_contains_required_sections"
  - id: AC-2
    description: "Review either keeps, modifies, or blocks the planned approved holdout evaluation phase without opening holdout."
    test: "tests/reset/test_holdout_access_protocol_review.py::test_holdout_access_protocol_review_records_roadmap_evaluation"
  - id: AC-3
    description: "Audit index and prompt record Phase 9 completion and the next active task selected by roadmap evaluation."
    test: "tests/reset/test_holdout_access_protocol_review.py::test_holdout_access_protocol_review_updates_state"

Files:
  - docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_holdout_access_protocol_review.py

Context-Refs:
  - docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md
  - docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md
  - docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md
  - docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md

Notes: |
  This is a phase-boundary review. Continue automatically after roadmap evaluation unless a blocker is found.

## T40: Holdout Approval Request Packet Scaffold

Owner:      codex
Phase:      10
Type:       none
Depends-On: T39
Status:     done 2026-05-09

Objective: |
  Scaffold a no-read holdout approval request packet that assembles Phase 9 protocol evidence, missing approvals, and blocked boundaries without creating approval.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/approvals/HOLDOUT_APPROVAL_REQUEST_PACKET.md` lists protocol, schema, audit, leakage guard, and review evidence required before any future approval decision."
    test: "tests/reset/test_holdout_approval_request_packet.py::test_holdout_approval_request_packet_lists_required_evidence"
  - id: AC-2
    description: "Packet records that no explicit approval event currently exists and that holdout read/unlock remain blocked."
    test: "tests/reset/test_holdout_approval_request_packet.py::test_holdout_approval_request_packet_preserves_no_approval_state"
  - id: AC-3
    description: "Prompt and handoff record Phase 10 as no-read approval decision work."
    test: "tests/reset/test_holdout_approval_request_packet.py::test_state_docs_record_phase10_no_read_decision_work"

Files:
  - docs/approvals/HOLDOUT_APPROVAL_REQUEST_PACKET.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - tests/reset/test_holdout_approval_request_packet.py

Context-Refs:
  - docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md
  - docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md
  - docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md
  - docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md
  - docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md

Notes: |
  Request packet scaffold only. Do not create approval, read holdout, or unlock holdout.

## T41: Holdout Approval Evidence Intake Contract

Owner:      codex
Phase:      10
Type:       none
Depends-On: T40
Status:     done 2026-05-09

Objective: |
  Define local intake checks for a future explicit holdout approval event while rejecting absent, generated, inferred, expired, revoked, stale, or scope-mismatched evidence.

Acceptance-Criteria:
  - id: AC-1
    description: "Intake contract lists required approval event fields and hash bindings."
    test: "tests/reset/test_holdout_approval_intake_contract.py::test_holdout_approval_intake_lists_required_fields"
  - id: AC-2
    description: "Intake fixtures reject absent, generated, inferred, expired, revoked, stale, or scope-mismatched evidence."
    test: "tests/reset/test_holdout_approval_intake_contract.py::test_holdout_approval_intake_rejects_invalid_evidence"
  - id: AC-3
    description: "State docs preserve no approval event until explicit evidence exists."
    test: "tests/reset/test_holdout_approval_intake_contract.py::test_state_docs_preserve_no_approval_event"

Files:
  - docs/approvals/HOLDOUT_APPROVAL_INTAKE_CONTRACT.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - tests/reset/test_holdout_approval_intake_contract.py

Context-Refs:
  - docs/approvals/HOLDOUT_APPROVAL_REQUEST_PACKET.md
  - docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md

Notes: |
  Intake contract only. Do not create a real approval event.

## T42: Holdout Approval Absence Denial Packet

Owner:      codex
Phase:      10
Type:       none
Depends-On: T41
Status:     done 2026-05-09

Objective: |
  Record a deterministic denial packet for the current no-approval state without opening or reading holdout data.

Acceptance-Criteria:
  - id: AC-1
    description: "Denial packet records missing explicit approval, missing phase-gate approval, and incomplete guard state."
    test: "tests/reset/test_holdout_approval_absence_denial.py::test_denial_packet_records_missing_prerequisites"
  - id: AC-2
    description: "Denial packet records no holdout path opened, no holdout read, and no unlock requested."
    test: "tests/reset/test_holdout_approval_absence_denial.py::test_denial_packet_preserves_no_read_boundary"
  - id: AC-3
    description: "Denial packet rejects OOS/performance, production, and capital-ready conclusions."
    test: "tests/reset/test_holdout_approval_absence_denial.py::test_denial_packet_rejects_claim_surfaces"

Files:
  - docs/approvals/HOLDOUT_APPROVAL_ABSENCE_DENIAL.md
  - tests/reset/test_holdout_approval_absence_denial.py

Context-Refs:
  - docs/approvals/HOLDOUT_APPROVAL_INTAKE_CONTRACT.md
  - docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md

Notes: |
  Denial evidence only. Do not read or unlock holdout.

## T43: Holdout Non-Approval Source Regression

Owner:      codex
Phase:      10
Type:       none
Depends-On: T42
Status:     done 2026-05-09

Objective: |
  Sweep active Phase 10 approval-decision artifacts to prove roadmap phases, reviews, tests, readiness packets, protocol docs, and generated scaffolds cannot be treated as approval.

Acceptance-Criteria:
  - id: AC-1
    description: "Regression test scans active docs for restricted approval flags and implicit approval language."
    test: "tests/reset/test_holdout_non_approval_source_regression.py::test_phase10_docs_reject_implicit_approval_sources"
  - id: AC-2
    description: "Regression test confirms no approval event currently exists in prompt and handoff."
    test: "tests/reset/test_holdout_non_approval_source_regression.py::test_state_docs_record_no_current_approval_event"
  - id: AC-3
    description: "Regression test confirms holdout read/unlock remain blocked."
    test: "tests/reset/test_holdout_non_approval_source_regression.py::test_holdout_read_unlock_remain_blocked"

Files:
  - tests/reset/test_holdout_non_approval_source_regression.py
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md

Context-Refs:
  - docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md
  - docs/approvals/HOLDOUT_APPROVAL_ABSENCE_DENIAL.md

Notes: |
  Regression only. Do not create approval or read holdout.

## T44: Holdout Decision No-Read Dry Run

Owner:      codex
Phase:      10
Type:       none
Depends-On: T43
Status:     done 2026-05-09

Objective: |
  Add a local no-read dry run proving the approval decision packet can assemble protocol and denial evidence without opening holdout data.

Acceptance-Criteria:
  - id: AC-1
    description: "Dry run assembles Phase 9 and Phase 10 artifacts without opening a holdout path."
    test: "tests/reset/test_holdout_decision_no_read_dry_run.py::test_decision_dry_run_uses_no_read_artifacts"
  - id: AC-2
    description: "Dry run fails if any holdout read/unlock or OOS/performance approval flag is present."
    test: "tests/reset/test_holdout_decision_no_read_dry_run.py::test_decision_dry_run_rejects_restricted_flags"
  - id: AC-3
    description: "Dry run records current denial and missing approval prerequisites."
    test: "tests/reset/test_holdout_decision_no_read_dry_run.py::test_decision_dry_run_records_denial_state"

Files:
  - docs/approvals/HOLDOUT_DECISION_DRY_RUN.md
  - tests/reset/test_holdout_decision_no_read_dry_run.py

Context-Refs:
  - docs/approvals/HOLDOUT_APPROVAL_ABSENCE_DENIAL.md
  - docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md

Notes: |
  Dry run only. Do not open holdout path.

## T45: Holdout Approval Decision Review

Owner:      codex
Phase:      10
Type:       none
Depends-On: T44
Status:     done 2026-05-09

Objective: |
  Review Phase 10 approval decision artifacts and evaluate whether a future explicit human holdout approval request may be presented.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md` summarizes request packet, intake contract, denial packet, regression sweep, dry run, validation, limitations, findings, and roadmap evaluation."
    test: "tests/reset/test_holdout_approval_decision_review.py::test_holdout_approval_decision_review_contains_required_sections"
  - id: AC-2
    description: "Review either keeps, modifies, or blocks the future approved holdout evaluation phase without opening holdout."
    test: "tests/reset/test_holdout_approval_decision_review.py::test_holdout_approval_decision_review_records_roadmap_evaluation"
  - id: AC-3
    description: "Audit index and prompt record Phase 10 completion and the next active task selected by roadmap evaluation."
    test: "tests/reset/test_holdout_approval_decision_review.py::test_holdout_approval_decision_review_updates_state"

Files:
  - docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_holdout_approval_decision_review.py

Context-Refs:
  - docs/approvals/HOLDOUT_DECISION_DRY_RUN.md
  - docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md

Notes: |
  This is a phase-boundary review. Continue automatically after roadmap evaluation unless a blocker is found.

## T46: Live-Feed Boundary Contract

Owner:      codex
Phase:      11
Type:       none
Depends-On: T45
Status:     done 2026-05-09

Objective: |
  Define the local live-feed dry-run boundary so market-data readiness work cannot place orders, connect to broker/exchange execution, deploy credentials, activate live capital, or alter holdout status.

Acceptance-Criteria:
  - id: AC-1
    description: "Boundary contract records allowed local fixture and dry-run operations."
    test: "tests/reset/test_live_feed_boundary_contract.py::test_live_feed_boundary_contract_records_allowed_operations"
  - id: AC-2
    description: "Boundary contract blocks orders, broker/exchange execution, credentials, live capital, production labels, and holdout access."
    test: "tests/reset/test_live_feed_boundary_contract.py::test_live_feed_boundary_contract_blocks_external_effects"
  - id: AC-3
    description: "Prompt and handoff record Phase 11 as local-only live-feed readiness."
    test: "tests/reset/test_live_feed_boundary_contract.py::test_state_docs_record_phase11_local_only_scope"

Files:
  - docs/protocols/LIVE_FEED_DRY_RUN_BOUNDARY.md
  - tests/reset/test_live_feed_boundary_contract.py

Context-Refs:
  - docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md
  - docs/ARCHITECTURE.md

Notes: |
  Boundary only. Do not connect to live feeds, broker/exchange execution, credentials, or capital.

## T47: Live-Feed Fixture Manifest

Owner:      codex
Phase:      11
Type:       none
Depends-On: T46
Status:     done 2026-05-09

Objective: |
  Define deterministic local market-data fixture manifest requirements for live-feed dry-run readiness without pulling live data.

Acceptance-Criteria:
  - id: AC-1
    description: "Manifest records fixture identity, source class, hashes, schema, and replay constraints."
    test: "tests/reset/test_live_feed_fixture_manifest.py::test_live_feed_fixture_manifest_records_required_fields"
  - id: AC-2
    description: "Manifest rejects live credentials, live network pulls, broker/exchange execution, and capital actions."
    test: "tests/reset/test_live_feed_fixture_manifest.py::test_live_feed_fixture_manifest_rejects_live_effects"
  - id: AC-3
    description: "Manifest binds fixtures to local dry-run scope and no-holdout state."
    test: "tests/reset/test_live_feed_fixture_manifest.py::test_live_feed_fixture_manifest_binds_local_scope"

Files:
  - docs/protocols/LIVE_FEED_FIXTURE_MANIFEST.md
  - tests/reset/test_live_feed_fixture_manifest.py

Context-Refs:
  - docs/protocols/LIVE_FEED_DRY_RUN_BOUNDARY.md

Notes: |
  Manifest only. Do not fetch live market data.

## T48: Live-Feed Adapter Dry-Run Contract

Owner:      codex
Phase:      11
Type:       none
Depends-On: T47
Status:     done 2026-05-09

Objective: |
  Define adapter dry-run checks that exercise local parsing and normalization boundaries without live connectivity or order paths.

Acceptance-Criteria:
  - id: AC-1
    description: "Contract records local parser, normalization, clock, and replay checks."
    test: "tests/reset/test_live_feed_adapter_dry_run_contract.py::test_adapter_dry_run_contract_records_local_checks"
  - id: AC-2
    description: "Contract rejects network sockets, credentials, order placement, and broker/exchange execution."
    test: "tests/reset/test_live_feed_adapter_dry_run_contract.py::test_adapter_dry_run_contract_rejects_external_paths"
  - id: AC-3
    description: "Contract records no production or capital-ready claim."
    test: "tests/reset/test_live_feed_adapter_dry_run_contract.py::test_adapter_dry_run_contract_rejects_claims"

Files:
  - docs/protocols/LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT.md
  - tests/reset/test_live_feed_adapter_dry_run_contract.py

Context-Refs:
  - docs/protocols/LIVE_FEED_FIXTURE_MANIFEST.md

Notes: |
  Contract only. Do not connect to any external feed.

## T49: Live-Feed Observability Packet

Owner:      codex
Phase:      11
Type:       none
Depends-On: T48
Status:     done 2026-05-09

Objective: |
  Define local observability evidence for dry-run feed readiness, including logging, counters, and failure states without external side effects.

Acceptance-Criteria:
  - id: AC-1
    description: "Packet records local dry-run observability fields and failure counters."
    test: "tests/reset/test_live_feed_observability_packet.py::test_observability_packet_records_required_fields"
  - id: AC-2
    description: "Packet records no credentials, raw secrets, orders, capital actions, or holdout reads."
    test: "tests/reset/test_live_feed_observability_packet.py::test_observability_packet_rejects_sensitive_and_external_effects"
  - id: AC-3
    description: "Packet records readiness limitations and no production claim."
    test: "tests/reset/test_live_feed_observability_packet.py::test_observability_packet_records_limitations"

Files:
  - docs/protocols/LIVE_FEED_OBSERVABILITY_PACKET.md
  - tests/reset/test_live_feed_observability_packet.py

Context-Refs:
  - docs/protocols/LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT.md

Notes: |
  Observability evidence only. Do not emit live feed telemetry.

## T50: Live-Feed Dry Run Readiness Review

Owner:      codex
Phase:      11
Type:       none
Depends-On: T49
Status:     done 2026-05-09

Objective: |
  Review Phase 11 live-feed dry-run readiness artifacts and evaluate the next roadmap step without enabling broker/exchange execution or capital.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes boundary, manifest, adapter contract, observability packet, validation, limitations, findings, and roadmap evaluation."
    test: "tests/reset/test_live_feed_readiness_review.py::test_live_feed_readiness_review_contains_required_sections"
  - id: AC-2
    description: "Review records whether to keep, modify, or block the broker sandbox phase."
    test: "tests/reset/test_live_feed_readiness_review.py::test_live_feed_readiness_review_records_roadmap_evaluation"
  - id: AC-3
    description: "Audit index and prompt record Phase 11 completion and the next active task selected by roadmap evaluation."
    test: "tests/reset/test_live_feed_readiness_review.py::test_live_feed_readiness_review_updates_state"

Files:
  - docs/audit/LIVE_FEED_READINESS_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_live_feed_readiness_review.py

Context-Refs:
  - docs/protocols/LIVE_FEED_OBSERVABILITY_PACKET.md

Notes: |
  Review only. Do not enable broker/exchange execution or capital.

## T51: Broker Sandbox Boundary Contract

Owner:      codex
Phase:      12
Type:       none
Depends-On: T50
Status:     done 2026-05-09

Objective: |
  Define sandbox-only broker/exchange boundaries before any execution risk artifact work.

Acceptance-Criteria:
  - id: AC-1
    description: "Boundary records allowed sandbox-only operations and required local controls."
    test: "tests/reset/test_broker_sandbox_boundary_contract.py::test_broker_sandbox_boundary_records_allowed_operations"
  - id: AC-2
    description: "Boundary blocks live orders, production credentials, live capital, production labels, and holdout access."
    test: "tests/reset/test_broker_sandbox_boundary_contract.py::test_broker_sandbox_boundary_blocks_live_effects"
  - id: AC-3
    description: "Prompt and handoff record Phase 12 as sandbox-only execution risk audit."
    test: "tests/reset/test_broker_sandbox_boundary_contract.py::test_state_docs_record_phase12_sandbox_only_scope"

Files:
  - docs/protocols/BROKER_SANDBOX_BOUNDARY.md
  - tests/reset/test_broker_sandbox_boundary_contract.py

Context-Refs:
  - docs/audit/LIVE_FEED_READINESS_REVIEW.md

Notes: |
  Boundary only. Do not connect to live broker/exchange execution or capital.

## T52: Broker Sandbox Fixture Manifest

Owner:      codex
Phase:      12
Type:       none
Depends-On: T51
Status:     done 2026-05-09

Objective: |
  Define deterministic sandbox fixture requirements for broker/exchange execution risk tests without live connectivity.

Acceptance-Criteria:
  - id: AC-1
    description: "Manifest records fixture identity, order scenario class, hashes, schema, and replay constraints."
    test: "tests/reset/test_broker_sandbox_fixture_manifest.py::test_broker_sandbox_fixture_manifest_records_required_fields"
  - id: AC-2
    description: "Manifest rejects production credentials, live orders, live capital, and holdout access."
    test: "tests/reset/test_broker_sandbox_fixture_manifest.py::test_broker_sandbox_fixture_manifest_rejects_live_effects"
  - id: AC-3
    description: "Manifest binds fixtures to sandbox-only scope and risk-audit boundaries."
    test: "tests/reset/test_broker_sandbox_fixture_manifest.py::test_broker_sandbox_fixture_manifest_binds_scope"

Files:
  - docs/protocols/BROKER_SANDBOX_FIXTURE_MANIFEST.md
  - tests/reset/test_broker_sandbox_fixture_manifest.py

Context-Refs:
  - docs/protocols/BROKER_SANDBOX_BOUNDARY.md

Notes: |
  Manifest only. Do not open broker/exchange connectivity.

## T53: Execution Risk Control Contract

Owner:      codex
Phase:      12
Type:       none
Depends-On: T52
Status:     done 2026-05-09

Objective: |
  Define sandbox execution risk controls for order validation, limits, rejection, and deterministic audit behavior.

Acceptance-Criteria:
  - id: AC-1
    description: "Contract records sandbox order validation, limits, rejection, and risk state fields."
    test: "tests/reset/test_execution_risk_control_contract.py::test_execution_risk_contract_records_controls"
  - id: AC-2
    description: "Contract rejects live order placement, production credentials, live capital, and production labels."
    test: "tests/reset/test_execution_risk_control_contract.py::test_execution_risk_contract_rejects_live_effects"
  - id: AC-3
    description: "Contract records deterministic audit and no-capital boundaries."
    test: "tests/reset/test_execution_risk_control_contract.py::test_execution_risk_contract_records_audit_boundaries"

Files:
  - docs/protocols/EXECUTION_RISK_CONTROL_CONTRACT.md
  - tests/reset/test_execution_risk_control_contract.py

Context-Refs:
  - docs/protocols/BROKER_SANDBOX_FIXTURE_MANIFEST.md

Notes: |
  Risk contract only. Do not place orders.

## T54: Kill-Switch Audit Log Contract

Owner:      codex
Phase:      12
Type:       none
Depends-On: T53
Status:     done 2026-05-09

Objective: |
  Define sandbox kill-switch audit requirements and fail-closed evidence without live capital or live order paths.

Acceptance-Criteria:
  - id: AC-1
    description: "Contract records kill-switch trigger, state, actor, timestamp, and audit fields."
    test: "tests/reset/test_kill_switch_audit_log_contract.py::test_kill_switch_contract_records_required_fields"
  - id: AC-2
    description: "Contract records fail-closed behavior and blocks order/capital activation."
    test: "tests/reset/test_kill_switch_audit_log_contract.py::test_kill_switch_contract_records_fail_closed_behavior"
  - id: AC-3
    description: "Contract rejects secrets, production credentials, raw account identifiers, and holdout data."
    test: "tests/reset/test_kill_switch_audit_log_contract.py::test_kill_switch_contract_rejects_sensitive_surfaces"

Files:
  - docs/protocols/KILL_SWITCH_AUDIT_LOG_CONTRACT.md
  - tests/reset/test_kill_switch_audit_log_contract.py

Context-Refs:
  - docs/protocols/EXECUTION_RISK_CONTROL_CONTRACT.md

Notes: |
  Audit contract only. Do not emit live order telemetry.

## T55: Sandbox Execution No-Capital Dry Run

Owner:      codex
Phase:      12
Type:       none
Depends-On: T54
Status:     done 2026-05-09

Objective: |
  Assemble sandbox execution risk artifacts into a local no-capital dry run without live orders or live connectivity.

Acceptance-Criteria:
  - id: AC-1
    description: "Dry run assembles sandbox boundary, fixture, risk control, and kill-switch artifacts."
    test: "tests/reset/test_sandbox_execution_no_capital_dry_run.py::test_sandbox_dry_run_assembles_artifacts"
  - id: AC-2
    description: "Dry run rejects live orders, production credentials, live capital, and production claims."
    test: "tests/reset/test_sandbox_execution_no_capital_dry_run.py::test_sandbox_dry_run_rejects_live_effects"
  - id: AC-3
    description: "Dry run records no holdout access and no capital-ready conclusion."
    test: "tests/reset/test_sandbox_execution_no_capital_dry_run.py::test_sandbox_dry_run_records_limitations"

Files:
  - docs/protocols/SANDBOX_EXECUTION_NO_CAPITAL_DRY_RUN.md
  - tests/reset/test_sandbox_execution_no_capital_dry_run.py

Context-Refs:
  - docs/protocols/KILL_SWITCH_AUDIT_LOG_CONTRACT.md

Notes: |
  Dry run only. Do not place live or sandbox orders from code.

## T56: Broker Sandbox Readiness Review

Owner:      codex
Phase:      12
Type:       none
Depends-On: T55
Status:     done 2026-05-09

Objective: |
  Review Phase 12 broker sandbox and execution risk audit artifacts and evaluate the next roadmap step without enabling production or capital.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes sandbox boundary, fixture manifest, risk controls, kill-switch contract, dry run, validation, limitations, findings, and roadmap evaluation."
    test: "tests/reset/test_broker_sandbox_readiness_review.py::test_broker_sandbox_readiness_review_contains_required_sections"
  - id: AC-2
    description: "Review records whether to keep, modify, or block the production/capital gate phase."
    test: "tests/reset/test_broker_sandbox_readiness_review.py::test_broker_sandbox_readiness_review_records_roadmap_evaluation"
  - id: AC-3
    description: "Audit index and prompt record Phase 12 completion and the next active task selected by roadmap evaluation."
    test: "tests/reset/test_broker_sandbox_readiness_review.py::test_broker_sandbox_readiness_review_updates_state"

Files:
  - docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_broker_sandbox_readiness_review.py

Context-Refs:
  - docs/protocols/SANDBOX_EXECUTION_NO_CAPITAL_DRY_RUN.md

Notes: |
  Review only. Do not enable production, live capital, or live orders.

## T57: Product Hypothesis Confirmation Request Packet

Owner:      codex
Phase:      13
Type:       none
Depends-On: T56
Status:     done 2026-05-09

Objective: |
  Assemble a local-only request packet that states the product hypothesis confirmation goal, current evidence, missing approvals, and safest next validation options without opening production, capital, live orders, broker/exchange execution, production credentials, or holdout access.

Acceptance-Criteria:
  - id: AC-1
    description: "Packet lists current evidence from archive, readiness, holdout protocol, live-feed dry-run, and broker sandbox phases."
    test: "tests/reset/test_product_hypothesis_confirmation_request.py::test_product_hypothesis_request_lists_current_evidence"
  - id: AC-2
    description: "Packet records missing approvals and rejects production/capital/live/holdout actions."
    test: "tests/reset/test_product_hypothesis_confirmation_request.py::test_product_hypothesis_request_rejects_restricted_actions"
  - id: AC-3
    description: "Prompt and handoff open Phase 13 as local-only hypothesis confirmation decision work."
    test: "tests/reset/test_product_hypothesis_confirmation_request.py::test_state_docs_open_phase13_local_only_decision_work"

Files:
  - docs/approvals/PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md
  - tests/reset/test_product_hypothesis_confirmation_request.py

Context-Refs:
  - docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md

Notes: |
  Request packet only. Do not read holdout, place orders, load credentials, connect to broker/exchange systems, or activate capital.

## T58: Product Validation Approval Intake Contract

Owner:      codex
Phase:      13
Type:       none
Depends-On: T57
Status:     done 2026-05-09

Objective: |
  Define local-only intake requirements for any future validation approval event before holdout, live-feed, broker sandbox execution, production, or capital validation could be considered.

Acceptance-Criteria:
  - id: AC-1
    description: "Contract lists required approval fields, evidence references, risk owner, scope, expiry, and revocation fields."
    test: "tests/reset/test_product_validation_approval_intake_contract.py::test_product_validation_intake_lists_required_fields"
  - id: AC-2
    description: "Contract rejects incomplete, generated, inferred, stale, revoked, or overbroad validation approvals."
    test: "tests/reset/test_product_validation_approval_intake_contract.py::test_product_validation_intake_rejects_invalid_approvals"
  - id: AC-3
    description: "Contract preserves current no-approval state and blocked restricted actions."
    test: "tests/reset/test_product_validation_approval_intake_contract.py::test_product_validation_intake_preserves_no_approval_state"

Files:
  - docs/approvals/PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT.md
  - tests/reset/test_product_validation_approval_intake_contract.py

Context-Refs:
  - docs/approvals/PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md

Notes: |
  Intake contract only. Do not create an approval event.

## T59: Product Hypothesis Validation Path Decision

Owner:      codex
Phase:      13
Type:       none
Depends-On: T58
Status:     done 2026-05-09

Objective: |
  Record the current deterministic decision for the safest next validation path toward product hypothesis confirmation.

Acceptance-Criteria:
  - id: AC-1
    description: "Decision packet compares archive-only, no-read holdout, live-feed dry-run, broker sandbox, and production/capital paths."
    test: "tests/reset/test_product_hypothesis_validation_path_decision.py::test_validation_path_decision_compares_options"
  - id: AC-2
    description: "Decision packet selects only approved local/no-effect next steps and blocks restricted paths."
    test: "tests/reset/test_product_hypothesis_validation_path_decision.py::test_validation_path_decision_selects_safe_next_step"
  - id: AC-3
    description: "Decision packet records that product hypothesis is not confirmed yet."
    test: "tests/reset/test_product_hypothesis_validation_path_decision.py::test_validation_path_decision_records_not_confirmed"

Files:
  - docs/approvals/PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md
  - tests/reset/test_product_hypothesis_validation_path_decision.py

Context-Refs:
  - docs/approvals/PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT.md

Notes: |
  Decision packet only. Do not execute validation actions.

## T60: Production Capital Non-Approval Regression

Owner:      codex
Phase:      13
Type:       none
Depends-On: T59
Status:     done 2026-05-09

Objective: |
  Add regression coverage proving Phase 13 docs, reviews, tests, and request packets are not approval sources for production, capital, live order, broker/exchange execution, production credential, or holdout access.

Acceptance-Criteria:
  - id: AC-1
    description: "Regression rejects roadmap, review, test, and request-packet approval sources."
    test: "tests/reset/test_production_capital_non_approval_regression.py::test_non_approval_sources_are_rejected"
  - id: AC-2
    description: "Regression proves restricted action flags remain absent from active docs."
    test: "tests/reset/test_production_capital_non_approval_regression.py::test_restricted_action_flags_remain_absent"
  - id: AC-3
    description: "Prompt and handoff preserve no-current-approval state."
    test: "tests/reset/test_production_capital_non_approval_regression.py::test_state_docs_preserve_no_current_approval"

Files:
  - tests/reset/test_production_capital_non_approval_regression.py
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md

Context-Refs:
  - docs/approvals/PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md

Notes: |
  Regression only. Do not grant approval.

## T61: Local Next Validation Plan Packet

Owner:      codex
Phase:      13
Type:       none
Depends-On: T60
Status:     done 2026-05-09

Objective: |
  Assemble a local-only next validation plan packet that can be reviewed by a human before any future holdout, sandbox, live, production, or capital validation is approved.

Acceptance-Criteria:
  - id: AC-1
    description: "Plan lists objective, hypothesis, evidence inputs, validation options, prerequisites, risks, rollback, and blocked actions."
    test: "tests/reset/test_local_next_validation_plan_packet.py::test_next_validation_plan_lists_required_sections"
  - id: AC-2
    description: "Plan records no current approval and no claim of product hypothesis confirmation."
    test: "tests/reset/test_local_next_validation_plan_packet.py::test_next_validation_plan_records_no_confirmation"
  - id: AC-3
    description: "Plan rejects live/capital/production/holdout execution unless future explicit approval exists."
    test: "tests/reset/test_local_next_validation_plan_packet.py::test_next_validation_plan_rejects_restricted_execution"

Files:
  - docs/approvals/LOCAL_NEXT_VALIDATION_PLAN_PACKET.md
  - tests/reset/test_local_next_validation_plan_packet.py

Context-Refs:
  - docs/approvals/PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md

Notes: |
  Plan packet only. Do not execute the plan.

## T62: Product Hypothesis Confirmation Decision Review

Owner:      codex
Phase:      13
Type:       none
Depends-On: T61
Status:     done 2026-05-09

Objective: |
  Review Phase 13 local-only product hypothesis confirmation decision artifacts and record the next human decision point.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes request, intake, path decision, non-approval regression, validation plan, validation, limitations, findings, and next decision point."
    test: "tests/reset/test_product_hypothesis_confirmation_decision_review.py::test_confirmation_decision_review_contains_required_sections"
  - id: AC-2
    description: "Review records whether product hypothesis is confirmed, rejected, or still unconfirmed pending future validation."
    test: "tests/reset/test_product_hypothesis_confirmation_decision_review.py::test_confirmation_decision_review_records_status"
  - id: AC-3
    description: "Audit index and prompt record Phase 13 completion and the required next human decision."
    test: "tests/reset/test_product_hypothesis_confirmation_decision_review.py::test_confirmation_decision_review_updates_state"

Files:
  - docs/audit/PRODUCT_HYPOTHESIS_CONFIRMATION_DECISION_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_product_hypothesis_confirmation_decision_review.py

Context-Refs:
  - docs/approvals/LOCAL_NEXT_VALIDATION_PLAN_PACKET.md

Notes: |
  Review only. Do not approve production, capital, live orders, broker/exchange execution, production credentials, or holdout access.

## T63: Local Broker Sandbox Replay Approval Event

Owner:      codex
Phase:      14
Type:       none
Depends-On: T62
Status:     done 2026-05-09

Objective: |
  Record the operator approval for the local broker sandbox no-capital replay extension while preserving no-effect and no-claim boundaries.

Acceptance-Criteria:
  - id: AC-1
    description: "Approval event records the explicit operator approval source and local replay scope."
    test: "tests/reset/test_local_broker_sandbox_replay_approval_event.py::test_local_replay_approval_event_records_operator_scope"
  - id: AC-2
    description: "Approval event blocks sandbox order emission from code, live orders, broker/exchange execution, credentials, capital, holdout, and OOS/performance claims."
    test: "tests/reset/test_local_broker_sandbox_replay_approval_event.py::test_local_replay_approval_event_blocks_restricted_actions"
  - id: AC-3
    description: "Approval event preserves unconfirmed product hypothesis status before replay."
    test: "tests/reset/test_local_broker_sandbox_replay_approval_event.py::test_local_replay_approval_event_preserves_unconfirmed_hypothesis"

Files:
  - docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md
  - tests/reset/test_local_broker_sandbox_replay_approval_event.py

Context-Refs:
  - docs/approvals/LOCAL_NEXT_VALIDATION_PLAN_PACKET.md

Notes: |
  This approval is scoped to local no-effect replay only. Do not emit orders or connect to broker/exchange systems.

## T64: Broker Sandbox No-Capital Replay Primitive

Owner:      codex
Phase:      14
Type:       none
Depends-On: T63
Status:     done 2026-05-09

Objective: |
  Add a deterministic SimBroker replay primitive that runs only against local fixture scenarios and returns explicit no-effect result flags.

Acceptance-Criteria:
  - id: AC-1
    description: "Replay is deterministic and hash-bound for identical local fixture inputs."
    test: "tests/unit/test_simbroker_replay.py::test_no_capital_sandbox_replay_is_deterministic_and_hash_bound"
  - id: AC-2
    description: "Replay result records no order emission, no broker/exchange connection, no credential loading, no capital activation, and no holdout access."
    test: "tests/unit/test_simbroker_replay.py::test_no_capital_sandbox_replay_preserves_no_effect_boundaries"
  - id: AC-3
    description: "Replay rejects invalid approval scope, empty scenarios, duplicate scenario ids, and live broker/exchange imports."
    test: "tests/unit/test_simbroker_replay.py"

Files:
  - src/entropy/simbroker/replay.py
  - src/entropy/simbroker/__init__.py
  - tests/unit/test_simbroker_replay.py

Context-Refs:
  - docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md
  - docs/protocols/SANDBOX_EXECUTION_NO_CAPITAL_DRY_RUN.md

Notes: |
  Local code primitive only. Do not add broker/exchange clients, sockets, credentials, or order emission.

## T65: Broker Sandbox Replay Evidence Packet

Owner:      codex
Phase:      14
Type:       none
Depends-On: T64
Status:     done 2026-05-09

Objective: |
  Record the approved local replay contract and replay result packet with deterministic hash, scenario summary, no-effect flags, and product hypothesis evidence delta.

Acceptance-Criteria:
  - id: AC-1
    description: "Replay contract binds the local approval event, replay inputs, deterministic result fields, and rejection conditions."
    test: "tests/reset/test_broker_sandbox_no_capital_replay_contract.py::test_replay_contract_binds_local_approval_and_inputs"
  - id: AC-2
    description: "Replay contract rejects restricted scopes and claim interpretations."
    test: "tests/reset/test_broker_sandbox_no_capital_replay_contract.py::test_replay_contract_rejects_restricted_scope_and_claims"
  - id: AC-3
    description: "Replay result records deterministic local evidence delta and state docs open the next evidence-delta task."
    test: "tests/reset/test_broker_sandbox_no_capital_replay_contract.py"

Files:
  - docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_CONTRACT.md
  - docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md
  - tests/reset/test_broker_sandbox_no_capital_replay_contract.py
  - docs/tasks.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md

Context-Refs:
  - src/entropy/simbroker/replay.py

Notes: |
  Evidence packet only. The product hypothesis is strengthened locally but remains unconfirmed.

## T66: Local Replay Evidence Delta Decision

Owner:      codex
Phase:      14
Type:       none
Depends-On: T65
Status:     deferred 2026-05-11 artifact-support override

Objective: |
  Decide how the local no-effect replay evidence changes the product hypothesis confirmation posture without creating production, capital-ready, holdout, or OOS/performance claims.

Acceptance-Criteria:
  - id: AC-1
    description: "Decision packet compares pre-replay and post-replay evidence."
    test: "tests/reset/test_local_replay_evidence_delta_decision.py::test_replay_delta_decision_compares_evidence"
  - id: AC-2
    description: "Decision packet records that the product hypothesis is strengthened locally but not confirmed or rejected."
    test: "tests/reset/test_local_replay_evidence_delta_decision.py::test_replay_delta_decision_preserves_unconfirmed_status"
  - id: AC-3
    description: "Decision packet lists the next bounded validation option without opening restricted actions."
    test: "tests/reset/test_local_replay_evidence_delta_decision.py::test_replay_delta_decision_keeps_restricted_actions_blocked"

Files:
  - docs/approvals/LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md
  - tests/reset/test_local_replay_evidence_delta_decision.py

Context-Refs:
  - docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md

Notes: |
  Decision only. Do not claim production readiness or OOS/performance.

## T67: Replay Evidence Non-Approval Regression

Owner:      codex
Phase:      14
Type:       none
Depends-On: T66
Status:     deferred 2026-05-11 artifact-support override

Objective: |
  Add regression coverage proving replay approval, replay results, and local evidence deltas are not approval sources for restricted execution or product claims.

Acceptance-Criteria:
  - id: AC-1
    description: "Regression rejects replay packets as production/capital/live/holdout approval sources."
    test: "tests/reset/test_replay_evidence_non_approval_regression.py::test_replay_packets_are_not_restricted_approvals"
  - id: AC-2
    description: "Regression proves replay evidence cannot create OOS/performance, production, or capital-ready labels."
    test: "tests/reset/test_replay_evidence_non_approval_regression.py::test_replay_evidence_cannot_create_claim_labels"
  - id: AC-3
    description: "Prompt and handoff keep restricted surfaces blocked."
    test: "tests/reset/test_replay_evidence_non_approval_regression.py::test_state_docs_keep_restricted_surfaces_blocked"

Files:
  - tests/reset/test_replay_evidence_non_approval_regression.py
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md

Context-Refs:
  - docs/approvals/LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md

Notes: |
  Regression only. Do not broaden approval scope.

## T68: Local Replay Extension Review

Owner:      codex
Phase:      14
Type:       none
Depends-On: T67
Status:     deferred 2026-05-11 artifact-support override

Objective: |
  Review Phase 14 local broker sandbox no-capital replay extension artifacts and decide the next safe human decision or local validation phase.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes approval event, replay primitive, replay evidence, evidence-delta decision, regression, validation, limitations, findings, and next decision point."
    test: "tests/reset/test_local_replay_extension_review.py::test_local_replay_review_contains_required_sections"
  - id: AC-2
    description: "Review records product hypothesis status after replay."
    test: "tests/reset/test_local_replay_extension_review.py::test_local_replay_review_records_hypothesis_status"
  - id: AC-3
    description: "Audit index and prompt record Phase 14 completion and next boundary."
    test: "tests/reset/test_local_replay_extension_review.py::test_local_replay_review_updates_state"

Files:
  - docs/audit/LOCAL_REPLAY_EXTENSION_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - tests/reset/test_local_replay_extension_review.py

Context-Refs:
  - docs/approvals/LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md

Notes: |
  Review only. Keep all restricted execution and claim surfaces blocked.

## T69: Shared Artifact Contract Freeze

Owner:      codex
Phase:      15
Type:       docs
Depends-On: none
Status:     done 2026-05-12

Objective: |
  Define the minimal shared artifact contract that Trader Risk Audit and Signal
  Analytics Sandbox can attach to real reports without forcing product-specific
  logic into Core.

Acceptance-Criteria:
  - id: AC-1
    description: "A shared artifact contract doc defines required fields: product, run id, input refs/hashes where safe, policy/config hash, code version/ref, generated artifact refs, limitations, no-claim boundary, manual validation status, error register ref, and external-delivery approval status."
    test: "manual-evidence: shared artifact contract doc exists."
  - id: AC-2
    description: "Contract includes product adoption notes for Trader and Signal, including optional/limited fields for public-source capture reproducibility."
    test: "manual-evidence: product adoption sections exist."
  - id: AC-3
    description: "Contract explicitly says Core must not own product-specific report logic."
    test: "manual-evidence: boundary section exists."

Files:
  - docs/ARTIFACT_SUPPORT_ROADMAP.md
  - docs/core/ARTIFACT_CONTRACT.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/EVIDENCE_INDEX.md

Context-Refs:
  - docs/ARTIFACT_SUPPORT_ROADMAP.md#3-phase-ec-af-0---shared-artifact-contract-freeze
  - ../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md#phase-1---real-data-intake

Notes: |
  Prefer docs first. Add code only if a product artifact cannot adopt the
  contract without a reusable primitive.

## T70: Report Validity Checklist

Owner:      codex
Phase:      15
Type:       docs
Depends-On: T69
Status:     done 2026-05-12

Objective: |
  Create the shared checklist used before a Trader or Signal report can move
  from internal artifact to external pilot artifact.

Acceptance-Criteria:
  - id: AC-1
    description: "Checklist covers input provenance, deterministic processing, evidence/source traceability, manual validation, claim safety, limitations, privacy/redaction, reproducibility notes, and delivery approval."
    test: "manual-evidence: checklist doc exists."
  - id: AC-2
    description: "Checklist defines P0/P1/P2/P3 severity and stop-ship rules for report artifacts."
    test: "manual-evidence: severity section exists."
  - id: AC-3
    description: "Checklist distinguishes internal demo readiness from external pilot readiness."
    test: "manual-evidence: decision states exist."

Files:
  - docs/core/REPORT_VALIDITY_CHECKLIST.md
  - docs/ARTIFACT_SUPPORT_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_SUPPORT_ROADMAP.md#4-phase-ec-af-1---report-validity-checklist

Notes: |
  The checklist should be usable by future agents without reading Core source.

## T71: Reproducibility Checklist

Owner:      codex
Phase:      15
Type:       docs
Depends-On: T70
Status:     done 2026-05-12

Objective: |
  Define how product agents rerun the same inputs, compare deterministic
  outputs, and document accepted nondeterminism for reports.

Acceptance-Criteria:
  - id: AC-1
    description: "Checklist defines rerun steps, output hash comparison, and accepted nondeterminism such as timestamps, local paths, external source availability, and manual review timestamps."
    test: "manual-evidence: reproducibility checklist exists."
  - id: AC-2
    description: "Trader guidance states how to confirm the same real audit inputs produce the same material findings."
    test: "manual-evidence: Trader section exists."
  - id: AC-3
    description: "Signal guidance states which public-source/report elements are reproducible and which depend on source availability or manual review."
    test: "manual-evidence: Signal section exists."

Files:
  - docs/core/REPRODUCIBILITY_CHECKLIST.md
  - docs/ARTIFACT_SUPPORT_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_SUPPORT_ROADMAP.md#5-phase-ec-af-2---reproducibility-runner-or-checklist

Notes: |
  Do not build a heavy runner unless a product report proves the checklist is
  insufficient.

## T72: Product Bridge Support Notes

Owner:      codex
Phase:      15
Type:       docs
Depends-On: T71
Status:     done 2026-05-12

Objective: |
  Document narrow Core support boundaries for Trader and Signal artifact
  validation so each product keeps its own product-specific reporting logic.

Acceptance-Criteria:
  - id: AC-1
    description: "Trader bridge notes cover violation record shape, policy/config hash, manifest conventions, report no-claim boundary, and manual validation status."
    test: "manual-evidence: Trader bridge section exists."
  - id: AC-2
    description: "Signal bridge notes cover source/evidence refs, reviewed/draft status language, ambiguity/insufficient-evidence status, and no-advice/no-future-performance boundary."
    test: "manual-evidence: Signal bridge section exists."
  - id: AC-3
    description: "Notes explicitly forbid Core-driven rewrites of Trader or Signal during artifact validation."
    test: "manual-evidence: ownership boundary exists."

Files:
  - docs/core/PRODUCT_ARTIFACT_BRIDGES.md
  - docs/ARTIFACT_SUPPORT_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_SUPPORT_ROADMAP.md#6-phase-ec-af-3---product-bridge-support
  - tests/integration/test_trader_risk_bridge_contract.py

Notes: |
  Add tests only if a bridge becomes code, not for docs-only support notes.

## T73: Internal Review Packet Templates

Owner:      codex
Phase:      15
Type:       docs
Depends-On: T72
Status:     done 2026-05-12

Objective: |
  Provide small shared templates for manual validation and external-delivery
  decisions used by both product workspaces.

Acceptance-Criteria:
  - id: AC-1
    description: "Templates cover real input scope note, manual validation notes, error register, external-delivery decision, redaction approval, and pilot feedback log."
    test: "manual-evidence: templates exist or required headings are documented."
  - id: AC-2
    description: "Templates are short and product-neutral enough for Trader and Signal to reuse without rewriting."
    test: "manual-evidence: template review."
  - id: AC-3
    description: "Docs state whether the canonical template lives in Core or product-local copies are preferred."
    test: "manual-evidence: ownership note exists."

Files:
  - docs/templates/ARTIFACT_SCOPE_NOTE.md
  - docs/templates/MANUAL_VALIDATION_NOTES.md
  - docs/templates/ERROR_REGISTER.md
  - docs/templates/EXTERNAL_DELIVERY_DECISION.md
  - docs/ARTIFACT_SUPPORT_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_SUPPORT_ROADMAP.md#7-phase-ec-af-4---internal-review-packet-templates

Notes: |
  Templates must not encourage committing raw private/customer data.

## T74: Core Artifact Support Review And Platformization Gate

Owner:      codex
Phase:      15
Type:       review
Depends-On: T73
Status:     done 2026-05-12

Objective: |
  Review Phase 15 artifact-support outputs and decide whether Core should stay
  hidden/internal, expose an internal SDK surface, or remain frozen until
  Trader/Signal reports validate.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes contract, checklist, reproducibility guidance, bridge notes, templates, freeze list, and product adoption readiness."
    test: "manual-evidence: Phase 15 review exists."
  - id: AC-2
    description: "Review records that Core remains internal unless repeated product artifacts prove platformization demand."
    test: "manual-evidence: platformization decision exists."
  - id: AC-3
    description: "CODEX prompt, README, evidence index, audit index, and handoff docs are updated with the Phase 15 decision and next boundary."
    test: "manual/docs-review."

Files:
  - docs/audit/ARTIFACT_SUPPORT_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/EVIDENCE_INDEX.md
  - README.md
  - PHASE_HANDOFF.md

Context-Refs:
  - docs/ARTIFACT_SUPPORT_ROADMAP.md#9-phase-ec-af-6---platformization-decision-gate
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This task must not approve live, holdout, OOS, hosted service, public SDK, or
  execution scope by implication.

## T75: Artifact Contract V1 Schema

Owner:      codex
Phase:      16
Type:       code
Depends-On: T74
Status:     done 2026-05-14

Objective: |
  Implement the executable Pydantic model for `entropy-core-artifact/v1` so the
  Phase 15 Markdown contract has a machine-checkable authority.

Acceptance-Criteria:
  - id: AC-1
    description: "`ArtifactContractV1` accepts every required field named in `docs/core/ARTIFACT_CONTRACT.md` and rejects unknown fields."
    test: "tests/unit/test_artifact_contract_v1.py::test_contract_accepts_required_fields_and_rejects_extra"
  - id: AC-2
    description: "Manual validation and external delivery states are restricted to the frozen Phase 15 vocabularies."
    test: "tests/unit/test_artifact_contract_v1.py::test_contract_rejects_unknown_decision_states"
  - id: AC-3
    description: "Unsafe claim labels such as production, capital-ready, investment advice, holdout approval, live execution, or future performance are rejected unless explicitly represented as blocked no-claim boundaries."
    test: "tests/unit/test_artifact_contract_v1.py::test_contract_rejects_unsafe_claim_labels"

Files:
  - src/entropy/artifacts/__init__.py
  - src/entropy/artifacts/contract.py
  - tests/unit/test_artifact_contract_v1.py

Context-Refs:
  - docs/core/ARTIFACT_CONTRACT.md
  - docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules

Notes: |
  This is Core schema work only. Do not add product-specific report generation.

## T76: Artifact Loader And Validation Result

Owner:      codex
Phase:      16
Type:       code
Depends-On: T75
Status:     done 2026-05-14

Objective: |
  Add deterministic JSON/YAML loading and a stable validation result object
  that reports errors without leaking private artifact payloads.

Acceptance-Criteria:
  - id: AC-1
    description: "JSON and YAML artifact files load into the same normalized `ArtifactContractV1` model."
    test: "tests/unit/test_artifact_validation.py::test_json_and_yaml_load_to_same_model"
  - id: AC-2
    description: "Invalid files return deterministic validation errors containing path, code, severity, and message."
    test: "tests/unit/test_artifact_validation.py::test_invalid_artifact_returns_deterministic_errors"
  - id: AC-3
    description: "Validation errors do not print raw private input payloads, secrets, or full source contents."
    test: "tests/unit/test_artifact_validation.py::test_validation_errors_do_not_leak_payloads"

Files:
  - src/entropy/artifacts/validation.py
  - tests/unit/test_artifact_validation.py
  - tests/fixtures/artifacts/

Context-Refs:
  - docs/core/REPORT_VALIDITY_CHECKLIST.md

Notes: |
  Prefer PyYAML only if already available or explicitly added to dependencies.
  Otherwise support JSON first and document YAML as deferred.

## T77: Artifact Validate CLI

Owner:      codex
Phase:      16
Type:       code
Depends-On: T76
Status:     done 2026-05-14

Objective: |
  Expose executable artifact validation through the local operator CLI.

Acceptance-Criteria:
  - id: AC-1
    description: "`entropy artifact validate <path>` exits 0 for a valid artifact and prints stable JSON by default."
    test: "tests/unit/test_artifact_cli.py::test_artifact_validate_accepts_valid_artifact"
  - id: AC-2
    description: "`entropy artifact validate <path>` exits non-zero for invalid artifacts and includes validation error codes."
    test: "tests/unit/test_artifact_cli.py::test_artifact_validate_rejects_invalid_artifact"
  - id: AC-3
    description: "CLI help exposes the artifact command group without changing existing `health` and `version` behavior."
    test: "tests/unit/test_artifact_cli.py::test_artifact_cli_help_preserves_existing_commands"

Files:
  - src/entropy/cli.py
  - tests/unit/test_artifact_cli.py

Context-Refs:
  - docs/ARCHITECTURE.md#component-table

Notes: |
  Do not add public SDK, service, API server, or product workspace edits.

## T78: Executable Artifact Validation Review

Owner:      codex
Phase:      16
Type:       review
Depends-On: T77
Status:     done 2026-05-14

Objective: |
  Review Phase 16 and decide whether Core can auto-open the artifact registry
  phase.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes schema, loader, CLI, fixtures, validation commands, limitations, and blocked surfaces."
    test: "manual-evidence: `docs/audit/EXECUTABLE_ARTIFACT_VALIDATION_REVIEW.md` exists."
  - id: AC-2
    description: "Evidence index and compact state docs record Phase 16 completion and T79 as the next task."
    test: "manual/docs-review."
  - id: AC-3
    description: "Review explicitly states that Phase 16 does not approve public SDK, hosted service, product runtime ownership, holdout, live, OOS, or capital-ready scope."
    test: "manual-evidence: blocked-scope section exists."

Files:
  - docs/audit/EXECUTABLE_ARTIFACT_VALIDATION_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md
  - docs/AI_LOOP_OPERATING_MODEL.md

Notes: |
  If no P0/P1 finding exists and no human gate is triggered, open Phase 17.

## T79: Artifact Registry Model

Owner:      codex
Phase:      17
Type:       code
Depends-On: T78
Status:     done 2026-05-14

Objective: |
  Define the governed artifact registry record, status vocabulary, and
  append-only event shape.

Acceptance-Criteria:
  - id: AC-1
    description: "Artifact registry records include id, contract version, product/source, validation status, hash set, generated refs, created timestamp, and current governance state."
    test: "tests/unit/test_artifact_registry.py::test_registry_record_requires_governed_fields"
  - id: AC-2
    description: "Corrections are represented as new events or records, not mutation of prior records."
    test: "tests/unit/test_artifact_registry.py::test_registry_corrections_are_append_only"
  - id: AC-3
    description: "Registry model rejects records with missing validation result or unresolved unsafe claims."
    test: "tests/unit/test_artifact_registry.py::test_registry_rejects_unvalidated_or_unsafe_records"

Files:
  - src/entropy/artifacts/registry.py
  - tests/unit/test_artifact_registry.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#registry-append-only

Notes: |
  Start with local file-backed registry unless database persistence is explicitly
  scoped in Phase 23.

## T80: Artifact Register And Show CLI

Owner:      codex
Phase:      17
Type:       code
Depends-On: T79
Status:     done 2026-05-14

Objective: |
  Add local artifact registration and read commands over validated artifact
  records.

Acceptance-Criteria:
  - id: AC-1
    description: "`entropy artifact register <path>` validates and writes an append-only registry event."
    test: "tests/unit/test_artifact_registry_cli.py::test_register_writes_append_only_event"
  - id: AC-2
    description: "`entropy artifact show <artifact_id>` prints metadata and validation status without raw private payloads."
    test: "tests/unit/test_artifact_registry_cli.py::test_show_prints_safe_metadata"
  - id: AC-3
    description: "Duplicate artifact registration is deterministic and either idempotent or rejected with a stable error code."
    test: "tests/unit/test_artifact_registry_cli.py::test_duplicate_registration_is_deterministic"

Files:
  - src/entropy/cli.py
  - src/entropy/artifacts/registry.py
  - tests/unit/test_artifact_registry_cli.py

Context-Refs:
  - docs/AI_LOOP_OPERATING_MODEL.md

Notes: |
  Keep output machine-readable by default.

## T81: Artifact List And History CLI

Owner:      codex
Phase:      17
Type:       code
Depends-On: T80
Status:     done 2026-05-14

Objective: |
  Add safe local listing and event-history inspection for registered artifacts.

Acceptance-Criteria:
  - id: AC-1
    description: "`entropy artifact list` shows ids, product/source, status, contract version, and timestamps without private payload fields."
    test: "tests/unit/test_artifact_registry_cli.py::test_list_prints_safe_summary"
  - id: AC-2
    description: "`entropy artifact history <artifact_id>` shows append-only validation and correction events in deterministic order."
    test: "tests/unit/test_artifact_registry_cli.py::test_history_prints_append_only_events"
  - id: AC-3
    description: "Missing artifact ids fail with a stable not-found error."
    test: "tests/unit/test_artifact_registry_cli.py::test_history_rejects_missing_id"

Files:
  - src/entropy/cli.py
  - src/entropy/artifacts/registry.py
  - tests/unit/test_artifact_registry_cli.py

Context-Refs:
  - docs/core/ARTIFACT_CONTRACT.md

Notes: |
  This is still local/internal operator tooling, not public platform behavior.

## T82: Artifact Registry Review

Owner:      codex
Phase:      17
Type:       review
Depends-On: T81
Status:     done 2026-05-14

Objective: |
  Review the artifact registry phase and open reproducibility work if registry
  semantics are stable.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes registry model, register/show/list/history commands, append-only behavior, validation, and limitations."
    test: "manual-evidence: registry review exists."
  - id: AC-2
    description: "Review records whether local file-backed registry remains sufficient until Phase 23."
    test: "manual-evidence: storage decision note exists."
  - id: AC-3
    description: "State docs open T83 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/ARTIFACT_REGISTRY_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  Do not introduce database persistence before Phase 23.

## T83: Reproducibility Manifest Schema

Owner:      codex
Phase:      18
Type:       code
Depends-On: T82
Status:     done 2026-05-14

Objective: |
  Define the manifest that tells Core how an artifact can be rerun, compared,
  or declared partially/non-reproducible.

Acceptance-Criteria:
  - id: AC-1
    description: "Reproducibility manifests declare command, input refs, expected output refs, hash policy, volatile fields, and accepted nondeterminism."
    test: "tests/unit/test_reproducibility_manifest.py::test_manifest_requires_rerun_contract_fields"
  - id: AC-2
    description: "Manifests reject unrestricted shell commands, missing hash policy, or undeclared volatile fields."
    test: "tests/unit/test_reproducibility_manifest.py::test_manifest_rejects_unsafe_or_incomplete_contracts"
  - id: AC-3
    description: "Artifacts may explicitly declare non-reproducible fields without hiding that status."
    test: "tests/unit/test_reproducibility_manifest.py::test_manifest_accepts_declared_partial_reproducibility"

Files:
  - src/entropy/artifacts/reproducibility.py
  - tests/unit/test_reproducibility_manifest.py

Context-Refs:
  - docs/core/REPRODUCIBILITY_CHECKLIST.md

Notes: |
  Rerun commands must stay local and deterministic. No external side effects.

## T84: Artifact Hash Compare Runner

Owner:      codex
Phase:      18
Type:       code
Depends-On: T83
Status:     done 2026-05-14

Objective: |
  Implement deterministic hash comparison and material-equivalence
  classification for artifact outputs.

Acceptance-Criteria:
  - id: AC-1
    description: "Runner classifies exact, materially equivalent, partial, declared non-reproducible, and failed reproduction states."
    test: "tests/unit/test_reproducibility_runner.py::test_runner_classifies_reproduction_states"
  - id: AC-2
    description: "Hash comparisons ignore only fields explicitly declared volatile in the manifest."
    test: "tests/unit/test_reproducibility_runner.py::test_runner_ignores_only_declared_volatile_fields"
  - id: AC-3
    description: "Failed comparisons include stable diff metadata without raw private payload dumps."
    test: "tests/unit/test_reproducibility_runner.py::test_failed_compare_reports_safe_metadata"

Files:
  - src/entropy/artifacts/reproducibility.py
  - tests/unit/test_reproducibility_runner.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#hash-and-run-reproducibility

Notes: |
  Do not execute arbitrary shell commands in this task unless command execution
  is explicitly sandboxed and tested.

## T85: Reproducibility CLI

Owner:      codex
Phase:      18
Type:       code
Depends-On: T84
Status:     done 2026-05-14

Objective: |
  Expose artifact reproduction and comparison through CLI commands.

Acceptance-Criteria:
  - id: AC-1
    description: "`entropy artifact compare <artifact_id> --against <path>` prints a deterministic reproduction status."
    test: "tests/unit/test_reproducibility_cli.py::test_compare_prints_reproduction_status"
  - id: AC-2
    description: "`entropy artifact reproduce <artifact_id>` refuses artifacts without an approved local reproducibility manifest."
    test: "tests/unit/test_reproducibility_cli.py::test_reproduce_requires_manifest"
  - id: AC-3
    description: "CLI output records limitations and declared nondeterminism."
    test: "tests/unit/test_reproducibility_cli.py::test_cli_records_limitations"

Files:
  - src/entropy/cli.py
  - src/entropy/artifacts/reproducibility.py
  - tests/unit/test_reproducibility_cli.py

Context-Refs:
  - docs/core/REPRODUCIBILITY_CHECKLIST.md

Notes: |
  If direct rerun execution is too risky, implement compare-only behavior first
  and document rerun execution as blocked.

## T86: Reproducibility Runner Review

Owner:      codex
Phase:      18
Type:       review
Depends-On: T85
Status:     done 2026-05-14

Objective: |
  Review reproducibility work and open evidence pipeline work if status
  classification is stable.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes manifest, compare runner, CLI, status taxonomy, limitations, and safety boundaries."
    test: "manual-evidence: reproducibility runner review exists."
  - id: AC-2
    description: "Review records whether direct rerun execution is approved, deferred, or limited to compare-only behavior."
    test: "manual-evidence: rerun execution decision exists."
  - id: AC-3
    description: "State docs open T87 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  Do not let reproducibility status imply performance or pilot approval.

## T87: Evidence Packet Schema

Owner:      codex
Phase:      19
Type:       code
Depends-On: T86
Status:     done 2026-05-14

Objective: |
  Define the machine-readable evidence packet emitted for validated and
  registered artifacts.

Acceptance-Criteria:
  - id: AC-1
    description: "Evidence packets include artifact summary, validation result, registry status, reproducibility status, limitations, claim boundary, and review refs."
    test: "tests/unit/test_artifact_evidence_packet.py::test_evidence_packet_requires_core_sections"
  - id: AC-2
    description: "Evidence packets serialize deterministically with stable key ordering."
    test: "tests/unit/test_artifact_evidence_packet.py::test_evidence_packet_serializes_deterministically"
  - id: AC-3
    description: "Evidence packets reject approval states not supported by registry/governance history."
    test: "tests/unit/test_artifact_evidence_packet.py::test_evidence_packet_rejects_unsupported_approval_state"

Files:
  - src/entropy/artifacts/evidence.py
  - tests/unit/test_artifact_evidence_packet.py

Context-Refs:
  - docs/core/REPORT_VALIDITY_CHECKLIST.md

Notes: |
  Evidence packets explain status; they do not grant external delivery approval.

## T88: Evidence Build And Inspect CLI

Owner:      codex
Phase:      19
Type:       code
Depends-On: T87
Status:     done 2026-05-14

Objective: |
  Add CLI commands that build and inspect artifact evidence packets.

Acceptance-Criteria:
  - id: AC-1
    description: "`entropy evidence build <artifact_id>` writes a deterministic evidence packet."
    test: "tests/unit/test_artifact_evidence_cli.py::test_evidence_build_writes_packet"
  - id: AC-2
    description: "`entropy evidence inspect <artifact_id>` prints safe summary fields."
    test: "tests/unit/test_artifact_evidence_cli.py::test_evidence_inspect_prints_safe_summary"
  - id: AC-3
    description: "Evidence build fails when artifact validation, registry, or reproducibility prerequisites are inconsistent."
    test: "tests/unit/test_artifact_evidence_cli.py::test_evidence_build_fails_inconsistent_prerequisites"

Files:
  - src/entropy/cli.py
  - src/entropy/artifacts/evidence.py
  - tests/unit/test_artifact_evidence_cli.py

Context-Refs:
  - docs/EVIDENCE_INDEX.md

Notes: |
  Keep evidence packet output local and internal.

## T89: Evidence Index Automation

Owner:      codex
Phase:      19
Type:       code
Depends-On: T88
Status:     done 2026-05-14

Objective: |
  Add a safe helper for indexing generated evidence packets without making the
  Markdown evidence index the source of truth.

Acceptance-Criteria:
  - id: AC-1
    description: "Evidence index helper verifies referenced files exist before emitting or updating rows."
    test: "tests/unit/test_artifact_evidence_index.py::test_index_helper_requires_existing_refs"
  - id: AC-2
    description: "Helper emits deterministic rows for artifact validation, registry, reproducibility, and evidence packet outputs."
    test: "tests/unit/test_artifact_evidence_index.py::test_index_helper_emits_deterministic_rows"
  - id: AC-3
    description: "Helper refuses to mark pending or missing artifacts as canonical proof."
    test: "tests/unit/test_artifact_evidence_index.py::test_index_helper_rejects_missing_canonical_proof"

Files:
  - src/entropy/artifacts/evidence_index.py
  - tests/unit/test_artifact_evidence_index.py

Context-Refs:
  - docs/EVIDENCE_INDEX.md

Notes: |
  The helper may generate row text; human or task code still controls final docs.

## T90: Evidence Pipeline Review

Owner:      codex
Phase:      19
Type:       review
Depends-On: T89
Status:     done 2026-05-14

Objective: |
  Review evidence packet and index automation work, then open product bridge
  profile hardening.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes evidence schemas, CLI, index helper, validation, limitations, and blocked claim surfaces."
    test: "manual-evidence: evidence pipeline review exists."
  - id: AC-2
    description: "Review includes at least one generated evidence packet path."
    test: "manual-evidence: generated packet path exists."
  - id: AC-3
    description: "State docs open T91 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/EVIDENCE_PIPELINE_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  Do not let evidence packet creation become external delivery approval.

## T91: Product Bridge Profile Model

Owner:      codex
Phase:      20
Type:       code
Depends-On: T90
Status:     done 2026-05-14

Objective: |
  Add narrow product profile overlays that validate product-shaped artifacts
  without moving product-specific logic into Core.

Acceptance-Criteria:
  - id: AC-1
    description: "Profiles exist for `generic`, `trader-risk-audit`, and `signal-analytics-sandbox`."
    test: "tests/unit/test_product_bridge_profiles.py::test_known_profiles_exist"
  - id: AC-2
    description: "Profile overlays add allowed and forbidden no-claim labels without changing the base artifact contract."
    test: "tests/unit/test_product_bridge_profiles.py::test_profiles_overlay_claim_boundaries"
  - id: AC-3
    description: "Unknown profiles are rejected with a stable error."
    test: "tests/unit/test_product_bridge_profiles.py::test_unknown_profile_rejected"

Files:
  - src/entropy/artifacts/profiles.py
  - tests/unit/test_product_bridge_profiles.py

Context-Refs:
  - docs/core/PRODUCT_ARTIFACT_BRIDGES.md

Notes: |
  Profiles validate shape and boundaries only. They do not generate product
  reports.

## T92: Profile-Aware Validation CLI

Owner:      codex
Phase:      20
Type:       code
Depends-On: T91
Status:     done 2026-05-14

Objective: |
  Add `--profile` support to artifact validation and registration commands.

Acceptance-Criteria:
  - id: AC-1
    description: "`entropy artifact validate <path> --profile trader-risk-audit` applies Trader-specific blocked-surface checks."
    test: "tests/unit/test_product_bridge_profile_cli.py::test_trader_profile_validation_applies_boundaries"
  - id: AC-2
    description: "`entropy artifact validate <path> --profile signal-analytics-sandbox` applies Signal-specific no-advice/no-future-performance checks."
    test: "tests/unit/test_product_bridge_profile_cli.py::test_signal_profile_validation_applies_boundaries"
  - id: AC-3
    description: "Profile-aware validation keeps product-specific optional fields outside the Core base schema."
    test: "tests/unit/test_product_bridge_profile_cli.py::test_profile_validation_does_not_absorb_product_schema"

Files:
  - src/entropy/cli.py
  - src/entropy/artifacts/profiles.py
  - tests/unit/test_product_bridge_profile_cli.py

Context-Refs:
  - docs/core/PRODUCT_ARTIFACT_BRIDGES.md

Notes: |
  Do not edit Trader or Signal workspaces from this task.

## T93: Product-Shaped Artifact Fixtures

Owner:      codex
Phase:      20
Type:       test
Depends-On: T92
Status:     done 2026-05-14

Objective: |
  Add redacted/synthetic product-shaped fixture artifacts that exercise bridge
  profile validation.

Acceptance-Criteria:
  - id: AC-1
    description: "Trader-shaped fixture validates under the Trader profile and fails under unsafe claim variants."
    test: "tests/unit/test_product_bridge_profile_fixtures.py::test_trader_fixture_profile_behavior"
  - id: AC-2
    description: "Signal-shaped fixture validates under the Signal profile and fails under advice/future-performance variants."
    test: "tests/unit/test_product_bridge_profile_fixtures.py::test_signal_fixture_profile_behavior"
  - id: AC-3
    description: "Fixtures contain no real customer, private source, credential, or raw confidential payload data."
    test: "tests/unit/test_product_bridge_profile_fixtures.py::test_profile_fixtures_are_synthetic"

Files:
  - tests/fixtures/artifacts/profiles/
  - tests/unit/test_product_bridge_profile_fixtures.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

Notes: |
  Fixture names may reference product shape, not real product-owned reports.

## T94: Product Bridge Profile Review

Owner:      codex
Phase:      20
Type:       review
Depends-On: T93
Status:     done 2026-05-14

Objective: |
  Review profile hardening and confirm Core remains separate from neighboring
  products.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes profile model, CLI support, fixtures, limitations, and product ownership boundary."
    test: "manual-evidence: product bridge profile review exists."
  - id: AC-2
    description: "Review states that Core may validate product-shaped artifacts but does not own product runtime or report generation."
    test: "manual-evidence: ownership boundary section exists."
  - id: AC-3
    description: "State docs open T95 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/PRODUCT_BRIDGE_PROFILE_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/core/PRODUCT_ARTIFACT_BRIDGES.md

Notes: |
  Do not interpret product-shaped fixtures as pilot-ready product artifacts.

## T95: Artifact Governance State Model

Owner:      codex
Phase:      21
Type:       code
Depends-On: T94
Status:     done 2026-05-14

Objective: |
  Define deterministic artifact governance states and transition rules.

Acceptance-Criteria:
  - id: AC-1
    description: "State model includes draft, validated_internal, blocked, needs_manual_review, approved_for_controlled_external_pilot, rejected, and superseded."
    test: "tests/unit/test_artifact_governance_state.py::test_state_model_lists_required_states"
  - id: AC-2
    description: "Forbidden transitions such as invalid to external pilot approval are rejected."
    test: "tests/unit/test_artifact_governance_state.py::test_forbidden_transitions_rejected"
  - id: AC-3
    description: "External pilot approval requires a human approval event reference."
    test: "tests/unit/test_artifact_governance_state.py::test_external_pilot_requires_human_approval_event"

Files:
  - src/entropy/artifacts/governance.py
  - tests/unit/test_artifact_governance_state.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#deterministic-runtime-truth

Notes: |
  This does not approve actual external delivery; it models the gate.

## T96: Governance Transition CLI

Owner:      codex
Phase:      21
Type:       code
Depends-On: T95
Status:     done 2026-05-14

Objective: |
  Add local CLI commands for governed artifact state transitions and history.

Acceptance-Criteria:
  - id: AC-1
    description: "`entropy governance transition <artifact_id> --to <state>` records append-only transition events."
    test: "tests/unit/test_artifact_governance_cli.py::test_transition_records_append_only_event"
  - id: AC-2
    description: "Invalid transitions fail before any event is written."
    test: "tests/unit/test_artifact_governance_cli.py::test_invalid_transition_fails_before_write"
  - id: AC-3
    description: "`entropy governance history <artifact_id>` prints deterministic transition history."
    test: "tests/unit/test_artifact_governance_cli.py::test_history_prints_deterministic_transitions"

Files:
  - src/entropy/cli.py
  - src/entropy/artifacts/governance.py
  - tests/unit/test_artifact_governance_cli.py

Context-Refs:
  - docs/AI_LOOP_OPERATING_MODEL.md

Notes: |
  Transition commands must not create approval events by implication.

## T97: Approval Event Binding

Owner:      codex
Phase:      21
Type:       code
Depends-On: T96
Status:     done 2026-05-14

Objective: |
  Bind artifact governance transitions to explicit human approval event
  references where required.

Acceptance-Criteria:
  - id: AC-1
    description: "Approval-bound transitions require approval id, approver, scope, maximum effect, timestamp, and blocked surfaces."
    test: "tests/unit/test_artifact_approval_binding.py::test_approval_bound_transitions_require_event_fields"
  - id: AC-2
    description: "Approval scopes outside artifact validation and controlled external pilot are rejected unless future tasks explicitly add them."
    test: "tests/unit/test_artifact_approval_binding.py::test_approval_binding_rejects_scope_expansion"
  - id: AC-3
    description: "Approval binding preserves no live, no holdout, no broker/exchange, no production, and no capital-ready surfaces by default."
    test: "tests/unit/test_artifact_approval_binding.py::test_approval_binding_preserves_restricted_boundaries"

Files:
  - src/entropy/artifacts/governance.py
  - tests/unit/test_artifact_approval_binding.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries

Notes: |
  Approval event binding is an audit mechanism, not a product delivery decision.

## T98: Governance State Machine Review

Owner:      codex
Phase:      21
Type:       review
Depends-On: T97
Status:     done 2026-05-14

Objective: |
  Review artifact governance state machine and open research integration work.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes state model, transition CLI, approval binding, append-only behavior, and blocked surfaces."
    test: "manual-evidence: governance state machine review exists."
  - id: AC-2
    description: "Review confirms no state creates live, holdout, broker/exchange, production, capital-ready, or performance claims."
    test: "manual-evidence: blocked-surface section exists."
  - id: AC-3
    description: "State docs open T99 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/ARTIFACT_GOVERNANCE_STATE_MACHINE_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  This phase enables governance mechanics, not external product launch.

## T99: Research Artifact Schemas

Owner:      codex
Phase:      22
Type:       code
Depends-On: T98
Status:     done 2026-05-14

Objective: |
  Represent Core research candidate, dataset, evaluation, and report outputs as
  artifact-contract-compatible objects.

Acceptance-Criteria:
  - id: AC-1
    description: "Research artifact schemas bind candidate id, dataset hash, code hash, policy hash, leakage status, and no-claim labels."
    test: "tests/unit/test_research_artifact_schemas.py::test_research_artifacts_bind_required_hashes"
  - id: AC-2
    description: "Research artifacts reject OOS/performance labels when holdout/leakage gates are absent."
    test: "tests/unit/test_research_artifact_schemas.py::test_research_artifacts_reject_unsupported_claims"
  - id: AC-3
    description: "Existing archive-only research packets can be represented without changing their historical meaning."
    test: "tests/unit/test_research_artifact_schemas.py::test_existing_archive_packets_map_to_no_claim_artifacts"

Files:
  - src/entropy/artifacts/research.py
  - tests/unit/test_research_artifact_schemas.py

Context-Refs:
  - docs/core/PROTOCOL_SPEC.md
  - docs/IMPLEMENTATION_CONTRACT.md#leakage-and-holdout-boundary

Notes: |
  This does not open holdout or create new evaluation claims.

## T100: Research Artifact Adapter

Owner:      codex
Phase:      22
Type:       code
Depends-On: T99
Status:     done 2026-05-14

Objective: |
  Add adapters that convert existing Core research/evidence packet objects into
  artifact validation inputs.

Acceptance-Criteria:
  - id: AC-1
    description: "Adapter converts existing archive-only research evidence into `ArtifactContractV1`-compatible payloads."
    test: "tests/unit/test_research_artifact_adapter.py::test_archive_packet_converts_to_artifact_payload"
  - id: AC-2
    description: "Adapter preserves no-claim labels and blocked surfaces."
    test: "tests/unit/test_research_artifact_adapter.py::test_adapter_preserves_no_claim_boundaries"
  - id: AC-3
    description: "Adapter fails when required dataset, code, policy, or report hashes are unresolved."
    test: "tests/unit/test_research_artifact_adapter.py::test_adapter_rejects_unresolved_hashes"

Files:
  - src/entropy/artifacts/research.py
  - tests/unit/test_research_artifact_adapter.py

Context-Refs:
  - docs/research/

Notes: |
  Do not rewrite research packet generation in this task.

## T101: Research Artifact Validation Fixtures

Owner:      codex
Phase:      22
Type:       test
Depends-On: T100
Status:     done 2026-05-14

Objective: |
  Add synthetic fixtures that exercise research artifact validation paths.

Acceptance-Criteria:
  - id: AC-1
    description: "Valid no-claim research artifact fixture passes validation."
    test: "tests/unit/test_research_artifact_fixtures.py::test_valid_research_artifact_fixture_passes"
  - id: AC-2
    description: "Unsafe OOS/performance and holdout variants fail validation."
    test: "tests/unit/test_research_artifact_fixtures.py::test_unsafe_research_claim_variants_fail"
  - id: AC-3
    description: "Fixtures contain no real private strategy payloads."
    test: "tests/unit/test_research_artifact_fixtures.py::test_research_fixtures_are_synthetic"

Files:
  - tests/fixtures/artifacts/research/
  - tests/unit/test_research_artifact_fixtures.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

Notes: |
  Research fixtures may be synthetic but must preserve realistic hash-binding
  shape.

## T102: Research Evaluation Integration Review

Owner:      codex
Phase:      22
Type:       review
Depends-On: T101
Status:     done 2026-05-14

Objective: |
  Review research artifact integration and open storage backend work.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes research schemas, adapter, fixtures, no-claim behavior, and unresolved gaps."
    test: "manual-evidence: research integration review exists."
  - id: AC-2
    description: "Review confirms no holdout read/unlock or OOS/performance label has been opened."
    test: "manual-evidence: blocked-holdout section exists."
  - id: AC-3
    description: "State docs open T103 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/RESEARCH_ARTIFACT_INTEGRATION_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  Phase 22 is integration into artifact governance, not research claim expansion.

## T103: Artifact Metadata Migration

Owner:      codex
Phase:      23
Type:       code
Depends-On: T102
Status:     done 2026-05-14

Objective: |
  Add database metadata tables for artifact records, validation events,
  reproducibility events, evidence packets, and governance transitions.

Acceptance-Criteria:
  - id: AC-1
    description: "Alembic migration adds artifact metadata tables with append-only event tables."
    test: "tests/integration/test_artifact_metadata_migration.py::test_artifact_metadata_tables_exist"
  - id: AC-2
    description: "Application write paths do not UPDATE or DELETE append-only artifact event tables."
    test: "tests/integration/test_artifact_metadata_migration.py::test_artifact_event_tables_are_append_only"
  - id: AC-3
    description: "Migration does not introduce tenant, auth, hosted service, or public API assumptions."
    test: "tests/integration/test_artifact_metadata_migration.py::test_migration_has_no_saas_assumptions"

Files:
  - migrations/versions/
  - src/entropy/db/models.py
  - tests/integration/test_artifact_metadata_migration.py

Context-Refs:
  - docs/ARCHITECTURE.md#runtime-and-isolation-model
  - docs/IMPLEMENTATION_CONTRACT.md#registry-append-only

Notes: |
  Use existing SQLAlchemy/Alembic patterns. No multi-tenant behavior in this
  task.

## T104: Artifact Store Abstraction

Owner:      codex
Phase:      23
Type:       code
Depends-On: T103
Status:     done 2026-05-14

Objective: |
  Add a filesystem artifact-store abstraction with a future object-store
  boundary but no hosted storage dependency.

Acceptance-Criteria:
  - id: AC-1
    description: "Filesystem store writes content-addressed artifact payloads and returns stable refs."
    test: "tests/unit/test_artifact_store.py::test_filesystem_store_writes_content_addressed_payloads"
  - id: AC-2
    description: "Store rejects path traversal and unsafe absolute path writes."
    test: "tests/unit/test_artifact_store.py::test_store_rejects_unsafe_paths"
  - id: AC-3
    description: "Object-store interface is declared but no external service dependency is required."
    test: "tests/unit/test_artifact_store.py::test_object_store_boundary_has_no_runtime_dependency"

Files:
  - src/entropy/artifacts/store.py
  - tests/unit/test_artifact_store.py

Context-Refs:
  - docs/ARCHITECTURE.md#persistence-model

Notes: |
  Keep local filesystem as the only active backend.

## T105: Metadata Repository

Owner:      codex
Phase:      23
Type:       code
Depends-On: T104
Status:     done 2026-05-14

Objective: |
  Add repository functions that persist artifact metadata and append-only
  events to PostgreSQL when configured.

Acceptance-Criteria:
  - id: AC-1
    description: "Repository inserts artifact metadata and event rows with parameterized SQL/SQLAlchemy calls."
    test: "tests/integration/test_artifact_metadata_repository.py::test_repository_inserts_artifact_metadata"
  - id: AC-2
    description: "Repository rejects mutation operations for append-only events."
    test: "tests/integration/test_artifact_metadata_repository.py::test_repository_has_no_update_delete_event_paths"
  - id: AC-3
    description: "Repository can fall back to local registry behavior when database is not configured."
    test: "tests/unit/test_artifact_metadata_repository.py::test_repository_fallback_without_database"

Files:
  - src/entropy/artifacts/repository.py
  - tests/unit/test_artifact_metadata_repository.py
  - tests/integration/test_artifact_metadata_repository.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#sql-safety

Notes: |
  Do not require PostgreSQL for simple local validation commands.

## T106: Storage And Audit Backend Review

Owner:      codex
Phase:      23
Type:       review
Depends-On: T105
Status:     done 2026-05-14

Objective: |
  Review durable metadata and artifact-store boundaries before any internal
  API/job work.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes migrations, store abstraction, repository behavior, append-only guarantees, and local fallback."
    test: "manual-evidence: storage backend review exists."
  - id: AC-2
    description: "Review confirms no multi-tenant SaaS, public API, or hosted storage behavior was introduced."
    test: "manual-evidence: no-saas section exists."
  - id: AC-3
    description: "State docs open T107 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/STORAGE_AND_AUDIT_BACKEND_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  A service/API remains optional and internal-only after this phase.

## T107: Internal API Boundary ADR

Owner:      codex
Phase:      24
Type:       docs
Depends-On: T106
Status:     done 2026-05-14

Objective: |
  Decide whether Core needs an internal API/job boundary or whether CLI/local
  batch remains sufficient.

Acceptance-Criteria:
  - id: AC-1
    description: "ADR compares CLI-only, internal Python API, FastAPI internal service, and background job options."
    test: "manual-evidence: ADR exists."
  - id: AC-2
    description: "ADR states whether API/job implementation is accepted, deferred, or rejected for this roadmap."
    test: "manual-evidence: decision field exists."
  - id: AC-3
    description: "ADR preserves no public SDK, hosted service, auth, tenant, or external SLA claims."
    test: "manual-evidence: boundary section exists."

Files:
  - docs/adr/ADR-CORE-INTERNAL-API-JOB-BOUNDARY.md

Context-Refs:
  - docs/ARCHITECTURE.md#security-boundaries
  - docs/AI_LOOP_OPERATING_MODEL.md

Notes: |
  If ADR rejects or defers API/jobs, T108-T109 should be rewritten to reinforce
  CLI/library boundaries instead.

## T108: Internal Python API Facade

Owner:      codex
Phase:      24
Type:       code
Depends-On: T107
Status:     done 2026-05-14

Objective: |
  Provide a stable internal Python API facade over validation, registry,
  reproducibility, evidence, and governance operations.

Acceptance-Criteria:
  - id: AC-1
    description: "Facade exposes typed functions for validate, register, compare, build evidence, and transition state."
    test: "tests/unit/test_internal_api_facade.py::test_facade_exposes_core_operations"
  - id: AC-2
    description: "Facade preserves the same validation and governance errors as CLI paths."
    test: "tests/unit/test_internal_api_facade.py::test_facade_matches_cli_error_semantics"
  - id: AC-3
    description: "Facade has no network, auth, or multi-tenant behavior."
    test: "tests/unit/test_internal_api_facade.py::test_facade_has_no_service_surface"

Files:
  - src/entropy/artifacts/api.py
  - tests/unit/test_internal_api_facade.py

Context-Refs:
  - docs/adr/ADR-CORE-INTERNAL-API-JOB-BOUNDARY.md

Notes: |
  This is an internal library facade, not a public SDK.

## T109: Internal Job Model

Owner:      codex
Phase:      24
Type:       code
Depends-On: T108
Status:     done 2026-05-14

Objective: |
  Define an idempotent internal job model for validation/evidence operations
  without adding a worker service unless ADR explicitly approves it.

Acceptance-Criteria:
  - id: AC-1
    description: "Job model records job id, operation, artifact ref, idempotency key, status, result ref, and error code."
    test: "tests/unit/test_internal_job_model.py::test_job_model_requires_idempotency_fields"
  - id: AC-2
    description: "Duplicate idempotency keys return the same job identity or stable duplicate error."
    test: "tests/unit/test_internal_job_model.py::test_job_idempotency_is_deterministic"
  - id: AC-3
    description: "Job execution remains in-process unless ADR explicitly approves a worker runtime."
    test: "tests/unit/test_internal_job_model.py::test_job_model_has_no_worker_runtime_dependency"

Files:
  - src/entropy/artifacts/jobs.py
  - tests/unit/test_internal_job_model.py

Context-Refs:
  - docs/adr/ADR-CORE-INTERNAL-API-JOB-BOUNDARY.md

Notes: |
  Do not add Celery, Redis, Temporal, Kafka, or service containers in this task.

## T110: Internal API And Job Boundary Review

Owner:      codex
Phase:      24
Type:       review
Depends-On: T109
Status:     done 2026-05-14

Objective: |
  Review internal API/job boundary work and decide whether CAF primitives can
  open.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes ADR decision, facade, job model, validation, limitations, and blocked service surfaces."
    test: "manual-evidence: internal API/job boundary review exists."
  - id: AC-2
    description: "Review confirms no public SDK, hosted service, multi-tenant auth, or background worker dependency was introduced unless separately approved."
    test: "manual-evidence: blocked-service section exists."
  - id: AC-3
    description: "State docs open T111 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/INTERNAL_API_JOB_BOUNDARY_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  If API/job scope was deferred, record that clearly and continue to CAF schemas
  through internal library/CLI paths.

## T111: CAF Artifact Vocabulary

Owner:      codex
Phase:      25
Type:       code
Depends-On: T110
Status:     done 2026-05-14

Objective: |
  Define the initial Capital Allocation Framework artifact vocabulary without
  enabling capital movement or investment advice.

Acceptance-Criteria:
  - id: AC-1
    description: "CAF vocabulary includes allocation decision, risk policy, portfolio constraint, decision rationale, and decision evidence bundle artifacts."
    test: "tests/unit/test_caf_artifact_vocabulary.py::test_caf_vocabulary_lists_required_artifacts"
  - id: AC-2
    description: "CAF artifacts require no-claim labels for not investment advice, not live allocation, not capital-ready, and not automated execution."
    test: "tests/unit/test_caf_artifact_vocabulary.py::test_caf_artifacts_require_no_claim_labels"
  - id: AC-3
    description: "CAF vocabulary does not include broker/order/capital execution fields."
    test: "tests/unit/test_caf_artifact_vocabulary.py::test_caf_vocabulary_has_no_execution_fields"

Files:
  - src/entropy/artifacts/caf.py
  - tests/unit/test_caf_artifact_vocabulary.py

Context-Refs:
  - docs/core/CHARTER.md
  - docs/core/PROTOCOL_SPEC.md

Notes: |
  This phase models decision evidence, not trading execution.

## T112: Allocation Decision Artifact Schema

Owner:      codex
Phase:      25
Type:       code
Depends-On: T111
Status:     done 2026-05-14

Objective: |
  Implement the first governed allocation decision artifact schema.

Acceptance-Criteria:
  - id: AC-1
    description: "Allocation decision artifacts bind decision id, portfolio context, constraints, evidence refs, rationale refs, limitations, and no-claim boundaries."
    test: "tests/unit/test_allocation_decision_artifact.py::test_allocation_decision_requires_governed_fields"
  - id: AC-2
    description: "Artifacts reject future-performance, advice, capital-ready, and automated-execution claims."
    test: "tests/unit/test_allocation_decision_artifact.py::test_allocation_decision_rejects_unsafe_claims"
  - id: AC-3
    description: "Four-stream P&L attribution references are supported without blending treasury into net Sharpe."
    test: "tests/unit/test_allocation_decision_artifact.py::test_allocation_decision_preserves_four_stream_boundary"

Files:
  - src/entropy/artifacts/caf.py
  - tests/unit/test_allocation_decision_artifact.py

Context-Refs:
  - docs/core/CHARTER.md#b-non-negotiables

Notes: |
  Do not add portfolio execution, broker APIs, or live allocation logic.

## T113: CAF Validation Fixtures

Owner:      codex
Phase:      25
Type:       test
Depends-On: T112
Status:     done 2026-05-14

Objective: |
  Add synthetic CAF artifacts that exercise allocation decision validation and
  unsafe-claim rejection.

Acceptance-Criteria:
  - id: AC-1
    description: "Valid allocation decision fixture passes base artifact and CAF-specific validation."
    test: "tests/unit/test_caf_artifact_fixtures.py::test_valid_caf_fixture_passes"
  - id: AC-2
    description: "Unsafe live allocation, investment advice, and capital-ready variants fail validation."
    test: "tests/unit/test_caf_artifact_fixtures.py::test_unsafe_caf_variants_fail"
  - id: AC-3
    description: "Fixtures are synthetic and contain no real portfolio, account, customer, or private strategy payloads."
    test: "tests/unit/test_caf_artifact_fixtures.py::test_caf_fixtures_are_synthetic"

Files:
  - tests/fixtures/artifacts/caf/
  - tests/unit/test_caf_artifact_fixtures.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

Notes: |
  Use realistic structure, not real capital data.

## T114: CAF Decision Primitives Review

Owner:      codex
Phase:      25
Type:       review
Depends-On: T113
Status:     done 2026-05-14

Objective: |
  Review CAF primitive schemas and confirm the roadmap can proceed to audit
  readiness.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes CAF vocabulary, allocation decision schema, fixtures, validation, and limitations."
    test: "manual-evidence: CAF decision primitives review exists."
  - id: AC-2
    description: "Review confirms no capital movement, investment advice, live allocation, broker/exchange execution, or production label is approved."
    test: "manual-evidence: no-capital-execution section exists."
  - id: AC-3
    description: "State docs open T115 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/CAF_DECISION_PRIMITIVES_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  CAF primitives are evidence contracts, not execution systems.

## T115: Audit Bundle Schema

Owner:      codex
Phase:      26
Type:       code
Depends-On: T114
Status:     done 2026-05-14

Objective: |
  Define an exportable audit bundle that packages artifact lineage, validation,
  reproducibility, evidence, governance, and limitations.

Acceptance-Criteria:
  - id: AC-1
    description: "Audit bundles include artifact lineage graph, evidence packet refs, validation events, governance events, reviewer notes, and limitations."
    test: "tests/unit/test_audit_bundle.py::test_audit_bundle_requires_lineage_sections"
  - id: AC-2
    description: "Bundles serialize deterministically and include content hashes."
    test: "tests/unit/test_audit_bundle.py::test_audit_bundle_serializes_deterministically"
  - id: AC-3
    description: "Bundles do not claim SOC 2, regulatory certification, investment-advice compliance, or enterprise readiness by default."
    test: "tests/unit/test_audit_bundle.py::test_audit_bundle_rejects_external_certification_claims"

Files:
  - src/entropy/artifacts/audit_bundle.py
  - tests/unit/test_audit_bundle.py

Context-Refs:
  - docs/ARCHITECTURE.md#security-boundaries

Notes: |
  This is enterprise audit readiness, not external compliance certification.

## T116: Lineage Graph Builder

Owner:      codex
Phase:      26
Type:       code
Depends-On: T115
Status:     done 2026-05-14

Objective: |
  Build artifact lineage graphs across input refs, generated refs, registry
  events, evidence packets, and governance transitions.

Acceptance-Criteria:
  - id: AC-1
    description: "Lineage builder returns deterministic graph nodes and edges for artifact refs and events."
    test: "tests/unit/test_lineage_graph.py::test_lineage_graph_is_deterministic"
  - id: AC-2
    description: "Missing refs are represented as explicit unresolved nodes, not silently ignored."
    test: "tests/unit/test_lineage_graph.py::test_lineage_graph_records_unresolved_refs"
  - id: AC-3
    description: "Lineage output avoids raw private payloads."
    test: "tests/unit/test_lineage_graph.py::test_lineage_graph_avoids_private_payloads"

Files:
  - src/entropy/artifacts/lineage.py
  - tests/unit/test_lineage_graph.py

Context-Refs:
  - docs/EVIDENCE_INDEX.md

Notes: |
  Keep graph output simple JSON; no graph database is approved.

## T117: Data Classification And Reviewer Role Model

Owner:      codex
Phase:      26
Type:       code
Depends-On: T116
Status:     done 2026-05-14

Objective: |
  Add lightweight data classification and reviewer-role metadata for audit
  bundles without implementing full RBAC.

Acceptance-Criteria:
  - id: AC-1
    description: "Data classification model distinguishes public, internal, confidential, private/customer, and secret categories."
    test: "tests/unit/test_audit_data_classification.py::test_data_classification_lists_required_categories"
  - id: AC-2
    description: "Reviewer role metadata records reviewer id/ref, role, reviewed sections, decision, timestamp, and limitations."
    test: "tests/unit/test_audit_data_classification.py::test_reviewer_role_metadata_requires_review_fields"
  - id: AC-3
    description: "Model does not implement auth, SSO, RBAC, or tenant isolation."
    test: "tests/unit/test_audit_data_classification.py::test_model_has_no_auth_or_tenant_behavior"

Files:
  - src/entropy/artifacts/audit_bundle.py
  - tests/unit/test_audit_data_classification.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#authorization

Notes: |
  This prepares audit semantics; it is not an authorization system.

## T118: Enterprise Audit Readiness Review

Owner:      codex
Phase:      26
Type:       review
Depends-On: T117
Status:     done 2026-05-14

Objective: |
  Review audit readiness work and decide whether Core V1 productization can
  open.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes audit bundles, lineage, data classification, reviewer roles, limitations, and non-certification boundary."
    test: "manual-evidence: enterprise audit readiness review exists."
  - id: AC-2
    description: "Review states remaining gaps before any external enterprise/compliance claim."
    test: "manual-evidence: enterprise gap section exists."
  - id: AC-3
    description: "State docs open T119 unless P0/P1 findings remain."
    test: "manual/docs-review."

Files:
  - docs/audit/ENTERPRISE_AUDIT_READINESS_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  Do not claim SOC 2, regulated investment-advice compliance, or enterprise SLA.

## T119: Core V1 Surface Freeze

Owner:      codex
Phase:      27
Type:       docs
Depends-On: T118
Status:     done 2026-05-14

Objective: |
  Freeze the Core V1 internal product surface across CLI commands, schemas,
  artifact states, evidence formats, and storage boundaries.

Acceptance-Criteria:
  - id: AC-1
    description: "Surface freeze document lists stable CLI commands, schema versions, state vocabularies, storage boundaries, and unsupported surfaces."
    test: "manual-evidence: Core V1 surface freeze document exists."
  - id: AC-2
    description: "Freeze document distinguishes internal API from public SDK and explicitly keeps public SDK unapproved."
    test: "manual-evidence: public SDK boundary exists."
  - id: AC-3
    description: "Freeze document identifies any schema/version migration required before V1 release."
    test: "manual-evidence: migration section exists."

Files:
  - docs/core/CORE_V1_SURFACE_FREEZE.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md

Notes: |
  This task freezes internal surface only.

## T120: Operator Runbook And Examples

Owner:      codex
Phase:      27
Type:       docs
Depends-On: T119
Status:     done 2026-05-14

Objective: |
  Create operator-facing runbooks and examples for validating, registering,
  reproducing, governing, and exporting artifacts.

Acceptance-Criteria:
  - id: AC-1
    description: "Runbook contains end-to-end command sequences for generic, research, product-shaped, and CAF-shaped artifacts."
    test: "manual-evidence: runbook examples exist."
  - id: AC-2
    description: "Examples use synthetic/redacted fixtures only."
    test: "manual-evidence: examples reference fixture paths only."
  - id: AC-3
    description: "Runbook includes failure handling and blocked-surface guidance."
    test: "manual-evidence: failure and boundary sections exist."

Files:
  - RUNBOOK.md
  - docs/core/CORE_V1_EXAMPLES.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/AI_LOOP_OPERATING_MODEL.md

Notes: |
  Do not include real customer, product, or private research payloads.

## T121: Documentation And Test Alignment Sweep

Owner:      codex
Phase:      27
Type:       docs
Depends-On: T120
Status:     done 2026-05-14

Objective: |
  Align architecture, implementation contract references, task graph, evidence
  index, examples, and test names with the final Core V1 surface.

Acceptance-Criteria:
  - id: AC-1
    description: "Architecture docs match implemented Core V1 components and do not describe unimplemented public service behavior."
    test: "manual/docs-review."
  - id: AC-2
    description: "Evidence index rows for Core V1 capabilities point to existing tests, fixtures, generated packets, or review artifacts."
    test: "manual/docs-review."
  - id: AC-3
    description: "Known obsolete phase anchors are either updated or explicitly preserved as historical anchors."
    test: "manual/docs-review."

Files:
  - docs/ARCHITECTURE.md
  - docs/IMPLEMENTATION_CONTRACT.md
  - docs/EVIDENCE_INDEX.md
  - docs/tasks.md
  - docs/CODEX_PROMPT.md
  - README.md

Context-Refs:
  - docs/core/CORE_V1_SURFACE_FREEZE.md

Notes: |
  Contract changes still require ADR where the implementation contract says so.

## T122: Core V1 Productization Review

Owner:      codex
Phase:      27
Type:       review
Depends-On: T121
Status:     done 2026-05-14

Objective: |
  Final review for Core V1 as a documented, tested internal product kernel and
  roadmap handoff to Core V2 planning.

Acceptance-Criteria:
  - id: AC-1
    description: "Review summarizes Core V1 capabilities, stable surfaces, verification evidence, limitations, open findings, and V2 recommendations."
    test: "manual-evidence: Core V1 productization review exists."
  - id: AC-2
    description: "Review explicitly states which commercial, SaaS, enterprise-compliance, live, holdout, and capital surfaces remain unapproved."
    test: "manual-evidence: unapproved surfaces section exists."
  - id: AC-3
    description: "State docs checkpoint Core V1 and stop automatic roadmap expansion until a new V2 roadmap is approved."
    test: "manual/docs-review."

Files:
  - docs/audit/CORE_V1_PRODUCTIZATION_REVIEW.md
  - docs/EVIDENCE_INDEX.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md
  - README.md

Context-Refs:
  - docs/CORE_12_MONTH_EXECUTION_ROADMAP.md
  - docs/AI_LOOP_OPERATING_MODEL.md

Notes: |
  Core V1 completion is an internal product-kernel milestone, not public SaaS
  launch or enterprise compliance certification.
