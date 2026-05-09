# Task Graph - Trader Risk Audit

Version: 1.3
Last updated: 2026-05-08
Status: Phase 7 active - internal validation with public samples; Phase 8-10 planned for demo quality and pilot conversion

---

## Phase Plan

| Phase | Name | Tasks | Delivery | Gate criteria |
|-------|------|-------|----------|---------------|
| 1 | Foundation | T01-T03 | Python package skeleton, CI contract, and baseline smoke tests. | Phase 1 audit passes; CI file exists; first local test baseline can be established. |
| 2 | Input Contracts | T04-T07 | Canonical trade records, import normalization, risk policy schema, and human review packet. | Supported fixtures normalize deterministically; unsupported or ambiguous inputs fail with explicit errors. |
| 3 | Rule Evaluation | T08-T12 | Aggregation, deterministic rule evaluators, violation records, and P&L attribution. | Golden fixtures prove violation truth, source-row traceability, and reconciled attribution. |
| 4 | Reporting and Artifacts | T13-T16 | Report data model, Markdown output, claim guard, and reproducible manifest hashes. | Reports are generated from deterministic artifacts and blocked when unsupported claims appear. |
| 5 | Concierge Pilot Workflow | T17-T20 | End-to-end CLI, Telegram-ready packet, retention/delete workflow, and pilot regression fixtures. | A local operator can run a complete anonymized audit and reproduce the same artifact hashes. |
| 6 | Pilot Validation and Telegram Intake | T21-T29 | Demo artifacts, pilot intake contracts, local audit workspace conventions, Telegram intake/delivery gate, operator queue, and pilot evidence log. | A user can submit files through a constrained pilot path, an operator can review/run/deliver an audit, and business evidence is captured without live trading scope. |
| 7 | Internal Validation with Public Samples | T30-T32 | Public sample source policy, soft/medium/hard starter policy profiles, reproducible public evidence pack, optional Telegram demo/intake/delivery surface, and internal readiness review before trader outreach. | The team can prove the audit workflow on licensed public/anonymized examples, explain its limits, demo the upload-status-report loop through Telegram where useful, and decide whether to start trader outreach without counting public samples as paid pilot evidence. |
| 8 | Demo Productization | T33-T36 | Telegram happy path, public-sample demo mode, report polish, and two-minute demo scripts. | A prospect can experience a clear mini-product demo from Telegram entry to approved report without confusing the audit with advice, broker control, or signal analytics. |
| 9 | Intake Quality and Operator Speed | T37-T40 | Policy profile selection, intake file validation, operator runbook CLI, and evidence capture automation. | A pilot request can move from user upload to operator-ready workspace quickly, with actionable validation errors and disciplined evidence capture. |
| 10 | Conversion Assets | T41-T44 | Before/after report comparison, objection handling, ICP-specific demo variants, and paid pilot offer page. | The founder can run manual sales calls with concrete assets that explain value, reduce trust objections, and ask for a paid pilot without overclaiming. |

---

## Loop Continuation Rule

The orchestrator should not stop just because a planned phase ends. At each phase boundary:

1. Run the mandatory strategy/deep review required by `docs/prompts/ORCHESTRATOR.md`.
2. Archive the review and update audit indexes/state docs.
3. Apply required fixes for any stop-ship or accepted findings.
4. If no stop-ship finding remains, advance `docs/CODEX_PROMPT.md` to the next planned phase/task and continue the loop.
5. If review findings, pilot evidence, or implementation discoveries show that the roadmap should change, update this task graph, `docs/CODEX_PROMPT.md`, README, and relevant audit notes before continuing.

Do not wait for a separate user instruction between planned phases unless the next phase would add forbidden scope, require a new ADR, or contradict current validation evidence.

---

## T01: Project Skeleton

Owner:      codex
Phase:      1
Type:       none
Depends-On: none

Objective: |
  Create the Python package skeleton, local CLI entry point, configuration loader, shared observability module, dependency files, and initial package import tests needed for all later implementation tasks.

Acceptance-Criteria:
  - id: AC-1
    description: "Importing `trader_risk_audit` exposes a non-empty `__version__` string."
    test: "tests/test_project_skeleton.py::test_package_exposes_version"
  - id: AC-2
    description: "`python -m trader_risk_audit --version` exits with code 0 and includes the package version in stdout."
    test: "tests/test_project_skeleton.py::test_module_version_command"
  - id: AC-3
    description: "The config loader defaults `TRA_LIVE_BROKER_API_ENABLED` and `TRA_ORDER_BLOCKING_ENABLED` to false and rejects true values with a configuration error."
    test: "tests/test_project_skeleton.py::test_config_rejects_live_trading_flags"

Files:
  - pyproject.toml
  - requirements.txt
  - requirements-dev.txt
  - trader_risk_audit/__init__.py
  - trader_risk_audit/__main__.py
  - trader_risk_audit/cli.py
  - trader_risk_audit/config.py
  - trader_risk_audit/observability.py
  - tests/test_project_skeleton.py

Context-Refs:
  - docs/DECISION_LOG.md#D-001
  - docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules

Notes: |
  Do not add broker clients, network services, databases, background workers, or report logic in this task. Keep the CLI command bodies skeletal but executable.

## T02: CI Setup

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01

Objective: |
  Add the GitHub Actions workflow and local CI contract checks that install the package, run ruff linting, verify ruff formatting, and execute pytest against the product package and tests.

Acceptance-Criteria:
  - id: AC-1
    description: "`.github/workflows/ci.yml` specifies Python 3.12 and installs with `pip install -r requirements-dev.txt -e .`."
    test: "tests/test_ci_contract.py::test_ci_uses_python_312_and_editable_install"
  - id: AC-2
    description: "`.github/workflows/ci.yml` contains separate steps for `ruff check`, `ruff format --check`, and `python -m pytest`."
    test: "tests/test_ci_contract.py::test_ci_has_lint_format_and_pytest_steps"
  - id: AC-3
    description: "The CI workflow does not define broker, exchange, Telegram, or other external service credentials."
    test: "tests/test_ci_contract.py::test_ci_has_no_runtime_external_credentials"

Files:
  - .github/workflows/ci.yml
  - tests/test_ci_contract.py

Context-Refs:
  - docs/DECISION_LOG.md#D-002

Notes: |
  The workflow may use local-only environment defaults. Do not add service containers unless a later task introduces a tested local database.

## T03: Baseline Smoke Tests

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01, T02

Objective: |
  Establish the first smoke test baseline for the package, CLI command surface, and shared observability boundary before domain behavior is added.

Acceptance-Criteria:
  - id: AC-1
    description: "The package imports without importing pandas, polars, network clients, or Telegram dependencies at import time."
    test: "tests/test_baseline_smoke.py::test_import_has_no_heavy_runtime_dependencies"
  - id: AC-2
    description: "The CLI help output lists the `audit`, `manifest`, and `retention` command groups or stubs."
    test: "tests/test_baseline_smoke.py::test_cli_help_lists_initial_command_surface"
  - id: AC-3
    description: "`get_tracer()` returns an object with `start_as_current_span` so later code uses one shared tracing boundary."
    test: "tests/test_baseline_smoke.py::test_shared_tracer_interface_exists"

Files:
  - trader_risk_audit/cli.py
  - trader_risk_audit/observability.py
  - tests/test_baseline_smoke.py

Context-Refs:
  - docs/CODEX_PROMPT.md#current-state

Notes: |
  After this task, update `docs/CODEX_PROMPT.md` with the passing test count.

## T04: Canonical Trade Schema

Owner:      codex
Phase:      2
Type:       none
Depends-On: T03

Objective: |
  Define the canonical trade record schema, side normalization, row identifiers, validation errors, and anonymized fixture records used by importers and evaluators.

Acceptance-Criteria:
  - id: AC-1
    description: "A valid trade record accepts timestamp, symbol, side, quantity, price, fees, account id, source file, and source row number, then exposes a stable `row_id`."
    test: "tests/unit/trades/test_trade_schema.py::test_valid_trade_record_generates_stable_row_id"
  - id: AC-2
    description: "Invalid records missing timestamp, symbol, side, quantity, or price return validation errors naming each missing canonical field."
    test: "tests/unit/trades/test_trade_schema.py::test_missing_required_fields_report_canonical_names"
  - id: AC-3
    description: "Side normalization accepts only configured buy/sell aliases and rejects unknown side values without coercing them."
    test: "tests/unit/trades/test_trade_schema.py::test_side_normalization_rejects_unknown_values"

Files:
  - trader_risk_audit/trades/__init__.py
  - trader_risk_audit/trades/schema.py
  - tests/unit/trades/test_trade_schema.py
  - tests/fixtures/trades/valid_trades.csv

Context-Refs:
  - docs/ARCHITECTURE.md#component-table

Notes: |
  Keep source row references separate from generated `row_id` so importer errors can point back to the original export.

## T05: Trade Export Importer

Owner:      codex
Phase:      2
Type:       none
Depends-On: T04

