# Task Graph — Entropy Protocol

Version: 1.0
Date: 2026-05-01

Status legend:
- `[ ]` Not started
- `[~]` Implemented, pending review
- `[x]` Complete
- `[!]` Blocked

---

## Phase 1 — Foundation

### [x] T01: Project Skeleton

Owner:      codex
Phase:      1
Type:       none
Depends-On: none

Objective: |
  Create the complete project skeleton for Entropy Protocol: pyproject.toml with all
  declared dependencies and dev extras, the full entropy/ package directory structure
  with __init__.py files at each level, a typer/rich CLI entry point registered as a
  console script, and a .gitignore covering Python artifacts, .env files, Parquet data
  directories, and pytest cache.

Acceptance-Criteria:
  - id: AC-1
    description: "Running `python -m entropy --help` from the project root exits 0 and prints the CLI help text without ImportError or ModuleNotFoundError."
    test: "tests/smoke/test_smoke.py::test_cli_help_exits_zero"
  - id: AC-2
    description: "All entropy/ subpackages (models, db, registry, hashing, data, simbroker, walkforward, attribution, governance, stats, evidence) are importable without error after `uv pip install -e .`."
    test: "tests/smoke/test_smoke.py::test_all_subpackages_importable"
  - id: AC-3
    description: "pyproject.toml declares all required dependencies: pydantic>=2.0, polars, pyarrow, duckdb, sqlalchemy>=2.0, alembic, typer, rich, structlog, opentelemetry-api, pytest, ruff, pyright as dev dependencies."
    test: "tests/smoke/test_smoke.py::test_pyproject_declares_required_deps"
  - id: AC-4
    description: ".gitignore contains entries for __pycache__/, *.pyc, .env, data/market/, .pytest_cache/, dist/, and .venv/."
    test: "tests/smoke/test_smoke.py::test_gitignore_has_required_entries"

Files:
  - pyproject.toml
  - entropy/__init__.py
  - entropy/cli.py
  - entropy/tracing.py
  - entropy/metrics.py
  - entropy/models/__init__.py
  - entropy/db/__init__.py
  - entropy/registry/__init__.py
  - entropy/hashing/__init__.py
  - entropy/data/__init__.py
  - entropy/simbroker/__init__.py
  - entropy/walkforward/__init__.py
  - entropy/attribution/__init__.py
  - entropy/governance/__init__.py
  - entropy/stats/__init__.py
  - entropy/evidence/__init__.py
  - .gitignore
  - tests/__init__.py
  - tests/smoke/__init__.py
  - tests/smoke/test_smoke.py

Context-Refs:
  - docs/ARCHITECTURE.md §File Layout
  - docs/ARCHITECTURE.md §Tech Stack

---

## [x] T02: CI Setup

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01

Objective: |
  Configure GitHub Actions CI for Entropy Protocol with a PostgreSQL 16 service container,
  ruff linting, ruff format check, pyright type checking, and pytest execution. The CI
  workflow must set all required environment variables and run against Python 3.12.

Acceptance-Criteria:
  - id: AC-1
    description: ".github/workflows/ci.yml exists and declares a PostgreSQL 16 service with POSTGRES_DB=entropy_test, POSTGRES_USER=entropy, POSTGRES_PASSWORD=entropy_test on port 5432."
    test: "tests/smoke/test_smoke.py::test_ci_yml_declares_postgres_service"
  - id: AC-2
    description: ".github/workflows/ci.yml declares all four required env vars: DATABASE_URL, ENTROPY_DATA_DIR, ENTROPY_REGISTRY_DIR, LOG_LEVEL."
    test: "tests/smoke/test_smoke.py::test_ci_yml_declares_required_env_vars"
  - id: AC-3
    description: ".github/workflows/ci.yml includes steps for: ruff check, ruff format --check, pyright, and pytest in that order."
    test: "tests/smoke/test_smoke.py::test_ci_yml_includes_all_required_steps"
  - id: AC-4
    description: ".github/workflows/ci.yml triggers on push to main and master branches and on pull_request events."
    test: "tests/smoke/test_smoke.py::test_ci_yml_triggers_on_push_and_pr"

Files:
  - .github/workflows/ci.yml

Context-Refs:
  - docs/ARCHITECTURE.md §Runtime Contract

---

## [x] T03: Smoke Tests

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01, T02

Objective: |
  Write smoke tests that verify: the project skeleton imports cleanly with no errors,
  a PostgreSQL connection fixture connects successfully to the test database, and a
  DuckDB embedded query returns a correct result. These tests serve as the initial
  baseline for all subsequent CI runs.

Acceptance-Criteria:
  - id: AC-1
    description: "The conftest.py PostgreSQL fixture establishes a connection to DATABASE_URL and executes `SELECT 1` without raising; the fixture tears down cleanly after each test."
    test: "tests/smoke/test_smoke.py::test_postgres_connection_fixture"
  - id: AC-2
    description: "A DuckDB embedded query `SELECT 42 AS answer` returns a result with answer=42 without requiring any external service."
    test: "tests/smoke/test_smoke.py::test_duckdb_embedded_query"
  - id: AC-3
    description: "Importing `from entropy import cli` and `from entropy.models import market, registry, performance` in a single test module raises no ImportError."
    test: "tests/smoke/test_smoke.py::test_all_subpackages_importable"

Files:
  - tests/conftest.py
  - tests/smoke/test_smoke.py

Context-Refs:
  - docs/ARCHITECTURE.md §Runtime Contract

---

## Phase 2 — Core Domain Models

### T04: Market Data Models

Owner:      codex
Phase:      2
Type:       none
Depends-On: T01

Objective: |
  Implement Pydantic v2 domain models for market data in entropy/models/market.py:
  OHLCVBar (open, high, low, close, volume, timestamp in UTC), Dataset (list of bars
  with provenance), DatasetKey (symbol + timeframe + date range), and Timeframe enum
  (M1, M5, M15, M30, H1, H4, D1, W1).

Acceptance-Criteria:
  - id: AC-1
    description: "OHLCVBar raises ValidationError when close <= 0, volume < 0, high < max(open, close), or low > min(open, close)."
    test: "tests/unit/test_models.py::test_ohlcv_bar_validates_price_sanity"
  - id: AC-2
    description: "OHLCVBar raises ValidationError when timestamp is not timezone-aware UTC (naive datetime or non-UTC timezone)."
    test: "tests/unit/test_models.py::test_ohlcv_bar_requires_utc_timestamp"
  - id: AC-3
    description: "Dataset constructed with a valid list of OHLCVBars is accepted; Dataset constructed with an empty list raises ValidationError."
    test: "tests/unit/test_models.py::test_dataset_requires_nonempty_bars"
  - id: AC-4
    description: "DatasetKey with a valid symbol, Timeframe, start, and end is accepted; DatasetKey with end <= start raises ValidationError."
    test: "tests/unit/test_models.py::test_dataset_key_validates_date_range"
  - id: AC-5
    description: "Timeframe enum contains exactly: M1, M5, M15, M30, H1, H4, D1, W1 and each has a string value."
    test: "tests/unit/test_models.py::test_timeframe_enum_members"

Files:
  - entropy/models/market.py
  - tests/unit/test_models.py

Context-Refs:
  - docs/spec.md §Data Pipeline

---

## T05: Registry and Run Models

Owner:      codex
Phase:      2
Type:       none
Depends-On: T01

Objective: |
  Implement Pydantic v2 domain models for the trial registry and run records in
  entropy/models/registry.py: TrialSpec (required fields: trial_id, family_tag,
  hypothesis, dataset_hash, code_hash, policy_hash, parameter_lock, registered_at),
  RegistryEntry (TrialSpec + status), RunRecord (trial_id, run_id, dataset_hash,
  code_hash, policy_hash, simbroker_version, IS/OOS windows, leakage_status),
  FillLog (per-fill cost breakdown), GovernanceEvent (event_type, timestamp,
  trial_id, actor, reason, policy_hash).

