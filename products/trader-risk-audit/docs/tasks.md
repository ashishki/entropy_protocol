# Task Graph - Trader Risk Audit

Version: 1.8
Last updated: 2026-05-15
Status: active Phase 23. Phase 21 is complete and archived; T93 deferred real
read-only exchange fetching, so T94-T97 remain blocked until future market
evidence reopens the gate. Core is paused. The next active work is an
open-source audit case bank and multi-case validation loop before warm prospect
delivery.
Phase 14/15 exchange-import work is complete and remains available only when
it directly supports the selected real audit artifact.

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
| 11 | Read-Only Exchange Import Safety | T45-T47 | ADR-002, credential permission contract, and exchange fixture/redaction policy. | The team can plan Binance/Bybit historical-fill import without approving exchange control or real network code before safety gates. |
| 12 | Exchange Import Core | T48-T50 | Raw snapshot schema, import manifest, normalizer interface, and fixture-backed CLI. | Fixture-backed exchange imports can produce deterministic raw snapshots, normalized trades, and import manifests consumed by the existing audit flow. |
| 13 | Bybit Read-Only MVP | T51-T54 | Bybit key metadata check, execution fetch planner, normalizer, and import-to-audit integration. | Bybit historical executions can be imported safely from sanitized fixtures with read-only enforcement and deterministic audit outputs. |
| 14 | Binance Read-Only MVP | T55-T58 | Binance signed account request helper, spot trade fetch planner, normalizer, and import-to-audit integration. | Binance Spot trade history can be imported safely from sanitized fixtures with explicit symbols/time range and deterministic audit outputs. |
| 15 | Operator UX and Pilot Validation | T59-T62 | Exchange import runbook, safety guidance, evidence fields, and deep review. | Read-only exchange import is ready for founder-led pilot use only after secret handling, permission enforcement, reproducibility, and boundary review pass. |
| 16 | Artifact-First Real Audit Validation | T63-T69 | Scope one real audit, ingest real data, generate a complete report pack, manually validate calculations, polish the report, package an internal demo, and decide external pilot readiness. | A real-data audit report is trusted by the operator, claim-safe, traceable to source rows, and ready for controlled warm-prospect delivery. |
| 17 | Automated Intake Profiler | T70-T73 | Intake session model, CSV schema profiling, actionable intake report, and deep review. | A prospect export can be profiled automatically with safe field mapping, blockers, unsupported fields, privacy notes, and next action. |
| 18 | Structured Rule Builder | T74-T78 | Supported rule catalog, profile-to-policy builder, threshold prompts, unsupported-rule register, and deep review. | A prospect can create a valid deterministic policy without hand-writing YAML, while unsupported free text is safely captured as a limitation/review item. |
| 19 | One-Click Audit Runner | T79-T82 | End-to-end local audit session runner, status model, artifact bundle, reproducibility checks, and deep review. | A valid intake session and policy can produce the complete report pack without developer intervention. |
| 20 | Report Preview And Paid CTA | T83-T87 | Claim-safe preview, redacted value summary, paid pilot CTA, conversion events, and deep review. | A prospect can see enough value to request/pay for a reviewed report without receiving unsafe claims or raw-data exposure. |
| 21 | Hypothesis Evidence Dashboard | T88-T92 | Funnel event schema, dashboard CLI/report, validation thresholds, privacy-safe export, and deep review. | The operator can measure upload, valid export, preview, paid ask, paid report, repeat commitment, and referral evidence. |
| 22 | Conditional Real Read-Only Import | T93-T97 | CSV friction decision gate, ADR update, minimal local real fetch path if justified, import-to-runner integration, and deep review. | Real read-only exchange fetching is added only if evidence shows CSV/export friction blocks conversion, and remains local, read-only, and no hosted secrets. |
| 23 | Open-Source Audit Case Bank | T98-T103 | Source-selection protocol, case-pack directory contract, 5+ open-source/synthetic validation packs, manual validation notes, and deep review. | Multiple real or public transaction-like packs prove report validity, limitations, and reproducibility without private data. |
| 24 | Multi-Case Report Quality Loop | T104-T109 | Report quality scorecard, rule/data coverage matrix, multi-case dashboard, polished demo pack selection, regression coverage, and deep review. | At least 3 packs are demo-quality, including positive-finding and limitation/reject examples, with no P0/P1 report-validity findings. |
| 25 | Private Pilot Readiness | T110-T115 | Private data intake checklist, local-only artifact handling, private report review checklist, paid-pilot package, feedback log, and go/no-go review. | 1-3 operator-approved private/anonymized reports can be run outside git and delivered with safe wording. |

---

## Loop Continuation Rule

The orchestrator should not stop just because a planned phase ends. At each phase boundary:

1. Run the mandatory strategy/deep review required by `docs/prompts/ORCHESTRATOR.md`.
2. Archive the review and update audit indexes/state docs.
3. Apply required fixes for any stop-ship or accepted findings.
4. If no stop-ship finding remains, advance `docs/CODEX_PROMPT.md` to the next planned phase/task and continue the loop.
5. If review findings, pilot evidence, or implementation discoveries show that the roadmap should change, update this task graph, `docs/CODEX_PROMPT.md`, README, and relevant audit notes before continuing.

Do not wait for a separate user instruction between planned phases unless the next phase would add forbidden scope, require a new ADR, or contradict current validation evidence.

## Artifact-First Priority Override

As of 2026-05-11, the operator confirmed warm demand/pre-order interest and
asked to validate real report artifacts before going to people. On 2026-05-12,
the operator clarified that if private data is missing, valid open sources
should be used instead of blocking. Phase 16 is complete; this section remains
as historical routing context only.

T56-T62 are complete, but they should not drive the next orchestration step. If
the selected real audit requires Binance/Bybit read-only import, use only the
smallest completed path needed for that artifact. Otherwise, run the real audit
via CSV/export paths. New implementation should follow the automated pilot
priority below.

For Phase 16, "real input" can mean either a private operator/customer export
or a verified public/open-source transaction dataset with source metadata,
privacy review, and limitation wording. Public/open-source artifact validation
does not count as paid pilot evidence or PMF evidence.

## Automated Pilot Priority

As of 2026-05-14, Phase 16 proved artifact quality on a verified open-source
pack. The next blocker is reducing founder/operator labor enough to test the
hypothesis repeatedly. Phases 17-22 must automate intake, rules, audit running,
preview/CTA, and evidence measurement before any public SaaS expansion.

The automated loop must remain deterministic and local-first until paid/repeat
evidence justifies hosted product work. Real exchange network fetching remains
conditional on CSV/export friction evidence and must not be implemented before
T93/T94.

## Open-Source Audit Validation Priority

As of 2026-05-15, the operator paused Core and narrowed the active work to
Trader Risk Audit and Signal Analytics Sandbox. For Trader, the next blocker is
not more platform work or SaaS scope; it is a larger bank of valid audit
artifacts from open-source, public, synthetic edge-case, and later
operator-approved private data.

The next loop must follow `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`.
Validation success means truthful and reproducible reports, not only
impressive-looking violations. Each validation batch must preserve positive,
limitation/reject, and edge-case examples to avoid cherry-picking.

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

## T45: Read-Only Exchange Import ADR

Owner:      codex
Phase:      11
Type:       docs
Depends-On: T44

Objective: |
  Accept and document the read-only exchange import boundary for Binance/Bybit historical trade ingestion without approving exchange control.

Acceptance-Criteria:
  - id: AC-1
    description: "ADR-002 states the allowed read-only import scope and explicitly forbids order write, withdrawal, transfer, leverage/margin mutation, hosted secrets, signal analytics, and advice."
    test: "manual/docs-review"
  - id: AC-2
    description: "The roadmap plan maps read-only import into phased tasks with safety gates before real network calls."
    test: "manual/docs-review"
  - id: AC-3
    description: "Decision log and loop state point to ADR-002 as the canonical boundary."
    test: "manual/docs-review"

Files:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/EXCHANGE_API_IMPORT_PLAN_RU.md
  - docs/DECISION_LOG.md
  - docs/CODEX_PROMPT.md

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md
  - docs/ARCHITECTURE.md

Notes: |
  This is a scope decision only. Do not add exchange network code in this task.

## T46: Exchange Credential Permission Contract

Owner:      codex
Phase:      11
Type:       security
Depends-On: T45

Objective: |
  Define a deterministic contract for exchange API credential handling, permission inspection, safe failure modes, and redaction.

Acceptance-Criteria:
  - id: AC-1
    description: "The contract requires read-only keys, rejects detectable trade/withdraw/transfer/account-mutation permissions, and marks unverifiable permissions as needs_operator_review."
    test: "tests/unit/exchange/test_credentials.py::test_permission_contract_rejects_write_scopes"
  - id: AC-2
    description: "Credential objects redact API keys, secrets, signatures, account ids, and raw secret values in repr, logs, errors, and serialized metadata."
    test: "tests/unit/exchange/test_credentials.py::test_credentials_are_redacted_in_output"
  - id: AC-3
    description: "No credential values are written into manifests, queue metadata, workspace metadata, or generated reports."
    test: "tests/integration/test_exchange_secret_redaction.py::test_exchange_import_does_not_persist_secrets"

Files:
  - trader_risk_audit/exchange/credentials.py
  - tests/unit/exchange/test_credentials.py
  - tests/integration/test_exchange_secret_redaction.py
  - docs/IMPLEMENTATION_CONTRACT.md

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/IMPLEMENTATION_CONTRACT.md#credentials-and-secrets

Notes: |
  Use fixture credentials only. Do not contact Binance or Bybit.

## T47: Exchange Fixture and Redaction Policy

Owner:      codex
Phase:      11
Type:       tests
Depends-On: T45, T46

Objective: |
  Establish the policy and tests for synthetic or sanitized exchange-like raw JSON fixtures before connector code exists.

Acceptance-Criteria:
  - id: AC-1
    description: "Fixture policy forbids real API keys, signatures, account ids, balances, customer identifiers, and private notes."
    test: "tests/test_exchange_fixture_policy.py::test_exchange_fixture_policy_rejects_sensitive_fields"
  - id: AC-2
    description: "Committed exchange fixtures are synthetic or explicitly sanitized and pass identifier scans."
    test: "tests/test_exchange_fixture_policy.py::test_committed_exchange_fixtures_are_sanitized"
  - id: AC-3
    description: "The policy documents allowed raw execution fields that can be committed for regression tests."
    test: "manual/docs-review"

Files:
  - docs/EXCHANGE_FIXTURE_POLICY_RU.md
  - tests/test_exchange_fixture_policy.py
  - tests/fixtures/exchange/

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md

Notes: |
  Fixture policy must be in place before raw exchange snapshot examples are committed.

## T48: Exchange Raw Snapshot Schema and Import Manifest

Owner:      codex
Phase:      12
Type:       none
Depends-On: T46, T47

Objective: |
  Add deterministic local data structures for raw exchange snapshots and import manifests that can be hashed and audited before normalization.

