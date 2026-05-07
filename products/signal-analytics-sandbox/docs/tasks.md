# Tasks — Signal Analytics Sandbox

Version: 1.0
Last updated: 2026-05-07

This task graph is the implementation contract. Acceptance criteria are testable; vague phrases are forbidden (see `templates/tasks_schema.md` §Acceptance Criteria Rules).

Phase 0 contains pre-engineering gates that are **owned by humans, not codex**. Engineering Phase 1 must not begin until both Phase 0 tasks are explicitly acknowledged in `docs/CODEX_PROMPT.md §Phase 0 Gate Status`.

Phases:
- **Phase 0** — Paid pilot demand validation + legal/risk memo (gating, non-codex).
- **Phase 1** — Project skeleton, CI, smoke tests.
- **Phase 2** — Source manifest + capture loader + signal record schema.
- **Phase 3** — Ledger I/O + dedup/ambiguity.
- **Phase 4** — Price-data adapter interface + operator-file provider + snapshot provenance.
- **Phase 5** — Outcome matching + aggregation + Markdown report (heavy-task).
- **Phase 6** — Manual + rule extraction adapters.
- **Phase 7** — Additional price adapters (exchange-public, yfinance-dev).
- **Phase 8** — Gated LLM extraction adapter (heavy-task).

---

## Phase 0 — Pre-Engineering Gates (non-codex)

### SAS-001: Paid Pilot Demand Validation

Owner:      operator (human)
Phase:      0
Type:       none
Depends-On: none

Objective: |
  Confirm at least 3 paid or strongly-committed pilot reports from reachable signal subscribers / signal-research users before the engineering Phase 1 begins. Without this gate, engineering is speculative spend on an unvalidated wedge.

Acceptance-Criteria:
  - id: AC-1
    description: "At least 3 named pilot users have either paid an upfront commitment or signed a written intent-to-pay for a sample report. Recorded in docs/PILOT_LOG.md (created during this task) with name reference, contact, commitment type, date."
    test: "manual-evidence: docs/PILOT_LOG.md exists with ≥3 rows."
  - id: AC-2
    description: "Each pilot has a stated source-of-interest in the log so SAS-002 can scope ToS posture concretely."
    test: "manual-evidence: every row in docs/PILOT_LOG.md has a non-empty source-of-interest column."

Files:
  - docs/PILOT_LOG.md         # created by this task

Notes: |
  This task does not modify any source code. It is a prerequisite for Phase 1 engineering.
  Engineering Phase 1 begins only after the operator marks the Phase 0 Gate Status block in
  docs/CODEX_PROMPT.md as "SAS-001: ✅ acknowledged".

---

### SAS-002: Public-Source Legal / Terms-of-Service Memo

Owner:      legal-risk (human)
Phase:      0
Type:       none
Depends-On: SAS-001

Objective: |
  Produce a memo that defines, for the pilot scope identified in SAS-001, the allowed public sources, forbidden sources, capture mechanisms, screenshot/OCR posture, and data-retention rules. The memo is cited by every SourceManifest and every report's eligibility section.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/legal_risk_memo.md exists and explicitly enumerates allowed source classes (telegram_public, x_public, website_public) and forbidden source classes (private telegram groups, paywalled, login-walled, scraped behind controls)."
    test: "manual-evidence: docs/legal_risk_memo.md present with required sections."
  - id: AC-2
    description: "Memo specifies a data-retention rule for raw captures (max retention period, deletion trigger, evidence-snapshot policy)."
    test: "manual-evidence: memo §Retention is non-empty."
  - id: AC-3
    description: "Memo addresses screenshot/OCR posture: deferred in v1 unless paid demand proves screenshots are the bottleneck and a follow-up memo authorizes them."
    test: "manual-evidence: memo §Screenshots states current posture and gating condition."
  - id: AC-4
    description: "Memo references each pilot's source-of-interest from docs/PILOT_LOG.md and provides an eligibility verdict per source-of-interest (approved | blocked | pending)."
    test: "manual-evidence: every row in docs/PILOT_LOG.md has a corresponding verdict in docs/legal_risk_memo.md §Per-Pilot Verdicts."

Files:
  - docs/legal_risk_memo.md   # created by this task

Notes: |
  This task does not modify any source code. Engineering Phase 1 must not begin until
  both this task and SAS-001 are marked acknowledged in docs/CODEX_PROMPT.md §Phase 0 Gate Status.

---

## Phase 1 — Project Skeleton

### T01: Project Skeleton ✅

Owner:      codex
Phase:      1
Type:       none
Depends-On: none

Objective: |
  Initialize the Python package skeleton, console-script entry, dependency manifests, and base directory structure. After this task the package can be installed in editable mode and `signal-sandbox --help` prints the planned subcommand list (subcommands are stubs that return "not implemented" except `status`).

Acceptance-Criteria:
  - id: AC-1
    description: "pyproject.toml declares package name 'signal-sandbox', requires python>=3.12, lists runtime deps (pydantic>=2, polars, pandas, ccxt, click or typer for CLI), and exposes console_script 'signal-sandbox' = 'signal_sandbox.cli:main'."
    test: "tests/unit/test_skeleton.py::test_pyproject_declares_console_script"
  - id: AC-2
    description: "pip install -e . succeeds and `signal-sandbox --help` exits 0 and prints all subcommands listed in spec.md F10 AC-1."
    test: "tests/integration/test_cli_smoke.py::test_help_lists_subcommands"
  - id: AC-3
    description: "Package directory layout matches docs/ARCHITECTURE.md §File Layout: src/signal_sandbox/ with subpackages sources/, capture/, extraction/, ledger/, prices/, outcomes/, reports/. Each has an __init__.py."
    test: "tests/unit/test_skeleton.py::test_subpackages_exist"
  - id: AC-4
    description: "Every CLI subcommand other than `status` exits with code 2 and prints 'not implemented' when invoked. `status` exits 0."
    test: "tests/integration/test_cli_smoke.py::test_unimplemented_subcommands_exit_2"

Files:
  - pyproject.toml
  - requirements.txt
  - requirements-dev.txt
  - src/signal_sandbox/__init__.py
  - src/signal_sandbox/cli.py
  - src/signal_sandbox/config.py
  - src/signal_sandbox/observability.py
  - src/signal_sandbox/sources/__init__.py
  - src/signal_sandbox/capture/__init__.py
  - src/signal_sandbox/extraction/__init__.py
  - src/signal_sandbox/ledger/__init__.py
  - src/signal_sandbox/prices/__init__.py
  - src/signal_sandbox/outcomes/__init__.py
  - src/signal_sandbox/reports/__init__.py
  - tests/__init__.py
  - tests/conftest.py
  - tests/unit/__init__.py
  - tests/unit/test_skeleton.py
  - tests/integration/__init__.py
  - tests/integration/test_cli_smoke.py
  - README.md

Notes: |
  Phase 0 gates SAS-001 and SAS-002 are enforced by docs/CODEX_PROMPT.md
  §Phase 0 Gate Status and IMPLEMENTATION_CONTRACT §PSR-10, not by this
  engineering-task dependency field.
  Use a single CLI library (pick typer or click and stay with it through the project).
  The observability module must export `get_tracer()` returning a no-op tracer in v1; this
  is the load-bearing tracing-module-shared-singleton requirement of IMPLEMENTATION_CONTRACT
  §Shared Tracing Module. Do not scatter inline noop spans elsewhere.

---

### T02: CI Setup ✅

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01

Objective: |
  Add a GitHub Actions workflow that runs ruff check, ruff format --check, pyright, and pytest on every push and PR to master/main. CI must be green on the same commit that closes Phase 1.