Acceptance-Criteria:
  - id: AC-1
    description: "TrialSpec raises ValidationError when any of trial_id, family_tag, hypothesis, dataset_hash, code_hash, or policy_hash is absent or empty string."
    test: "tests/unit/test_models.py::test_trial_spec_requires_all_hash_fields"
  - id: AC-2
    description: "TrialSpec raises ValidationError when family_tag is not assigned (None or empty)."
    test: "tests/unit/test_models.py::test_trial_spec_requires_family_tag"
  - id: AC-3
    description: "RunRecord raises ValidationError when simbroker_version is absent."
    test: "tests/unit/test_models.py::test_run_record_requires_simbroker_version"
  - id: AC-4
    description: "FillLog contains fields: timestamp, symbol, side, quantity, fill_price, commission, slippage, market_impact, borrow_rate, funding_rate, total_cost; all cost fields are non-negative Decimal or float."
    test: "tests/unit/test_models.py::test_fill_log_cost_fields_nonnegative"
  - id: AC-5
    description: "GovernanceEvent raises ValidationError when event_type is not one of the declared enum values (APPROVAL, REJECTION, PHASE_GATE, P1_TRIP, P1_RESET, P3_FIRE, P3_CLEAR)."
    test: "tests/unit/test_models.py::test_governance_event_validates_event_type"

Files:
  - entropy/models/registry.py
  - tests/unit/test_models.py

Context-Refs:
  - docs/spec.md §Trial Registry
  - docs/ARCHITECTURE.md §Human Approval Boundaries

---

## T06: Performance Models

Owner:      codex
Phase:      2
Type:       none
Depends-On: T04, T05

Objective: |
  Implement Pydantic v2 domain models for performance data in entropy/models/performance.py:
  PnLStreams (streams a, b, c, d as separate fields; net_sharpe_streams property returns
  only a+b+c), NetSharpe (value, confidence_interval_68, method_id="CI-SR-ACF-v1",
  sample_length, M_total), DrawdownRecord (start_ts, end_ts, peak_value, trough_value,
  drawdown_pct, recovery_ts), PerformanceMetrics (net_sharpe, max_drawdown, calmar_ratio,
  n_eff, harvey_liu_deflated_sharpe with stub fields).

Acceptance-Criteria:
  - id: AC-1
    description: "PnLStreams.net_sharpe_streams returns the sum of streams a, b, and c; stream d is excluded; accessing net_sharpe_streams never includes stream d values."
    test: "tests/unit/test_models.py::test_pnl_streams_net_sharpe_excludes_stream_d"
  - id: AC-2
    description: "NetSharpe raises ValidationError when method_id is not 'CI-SR-ACF-v1'."
    test: "tests/unit/test_models.py::test_net_sharpe_requires_canonical_method_id"
  - id: AC-3
    description: "DrawdownRecord raises ValidationError when drawdown_pct is not in the range [0.0, 1.0] or when trough_value > peak_value."
    test: "tests/unit/test_models.py::test_drawdown_record_validates_values"
  - id: AC-4
    description: "PerformanceMetrics allows None for harvey_liu_deflated_sharpe and n_eff with a reason_code field explaining the stub status."
    test: "tests/unit/test_models.py::test_performance_metrics_allows_stub_fields"

Files:
  - entropy/models/performance.py
  - tests/unit/test_models.py

Context-Refs:
  - docs/spec.md §P&L Attribution
  - docs/core/PROTOCOL_SPEC.md §NN-2

---

## Phase 3 — Database Schema + Hashing

### T07: Database Schema + Alembic Migrations

Owner:      codex
Phase:      3
Type:       none
Depends-On: T05

Objective: |
  Create SQLAlchemy 2.x table models and Alembic migrations for all four core tables:
  trial_registry, runs, fill_logs, and governance_events. All tables must have
  created_at timestamps. trial_registry and governance_events must have no UPDATE
  or DELETE triggers or permissions in migration scripts. Alembic must apply cleanly
  to a fresh PostgreSQL 16 database.

Acceptance-Criteria:
  - id: AC-1
    description: "Running `alembic upgrade head` against a fresh entropy_test database exits 0 and creates all four tables: trial_registry, runs, fill_logs, governance_events."
    test: "tests/integration/test_registry_db.py::test_alembic_upgrade_creates_all_tables"
  - id: AC-2
    description: "The trial_registry table has columns: trial_id (primary key), family_tag, hypothesis, dataset_hash, code_hash, policy_hash, status, parameter_lock (JSONB), registered_at, created_at."
    test: "tests/integration/test_registry_db.py::test_trial_registry_schema"
  - id: AC-3
    description: "The runs table has columns: run_id (primary key), trial_id (FK to trial_registry), dataset_hash, code_hash, policy_hash, simbroker_version, is_start, is_end, oos_start, oos_end, embargo_bars, leakage_status, created_at."
    test: "tests/integration/test_registry_db.py::test_runs_table_schema"
  - id: AC-4
    description: "The governance_events table has columns: event_id (primary key), trial_id, event_type, actor, reason, policy_hash, prior_state, next_state, created_at."
    test: "tests/integration/test_registry_db.py::test_governance_events_schema"
  - id: AC-5
    description: "Running `alembic downgrade -1` after `upgrade head` exits 0 and removes the tables created in the latest migration."
    test: "tests/integration/test_registry_db.py::test_alembic_downgrade_reverts_migration"

Files:
  - entropy/db/models.py
  - entropy/db/session.py
  - migrations/env.py
  - migrations/alembic.ini
  - migrations/versions/0001_initial_schema.py
  - tests/integration/test_registry_db.py

Context-Refs:
  - docs/ARCHITECTURE.md §Component Table
  - docs/IMPLEMENTATION_CONTRACT.md §Registry Append-Only

---

## T08: Deterministic Hashing

Owner:      codex
Phase:      3
Type:       none
Depends-On: T04

Objective: |
  Implement deterministic SHA-256 hashing in entropy/hashing/hashing.py:
  dataset hash (SHA-256 of sorted Parquet rows + schema fingerprint, row-order
  independent), run hash (dataset_hash + code_hash + policy_hash combined),
  policy hash (SHA-256 of serialized policy config). All hash functions must be
  idempotent and tested with worked examples.

Acceptance-Criteria:
  - id: AC-1
    description: "SHA-256 hash of the same Parquet dataset is identical across two invocations with identical rows supplied in different row order (sorted before hashing)."
    test: "tests/unit/test_hashing.py::test_dataset_hash_is_row_order_independent"
  - id: AC-2
    description: "SHA-256 hash of a dataset with one row changed is different from the hash of the original dataset."
    test: "tests/unit/test_hashing.py::test_dataset_hash_detects_row_change"
  - id: AC-3
    description: "SHA-256 hash of a dataset with the same rows but a different schema (column added) is different from the original hash."
    test: "tests/unit/test_hashing.py::test_dataset_hash_detects_schema_change"
  - id: AC-4
    description: "The run hash computed from (dataset_hash='aaa', code_hash='bbb', policy_hash='ccc') is identical across two invocations with identical inputs."
    test: "tests/unit/test_hashing.py::test_run_hash_is_deterministic"
  - id: AC-5
    description: "The policy hash of a serialized policy dict is identical across two invocations regardless of dict key insertion order."
    test: "tests/unit/test_hashing.py::test_policy_hash_is_key_order_independent"

Files:
  - entropy/hashing/hashing.py
  - tests/unit/test_hashing.py

Context-Refs:
  - docs/DECISION_LOG.md §D-008
  - docs/IMPLEMENTATION_CONTRACT.md §Hash Determinism