Objective: |
  Implement supported CSV import normalization from broker-like exports into canonical trade records with deterministic output ordering and explicit unsupported-column errors.

Acceptance-Criteria:
  - id: AC-1
    description: "A supported CSV fixture normalizes into canonical records sorted by timestamp and source row number."
    test: "tests/unit/trades/test_importers.py::test_supported_csv_normalizes_to_canonical_records"
  - id: AC-2
    description: "A fixture missing required source columns fails with an error listing missing canonical fields and inspected source columns."
    test: "tests/unit/trades/test_importers.py::test_missing_source_columns_return_inspected_columns"
  - id: AC-3
    description: "Normalizing the same fixture twice produces byte-identical JSON serialization."
    test: "tests/unit/trades/test_importers.py::test_import_output_is_byte_identical_across_runs"

Files:
  - trader_risk_audit/trades/importers.py
  - tests/unit/trades/test_importers.py
  - tests/fixtures/trades/supported_export.csv
  - tests/fixtures/trades/missing_columns_export.csv

Context-Refs:
  - docs/DECISION_LOG.md#D-003

Notes: |
  Do not implement live broker APIs. XLSX support may be added later behind the same interface if pilot exports require it.

## T06: Risk Policy Schema

Owner:      codex
Phase:      2
Type:       none
Depends-On: T04

Objective: |
  Define the versioned risk policy schema with supported rule types, thresholds, units, account scope, timezone/session data, and stable rule ids.

Acceptance-Criteria:
  - id: AC-1
    description: "A valid policy fixture loads with schema version, account scope, timezone, session definition, and at least one supported rule."
    test: "tests/unit/policy/test_policy_schema.py::test_valid_policy_fixture_loads_required_fields"
  - id: AC-2
    description: "Unsupported rule types fail validation with the offending rule id and unsupported type."
    test: "tests/unit/policy/test_policy_schema.py::test_unsupported_rule_type_reports_rule_id"
  - id: AC-3
    description: "Every accepted rule exposes a stable `rule_id` used unchanged in serialized policy output."
    test: "tests/unit/policy/test_policy_schema.py::test_rule_ids_remain_stable_after_serialization"

Files:
  - trader_risk_audit/policy/__init__.py
  - trader_risk_audit/policy/schema.py
  - tests/unit/policy/test_policy_schema.py
  - tests/fixtures/policies/valid_policy.yaml
  - tests/fixtures/policies/unsupported_rule_policy.yaml

Context-Refs:
  - docs/ARCHITECTURE.md#deterministic-vs-llm-owned-subproblems

Notes: |
  Supported v1 rule types: max_daily_loss, max_drawdown, cooldown_after_loss, max_position_size, forbidden_assets, max_leverage.

## T07: Policy Review Packet

Owner:      codex
Phase:      2
Type:       none
Depends-On: T06

Objective: |
  Generate a human review packet for ambiguous or incomplete trader-written rules so the operator must approve deterministic mappings before evaluation runs.

Acceptance-Criteria:
  - id: AC-1
    description: "A policy with ambiguous free-text rule notes produces a review packet containing rule id, source text, missing deterministic fields, and required operator decision."
    test: "tests/unit/policy/test_policy_review.py::test_ambiguous_rule_generates_review_packet"
  - id: AC-2
    description: "The evaluator entry point rejects policies with unresolved review packet items before any violation records are created."
    test: "tests/unit/policy/test_policy_review.py::test_unresolved_review_items_block_evaluation"
  - id: AC-3
    description: "An approved review decision writes the deterministic rule fields and preserves the original source text for audit traceability."
    test: "tests/unit/policy/test_policy_review.py::test_approved_review_preserves_source_text"

Files:
  - trader_risk_audit/policy/validation.py
  - trader_risk_audit/policy/review.py
  - tests/unit/policy/test_policy_review.py
  - tests/fixtures/policies/ambiguous_policy.yaml

Context-Refs:
  - docs/ARCHITECTURE.md#human-approval-boundaries
  - docs/IMPLEMENTATION_CONTRACT.md#human-approval-for-ambiguous-inputs

Notes: |
  This is a deterministic review artifact, not an LLM planner or agent loop.

## T08: Session Calendar and Aggregates

Owner:      codex
Phase:      3
Type:       none
Depends-On: T05, T06

Objective: |
  Build session/day grouping, realized P&L aggregation, exposure totals, and equity curve inputs required by deterministic rule evaluators.

Acceptance-Criteria:
  - id: AC-1
    description: "Trades on timezone boundaries are assigned to the configured trading session date."
    test: "tests/unit/evaluation/test_aggregates.py::test_trades_assign_to_configured_session_date"
  - id: AC-2
    description: "Daily realized P&L equals gross trade P&L minus fees for each configured account and session date."
    test: "tests/unit/evaluation/test_aggregates.py::test_daily_realized_pnl_subtracts_fees"
  - id: AC-3
    description: "Equity curve output records peak equity, current equity, and drawdown after each closed trade event."
    test: "tests/unit/evaluation/test_aggregates.py::test_equity_curve_records_peak_and_drawdown"

Files:
  - trader_risk_audit/evaluation/__init__.py
  - trader_risk_audit/evaluation/calendar.py
  - trader_risk_audit/evaluation/aggregates.py
  - tests/unit/evaluation/test_aggregates.py
  - tests/fixtures/trades/aggregate_scenarios.csv

Context-Refs:
  - docs/ARCHITECTURE.md#data-flow-primary-audit-path

Notes: |
  Do not use wall-clock `now()` in calculations. Inputs and config determine every aggregate.

## T09: Position and Asset Rule Evaluators

Owner:      codex
Phase:      3
Type:       none
Depends-On: T04, T06, T08

Objective: |
  Implement deterministic evaluators for forbidden assets, max position size, and max leverage when leverage data is present.

Acceptance-Criteria:
  - id: AC-1
    description: "Forbidden assets evaluator emits one violation per matching source row with rule id, normalized symbol, timestamp, and source row id."
    test: "tests/unit/evaluation/test_position_asset_rules.py::test_forbidden_assets_emit_source_row_violations"
  - id: AC-2
    description: "Max position size evaluator flags rows where absolute exposure is greater than the configured threshold and records evaluated exposure and threshold."
    test: "tests/unit/evaluation/test_position_asset_rules.py::test_max_position_size_records_exposure_and_threshold"
  - id: AC-3
    description: "Max leverage evaluator emits an unsupported-data warning when leverage fields are absent and emits no guessed leverage violation."
    test: "tests/unit/evaluation/test_position_asset_rules.py::test_max_leverage_requires_source_leverage_fields"

Files:
  - trader_risk_audit/evaluation/rules.py
  - trader_risk_audit/evaluation/violations.py
  - tests/unit/evaluation/test_position_asset_rules.py
  - tests/fixtures/policies/position_asset_policy.yaml

Context-Refs:
  - docs/ARCHITECTURE.md#deterministic-vs-llm-owned-subproblems

Notes: |
  Evaluators must be pure functions over normalized trades, policy rules, and aggregate inputs.

## T10: Loss, Drawdown, and Cooldown Evaluators

Owner:      codex
Phase:      3
Type:       none
Depends-On: T06, T08, T09

Objective: |
  Implement deterministic evaluators for max daily loss, max drawdown, and cooldown-after-loss rules using aggregate inputs and source-traceable violations.

Acceptance-Criteria:
  - id: AC-1
    description: "Max daily loss flags only trades that occur after the configured realized daily loss threshold is breached."
    test: "tests/unit/evaluation/test_loss_rules.py::test_max_daily_loss_flags_post_breach_trades"
  - id: AC-2
    description: "Max drawdown flags trades after equity drawdown exceeds the configured threshold and records peak, current equity, drawdown, and threshold."
    test: "tests/unit/evaluation/test_loss_rules.py::test_max_drawdown_records_equity_values"
  - id: AC-3
    description: "Cooldown evaluator flags trades opened within the configured cooldown window after a qualifying loss event and records the window start and end."
    test: "tests/unit/evaluation/test_loss_rules.py::test_cooldown_flags_trades_inside_window"

Files:
  - trader_risk_audit/evaluation/rules.py
  - trader_risk_audit/evaluation/violations.py
  - tests/unit/evaluation/test_loss_rules.py
  - tests/fixtures/policies/loss_rules_policy.yaml
  - tests/fixtures/trades/loss_rule_scenarios.csv

Context-Refs:
  - docs/ARCHITECTURE.md#cost-risk-reasoning

Notes: |
  Threshold comparison rules must be explicit in code and tests: greater-than versus greater-than-or-equal cannot be implicit.

## T11: Violation Record Determinism

Owner:      codex
Phase:      3
Type:       none
Depends-On: T09, T10

Objective: |
  Provide a stable violation record model, deterministic violation ids, serialization ordering, and warning records for unsupported but non-fatal evaluator conditions.

