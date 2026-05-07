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

### T16: ManualExtractionAdapter

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

### T17: RuleExtractionAdapter

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

### T18: ExchangePublicOHLCVProvider

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

### T19: YFinanceDevProvider (prototype only)

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

### T20: LLMExtractionAdapter

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