Acceptance-Criteria:
  - id: AC-1
    description: ".github/workflows/ci.yml triggers on push and pull_request to master and main. Uses Python 3.12. Caches pip."
    test: "tests/unit/test_ci_workflow.py::test_workflow_triggers_and_python_version"
  - id: AC-2
    description: "Workflow runs the steps `ruff check src/ tests/`, `ruff format --check src/ tests/`, `pyright`, and `python -m pytest tests/ -q --tb=short` in this order."
    test: "tests/unit/test_ci_workflow.py::test_workflow_step_order"
  - id: AC-3
    description: "Workflow installs deps via `pip install -r requirements-dev.txt -e .`. requirements-dev.txt includes ruff, pyright, pytest, pytest-cov."
    test: "tests/unit/test_ci_workflow.py::test_dev_deps_listed"

Files:
  - .github/workflows/ci.yml
  - requirements-dev.txt

Notes: |
  pyright config goes into pyproject.toml under [tool.pyright] with `pythonVersion = "3.12"`.
  ruff config goes into pyproject.toml under [tool.ruff] (rule selection minimal: E, F, I,
  UP, B). Do not over-configure on first pass.

---

### T03: Phase 1 Smoke Tests ✅

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01, T02

Objective: |
  Establish the Phase 1 baseline: smoke tests that prove the skeleton is importable, the CLI is wired, and the observability module is shared. After this task the baseline recorded in CODEX_PROMPT.md is non-zero.

Acceptance-Criteria:
  - id: AC-1
    description: "tests/unit/test_observability.py::test_get_tracer_is_singleton verifies that two calls to get_tracer() return the same object instance."
    test: "tests/unit/test_observability.py::test_get_tracer_is_singleton"
  - id: AC-2
    description: "tests/unit/test_observability.py::test_logger_is_json verifies the configured logger emits structured JSON with fields {timestamp, subcommand, result}."
    test: "tests/unit/test_observability.py::test_logger_is_json"
  - id: AC-3
    description: "tests/integration/test_cli_smoke.py::test_status_exits_zero verifies `signal-sandbox status` exits 0 against a temporary workspace."
    test: "tests/integration/test_cli_smoke.py::test_status_exits_zero"
  - id: AC-4
    description: "Phase 1 baseline recorded in docs/CODEX_PROMPT.md §Current State as the count of passing tests at the close of Phase 1."
    test: "manual-evidence: docs/CODEX_PROMPT.md updated."

Files:
  - tests/unit/test_observability.py
  - tests/integration/test_cli_smoke.py     # extended in this task
  - docs/CODEX_PROMPT.md                    # updated, not created

Notes: |
  Phase 1 close requires all three universal tests + ruff clean + pyright clean + CI green
  on the same commit.

---

## Phase 2 — Source Manifest, Capture, Signal Record Schema

### T04: SourceManifest Pydantic Schema ✅

Owner:      codex
Phase:      2
Type:       none
Depends-On: T03

Objective: |
  Implement `SourceManifest` (Pydantic v2) with eligibility validation. Loading any source whose `eligibility_verdict != "approved"` from a downstream subcommand must raise `SourceNotApproved`.

Acceptance-Criteria:
  - id: AC-1
    description: "SourceManifest accepts source_type ∈ {telegram_public, x_public, website_public}; any other value raises pydantic ValidationError."
    test: "tests/unit/test_source_manifest.py::test_source_type_allowlist"
  - id: AC-2
    description: "SourceManifest requires eligibility_verdict ∈ {approved, blocked, pending}; missing field raises pydantic ValidationError."
    test: "tests/unit/test_source_manifest.py::test_eligibility_required"
  - id: AC-3
    description: "load_source(workspace, source_id) raises SourceNotApproved when manifest's eligibility_verdict != 'approved'."
    test: "tests/unit/test_source_manifest.py::test_blocked_source_rejected"
  - id: AC-4
    description: "SourceManifest persists to JSON and round-trips byte-identically when re-serialized with Pydantic's model_dump_json(by_alias=False, sort_keys=True)."
    test: "tests/unit/test_source_manifest.py::test_round_trip_byte_identical"

Files:
  - src/signal_sandbox/sources/manifest.py
  - tests/unit/test_source_manifest.py

Notes: |
  Use pydantic v2 strict mode. Source types are an Enum to make adding new types an
  intentional code change (per IMPLEMENTATION_CONTRACT §Public-Source-Only Posture).

---

### T05: Capture Loader ✅

Owner:      codex
Phase:      2
Type:       none
Depends-On: T04

Objective: |
  Load operator-captured raw posts from disk. Verify checksums; reject private-source URL patterns; produce a deterministic ordering for batch loads.

Acceptance-Criteria:
  - id: AC-1
    description: "load_capture(path) returns a CapturedPost whose recomputed SHA-256 of raw_text equals the file's declared text_sha256; mismatch raises CaptureChecksumMismatch."
    test: "tests/unit/test_capture_loader.py::test_checksum_mismatch_rejected"
  - id: AC-2
    description: "load_capture(path) raises PrivateSourceForbidden when evidence_url matches private-source patterns from src/signal_sandbox/sources/private_patterns.py."
    test: "tests/unit/test_capture_loader.py::test_private_source_rejected"
  - id: AC-3
    description: "load_captures(workspace, source_id) returns CapturedPosts sorted by (capture_timestamp_utc, capture_id). Order is stable across re-runs."
    test: "tests/unit/test_capture_loader.py::test_deterministic_order"
  - id: AC-4
    description: "load_captures returns an empty list (not raises) when the captures directory exists but has no files."
    test: "tests/unit/test_capture_loader.py::test_empty_directory"

Files:
  - src/signal_sandbox/capture/loader.py
  - src/signal_sandbox/sources/private_patterns.py
  - tests/unit/test_capture_loader.py

Notes: |
  private_patterns.py is a small module of regexes. Public-source allowlist is enforced by
  SourceManifest source_type at the source level; this module is a defense-in-depth check
  at the URL level.

---

### T06: SignalRecord Schema ✅

Owner:      codex
Phase:      2
Type:       none
Depends-On: T04

Objective: |
  Implement `SignalRecord` Pydantic v2 model and the canonical dedup-key computation.

Acceptance-Criteria:
  - id: AC-1
    description: "SignalRecord with direction ∈ {long, short, flat, unknown}; any other value raises ValidationError."
    test: "tests/unit/test_signal_record.py::test_direction_enum"
  - id: AC-2
    description: "SignalRecord with non-empty ambiguity_flags is accepted (does not raise) but is_evaluable() returns False."
    test: "tests/unit/test_signal_record.py::test_ambiguous_records_not_evaluable"
  - id: AC-3
    description: "compute_dedup_key(record) returns the SHA-256 hex of canonical JSON of {source_id, extracted_timestamp_utc, asset_symbol, direction, entry, stop, target} with sort_keys=True. Two records with identical fields produce identical keys."
    test: "tests/unit/test_signal_record.py::test_dedup_key_canonical"
  - id: AC-4
    description: "compute_dedup_key is sensitive to whitespace and case in asset_symbol — 'BTC' vs ' btc ' produce different keys (no implicit normalization that could mask duplicates incorrectly)."
    test: "tests/unit/test_signal_record.py::test_dedup_key_sensitive_to_normalization"

Files:
  - src/signal_sandbox/ledger/record.py
  - tests/unit/test_signal_record.py

Notes: |
  Make the dedup-key formula explicit in module docstring — this is consumed by T07 and is
  the load-bearing identity contract for the ledger.

---

## Phase 3 — Ledger I/O + Dedup

### T07: Ledger I/O (Parquet) ✅

Owner:      codex
Phase:      3
Type:       none
Depends-On: T06

Objective: |
  Read/write the approved ledger as Parquet. Enforce idempotent writes (same input ⇒ byte-identical Parquet) and deterministic column ordering.