---

## Phase 4 — Trial Registry

### T09: Trial Registry Write Path

Owner:      codex
Phase:      4
Type:       none
Depends-On: T07, T08, T05

Objective: |
  Implement the Trial Registry preregistration write path in entropy/registry/write.py:
  validate TrialSpec for completeness, assign family tag, lock parameters, verify all
  three hashes are present, check for duplicate trial_id, perform INSERT-only DB write,
  and return TrialID. Raise structured errors for each validation failure.

Acceptance-Criteria:
  - id: AC-1
    description: "Submitting a valid TrialSpec with all required fields and all hashes inserts exactly one row into trial_registry and returns the trial_id string."
    test: "tests/integration/test_registry_db.py::test_write_valid_trial_spec_inserts_row"
  - id: AC-2
    description: "Submitting a TrialSpec with dataset_hash=None raises MissingHashError before any DB write; the trial_registry table has zero rows after the call."
    test: "tests/integration/test_registry_db.py::test_write_rejects_missing_dataset_hash"
  - id: AC-3
    description: "Submitting a TrialSpec with a trial_id that already exists in trial_registry raises DuplicateTrialError; the table row count does not increase."
    test: "tests/integration/test_registry_db.py::test_write_rejects_duplicate_trial_id"
  - id: AC-4
    description: "The write path uses SQLAlchemy parameterized INSERT (no f-string or string concat in execute calls); verified by code inspection test that checks for absence of f-strings in write.py."
    test: "tests/unit/test_registry.py::test_write_path_uses_parameterized_sql"
  - id: AC-5
    description: "The write path does not issue any UPDATE or DELETE statement; a mock DB session that raises on UPDATE/DELETE must not raise during a normal write call."
    test: "tests/unit/test_registry.py::test_write_path_issues_no_update_or_delete"

Files:
  - entropy/registry/write.py
  - tests/unit/test_registry.py
  - tests/integration/test_registry_db.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md §Registry Append-Only
  - docs/IMPLEMENTATION_CONTRACT.md §SQL Safety

---

## T10: Experiment Readiness Gate

Owner:      codex
Phase:      4
Type:       none
Depends-On: T09

Objective: |
  Implement the Experiment Readiness Gate in entropy/registry/gate.py: check spec
  completeness (all required fields present and non-empty), family tag assigned,
  all three hashes present, no duplicate trial_id in the registry. Return ReadinessResult
  with status READY or a structured list of named failures. This is a pure read + validate
  operation with no DB writes.

Acceptance-Criteria:
  - id: AC-1
    description: "gate.check(trial_id) returns ReadinessResult(status=READY) when the registered trial has all required fields, family_tag assigned, all three hashes, and no duplicate trial_id."
    test: "tests/unit/test_registry.py::test_gate_returns_ready_for_complete_trial"
  - id: AC-2
    description: "gate.check(trial_id) returns ReadinessResult(status=NOT_READY, failures=['missing_dataset_hash']) when dataset_hash is absent."
    test: "tests/unit/test_registry.py::test_gate_lists_missing_dataset_hash"
  - id: AC-3
    description: "gate.check(trial_id) returns ReadinessResult(status=NOT_READY, failures=['missing_family_tag']) when family_tag is None or empty."
    test: "tests/unit/test_registry.py::test_gate_lists_missing_family_tag"
  - id: AC-4
    description: "gate.check(trial_id) returns ReadinessResult(status=NOT_READY, failures=['duplicate_trial_id']) when another trial with the same family and overlapping parameters exists."
    test: "tests/unit/test_registry.py::test_gate_detects_duplicate_trial_id"
  - id: AC-5
    description: "gate.check(trial_id) called on a trial_id that does not exist in the registry raises TrialNotFoundError."
    test: "tests/unit/test_registry.py::test_gate_raises_for_unknown_trial_id"

Files:
  - entropy/registry/gate.py
  - tests/unit/test_registry.py

Context-Refs:
  - docs/spec.md §Trial Registry
  - docs/IMPLEMENTATION_CONTRACT.md §Registry Append-Only

---

## T11: Trial Registry Read Path

Owner:      codex
Phase:      4
Type:       none
Depends-On: T09

Objective: |
  Implement the Trial Registry read path in entropy/registry/read.py: query by trial_id
  (returns RegistryEntry or raises TrialNotFoundError), query by family tag (returns list
  of RegistryEntry), query by status (PENDING/READY), and trial-count-per-family
  accounting. All operations are read-only; no writes occur.

Acceptance-Criteria:
  - id: AC-1
    description: "get_by_trial_id(trial_id) returns the RegistryEntry for a trial that exists; raises TrialNotFoundError for a trial_id not in the registry."
    test: "tests/unit/test_registry.py::test_read_by_trial_id_found_and_not_found"
  - id: AC-2
    description: "get_by_family(family_tag) returns a list of all RegistryEntry records with that family_tag; returns an empty list for a family_tag with no registered trials."
    test: "tests/unit/test_registry.py::test_read_by_family_returns_correct_list"
  - id: AC-3
    description: "get_by_status('PENDING') returns only trials with status PENDING; get_by_status('READY') returns only trials with status READY."
    test: "tests/unit/test_registry.py::test_read_by_status_filters_correctly"
  - id: AC-4
    description: "count_trials_in_family(family_tag) returns the integer count of all trials in the family, including both PENDING and READY entries."
    test: "tests/unit/test_registry.py::test_count_trials_in_family_includes_all_statuses"
  - id: AC-5
    description: "No write operation (INSERT/UPDATE/DELETE) is issued in any read path function; verified by mock session that raises on any write attempt."
    test: "tests/unit/test_registry.py::test_read_path_issues_no_writes"

Files:
  - entropy/registry/read.py
  - tests/unit/test_registry.py

Context-Refs:
  - docs/spec.md §Trial Registry

---

## Phase 5 — Data Pipeline

### T12: Data Ingestion Interface

Owner:      codex
Phase:      5
Type:       none
Depends-On: T04

Objective: |
  Implement the abstract DataProvider base class in entropy/data/provider.py with abstract
  methods fetch_ohlcv(symbol, timeframe, start, end) -> list[OHLCVBar], list_symbols() ->
  list[str], check_health() -> HealthStatus. Implement the DataIngestionError hierarchy:
  DataIngestionError (base), DataProviderError, DataQualityError, TimestampNormalizationError,
  GapDetectionError, OHLCVSanityError, ProviderNotFoundError. Implement the provider
  registry (name -> DataProvider class mapping).

Acceptance-Criteria:
  - id: AC-1
    description: "Attempting to instantiate DataProvider directly raises TypeError because it is an abstract class."
    test: "tests/unit/test_data_quality.py::test_data_provider_is_abstract"
  - id: AC-2
    description: "A concrete subclass that implements all three abstract methods (fetch_ohlcv, list_symbols, check_health) instantiates successfully."
    test: "tests/unit/test_data_quality.py::test_concrete_provider_instantiates"
  - id: AC-3
    description: "A concrete subclass that omits check_health raises TypeError on instantiation with a message identifying the missing method."
    test: "tests/unit/test_data_quality.py::test_provider_missing_method_raises_type_error"
  - id: AC-4
    description: "provider_registry.get('fixture') returns the LocalFixtureAdapter class after it is registered; provider_registry.get('unknown') raises ProviderNotFoundError."
    test: "tests/unit/test_data_quality.py::test_provider_registry_get_and_not_found"
  - id: AC-5
    description: "All six error classes (DataIngestionError, DataProviderError, DataQualityError, TimestampNormalizationError, GapDetectionError, OHLCVSanityError) are importable from entropy.data and form a correct inheritance hierarchy."
    test: "tests/unit/test_data_quality.py::test_error_hierarchy_inheritance"

