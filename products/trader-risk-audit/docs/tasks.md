# Task Graph - Trader Risk Audit

Version: 1.0
Last updated: 2026-05-07
Status: Phase 1 ready for validation

---

## Phase Plan

| Phase | Name | Tasks | Delivery | Gate criteria |
|-------|------|-------|----------|---------------|
| 1 | Foundation | T01-T03 | Python package skeleton, CI contract, and baseline smoke tests. | Phase 1 audit passes; CI file exists; first local test baseline can be established. |
| 2 | Input Contracts | T04-T07 | Canonical trade records, import normalization, risk policy schema, and human review packet. | Supported fixtures normalize deterministically; unsupported or ambiguous inputs fail with explicit errors. |
| 3 | Rule Evaluation | T08-T12 | Aggregation, deterministic rule evaluators, violation records, and P&L attribution. | Golden fixtures prove violation truth, source-row traceability, and reconciled attribution. |
| 4 | Reporting and Artifacts | T13-T16 | Report data model, Markdown output, claim guard, and reproducible manifest hashes. | Reports are generated from deterministic artifacts and blocked when unsupported claims appear. |
| 5 | Concierge Pilot Workflow | T17-T20 | End-to-end CLI, Telegram-ready packet, retention/delete workflow, and pilot regression fixtures. | A local operator can run a complete anonymized audit and reproduce the same artifact hashes. |

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
    test: "tests/test_ci_contract.py::test_ci_uses_python_311_and_editable_install"
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
  Wire the local `audit` CLI command end to end from supported export and policy files to normalized artifacts, violations, attribution, report, and manifest.

Acceptance-Criteria:
  - id: AC-1
    description: "`audit --trades fixture.csv --policy valid_policy.yaml --output-dir tmp` writes normalized trades, violations, attribution, report Markdown, and manifest files."
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
