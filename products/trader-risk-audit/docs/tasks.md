# Task Graph - Trader Risk Audit

Version: 1.2
Last updated: 2026-05-07
Status: Phase 7 planned - internal validation with public samples

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
| 7 | Internal Validation with Public Samples | T30-T32 | Public sample source policy, reproducible public evidence pack, and internal readiness review before trader outreach. | The team can prove the audit workflow on licensed public/anonymized examples, explain its limits, and decide whether to start trader outreach without counting public samples as paid pilot evidence. |

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
  Define the source, licensing, privacy, and evidence-labeling rules for public or public-like records that can be used to validate Trader Risk Audit internally before approaching real traders.

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

Files:
  - docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md
  - tests/test_public_sample_source_policy.py

Context-Refs:
  - docs/DEMO_CASE_RU.md
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - STARTUP_PRESSURE_TEST_RU.md#14-final-recommendation
  - README.md#current-status

Notes: |
  This task only defines the source policy and internal readiness gate. Do not fetch public data, add public sample artifacts, contact traders, or mark validation evidence as paid pilot proof.
  Candidate primary source for T31: SEC EDGAR Insider Transactions Data Sets / Form 4 non-derivative transactions, using only P/S transaction rows with required date, ticker, shares, and price fields. Source policy must require removing reporting owner names, signatures, remarks, footnotes, and any unnecessary personal fields before committing a sample pack.
  Candidate backup source: public exchange trade-print samples only if SEC Form 4 cannot support at least three explainable risk scenarios; backup samples must be labeled as market trade prints, not account history.

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

Files:
  - demo/public_sample_001/source.md
  - demo/public_sample_001/trades.csv
  - demo/public_sample_001/policy.yaml
  - demo/public_sample_001/output/
  - docs/PUBLIC_SAMPLE_EVIDENCE_RU.md
  - tests/integration/test_public_sample_pack.py

Context-Refs:
  - docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md
  - docs/DEMO_CASE_RU.md
  - docs/IMPLEMENTATION_CONTRACT.md#report-claim-boundaries
  - docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling

Notes: |
  Preferred source path: use SEC EDGAR Insider Transactions Data Sets / Form 4 non-derivative transactions after T30 confirms source, licensing, privacy, and transformation rules. Map `TRANS_DATE` to timestamp, `ISSUERTRADINGSYMBOL` to symbol, `TRANS_ACQUIRED_DISP_CD` A/D to buy/sell, `TRANS_SHARES` to quantity, `TRANS_PRICEPERSHARE` to price, and `ACCESSION_NUMBER` plus row key to source traceability. Do not include reporting owner names, signatures, remarks, footnotes, broker credentials, or unverifiable copied private exports.
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