Files:
  - entropy/data/provider.py
  - tests/unit/test_data_quality.py

Context-Refs:
  - docs/spec.md §Data Pipeline
  - docs/ARCHITECTURE.md §External Integrations

---

## T13: Local Fixture Adapter + Parquet Store

Owner:      codex
Phase:      5
Type:       none
Depends-On: T12, T08, T07

Objective: |
  Implement the LocalFixtureAdapter in entropy/data/fixture_adapter.py: reads OHLCV data
  from local CSV or Parquet fixture files, validates the data against the OHLCVBar schema,
  writes versioned Parquet to ENTROPY_DATA_DIR/market/{symbol}/{timeframe}/{hash}.parquet,
  computes the dataset hash, and records the hash + provenance in the DB in a single
  transaction.

Acceptance-Criteria:
  - id: AC-1
    description: "LocalFixtureAdapter.fetch_ohlcv() called with a valid fixture CSV path returns a list of OHLCVBar objects with UTC timestamps and correct OHLCV values."
    test: "tests/unit/test_data_quality.py::test_fixture_adapter_parses_csv"
  - id: AC-2
    description: "After fetch_ohlcv() completes, a Parquet file exists at ENTROPY_DATA_DIR/market/{symbol}/{timeframe}/{hash}.parquet and is readable by polars.read_parquet()."
    test: "tests/integration/test_registry_db.py::test_fixture_adapter_writes_parquet"
  - id: AC-3
    description: "The dataset hash recorded in the DB after ingestion matches the hash computed directly from the written Parquet file using the deterministic hashing function."
    test: "tests/integration/test_registry_db.py::test_fixture_adapter_records_correct_hash"
  - id: AC-4
    description: "If the DB write for the provenance record fails (simulated by raising IntegrityError), the Parquet file is not left on disk (transaction rollback removes both)."
    test: "tests/unit/test_data_quality.py::test_fixture_adapter_rolls_back_on_db_failure"
  - id: AC-5
    description: "LocalFixtureAdapter.check_health() returns HealthStatus(ok=True) when the fixture directory exists and is readable; returns HealthStatus(ok=False, reason='directory_missing') otherwise."
    test: "tests/unit/test_data_quality.py::test_fixture_adapter_health_check"

Files:
  - entropy/data/fixture_adapter.py
  - tests/unit/test_data_quality.py
  - tests/integration/test_registry_db.py

Context-Refs:
  - docs/spec.md §Data Pipeline
  - docs/IMPLEMENTATION_CONTRACT.md §Hash Determinism

---

## T14: Data Quality Checks

Owner:      codex
Phase:      5
Type:       none
Depends-On: T04, T12

Objective: |
  Implement data quality validation in entropy/data/quality.py: UTC timestamp enforcement
  (raise TimestampNormalizationError for non-UTC bars), configurable gap detection (raise
  GapDetectionError when consecutive bar gap exceeds max_gap_seconds), and OHLCV sanity
  checks (positive prices, volume >= 0, high >= max(open,close), low <= min(open,close)).
  Return a DataQualityReport with per-check verdicts and affected bar counts.

Acceptance-Criteria:
  - id: AC-1
    description: "validate_timestamps() raises TimestampNormalizationError when any bar has a naive datetime timestamp (no tzinfo)."
    test: "tests/unit/test_data_quality.py::test_validate_timestamps_raises_for_naive_datetime"
  - id: AC-2
    description: "validate_timestamps() raises TimestampNormalizationError when any bar has a non-UTC timezone (e.g., America/New_York)."
    test: "tests/unit/test_data_quality.py::test_validate_timestamps_raises_for_non_utc_timezone"
  - id: AC-3
    description: "detect_gaps() raises GapDetectionError when the time difference between two consecutive bars exceeds max_gap_seconds; the error message names the exact timestamps of the gap."
    test: "tests/unit/test_data_quality.py::test_detect_gaps_raises_at_threshold"
  - id: AC-4
    description: "check_ohlcv_sanity() raises OHLCVSanityError when close <= 0; the error identifies which bar index failed."
    test: "tests/unit/test_data_quality.py::test_sanity_check_raises_for_zero_close"
  - id: AC-5
    description: "check_ohlcv_sanity() raises OHLCVSanityError when high < close (close higher than declared high)."
    test: "tests/unit/test_data_quality.py::test_sanity_check_raises_for_high_below_close"
  - id: AC-6
    description: "run_all_checks() returns a DataQualityReport with status='PASS' when all bars pass; with status='FAIL' and per_check_results listing each failed check and affected bar count when any check fails."
    test: "tests/unit/test_data_quality.py::test_run_all_checks_returns_report"

Files:
  - entropy/data/quality.py
  - tests/unit/test_data_quality.py

Context-Refs:
  - docs/spec.md §Data Pipeline

---

## Phase 6 — SimBroker

### T15: SimBroker Cost Model

Owner:      codex
Phase:      6
Type:       none
Depends-On: T05

Objective: |
  Implement the deterministic SimBroker cost model in entropy/simbroker/costs.py:
  total fill cost = fixed commission + percentage commission + linear slippage +
  square-root market impact + borrow rate charge + funding rate charge. All parameters
  are configurable. All formulas are tested against worked examples with known inputs
  and expected outputs.

Acceptance-Criteria:
  - id: AC-1
    description: "compute_cost(fill_price=100.0, quantity=10, fixed_commission=1.0, pct_commission=0.0008, slippage_linear=0.0002, sqrt_impact_coef=0.0002, borrow_rate=0.0, funding_rate=0.0) returns total_cost matching the sum of each component within 1e-6 tolerance."
    test: "tests/unit/test_simbroker.py::test_cost_model_worked_example"
  - id: AC-2
    description: "compute_cost called twice with identical parameters returns identical float values (determinism)."
    test: "tests/unit/test_simbroker.py::test_cost_model_is_deterministic"
  - id: AC-3
    description: "compute_cost with borrow_rate=0.015/365 (daily equity borrow) and funding_rate=0.0 returns a total_cost with borrow component equal to fill_price * quantity * (0.015/365) within 1e-10 tolerance."
    test: "tests/unit/test_simbroker.py::test_cost_model_borrow_component"
  - id: AC-4
    description: "compute_cost with all cost parameters set to zero returns total_cost=0.0 exactly."
    test: "tests/unit/test_simbroker.py::test_cost_model_zero_costs"
  - id: AC-5
    description: "CostModelConfig is a Pydantic v2 model with all cost parameters; instantiation with a negative pct_commission raises ValidationError."
    test: "tests/unit/test_simbroker.py::test_cost_model_config_validates_nonnegative"

Files:
  - entropy/simbroker/costs.py
  - tests/unit/test_simbroker.py

Context-Refs:
  - docs/spec.md §SimBroker
  - docs/core/PROTOCOL_SPEC.md §Cost Model Components

---

## T16: SimBroker Fill Engine

Owner:      codex
Phase:      6
Type:       none
Depends-On: T15, T05

Execution-Mode: heavy
Evidence:
  - "tests/unit/test_simbroker.py::test_fill_engine_determinism — two invocations with same inputs produce byte-identical FillLog"
  - "tests/unit/test_simbroker.py::test_fill_engine_no_lookahead — fill price references only current bar data"
  - "tests/unit/test_simbroker.py::test_fill_constrained_to_bar_range — fill outside [low, high] is constrained"
Verifier-Focus: |
  Confirm that: (1) no bar future data is accessed (fill uses only current bar OHLCV),
  (2) fill price constraint to [low, high] is enforced by code path, not just tested,
  (3) FillLog contains all required cost breakdown fields, (4) determinism holds across
  two independent invocations with identical inputs.