Acceptance-Criteria:
  - id: AC-1
    description: "Raw snapshot schema records exchange, market/category, symbols, time range, fetched pages, source endpoint labels, and raw records without credentials."
    test: "tests/unit/exchange/test_snapshot_schema.py::test_snapshot_schema_serializes_without_secrets"
  - id: AC-2
    description: "Import manifest records raw snapshot hash, normalized output hash, package version, and generated timestamp excluded from deterministic content hash."
    test: "tests/unit/exchange/test_import_manifest.py::test_import_manifest_hash_is_deterministic"
  - id: AC-3
    description: "Manifest validation detects missing or drifted raw snapshot and normalized output files."
    test: "tests/unit/exchange/test_import_manifest.py::test_import_manifest_detects_artifact_drift"

Files:
  - trader_risk_audit/exchange/snapshot.py
  - trader_risk_audit/exchange/manifest.py
  - tests/unit/exchange/test_snapshot_schema.py
  - tests/unit/exchange/test_import_manifest.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - trader_risk_audit/artifacts/manifest.py

Notes: |
  Keep import manifests separate from final audit manifests; final audit truth still comes from the existing audit command.

## T49: Exchange Normalizer Interface

Owner:      codex
Phase:      12
Type:       none
Depends-On: T48, T05

Objective: |
  Add a shared interface that maps exchange-specific raw fills/executions into canonical trade records accepted by the existing audit engine.

Acceptance-Criteria:
  - id: AC-1
    description: "Normalizer interface emits canonical trade records with stable source row ids derived from exchange, symbol, execution id/order id, and timestamp."
    test: "tests/unit/exchange/test_normalizer.py::test_exchange_normalizer_emits_stable_row_ids"
  - id: AC-2
    description: "Missing required price, quantity, side, symbol, or timestamp fields produce safe validation errors without raw row leakage."
    test: "tests/unit/exchange/test_normalizer.py::test_exchange_normalizer_reports_safe_missing_field_errors"
  - id: AC-3
    description: "Normalized exchange records serialize byte-identically across repeated runs."
    test: "tests/unit/exchange/test_normalizer.py::test_exchange_normalization_is_deterministic"

Files:
  - trader_risk_audit/exchange/normalizer.py
  - tests/unit/exchange/test_normalizer.py
  - tests/fixtures/exchange/

Context-Refs:
  - trader_risk_audit/trades/schema.py
  - trader_risk_audit/trades/importers.py

Notes: |
  Do not change evaluator semantics for exchange data in this task.

## T50: Fixture-Backed Exchange Import CLI

Owner:      codex
Phase:      12
Type:       cli
Depends-On: T48, T49

Objective: |
  Add an `exchange-import` CLI skeleton that runs against local fixture snapshots and writes raw snapshot, normalized trades, and import manifest artifacts.

Acceptance-Criteria:
  - id: AC-1
    description: "`exchange-import fixture --snapshot fixture.json --output-dir tmp` writes raw snapshot, normalized trades, and import manifest files."
    test: "tests/integration/test_exchange_import_cli.py::test_fixture_exchange_import_writes_expected_artifacts"
  - id: AC-2
    description: "Running fixture import twice produces identical normalized output hashes and import manifest content hashes."
    test: "tests/integration/test_exchange_import_cli.py::test_fixture_exchange_import_is_deterministic"
  - id: AC-3
    description: "The existing `audit` command can consume the normalized exchange trades from the fixture import."
    test: "tests/integration/test_exchange_import_to_audit.py::test_fixture_exchange_import_feeds_audit"

Files:
  - trader_risk_audit/cli.py
  - trader_risk_audit/exchange/
  - tests/integration/test_exchange_import_cli.py
  - tests/integration/test_exchange_import_to_audit.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/EXCHANGE_API_IMPORT_PLAN_RU.md

Notes: |
  This phase still must not make real Binance or Bybit network calls.

## T51: Bybit API Key Metadata Check

Owner:      codex
Phase:      13
Type:       security
Depends-On: T46, T50

Objective: |
  Implement Bybit API key metadata inspection for read-only enforcement using sanitized tests and mocked HTTP responses.

Acceptance-Criteria:
  - id: AC-1
    description: "Bybit permission checker accepts `readOnly == 1` and rejects `readOnly != 1`."
    test: "tests/unit/exchange/test_bybit_permissions.py::test_bybit_permission_checker_requires_read_only"
  - id: AC-2
    description: "Detected wallet transfer, withdraw, order-write, or account mutation permissions return a safe rejection reason."
    test: "tests/unit/exchange/test_bybit_permissions.py::test_bybit_permission_checker_rejects_write_scopes"
  - id: AC-3
    description: "Permission-check failures do not log or persist API credentials."
    test: "tests/unit/exchange/test_bybit_permissions.py::test_bybit_permission_errors_are_redacted"

Files:
  - trader_risk_audit/exchange/bybit.py
  - tests/unit/exchange/test_bybit_permissions.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md

Notes: |
  Use mocked HTTP only. Real credential smoke tests require explicit operator action outside CI.

## T52: Bybit Execution Fetch Planner

Owner:      codex
Phase:      13
Type:       none
Depends-On: T51

Objective: |
  Plan deterministic Bybit execution-history fetches for `spot` and `linear` categories with seven-day windows and cursor pagination.

Acceptance-Criteria:
  - id: AC-1
    description: "Planner slices requested date ranges into exchange-valid seven-day windows."
    test: "tests/unit/exchange/test_bybit_fetch_plan.py::test_bybit_fetch_plan_slices_seven_day_windows"
  - id: AC-2
    description: "Paginator follows `nextPageCursor` until exhausted and preserves deterministic page ordering."
    test: "tests/unit/exchange/test_bybit_fetch_plan.py::test_bybit_cursor_pagination_is_deterministic"
  - id: AC-3
    description: "Only execution-history and key-info endpoint labels are present; no order/write endpoint labels are implemented."
    test: "tests/unit/exchange/test_bybit_fetch_plan.py::test_bybit_client_exposes_no_write_endpoints"

Files:
  - trader_risk_audit/exchange/bybit.py
  - tests/unit/exchange/test_bybit_fetch_plan.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md

Notes: |
  Fetch planning can be implemented before enabling real network execution.

## T53: Bybit Raw-to-Canonical Normalizer

Owner:      codex
Phase:      13
Type:       none
Depends-On: T49, T52

Objective: |
  Normalize Bybit execution records into canonical trade records with stable ids, fees, side mapping, symbol mapping, and timestamps.

Acceptance-Criteria:
  - id: AC-1
    description: "Bybit execution fixtures normalize to expected canonical trade JSON."
    test: "tests/unit/exchange/test_bybit_normalizer.py::test_bybit_executions_normalize_to_canonical_trades"
  - id: AC-2
    description: "Duplicate or same-timestamp executions preserve deterministic ordering by execution id/order id."
    test: "tests/unit/exchange/test_bybit_normalizer.py::test_bybit_normalizer_orders_same_timestamp_executions"
  - id: AC-3
    description: "Unsupported Bybit execution fields become limitations/warnings rather than guessed audit truth."
    test: "tests/unit/exchange/test_bybit_normalizer.py::test_bybit_unsupported_fields_are_reported_safely"

Files:
  - trader_risk_audit/exchange/bybit.py
  - tests/unit/exchange/test_bybit_normalizer.py
  - tests/fixtures/exchange/bybit/

Context-Refs:
  - trader_risk_audit/trades/schema.py
  - docs/EXCHANGE_FIXTURE_POLICY_RU.md

Notes: |
  This task should use sanitized fixtures only.

## T54: Bybit Import-to-Audit Integration

Owner:      codex
Phase:      13
Type:       integration
Depends-On: T51, T52, T53

Objective: |
  Prove the Bybit read-only import path feeds the existing deterministic audit workflow end to end.

Acceptance-Criteria:
  - id: AC-1
    description: "Fixture-backed Bybit import writes raw snapshot, normalized trades, import manifest, and then audit report/manifest artifacts."
    test: "tests/integration/test_bybit_import_to_audit.py::test_bybit_import_feeds_audit"
  - id: AC-2
    description: "Bybit import and audit artifacts regenerate with identical hashes across output directories."
    test: "tests/integration/test_bybit_import_to_audit.py::test_bybit_import_to_audit_is_deterministic"
  - id: AC-3
    description: "Audit output includes source-row traceability back to Bybit execution ids without exposing credentials."
    test: "tests/integration/test_bybit_import_to_audit.py::test_bybit_audit_preserves_safe_traceability"

Files:
  - trader_risk_audit/exchange/bybit.py
  - tests/integration/test_bybit_import_to_audit.py
  - tests/fixtures/exchange/bybit/

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - trader_risk_audit/cli.py

Notes: |
  Passing this task is the Phase 13 gate.

## T55: Binance Signed Account Request Helper

Owner:      codex
Phase:      14
Type:       security
Depends-On: T46, T50

Objective: |
  Implement Binance signed account-data request construction for read-only trade-history imports without adding write endpoints.

Acceptance-Criteria:
  - id: AC-1
    description: "Signed query construction is deterministic and covered by fixture credentials."
    test: "tests/unit/exchange/test_binance_signing.py::test_binance_signed_query_is_deterministic"
  - id: AC-2
    description: "Signer redacts API key, secret, and signature in repr, errors, and debug output."
    test: "tests/unit/exchange/test_binance_signing.py::test_binance_signer_redacts_secrets"
  - id: AC-3
    description: "Binance client exposes only account trade-history endpoint labels; no order/write/withdraw/transfer endpoints are implemented."
    test: "tests/unit/exchange/test_binance_signing.py::test_binance_client_exposes_no_write_endpoints"

Files:
  - trader_risk_audit/exchange/binance.py
  - tests/unit/exchange/test_binance_signing.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md

Notes: |
  Do not use real credentials in tests.

## T56: Binance Spot Trade Fetch Planner

Owner:      codex
Phase:      14
Type:       none
Depends-On: T55

Objective: |
  Plan deterministic Binance Spot `myTrades` imports by explicit symbols and time ranges.

Acceptance-Criteria:
  - id: AC-1
    description: "CLI requires explicit symbols and date range for Binance spot imports."
    test: "tests/integration/test_binance_import_cli.py::test_binance_import_requires_symbols_and_range"
  - id: AC-2
    description: "Planner builds deterministic symbol/window requests and records source endpoint metadata."
    test: "tests/unit/exchange/test_binance_fetch_plan.py::test_binance_fetch_plan_is_deterministic"
  - id: AC-3
    description: "Pagination/window handling preserves deterministic ordering across symbols and windows."
    test: "tests/unit/exchange/test_binance_fetch_plan.py::test_binance_fetch_order_is_stable"

Files:
  - trader_risk_audit/exchange/binance.py
  - tests/unit/exchange/test_binance_fetch_plan.py
  - tests/integration/test_binance_import_cli.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md

Notes: |
  Binance all-account history is not assumed; symbols are explicit.

## T57: Binance Raw-to-Canonical Normalizer

Owner:      codex
Phase:      14
Type:       none
Depends-On: T49, T56

Objective: |
  Normalize Binance Spot trade history records into canonical trade records with stable ids, price/quantity/fee mapping, and side inference.

Acceptance-Criteria:
  - id: AC-1
    description: "Binance spot trade fixtures normalize to expected canonical trade JSON."
    test: "tests/unit/exchange/test_binance_normalizer.py::test_binance_trades_normalize_to_canonical_trades"
  - id: AC-2
    description: "Stable source row ids include exchange, symbol, order id, trade id, and timestamp."
    test: "tests/unit/exchange/test_binance_normalizer.py::test_binance_normalizer_emits_stable_row_ids"
  - id: AC-3
    description: "Fee, maker/taker, and unsupported fields are preserved or reported without guessing missing audit truth."
    test: "tests/unit/exchange/test_binance_normalizer.py::test_binance_unsupported_fields_are_reported_safely"