Acceptance-Criteria:
  - id: AC-1
    description: "write_ledger(records, path) writes a Parquet file with columns in a fixed canonical order (declared in module). Two writes of the same record set produce byte-identical files (compared by SHA-256 of the file)."
    test: "tests/unit/test_ledger_io.py::test_write_idempotent"
  - id: AC-2
    description: "read_ledger(path) ⇒ write_ledger(records, path2) produces a Parquet file with SHA-256 identical to path."
    test: "tests/unit/test_ledger_io.py::test_round_trip_byte_identical"
  - id: AC-3
    description: "write_ledger raises DuplicateSignalRecord when two records share a dedup_key, unless force_duplicate=True; with force, both records have ambiguity_flags=['duplicate_dedup_key']."
    test: "tests/unit/test_ledger_io.py::test_duplicate_handling"
  - id: AC-4
    description: "Empty ledger (zero records) writes a Parquet file containing the schema but no rows; reads back as an empty list."
    test: "tests/unit/test_ledger_io.py::test_empty_ledger_round_trip"

Files:
  - src/signal_sandbox/ledger/io.py
  - tests/unit/test_ledger_io.py

Notes: |
  Polars supports deterministic Parquet writes via explicit `compression="zstd"` and
  `statistics=False`. Confirm in tests that file metadata does not embed a per-write
  timestamp. If pyarrow is needed for full determinism control, add it to requirements
  and document in DECISION_LOG.

---

### T08: Dedup + Ambiguity Flagging ✅

Owner:      codex
Phase:      3
Type:       none
Depends-On: T06, T07

Objective: |
  Provide the deduplication and ambiguity-flagging pipeline used between extraction drafts and the approved ledger. Pure functions over `SignalRecord`.

Acceptance-Criteria:
  - id: AC-1
    description: "deduplicate(records) groups by dedup_key; for any group of size > 1, all records get ambiguity_flags=['duplicate_dedup_key'] appended unless they were already flagged."
    test: "tests/unit/test_dedup.py::test_grouping_and_flagging"
  - id: AC-2
    description: "flag_ambiguous(record) appends 'missing_entry' when entry is None, 'missing_target_and_stop' when both target and stop are None, 'unknown_direction' when direction == 'unknown'. Existing flags are preserved (set semantics, not list-append duplicates)."
    test: "tests/unit/test_dedup.py::test_flag_combinations"
  - id: AC-3
    description: "Pipeline is deterministic — running twice on the same input produces identical output (compared by canonical JSON serialization)."
    test: "tests/unit/test_dedup.py::test_deterministic"

Files:
  - src/signal_sandbox/ledger/dedup.py
  - tests/unit/test_dedup.py

Notes: |
  Explicit set semantics on ambiguity_flags so re-running on already-flagged records is
  idempotent.

---

## Phase 4 — Price Adapters + Snapshot

### T09: PriceDataProvider Abstract Interface ✅

Owner:      codex
Phase:      4
Type:       none
Depends-On: T03

Objective: |
  Define the `PriceDataProvider` ABC and the `PriceSnapshot` record type. The interface is the contract that every concrete provider in this and subsequent phases must satisfy.

Acceptance-Criteria:
  - id: AC-1
    description: "PriceDataProvider.snapshot(assets: list[str], range_start_utc, range_end_utc, as_of_utc) is an abstract method. Subclasses that don't implement it raise TypeError on instantiation."
    test: "tests/unit/test_price_provider_base.py::test_abstract_method_required"
  - id: AC-2
    description: "PriceSnapshot has fields {provider_id, provider_status, as_of_utc, range_start_utc, range_end_utc, assets, ohlcv_bytes, sha256}. Constructing with mismatched sha256 vs ohlcv_bytes raises SnapshotChecksumMismatch."
    test: "tests/unit/test_price_provider_base.py::test_snapshot_checksum_validated"
  - id: AC-3
    description: "PriceSnapshot.canonical_bytes() returns deterministic bytes (Parquet with fixed compression + no per-write metadata, or msgpack — choose and document); two snapshots with identical content produce identical canonical_bytes."
    test: "tests/unit/test_price_provider_base.py::test_canonical_bytes_deterministic"

Files:
  - src/signal_sandbox/prices/base.py
  - tests/unit/test_price_provider_base.py

Notes: |
  Document the snapshot serialization choice in DECISION_LOG (D-N) — it is the contract
  for reproducibility. Prefer Parquet to keep one serialization library across the project.

---

### T10: OperatorFilePriceProvider ✅

Owner:      codex
Phase:      4
Type:       none
Depends-On: T09

Objective: |
  Implement the operator-file price-data adapter: read OHLCV from operator-supplied CSV/Parquet at a known workspace path; produce a `PriceSnapshot` with `provider_status="operator_supplied"`.

Acceptance-Criteria:
  - id: AC-1
    description: "OperatorFilePriceProvider.snapshot(...) loads OHLCV from <workspace>/price_inputs/<asset>.parquet, validates the schema (open, high, low, close, volume, timestamp_utc), and returns a PriceSnapshot with provider_status='operator_supplied'."
    test: "tests/integration/test_operator_file_provider.py::test_basic_snapshot"
  - id: AC-2
    description: "Snapshot is byte-identical (sha256) when invoked twice with the same inputs and the same source files."
    test: "tests/integration/test_operator_file_provider.py::test_idempotent"
  - id: AC-3
    description: "Missing or malformed input file raises OperatorPriceFileMissing or OperatorPriceFileMalformed (no silent empty result)."
    test: "tests/integration/test_operator_file_provider.py::test_missing_and_malformed"

Files:
  - src/signal_sandbox/prices/operator_file.py
  - tests/integration/test_operator_file_provider.py

Notes: |
  This is the canonical v1 provider. The other providers in Phase 7 must satisfy the same
  contract; this one defines the test fixtures.

---

### T11: PriceSnapshot Persistence + Provenance ✅

Owner:      codex
Phase:      4
Type:       none
Depends-On: T09, T10

Objective: |
  Persist `PriceSnapshot` to disk with provenance metadata (`<workspace>/snapshots/<snapshot_id>/{ohlcv.parquet,metadata.json}`). The metadata includes provider_id, provider_status, as_of_utc, range, assets, sha256, and is the load-bearing provenance record cited by reports.

Acceptance-Criteria:
  - id: AC-1
    description: "save_snapshot(snapshot, workspace) writes ohlcv.parquet and metadata.json. metadata.json's sha256 field equals SHA-256 of ohlcv.parquet on disk."
    test: "tests/unit/test_snapshot_persistence.py::test_metadata_sha_matches_file"
  - id: AC-2
    description: "Re-saving the same snapshot to the same path produces byte-identical files. Saving a different snapshot to the same path raises SnapshotAlreadyExists (snapshots are immutable)."
    test: "tests/unit/test_snapshot_persistence.py::test_idempotent_and_immutable"
  - id: AC-3
    description: "load_snapshot(workspace, snapshot_id) recomputes ohlcv.parquet's SHA-256 and raises SnapshotChecksumMismatch when it disagrees with metadata.json."
    test: "tests/unit/test_snapshot_persistence.py::test_load_verifies_checksum"

Files:
  - src/signal_sandbox/prices/snapshot.py
  - tests/unit/test_snapshot_persistence.py

Notes: |
  Snapshot immutability is the basis of report reproducibility. Document the SnapshotAlreadyExists
  rule in IMPLEMENTATION_CONTRACT §Project-Specific Rules (already done in this Phase 1 draft).

---

## Phase 5 — Outcome Matching + Aggregation + Report (heavy)

### T12: Outcome Matching Engine ✅

Owner:      codex
Phase:      5
Type:       none
Depends-On: T07, T11

Execution-Mode: heavy
Evidence:
  - tests/integration/test_outcome_matcher.py covering: target_hit, stop_hit, timeout_no_hit, excluded_ambiguous, excluded_no_price.
  - tests/integration/test_outcome_matcher.py::test_byte_identical_re_run with a fixed ledger + snapshot fixture.
  - docs/audit/HEAVY_T12_EVIDENCE.md citing the rule_registry version, the fixture provenance, and an enumerated example for each outcome type.
Verifier-Focus: |
  Confirm: deterministic floating-point math (rounding rule honored), each outcome cites a
  rule_id from the registry, the same (ledger.sha256, snapshot.sha256) tuple produces a
  byte-identical outcomes Parquet, and exclusion semantics match spec F6 AC-2 / AC-3.