Acceptance-Criteria:
  - id: AC-1
    description: "Violation ids are stable hashes over audit id, rule id, source row ids, rule type, and evaluated timestamp."
    test: "tests/unit/evaluation/test_violation_records.py::test_violation_ids_are_stable_hashes"
  - id: AC-2
    description: "Serialized violations sort by timestamp, rule id, and violation id."
    test: "tests/unit/evaluation/test_violation_records.py::test_violation_serialization_order_is_deterministic"
  - id: AC-3
    description: "Unsupported-data warnings serialize separately from violations and include rule id, reason code, and affected source fields."
    test: "tests/unit/evaluation/test_violation_records.py::test_warnings_serialize_separately_from_violations"

Files:
  - trader_risk_audit/evaluation/violations.py
  - tests/unit/evaluation/test_violation_records.py

Context-Refs:
  - docs/ARCHITECTURE.md#minimum-viable-control-surface

Notes: |
  Violation ids must not include generated timestamps or file system paths.

## T12: Violation P&L Attribution

Owner:      codex
Phase:      3
Type:       none
Depends-On: T08, T11

Objective: |
  Implement reconciled P&L attribution for compliant versus violating trades, including overlap handling when one trade triggers multiple rules and golden evidence for reviewer verification.

Acceptance-Criteria:
  - id: AC-1
    description: "Top-level attribution buckets each trade row into exactly one of compliant, violating, or unclassified P&L."
    test: "tests/unit/evaluation/test_attribution.py::test_top_level_buckets_each_trade_once"
  - id: AC-2
    description: "Rule-level attribution can list overlapping rule membership while total realized P&L equals compliant plus violating plus unclassified plus reconciliation delta."
    test: "tests/unit/evaluation/test_attribution.py::test_rule_overlap_reconciles_to_total_pnl"
  - id: AC-3
    description: "A non-zero reconciliation delta raises an attribution error before report generation."
    test: "tests/unit/evaluation/test_attribution.py::test_nonzero_reconciliation_delta_blocks_report_generation"
  - id: AC-4
    description: "Golden attribution fixture values match the expected JSON file for overlap, fees, and no-violation scenarios."
    test: "tests/integration/test_attribution_golden.py::test_golden_attribution_fixture_matches_expected_json"

Execution-Mode: heavy
Evidence:
  - tests/fixtures/expected/attribution_overlap_expected.json
  - tests/integration/test_attribution_golden.py::test_golden_attribution_fixture_matches_expected_json
  - docs/EVIDENCE_INDEX.md row for T12 attribution proof
Verifier-Focus: |
  Confirm that overlapping violations do not double count top-level P&L, fees are included exactly once, and non-zero reconciliation deltas block report generation before any customer-facing artifact is created.

Files:
  - trader_risk_audit/evaluation/attribution.py
  - trader_risk_audit/evaluation/violations.py
  - tests/unit/evaluation/test_attribution.py
  - tests/integration/test_attribution_golden.py
  - tests/fixtures/trades/attribution_overlap.csv
  - tests/fixtures/expected/attribution_overlap_expected.json
  - docs/EVIDENCE_INDEX.md

Context-Refs:
  - docs/ARCHITECTURE.md#cost-risk-reasoning
  - docs/DECISION_LOG.md#D-005
  - docs/EVIDENCE_INDEX.md#evidence-table

Notes: |
  This task is proof-first because attribution errors can falsely assign monetary damage to a trader's rule break.

## T13: Report Model and Summaries

Owner:      codex
Phase:      4
Type:       none
Depends-On: T12

Objective: |
  Build the report data model that transforms normalized trades, policies, violations, warnings, and attribution into deterministic report sections.

Acceptance-Criteria:
  - id: AC-1
    description: "Report model includes input summary, policy summary, violation table, repeated pattern summary, worst violation days, attribution summary, limitations, and next-review checklist sections."
    test: "tests/unit/reporting/test_report_model.py::test_report_model_contains_required_sections"
  - id: AC-2
    description: "Each report violation row includes rule id, timestamp, source row ids, evaluated value, threshold, severity, and P&L impact field."
    test: "tests/unit/reporting/test_report_model.py::test_report_violation_rows_include_traceability_fields"
  - id: AC-3
    description: "Warnings for unsupported leverage data appear in the limitations section and not in the violation table."
    test: "tests/unit/reporting/test_report_model.py::test_warnings_render_as_limitations"

Files:
  - trader_risk_audit/reporting/__init__.py
  - trader_risk_audit/reporting/model.py
  - tests/unit/reporting/test_report_model.py

Context-Refs:
  - docs/ARCHITECTURE.md#data-flow-primary-audit-path

Notes: |
  The model should not produce Markdown directly; keep rendering in T14.

## T14: Markdown Report Generator

Owner:      codex
Phase:      4
Type:       none
Depends-On: T13

Objective: |
  Render deterministic Markdown reports from the report model with stable section ordering, source-row traceability, and local artifact paths.

Acceptance-Criteria:
  - id: AC-1
    description: "Markdown output contains headings for Summary, Policy, Violations, P&L Attribution, Limitations, and Next Review."
    test: "tests/unit/reporting/test_markdown_report.py::test_markdown_contains_required_headings"
  - id: AC-2
    description: "The violations table renders rule id, timestamp, source row ids, evaluated value, threshold, severity, and P&L impact columns."
    test: "tests/unit/reporting/test_markdown_report.py::test_markdown_violation_table_has_traceability_columns"
  - id: AC-3
    description: "Rendering the same report model twice produces byte-identical Markdown."
    test: "tests/unit/reporting/test_markdown_report.py::test_markdown_rendering_is_deterministic"

Files:
  - trader_risk_audit/reporting/markdown.py
  - tests/unit/reporting/test_markdown_report.py
  - tests/fixtures/expected/report_expected.md

Context-Refs:
  - docs/spec.md#feature-area-6---report-generation-and-claim-guard

Notes: |
  Avoid current timestamps in the report body; volatile generation metadata belongs in the manifest.

## T15: Claim Guard and Disclaimers

Owner:      codex
Phase:      4
Type:       none
Depends-On: T14

Objective: |
  Add deterministic report-language guardrails that require disclaimers and reject unsupported investment advice, performance promises, live-control claims, or causal-loss assertions.

Acceptance-Criteria:
  - id: AC-1
    description: "A report without the configured not-investment-advice disclaimer fails claim guard validation."
    test: "tests/unit/reporting/test_claim_guard.py::test_missing_disclaimer_fails_validation"
  - id: AC-2
    description: "Report text containing configured profit-promise or live-order-control phrases fails validation with phrase category and matched text."
    test: "tests/unit/reporting/test_claim_guard.py::test_forbidden_claim_phrases_return_category_and_match"
  - id: AC-3
    description: "A report that states violations and P&L impact from deterministic fields passes claim guard validation."
    test: "tests/unit/reporting/test_claim_guard.py::test_evidence_backed_violation_language_passes"

Files:
  - trader_risk_audit/reporting/claim_guard.py
  - trader_risk_audit/reporting/markdown.py
  - tests/unit/reporting/test_claim_guard.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#report-claim-boundaries

Notes: |
  The guard is a deterministic text validator, not an LLM moderation call.

## T16: Artifact Manifest and Reproducible Hashes

Owner:      codex
Phase:      4
Type:       none
Depends-On: T12, T14, T15

Objective: |
  Write and validate reproducible audit manifests that record input hashes, output hashes, command metadata, artifact paths, and content-hash drift checks.

Acceptance-Criteria:
  - id: AC-1
    description: "Manifest records hashes for source export, policy file, normalized trades, violations, attribution summary, report Markdown, and delivery packet when present."
    test: "tests/unit/artifacts/test_manifest.py::test_manifest_records_required_artifact_hashes"
  - id: AC-2
    description: "Content hash calculation excludes generation timestamp and includes package version and deterministic artifact content."
    test: "tests/unit/artifacts/test_manifest.py::test_content_hash_excludes_generation_timestamp"
  - id: AC-3
    description: "Manifest validation fails with a missing artifact error when any referenced path is absent."
    test: "tests/unit/artifacts/test_manifest.py::test_manifest_validation_fails_for_missing_artifact"

Files:
  - trader_risk_audit/artifacts/__init__.py
  - trader_risk_audit/artifacts/manifest.py
  - tests/unit/artifacts/test_manifest.py

Context-Refs:
  - docs/ARCHITECTURE.md#minimum-viable-control-surface

Notes: |
  Manifest hashes are the audit re-run contract. Keep them independent of absolute local paths where possible.

## T17: End-to-End Audit CLI

Owner:      codex
Phase:      5
Type:       none
Depends-On: T05, T07, T10, T12, T16

Objective: |
  Wire the local `audit` CLI command end to end from supported export and policy files to normalized artifacts, violations, attribution, report, delivery packet, and manifest.