Files:
  - trader_risk_audit/exchange/binance.py
  - tests/unit/exchange/test_binance_normalizer.py
  - tests/fixtures/exchange/binance/

Context-Refs:
  - trader_risk_audit/trades/schema.py
  - docs/EXCHANGE_FIXTURE_POLICY_RU.md

Notes: |
  Keep futures/perps/funding out of the first Binance MVP unless a later task adds them explicitly.

## T58: Binance Import-to-Audit Integration

Owner:      codex
Phase:      14
Type:       integration
Depends-On: T55, T56, T57

Objective: |
  Prove the Binance Spot read-only import path feeds the existing deterministic audit workflow end to end.

Acceptance-Criteria:
  - id: AC-1
    description: "Fixture-backed Binance import writes raw snapshot, normalized trades, import manifest, and then audit report/manifest artifacts."
    test: "tests/integration/test_binance_import_to_audit.py::test_binance_import_feeds_audit"
  - id: AC-2
    description: "Binance import and audit artifacts regenerate with identical hashes across output directories."
    test: "tests/integration/test_binance_import_to_audit.py::test_binance_import_to_audit_is_deterministic"
  - id: AC-3
    description: "Audit output includes source-row traceability back to Binance trade ids without exposing credentials."
    test: "tests/integration/test_binance_import_to_audit.py::test_binance_audit_preserves_safe_traceability"

Files:
  - trader_risk_audit/exchange/binance.py
  - tests/integration/test_binance_import_to_audit.py
  - tests/fixtures/exchange/binance/

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - trader_risk_audit/cli.py

Notes: |
  Passing this task is the Phase 14 gate.

## T59: Exchange Import Operator Runbook

Owner:      codex
Phase:      15
Type:       docs
Depends-On: T54, T58

Objective: |
  Update operator runbooks and pilot intake docs so exchange import is an optional intake path alongside CSV upload.

Acceptance-Criteria:
  - id: AC-1
    description: "Runbook explains CSV upload and read-only API import as separate intake methods with different risk and setup steps."
    test: "tests/test_exchange_import_runbook.py::test_exchange_runbook_covers_csv_and_api_paths"
  - id: AC-2
    description: "Docs instruct users to create read-only keys, disable trade/withdraw/transfer permissions, and prefer IP allowlisting."
    test: "tests/test_exchange_import_runbook.py::test_exchange_runbook_covers_key_safety"
  - id: AC-3
    description: "Docs preserve no-advice, no-live-control, no-order-blocking, and local-secret boundaries."
    test: "tests/test_exchange_import_runbook.py::test_exchange_runbook_preserves_boundaries"

Files:
  - docs/AUDIT_WORKSPACE_RUNBOOK_RU.md
  - docs/PILOT_INTAKE_CONTRACT_RU.md
  - docs/EXCHANGE_API_IMPORT_PLAN_RU.md
  - tests/test_exchange_import_runbook.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/OBJECTION_HANDLING_RU.md

Notes: |
  Do not create hosted onboarding or public SaaS account flows.

## T60: Exchange Import CLI Safety Guidance

Owner:      codex
Phase:      15
Type:       docs
Depends-On: T59

Objective: |
  Add safe command examples, setup checklist, and troubleshooting guidance for local exchange imports.

Acceptance-Criteria:
  - id: AC-1
    description: "Guidance shows env-var and prompt-based secret input without committing keys to files."
    test: "tests/test_exchange_import_guidance.py::test_exchange_guidance_avoids_persisted_secrets"
  - id: AC-2
    description: "Guidance explains common failure states: non-read-only key, missing symbol/category, time range too wide, rate limit, and permission unverifiable."
    test: "tests/test_exchange_import_guidance.py::test_exchange_guidance_covers_failure_states"
  - id: AC-3
    description: "Guidance points users back to CSV upload if they do not want to create API keys."
    test: "tests/test_exchange_import_guidance.py::test_exchange_guidance_keeps_csv_fallback"

Files:
  - docs/EXCHANGE_IMPORT_GUIDE_RU.md
  - docs/EXCHANGE_IMPORT_GUIDE_EN.md
  - tests/test_exchange_import_guidance.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md

Notes: |
  Keep copy factual; do not imply exchange endorsement.

## T61: Exchange Import Evidence Fields

Owner:      codex
Phase:      15
Type:       none
Depends-On: T59

Objective: |
  Extend pilot evidence capture so validation can distinguish CSV pilots from read-only exchange-import pilots and track API-setup objections.

Acceptance-Criteria:
  - id: AC-1
    description: "Evidence row supports intake method values such as csv_export, bybit_read_only_api, and binance_read_only_api."
    test: "tests/unit/test_evidence_capture.py::test_evidence_capture_records_intake_method"
  - id: AC-2
    description: "Evidence summary can count exchange-import pilots separately from CSV pilots without including raw trade data."
    test: "tests/unit/test_evidence_capture.py::test_evidence_summary_counts_exchange_imports"
  - id: AC-3
    description: "Evidence docs list API key setup objections and safety concerns as non-sensitive fields."
    test: "tests/test_pilot_evidence_log.py::test_pilot_evidence_log_covers_exchange_import_fields"

Files:
  - trader_risk_audit/evidence.py
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - tests/unit/test_evidence_capture.py
  - tests/test_pilot_evidence_log.py

Context-Refs:
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - docs/adr/ADR-002-read-only-exchange-import.md

Notes: |
  Do not treat successful API connection as PMF. Payment and repeat-use evidence still matter.

## T62: Exchange Import Deep Review

Owner:      codex
Phase:      15
Type:       review
Depends-On: T59, T60, T61

Objective: |
  Run a phase-boundary deep review focused on secrets, permissions, reproducibility, deterministic truth, and product boundary after exchange import MVP work.

Acceptance-Criteria:
  - id: AC-1
    description: "Review reports P0/P1/P2 findings across code, architecture, security, docs, and tests."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, evidence index, and phase report are updated with final Phase 15 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any stop-ship finding is fixed before exchange import is considered pilot-ready."
    test: "manual/review"

Files:
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/IMPLEMENTATION_CONTRACT.md

Notes: |
  This is the release gate for calling read-only exchange import pilot-ready.

## T63: Real Audit Scope Lock

Owner:      operator + codex
Phase:      16
Type:       validation
Depends-On: none
Status:     [x] complete - open-source SEC Form 4 scope locked

Objective: |
  Define the first real Trader Risk Audit run or open-source artifact
  validation run: source, period, timezone, policy/rules, privacy boundary,
  allowed artifacts, and delivery format before any implementation or report
  generation work begins.

Acceptance-Criteria:
  - id: AC-1
    description: "A real audit scope note records trade source type, account/subaccount label or anonymized label, period, timezone, instrument universe, report language, and delivery format."
    test: "manual-evidence: operator scope note exists outside raw private data or in a sanitized committed doc."
  - id: AC-2
    description: "The scope note records whether the audit uses custom written rules or a starter profile, and lists unsupported/ambiguous rules."
    test: "manual-evidence: scope note policy section is complete."
  - id: AC-3
    description: "The privacy boundary states which files stay local, which may be committed after anonymization, and which may be shown externally."
    test: "manual-evidence: scope note privacy section is complete."

Files:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/REAL_AUDIT_SCOPE_OPEN_SOURCE_EN.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#3-phase-tra-af-0---real-audit-scope-lock
  - ../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md#phase-0---scope-lock-and-evidence-rules

Notes: |
  Do not commit raw private trade exports. If no private data is available,
  use a valid public/open-source transaction dataset with source metadata,
  privacy review, and explicit limits instead of inventing a synthetic
  substitute.

## T64: Real Data Intake And Policy Mapping

Owner:      codex
Phase:      16
Type:       validation
Depends-On: T63
Status:     [x] complete - SEC Form 4 intake and policy mapping reviewed

Objective: |
  Validate and normalize the real trade export or read-only historical export,
  load the selected policy, and produce a visible unsupported-field and policy
  mapping register.

Acceptance-Criteria:
  - id: AC-1
    description: "The real export either normalizes into canonical trade records or blocks with actionable field-level validation errors."
    test: "manual-evidence plus existing importer/validator command output."
  - id: AC-2
    description: "A sanitized schema summary lists mapped fields, missing fields, timezone assumptions, unsupported leverage/fee/position fields, and source row coverage."
    test: "manual-evidence: sanitized schema summary exists."
  - id: AC-3
    description: "Policy mapping review records custom/starter rules, unsupported rules, and any ambiguity before evaluation."
    test: "manual-evidence: policy mapping review exists and unresolved blockers are explicit."

Files:
  - trader_risk_audit/trades/
  - trader_risk_audit/policy/
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/REAL_DATA_INTAKE_SEC_FORM4_EN.md
  - docs/POLICY_MAPPING_REVIEW_SEC_FORM4_EN.md
  - demo/open_source_sec_form4_001/
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#4-phase-tra-af-1---real-data-intake-and-policy-mapping
  - docs/STARTER_POLICY_PROFILES_RU.md

Notes: |
  Add code or fixtures only for real parser/validation gaps discovered in this
  run. Use sanitized fixture rows only. Do not add live credential collection to
  bypass export friction.

## T65: First Real Audit Artifact Run

Owner:      codex
Phase:      16
Type:       validation
Depends-On: T64
Status:     [x] complete - SEC Form 4 artifact pack generated

Objective: |
  Run the deterministic audit workflow on the real validated input and produce
  the complete artifact pack: normalized trades, violations, attribution,
  report, delivery packet, manifest, and run notes.

Acceptance-Criteria:
  - id: AC-1
    description: "The audit run writes normalized trades, violation rows, attribution summary, Markdown report, delivery packet, and manifest or explicitly blocks with a documented reason."
    test: "manual-evidence: artifact pack exists or blocked-run note exists."
  - id: AC-2
    description: "The generated report includes executive summary, traceable violation table, P&L attribution, limitations, next-review checklist, and claim-safety disclaimer."
    test: "manual-evidence: report review."
  - id: AC-3
    description: "Manifest or run notes bind all safe input refs and generated output refs with hashes where possible."
    test: "manual-evidence: manifest/run notes review."

Files:
  - trader_risk_audit/cli.py
  - trader_risk_audit/artifacts/
  - trader_risk_audit/reporting/
  - trader_risk_audit/evaluation/
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/FIRST_AUDIT_RUN_SEC_FORM4_EN.md
  - demo/open_source_sec_form4_001/output/

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#5-phase-tra-af-2---first-real-audit-run

Notes: |
  Stop on attribution mismatch, unstable rerun results, missing source-row refs,
  or report claims that imply advice, causality, live control, or future
  performance.

## T66: Manual Calculation Validation

Owner:      operator + codex
Phase:      16
Type:       validation
Depends-On: T65
Status:     [x] complete - manual SEC Form 4 validation passed with P2 polish item

Objective: |
  Manually validate representative report findings against source data and
  record an error register before any external delivery.