Objective: |
  Implement the SimBroker fill engine in entropy/simbroker/fills.py: accept a strategy
  signal, an OHLCVBar, and a CostModelConfig, produce a FillLog entry with complete
  cost breakdown. Fills must be constrained to the bar's [low, high] range. No lookahead
  is used (only current bar data). Deterministic given same inputs.

Acceptance-Criteria:
  - id: AC-1
    description: "process_fill(signal=BUY, bar=OHLCVBar(open=100, high=105, low=99, close=103, ...), proposed_price=110) constrains fill to high=105 and sets FillLog.constrained=True."
    test: "tests/unit/test_simbroker.py::test_fill_constrained_to_bar_high"
  - id: AC-2
    description: "process_fill(signal=SELL, bar=OHLCVBar(open=100, high=105, low=99, close=103, ...), proposed_price=95) constrains fill to low=99 and sets FillLog.constrained=True."
    test: "tests/unit/test_simbroker.py::test_fill_constrained_to_bar_low"
  - id: AC-3
    description: "process_fill with proposed_price=102 (within bar range) produces FillLog.constrained=False and fill_price=102."
    test: "tests/unit/test_simbroker.py::test_fill_unconstrained_within_bar"
  - id: AC-4
    description: "Two calls to process_fill with identical signal, bar, and CostModelConfig produce FillLog entries with identical values in every field."
    test: "tests/unit/test_simbroker.py::test_fill_engine_determinism"
  - id: AC-5
    description: "FillLog produced by process_fill contains all required fields: timestamp, symbol, side, quantity, fill_price, commission, slippage, market_impact, borrow_rate, funding_rate, total_cost, constrained."
    test: "tests/unit/test_simbroker.py::test_fill_log_has_all_required_fields"
  - id: AC-6
    description: "process_fill does not access any OHLCV bar data beyond the single bar passed as argument (no lookahead); verified by passing a mock bar that raises AttributeError on next_bar access."
    test: "tests/unit/test_simbroker.py::test_fill_engine_no_lookahead"

Files:
  - entropy/simbroker/fills.py
  - tests/unit/test_simbroker.py

Context-Refs:
  - docs/spec.md §SimBroker
  - docs/EVIDENCE_INDEX.md §Heavy Task Evidence

---

## T17: SimBroker Calibration Interface

Owner:      codex
Phase:      6
Type:       none
Depends-On: T15

Execution-Mode: heavy
Evidence:
  - "tests/unit/test_simbroker.py::test_bid_ask_provider_abstract — abstract method enforcement"
  - "tests/unit/test_simbroker.py::test_noop_bid_ask_provider_passes — no-op mock passes all calls"
Verifier-Focus: |
  Confirm that: (1) BidAskProvider is abstract with get_bid_ask as abstract method,
  (2) NoOpBidAskProvider returns None without raising, (3) the interface is documented
  as a placeholder for Phase 1+ broker calibration work.

Objective: |
  Implement the BidAskProvider abstract interface and no-op mock in
  entropy/simbroker/calibration.py as a placeholder for future broker-data calibration.
  The abstract base class defines get_bid_ask(symbol, timestamp). The no-op mock returns
  None for all calls. All tests pass with the no-op mock. The interface is documented as
  a stub pending Phase 1+ calibration work.

Acceptance-Criteria:
  - id: AC-1
    description: "Attempting to instantiate BidAskProvider directly raises TypeError because get_bid_ask is abstract."
    test: "tests/unit/test_simbroker.py::test_bid_ask_provider_is_abstract"
  - id: AC-2
    description: "NoOpBidAskProvider().get_bid_ask(symbol='BTCUSDT', timestamp=any_utc_datetime) returns None without raising any exception."
    test: "tests/unit/test_simbroker.py::test_noop_bid_ask_provider_returns_none"
  - id: AC-3
    description: "NoOpBidAskProvider is a valid BidAskProvider subclass: isinstance(NoOpBidAskProvider(), BidAskProvider) returns True."
    test: "tests/unit/test_simbroker.py::test_noop_is_valid_subclass"

Files:
  - entropy/simbroker/calibration.py
  - tests/unit/test_simbroker.py

Context-Refs:
  - docs/spec.md §SimBroker
  - docs/EVIDENCE_INDEX.md §Statistical Formula Stubs

---

## Phase 7 — Walk-Forward Harness

### T18: IS/OOS Splitter

Owner:      codex
Phase:      7
Type:       none
Depends-On: T04

Execution-Mode: heavy
Evidence:
  - "tests/integration/test_walk_forward.py::test_no_future_leakage — OOS bars never appear in IS window"
  - "tests/integration/test_walk_forward.py::test_embargo_excludes_correct_bars — exactly N bars excluded"
Verifier-Focus: |
  Confirm that: (1) the IS window contains no bar with timestamp >= (oos_start - embargo),
  (2) the embargo band excludes exactly the configured number of bars,
  (3) LeakageError is raised when a feature is computed on data beyond the IS cutoff,
  (4) the splitter's formula assumption for the embargo is documented in code comments.

Objective: |
  Implement strict time-based IS/OOS splitting in entropy/walkforward/splitter.py with
  configurable embargo band (purge N bars before OOS start). Validate that no future
  data leaks into the IS window. The embargo formula assumption must be documented
  in code comments pending resolution of the open blocker (purge/embargo formula
  is not independently verified). A leakage validation test is required.

Acceptance-Criteria:
  - id: AC-1
    description: "split(bars, oos_start, embargo_bars=5) returns IS window where the last bar timestamp is strictly before (oos_start - 5 * bar_duration); no IS bar has timestamp >= (oos_start - embargo)."
    test: "tests/integration/test_walk_forward.py::test_splitter_is_window_ends_before_embargo"
  - id: AC-2
    description: "split(bars, oos_start, embargo_bars=5) returns OOS window starting at oos_start; no OOS bar timestamp is before oos_start."
    test: "tests/integration/test_walk_forward.py::test_splitter_oos_window_starts_at_cutoff"
  - id: AC-3
    description: "split() raises LeakageError when any element of the IS window has a feature value that was computed using data after the IS cutoff timestamp."
    test: "tests/integration/test_walk_forward.py::test_no_future_leakage"
  - id: AC-4
    description: "split() with embargo_bars=0 returns IS window ending at the last bar before oos_start with no gap; OOS starts at oos_start."
    test: "tests/integration/test_walk_forward.py::test_splitter_zero_embargo"
  - id: AC-5
    description: "split() with oos_start equal to the first bar timestamp raises ValueError because the IS window would be empty."
    test: "tests/integration/test_walk_forward.py::test_splitter_raises_for_empty_is_window"

Files:
  - entropy/walkforward/splitter.py
  - tests/integration/test_walk_forward.py

Context-Refs:
  - docs/EVIDENCE_INDEX.md §Statistical Formula Stubs (purge/embargo formula)
  - docs/IMPLEMENTATION_JOURNAL.md §2026-05-01

Notes: |
  The purge/embargo formula is documented as an open blocker. The implementation must
  include a comment noting the formula assumption used (e.g., embargo = N consecutive
  bars) and flag it for resolution when the independent formula derivation is available.
  The leakage test must use a synthetic dataset where the leakage is injected and
  verifiably detected.

---

## T19: Leakage Detection Checklist

Owner:      codex
Phase:      7
Type:       none
Depends-On: T18

Execution-Mode: heavy
Evidence:
  - "tests/integration/test_leakage.py::test_full_leakage_checklist — all four checks run and report correctly"
  - "tests/integration/test_leakage.py::test_leakage_normalization_detected — normalization leakage injected and detected"
  - "tests/integration/test_leakage.py::test_leakage_regime_lookahead_detected — regime label look-ahead injected and detected"