Objective: |
  Implement the outcome matcher: for each evaluable signal, walk forward through the snapshot from extracted_timestamp_utc and apply a deterministic entry/stop/target rule, emitting an OutcomeRecord with rule_id citation.

Acceptance-Criteria:
  - id: AC-1
    description: "Re-running match(ledger, snapshot) on the same inputs produces a byte-identical outcomes Parquet (compared by SHA-256)."
    test: "tests/integration/test_outcome_matcher.py::test_byte_identical_re_run"
  - id: AC-2
    description: "A signal with a target above entry and a stop below entry (long) produces outcome='target_hit' when high >= target before low <= stop in the snapshot's timestamp order, and 'stop_hit' otherwise. Verified on a synthetic OHLCV fixture."
    test: "tests/integration/test_outcome_matcher.py::test_long_target_and_stop"
  - id: AC-3
    description: "Signals with direction in {flat, unknown} or non-empty ambiguity_flags produce outcome='excluded_ambiguous' and contribute zero to win/loss aggregates."
    test: "tests/integration/test_outcome_matcher.py::test_excluded_ambiguous"
  - id: AC-4
    description: "Signals whose asset_symbol is not in snapshot.assets produce outcome='excluded_no_price'."
    test: "tests/integration/test_outcome_matcher.py::test_excluded_no_price"
  - id: AC-5
    description: "Each OutcomeRecord cites a rule_id from src/signal_sandbox/outcomes/rule_registry.py. The rule registry version (semver string) is recorded in the outcomes Parquet metadata."
    test: "tests/integration/test_outcome_matcher.py::test_rule_id_cited"
  - id: AC-6
    description: "All numerical fields are rounded to 6 decimal places using banker's rounding and produced via Decimal-based math; doubles are converted only at write boundary. Verified by comparing round-trip results."
    test: "tests/integration/test_outcome_matcher.py::test_rounding_determinism"

Context-Refs:
  - docs/legal_risk_memo.md      # for source-eligibility coupling at exclusion time
  - docs/DECISION_LOG.md#D-001   # snapshot serialization choice (T09)
  - docs/IMPLEMENTATION_CONTRACT.md#§Reproducibility-Contract

Files:
  - src/signal_sandbox/outcomes/matcher.py
  - src/signal_sandbox/outcomes/rule_registry.py
  - tests/integration/test_outcome_matcher.py
  - docs/audit/HEAVY_T12_EVIDENCE.md

Notes: |
  Floating-point determinism: use Decimal for all arithmetic in the matcher; convert to
  float only at Parquet write. Document the rounding rule in rule_registry.py and the
  registry's semver in module docstring. The rule registry is append-only — adding rules
  is allowed; modifying an existing rule's behavior requires a new rule_id.

---

### T13: Aggregator ✅

Owner:      codex
Phase:      5
Type:       none
Depends-On: T12

Objective: |
  Aggregate per-signal OutcomeRecords into a summary: total signals, evaluated signals, wins, losses, timeouts, exclusions by reason, win rate, mean/median return, max drawdown of the cumulative-return series.

Acceptance-Criteria:
  - id: AC-1
    description: "aggregate(outcomes) on the same outcomes Parquet produces a byte-identical SummaryRecord JSON (compared by SHA-256)."
    test: "tests/unit/test_aggregator.py::test_summary_byte_identical"
  - id: AC-2
    description: "Win rate is computed only over evaluated signals (excludes excluded_*); win_rate = wins / (wins + losses). Verified with a fixture where evaluated count differs from total."
    test: "tests/unit/test_aggregator.py::test_win_rate_excludes_excluded"
  - id: AC-3
    description: "Summary contains no forward-looking values; field names are explicitly historical (e.g., 'historical_win_rate', not 'expected_win_rate'). Validated by lint check on field names in the model."
    test: "tests/unit/test_aggregator.py::test_no_forward_looking_field_names"
  - id: AC-4
    description: "Cumulative-return series and its max drawdown are computed from per-signal returns in deterministic chronological order (by signal extracted_timestamp_utc, then dedup_key)."
    test: "tests/unit/test_aggregator.py::test_drawdown_deterministic"

Files:
  - src/signal_sandbox/outcomes/aggregate.py
  - tests/unit/test_aggregator.py

Notes: |
  Use Decimal in the aggregator as well, for the same reasons as T12.

---

### T14: Markdown Report Generator ✅

Owner:      codex
Phase:      5
Type:       none
Depends-On: T13

Execution-Mode: heavy
Evidence:
  - tests/integration/test_report_generator.py with a fixed (ledger, snapshot, outcomes, summary) fixture.
  - tests/integration/test_report_generator.py::test_byte_identical_re_run.
  - docs/audit/HEAVY_T14_EVIDENCE.md citing the disclaimer canonical text, the provenance block format, and a rendered sample.
Verifier-Focus: |
  Confirm: disclaimer block matches src/signal_sandbox/reports/disclaimers.py exactly,
  provenance section cites snapshot.sha256 + provider_id + as_of_utc once, every signal
  row links to evidence with text_sha256, prototype-snapshot warning fires when required,
  and rendering aborts with PrototypeSnapshotNotAccepted when --accept-prototype-prices
  is missing on a prototype snapshot.

Objective: |
  Render the audit report in Markdown. Deterministic, evidence-rich, and shipped with a non-removable non-advice disclaimer.

Acceptance-Criteria:
  - id: AC-1
    description: "Re-rendering on the same (ledger.sha256, snapshot.sha256, outcomes.sha256, summary.sha256) tuple produces a byte-identical Markdown file."
    test: "tests/integration/test_report_generator.py::test_byte_identical_re_run"
  - id: AC-2
    description: "Rendered report contains, exactly once, the canonical disclaimer string from src/signal_sandbox/reports/disclaimers.py:CANONICAL_DISCLAIMER. Removing the import or substituting the string fails a string-presence check at render time (raises DisclaimerMissing)."
    test: "tests/integration/test_report_generator.py::test_disclaimer_present_and_canonical"
  - id: AC-3
    description: "Provenance section lists provider_id, as_of_utc, snapshot.sha256, and ledger.sha256, each exactly once."
    test: "tests/integration/test_report_generator.py::test_provenance_complete"
  - id: AC-4
    description: "Every per-signal row in the Per-Signal Outcomes table includes evidence_url, capture_timestamp_utc, and text_sha256."
    test: "tests/integration/test_report_generator.py::test_per_signal_evidence_present"
  - id: AC-5
    description: "Rendering aborts with PrototypeSnapshotNotAccepted when snapshot.provider_status='prototype' and --accept-prototype-prices is not set."
    test: "tests/integration/test_report_generator.py::test_prototype_snapshot_gated"
  - id: AC-6
    description: "Excluded signals appear in an Excluded Signals table grouped by exclusion reason, with row counts; no excluded signal appears in the win/loss section."
    test: "tests/integration/test_report_generator.py::test_excluded_signals_separated"

Context-Refs:
  - docs/legal_risk_memo.md
  - docs/IMPLEMENTATION_CONTRACT.md#§Reproducibility-Contract

Files:
  - src/signal_sandbox/reports/markdown.py
  - src/signal_sandbox/reports/disclaimers.py
  - tests/integration/test_report_generator.py
  - docs/audit/HEAVY_T14_EVIDENCE.md

Notes: |
  Disclaimers module is small and immutable in spirit — modifications require an ADR.
  The presence-and-canonical check is what prevents accidental disclaimer drift.

---

## Phase 6 — Manual + Rule Extraction Adapters

### T15: ExtractionAdapter ABC ✅

Owner:      codex
Phase:      6
Type:       none
Depends-On: T05, T06

Objective: |
  Define the `ExtractionAdapter` ABC and the `ExtractionResult` envelope. Every adapter returns a `draft_pending_review` record or a `defer_to_human` reason.