Acceptance-Criteria:
  - id: AC-1
    description: "`audit --trades fixture.csv --policy valid_policy.yaml --output-dir tmp` writes normalized trades, violations, attribution, report Markdown, Telegram-ready delivery packet, and manifest files."
    test: "tests/integration/test_audit_cli.py::test_audit_cli_writes_expected_artifacts"
  - id: AC-2
    description: "The audit command exits non-zero and writes no report when policy review items are unresolved."
    test: "tests/integration/test_audit_cli.py::test_audit_cli_blocks_unresolved_policy_review_items"
  - id: AC-3
    description: "Running the audit command twice with the same immutable fixtures produces identical deterministic content hashes in the manifest."
    test: "tests/integration/test_audit_cli.py::test_audit_cli_repeated_run_has_same_content_hashes"

Files:
  - trader_risk_audit/cli.py
  - trader_risk_audit/artifacts/manifest.py
  - tests/integration/test_audit_cli.py

Context-Refs:
  - docs/ARCHITECTURE.md#data-flow-primary-audit-path
  - docs/IMPLEMENTATION_CONTRACT.md#reproducibility

Notes: |
  The CLI remains local-only. Do not add network calls or hosted service assumptions.

## T18: Telegram-Ready Delivery Packet

Owner:      codex
Phase:      5
Type:       none
Depends-On: T14, T15, T16

Objective: |
  Generate a deterministic Telegram-ready text packet from approved report content without sending messages or requiring Telegram credentials.

Acceptance-Criteria:
  - id: AC-1
    description: "Delivery packet includes trader-facing summary, top violation counts, violating P&L, limitations, disclaimer, and local report path."
    test: "tests/unit/reporting/test_delivery_packet.py::test_delivery_packet_contains_required_fields"
  - id: AC-2
    description: "Delivery packet stays below the configured character limit and truncates repeated pattern details with a count of omitted items."
    test: "tests/unit/reporting/test_delivery_packet.py::test_delivery_packet_respects_character_limit"
  - id: AC-3
    description: "Delivery packet generation fails if claim guard validation fails on the source report."
    test: "tests/unit/reporting/test_delivery_packet.py::test_delivery_packet_requires_claim_guard_pass"

Files:
  - trader_risk_audit/reporting/delivery.py
  - trader_risk_audit/reporting/claim_guard.py
  - tests/unit/reporting/test_delivery_packet.py

Context-Refs:
  - docs/ARCHITECTURE.md#external-integrations

Notes: |
  This task prepares copyable text only. Sending through a bot would require a later ADR and Tool-Use/Profile review if LLM-directed.

## T19: Local Retention and Deletion Workflow

Owner:      codex
Phase:      5
Type:       none
Depends-On: T16, T17

Objective: |
  Implement local retention listing, dry-run deletion, and confirmed deletion for artifact groups referenced by a manifest while avoiding raw trade data in command output.

Acceptance-Criteria:
  - id: AC-1
    description: "Retention list output shows manifest id, artifact count, created timestamp, and report path without printing raw trade rows."
    test: "tests/unit/storage/test_retention.py::test_retention_list_omits_raw_trade_data"
  - id: AC-2
    description: "Dry-run deletion returns the full referenced path set and leaves every file on disk."
    test: "tests/unit/storage/test_retention.py::test_delete_dry_run_leaves_files"
  - id: AC-3
    description: "Confirmed deletion removes existing referenced files and reports already-missing paths separately."
    test: "tests/unit/storage/test_retention.py::test_confirmed_delete_removes_files_and_reports_missing"

Files:
  - trader_risk_audit/storage/__init__.py
  - trader_risk_audit/storage/retention.py
  - trader_risk_audit/cli.py
  - tests/unit/storage/test_retention.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling

Notes: |
  Local deletion is a v1 operator control. Do not add hosted retention jobs.

## T20: Pilot Regression Fixture Pack

Owner:      codex
Phase:      5
Type:       none
Depends-On: T17, T18, T19

Objective: |
  Add an anonymized end-to-end fixture pack that exercises the full local audit path and records expected outputs for future pilot regression checks.

Acceptance-Criteria:
  - id: AC-1
    description: "The fixture pack contains anonymized trades, a valid policy, expected violation JSON, expected attribution JSON, expected report Markdown, and expected manifest content hashes."
    test: "tests/integration/test_pilot_fixture_pack.py::test_fixture_pack_contains_expected_artifacts"
  - id: AC-2
    description: "The end-to-end fixture test regenerates artifacts and compares deterministic outputs to expected files."
    test: "tests/integration/test_pilot_fixture_pack.py::test_end_to_end_fixture_outputs_match_expected_files"
  - id: AC-3
    description: "A fixture scan fails if account ids, trader names, Telegram handles, email addresses, or broker account-like numeric ids appear in committed fixture files."
    test: "tests/integration/test_pilot_fixture_pack.py::test_committed_fixtures_do_not_contain_customer_identifiers"

Files:
  - tests/integration/test_pilot_fixture_pack.py
  - tests/fixtures/pilot/trades.csv
  - tests/fixtures/pilot/policy.yaml
  - tests/fixtures/expected/pilot_violations.json
  - tests/fixtures/expected/pilot_attribution.json
  - tests/fixtures/expected/pilot_report.md
  - tests/fixtures/expected/pilot_manifest_hashes.json
  - docs/EVIDENCE_INDEX.md

Context-Refs:
  - docs/EVIDENCE_INDEX.md#evidence-table
  - docs/IMPLEMENTATION_JOURNAL.md#entries

Notes: |
  This task closes the concierge pilot implementation baseline. Real customer exports must never be committed as fixtures.

## T21: Demo Audit Pack

Owner:      codex
Phase:      6
Type:       none
Depends-On: T17, T18, T20

Objective: |
  Add a clearly synthetic demonstration audit pack and Russian demo case so the founder can show real audit artifacts before asking prospects for their own exports and rules.

Acceptance-Criteria:
  - id: AC-1
    description: "The demo pack contains synthetic trades, a policy, generated report Markdown, generated Telegram-ready packet text, and a manifest-backed output folder."
    test: "tests/integration/test_demo_pack.py::test_demo_pack_contains_required_artifacts"
  - id: AC-2
    description: "The demo audit can be regenerated through the existing local audit workflow and produces deterministic report and attribution outputs."
    test: "tests/integration/test_demo_pack.py::test_demo_pack_regenerates_deterministically"
  - id: AC-3
    description: "The Russian demo case states that the data is synthetic and does not present the report as investment advice, strategy proof, or live trading control."
    test: "tests/integration/test_demo_pack.py::test_demo_case_contains_synthetic_data_and_claim_boundaries"

Files:
  - demo/risk_audit_case_001/trades.csv
  - demo/risk_audit_case_001/policy.yaml
  - demo/risk_audit_case_001/output/report.md
  - demo/risk_audit_case_001/output/telegram_packet.txt
  - demo/risk_audit_case_001/output/manifest.json
  - docs/DEMO_CASE_RU.md
  - tests/integration/test_demo_pack.py

Context-Refs:
  - STARTUP_PRESSURE_TEST_RU.md#11-mvp--pilot-test
  - docs/IMPLEMENTATION_CONTRACT.md#report-claim-boundaries

Notes: |
  This is a sales/demo artifact, not market validation. Do not use real customer exports or imply that synthetic evidence proves willingness to pay.

## T22: Pilot Intake Contract

Owner:      codex
Phase:      6
Type:       none
Depends-On: T21

Objective: |
  Define the exact pilot intake contract a trader must satisfy before a manual audit can run: files, metadata, written risk rules, privacy/disclaimer text, and operator checklist.

Acceptance-Criteria:
  - id: AC-1
    description: "The Russian intake contract lists required files, supported file types, timezone/session fields, broker/platform field, account currency, audit period, and written risk rule requirements."
    test: "tests/test_pilot_intake_contract.py::test_intake_contract_mentions_required_fields"
  - id: AC-2
    description: "The risk-rules template asks for past/current rules in trader language while warning that ambiguous rules require operator approval before evaluation."
    test: "tests/test_pilot_intake_contract.py::test_risk_rules_template_preserves_human_approval_boundary"
  - id: AC-3
    description: "The privacy/disclaimer template states local-first handling, no investment advice, no live trading control, and no broker/exchange API connection."
    test: "tests/test_pilot_intake_contract.py::test_privacy_disclaimer_contains_required_boundaries"

Files:
  - docs/PILOT_INTAKE_CONTRACT_RU.md
  - templates/intake_request.yaml
  - templates/risk_rules_template_ru.md
  - templates/privacy_disclaimer_ru.md
  - tests/test_pilot_intake_contract.py

Context-Refs:
  - STARTUP_PRESSURE_TEST_RU.md#10-first-10-customers-plan
  - docs/ARCHITECTURE.md#human-approval-boundaries
  - docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling

Notes: |
  Keep this contract simple enough for Telegram/manual intake. Do not introduce user accounts, hosted storage, payments, or SaaS onboarding.

## T23: Local Audit Workspace Convention

Owner:      codex
Phase:      6
Type:       none
Depends-On: T17, T22