Verifier-Focus: |
  Confirm that: (1) each of the four checks is independently testable with an injected
  violation, (2) the LeakageReport contains PASS/FAIL per check with description,
  (3) all four PASS conditions are tested with clean data, (4) all four FAIL conditions
  are tested with injected violations.

Objective: |
  Implement the machine-checkable leakage audit in entropy/walkforward/leakage.py with
  four checks: (1) normalization leakage (features computed on full series including OOS),
  (2) regime label look-ahead (labels assigned using post-OOS-start data),
  (3) universe selection bias (symbols selected using OOS return data),
  (4) within-window optimization (params re-fitted inside OOS window).
  Return a LeakageReport with PASS/FAIL per check.

Acceptance-Criteria:
  - id: AC-1
    description: "run_checklist(is_window, oos_window, feature_fn=normalize_on_full_series) returns LeakageReport with normalization_leakage=FAIL and a non-empty description."
    test: "tests/integration/test_leakage.py::test_leakage_normalization_detected"
  - id: AC-2
    description: "run_checklist with feature_fn=normalize_on_is_only returns LeakageReport with normalization_leakage=PASS."
    test: "tests/integration/test_leakage.py::test_leakage_normalization_clean"
  - id: AC-3
    description: "run_checklist(is_window, oos_window, regime_label_fn=label_using_post_oos_data) returns LeakageReport with regime_label_lookahead=FAIL."
    test: "tests/integration/test_leakage.py::test_leakage_regime_lookahead_detected"
  - id: AC-4
    description: "run_checklist with universe_selector=select_using_oos_returns returns LeakageReport with universe_selection_bias=FAIL."
    test: "tests/integration/test_leakage.py::test_leakage_universe_selection_detected"
  - id: AC-5
    description: "run_checklist with optimizer=refit_inside_oos returns LeakageReport with within_window_optimization=FAIL."
    test: "tests/integration/test_leakage.py::test_leakage_within_window_optimization_detected"
  - id: AC-6
    description: "run_checklist with all four clean functions returns LeakageReport with all four checks=PASS and overall_status=PASS."
    test: "tests/integration/test_leakage.py::test_full_leakage_checklist"

Files:
  - entropy/walkforward/leakage.py
  - tests/integration/test_leakage.py

Context-Refs:
  - docs/spec.md §Walk-Forward Harness
  - docs/EVIDENCE_INDEX.md §Heavy Task Evidence

---

## T20: Walk-Forward Runner

Owner:      codex
Phase:      7
Type:       none
Depends-On: T18, T19, T09, T16

Execution-Mode: heavy
Evidence:
  - "tests/integration/test_walk_forward.py::test_runner_produces_run_record_with_all_hashes"
  - "tests/integration/test_walk_forward.py::test_runner_blocks_oos_before_leakage_check"
Verifier-Focus: |
  Confirm that: (1) the runner raises if leakage check has not been run before OOS
  evaluation, (2) the RunRecord persisted to the DB contains all four required hashes,
  (3) a run with a missing hash raises IncompleteRunRecordError before any DB write,
  (4) the run uses only IS data for strategy computation and only OOS data for evaluation.

Objective: |
  Implement the walk-forward runner in entropy/walkforward/runner.py that orchestrates:
  load data, apply IS/OOS split, run strategy on IS, validate IS leakage check, run
  strategy on OOS, record RunRecord to DB. The RunRecord must include all hashes for
  reproducibility. OOS evaluation is blocked until leakage check passes.

Acceptance-Criteria:
  - id: AC-1
    description: "run_walk_forward(trial_id, dataset, strategy) returns a RunRecord with non-None values for trial_id, dataset_hash, code_hash, policy_hash, and simbroker_version."
    test: "tests/integration/test_walk_forward.py::test_runner_produces_run_record_with_all_hashes"
  - id: AC-2
    description: "run_walk_forward raises LeakageBlockError if the leakage checklist has not been run and passed on the IS window before OOS evaluation begins."
    test: "tests/integration/test_walk_forward.py::test_runner_blocks_oos_before_leakage_check"
  - id: AC-3
    description: "The RunRecord written to the DB by run_walk_forward is retrievable by run_id and matches the in-memory RunRecord."
    test: "tests/integration/test_walk_forward.py::test_runner_persists_run_record_to_db"
  - id: AC-4
    description: "run_walk_forward raises IncompleteRunRecordError before any DB write when code_hash is None."
    test: "tests/integration/test_walk_forward.py::test_runner_rejects_missing_code_hash"

Files:
  - entropy/walkforward/runner.py
  - tests/integration/test_walk_forward.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md §Run Reproducibility
  - docs/IMPLEMENTATION_CONTRACT.md §OOS Separation Enforcement

---

## Phase 8 — P&L Attribution + Governance State Machine

### T21: P&L Attribution Engine

Owner:      codex
Phase:      8
Type:       none
Depends-On: T05, T06, T16

Execution-Mode: heavy
Evidence:
  - "tests/unit/test_attribution.py::test_four_stream_worked_example — known inputs, expected stream values and net Sharpe"
  - "tests/unit/test_attribution.py::test_net_sharpe_excludes_stream_d — stream d never enters net Sharpe computation"
Verifier-Focus: |
  Confirm that: (1) stream (d) is computed separately and cannot be passed to the net
  Sharpe function, (2) the worked example test verifies stream values against manually
  computed expected values, (3) the net Sharpe boundary is enforced in code (not by
  convention), (4) DrawdownRecord timestamps and values are correct for a known sequence.

Objective: |
  Implement the P&L Attribution Engine in entropy/attribution/engine.py: compute four
  streams (a, b, c, d) from FillLog entries, compute net Sharpe ONLY from streams
  (a)+(b)+(c) using method CI-SR-ACF-v1, generate DrawdownRecords, and produce
  PerformanceMetrics. All formulas tested against worked examples.

Acceptance-Criteria:
  - id: AC-1
    description: "Given a list of FillLog entries with 3 long fills (+1%, +2%, -0.5%) and no overlay or carry, compute_streams() returns PnLStreams with stream_a=[+1%, +2%, -0.5%], stream_b=[0,0,0], stream_c=[cost values], stream_d=[0,0,0]."
    test: "tests/unit/test_attribution.py::test_four_stream_worked_example"
  - id: AC-2
    description: "compute_net_sharpe(pnl_streams) uses only pnl_streams.stream_a + pnl_streams.stream_b + pnl_streams.stream_c; passing stream_d to the computation raises StreamBoundaryError."
    test: "tests/unit/test_attribution.py::test_net_sharpe_excludes_stream_d"
  - id: AC-3
    description: "compute_drawdown_records returns a DrawdownRecord for a return sequence [+1%, +2%, -4%, -3%, +5%] where the drawdown peak is at index 1 (cumulative ~3%), trough at index 3 (approximately -6.9% from peak), and recovery at index 4."
    test: "tests/unit/test_attribution.py::test_drawdown_record_worked_example"
  - id: AC-4
    description: "Net Sharpe computed from [+0.5%, +0.3%, -0.2%, +0.4%, +0.1%] annual returns matches the manually computed value (mean/stdev annualized) within 1e-6 tolerance."
    test: "tests/unit/test_attribution.py::test_net_sharpe_numerical_accuracy"
  - id: AC-5
    description: "compute_performance_metrics returns a PerformanceMetrics where harvey_liu_deflated_sharpe is None with reason_code='stub_pending_formula_verification'."
    test: "tests/unit/test_attribution.py::test_performance_metrics_stub_fields"

Files:
  - entropy/attribution/engine.py
  - tests/unit/test_attribution.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md §Net Sharpe Stream Boundary
  - docs/core/PROTOCOL_SPEC.md §NN-2
  - docs/EVIDENCE_INDEX.md §Heavy Task Evidence

---

## T22: P1/P3 Governance State Machine