Acceptance-Criteria:
  - id: AC-1
    description: "Manual validation covers at least 5-10 representative examples, including high-loss days, largest violations, and any cooldown/drawdown/position/forbidden-asset cases present."
    test: "manual-evidence: validation notes list reviewed examples."
  - id: AC-2
    description: "The error register labels findings P0/P1/P2/P3 and blocks external delivery for unresolved P0/P1 correctness issues."
    test: "manual-evidence: error register exists."
  - id: AC-3
    description: "Report limitations are updated or confirmed for every accepted unresolved limitation."
    test: "manual-evidence: report/limitations review."

Files:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/EVIDENCE_INDEX.md
  - docs/MANUAL_VALIDATION_SEC_FORM4_EN.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#6-phase-tra-af-3---manual-calculation-validation

Notes: |
  This task is allowed to produce manual evidence outside git when customer data
  is sensitive. Commit only sanitized summaries.

## T67: Report Polish And Claim Safety Review

Owner:      codex
Phase:      16
Type:       docs
Depends-On: T66
Status:     [x] complete - reviewed SEC report and packet are claim-safe

Objective: |
  Polish the real audit report and delivery packet so a non-developer can read
  the artifact quickly while all claims remain traceable and safe.

Acceptance-Criteria:
  - id: AC-1
    description: "Report first page/screen explains what was audited, strongest findings, material limitations, and next action."
    test: "manual-evidence: operator readability review."
  - id: AC-2
    description: "Delivery packet is copy-ready and does not expose raw private data or unsafe claims."
    test: "manual-evidence: delivery packet review."
  - id: AC-3
    description: "No-advice, no-performance, no-live-control, and unsupported-field boundaries remain visible."
    test: "manual-evidence: claim-safety review."

Files:
  - trader_risk_audit/reporting/
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/REPORT_POLISH_SEC_FORM4_EN.md
  - demo/open_source_sec_form4_001/output/report_reviewed.md
  - demo/open_source_sec_form4_001/output/telegram_packet_reviewed.txt

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#7-phase-tra-af-4---report-polish-and-operator-trust-review
  - docs/OBJECTION_HANDLING_RU.md

Notes: |
  Prefer report wording and layout improvements over new product surfaces.

## T68: Internal Demo Pack

Owner:      codex
Phase:      16
Type:       docs
Depends-On: T67
Status:     [x] complete - SEC open-source internal demo pack ready

Objective: |
  Package the validated real audit into an internal demo/pilot pack the operator
  can use in warm conversations without opening code or exposing sensitive raw
  data.

Acceptance-Criteria:
  - id: AC-1
    description: "Demo pack contains report, delivery packet, manifest/run notes, validation summary, safe excerpts/screenshots if available, and a short talk track."
    test: "manual-evidence: demo pack review."
  - id: AC-2
    description: "Demo pack redacts or excludes private trader identifiers and raw sensitive data."
    test: "manual-evidence: privacy review."
  - id: AC-3
    description: "Talk track leads to a paid audit pilot and does not imply SaaS, advice, or live-control scope."
    test: "manual-evidence: operator review."

Files:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/ICP_DEMO_VARIANTS_RU.md
  - docs/PAID_PILOT_OFFER_RU.md
  - docs/INTERNAL_DEMO_PACK_SEC_FORM4_EN.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#8-phase-tra-af-5---internal-demo-pack

Notes: |
  If a committed demo pack is needed, use sanitized/anonymized derivatives only.

## T69: External Pilot Ready Gate

Owner:      operator + codex
Phase:      16
Type:       review
Depends-On: T68
Status:     [x] complete - ready for controlled warm conversations

Objective: |
  Decide whether the real audit artifact is ready for controlled external
  pilot delivery and record the first paid pilot package scope.

Acceptance-Criteria:
  - id: AC-1
    description: "Ready-gate review states ready / needs fixes / reject input and cites report validity, unresolved findings, privacy, and claim safety."
    test: "manual-evidence: ready-gate review exists."
  - id: AC-2
    description: "Paid pilot package records inputs, deliverables, turnaround, pricing hypothesis, and feedback questions."
    test: "manual-evidence: paid pilot package section exists."
  - id: AC-3
    description: "CODEX prompt, README, implementation journal, and evidence index reflect the Phase 16 decision and next task."
    test: "manual/docs-review."

Files:
  - docs/audit/PHASE16_ARTIFACT_VALIDATION_REVIEW.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/EVIDENCE_INDEX.md
  - README.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#9-phase-tra-af-6---controlled-external-pilot-ready-gate
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is the gate for showing the validated artifact to warm prospects. It is
  not a gate for launching a public SaaS product.

## T70: Automated Intake Session Contract

Owner:      codex
Phase:      17
Type:       validation
Depends-On: T69
Status:     [x] complete - local intake session contract and CLI create command

Objective: |
  Define a local intake session contract that captures prospect/source metadata,
  privacy choices, expected export type, source timezone, display timezone
  (MSK by default for pilot evidence), session/currency, and safe status
  transitions before parsing any rows.

Acceptance-Criteria:
  - id: AC-1
    description: "Intake session model records source type, file refs, source timezone, display timezone, session, currency, privacy flags, prospect-safe label, and status without raw row data."
    test: "tests/unit/intake/test_intake_session.py::test_intake_session_records_safe_metadata"
  - id: AC-2
    description: "Session validation rejects credentials, API keys, private notes, Telegram handles, and unsupported live-control flags in metadata."
    test: "tests/unit/intake/test_intake_session.py::test_intake_session_rejects_sensitive_metadata"
  - id: AC-3
    description: "CLI can create a local intake session from explicit arguments and write a deterministic metadata JSON file."
    test: "tests/integration/test_intake_session_cli.py::test_intake_session_create_writes_safe_metadata"

Files:
  - trader_risk_audit/intake/
  - trader_risk_audit/cli.py
  - tests/unit/intake/test_intake_session.py
  - tests/integration/test_intake_session_cli.py
  - docs/AUTOMATED_PILOT_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/AUTOMATED_PILOT_ROADMAP.md
  - docs/PILOT_INTAKE_CONTRACT_RU.md
  - docs/IMPLEMENTATION_CONTRACT.md

Notes: |
  Keep this local-first. Do not add accounts, auth, uploads over HTTP, checkout,
  hosted storage, or exchange credential collection.

## T71: CSV Schema Profiler

Owner:      codex
Phase:      17
Type:       validation
Depends-On: T70
Status:     [x] complete - safe CSV schema profiler and CLI profile command

Objective: |
  Profile a submitted CSV/export before normalization and produce safe field
  mapping candidates, missing fields, row counts, duplicate risks, timezone
  assumptions, and unsupported data coverage.

Acceptance-Criteria:
  - id: AC-1
    description: "Profiler maps known aliases to canonical fields and reports missing timestamp/symbol/side/quantity/price fields without raw row leakage."
    test: "tests/unit/intake/test_csv_profiler.py::test_csv_profiler_maps_aliases_and_missing_fields"
  - id: AC-2
    description: "Profiler reports row count, duplicate row-id risk, timezone coverage, fee/leverage/P&L availability, and unsupported-field coverage."
    test: "tests/unit/intake/test_csv_profiler.py::test_csv_profiler_reports_coverage"
  - id: AC-3
    description: "CLI profile command writes deterministic sanitized schema summary for an intake session."
    test: "tests/integration/test_intake_profile_cli.py::test_intake_profile_writes_schema_summary"

Files:
  - trader_risk_audit/intake/
  - trader_risk_audit/trades/importers.py
  - trader_risk_audit/cli.py
  - tests/unit/intake/test_csv_profiler.py
  - tests/integration/test_intake_profile_cli.py
  - docs/AUTOMATED_PILOT_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - trader_risk_audit/trades/importers.py
  - docs/REAL_DATA_INTAKE_SEC_FORM4_EN.md

Notes: |
  This is a profiler, not the final normalizer. It should help a prospect fix
  export problems before a manual operator review.

## T72: Actionable Intake Report

Owner:      codex
Phase:      17
Type:       validation
Depends-On: T71
Status:     [x] complete - safe actionable intake Markdown report and CLI command

Objective: |
  Convert intake session metadata and schema profile into a prospect-readable
  intake report with accepted fields, blockers, unsupported checks, and next
  action.

Acceptance-Criteria:
  - id: AC-1
    description: "Intake report separates runnable, needs-user-fix, needs-operator-review, and rejected states with concrete reasons."
    test: "tests/unit/intake/test_intake_report.py::test_intake_report_status_sections"
  - id: AC-2
    description: "Report includes unsupported checks such as P&L, drawdown, leverage, fees, and account balance only when source fields are absent."
    test: "tests/unit/intake/test_intake_report.py::test_intake_report_lists_unsupported_checks"
  - id: AC-3
    description: "CLI emits a Markdown intake report without raw trade rows or private identifiers."
    test: "tests/integration/test_intake_report_cli.py::test_intake_report_cli_writes_safe_markdown"

Files:
  - trader_risk_audit/intake/
  - trader_risk_audit/cli.py
  - tests/unit/intake/test_intake_report.py
  - tests/integration/test_intake_report_cli.py
  - docs/AUTOMATED_PILOT_ROADMAP.md

Context-Refs:
  - docs/PILOT_INTAKE_CONTRACT_RU.md
  - docs/OBJECTION_HANDLING_RU.md

Notes: |
  The report should reduce operator labor and make user-fixable upload errors
  clear before a paid audit is requested.

## T73: Automated Intake Profiler Deep Review

Owner:      codex
Phase:      17
Type:       review
Depends-On: T70, T71, T72
Status:     [x] complete - Cycle 22 deep review archived with no stop-ship items

Objective: |
  Run the Phase 17 boundary review for automated intake profiling, focusing on
  privacy, raw-row leakage, deterministic profiling, and operator handoff.

Acceptance-Criteria:
  - id: AC-1
    description: "Review reports P0/P1/P2 findings across intake metadata, schema profiling, CLI output, docs, and tests."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, evidence index, and phase report are updated with final Phase 17 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any stop-ship privacy or raw-row leakage finding is fixed before Phase 18 begins."
    test: "manual/review"

Files:
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md
  - docs/IMPLEMENTATION_CONTRACT.md

Notes: |
  This is a phase gate. Do not skip deep review.

## T74: Supported Rule Catalog

Owner:      codex
Phase:      18
Type:       validation
Depends-On: T73
Status:     [x] complete - deterministic catalog and availability tests added

Objective: |
  Define a structured catalog of supported audit rule types, required inputs,
  threshold units, default copy, unsupported prerequisites, and profile
  applicability.

Acceptance-Criteria:
  - id: AC-1
    description: "Rule catalog lists every supported deterministic rule type with required source fields, threshold unit, and safe description."
    test: "tests/unit/policy/test_rule_catalog.py::test_rule_catalog_lists_supported_rules"
  - id: AC-2
    description: "Catalog marks rules as unavailable when intake profile lacks required fields such as P&L, leverage, fees, or account balance."
    test: "tests/unit/policy/test_rule_catalog.py::test_rule_catalog_marks_unavailable_rules"
  - id: AC-3
    description: "Catalog copy avoids advice, performance promises, and live-control language."
    test: "tests/unit/policy/test_rule_catalog.py::test_rule_catalog_copy_is_claim_safe"

Files:
  - trader_risk_audit/policy/
  - tests/unit/policy/test_rule_catalog.py
  - docs/AUTOMATED_PILOT_ROADMAP.md
  - docs/STARTER_POLICY_PROFILES_RU.md