Acceptance-Criteria:
  - id: AC-1
    description: "ExtractionAdapter.extract(post) is an abstract method. Subclasses without it cannot be instantiated."
    test: "tests/unit/test_extraction_base.py::test_abstract_method_required"
  - id: AC-2
    description: "ExtractionResult has status ∈ {draft_pending_review, defer_to_human}; status='draft_pending_review' requires a non-None record; status='defer_to_human' requires a non-empty reason string. Mismatches raise ValidationError."
    test: "tests/unit/test_extraction_base.py::test_envelope_invariants"
  - id: AC-3
    description: "Every record returned in an ExtractionResult preserves the post's evidence_url and text_sha256 byte-identically."
    test: "tests/unit/test_extraction_base.py::test_evidence_preserved"

Files:
  - src/signal_sandbox/extraction/base.py
  - tests/unit/test_extraction_base.py

Notes: |
  The "evidence preserved" rule is the load-bearing extraction-side contract. The LLM
  adapter in Phase 8 is also bound by it.

---

### T16: ManualExtractionAdapter ✅

Owner:      codex
Phase:      6
Type:       none
Depends-On: T15

Objective: |
  Implement the manual extraction adapter — the operator's editor opens with a pre-filled template; the operator saves; the adapter parses the saved template into a SignalRecord draft.

Acceptance-Criteria:
  - id: AC-1
    description: "ManualExtractionAdapter.extract(post) writes a template file containing every required SignalRecord field plus pre-filled evidence_url and text_sha256. Tested via injected editor command (no real $EDITOR call)."
    test: "tests/unit/test_manual_extraction.py::test_template_prefilled"
  - id: AC-2
    description: "When the operator's saved file contains all required fields, the adapter returns ExtractionResult(status='draft_pending_review', record=...). When required fields are blank, the adapter returns status='defer_to_human' with a reason listing the missing fields."
    test: "tests/unit/test_manual_extraction.py::test_status_branches"

Files:
  - src/signal_sandbox/extraction/manual.py
  - tests/unit/test_manual_extraction.py

---

### T17: RuleExtractionAdapter ✅

Owner:      codex
Phase:      6
Type:       none
Depends-On: T15

Objective: |
  Implement a rule/regex-based adapter keyed by named rule templates. Templates live in src/signal_sandbox/extraction/rule_templates.py.

Acceptance-Criteria:
  - id: AC-1
    description: "RuleExtractionAdapter(template='binance_spot_v1').extract(post) returns ExtractionResult(status='draft_pending_review', record=...) when the post matches the template; otherwise status='defer_to_human'."
    test: "tests/unit/test_rule_extraction.py::test_match_and_defer"
  - id: AC-2
    description: "Templates are versioned (e.g., 'binance_spot_v1', 'binance_spot_v2'); changing the regex of an existing template version raises a CI lint error (template version is append-only)."
    test: "tests/unit/test_rule_templates.py::test_templates_are_versioned"

Files:
  - src/signal_sandbox/extraction/rule.py
  - src/signal_sandbox/extraction/rule_templates.py
  - tests/unit/test_rule_extraction.py
  - tests/unit/test_rule_templates.py

Notes: |
  Append-only templates make extraction reproducibility honest — re-extracting an old post
  with a new template produces a new record, not a silent edit of an old one.

---

## Phase 7 — Additional Price Adapters

### T18: ExchangePublicOHLCVProvider ✅

Owner:      codex
Phase:      7
Type:       none
Depends-On: T09

Objective: |
  Implement a ccxt-based public-exchange OHLCV adapter for crypto-heavy pilots. provider_status='public_exchange'. Cached snapshots are stored in <workspace>/snapshots/.

Acceptance-Criteria:
  - id: AC-1
    description: "ExchangePublicOHLCVProvider(exchange='binance', timeframe='1m').snapshot(...) returns a PriceSnapshot with provider_status='public_exchange'. ccxt rate-limit defaults are honored."
    test: "tests/integration/test_exchange_public_provider.py::test_basic_snapshot"
  - id: AC-2
    description: "Snapshots are persisted (T11) so that re-running with the same range hits the cache (zero network call on second run)."
    test: "tests/integration/test_exchange_public_provider.py::test_cache_hit_no_network"
  - id: AC-3
    description: "Network failure during fetch raises PriceProviderUnavailable; no partial snapshot is persisted."
    test: "tests/integration/test_exchange_public_provider.py::test_failure_no_partial_snapshot"

Files:
  - src/signal_sandbox/prices/exchange_public.py
  - tests/integration/test_exchange_public_provider.py

Notes: |
  Tests use a recorded ccxt response (vcrpy or equivalent fixture) so CI does not depend
  on a live exchange.

---

### T19: YFinanceDevProvider (prototype only) ✅

Owner:      codex
Phase:      7
Type:       none
Depends-On: T09

Objective: |
  Implement a yfinance-backed provider strictly for dev/prototype use. provider_status='prototype'. The report generator (T14) refuses to render against this snapshot unless --accept-prototype-prices is passed.

Acceptance-Criteria:
  - id: AC-1
    description: "YFinanceDevProvider.snapshot(...) returns a PriceSnapshot with provider_status='prototype'."
    test: "tests/unit/test_yfinance_provider.py::test_status_prototype"
  - id: AC-2
    description: "Activation requires SIGNAL_SANDBOX_ALLOW_YFINANCE=1; absence raises YFinanceNotAllowed at provider construction time."
    test: "tests/unit/test_yfinance_provider.py::test_activation_gated"

Files:
  - src/signal_sandbox/prices/yfinance_dev.py
  - tests/unit/test_yfinance_provider.py

Notes: |
  Brief explicitly says: "yfinance allowed only as a dev/prototype adapter, not canonical
  evidence unless explicitly approved." The activation gate and the report-time
  --accept-prototype-prices gate together enforce that.

---

## Phase 8 — Gated LLM Extraction Adapter (heavy)

### T20: LLMExtractionAdapter ✅

Owner:      codex
Phase:      8
Type:       none
Depends-On: T15

Execution-Mode: heavy
Evidence:
  - tests/integration/test_llm_extraction.py with a fixed mock LLM client (no live API in CI).
  - tests/eval/test_llm_extraction_quality.py: extraction acceptance rate measured on a held-out fixture set.
  - docs/audit/HEAVY_T20_EVIDENCE.md citing the cost-cap behavior, gate behavior, and acceptance-rate baseline.
Verifier-Focus: |
  Confirm: LLM output is never written to the approved ledger directly, every draft has
  status='draft_pending_review' and adapter_id='llm/<provider>/<model>', cost-cap
  enforcement aborts the run cleanly with CostCapExceeded, and activation requires both
  SIGNAL_SANDBOX_ENABLE_LLM=1 and --llm-approved.

Objective: |
  Implement the LLM extraction adapter as a gated escalation. v1 supports a local Ollama
  small-model backend and an optional Anthropic Claude Haiku backend. Both produce
  ExtractionResult records with status='draft_pending_review' only.

Acceptance-Criteria:
  - id: AC-1
    description: "LLMExtractionAdapter(...) raises LLMNotApproved unless SIGNAL_SANDBOX_ENABLE_LLM=1 AND the per-run --llm-approved flag is set."
    test: "tests/unit/test_llm_extraction.py::test_activation_requires_both_gates"
  - id: AC-2
    description: "Every returned ExtractionResult has status='draft_pending_review' and record.extraction_metadata.adapter_id matches the regex 'llm/(ollama|claude)/[A-Za-z0-9._-]+'."
    test: "tests/unit/test_llm_extraction.py::test_status_and_adapter_id"
  - id: AC-3
    description: "Cumulative paid-call cost_usd is tracked across calls; once it exceeds SIGNAL_SANDBOX_COST_CAP_USD, subsequent extract() calls raise CostCapExceeded immediately without invoking the model."
    test: "tests/unit/test_llm_extraction.py::test_cost_cap_enforced"
  - id: AC-4
    description: "There is no code path that writes an LLM-sourced record into the approved ledger. Verified by static check: src/signal_sandbox/ledger/io.py write_ledger refuses records whose extraction_metadata.adapter_id starts with 'llm/' unless they have a non-None reviewer_id."
    test: "tests/unit/test_llm_extraction.py::test_no_direct_write_to_ledger"
  - id: AC-5
    description: "Extraction acceptance rate (proportion of LLM drafts a human reviewer approves without modification) is measured on a fixed eval set in tests/eval/. The baseline is recorded in docs/CODEX_PROMPT.md §Evaluation State on first run."
    test: "tests/eval/test_llm_extraction_quality.py::test_acceptance_rate_baseline"

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#§Project-Specific-Rules
  - docs/legal_risk_memo.md