Owner:      codex
Phase:      8
Type:       none
Depends-On: T05, T07

Execution-Mode: heavy
Evidence:
  - "tests/unit/test_governance.py::test_p1_circuit_breaker_suite — synthetic suite: trip, reset, idempotency, boundary"
  - "tests/unit/test_governance.py::test_p3_correlation_trigger_suite — synthetic suite: fire, clear, cooldown, boundary"
  - "tests/unit/test_governance.py::test_p1_p3_concurrent — P1 active blocks new positions while P3 ramp is paused"
Verifier-Focus: |
  Confirm that: (1) the P1 trip boundary condition at exactly 12% is correctly handled,
  (2) the P1 reset requires BOTH conditions (gap < 8% AND >= 5 business days),
  (3) idempotency holds for both trip and reset paths,
  (4) GovernanceEvents are appended (not updated) for every state transition,
  (5) the concurrent P1+P3 case correctly pauses the P3 ramp when P1 activates.

Objective: |
  Implement the P1/P3 governance state machine in entropy/governance/state_machine.py:
  P1 drawdown circuit breaker (trips at 12% from HWM, blocks new positions, resets when
  gap < 8% AND >= 5 business days elapsed), P3 correlation trigger (fires at rho_avg > 0.55,
  clears at rho_avg < 0.45, cooldown enforced). All state transitions emit GovernanceEvents
  as append-only DB writes. Synthetic test suite required.

Acceptance-Criteria:
  - id: AC-1
    description: "P1StateMachine.update(drawdown_pct=0.12) sets is_p1_active=True; update(drawdown_pct=0.119) does not set is_p1_active=True."
    test: "tests/unit/test_governance.py::test_p1_trips_at_threshold_boundary"
  - id: AC-2
    description: "While is_p1_active=True, can_open_new_position() returns False; after reset, can_open_new_position() returns True."
    test: "tests/unit/test_governance.py::test_p1_blocks_new_positions"
  - id: AC-3
    description: "P1 reset requires both conditions: gap_from_hwm < 0.08 AND business_days_elapsed >= 5; reset with only one condition met does not clear P1."
    test: "tests/unit/test_governance.py::test_p1_reset_requires_both_conditions"
  - id: AC-4
    description: "Calling update() with the same drawdown_pct=0.15 twice when already active does not create a second GovernanceEvent (idempotency)."
    test: "tests/unit/test_governance.py::test_p1_trip_is_idempotent"
  - id: AC-5
    description: "P3StateMachine.update(rho_avg=0.56) sets is_p3_active=True; update(rho_avg=0.44) (below 0.45 hysteresis) clears P3 after cooldown."
    test: "tests/unit/test_governance.py::test_p3_fire_and_clear_with_hysteresis"
  - id: AC-6
    description: "When P1 is active, P3 ramp is paused (p3_ramp_progress frozen); when P1 clears, P3 ramp resumes from frozen progress."
    test: "tests/unit/test_governance.py::test_p1_p3_concurrent"
  - id: AC-7
    description: "Every state transition (P1_TRIP, P1_RESET, P3_FIRE, P3_CLEAR) produces exactly one GovernanceEvent with correct event_type, prior_state, next_state; verified by counting GovernanceEvents emitted."
    test: "tests/unit/test_governance.py::test_p1_circuit_breaker_suite"

Files:
  - entropy/governance/state_machine.py
  - tests/unit/test_governance.py

Context-Refs:
  - docs/core/PROTOCOL_SPEC.md §D Regime Signal Governance
  - docs/EVIDENCE_INDEX.md §Heavy Task Evidence
  - docs/IMPLEMENTATION_CONTRACT.md §Phase Gate Human Approval

---

## Phase 9 — Statistical Analysis + Phase Gate Evidence

### T23: Statistical Analysis Stubs

Owner:      codex
Phase:      9
Type:       none
Depends-On: T06

Objective: |
  Implement statistical analysis stubs in entropy/stats/analysis.py with documented
  formula assumptions: (1) Sharpe CI stub using CI-SR-ACF-v1 (analytical base with
  configurable bootstrap fallback), (2) Harvey-Liu deflation stub (formula skeleton +
  unit test against a worked example noting the formula is unverified pending independent
  reproducibility), (3) N_eff estimator stub using K3 formula k/(1+(k-1)*rho_avg). All
  stubs are documented as stubs pending formula-level verification.

Acceptance-Criteria:
  - id: AC-1
    description: "compute_sharpe_ci(returns=[0.01, 0.02, -0.005, 0.015], method='analytical') returns a tuple (lower, upper) where lower < sharpe_estimate < upper."
    test: "tests/unit/test_stats.py::test_sharpe_ci_bounds_contain_estimate"
  - id: AC-2
    description: "compute_sharpe_ci with method='bootstrap' and n_bootstrap=100 returns a tuple (lower, upper) without raising; the result is documented as stub output."
    test: "tests/unit/test_stats.py::test_sharpe_ci_bootstrap_runs_without_error"
  - id: AC-3
    description: "compute_harvey_liu_deflation(raw_sharpe=0.35, M_total=10, sample_length=252) returns a DeflatedSharpe with deflated_value < raw_sharpe and method_id='HL-HB-v1'; the function's docstring states 'STUB: formula pending independent reproducibility verification'."
    test: "tests/unit/test_stats.py::test_harvey_liu_deflation_reduces_sharpe"
  - id: AC-4
    description: "compute_n_eff(k=6, rho_avg=0.30) returns a value equal to 6/(1+(5*0.30))=2.4 within 1e-10 tolerance."
    test: "tests/unit/test_stats.py::test_n_eff_formula_k3_worked_example"
  - id: AC-5
    description: "compute_n_eff(k=1, rho_avg=any_value) returns 1.0 (single factor; rho is irrelevant)."
    test: "tests/unit/test_stats.py::test_n_eff_single_factor"

Files:
  - entropy/stats/analysis.py
  - tests/unit/test_stats.py

Context-Refs:
  - docs/EVIDENCE_INDEX.md §Statistical Formula Stubs
  - docs/core/PROTOCOL_SPEC.md §Harvey-Liu Haircut Method

---

## T24: Phase 0 Exit Artifacts

Owner:      codex
Phase:      9
Type:       none
Depends-On: T21, T19, T09, T11

Objective: |
  Implement Phase 0 exit artifact generation in entropy/evidence/artifacts.py:
  (1) evaluation report generator (trial_id -> Markdown report with all hashes and
  reproducibility proof), (2) leakage audit evidence collector (runs T19 checklist on
  registered runs, appends to EVIDENCE_INDEX), (3) Phase 0 gate report generator
  (lists all T01-T24 tasks with test paths and status). All outputs are reproducible
  given identical DB state.

Acceptance-Criteria:
  - id: AC-1
    description: "generate_evaluation_report(trial_id) returns a string containing: trial_id, dataset_hash, code_hash, policy_hash, IS window dates, OOS window dates, leakage_status, and net_sharpe (or 'not_computed' if absent)."
    test: "tests/integration/test_evidence.py::test_evaluation_report_contains_all_required_fields"
  - id: AC-2
    description: "Two calls to generate_evaluation_report(trial_id) with identical DB state return byte-identical strings."
    test: "tests/integration/test_evidence.py::test_evaluation_report_is_reproducible"
  - id: AC-3
    description: "collect_leakage_evidence(trial_id) appends a row to EVIDENCE_INDEX.md with trial_id, run_id, check date, and per-check verdicts when the leakage checklist passes for all runs."
    test: "tests/integration/test_evidence.py::test_leakage_evidence_appends_to_index"
  - id: AC-4
    description: "collect_leakage_evidence raises EvidenceCollectionError when any RunRecord for the trial_id has no associated LeakageReport."
    test: "tests/integration/test_evidence.py::test_leakage_evidence_raises_for_missing_report"
  - id: AC-5
    description: "generate_phase0_gate_report() returns a Markdown string listing all 24 task IDs (T01 through T24) each with status PASS if the corresponding test function exists and passes, or FAIL otherwise."
    test: "tests/integration/test_evidence.py::test_phase0_gate_report_lists_all_tasks"