Objective: |
  Add a local audit workspace convention so every pilot request has predictable input, output, operator notes, status metadata, and generated artifacts without requiring a database or SaaS surface.

Acceptance-Criteria:
  - id: AC-1
    description: "A helper creates the expected audit workspace directories for input, output, and operator notes from an audit id."
    test: "tests/unit/test_workspace_layout.py::test_workspace_layout_creates_expected_directories"
  - id: AC-2
    description: "Workspace metadata stores audit id, created timestamp, status, and non-sensitive file references without raw trade rows."
    test: "tests/unit/test_workspace_layout.py::test_workspace_metadata_omits_raw_trade_data"
  - id: AC-3
    description: "The Russian runbook documents the local folder convention and the manual operator handoff from intake to audit output."
    test: "tests/unit/test_workspace_layout.py::test_workspace_runbook_documents_required_layout"

Files:
  - trader_risk_audit/workspace.py
  - docs/AUDIT_WORKSPACE_RUNBOOK_RU.md
  - tests/unit/test_workspace_layout.py

Context-Refs:
  - docs/ARCHITECTURE.md#runtime-and-isolation-model
  - docs/IMPLEMENTATION_CONTRACT.md#runtime-boundary

Notes: |
  The workspace is a local operator convention. It must not add a hosted database, multi-tenant auth, or network dependency.

## T24: Telegram Intake ADR

Owner:      codex
Phase:      6
Type:       adr
Depends-On: T22, T23

Objective: |
  File an ADR that permits Telegram as a constrained pilot intake and delivery surface while keeping Trader Risk Audit separate from signal analytics, broker control, and investment-advice behavior.

Acceptance-Criteria:
  - id: AC-1
    description: "The ADR states Telegram may receive user files, return status, and deliver approved reports, but may not connect to brokers, accept API keys, block orders, parse signal channels, or generate trading advice."
    test: "tests/test_telegram_intake_adr.py::test_adr_declares_allowed_and_forbidden_telegram_scope"
  - id: AC-2
    description: "The ADR defines operator approval before report delivery and keeps final violation truth in deterministic audit artifacts."
    test: "tests/test_telegram_intake_adr.py::test_adr_preserves_operator_approval_and_deterministic_truth"
  - id: AC-3
    description: "The ADR documents secrets, logging, local storage, and retention boundaries for Telegram pilot files."
    test: "tests/test_telegram_intake_adr.py::test_adr_documents_security_and_retention_boundaries"

Files:
  - docs/adr/ADR-001-telegram-intake-delivery.md
  - tests/test_telegram_intake_adr.py

Context-Refs:
  - docs/ARCHITECTURE.md#external-integrations
  - docs/IMPLEMENTATION_CONTRACT.md#runtime-boundary
  - STARTUP_PRESSURE_TEST_RU.md#12-next-development-phases

Notes: |
  This ADR is required before bot implementation. It does not approve Telegram signal analytics or any live trading behavior.

## T25: Minimal Telegram Bot Skeleton

Owner:      codex
Phase:      6
Type:       none
Depends-On: T23, T24

Objective: |
  Add a minimal Telegram pilot bot that can start an audit request, accept allowed document uploads, store files in a local audit workspace, and return an audit id with status `received`.

Acceptance-Criteria:
  - id: AC-1
    description: "The bot refuses to start unless `TRA_TELEGRAM_BOT_ENABLED=true` and a token is provided through environment variables."
    test: "tests/unit/telegram_bot/test_handlers.py::test_bot_requires_explicit_enable_and_token"
  - id: AC-2
    description: "`/start`, `/help`, `/new_audit`, `/status`, and `/cancel` handlers return deterministic user-facing messages without exposing raw trade data."
    test: "tests/unit/telegram_bot/test_handlers.py::test_core_commands_return_safe_messages"
  - id: AC-3
    description: "Allowed uploaded files are saved under the local audit workspace and the user receives a stable audit id."
    test: "tests/unit/telegram_bot/test_handlers.py::test_document_upload_creates_local_audit_request"

Files:
  - trader_risk_audit/telegram_bot/__init__.py
  - trader_risk_audit/telegram_bot/bot.py
  - trader_risk_audit/telegram_bot/handlers.py
  - trader_risk_audit/telegram_bot/storage.py
  - tests/unit/telegram_bot/test_handlers.py
  - .env.example

Context-Refs:
  - docs/adr/ADR-001-telegram-intake-delivery.md
  - docs/IMPLEMENTATION_CONTRACT.md#credentials
  - docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling

Notes: |
  This is intake only. Do not auto-run audits, send final reports, process payments, parse signal channels, or request broker credentials.

## T26: Operator Review Queue

Owner:      codex
Phase:      6
Type:       none
Depends-On: T23, T25

Objective: |
  Add a local operator review queue and CLI commands so pilot requests from Telegram/manual intake can be listed, inspected, statused, rejected, or marked ready for local audit execution.

Acceptance-Criteria:
  - id: AC-1
    description: "The queue persists statuses: received, needs_policy_mapping, needs_user_clarification, ready_to_run, processing, ready_for_review, delivered, and rejected."
    test: "tests/unit/test_pilot_queue.py::test_queue_persists_allowed_statuses"
  - id: AC-2
    description: "CLI commands list and show audit requests without printing raw trade rows or confidential free-text notes."
    test: "tests/unit/test_pilot_queue.py::test_queue_cli_omits_confidential_data"
  - id: AC-3
    description: "The operator can change status and reject a request with a non-sensitive reason."
    test: "tests/unit/test_pilot_queue.py::test_queue_cli_status_and_reject_transitions"

Files:
  - trader_risk_audit/pilot_queue.py
  - trader_risk_audit/cli.py
  - tests/unit/test_pilot_queue.py

Context-Refs:
  - docs/adr/ADR-001-telegram-intake-delivery.md
  - docs/IMPLEMENTATION_CONTRACT.md#human-approval-for-ambiguous-inputs

Notes: |
  The queue is local-first and operator-owned. Do not add background workers, hosted queue services, or automated report sending.

## T27: Telegram Delivery Packet Send

Owner:      codex
Phase:      6
Type:       none
Depends-On: T18, T24, T26

Objective: |
  Send an approved Telegram-ready summary and report file to the requesting user after operator approval, claim guard validation, and local audit artifact generation.

Acceptance-Criteria:
  - id: AC-1
    description: "Delivery is allowed only for requests in `ready_for_review` with an existing report and delivery packet."
    test: "tests/unit/telegram_bot/test_delivery.py::test_delivery_requires_ready_for_review_status"
  - id: AC-2
    description: "The source report must pass claim guard before any Telegram delivery message is sent."
    test: "tests/unit/telegram_bot/test_delivery.py::test_delivery_requires_claim_guard_pass"
  - id: AC-3
    description: "Successful delivery sends summary text, attaches report Markdown, includes the disclaimer, and marks the request `delivered`."
    test: "tests/unit/telegram_bot/test_delivery.py::test_delivery_sends_summary_report_and_marks_delivered"

Files:
  - trader_risk_audit/telegram_bot/delivery.py
  - tests/unit/telegram_bot/test_delivery.py

Context-Refs:
  - docs/adr/ADR-001-telegram-intake-delivery.md
  - docs/IMPLEMENTATION_CONTRACT.md#report-claim-boundaries

Notes: |
  Delivery sends only approved audit artifacts. Do not add live alerts, trade suggestions, recurring schedulers, or signal-channel messages.

## T28: End-to-End Telegram Pilot Test

Owner:      codex
Phase:      6
Type:       none
Depends-On: T25, T26, T27

Objective: |
  Prove the full Telegram pilot loop with a mocked Telegram client: user starts a request, uploads files, operator reviews and runs audit locally, report is approved, and delivery is sent.

Acceptance-Criteria:
  - id: AC-1
    description: "The integration test covers `/new_audit`, document upload, local workspace creation, status transitions, audit output registration, and delivery through a mocked Telegram client."
    test: "tests/integration/test_telegram_pilot_flow.py::test_full_mocked_telegram_pilot_flow"
  - id: AC-2
    description: "The end-to-end test requires no real network access and no real Telegram credentials."
    test: "tests/integration/test_telegram_pilot_flow.py::test_telegram_pilot_flow_uses_mocked_client_only"
  - id: AC-3
    description: "Logs and test output do not contain raw trade rows, Telegram handles, emails, broker account ids, or customer identifiers."
    test: "tests/integration/test_telegram_pilot_flow.py::test_telegram_pilot_flow_redacts_confidential_data"

Files:
  - tests/integration/test_telegram_pilot_flow.py

Context-Refs:
  - docs/adr/ADR-001-telegram-intake-delivery.md
  - docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling

Notes: |
  The test must mock Telegram network behavior. Do not require real bot credentials in CI.

## T29: Pilot Payment and Evidence Log

Owner:      codex
Phase:      6
Type:       none
Depends-On: T21, T22

Objective: |
  Add simple pilot evidence artifacts so business validation does not disappear behind engineering work.