Files:
  - src/signal_sandbox/extraction/llm.py
  - src/signal_sandbox/extraction/llm_providers/__init__.py
  - src/signal_sandbox/extraction/llm_providers/ollama.py
  - src/signal_sandbox/extraction/llm_providers/claude.py
  - tests/unit/test_llm_extraction.py
  - tests/integration/test_llm_extraction.py
  - tests/eval/test_llm_extraction_quality.py
  - docs/audit/HEAVY_T20_EVIDENCE.md

Notes: |
  No live API in CI — record ollama and Anthropic responses to fixtures via a lightweight
  recorder. The cost-cap mechanism is the budget gate referenced in ARCHITECTURE.md
  §Inference / Model Strategy. Activation flow:
    SIGNAL_SANDBOX_ENABLE_LLM=1  signal-sandbox extract --llm-approved --source ...
  The double gate is intentional — env var alone is insufficient.

---

## Phase 9 — Customer-Backed Telegram Pilot Loop

Phase 9 turns the completed sandbox into a customer-backed pilot on the three
public Telegram sources already provided by potential customers:

- `https://t.me/bablos79`
- `https://t.me/nemphiscrypts`
- `https://t.me/pifagortrade`

This phase is validation-first. It may create pilot documentation, logs,
manual-report artifacts, and narrowly scoped operator workflow improvements
only after a bottleneck is proven. It must not start a Telegram bot, public
SaaS, private-source scraping, marketplace, copy-trading, broker integration,
or Entropy Core research feed.

### SAS-PILOT-001: Pilot Scope ✅

Owner:      codex
Phase:      9
Type:       validation
Depends-On: T20

Objective: |
  Create the concrete pilot scope for the three customer-provided public
  Telegram sources. The scope must define which source is audited first, the
  historical window or target signal count, what qualifies as a signal, what is
  excluded, and what customer decision the report is meant to support.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/PILOT_SCOPE.md` lists all three Telegram sources from `docs/PILOT_LOG.md` and marks them as public Telegram pilot sources."
    test: "manual-evidence: docs/pilot/PILOT_SCOPE.md contains all three source URLs."
  - id: AC-2
    description: "The document chooses the first source to audit and states why that source goes first."
    test: "manual-evidence: docs/pilot/PILOT_SCOPE.md §First Source is non-empty."
  - id: AC-3
    description: "The document defines the audit window or target count per source, with a default target of 30-50 defensible signal records where available."
    test: "manual-evidence: docs/pilot/PILOT_SCOPE.md §Audit Window / Target Count is non-empty."
  - id: AC-4
    description: "The document explicitly states scope-out items: private groups, paywalled/login-walled sources, OCR/screenshots, X/Twitter, Discord, bot ingestion, public leaderboard, marketplace, copy trading, broker integration, and investment advice."
    test: "manual-evidence: forbidden scope list is present."
  - id: AC-5
    description: "The document defines success and kill criteria for the pilot in customer terms: decision impact, payment signal, repeat request/referral, or refusal reason."
    test: "manual-evidence: success/kill criteria sections are present."

Context-Refs:
  - docs/PILOT_LOG.md
  - docs/legal_risk_memo.md
  - docs/PILOT_DEVELOPMENT_LOOP_RU.md
  - STARTUP_PRESSURE_TEST_RU.md

Files:
  - docs/pilot/PILOT_SCOPE.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task is documentation/validation only. Do not change product code.
  The output should be written in Russian unless a source URL / field name is
  clearer in English.

---

### SAS-PILOT-002: Methodology V0 ✅

Owner:      codex
Phase:      9
Type:       validation
Depends-On: SAS-PILOT-001

Objective: |
  Define the pilot methodology before extracting signals. The methodology must
  explain how captures are recorded, how signals are manually extracted, how
  ambiguity is handled, which outcome rules are used, how price provenance is
  recorded, and how reports avoid advice or future-performance claims.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/METHODOLOGY_V0.md` defines required capture fields: source_id, public URL, capture timestamp, raw text, raw-text SHA-256, and operator notes."
    test: "manual-evidence: capture fields section is present."
  - id: AC-2
    description: "The document defines signal qualification rules for asset, direction, entry, stop, target, timestamp, and evidence reference."
    test: "manual-evidence: signal qualification section is present."
  - id: AC-3
    description: "The document defines statuses for approved, ambiguous, not_a_signal, insufficient_fields, duplicate, and needs_rule_template."
    test: "manual-evidence: extraction status table is present."
  - id: AC-4
    description: "The document defines deterministic outcome semantics and says excluded/ambiguous records do not contribute to win/loss stats."
    test: "manual-evidence: outcome/exclusion section is present."
  - id: AC-5
    description: "The document includes non-advice, historical-only, no-future-prediction, no-private-scraping, and no-Entropy-Core-contamination language."
    test: "manual-evidence: guardrail language is present."

Context-Refs:
  - docs/pilot/PILOT_SCOPE.md
  - docs/IMPLEMENTATION_CONTRACT.md
  - docs/ARCHITECTURE.md
  - docs/spec.md
  - docs/legal_risk_memo.md

Files:
  - docs/pilot/METHODOLOGY_V0.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task should use the existing deterministic boundaries. Do not weaken
  PSR-1 public-source-only, PSR-2 reproducibility, PSR-3 LLM output is never
  truth, PSR-6 disclaimer integrity, or PSR-11 no forward-looking claims.

---

### SAS-PILOT-003: First Source Capture Plan And Log ✅

Owner:      codex
Phase:      9
Type:       validation
Depends-On: SAS-PILOT-002

Objective: |
  Prepare and begin the capture package for the first selected public Telegram
  source. If the operator has not supplied raw captures yet, create the capture
  log structure and mark capture rows as pending-operator-input instead of
  inventing data.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/CAPTURE_LOG.md` exists and identifies the first selected source, capture status, capture method, and required evidence fields."
    test: "manual-evidence: docs/pilot/CAPTURE_LOG.md exists with required columns."
  - id: AC-2
    description: "The capture log distinguishes captured, skipped, blocked, and pending-operator-input rows."
    test: "manual-evidence: status definitions are present."
  - id: AC-3
    description: "The capture log records why any post/source is skipped or blocked, including non-public, paywalled, screenshot-only, or insufficient text cases."
    test: "manual-evidence: skip/block reason list is present."
  - id: AC-4
    description: "No private/authenticated scraping method is introduced or recommended."
    test: "manual-evidence: capture method section states public/operator-supplied only."

Context-Refs:
  - docs/pilot/PILOT_SCOPE.md
  - docs/pilot/METHODOLOGY_V0.md
  - docs/legal_risk_memo.md

Files:
  - docs/pilot/CAPTURE_LOG.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Do not fabricate source posts or trading calls. If real public captures are
  not available in the workspace, leave rows as pending operator input.

---

### SAS-PILOT-004: First Source Manual Extraction Log ✅

Owner:      codex
Phase:      9
Type:       validation
Depends-On: SAS-PILOT-003

Objective: |
  Create the manual extraction log for the first source and, if captures are
  available, record approved/ambiguous/excluded signal candidates. The task
  measures extraction feasibility and operator time before any new automation.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/EXTRACTION_LOG.md` exists with fields for capture_id, evidence_url, extracted fields, status, ambiguity_flags, reviewer_id, and operator_minutes."
    test: "manual-evidence: extraction log exists with required columns."
  - id: AC-2
    description: "The log records counts for approved, ambiguous, not_a_signal, insufficient_fields, duplicate, needs_rule_template, and pending_capture."
    test: "manual-evidence: summary count section is present."
  - id: AC-3
    description: "If no real captures are available, the log explicitly says extraction is blocked on operator-supplied captures."
    test: "manual-evidence: blocker section is present when applicable."
  - id: AC-4
    description: "The log identifies repeated formats that may justify future rule templates, without implementing them."
    test: "manual-evidence: future rule-template candidates section is present."