Context-Refs:
  - trader_risk_audit/policy/schema.py
  - docs/STARTER_POLICY_PROFILES_RU.md

Notes: |
  This catalog is the basis for automated rule building. Do not allow arbitrary
  free text to become executable rule truth.

## T75: Profile-To-Policy Builder

Owner:      codex
Phase:      18
Type:       validation
Depends-On: T74
Status:     [x] complete - profile builder API and policy build CLI added

Objective: |
  Build valid `RiskPolicy` YAML/JSON from soft, medium, hard, and custom
  structured threshold selections without hand-written policy files.

Acceptance-Criteria:
  - id: AC-1
    description: "Builder creates valid policy objects from starter profiles and intake account/timezone/session metadata."
    test: "tests/unit/policy/test_policy_builder.py::test_policy_builder_creates_profile_policy"
  - id: AC-2
    description: "Builder accepts explicit threshold overrides only for supported rule catalog fields and validates units."
    test: "tests/unit/policy/test_policy_builder.py::test_policy_builder_validates_threshold_overrides"
  - id: AC-3
    description: "CLI can write generated policy YAML deterministically for an intake session."
    test: "tests/integration/test_policy_builder_cli.py::test_policy_builder_cli_writes_yaml"

Files:
  - trader_risk_audit/policy/
  - trader_risk_audit/cli.py
  - tests/unit/policy/test_policy_builder.py
  - tests/integration/test_policy_builder_cli.py

Context-Refs:
  - docs/STARTER_POLICY_PROFILES_RU.md
  - trader_risk_audit/policy/schema.py

Notes: |
  Keep custom free-text rules outside executable policy until T77 records them
  as unsupported/manual-review items.

## T76: Rule Builder Prompt Flow

Owner:      codex
Phase:      18
Type:       validation
Depends-On: T75
Status:     [x] complete - structured policy flow CLI and availability output added

Objective: |
  Add a local interactive/non-interactive CLI flow that asks only necessary
  structured questions and outputs a valid policy or actionable blockers.

Acceptance-Criteria:
  - id: AC-1
    description: "Non-interactive CLI accepts profile, thresholds, timezone/session, and account label to generate policy without prompts."
    test: "tests/integration/test_rule_builder_flow_cli.py::test_rule_builder_noninteractive"
  - id: AC-2
    description: "Interactive CLI can be tested with provided stdin and never echoes secrets or raw trade rows."
    test: "tests/integration/test_rule_builder_flow_cli.py::test_rule_builder_interactive_safe_output"
  - id: AC-3
    description: "Flow explains unavailable rules from the intake profile and suggests safe alternatives or manual review."
    test: "tests/unit/policy/test_rule_builder_flow.py::test_rule_builder_explains_unavailable_rules"

Files:
  - trader_risk_audit/policy/
  - trader_risk_audit/cli.py
  - tests/unit/policy/test_rule_builder_flow.py
  - tests/integration/test_rule_builder_flow_cli.py

Context-Refs:
  - docs/AUTOMATED_PILOT_ROADMAP.md

Notes: |
  This can be CLI-only. Do not add web UI or accounts.

## T77: Unsupported Rule Register

Owner:      codex
Phase:      18
Type:       validation
Depends-On: T76
Status:     [x] complete - sanitized unsupported-rule register and CLI append added

Objective: |
  Capture prospect free-text or unsupported rule requests as a safe register
  that can appear in report limitations and evidence, without executing them as
  deterministic rules.

Acceptance-Criteria:
  - id: AC-1
    description: "Unsupported rule register records user text as redacted/sanitized summary with reason code and manual-review status."
    test: "tests/unit/policy/test_unsupported_rule_register.py::test_register_sanitizes_unsupported_rules"
  - id: AC-2
    description: "Generated policy excludes unsupported rules while report/intake artifacts list them as limitations."
    test: "tests/unit/policy/test_unsupported_rule_register.py::test_unsupported_rules_do_not_enter_policy"
  - id: AC-3
    description: "CLI can append unsupported rules without accepting credentials, handles, or private notes."
    test: "tests/integration/test_unsupported_rule_register_cli.py::test_cli_rejects_sensitive_unsupported_rule_text"

Files:
  - trader_risk_audit/policy/
  - trader_risk_audit/cli.py
  - tests/unit/policy/test_unsupported_rule_register.py
  - tests/integration/test_unsupported_rule_register_cli.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md
  - trader_risk_audit/policy/review.py

Notes: |
  This preserves safety while still measuring what prospects ask for.

## T78: Structured Rule Builder Deep Review

Owner:      codex
Phase:      18
Type:       review
Depends-On: T74, T75, T76, T77
Status:     [x] complete - Cycle 23 deep review archived with no stop-ship items

Objective: |
  Run the Phase 18 boundary review for structured policy generation and
  unsupported-rule handling.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks deterministic rule ownership, unsupported text safety, claim boundaries, and policy validity."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, evidence index, and phase report are updated with final Phase 18 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any P0/P1 policy truth or advice-language finding is fixed before Phase 19 begins."
    test: "manual/review"

Files:
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

## T79: Audit Session Runner

Owner:      codex
Phase:      19
Type:       validation
Depends-On: T78
Status:     [x] complete - local audit session runner and safe run status added
Completed:  2026-05-15

Objective: |
  Add a local one-click runner that consumes an intake session and generated
  policy, then runs normalization, evaluation, attribution, report, packet, and
  manifest generation.

Acceptance-Criteria:
  - id: AC-1
    description: "Runner executes end-to-end from intake session + policy refs and writes a run status file."
    test: "tests/integration/test_audit_session_runner.py::test_runner_writes_complete_status"
  - id: AC-2
    description: "Runner blocks before report generation when intake status or policy status is not runnable."
    test: "tests/integration/test_audit_session_runner.py::test_runner_blocks_unready_inputs"
  - id: AC-3
    description: "Runner output never includes raw private rows in status, logs, or CLI stdout."
    test: "tests/integration/test_audit_session_runner.py::test_runner_status_is_safe"

Files:
  - trader_risk_audit/audit_session/
  - trader_risk_audit/cli.py
  - tests/integration/test_audit_session_runner.py

Context-Refs:
  - trader_risk_audit/cli.py
  - docs/AUTOMATED_PILOT_ROADMAP.md

Notes: |
  Use the existing deterministic audit internals. Do not create a long-lived
  worker or service.

## T80: Artifact Bundle Index

Owner:      codex
Phase:      19
Type:       validation
Depends-On: T79
Status:     [x] complete - safe local bundle index and summary CLI added
Completed:  2026-05-15

Objective: |
  Produce a single local bundle index for every automated audit run that points
  to input metadata, normalized trades, report, packet, manifest, preview state,
  and limitation registers.

Acceptance-Criteria:
  - id: AC-1
    description: "Bundle index records safe artifact refs, hashes, status, and limitation refs without raw trade rows."
    test: "tests/unit/audit_session/test_artifact_bundle.py::test_bundle_index_records_safe_refs"
  - id: AC-2
    description: "Bundle validation catches missing or drifted required artifacts."
    test: "tests/unit/audit_session/test_artifact_bundle.py::test_bundle_validation_catches_drift"
  - id: AC-3
    description: "CLI can print a concise safe bundle summary for the operator."
    test: "tests/integration/test_artifact_bundle_cli.py::test_bundle_summary_is_safe"

Files:
  - trader_risk_audit/audit_session/
  - trader_risk_audit/cli.py
  - tests/unit/audit_session/test_artifact_bundle.py
  - tests/integration/test_artifact_bundle_cli.py

Context-Refs:
  - trader_risk_audit/artifacts/manifest.py

Notes: |
  This is the local substitute for a dashboard until Phase 21.

## T81: Automated Run Reproducibility Gate

Owner:      codex
Phase:      19
Type:       validation
Depends-On: T80
Status:     [x] complete - automated rerun hash gate added
Completed:  2026-05-15

Objective: |
  Add a reproducibility gate that can rerun an automated audit session in a
  separate output directory and compare content hashes before preview or
  delivery.

Acceptance-Criteria:
  - id: AC-1
    description: "Reproducibility gate reruns an audit session and reports matching/mismatched content hash."
    test: "tests/integration/test_audit_session_reproducibility.py::test_reproducibility_gate_matches_hash"
  - id: AC-2
    description: "Mismatches block preview/delivery status and include actionable artifact refs."
    test: "tests/integration/test_audit_session_reproducibility.py::test_reproducibility_mismatch_blocks_preview"
  - id: AC-3
    description: "Gate excludes generated timestamps and local output paths from deterministic comparison."
    test: "tests/unit/audit_session/test_reproducibility_gate.py::test_reproducibility_excludes_paths_and_timestamps"

Files:
  - trader_risk_audit/audit_session/
  - tests/unit/audit_session/test_reproducibility_gate.py
  - tests/integration/test_audit_session_reproducibility.py

Context-Refs:
  - trader_risk_audit/artifacts/manifest.py
  - docs/FIRST_AUDIT_RUN_SEC_FORM4_EN.md

Notes: |
  Preview should not proceed on nondeterministic artifact drift.

## T82: One-Click Audit Runner Deep Review

Owner:      codex
Phase:      19
Type:       review
Depends-On: T79, T80, T81
Status:     [x] complete - Cycle 24 deep review archived with no stop-ship items
Completed:  2026-05-15

Objective: |
  Run the Phase 19 boundary review for automated audit session execution and
  reproducibility.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks runner determinism, safe status output, artifact references, and no runtime-tier drift."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, evidence index, and phase report are updated with final Phase 19 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any stop-ship artifact drift or raw-data leakage finding is fixed before Phase 20 begins."
    test: "manual/review"

Files:
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

## T83: Claim-Safe Report Preview Model

Owner:      codex
Phase:      20
Type:       validation
Depends-On: T82
Status:     [x] complete - redacted claim-safe preview model and CLI added
Completed:  2026-05-15

Objective: |
  Generate a limited preview from a completed audit bundle that shows value,
  limitations, and next action without exposing full source-row tables or unsafe
  claims.

Acceptance-Criteria:
  - id: AC-1
    description: "Preview model includes counts, top rule categories, unsupported fields, and safe source coverage without full raw rows."
    test: "tests/unit/preview/test_preview_model.py::test_preview_model_is_redacted"
  - id: AC-2
    description: "Preview text passes claim guard and contains required no-advice/no-live-control boundary."
    test: "tests/unit/preview/test_preview_model.py::test_preview_claim_guard"
  - id: AC-3
    description: "CLI can generate preview Markdown from an artifact bundle."
    test: "tests/integration/test_preview_cli.py::test_preview_cli_writes_markdown"

Files:
  - trader_risk_audit/preview/
  - trader_risk_audit/cli.py
  - tests/unit/preview/test_preview_model.py
  - tests/integration/test_preview_cli.py

Context-Refs:
  - trader_risk_audit/reporting/claim_guard.py
  - docs/REPORT_POLISH_SEC_FORM4_EN.md

Notes: |
  Preview should create enough interest for a paid reviewed report, not give
  away unsafe or unsupported conclusions.

## T84: Paid Pilot CTA Copy And Package

Owner:      codex
Phase:      20
Type:       docs
Depends-On: T83
Status:     [x] complete - manual paid-pilot CTA copy and eligible preview packaging added
Completed:  2026-05-15