Files:
  - entropy/evidence/artifacts.py
  - tests/integration/test_evidence.py

Context-Refs:
  - docs/spec.md §Phase Gate Evidence
  - docs/EVIDENCE_INDEX.md §Phase Gate Evidence
  - docs/IMPLEMENTATION_CONTRACT.md §Phase Gate Human Approval

---

## Cycle 2 Review Findings — Remediation Tasks

### T-GOV-1: Spec Owner Phase Gate Disposition (ARCH-3 / P1-1)

Owner:      human (Spec Owner)
Phase:      1 (pre-T04 gate)
Type:       governance
Depends-On: none
Review-Source: REVIEW_REPORT Cycle 2, P1-1 / ARCH-3 / META_ANALYSIS MG-06

Objective: |
  Record a formal written disposition in docs/DECISION_LOG.md that resolves the
  phase gate inconsistency identified in ARCH-3: Phase 1 implementation is active
  while protocol-level P0 findings (F-1, F-2, F-4, F-5, F-30, F-31) from Cycle 1
  REVIEW_REPORT remain Inherited-Open or Partial-Mitigation. The disposition must
  choose and document one of: (a) scope separation — PHASE1_AUDIT.md scope is
  formally accepted as sufficient for Phase 1 engineering start; protocol P0
  findings are a parallel non-blocking track; or (b) resolution gate — list which
  protocol P0 findings must be closed before formula-encoding tasks (T08, T15,
  T21, T22, T23) may begin. This task does NOT require code changes.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/DECISION_LOG.md contains a new entry with date 2026-05-03 or later referencing ARCH-3 and explicitly choosing disposition (a) or (b) with rationale."
    test: "grep -i 'ARCH-3' docs/DECISION_LOG.md returns non-empty"
  - id: AC-2
    description: "docs/CODEX_PROMPT.md §Open Findings records ARCH-3 with disposition status (open pending Spec Owner sign-off, or closed with reference to DECISION_LOG entry)."
    test: "grep 'ARCH-3' docs/CODEX_PROMPT.md returns non-empty"

Files:
  - docs/DECISION_LOG.md
  - docs/CODEX_PROMPT.md

Context-Refs:
  - docs/audit/REVIEW_REPORT.md §P1 Issues §P1-1
  - docs/audit/ARCH_REPORT.md §ARCH-3
  - docs/audit/META_ANALYSIS.md §MG-06

---

### T-OBS-1: `entropy health` CLI Command (ARCH-1 / CODE-3)

Owner:      codex
Phase:      1 (before Phase 0 exit gate)
Type:       none
Depends-On: T01
Review-Source: REVIEW_REPORT Cycle 2, CODE-3 / ARCH-1

Objective: |
  Implement the `entropy health` CLI command in entropy/cli.py as required by
  docs/ARCHITECTURE.md §Observability and docs/IMPLEMENTATION_CONTRACT.md §OBS-3.
  The command must perform: (1) PostgreSQL connectivity check (attempt SELECT 1;
  catch and report failure), (2) DuckDB availability check (attempt in-memory
  query). Return JSON {"status": "ok"} on success or
  {"status": "degraded", "checks": [{"name": "...", "status": "fail", "error": "..."}]}
  on any failure. Exit code 0 on ok, 1 on degraded.

Acceptance-Criteria:
  - id: AC-1
    description: "`entropy health` command exists in entropy/cli.py and exits 0 when PostgreSQL and DuckDB are available, printing JSON with status=ok."
    test: "tests/unit/test_cli.py::test_health_command_ok"
  - id: AC-2
    description: "`entropy health` exits 1 and prints JSON with status=degraded when DATABASE_URL is unset or PostgreSQL connection fails."
    test: "tests/unit/test_cli.py::test_health_command_degraded_no_postgres"
  - id: AC-3
    description: "The JSON output is valid JSON parseable by json.loads(); the top-level key is 'status'."
    test: "tests/unit/test_cli.py::test_health_command_output_is_valid_json"

Files:
  - entropy/cli.py
  - tests/unit/test_cli.py

Context-Refs:
  - docs/ARCHITECTURE.md §Observability
  - docs/IMPLEMENTATION_CONTRACT.md §OBS-3

---

### T-OBS-2: Unit Tests for `entropy/tracing.py` and `entropy/metrics.py` (CODE-1 / CODE-2)

Owner:      codex
Phase:      1 (before Phase 0 exit gate)
Type:       none
Depends-On: T01
Review-Source: REVIEW_REPORT Cycle 2, CODE-1 and CODE-2

Objective: |
  Add unit tests for the shared observability helpers. Also fix the return type
  annotation on get_tracer() (CODE-2): change `-> NoOpTracer` to
  `-> opentelemetry.trace.Tracer` so the public API is typed against the interface,
  not the concrete noop. Tests must assert: get_tracer() does not raise and returns
  an object; increment_counter() does not raise; record_histogram() does not raise.

Acceptance-Criteria:
  - id: AC-1
    description: "get_tracer() called with a module name string does not raise and returns a non-None object."
    test: "tests/unit/test_observability.py::test_get_tracer_does_not_raise"
  - id: AC-2
    description: "increment_counter() called with a counter name and integer value does not raise."
    test: "tests/unit/test_observability.py::test_increment_counter_does_not_raise"
  - id: AC-3
    description: "record_histogram() called with a metric name and float value does not raise."
    test: "tests/unit/test_observability.py::test_record_histogram_does_not_raise"
  - id: AC-4
    description: "entropy/tracing.py get_tracer() return annotation is `opentelemetry.trace.Tracer` (not NoOpTracer); verified by ast.parse or grep check."
    test: "tests/unit/test_observability.py::test_get_tracer_return_annotation_is_tracer_interface"

Files:
  - entropy/tracing.py
  - tests/unit/test_observability.py

Context-Refs:
  - docs/audit/REVIEW_REPORT.md §P2 Issues (CODE-1, CODE-2)
  - docs/IMPLEMENTATION_CONTRACT.md §Shared Tracing Module

---

### T-DB-1: `postgres_connection` Fixture Transaction Rollback (CODE-4)

Owner:      codex
Phase:      1 (before T07 integration tests begin)
Type:       none
Depends-On: T03
Review-Source: REVIEW_REPORT Cycle 2, CODE-4

Objective: |
  Fix the `postgres_connection` fixture in tests/conftest.py to wrap the yielded
  connection in an explicit transaction that is rolled back in the finally block.
  This ensures that any INSERT or other write performed inside a test using this
  fixture does not persist to the database after the test completes, preventing
  test contamination across runs. The current fixture only closes the connection
  without rolling back.

Acceptance-Criteria:
  - id: AC-1
    description: "A test that INSERTs a row using the postgres_connection fixture finds zero rows with that value in the same table when the next test runs (rollback isolation confirmed)."
    test: "tests/integration/test_fixture_isolation.py::test_postgres_fixture_rolls_back_on_teardown"
  - id: AC-2
    description: "The fixture still skips cleanly (pytest.skip) when DATABASE_URL is unset."
    test: "tests/smoke/test_smoke.py::test_postgres_connection_fixture (existing test must still pass)"

Files:
  - tests/conftest.py
  - tests/integration/test_fixture_isolation.py

Context-Refs:
  - docs/audit/REVIEW_REPORT.md §P2 Issues (CODE-4)
  - docs/IMPLEMENTATION_CONTRACT.md §SQL Safety