Acceptance-Criteria:
  - id: AC-1
    description: "The Russian evidence log defines required fields for prospect source, ICP, call date, export provided, rules provided, paid amount, objections, report delivered, repeat requested, and referral."
    test: "tests/test_pilot_evidence_log.py::test_evidence_log_documents_required_business_fields"
  - id: AC-2
    description: "The customer log CSV template contains the same required validation fields and no real customer rows."
    test: "tests/test_pilot_evidence_log.py::test_customer_log_template_contains_required_columns_only"
  - id: AC-3
    description: "The evidence log states the advancement gate: 3 paid audit reports from 10 qualified prospects within 14 days, then at least 2 repeat audit commitments within 30 days."
    test: "tests/test_pilot_evidence_log.py::test_evidence_log_records_advancement_gate"

Files:
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - templates/pilot_customer_log.csv
  - tests/test_pilot_evidence_log.py

Context-Refs:
  - STARTUP_PRESSURE_TEST_RU.md#14-final-recommendation
  - README.md#current-status

Notes: |
  This is a validation artifact. Do not commit real names, Telegram handles, emails, broker accounts, exports, or payment identifiers.

## T30: Public Sample Source Policy

Owner:      codex
Phase:      7
Type:       docs
Depends-On: T21, T29

Objective: |
  Define the source, licensing, privacy, evidence-labeling rules, and starter policy profile boundaries for public or public-like records that can be used to validate Trader Risk Audit internally before approaching real traders.

Acceptance-Criteria:
  - id: AC-1
    description: "The Russian source policy defines acceptable public/anonymized source types, required source metadata, license checks, and PII/secret rejection criteria."
    test: "tests/test_public_sample_source_policy.py::test_public_sample_policy_defines_source_license_and_privacy_rules"
  - id: AC-2
    description: "The policy explicitly states that public sample artifacts are internal/demo evidence and must not be counted as qualified prospect calls, paid pilot reports, repeat commitments, referrals, or PMF evidence."
    test: "tests/test_public_sample_source_policy.py::test_public_sample_policy_separates_demo_from_market_validation"
  - id: AC-3
    description: "The policy defines the readiness gate for moving from internal validation to trader outreach: reproducible reports, explainable violations, at least three risk scenarios, and a two-minute readable demo."
    test: "tests/test_public_sample_source_policy.py::test_public_sample_policy_defines_outreach_readiness_gate"
  - id: AC-4
    description: "The starter policy profile doc and YAML templates define soft, medium, and hard audit presets, explain customization, and preserve the no-advice boundary."
    test: "tests/test_starter_policy_profiles.py"

Files:
  - docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md
  - docs/STARTER_POLICY_PROFILES_RU.md
  - templates/policies/starter_policy_soft.yaml
  - templates/policies/starter_policy_medium.yaml
  - templates/policies/starter_policy_hard.yaml
  - tests/test_public_sample_source_policy.py
  - tests/test_starter_policy_profiles.py

Context-Refs:
  - docs/DEMO_CASE_RU.md
  - docs/STARTER_POLICY_PROFILES_RU.md
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - STARTUP_PRESSURE_TEST_RU.md#14-final-recommendation
  - README.md#current-status

Notes: |
  This task only defines the source policy and internal readiness gate. Do not fetch public data, add public sample artifacts, contact traders, or mark validation evidence as paid pilot proof.
  Candidate primary source for T31: SEC EDGAR Insider Transactions Data Sets / Form 4 non-derivative transactions, using only P/S transaction rows with required date, ticker, shares, and price fields. Source policy must require removing reporting owner names, signatures, remarks, footnotes, and any unnecessary personal fields before committing a sample pack.
  Candidate backup source: public exchange trade-print samples only if SEC Form 4 cannot support at least three explainable risk scenarios; backup samples must be labeled as market trade prints, not account history.
  Starter policies: provide `soft`, `medium`, and `hard` audit presets for internal validation and demos. They must be framed as customizable audit strictness profiles, not investment advice, strategy recommendations, optimal risk settings, or replacements for trader/prop account rules.
  Telegram demo boundary: Telegram may be used as the simple user entry point for upload, audit id/status, and approved report delivery. Do not add broker APIs, signal parsing, order blocking, auto-advice, live trading behavior, or report delivery without operator approval.

## T31: Public Sample Evidence Pack

Owner:      codex
Phase:      7
Type:       none
Depends-On: T30

Objective: |
  Create a reproducible public-sample evidence pack from allowed public/anonymized records or explicitly documented public-like sample records, then run the deterministic audit workflow end to end.

Acceptance-Criteria:
  - id: AC-1
    description: "The public sample pack includes source metadata, trade input, risk policy, generated audit outputs, delivery packet, and manifest with deterministic hashes."
    test: "tests/integration/test_public_sample_pack.py::test_public_sample_pack_contains_required_inputs_outputs_and_manifest"
  - id: AC-2
    description: "The generated report contains at least three distinct risk scenarios and passes claim guard without investment advice, performance promises, broker-control claims, or causal overclaims."
    test: "tests/integration/test_public_sample_pack.py::test_public_sample_report_is_explainable_and_claim_guard_safe"
  - id: AC-3
    description: "The source metadata labels the pack as internal/demo validation and records why it is not paid pilot evidence."
    test: "tests/integration/test_public_sample_pack.py::test_public_sample_pack_is_not_marked_as_market_validation"
  - id: AC-4
    description: "The public sample evidence pack records which starter profile was used and, where useful, compares soft, medium, and hard outputs without claiming one profile is objectively best."
    test: "tests/integration/test_public_sample_pack.py::test_public_sample_pack_records_starter_profile_context"
  - id: AC-5
    description: "Where Telegram is used for the demo, the flow remains upload, audit id/status, operator-approved report delivery, and no broker APIs, signal parsing, order blocking, auto-advice, or live trading behavior."
    test: "tests/integration/test_public_sample_pack.py::test_public_sample_pack_keeps_telegram_demo_inside_adr_boundary"

Files:
  - demo/public_sample_001/source.md
  - demo/public_sample_001/trades.csv
  - demo/public_sample_001/policy.yaml
  - demo/public_sample_001/output/
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md
  - docs/STARTER_POLICY_PROFILES_RU.md
  - templates/policies/starter_policy_soft.yaml
  - templates/policies/starter_policy_medium.yaml
  - templates/policies/starter_policy_hard.yaml
  - tests/integration/test_public_sample_pack.py

Context-Refs:
  - docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md
  - docs/STARTER_POLICY_PROFILES_RU.md
  - docs/DEMO_CASE_RU.md
  - docs/IMPLEMENTATION_CONTRACT.md#report-claim-boundaries
  - docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling

Notes: |
  Preferred source path: use SEC EDGAR Insider Transactions Data Sets / Form 4 non-derivative transactions after T30 confirms source, licensing, privacy, and transformation rules. Map `TRANS_DATE` to timestamp, `ISSUERTRADINGSYMBOL` to symbol, `TRANS_ACQUIRED_DISP_CD` A/D to buy/sell, `TRANS_SHARES` to quantity, `TRANS_PRICEPERSHARE` to price, and `ACCESSION_NUMBER` plus row key to source traceability. Do not include reporting owner names, signatures, remarks, footnotes, broker credentials, or unverifiable copied private exports.
  Starter profile path: use `soft`, `medium`, and `hard` templates to test internal explainability across strictness levels. Prefer custom trader or prop/funded account rules when available, and never present starter profiles as trading advice or optimal settings.
  Telegram demo path: when useful, present the public sample through the existing Telegram pilot flow as a simple mini-demo: `/new_audit`, upload files, audit id/status, local operator run, and approved report delivery. Keep the implementation inside ADR-001.
  If using live public internet sources, record the exact source URL, access date, license or terms summary, and transformation steps.

## T32: Internal Outreach Readiness Review

Owner:      codex
Phase:      7
Type:       docs
Depends-On: T31

Objective: |
  Review whether the public-sample evidence proves enough internal product confidence to start manual trader outreach, and capture remaining product risks separately from market validation risks.

Acceptance-Criteria:
  - id: AC-1
    description: "The readiness review records pass/fail against reproducibility, explainability, scenario coverage, two-minute demo readability, and claim safety."
    test: "tests/test_internal_readiness_review.py::test_internal_readiness_review_records_required_gate_results"
  - id: AC-2
    description: "The review separates internal product confidence from market validation and keeps the paid pilot gate from the evidence log unchanged."
    test: "tests/test_internal_readiness_review.py::test_internal_readiness_review_preserves_paid_pilot_gate"
  - id: AC-3
    description: "The review states the next go/no-go action for trader outreach and lists only concrete blockers or risks."
    test: "tests/test_internal_readiness_review.py::test_internal_readiness_review_states_go_no_go_action"

Files:
  - docs/INTERNAL_VALIDATION_REVIEW_RU.md
  - tests/test_internal_readiness_review.py

Context-Refs:
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - STARTUP_PRESSURE_TEST_RU.md#14-final-recommendation