Objective: |
  Attach a narrow paid pilot CTA to preview output with inputs, deliverables,
  turnaround, pricing hypothesis, and boundaries.

Acceptance-Criteria:
  - id: AC-1
    description: "CTA states one manual reviewed audit report, required inputs, 48-72 hour turnaround, and $49-$149 pricing hypothesis."
    test: "tests/test_paid_preview_cta.py::test_paid_preview_cta_package_terms"
  - id: AC-2
    description: "CTA does not imply SaaS, checkout, advice, live-control, or guaranteed improvement."
    test: "tests/test_paid_preview_cta.py::test_paid_preview_cta_boundaries"
  - id: AC-3
    description: "Preview output includes CTA only when intake/report status is eligible."
    test: "tests/unit/preview/test_preview_cta.py::test_preview_cta_requires_eligible_status"

Files:
  - trader_risk_audit/preview/
  - docs/PAID_PILOT_OFFER_RU.md
  - docs/PAID_PILOT_OFFER_EN.md
  - tests/test_paid_preview_cta.py
  - tests/unit/preview/test_preview_cta.py

Context-Refs:
  - docs/audit/PHASE16_ARTIFACT_VALIDATION_REVIEW.md
  - docs/PAID_PILOT_OFFER_RU.md

Notes: |
  This is CTA copy and local preview packaging, not checkout implementation.

## T85: Preview Conversion Events

Owner:      codex
Phase:      20
Type:       validation
Depends-On: T84
Status:     [x] complete - privacy-safe preview conversion events and CLI summary added
Completed:  2026-05-15

Objective: |
  Record privacy-safe events for preview generated, preview opened, CTA shown,
  CTA accepted/requested, and objections.

Acceptance-Criteria:
  - id: AC-1
    description: "Conversion event schema stores event type, timestamp, intake id, source type, and objection tags without raw rows or private identifiers."
    test: "tests/unit/evidence/test_preview_events.py::test_preview_event_schema_is_safe"
  - id: AC-2
    description: "CLI can append preview/CTA events and summarize counts."
    test: "tests/integration/test_preview_events_cli.py::test_preview_events_cli_summary"
  - id: AC-3
    description: "Events integrate with existing pilot evidence summary without counting demos/open-source samples as paid evidence."
    test: "tests/unit/evidence/test_preview_events.py::test_preview_events_do_not_count_demo_as_paid"

Files:
  - trader_risk_audit/evidence.py
  - trader_risk_audit/cli.py
  - tests/unit/evidence/test_preview_events.py
  - tests/integration/test_preview_events_cli.py

Context-Refs:
  - trader_risk_audit/evidence.py
  - docs/PILOT_EVIDENCE_LOG_RU.md

Notes: |
  Evidence must measure hypothesis validation, not vanity usage.

## T86: Paid Unlock Boundary

Owner:      codex
Phase:      20
Type:       validation
Depends-On: T85
Status:     [x] complete - local paid preview unlock status boundary added
Completed:  2026-05-15

Objective: |
  Define local status transitions for preview-only, paid-requested,
  operator-reviewed, and delivered report packages without implementing
  payment processing or checkout.

Acceptance-Criteria:
  - id: AC-1
    description: "Status model separates preview from full reviewed report and blocks delivery when review/claim safety is missing."
    test: "tests/unit/preview/test_paid_unlock_boundary.py::test_paid_unlock_status_blocks_unreviewed_delivery"
  - id: AC-2
    description: "Paid-requested status records manual payment/intent evidence without storing payment identifiers."
    test: "tests/unit/preview/test_paid_unlock_boundary.py::test_paid_requested_status_is_privacy_safe"
  - id: AC-3
    description: "CLI can mark paid-requested/operator-reviewed/delivered with safe metadata."
    test: "tests/integration/test_paid_unlock_cli.py::test_paid_unlock_cli_status_flow"

Files:
  - trader_risk_audit/preview/
  - trader_risk_audit/evidence.py
  - trader_risk_audit/cli.py
  - tests/unit/preview/test_paid_unlock_boundary.py
  - tests/integration/test_paid_unlock_cli.py

Context-Refs:
  - docs/PAID_PILOT_OFFER_RU.md
  - docs/IMPLEMENTATION_CONTRACT.md

Notes: |
  Do not implement Stripe, checkout, accounts, invoices, or hosted payment data.

## T87: Preview And Paid CTA Deep Review

Owner:      codex
Phase:      20
Type:       review
Depends-On: T83, T84, T85, T86
Status:     [x] complete - Cycle 25 deep review archived with no stop-ship items
Completed:  2026-05-15

Objective: |
  Run the Phase 20 boundary review for claim-safe preview, CTA copy, conversion
  events, and paid unlock boundary.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks claim safety, preview redaction, paid evidence integrity, and no checkout/SaaS scope creep."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, evidence index, and phase report are updated with final Phase 20 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any P0/P1 unsafe claim or payment-data finding is fixed before Phase 21 begins."
    test: "manual/review"

Files:
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

## T88: Hypothesis Funnel Event Schema

Owner:      codex
Phase:      21
Type:       validation
Depends-On: T87
Status:     complete

Objective: |
  Define a single evidence schema for automated hypothesis funnel events:
  prospect qualified, intake started, valid export, policy built, audit run,
  preview generated, CTA accepted, paid report, repeat commitment, referral.

Acceptance-Criteria:
  - id: AC-1
    description: "Funnel schema supports required event types and rejects raw trade data, credentials, direct identifiers, and payment identifiers."
    test: "tests/unit/evidence/test_hypothesis_funnel.py::test_funnel_schema_rejects_sensitive_fields"
  - id: AC-2
    description: "Event loader can read old pilot evidence rows and new funnel events together."
    test: "tests/unit/evidence/test_hypothesis_funnel.py::test_funnel_loader_preserves_legacy_rows"
  - id: AC-3
    description: "Evidence docs define which events count toward hypothesis gates and which are vanity/demo events."
    test: "tests/test_hypothesis_evidence_docs.py::test_hypothesis_docs_define_gate_events"

Files:
  - trader_risk_audit/evidence.py
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md
  - tests/unit/evidence/test_hypothesis_funnel.py
  - tests/test_hypothesis_evidence_docs.py

Context-Refs:
  - docs/PILOT_EVIDENCE_LOG_RU.md
  - docs/audit/PHASE16_ARTIFACT_VALIDATION_REVIEW.md

Notes: |
  This is measurement infrastructure, not a CRM.

## T89: Evidence Dashboard CLI

Owner:      codex
Phase:      21
Type:       validation
Depends-On: T88
Status:     complete

Objective: |
  Add a local dashboard command that summarizes funnel counts, conversion
  ratios, gate status, objections, unsupported-field blockers, and next action.

Acceptance-Criteria:
  - id: AC-1
    description: "Dashboard summarizes counts for qualified prospects, intake started, valid export, preview, CTA accepted, paid report, repeat, and referral."
    test: "tests/integration/test_hypothesis_dashboard_cli.py::test_dashboard_cli_counts_funnel"
  - id: AC-2
    description: "Dashboard excludes demos/open-source samples from paid/PMF evidence while still listing them as artifact evidence."
    test: "tests/integration/test_hypothesis_dashboard_cli.py::test_dashboard_excludes_demo_from_paid_gate"
  - id: AC-3
    description: "Dashboard prints no raw trade rows or private identifiers."
    test: "tests/integration/test_hypothesis_dashboard_cli.py::test_dashboard_output_is_privacy_safe"

Files:
  - trader_risk_audit/evidence.py
  - trader_risk_audit/cli.py
  - tests/integration/test_hypothesis_dashboard_cli.py

Context-Refs:
  - docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md

Notes: |
  Keep this local CLI/report first. Do not build web dashboard yet.

## T90: Hypothesis Gate Rules

Owner:      codex
Phase:      21
Type:       validation
Depends-On: T89
Status:     complete

Objective: |
  Encode explicit hypothesis gate rules for proceed / needs more evidence /
  pivot decisions based on paid audits, repeat commitments, referrals, and
  blocking objections.

Acceptance-Criteria:
  - id: AC-1
    description: "Gate evaluator returns proceed when thresholds are met: 10 qualified, 5 valid exports/rules, 3 paid reports, 2 repeat/referral signals."
    test: "tests/unit/evidence/test_hypothesis_gates.py::test_gate_evaluator_proceed"
  - id: AC-2
    description: "Gate evaluator returns needs_more_evidence or pivot with concrete reasons when thresholds are not met or objections dominate."
    test: "tests/unit/evidence/test_hypothesis_gates.py::test_gate_evaluator_needs_more_or_pivot"
  - id: AC-3
    description: "Gate docs warn that uploads/API connections alone are not PMF."
    test: "tests/test_hypothesis_evidence_docs.py::test_hypothesis_docs_reject_vanity_metrics"

Files:
  - trader_risk_audit/evidence.py
  - docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md
  - tests/unit/evidence/test_hypothesis_gates.py
  - tests/test_hypothesis_evidence_docs.py

Context-Refs:
  - docs/INTERNAL_DEMO_PACK_SEC_FORM4_EN.md
  - docs/PAID_PILOT_OFFER_RU.md

Notes: |
  This is the product decision gate before larger automation investments.

## T91: Privacy-Safe Evidence Export

Owner:      codex
Phase:      21
Type:       validation
Depends-On: T90
Status:     complete

Objective: |
  Export hypothesis evidence as a sanitized CSV/Markdown report for review,
  preserving metrics and objections while excluding raw user data.

Acceptance-Criteria:
  - id: AC-1
    description: "Export command writes CSV and Markdown summaries with aggregate counts, gate verdict, and objection tags."
    test: "tests/integration/test_evidence_export_cli.py::test_evidence_export_writes_safe_reports"
  - id: AC-2
    description: "Export scanner rejects emails, phone numbers, Telegram handles, payment ids, credentials, and raw row-like fields."
    test: "tests/unit/evidence/test_evidence_export_privacy.py::test_evidence_export_rejects_sensitive_fields"
  - id: AC-3
    description: "Export includes enough provenance to reproduce gate calculation from source event log."
    test: "tests/unit/evidence/test_evidence_export_privacy.py::test_evidence_export_includes_provenance"

Files:
  - trader_risk_audit/evidence.py
  - trader_risk_audit/cli.py
  - tests/unit/evidence/test_evidence_export_privacy.py
  - tests/integration/test_evidence_export_cli.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md

Notes: |
  This report can support investor/advisor discussions without exposing users.

## T92: Hypothesis Evidence Dashboard Deep Review

Owner:      codex
Phase:      21
Type:       review
Depends-On: T88, T89, T90, T91
Status:     complete

Objective: |
  Run the Phase 21 boundary review for automated evidence capture, dashboard,
  gate rules, and privacy-safe export.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks evidence integrity, vanity metric separation, privacy safety, and gate correctness."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, evidence index, and phase report are updated with final Phase 21 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any P0/P1 privacy or false-PMF finding is fixed before Phase 22 begins."
    test: "manual/review"

Files:
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

## T93: CSV Friction Decision Gate

Owner:      operator + codex
Phase:      22
Type:       review
Depends-On: T92
Status:     complete

Objective: |
  Decide from Phase 21 evidence whether CSV/export upload friction justifies
  implementing real local read-only exchange network fetching.