Context-Refs:
  - docs/pilot/CAPTURE_LOG.md
  - docs/pilot/METHODOLOGY_V0.md
  - docs/IMPLEMENTATION_CONTRACT.md

Files:
  - docs/pilot/EXTRACTION_LOG.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Manual extraction is the default. LLM may only be discussed as a draft helper
  after human approval; it must not be treated as final truth.

---

### SAS-PILOT-005: First Source Report V0 ✅

Owner:      codex
Phase:      9
Type:       validation
Depends-On: SAS-PILOT-004

Objective: |
  Produce the first customer-readable report artifact or a clear blocked report
  memo if captures/extraction are insufficient. The report should be private,
  historical-only, evidence-backed, and suitable for customer review.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/reports/` exists and contains a first-source report or blocked-report memo."
    test: "manual-evidence: docs/pilot/reports/ contains the artifact."
  - id: AC-2
    description: "The report includes source, audit window, capture count, extraction count, approved/evaluable count, excluded count, limitations, and non-advice language."
    test: "manual-evidence: required report sections are present."
  - id: AC-3
    description: "If outcome matching is possible, the report includes price-source provenance and deterministic outcome assumptions. If not possible, it states the blocker."
    test: "manual-evidence: outcome/provenance or blocker section is present."
  - id: AC-4
    description: "The report does not recommend trades, rank influencers publicly, predict future performance, or use defamation-style language."
    test: "manual-evidence: report language is historical and caveated."

Context-Refs:
  - docs/pilot/PILOT_SCOPE.md
  - docs/pilot/METHODOLOGY_V0.md
  - docs/pilot/CAPTURE_LOG.md
  - docs/pilot/EXTRACTION_LOG.md
  - docs/IMPLEMENTATION_CONTRACT.md

Files:
  - docs/pilot/reports/
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task can use existing deterministic code if the needed inputs exist, but
  it must not implement new product features. If the report is blocked, write a
  blocker memo rather than inventing data.

---

### SAS-PILOT-006: Customer Feedback And Payment Signal Log ✅

Owner:      codex
Phase:      9
Type:       validation
Depends-On: SAS-PILOT-005

Objective: |
  Create the customer feedback and payment-signal log for the first report.
  The goal is to capture whether the report changed a decision and whether
  there is payment, deposit, intent-to-pay, repeat request, or referral.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/CUSTOMER_FEEDBACK.md` exists with past-behavior questions, customer decision impact, objections, format preference, and next requested source."
    test: "manual-evidence: feedback log exists with required sections."
  - id: AC-2
    description: "`docs/pilot/PAYMENT_SIGNAL_LOG.md` exists and distinguishes paid, deposit, written intent-to-pay, repeat request, referral, no-payment, and false-positive enthusiasm."
    test: "manual-evidence: payment signal log exists with status definitions."
  - id: AC-3
    description: "The feedback questions avoid hypothetical 'would you pay/use' wording and focus on what the customer did or decided."
    test: "manual-evidence: question list is past-behavior oriented."
  - id: AC-4
    description: "The log records whether Telegram delivery mattered as delivery format only, not as approval to build bot ingestion."
    test: "manual-evidence: Telegram delivery section is present."

Context-Refs:
  - docs/pilot/reports/
  - docs/PILOT_DEVELOPMENT_LOOP_RU.md
  - STARTUP_PRESSURE_TEST_RU.md

Files:
  - docs/pilot/CUSTOMER_FEEDBACK.md
  - docs/pilot/PAYMENT_SIGNAL_LOG.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  If customer feedback has not been received yet, create the log and mark rows
  as pending-customer-review. Do not mark the pilot successful without a real
  behavior/payment signal.

---

### SAS-PILOT-007: Repeat Or Automate Decision ✅

Owner:      codex
Phase:      9
Type:       validation
Depends-On: SAS-PILOT-006

Objective: |
  Decide whether to repeat the manual audit on the remaining two sources,
  automate a narrow bottleneck, pivot the offer, or stop. This task is the
  Phase 9 decision gate and must not approve broad product expansion without
  payment evidence.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/PILOT_DECISION.md` exists and gives one of: repeat manual reports, automate narrow bottleneck, keep concierge, pivot to seller verification, stop/defer."
    test: "manual-evidence: decision document exists with explicit verdict."
  - id: AC-2
    description: "The decision cites evidence from capture, extraction, report, feedback, and payment-signal logs."
    test: "manual-evidence: evidence references section is present."
  - id: AC-3
    description: "If automation is recommended, it names the exact bottleneck and the smallest next engineering task. It must not approve bot ingestion, private scraping, marketplace, copy trading, broker integration, or public leaderboard."
    test: "manual-evidence: automation scope is narrow and forbidden expansions are still blocked."
  - id: AC-4
    description: "The document states whether to continue with the second and third Telegram sources and what must be true before doing so."
    test: "manual-evidence: remaining-source plan is present."

Context-Refs:
  - docs/pilot/CAPTURE_LOG.md
  - docs/pilot/EXTRACTION_LOG.md
  - docs/pilot/CUSTOMER_FEEDBACK.md
  - docs/pilot/PAYMENT_SIGNAL_LOG.md
  - docs/PILOT_DEVELOPMENT_LOOP_RU.md

Files:
  - docs/pilot/PILOT_DECISION.md
  - docs/tasks.md
  - docs/CODEX_PROMPT.md
  - docs/DECISION_LOG.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  If the decision creates new engineering work, add a new follow-up phase to
  docs/tasks.md only after this decision document exists. Do not silently widen
  the product.

---

## Phase 10 — Draft Extraction Assistant For Captured Telegram Posts

Phase 10 is a narrow automation phase justified by the captured first-source
batch: `workspace/captures/bablos79/` contains 60 public text captures and
`docs/pilot/EXTRACTION_LOG.md` has `pending_manual_extraction=60`.

This phase builds a deterministic draft parser / triage assistant. It may use a
frontier model offline for author-specific lexicon discovery, but only as a
draft candidate generator with evidence and human approval. It must not write
approved ledger records, treat parser output as truth, introduce LLM-owned final
extraction, add bot ingestion, scrape private sources, or expand into SaaS.
Human review remains required before any signal record becomes approved.

Reference plan: `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`.

### SAS-AUTO-001: Seed Labels For bablos79 Draft Parser

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-PILOT-007

Objective: |
  Create a representative hand-labeled seed set from the 60 captured public
  `bablos79` posts before implementing parser logic. The seed must include clear
  non-signals, insufficient-field trade mentions, ambiguous candidates, and any
  obvious review candidates if present.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/BABLOS79_LABEL_SEED.md` exists with 10-15 rows sampled from `workspace/captures/bablos79/`."
    test: "manual-evidence: seed file has 10-15 capture IDs."
  - id: AC-2
    description: "Each seed row includes capture_id, evidence_url, text_sha256, short text excerpt, expected suggested status, and reason."
    test: "manual-evidence: seed table has required columns."
  - id: AC-3
    description: "The seed includes at least `not_a_signal`, `insufficient_fields`, and `ambiguous` unless the captured corpus truly lacks one category, in which case the absence is documented."
    test: "manual-evidence: category coverage section is present."
  - id: AC-4
    description: "No approved ledger rows are created and no parser output is treated as final truth."
    test: "manual-evidence: seed file states human-review boundary."

Context-Refs:
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md
  - docs/pilot/CAPTURE_LOG.md
  - docs/pilot/EXTRACTION_LOG.md
  - docs/pilot/METHODOLOGY_V0.md