Notes: |
  This review may approve starting manual outreach, but it must not claim product-market fit or paid demand without real trader evidence.

## T33: Telegram Demo Happy Path

Owner:      codex
Phase:      8
Type:       none
Depends-On: T28, T31

Objective: |
  Turn the existing Telegram pilot pieces into a coherent demo happy path: start an audit, upload files or choose a demo sample, receive an audit id/status, and receive an operator-approved report.

Acceptance-Criteria:
  - id: AC-1
    description: "The Telegram demo flow supports `/start`, `/new_audit`, file upload guidance, audit id/status response, and approved report delivery copy without requiring real network access in tests."
    test: "tests/integration/test_telegram_demo_happy_path.py::test_telegram_demo_happy_path_uses_mocked_client"
  - id: AC-2
    description: "The flow makes the user-facing path clear without exposing raw trade rows, Telegram handles, broker account ids, or private notes."
    test: "tests/integration/test_telegram_demo_happy_path.py::test_telegram_demo_happy_path_redacts_sensitive_fields"
  - id: AC-3
    description: "The implementation stays inside ADR-001: no broker APIs, signal parsing, order blocking, auto-advice, or live trading behavior."
    test: "tests/integration/test_telegram_demo_happy_path.py::test_telegram_demo_happy_path_stays_inside_adr_boundary"

Files:
  - trader_risk_audit/telegram_bot/handlers.py
  - trader_risk_audit/telegram_bot/delivery.py
  - tests/integration/test_telegram_demo_happy_path.py
  - docs/TELEGRAM_DEMO_FLOW_RU.md

Context-Refs:
  - docs/adr/ADR-001-telegram-intake-delivery.md
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md
  - docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling

Notes: |
  This is a demo/intake surface, not a Telegram product expansion. Keep operator approval before delivery and keep final violation truth in deterministic artifacts.

## T34: Public Sample Demo Mode

Owner:      codex
Phase:      8
Type:       none
Depends-On: T31, T33

Objective: |
  Add a demo mode that can show the public sample audit without asking a prospect to upload private files first.

Acceptance-Criteria:
  - id: AC-1
    description: "A local command or Telegram handler can retrieve the public sample summary, report path, source label, and selected starter profile."
    test: "tests/integration/test_public_sample_demo_mode.py::test_public_sample_demo_mode_returns_demo_summary"
  - id: AC-2
    description: "The demo mode labels the sample as public/internal demo evidence and not paid pilot, PMF, or prospect evidence."
    test: "tests/integration/test_public_sample_demo_mode.py::test_public_sample_demo_mode_labels_evidence_correctly"
  - id: AC-3
    description: "The demo mode reuses existing report and delivery artifacts rather than creating a separate unsupported report format."
    test: "tests/integration/test_public_sample_demo_mode.py::test_public_sample_demo_mode_reuses_audit_artifacts"

Files:
  - trader_risk_audit/telegram_bot/handlers.py
  - trader_risk_audit/cli.py
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md
  - tests/integration/test_public_sample_demo_mode.py

Context-Refs:
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md
  - docs/STARTER_POLICY_PROFILES_RU.md
  - docs/IMPLEMENTATION_CONTRACT.md#report-claim-boundaries

Notes: |
  Demo mode should reduce friction in a sales call. It must not pretend a public sample is a real customer result.

## T35: Report Polish for Demo Readability

Owner:      codex
Phase:      8
Type:       none
Depends-On: T14, T18, T31

Objective: |
  Improve the audit report's demo readability so a prospect can understand the result in two minutes: executive summary first, violation table, P&L impact, limitations, and next-review checklist.

Acceptance-Criteria:
  - id: AC-1
    description: "The report starts with a compact executive summary including rule count, violation count, affected P&L, and selected policy profile."
    test: "tests/unit/reporting/test_demo_report_readability.py::test_demo_report_starts_with_compact_summary"
  - id: AC-2
    description: "Violation rows remain source-traceable and deterministic after the readability changes."
    test: "tests/unit/reporting/test_demo_report_readability.py::test_demo_report_preserves_source_traceability"
  - id: AC-3
    description: "The report keeps the required disclaimer and claim guard still blocks advice, performance promises, live-control claims, and causal overclaims."
    test: "tests/unit/reporting/test_demo_report_readability.py::test_demo_report_preserves_claim_guard_boundary"

Files:
  - trader_risk_audit/reporting/markdown.py
  - trader_risk_audit/reporting/model.py
  - tests/unit/reporting/test_demo_report_readability.py
  - tests/fixtures/expected/report_expected.md

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#report-claim-boundaries
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md

Notes: |
  Keep the report factual and artifact-backed. Do not add design-heavy frontend scope unless a later task explicitly introduces a web surface.

## T36: Two-Minute Demo Script

Owner:      codex
Phase:      8
Type:       docs
Depends-On: T31, T33, T35

Objective: |
  Create a short RU/EN demo script that tells the founder exactly what to show, what to say, what not to claim, and how to explain soft/medium/hard profiles.

Acceptance-Criteria:
  - id: AC-1
    description: "The script covers the two-minute flow: problem, upload, selected profile, report summary, source-row traceability, P&L impact, and next pilot ask."
    test: "tests/test_demo_script.py::test_demo_script_covers_required_flow"
  - id: AC-2
    description: "The script includes no-advice, no-live-control, no-performance-promise, and public-sample-not-market-validation boundaries."
    test: "tests/test_demo_script.py::test_demo_script_preserves_claim_boundaries"
  - id: AC-3
    description: "The script includes a concise explanation of soft, medium, hard, and custom rules."
    test: "tests/test_demo_script.py::test_demo_script_explains_policy_profiles"

Files:
  - docs/DEMO_SCRIPT_RU.md
  - docs/DEMO_SCRIPT_EN.md
  - tests/test_demo_script.py

Context-Refs:
  - docs/STARTER_POLICY_PROFILES_RU.md
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md
  - docs/PILOT_EVIDENCE_LOG_RU.md

Notes: |
  This is for founder-led sales calls. It should push toward real export/rules and paid pilot commitment, not toward more feature discussion.

## T37: Policy Profile Selector

Owner:      codex
Phase:      9
Type:       none
Depends-On: T30, T33

Objective: |
  Let a user or operator select `soft`, `medium`, `hard`, or `custom` during intake, while keeping custom rules as the preferred path when the trader already has written rules.

Acceptance-Criteria:
  - id: AC-1
    description: "The selector resolves soft, medium, and hard to the committed starter YAML templates and records the selected profile in non-sensitive workspace metadata."
    test: "tests/unit/test_policy_profile_selector.py::test_selector_records_starter_profile_metadata"
  - id: AC-2
    description: "Custom profile selection requires a provided policy file or risk-rules template and does not silently default to a starter profile."
    test: "tests/unit/test_policy_profile_selector.py::test_custom_profile_requires_user_rules"
  - id: AC-3
    description: "User-facing copy says starter profiles are customizable audit presets, not trading advice or optimal settings."
    test: "tests/unit/test_policy_profile_selector.py::test_selector_copy_preserves_no_advice_boundary"

Files:
  - trader_risk_audit/policy/profiles.py
  - trader_risk_audit/telegram_bot/handlers.py
  - trader_risk_audit/workspace.py
  - tests/unit/test_policy_profile_selector.py

Context-Refs:
  - docs/STARTER_POLICY_PROFILES_RU.md
  - docs/IMPLEMENTATION_CONTRACT.md#human-approval-for-ambiguous-inputs

Notes: |
  This task should reduce intake friction, not replace trader-owned risk rules.

## T38: Intake File Validator

Owner:      codex
Phase:      9
Type:       none
Depends-On: T22, T25, T37

Objective: |
  Validate uploaded intake files before operator review so a user receives clear feedback about missing columns, unsupported formats, empty fields, invalid sides, or missing policy/profile selection.

Acceptance-Criteria:
  - id: AC-1
    description: "The validator checks supported trade CSV fields, required policy/profile inputs, file extension, size boundary, and basic parse errors without printing raw trade rows."
    test: "tests/unit/test_intake_file_validator.py::test_validator_reports_actionable_errors_without_raw_rows"
  - id: AC-2
    description: "Telegram upload handling returns concise safe validation feedback and keeps invalid uploads in a non-runnable queue status."
    test: "tests/unit/telegram_bot/test_intake_validation.py::test_invalid_upload_returns_safe_feedback"
  - id: AC-3
    description: "Valid intake can be marked operator-ready without requiring a database, hosted storage, or external service."
    test: "tests/unit/test_intake_file_validator.py::test_valid_intake_can_be_marked_operator_ready"

Files:
  - trader_risk_audit/intake.py
  - trader_risk_audit/telegram_bot/storage.py
  - trader_risk_audit/telegram_bot/handlers.py
  - tests/unit/test_intake_file_validator.py
  - tests/unit/telegram_bot/test_intake_validation.py