Acceptance-Criteria:
  - id: AC-1
    description: "Decision report quantifies CSV/export blockers, valid-export drop-off, API-request objections, and paid-intent evidence."
    test: "manual-evidence: CSV friction decision report exists."
  - id: AC-2
    description: "Decision is proceed / defer / reject for real read-only fetch, with explicit safety and commercial rationale."
    test: "manual-evidence: decision verdict exists."
  - id: AC-3
    description: "If proceed, ADR update task is activated before implementation; if defer/reject, T94-T97 remain blocked."
    test: "manual/docs-review"

Files:
  - docs/EXCHANGE_API_IMPORT_PLAN_RU.md
  - docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/tasks.md

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md

Notes: |
  Do not implement real exchange network fetching unless this gate says proceed.

## T94: Real Read-Only Import ADR Update

Owner:      codex
Phase:      22
Type:       docs
Depends-On: T93
Status:     blocked_by_t93_defer

Objective: |
  If T93 says proceed, update ADR-002 or add a new ADR for minimal real local
  read-only exchange network fetching with no hosted secrets and no write/control
  endpoints.

Acceptance-Criteria:
  - id: AC-1
    description: "ADR states allowed exchange(s), endpoints, credential input method, redaction rules, rate-limit behavior, and stop conditions."
    test: "manual/docs-review"
  - id: AC-2
    description: "ADR explicitly forbids hosted secrets, write/control endpoints, withdrawals, transfers, order placement, order cancellation, leverage/margin mutation, and Telegram credential collection."
    test: "tests/test_exchange_import_runbook.py::test_exchange_runbook_preserves_boundaries"
  - id: AC-3
    description: "CODEX prompt, tasks, and exchange import plan reflect the ADR decision before any code implementation."
    test: "manual/docs-review"

Files:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/EXCHANGE_API_IMPORT_PLAN_RU.md
  - docs/CODEX_PROMPT.md
  - docs/tasks.md

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/EXCHANGE_IMPORT_GUIDE_EN.md
  - docs/EXCHANGE_IMPORT_GUIDE_RU.md

Notes: |
  This task is conditional. If T93 is not proceed, mark blocked/deferred.

## T95: Minimal Local Real Fetch Path

Owner:      codex
Phase:      22
Type:       validation
Depends-On: T94
Status:     blocked_by_t93_defer

Objective: |
  Implement the smallest real local read-only fetch path approved by ADR:
  explicit symbol/category/range, local env/prompt secrets, redacted request
  metadata, raw snapshot, no hosted secret storage, no write/control endpoints.

Acceptance-Criteria:
  - id: AC-1
    description: "Fetch command requires explicit scope and refuses missing symbol/category/range or non-read-only permission status."
    test: "tests/integration/test_real_read_only_fetch_cli.py::test_fetch_requires_explicit_scope"
  - id: AC-2
    description: "Fetched raw snapshot and logs contain no credentials, signatures, account ids, or secret-bearing request strings."
    test: "tests/integration/test_real_read_only_fetch_redaction.py::test_real_fetch_redacts_secrets"
  - id: AC-3
    description: "Endpoint allowlist excludes order/write/withdraw/transfer/leverage/margin mutation endpoints."
    test: "tests/unit/exchange/test_real_fetch_endpoint_allowlist.py::test_real_fetch_has_no_write_endpoints"

Files:
  - trader_risk_audit/exchange/
  - trader_risk_audit/cli.py
  - tests/unit/exchange/test_real_fetch_endpoint_allowlist.py
  - tests/integration/test_real_read_only_fetch_cli.py
  - tests/integration/test_real_read_only_fetch_redaction.py

Context-Refs:
  - docs/adr/ADR-002-read-only-exchange-import.md
  - docs/EXCHANGE_IMPORT_GUIDE_EN.md

Notes: |
  This task may need network-mocked tests by default and manual real-run notes
  outside git. Do not commit real account data.

## T96: Real Import To Automated Runner

Owner:      codex
Phase:      22
Type:       validation
Depends-On: T95
Status:     blocked_by_t93_defer

Objective: |
  Connect the approved real read-only raw snapshot path to the automated intake
  profiler and one-click audit runner.

Acceptance-Criteria:
  - id: AC-1
    description: "Real read-only snapshot can be profiled into safe intake metadata and unsupported-field report."
    test: "tests/integration/test_real_import_to_intake.py::test_real_snapshot_profiles_to_intake"
  - id: AC-2
    description: "Normalized output from real read-only snapshot can feed audit session runner deterministically."
    test: "tests/integration/test_real_import_to_runner.py::test_real_import_feeds_runner"
  - id: AC-3
    description: "Evidence events distinguish CSV pilots from real read-only import pilots without treating API connection as PMF."
    test: "tests/unit/evidence/test_real_import_evidence.py::test_real_import_evidence_is_not_pmf"

Files:
  - trader_risk_audit/exchange/
  - trader_risk_audit/intake/
  - trader_risk_audit/audit_session/
  - trader_risk_audit/evidence.py
  - tests/integration/test_real_import_to_intake.py
  - tests/integration/test_real_import_to_runner.py
  - tests/unit/evidence/test_real_import_evidence.py

Context-Refs:
  - docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md
  - docs/adr/ADR-002-read-only-exchange-import.md

Notes: |
  Keep CSV fallback visible. API connection success alone is not validation.

## T97: Conditional Real Import Deep Review

Owner:      codex
Phase:      22
Type:       review
Depends-On: T93, T94, T95, T96
Status:     blocked_by_t93_defer

Objective: |
  Run the Phase 22 boundary review for the CSV-friction decision and any
  approved real read-only import implementation.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks evidence justification, ADR compliance, secrets, permissions, endpoint allowlist, reproducibility, and no live-control scope."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, evidence index, and phase report are updated with final Phase 22 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any P0/P1 secret, permission, or exchange-control finding is fixed before real import is considered validated."
    test: "manual/review"

Files:
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md
  - docs/adr/ADR-002-read-only-exchange-import.md

Notes: |
  This is a phase gate. Do not skip deep review.

## T98: Open-Source Source Selection Protocol

Owner:      operator + codex
Phase:      23
Type:       docs
Depends-On: T93

Objective: |
  Define the source-selection protocol for the open-source audit case bank so
  the next validation loop cannot cherry-pick only impressive positive cases.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/OPEN_SOURCE_CASE_BANK.md` defines allowed source classes, excluded source classes, selection rationale, license/terms notes, and anti-cherry-pick batch composition."
    test: "manual/docs-review"
  - id: AC-2
    description: "Protocol requires each batch to include at least one positive-finding case, one limitation/reject case, and one edge/schema case when available."
    test: "manual/docs-review"
  - id: AC-3
    description: "Protocol states that public/open-source packs are artifact-quality evidence, not paid-pilot, PMF, or customer evidence."
    test: "manual/docs-review"

Files:
  - docs/OPEN_SOURCE_CASE_BANK.md
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md
  - docs/DECISION_LOG.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-23---open-source-audit-case-bank
  - docs/CSV_FRICTION_DECISION_REPORT.md

Notes: |
  Do not collect private data in this task. Do not reopen real exchange fetching.

## T99: Case Pack Directory Contract

Owner:      codex
Phase:      23
Type:       validation
Depends-On: T98

Objective: |
  Define and test the required directory/file contract for every open-source
  audit case pack.

Acceptance-Criteria:
  - id: AC-1
    description: "A validator confirms each case pack has source note, policy, input fixture, generated report, reviewed report, manifest, violations, attribution, and reproducibility status when applicable."
    test: "tests/unit/test_open_source_case_contract.py::test_case_pack_contract_requires_core_artifacts"
  - id: AC-2
    description: "Validator rejects packs that contain secret-looking fields, private paths, credentials, Telegram handles, account ids, or unreviewed customer/private markers."
    test: "tests/unit/test_open_source_case_contract.py::test_case_pack_contract_rejects_private_or_secret_markers"
  - id: AC-3
    description: "The SEC Form 4 pack is registered as a passing reference pack under the new contract."
    test: "tests/integration/test_open_source_case_contract_cli.py::test_sec_form4_pack_passes_contract"

Files:
  - trader_risk_audit/validation/open_source_case.py
  - trader_risk_audit/cli.py
  - tests/unit/test_open_source_case_contract.py
  - tests/integration/test_open_source_case_contract_cli.py
  - demo/open_source_sec_form4_001/

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-23---open-source-audit-case-bank

Notes: |
  Prefer a small reusable validator over ad hoc docs-only review.

## T100: First Open-Source Candidate Case Packs

Owner:      operator + codex
Phase:      23
Type:       validation
Depends-On: T99

Objective: |
  Create the first batch of open-source or synthetic edge-case candidate packs
  beyond the existing SEC Form 4 baseline.

Acceptance-Criteria:
  - id: AC-1
    description: "At least 5 total candidate packs are listed in `docs/OPEN_SOURCE_CASE_BANK.md`, including the existing SEC Form 4 pack."
    test: "manual/docs-review"
  - id: AC-2
    description: "At least 3 different data shapes are represented, such as disclosure-like rows, broker/export-like rows, and synthetic edge-case rows."
    test: "manual/docs-review"
  - id: AC-3
    description: "Each candidate records source rationale, expected evaluable fields, expected limitations, and whether it should produce positive findings, limitations, or rejection."
    test: "manual/docs-review"

Files:
  - docs/OPEN_SOURCE_CASE_BANK.md
  - demo/
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#anti-cherry-pick-rule

Notes: |
  If a public dataset cannot be safely committed, record only source metadata
  and use a sanitized fixture. Do not invent fake provenance.

## T101: Batch Audit Run And Artifact Generation

Owner:      codex
Phase:      23
Type:       validation
Depends-On: T100

Objective: |
  Run the deterministic audit loop for every approved Phase 23 candidate pack
  and generate complete artifact bundles.

Acceptance-Criteria:
  - id: AC-1
    description: "Every runnable candidate pack has generated normalized trades, violations, attribution, report, manifest, Telegram/delivery packet if applicable, and safe run status."
    test: "manual-evidence: generated artifacts exist and validator passes."
  - id: AC-2
    description: "Every non-runnable candidate pack has an explicit blocked/rejected status with actionable reasons and no partial report claims."
    test: "manual-evidence: blocked pack status exists."
  - id: AC-3
    description: "A batch index summarizes pack status, finding count, limitation count, and reproducibility status without raw private rows."
    test: "manual-evidence: `docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md` exists."

Files:
  - demo/
  - docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md
  - trader_risk_audit/audit_session/
  - trader_risk_audit/cli.py

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-23---open-source-audit-case-bank

Notes: |
  This task may reuse existing audit-session and artifact-bundle commands.

## T102: Manual Validation Notes And Error Register

Owner:      operator + codex
Phase:      23
Type:       validation
Depends-On: T101

Objective: |
  Manually review the generated open-source audit packs and record any report,
  calculation, traceability, or wording issues.

Acceptance-Criteria:
  - id: AC-1
    description: "Each generated pack has a manual review note under `docs/audit/open_source_case_reviews/`."
    test: "manual/docs-review"
  - id: AC-2
    description: "A Phase 23 error register classifies P0/P1/P2 findings and blocks demo use for unresolved P0/P1 issues."
    test: "manual/docs-review"
  - id: AC-3
    description: "Reviewed reports explicitly preserve material limitations and do not hide weak/reject cases."
    test: "manual/docs-review"

Files:
  - docs/audit/open_source_case_reviews/
  - docs/audit/PHASE23_ERROR_REGISTER.md
  - demo/
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-23---open-source-audit-case-bank

Notes: |
  Do not polish away evidence problems. Record them.

## T103: Open-Source Case Bank Deep Review

Owner:      codex
Phase:      23
Type:       review
Depends-On: T98, T99, T100, T101, T102

Objective: |
  Run the Phase 23 boundary review and decide whether enough case-bank
  evidence exists to enter the multi-case report quality loop.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks anti-cherry-pick compliance, source safety, artifact completeness, reproducibility, report truth, and limitation wording."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, handoff docs, and phase report are updated with final Phase 23 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any unresolved P0/P1 artifact-validity issue blocks Phase 24 until fixed."
    test: "manual/review"

Files:
  - docs/archive/PHASE23_REVIEW.md
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

## T104: Report Quality Scorecard

Owner:      codex
Phase:      24
Type:       docs
Depends-On: T103

Objective: |
  Define a repeatable scorecard for judging whether a generated audit report is
  readable, traceable, reproducible, and safe to show.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/REPORT_QUALITY_SCORECARD.md` defines scoring categories for source traceability, rule clarity, calculation clarity, limitation clarity, claim safety, and operator readability."
    test: "manual/docs-review"
  - id: AC-2
    description: "Scorecard includes fail conditions that block demo use regardless of total score."
    test: "manual/docs-review"
  - id: AC-3
    description: "At least the SEC Form 4 reviewed report is scored as the reference example."
    test: "manual/docs-review"