Files:
  - docs/pilot/BABLOS79_LABEL_SEED.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This is labeling/planning, not parser implementation. Do not add product code
  in this task.

---

### SAS-AUTO-001B: LLM-Assisted Author Lexicon Discovery

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-001

Objective: |
  Use a frontier model offline to propose `bablos79`-specific extraction terms
  from the 60 captured public posts. The model output is a review artifact only:
  it may widen the candidate vocabulary after human approval, but it must not
  create final extraction rows or become a parser/runtime dependency.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_LEXICON_DRAFT.md` exists and lists candidate terms grouped by extraction category."
    test: "manual-evidence: draft lexicon artifact exists with category sections."
  - id: AC-2
    description: "Every candidate includes term, category, evidence_capture_ids, short evidence excerpt, false-positive risk, and confidence."
    test: "manual-evidence: candidate table has required columns."
  - id: AC-3
    description: "`docs/pilot/bablos79_APPROVED_LEXICON.md` records a human decision for every candidate: approved, rejected, or deferred."
    test: "manual-evidence: approved lexicon includes decision column and no undecided rows."
  - id: AC-4
    description: "Rejected or deferred terms are explicitly excluded from parser fixtures and parser behavior."
    test: "manual-evidence: exclusion section cites rejected/deferred candidates."
  - id: AC-5
    description: "No LLM call is added to parser runtime, CLI export, ledger writing, tests, or any always-on product path."
    test: "manual-evidence: task closeout states LLM usage is offline-only; code review confirms no runtime LLM call was introduced."

Context-Refs:
  - docs/pilot/BABLOS79_LABEL_SEED.md
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md
  - docs/pilot/CAPTURE_LOG.md
  - docs/pilot/EXTRACTION_LOG.md
  - workspace/captures/bablos79/

Files:
  - docs/pilot/bablos79_LEXICON_DRAFT.md
  - docs/pilot/bablos79_APPROVED_LEXICON.md
  - workspace/lexicons/bablos79_lexicon_draft.json
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task may use a frontier model as an offline analyst over public local
  captures. The model proposes vocabulary only; it does not decide whether a
  post is a valid signal. Parser implementation starts after this task and can
  use only approved lexicon entries.

---

### SAS-AUTO-002: Deterministic Draft Parser Library

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-001B

Objective: |
  Implement pure deterministic parser functions over `CapturedPost` that suggest
  extraction statuses and candidate fields for human review. The parser may use
  the approved `bablos79` author lexicon as static local input. It must preserve
  evidence fields and must not call an LLM or network.

Acceptance-Criteria:
  - id: AC-1
    description: "`parse_draft(post)` returns a structured draft with capture_id, evidence_url, text_sha256, suggested_status, candidate fields, missing_required_fields, reason_codes, and confidence."
    test: "tests/unit/test_draft_parser.py::test_parse_draft_returns_structured_review_draft"
  - id: AC-2
    description: "Evidence fields from `CapturedPost` are preserved byte-identically in every draft."
    test: "tests/unit/test_draft_parser.py::test_parse_draft_preserves_evidence_fields"
  - id: AC-3
    description: "Seed labels in `docs/pilot/BABLOS79_LABEL_SEED.md` classify deterministically with no time, locale, network, or LLM dependency."
    test: "tests/unit/test_draft_parser.py::test_seed_labels_classify_deterministically"
  - id: AC-4
    description: "Parser output never maps directly to final `approved`; complete candidates use `review_candidate` until human review."
    test: "tests/unit/test_draft_parser.py::test_complete_candidate_requires_human_review"

Context-Refs:
  - docs/pilot/BABLOS79_LABEL_SEED.md
  - docs/pilot/bablos79_APPROVED_LEXICON.md
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md
  - src/signal_sandbox/capture/loader.py
  - src/signal_sandbox/extraction/rule.py
  - docs/IMPLEMENTATION_CONTRACT.md

Files:
  - src/signal_sandbox/extraction/draft_parser.py
  - tests/unit/test_draft_parser.py
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Keep this pure and local. No CLI wiring, no ledger writes, no LLM calls.
  Rejected or deferred lexicon candidates from `SAS-AUTO-001B` must not affect
  parser behavior.

---

### SAS-AUTO-003: Draft Export Artifact

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-002

Objective: |
  Export parser suggestions for all captured `bablos79` posts into a reviewable
  artifact. The export must be deterministic, sorted, and clearly marked as
  draft-only.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md` exists and contains one draft row per captured post."
    test: "manual-evidence: row count matches `load_captures(Path(\"workspace\"), \"bablos79\")`."
  - id: AC-2
    description: "Rows are sorted by source timestamp and capture_id, include suggested status, candidate fields, missing fields, reason codes, confidence, evidence_url, and text_sha256."
    test: "tests/unit/test_draft_export.py::test_export_rows_are_deterministic_and_complete"
  - id: AC-3
    description: "Every row has reviewer_id set to `pending`; export does not create or modify approved ledger files."
    test: "tests/unit/test_draft_export.py::test_export_is_draft_only_and_does_not_write_ledger"

Context-Refs:
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md
  - docs/pilot/BABLOS79_LABEL_SEED.md
  - src/signal_sandbox/extraction/draft_parser.py

Files:
  - src/signal_sandbox/extraction/draft_export.py
  - tests/unit/test_draft_export.py
  - docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task may add a local helper function, but not a new bot, service, or
  network collector.

---

### SAS-AUTO-004: Merge Draft Suggestions Into Extraction Log

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-003

Objective: |
  Update `docs/pilot/EXTRACTION_LOG.md` with parser suggestions while keeping
  final review status separate from draft status. This measures whether the
  parser reduces manual review work without approving records automatically.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/EXTRACTION_LOG.md` summary counts include draft suggested statuses separately from final approved statuses."
    test: "manual-evidence: draft-vs-final counts section is present."
  - id: AC-2
    description: "All 60 captured rows have a suggested status or documented parser failure reason."
    test: "manual-evidence: no `pending_manual_extraction` rows remain without a suggestion."
  - id: AC-3
    description: "Rows suggested as `review_candidate` still have reviewer_id=`pending` and final status is not `approved`."
    test: "manual-evidence: human-review boundary preserved."
  - id: AC-4
    description: "Repeated patterns that could become rule templates are listed without implementing new templates in this task."
    test: "manual-evidence: rule-template candidate section is present."

Context-Refs:
  - docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md
  - docs/pilot/METHODOLOGY_V0.md
  - docs/IMPLEMENTATION_CONTRACT.md

Files:
  - docs/pilot/EXTRACTION_LOG.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This is still draft classification. Approved ledger creation remains out of
  scope until human review is explicitly recorded.

---

### SAS-AUTO-005: Draft Parser Evaluation And Next Decision

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-004

Objective: |
  Evaluate whether the deterministic draft parser is useful enough to keep,
  improve, or discard. The decision must cite reviewed rows and measured false
  positives / useful suggestions.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/AUTO_EXTRACTION_EVAL.md` records eval source, date, row counts, suggested-status distribution, false-positive notes, and operator-review implications."
    test: "manual-evidence: eval artifact has Date and Eval Source fields."
  - id: AC-2
    description: "`docs/pilot/PILOT_DECISION.md` is updated with one of: keep draft helper, improve parser rules, discard parser, or continue manual-only."
    test: "manual-evidence: decision section cites eval artifact."
  - id: AC-3
    description: "If a next engineering task is proposed, it names the exact bottleneck and does not approve bot ingestion, private scraping, marketplace, copy trading, broker integration, public leaderboard, or LLM truth."
    test: "manual-evidence: automation boundary section is present."

Context-Refs:
  - docs/pilot/EXTRACTION_LOG.md
  - docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md
  - docs/pilot/PAYMENT_SIGNAL_LOG.md
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md

Files:
  - docs/pilot/AUTO_EXTRACTION_EVAL.md
  - docs/pilot/PILOT_DECISION.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This is the Phase 10 decision gate. Do not silently widen the product.