Context-Refs:
  - docs/PILOT_INTAKE_CONTRACT_RU.md
  - docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling

Notes: |
  Validate enough to help a user fix upload problems. Do not build full broker-specific importer coverage before real pilot exports prove demand.

## T39: Operator Runbook CLI

Owner:      codex
Phase:      9
Type:       none
Depends-On: T23, T26, T38

Objective: |
  Add an operator-oriented CLI path that prepares an audit workspace from intake, shows the next required action, runs the local audit when ready, and records output references.

Acceptance-Criteria:
  - id: AC-1
    description: "The CLI can prepare a workspace from an intake id and show input files, selected policy profile, status, and next operator action without raw trade rows."
    test: "tests/integration/test_operator_runbook_cli.py::test_operator_prepare_shows_safe_next_action"
  - id: AC-2
    description: "The CLI can run the local audit for a ready intake and register report, packet, manifest, and status references in the queue."
    test: "tests/integration/test_operator_runbook_cli.py::test_operator_run_registers_audit_outputs"
  - id: AC-3
    description: "The command remains local-first and does not require background workers, hosted queues, or network services."
    test: "tests/integration/test_operator_runbook_cli.py::test_operator_runbook_cli_is_local_first"

Files:
  - trader_risk_audit/cli.py
  - trader_risk_audit/pilot_queue.py
  - trader_risk_audit/workspace.py
  - tests/integration/test_operator_runbook_cli.py
  - docs/AUDIT_WORKSPACE_RUNBOOK_RU.md

Context-Refs:
  - docs/AUDIT_WORKSPACE_RUNBOOK_RU.md
  - docs/adr/ADR-001-telegram-intake-delivery.md

Notes: |
  This is founder/operator speed work. Keep it scriptable and deterministic.

## T40: Evidence Capture Automation

Owner:      codex
Phase:      9
Type:       none
Depends-On: T29, T39

Objective: |
  Make it hard to deliver a pilot report without capturing validation evidence: paid status, objection, repeat request, referral, and next follow-up.

Acceptance-Criteria:
  - id: AC-1
    description: "After report delivery, the operator can append a validation row using the existing pilot customer log schema without adding real customer identifiers to fixtures."
    test: "tests/unit/test_evidence_capture.py::test_evidence_capture_appends_customer_log_row"
  - id: AC-2
    description: "The evidence capture path distinguishes public sample/demo evidence from qualified prospect, paid pilot, repeat commitment, and referral evidence."
    test: "tests/unit/test_evidence_capture.py::test_evidence_capture_separates_demo_from_market_validation"
  - id: AC-3
    description: "The CLI can summarize current validation counts against the gate: 10 qualified prospects, 5 exports/rules, 3 paid audits, 2 repeat commitments."
    test: "tests/unit/test_evidence_capture.py::test_evidence_capture_summarizes_validation_gate"

Files:
  - trader_risk_audit/evidence.py
  - trader_risk_audit/cli.py
  - templates/pilot_customer_log.csv
  - tests/unit/test_evidence_capture.py
  - docs/PILOT_EVIDENCE_LOG_RU.md

Context-Refs:
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - STARTUP_PRESSURE_TEST_RU.md#14-final-recommendation

Notes: |
  This is not CRM scope. Keep the evidence file local, explicit, and privacy-safe.

## T41: Before/After Report Comparison

Owner:      codex
Phase:      10
Type:       docs
Depends-On: T31, T35

Objective: |
  Create a sales-friendly comparison that shows what a raw trade export fails to explain versus what the audit report adds: rule breach, source rows, and P&L impact.

Acceptance-Criteria:
  - id: AC-1
    description: "The comparison shows raw export fields next to audit report outputs without using real customer data."
    test: "tests/test_before_after_comparison.py::test_before_after_comparison_uses_safe_sample_data"
  - id: AC-2
    description: "The comparison highlights deterministic rule checks, source-row evidence, and violation-attributed P&L without performance or advice claims."
    test: "tests/test_before_after_comparison.py::test_before_after_comparison_preserves_claim_boundaries"
  - id: AC-3
    description: "The comparison includes a concise CTA to provide real export/rules for a paid pilot."
    test: "tests/test_before_after_comparison.py::test_before_after_comparison_has_paid_pilot_cta"

Files:
  - docs/BEFORE_AFTER_REPORT_COMPARISON_RU.md
  - docs/BEFORE_AFTER_REPORT_COMPARISON_EN.md
  - tests/test_before_after_comparison.py

Context-Refs:
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md
  - docs/PILOT_EVIDENCE_LOG_RU.md

Notes: |
  The comparison should help a prospect understand why this is not just another journal export.

## T42: Objection Handling Pack

Owner:      codex
Phase:      10
Type:       docs
Depends-On: T22, T24, T36

Objective: |
  Create a concise objection-handling pack for privacy, no broker API, no advice, "why not my journal?", pricing, and repeat-audit questions.

Acceptance-Criteria:
  - id: AC-1
    description: "The pack answers privacy, broker/API, advice, journal-comparison, price, and repeat-audit objections in RU and EN."
    test: "tests/test_objection_handling_pack.py::test_objection_pack_covers_required_objections"
  - id: AC-2
    description: "The answers remain factual and avoid legal, investment, performance, or live-control promises."
    test: "tests/test_objection_handling_pack.py::test_objection_pack_preserves_claim_boundaries"
  - id: AC-3
    description: "The pack points back to the pilot intake contract and paid pilot evidence gate."
    test: "tests/test_objection_handling_pack.py::test_objection_pack_points_to_pilot_gate"

Files:
  - docs/OBJECTION_HANDLING_RU.md
  - docs/OBJECTION_HANDLING_EN.md
  - tests/test_objection_handling_pack.py

Context-Refs:
  - docs/PILOT_INTAKE_CONTRACT_RU.md
  - docs/adr/ADR-001-telegram-intake-delivery.md
  - docs/PILOT_EVIDENCE_LOG_RU.md

Notes: |
  This is sales enablement, not compliance/legal advice.

## T43: ICP-Specific Demo Variants

Owner:      codex
Phase:      10
Type:       docs
Depends-On: T31, T36, T42

Objective: |
  Prepare targeted demo variants for the most plausible early adopters: prop/funded traders, active crypto discretionary traders, and small teams/coaches.

Acceptance-Criteria:
  - id: AC-1
    description: "Each ICP variant states the likely pain, current workaround, demo angle, required proof, and paid pilot ask."
    test: "tests/test_icp_demo_variants.py::test_icp_variants_cover_required_sections"
  - id: AC-2
    description: "Each variant keeps the same product boundary: post-trade audit, no broker control, no signal analytics, no advice."
    test: "tests/test_icp_demo_variants.py::test_icp_variants_preserve_product_boundary"
  - id: AC-3
    description: "Each variant maps to the same validation evidence gate rather than inventing vanity metrics."
    test: "tests/test_icp_demo_variants.py::test_icp_variants_map_to_validation_gate"

Files:
  - docs/ICP_DEMO_VARIANTS_RU.md
  - docs/ICP_DEMO_VARIANTS_EN.md
  - tests/test_icp_demo_variants.py

Context-Refs:
  - STARTUP_PRESSURE_TEST_RU.md#4-wedge-comparison
  - docs/PILOT_EVIDENCE_LOG_RU.md

Notes: |
  Do not split product implementation by ICP until real outreach evidence shows which group converts.

## T44: Paid Pilot Offer Page

Owner:      codex
Phase:      10
Type:       docs
Depends-On: T36, T41, T42, T43

Objective: |
  Create a minimal static paid pilot offer page/copy artifact that explains what the trader gets, what they must provide, privacy boundaries, pilot price placeholder, and next step.

Acceptance-Criteria:
  - id: AC-1
    description: "The offer page states deliverables, required inputs, timeline, privacy boundary, no-advice boundary, and paid pilot CTA."
    test: "tests/test_paid_pilot_offer_page.py::test_offer_page_contains_required_sections"
  - id: AC-2
    description: "The page does not claim PMF, guaranteed improvement, performance prediction, broker control, or live risk prevention."
    test: "tests/test_paid_pilot_offer_page.py::test_offer_page_preserves_claim_boundaries"
  - id: AC-3
    description: "The page links or references the demo script, before/after comparison, objection pack, and pilot intake contract."
    test: "tests/test_paid_pilot_offer_page.py::test_offer_page_references_conversion_assets"

Files:
  - docs/PAID_PILOT_OFFER_RU.md
  - docs/PAID_PILOT_OFFER_EN.md
  - tests/test_paid_pilot_offer_page.py

Context-Refs:
  - docs/PILOT_INTAKE_CONTRACT_RU.md
  - docs/BEFORE_AFTER_REPORT_COMPARISON_RU.md
  - docs/OBJECTION_HANDLING_RU.md
  - docs/DEMO_SCRIPT_RU.md

Notes: |
  Keep this static and founder-led. Do not build a landing-page app, checkout, account system, or public SaaS flow until paid pilot evidence justifies it.