Files:
  - docs/REPORT_QUALITY_SCORECARD.md
  - demo/open_source_sec_form4_001/output/report_reviewed.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-24---multi-case-report-quality-loop

Notes: |
  Scoring is a review aid, not a marketing claim.

## T105: Open-Source Rule And Data Coverage Matrix

Owner:      codex
Phase:      24
Type:       validation
Depends-On: T104

Objective: |
  Build a matrix showing which rules, data fields, limitations, and report
  sections are exercised by each open-source validation pack.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md` maps case packs to rule types, required fields, unsupported fields, limitations, and output sections."
    test: "manual/docs-review"
  - id: AC-2
    description: "Matrix highlights missing coverage needed before a paid pilot, such as P&L, fees, drawdown, cooldown, leverage, or session timezone cases."
    test: "manual/docs-review"
  - id: AC-3
    description: "Missing coverage becomes explicit follow-up cases or accepted limitations."
    test: "manual/docs-review"

Files:
  - docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md
  - docs/OPEN_SOURCE_CASE_BANK.md
  - demo/

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-24---multi-case-report-quality-loop

Notes: |
  Do not treat coverage gaps as failures if they are clearly stated.

## T106: Multi-Case Quality Dashboard

Owner:      codex
Phase:      24
Type:       validation
Depends-On: T105

Objective: |
  Summarize the open-source validation pack results in one operator-facing
  dashboard for readiness decisions.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md` lists every pack, status, scorecard result, finding count, limitation count, error-register status, and reproducibility status."
    test: "manual/docs-review"
  - id: AC-2
    description: "Dashboard separates demo-quality packs from internal-only packs and blocked packs."
    test: "manual/docs-review"
  - id: AC-3
    description: "Dashboard states the next concrete case/data gap to fill before private pilot readiness."
    test: "manual/docs-review"

Files:
  - docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md
  - docs/REPORT_QUALITY_SCORECARD.md
  - docs/audit/PHASE23_ERROR_REGISTER.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-24---multi-case-report-quality-loop

Notes: |
  Keep dashboard aggregate and privacy-safe.

## T107: Regression Tests For Discovered Report Issues

Owner:      codex
Phase:      24
Type:       validation
Depends-On: T106

Objective: |
  Convert any discovered calculation, formatting, limitation, or claim-safety
  issue from Phase 23/24 review into focused regression coverage.

Acceptance-Criteria:
  - id: AC-1
    description: "Every accepted P0/P1/P2 code or report-generation bug has a regression test or a documented reason why it is docs-only."
    test: "manual/docs-review plus pytest"
  - id: AC-2
    description: "Report claim guard tests cover any newly discovered unsafe wording pattern."
    test: "pytest tests -q --tb=short"
  - id: AC-3
    description: "Test baseline is updated in `docs/CODEX_PROMPT.md` after passing."
    test: "manual/docs-review"

Files:
  - trader_risk_audit/
  - tests/
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md
  - docs/audit/PHASE23_ERROR_REGISTER.md

Notes: |
  Keep fixes scoped to real findings. Do not refactor unrelated report code.

## T108: Internal Demo Pack From Validated Cases

Owner:      codex
Phase:      24
Type:       docs
Depends-On: T107

Objective: |
  Package the strongest validated open-source cases into a concise internal
  demo pack for warm prospect conversations.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md` includes one strong positive case, one limitation/reject case, and one edge-case explanation when available."
    test: "manual/docs-review"
  - id: AC-2
    description: "Demo pack explains that open-source cases prove artifact quality, not paid-pilot demand or customer PMF."
    test: "manual/docs-review"
  - id: AC-3
    description: "Demo pack has a talk track, safe screenshots/excerpts, buyer promise, and next paid-pilot ask."
    test: "manual/docs-review"

Files:
  - docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md
  - docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md
  - demo/

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-24---multi-case-report-quality-loop

Notes: |
  Do not add public landing-page or SaaS scope.

## T109: Multi-Case Report Quality Deep Review

Owner:      codex
Phase:      24
Type:       review
Depends-On: T104, T105, T106, T107, T108

Objective: |
  Run the Phase 24 boundary review and decide whether the product is ready for
  private/operator-approved pilot reports.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks scorecard rigor, coverage gaps, report quality, regression tests, demo pack safety, and paid-pilot readiness."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, handoff docs, and phase report are updated with final Phase 24 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "If fewer than 3 packs are demo-quality, Phase 25 is blocked and the next action is another case-bank batch."
    test: "manual/review"

Files:
  - docs/archive/PHASE24_REVIEW.md
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

## T110: Private Pilot Intake And Redaction Checklist

Owner:      operator + codex
Phase:      25
Type:       docs
Depends-On: T109

Objective: |
  Prepare the local-only checklist for receiving 1-3 operator-approved
  private/anonymized trade exports without committing raw private data.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md` defines allowed files, forbidden data, redaction expectations, local storage rules, deletion trigger, and operator approval step."
    test: "manual/docs-review"
  - id: AC-2
    description: "Checklist explicitly forbids committing raw rows, account ids, credentials, Telegram handles, payment ids, private paths, and unapproved screenshots."
    test: "manual/docs-review"
  - id: AC-3
    description: "Checklist maps private input to existing intake/session/rule/audit/report commands."
    test: "manual/docs-review"

Files:
  - docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md
  - docs/PILOT_INTAKE_CONTRACT_RU.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-25---private-pilot-readiness

Notes: |
  This task prepares private handling; it does not require private data in git.

## T111: Private Pilot Report Review Checklist

Owner:      codex
Phase:      25
Type:       docs
Depends-On: T110

Objective: |
  Define the manual review checklist that must pass before any private pilot
  audit report is delivered to a warm user.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md` covers source-row traceability, policy mapping, calculation review, limitation wording, privacy review, and claim safety."
    test: "manual/docs-review"
  - id: AC-2
    description: "Checklist blocks delivery for unresolved P0/P1 report truth, privacy, or advice/performance-claim issues."
    test: "manual/docs-review"
  - id: AC-3
    description: "Checklist includes reviewer signoff fields and safe external-delivery status."
    test: "manual/docs-review"

Files:
  - docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md
  - docs/REPORT_QUALITY_SCORECARD.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-25---private-pilot-readiness

Notes: |
  Keep this checklist short enough to use during concierge delivery.

## T112: Local Private Pilot Artifact Run Notes

Owner:      operator + codex
Phase:      25
Type:       validation
Depends-On: T111

Objective: |
  Run 1-3 operator-approved private/anonymized audit packs outside git and
  record only safe metadata, review status, and delivery decision inside the
  repo.

Acceptance-Criteria:
  - id: AC-1
    description: "Each private run has a safe run note with non-sensitive label, date, data shape, rule shape, report status, review status, and delivery decision."
    test: "manual-evidence: safe run notes exist without private rows."
  - id: AC-2
    description: "No raw private rows, account ids, credentials, private paths, or customer identifiers are committed."
    test: "manual/git-review"
  - id: AC-3
    description: "At least one private run reaches manually reviewed report status, or blockers are explicitly recorded."
    test: "manual/docs-review"

Files:
  - docs/private_pilot_runs/
  - docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md

Notes: |
  Private artifact files remain outside git. Commit only safe summaries.

## T113: Paid Pilot Package And Feedback Log

Owner:      codex
Phase:      25
Type:       docs
Depends-On: T112

Objective: |
  Package the paid-pilot offer, delivery boundary, and feedback capture loop
  for warm prospects.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/PAID_PILOT_PACKAGE.md` states deliverables, turnaround, pricing hypothesis, required user input, exclusions, and no-advice/no-live-control boundary."
    test: "manual/docs-review"
  - id: AC-2
    description: "`docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md` captures usefulness, trust, clarity, objection, payment, repeat, and referral evidence without raw private data."
    test: "manual/docs-review"
  - id: AC-3
    description: "Package references open-source demo pack and private review checklist instead of claiming production readiness."
    test: "manual/docs-review"

Files:
  - docs/PAID_PILOT_PACKAGE.md
  - docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md
  - docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-25---private-pilot-readiness

Notes: |
  No checkout or payment processor is in scope.

## T114: Paid Pilot Ready Gate

Owner:      operator + codex
Phase:      25
Type:       review
Depends-On: T113

Objective: |
  Decide whether Trader Risk Audit is ready to show to warm prospects as a
  paid concierge research/audit product.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/PAID_PILOT_READY_GATE.md` records ready / needs fixes / reject with evidence from open-source packs, private run notes, report review, and feedback package."
    test: "manual/docs-review"
  - id: AC-2
    description: "Gate states exact first-user ask, delivery promise, exclusions, and evidence still missing."
    test: "manual/docs-review"
  - id: AC-3
    description: "Gate does not approve SaaS, checkout, live exchange control, order blocking, or trading advice."
    test: "manual/docs-review"

Files:
  - docs/PAID_PILOT_READY_GATE.md
  - docs/PAID_PILOT_PACKAGE.md
  - docs/private_pilot_runs/

Context-Refs:
  - docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md#phase-25---private-pilot-readiness

Notes: |
  Human/operator decision is required.

## T115: Private Pilot Readiness Deep Review

Owner:      codex
Phase:      25
Type:       review
Depends-On: T110, T111, T112, T113, T114

Objective: |
  Run the Phase 25 boundary review and close the pre-prospect readiness loop.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks private data safety, report validity, paid-pilot package clarity, feedback loop, and scope boundaries."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, handoff docs, and phase report are updated with final Phase 25 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "If ready, next task is warm-prospect delivery/feedback; if not ready, next task is the specific blocking fix, not SaaS expansion."
    test: "manual/review"

Files:
  - docs/archive/PHASE25_REVIEW.md
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.
