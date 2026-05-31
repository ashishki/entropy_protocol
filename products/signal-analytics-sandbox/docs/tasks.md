# Tasks — Signal Analytics Sandbox

Version: 1.3
Last updated: 2026-05-15

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
- **Phase 9** — First public-source pilot loop and blocked report.
- **Phase 10** — Draft extraction assistant for captured Telegram posts.
- **Phase 11** — Author Market Intelligence architecture reset.
- **Phase 12** — Asset universe and market-data foundation.
- **Phase 13** — Universal source corpus and channel profiles.
- **Phase 14** — Local RAG context layer.
- **Phase 15** — Market idea extraction.
- **Phase 16** — Deterministic thesis evaluation.
- **Phase 17** — Bounded batch analyst.
- **Phase 18** — Author Market Report V0.
- **Phase 19** — Channel-specific modalities and tools.
- **Phase 20** — Telegram media evidence: voice and image/OCR drafts.
- **Phase 21** — Artifact-first real public-source report validation, including
  real public media acquisition when text-only evidence is insufficient.
- **Phase 22** — Expanded public corpus for deep channel retrospective.
- **Phase 23** — Image/OCR and reviewed multimodal evidence.
- **Phase 24** — Claim ledger and retrospective market outcomes.
- **Phase 25** — Author capability report and external-ready gate.
- **Phase 26** — Operator-gated evidence repair for `bablos79`.
- **Phase 27** — Three-channel V1 metric report: reviewed extraction,
  level-aware outcomes, multimodal claims, and external-ready gate.
- **Phase 36** — Channel impact framework and cross-channel evidence
  completion before dashboard/deep-report comparison.
- **Phase 37** — Pre-client artifact hardening: reliable free-dashboard,
  paid-report, review, evidence, and gate artifacts before outreach.
- **Phase 38** — Client-readiness evidence acceptance: operator decisions,
  accepted-row recompute, redacted buyer-demo subset, and discovery criteria.
- **Phase 39** — Telegram Trader Intelligence productization: product frame,
  receipts, referee verdicts, diverse analytical lenses, and buyer-demo report
  structure.
- **Phase 40** — Auto-validation evidence contract: define the proof bundle,
  validator result schema, audit log, and allowed auto-decision states.
- **Phase 41** — Auto-validation validator stack: deterministic and
  evidence-backed checks for pre-outcome timing, OCR/level confidence,
  setup consistency, asset/proxy/provider eligibility, and post-factum cues.
- **Phase 42** — Auto-accept decision engine and evaluation: combine validator
  evidence into strict auto-accepted / auto-rejected / needs-human decisions,
  then evaluate against the current 9 media candidates before any customer use.

Current active focus:

- Core is paused.
- The current `bablos79` Phase 21 source/window is rejected for external
  delivery but is not enough evidence to judge the channel.
- The next active route follows `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`:
  expand the public corpus, add image/OCR analysis, build a reviewed claim
  ledger, compare measurable claims to public market data, and produce a
  balanced author capability report.
- After Phase 25, the `bablos79` retrospective is internal-only/rejected for
  external delivery. Phase 26 is a new evidence repair loop focused on public
  corpus expansion, operator candidate review, explicit proxy/horizon approval,
  and recomputing outcomes only after prerequisites exist.
- After `SAS-ER-004`, the three-channel V0 metric report proves the end-to-end
  path but remains internal research. Phase 27 turns it into a reviewed V1
  channel comparison with extraction calibration, level-aware outcomes,
  multimodal evidence, provider/proxy expansion, and an external-ready gate.
- After Phase 35, the new active route is Phase 36: define a broader channel
  impact framework and run the same evidence-completion loop for `bablos79`,
  `nemphiscrypts`, and `pifagortrade` before dashboard/deep-report comparison.
- Phase 37 produced the internal artifact stack and deep review decision
  `continue_internal_hardening`. The next active route is Phase 38: operator
  acceptance, recompute, and redacted buyer-demo readiness before outreach.
- Phase 39 is the planned productization route after Phase 38: it turns the
  sandbox into Telegram Trader Intelligence without approving prediction,
  leaderboard, advice, private scraping, or autonomous trading.
- After Phase 38, the active internal-hardening route is Phases 40-42:
  automate validation only through auditable evidence bundles and deterministic
  validators. Model review may propose candidates, but auto-accept requires
  independent proof checks and conservative thresholds.

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

This phase builds a machine-first draft extraction assistant. It may use a
frontier model offline to generate pseudo-labels and author-specific lexicon
candidates for every captured public post. Deterministic validators must then
verify evidence spans, numbers, tickers, and confidence gates. The system must
not write approved ledger records, treat model/parser output as truth, introduce
LLM-owned final extraction, add bot ingestion, scrape private sources, or expand
into SaaS. Human review is moved from full manual seed labeling to exception
review before any customer-facing claim or approved signal record.

Reference plan: `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`.
Roadmap: `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md`.

### SAS-AUTO-001: Machine-First Pseudo-Label Bootstrap ✅

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-PILOT-007

Objective: |
  Generate structured pseudo-labels for all 60 captured public `bablos79` posts
  without manual seed labeling. The frontier model may propose extraction
  statuses, candidate fields, evidence spans, uncertainty reasons, and lexicon
  terms, but every row remains draft-only and unapproved.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_PSEUDO_LABELS.md` exists with one row per captured post from `workspace/captures/bablos79/`."
    test: "manual-evidence: pseudo-label row count matches `load_captures(Path(\"workspace\"), \"bablos79\")`."
  - id: AC-2
    description: "`workspace/extraction/bablos79_pseudo_labels.jsonl` exists and each JSONL row includes capture_id, suggested_status, candidate fields, missing_fields, evidence_spans, confidence, uncertainty_reason, lexicon_terms_found, and draft_only=true."
    test: "manual-evidence: JSONL artifact exists and has required fields."
  - id: AC-3
    description: "Every non-empty extracted field has at least one evidence span that is intended to be checked against raw capture text in the next task."
    test: "manual-evidence: pseudo-label schema requires field-level evidence spans."
  - id: AC-4
    description: "Low-confidence, contradictory, or uncertain rows are explicitly marked `needs_review` or include a non-empty uncertainty_reason."
    test: "manual-evidence: uncertainty/needs-review section is present."
  - id: AC-5
    description: "No approved ledger rows are created and no pseudo-label output is treated as final truth."
    test: "manual-evidence: pseudo-label artifact states draft-only boundary."

Context-Refs:
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md
  - docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md
  - docs/pilot/CAPTURE_LOG.md
  - docs/pilot/EXTRACTION_LOG.md
  - docs/pilot/METHODOLOGY_V0.md

Files:
  - docs/pilot/bablos79_PSEUDO_LABELS.md
  - workspace/extraction/bablos79_pseudo_labels.jsonl
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This is offline pseudo-label generation, not parser implementation. Do not add
  product code in this task. Do not write approved ledger records.

---

### SAS-AUTO-001B: Author Lexicon And Draft Profile Discovery ✅

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-001

Objective: |
  Derive a `bablos79`-specific lexicon and draft parser profile from pseudo-
  labels, raw public captures, and evidence spans. The output is a draft profile
  for deterministic triage, not approved extraction truth. Terms are classified
  as `accepted_for_draft`, `needs_review`, or `excluded`.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_AUTHOR_PROFILE.md` exists and lists candidate terms grouped by extraction category."
    test: "manual-evidence: author profile artifact exists with category sections."
  - id: AC-2
    description: "Every candidate includes term, category, evidence_capture_ids, short evidence excerpt, false-positive risk, and confidence."
    test: "manual-evidence: candidate table has required columns."
  - id: AC-3
    description: "Every candidate records profile_state as `accepted_for_draft`, `needs_review`, or `excluded`."
    test: "manual-evidence: profile_state column exists and has no empty rows."
  - id: AC-4
    description: "`needs_review` and `excluded` terms are explicitly prevented from becoming automatic parser truth."
    test: "manual-evidence: exclusion/review section cites risky candidates."
  - id: AC-5
    description: "No LLM call is added to parser runtime, CLI export, ledger writing, tests, or any always-on product path."
    test: "manual-evidence: task closeout states LLM usage is offline-only; code review confirms no runtime LLM call was introduced."

Context-Refs:
  - docs/pilot/bablos79_PSEUDO_LABELS.md
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md
  - docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md
  - docs/pilot/CAPTURE_LOG.md
  - docs/pilot/EXTRACTION_LOG.md
  - workspace/captures/bablos79/
  - workspace/extraction/bablos79_pseudo_labels.jsonl

Files:
  - docs/pilot/bablos79_AUTHOR_PROFILE.md
  - workspace/lexicons/bablos79_lexicon_draft.json
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task may use frontier-model output and pseudo-labels as offline analysis
  over public local captures. The model/profile proposes vocabulary only; it
  does not decide whether a post is an approved signal. Parser implementation
  can use only `accepted_for_draft` profile entries.

---

### SAS-AUTO-002: Deterministic Validators And Draft Parser Library ✅

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-001B

Objective: |
  Implement pure deterministic validation and parser functions over
  `CapturedPost` plus pseudo-label/profile artifacts. Validators must reject
  unsupported evidence spans, numbers, tickers, and directions. The parser may
  use only static `accepted_for_draft` author-profile entries and must not call
  an LLM or network.

Acceptance-Criteria:
  - id: AC-1
    description: "`validate_pseudo_label(post, pseudo_label)` rejects evidence spans and candidate fields that are not present in the raw capture text."
    test: "tests/unit/test_draft_validation.py::test_validate_pseudo_label_rejects_unsupported_fields"
  - id: AC-2
    description: "`parse_draft(post, profile)` returns a structured draft with capture_id, evidence_url, text_sha256, suggested_status, candidate fields, missing_required_fields, reason_codes, confidence, and review_required."
    test: "tests/unit/test_draft_parser.py::test_parse_draft_returns_structured_review_draft"
  - id: AC-3
    description: "Evidence fields from `CapturedPost` are preserved byte-identically in every draft."
    test: "tests/unit/test_draft_parser.py::test_parse_draft_preserves_evidence_fields"
  - id: AC-4
    description: "Pseudo-label fixtures classify deterministically with no time, locale, network, or LLM dependency."
    test: "tests/unit/test_draft_parser.py::test_pseudo_label_fixtures_classify_deterministically"
  - id: AC-5
    description: "Parser output never maps directly to final `approved`; complete candidates use `review_candidate` until human review."
    test: "tests/unit/test_draft_parser.py::test_complete_candidate_requires_human_review"

Context-Refs:
  - docs/pilot/bablos79_PSEUDO_LABELS.md
  - docs/pilot/bablos79_AUTHOR_PROFILE.md
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md
  - docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md
  - src/signal_sandbox/capture/loader.py
  - src/signal_sandbox/extraction/rule.py
  - docs/IMPLEMENTATION_CONTRACT.md

Files:
  - src/signal_sandbox/extraction/draft_validation.py
  - src/signal_sandbox/extraction/draft_parser.py
  - tests/unit/test_draft_validation.py
  - tests/unit/test_draft_parser.py
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Keep this pure and local. No CLI wiring, no ledger writes, no LLM calls.
  `needs_review` and `excluded` profile terms from `SAS-AUTO-001B` must not
  become automatic parser truth.

---

### SAS-AUTO-003: Draft Export Artifact ✅

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
  - docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md
  - docs/pilot/bablos79_PSEUDO_LABELS.md
  - docs/pilot/bablos79_AUTHOR_PROFILE.md
  - src/signal_sandbox/extraction/draft_validation.py
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

### SAS-AUTO-004: Exception Review Queue And Extraction Log Merge ✅

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-003

Objective: |
  Generate an exception review queue from parser suggestions and update
  `docs/pilot/EXTRACTION_LOG.md` while keeping final review status separate
  from draft status. This measures whether the system reduces manual review
  from full-corpus labeling to targeted review without approving records
  automatically.

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
    description: "`docs/pilot/bablos79_REVIEW_QUEUE.md` exists and includes all low-confidence, contradictory, customer-facing, and sampled non-signal rows."
    test: "manual-evidence: review queue artifact exists with inclusion policy."
  - id: AC-5
    description: "Repeated patterns that could become rule templates are listed without implementing new templates in this task."
    test: "manual-evidence: rule-template candidate section is present."

Context-Refs:
  - docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md
  - docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md
  - docs/pilot/METHODOLOGY_V0.md
  - docs/IMPLEMENTATION_CONTRACT.md

Files:
  - docs/pilot/bablos79_REVIEW_QUEUE.md
  - docs/pilot/EXTRACTION_LOG.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This is still draft classification. Approved ledger creation remains out of
  scope until human review is explicitly recorded.

---

### SAS-AUTO-005: Draft Extraction Evaluation And Next Decision ✅

Owner:      codex
Phase:      10
Type:       validation
Depends-On: SAS-AUTO-004

Objective: |
  Evaluate whether the machine-first draft extraction pipeline is useful enough
  to keep, improve, or discard. The decision must cite reviewed exception rows,
  measured false positives, useful suggestions, and review-load reduction.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/AUTO_EXTRACTION_EVAL.md` records eval source, date, row counts, suggested-status distribution, review-queue size, false-positive notes, and operator-review implications."
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
  - docs/pilot/bablos79_REVIEW_QUEUE.md
  - docs/pilot/PAYMENT_SIGNAL_LOG.md
  - docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md
  - docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md

Files:
  - docs/pilot/AUTO_EXTRACTION_EVAL.md
  - docs/pilot/PILOT_DECISION.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This is the Phase 10 decision gate. Do not silently widen the product.

---

## Phase 11 — Author Market Intelligence Architecture Reset

### SAS-MI-001: Author Market Intelligence Architecture ADR ✅

Owner:      codex
Phase:      11
Type:       governance
Depends-On: SAS-AUTO-005

Objective: |
  Convert the new product direction into an explicit architecture decision
  before implementation expands. The ADR must decide whether Author Market
  Intelligence activates RAG, Planning, and/or Agentic profiles; choose the
  first local retrieval/runtime substrate; and preserve Phase 10 artifacts as
  the first channel profile rather than replacing them.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/adr/ADR-002-author-market-intelligence.md` exists and records scope, non-goals, runtime tier, capability-profile changes, RAG storage choice, batch-agent boundaries, and rollback plan."
    test: "manual-evidence: ADR exists with required headings."
  - id: AC-2
    description: "`docs/ARCHITECTURE.md` capability-profile table and justifications are updated to match the ADR exactly."
    test: "manual-evidence: Architecture profile statuses match ADR."
  - id: AC-3
    description: "ADR explicitly states that RAG output is context-only and cannot produce final prices, returns, approved records, or outcome metrics."
    test: "manual-evidence: ADR has deterministic-truth boundary."
  - id: AC-4
    description: "ADR cites `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md` and Phase 10 artifacts as the initial corpus/profile seed."
    test: "manual-evidence: roadmap and Phase 10 files are referenced."
  - id: AC-5
    description: "`docs/CODEX_PROMPT.md` is advanced to `SAS-MI-002` only after this ADR and architecture update are complete."
    test: "manual-evidence: Next Task names `SAS-MI-002`."

Context-Refs:
  - docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md
  - docs/pilot/bablos79_AUTHOR_PROFILE.md
  - docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md
  - docs/pilot/AUTO_EXTRACTION_EVAL.md
  - docs/ARCHITECTURE.md
  - docs/DECISION_LOG.md

Files:
  - docs/adr/ADR-002-author-market-intelligence.md
  - docs/ARCHITECTURE.md
  - docs/DECISION_LOG.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task is a gate. Do not implement vector storage, embeddings, market-data
  adapters, or agent loops until the ADR is accepted.

---

### SAS-MI-002: MarketIdea Schema And Metrics Contract ✅

Owner:      codex
Phase:      11
Type:       validation
Depends-On: SAS-MI-001

Objective: |
  Specify the `MarketIdea` record and the deterministic metric contract for
  evaluating author commentary. The schema must cover explicit trade setups,
  soft directional views, market-regime comments, watchlists, catalyst/news
  reactions, risk warnings, and non-market content without overstating evidence.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/specs/MARKET_IDEA_SCHEMA.md` defines required fields, optional fields, enum values, evidence-span rules, approval states, and examples."
    test: "manual-evidence: spec exists with schema table and examples."
  - id: AC-2
    description: "Schema separates explicit trade signals from softer thesis/commentary categories."
    test: "manual-evidence: enum definitions include trade_setup, directional_thesis, market_regime, watchlist, catalyst_reaction, risk_warning, non_market."
  - id: AC-3
    description: "Spec defines deterministic evaluation horizons and labels which fields are human/LLM-assisted drafts only."
    test: "manual-evidence: metric contract section is present."
  - id: AC-4
    description: "Spec defines a review queue policy for ambiguous, high-impact, customer-facing, and unsupported claims."
    test: "manual-evidence: review policy section is present."
  - id: AC-5
    description: "`docs/CODEX_PROMPT.md` is advanced to `SAS-MI-003` only after the schema and metric contract are complete."
    test: "manual-evidence: Next Task names `SAS-MI-003`."

Context-Refs:
  - docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md
  - docs/pilot/METHODOLOGY_V0.md
  - docs/pilot/bablos79_REVIEW_QUEUE.md
  - src/signal_sandbox/ledger/record.py
  - src/signal_sandbox/outcomes/

Files:
  - docs/specs/MARKET_IDEA_SCHEMA.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task is a specification task. Do not add product code yet unless the ADR
  from `SAS-MI-001` explicitly requires a tiny validation fixture.

---

## Phase 12 — Asset Universe And Market-Data Foundation

### SAS-MI-003: Asset Universe And Alias Registry ✅

Owner:      codex
Phase:      12
Type:       validation
Depends-On: SAS-MI-002

Objective: |
  Implement the first canonical asset universe for crypto, funds, equities,
  indices, and unresolved mentions. The registry must resolve aliases from
  author text to canonical asset IDs while preserving uncertainty and evidence.

Acceptance-Criteria:
  - id: AC-1
    description: "`Asset` and `AssetAlias` schemas exist with canonical_id, instrument_type, provider_symbols, aliases, exchange/venue where applicable, and provenance."
    test: "tests/unit/test_asset_registry.py::test_asset_alias_schema_round_trip"
  - id: AC-2
    description: "Alias resolution returns exact, ambiguous, or unresolved with evidence instead of guessing."
    test: "tests/unit/test_asset_registry.py::test_alias_resolution_never_guesses"
  - id: AC-3
    description: "Seed registry covers BTC, ETH, SOL, SPY, QQQ, major crypto tickers observed in the pilot captures, and an unresolved fallback path."
    test: "tests/unit/test_asset_registry.py::test_seed_registry_contains_required_assets"
  - id: AC-4
    description: "No market data is fetched in this task."
    test: "manual-evidence: closeout states no network/data fetch was added."

Files:
  - src/signal_sandbox/assets/
  - tests/unit/test_asset_registry.py
  - docs/specs/ASSET_UNIVERSE.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

### SAS-MI-004: Market Data Store Contract ✅

Owner:      codex
Phase:      12
Type:       validation
Depends-On: SAS-MI-003

Objective: |
  Define and implement the local market-data store interface used by thesis
  evaluation. The store must preserve provider, symbol, time range, resolution,
  checksum, licensing/provenance, and immutable snapshot semantics.

Acceptance-Criteria:
  - id: AC-1
    description: "Market-data store protocol supports write_snapshot, load_snapshot, list_snapshots, and checksum verification."
    test: "tests/unit/test_market_data_store.py::test_snapshot_round_trip_with_checksum"
  - id: AC-2
    description: "Snapshots record provider, canonical asset ID, provider symbol, timeframe, source timestamp range, captured_at, and data_sha256."
    test: "tests/unit/test_market_data_store.py::test_snapshot_metadata_required_fields"
  - id: AC-3
    description: "Attempting to overwrite an existing snapshot with different bytes fails unless a new snapshot ID is used."
    test: "tests/unit/test_market_data_store.py::test_snapshot_overwrite_rejected"
  - id: AC-4
    description: "Store accepts operator-provided local OHLCV fixtures before any new paid or network provider."
    test: "tests/unit/test_market_data_store.py::test_operator_file_fixture_supported"

Files:
  - src/signal_sandbox/market_data/
  - tests/unit/test_market_data_store.py
  - docs/specs/MARKET_DATA_STORE.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

### SAS-MI-005: Deterministic Horizon Metrics ✅

Owner:      codex
Phase:      12
Type:       validation
Depends-On: SAS-MI-004

Objective: |
  Implement deterministic horizon metrics for market ideas without using LLM,
  RAG, or analyst summaries. Metrics must support multiple horizons and record
  unresolved/insufficient-data cases explicitly.

Acceptance-Criteria:
  - id: AC-1
    description: "Horizon evaluator computes 1d, 3d, 7d, and 30d returns from a post timestamp when matching OHLCV exists."
    test: "tests/unit/test_horizon_metrics.py::test_horizon_returns_are_deterministic"
  - id: AC-2
    description: "Evaluator computes max favorable excursion and max adverse excursion over each horizon."
    test: "tests/unit/test_horizon_metrics.py::test_mfe_mae_by_horizon"
  - id: AC-3
    description: "Insufficient data, unresolved asset, and non-directional idea cases return explicit status codes."
    test: "tests/unit/test_horizon_metrics.py::test_unresolved_cases_are_explicit"
  - id: AC-4
    description: "No LLM or retrieval dependency exists in horizon metric code."
    test: "manual-evidence: imports/code review show deterministic-only dependencies."

Files:
  - src/signal_sandbox/market_data/metrics.py
  - tests/unit/test_horizon_metrics.py
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

## Phase 13 — Universal Source Corpus And Channel Profiles

### SAS-MI-006: SourceDocument Corpus Schema ✅

Owner:      codex
Phase:      13
Type:       validation
Depends-On: SAS-MI-005

Objective: |
  Normalize public posts, transcripts, OCR references, images metadata, and
  channel context into a `SourceDocument` corpus schema that downstream
  extraction and retrieval can share.

Acceptance-Criteria:
  - id: AC-1
    description: "`SourceDocument` schema preserves capture_id, source_id, author, timestamp, text, evidence_url, text_sha256, media_refs, transcript_refs, ocr_refs, and metadata."
    test: "tests/unit/test_source_document.py::test_source_document_required_fields"
  - id: AC-2
    description: "Existing `CapturedPost` fixtures convert to `SourceDocument` without losing evidence URL or text hash."
    test: "tests/unit/test_source_document.py::test_captured_post_conversion_preserves_evidence"
  - id: AC-3
    description: "Voice/OCR references are optional evidence links; no transcription/OCR provider is introduced."
    test: "tests/unit/test_source_document.py::test_modal_refs_are_optional"

Files:
  - src/signal_sandbox/corpus/
  - tests/unit/test_source_document.py
  - docs/specs/SOURCE_CORPUS.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

### SAS-MI-007: Channel Profile Registry ✅

Owner:      codex
Phase:      13
Type:       validation
Depends-On: SAS-MI-006

Objective: |
  Convert the Phase 10 `bablos79` author profile into a versioned channel
  profile registry. The registry must allow channel-specific lexicons,
  extraction hints, modality needs, review rules, and parser boundaries.

Acceptance-Criteria:
  - id: AC-1
    description: "Channel profile schema stores channel_id, source URLs, profile version, accepted draft terms, needs-review terms, excluded terms, modality flags, and review rules."
    test: "tests/unit/test_channel_profile.py::test_channel_profile_schema"
  - id: AC-2
    description: "`bablos79` Phase 10 profile imports into registry format with profile_state preserved."
    test: "tests/unit/test_channel_profile.py::test_bablos79_profile_import_preserves_states"
  - id: AC-3
    description: "Unknown channel lookup returns no profile instead of falling back to `bablos79` rules."
    test: "tests/unit/test_channel_profile.py::test_unknown_channel_has_no_default_profile"

Files:
  - src/signal_sandbox/profiles/
  - tests/unit/test_channel_profile.py
  - docs/specs/CHANNEL_PROFILES.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

## Phase 14 — Local RAG Context Layer

### SAS-MI-008: Local Retrieval Store Prototype ✅

Owner:      codex
Phase:      14
Type:       rag:ingestion
Depends-On: SAS-MI-007

Objective: |
  Implement the ADR-approved local retrieval store over `SourceDocument`
  records. The prototype must ingest local corpus fixtures and expose cited
  retrieval results without affecting approved ledgers or deterministic metrics.

Acceptance-Criteria:
  - id: AC-1
    description: "Retrieval store ingests `SourceDocument` fixtures with stable document IDs and embedding/index metadata."
    test: "tests/unit/test_retrieval_store.py::test_ingest_preserves_document_ids"
  - id: AC-2
    description: "Repeated ingestion of the same document is idempotent."
    test: "tests/unit/test_retrieval_store.py::test_ingest_is_idempotent"
  - id: AC-3
    description: "Retrieval metadata records embedding model/provider/version or deterministic test-embedding fixture ID."
    test: "tests/unit/test_retrieval_store.py::test_embedding_metadata_recorded"
  - id: AC-4
    description: "Store code cannot import ledger outcome writers or mutate approved records."
    test: "manual-evidence: dependency check/code review."

Files:
  - src/signal_sandbox/retrieval/
  - tests/unit/test_retrieval_store.py
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

### SAS-MI-009: Cited Retrieval API ✅

Owner:      codex
Phase:      14
Type:       rag:query
Depends-On: SAS-MI-008

Objective: |
  Provide a retrieval API for batch analysis that returns cited corpus snippets,
  scores, document IDs, and filters by author/channel, asset, timestamp window,
  and idea type where metadata exists.

Acceptance-Criteria:
  - id: AC-1
    description: "Query API returns document_id, snippet, score, source timestamp, evidence URL, and text_sha256 for every result."
    test: "tests/unit/test_retrieval_query.py::test_query_results_are_cited"
  - id: AC-2
    description: "Filters for channel_id and timestamp window are deterministic."
    test: "tests/unit/test_retrieval_query.py::test_channel_and_time_filters"
  - id: AC-3
    description: "No result is returned without a traceable source document ID."
    test: "tests/unit/test_retrieval_query.py::test_uncited_results_rejected"

Files:
  - src/signal_sandbox/retrieval/query.py
  - tests/unit/test_retrieval_query.py
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

## Phase 15 — Market Idea Extraction

### SAS-MI-010: MarketIdea Draft Extractor ✅

Owner:      codex
Phase:      15
Type:       extraction
Depends-On: SAS-MI-009

Objective: |
  Implement draft extraction from `SourceDocument` to `MarketIdeaDraft` using
  deterministic rules and channel profiles first. LLM extraction may remain
  behind existing gates, but output must be draft-only.

Acceptance-Criteria:
  - id: AC-1
    description: "Extractor classifies fixtures into trade_setup, directional_thesis, market_regime, watchlist, catalyst_reaction, risk_warning, and non_market."
    test: "tests/unit/test_market_idea_extractor.py::test_market_idea_categories"
  - id: AC-2
    description: "Drafts preserve evidence spans for asset, direction, horizon, risk/invalidation, and catalyst when present."
    test: "tests/unit/test_market_idea_extractor.py::test_evidence_spans_preserved"
  - id: AC-3
    description: "Drafts never become approved records automatically."
    test: "tests/unit/test_market_idea_extractor.py::test_drafts_are_unapproved"

Files:
  - src/signal_sandbox/market_ideas/
  - tests/unit/test_market_idea_extractor.py
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

### SAS-MI-011: MarketIdea Batch Draft Export ✅

Owner:      codex
Phase:      15
Type:       extraction
Depends-On: SAS-MI-010

Objective: |
  Export a batch of `MarketIdeaDraft` rows for a channel slice, including
  parser status, review queue reason, evidence references, candidate assets,
  and suggested evaluation horizons.

Acceptance-Criteria:
  - id: AC-1
    description: "Batch export contains one row per input source document and clearly separates draft status from final review status."
    test: "tests/unit/test_market_idea_export.py::test_batch_export_one_row_per_document"
  - id: AC-2
    description: "Ambiguous assets, customer-facing claims, unsupported directions, and high-impact claims are queued for review."
    test: "tests/unit/test_market_idea_export.py::test_review_queue_policy"
  - id: AC-3
    description: "Export does not write approved ledgers or outcome reports."
    test: "tests/unit/test_market_idea_export.py::test_export_has_no_approved_side_effects"

Files:
  - src/signal_sandbox/market_ideas/export.py
  - tests/unit/test_market_idea_export.py
  - docs/pilot/MARKET_IDEA_DRAFTS_BABLOS79.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

## Phase 16 — Deterministic Thesis Evaluation

### SAS-MI-012: MarketIdea Outcome Evaluator ✅

Owner:      codex
Phase:      16
Type:       validation
Depends-On: SAS-MI-011

Objective: |
  Join reviewed or draft market ideas to canonical assets and market-data
  snapshots, then compute deterministic horizon outcomes while preserving
  unresolved cases.

Acceptance-Criteria:
  - id: AC-1
    description: "Evaluator resolves candidate assets through the asset registry and returns unresolved/ambiguous status without guessing."
    test: "tests/unit/test_market_idea_outcomes.py::test_asset_resolution_statuses"
  - id: AC-2
    description: "Evaluator computes horizon outcomes using the deterministic metrics from `SAS-MI-005`."
    test: "tests/unit/test_market_idea_outcomes.py::test_outcomes_use_horizon_metrics"
  - id: AC-3
    description: "Every outcome records source document ID, market idea ID, asset ID, snapshot ID, and metric version."
    test: "tests/unit/test_market_idea_outcomes.py::test_outcome_provenance_required"

Files:
  - src/signal_sandbox/market_ideas/outcomes.py
  - tests/unit/test_market_idea_outcomes.py
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

### SAS-MI-013: Author Metrics Aggregator ✅

Owner:      codex
Phase:      16
Type:       validation
Depends-On: SAS-MI-012

Objective: |
  Aggregate market idea outcomes into author/channel metrics that distinguish
  coverage, resolvability, directional behavior, risk framing, and null-content
  rates.

Acceptance-Criteria:
  - id: AC-1
    description: "Aggregator computes counts by idea type, asset type, horizon status, and review status."
    test: "tests/unit/test_author_metrics.py::test_counts_by_type_and_status"
  - id: AC-2
    description: "Aggregator computes directional hit rate only for evaluable directional ideas."
    test: "tests/unit/test_author_metrics.py::test_hit_rate_excludes_non_directional"
  - id: AC-3
    description: "Aggregator reports null/unclear/non-market rate separately from failed ideas."
    test: "tests/unit/test_author_metrics.py::test_null_content_rate_separate"

Files:
  - src/signal_sandbox/market_ideas/author_metrics.py
  - tests/unit/test_author_metrics.py
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

## Phase 17 — Bounded Batch Analyst

### SAS-MI-014: Batch Analyst Contract ✅

Owner:      codex
Phase:      17
Type:       agent:loop
Depends-On: SAS-MI-013

Objective: |
  Define and implement a bounded batch analyst contract that can retrieve
  context, inspect deterministic metrics, draft an internal memo, and stop.
  It must not mutate ledgers, fetch undeclared sources, publish reports, or run
  shell/tool actions outside declared application APIs.

Acceptance-Criteria:
  - id: AC-1
    description: "Batch job schema declares input channel/time window, allowed tools, max iterations, max retrieved documents, cost cap, and stop reasons."
    test: "tests/unit/test_batch_analyst_contract.py::test_batch_job_schema"
  - id: AC-2
    description: "Runner stops on max iterations, missing required data, cost cap, or completed memo."
    test: "tests/unit/test_batch_analyst_contract.py::test_runner_stop_reasons"
  - id: AC-3
    description: "Runner audit log records every retrieval, metric read, prompt input checksum, and generated memo checksum."
    test: "tests/unit/test_batch_analyst_contract.py::test_audit_log_records_steps"
  - id: AC-4
    description: "Runner cannot call shell, network collectors, broker APIs, or report publishers."
    test: "manual-evidence: dependency and tool surface review."

Files:
  - src/signal_sandbox/batch_analyst/
  - tests/unit/test_batch_analyst_contract.py
  - docs/specs/BATCH_ANALYST.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

### SAS-MI-015: Internal Analyst Memo Export ✅

Owner:      codex
Phase:      17
Type:       agent:loop
Depends-On: SAS-MI-014

Objective: |
  Export an internal analyst memo that separates deterministic metrics,
  cited evidence, and model/analyst interpretation.

Acceptance-Criteria:
  - id: AC-1
    description: "Memo contains sections for scope, corpus coverage, retrieved evidence, deterministic metrics, interpretation, limitations, and review queue."
    test: "tests/unit/test_analyst_memo_export.py::test_memo_sections"
  - id: AC-2
    description: "Every interpretive claim cites either retrieved source documents or deterministic metric IDs."
    test: "tests/unit/test_analyst_memo_export.py::test_interpretive_claims_are_cited"
  - id: AC-3
    description: "Memo is marked internal and not customer-facing."
    test: "tests/unit/test_analyst_memo_export.py::test_memo_internal_only"

Files:
  - src/signal_sandbox/batch_analyst/memo.py
  - tests/unit/test_analyst_memo_export.py
  - docs/pilot/BABLOS79_INTERNAL_MARKET_MEMO.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

## Phase 18 — Author Market Report V0

### SAS-MI-016: Author Market Report Template ✅

Owner:      codex
Phase:      18
Type:       validation
Depends-On: SAS-MI-015

Objective: |
  Build a customer-facing report template that combines channel profile,
  corpus coverage, thesis categories, deterministic outcome metrics, evidence
  examples, limitations, and non-advice guardrails.

Acceptance-Criteria:
  - id: AC-1
    description: "Report renderer outputs Markdown with channel overview, data coverage, idea taxonomy, deterministic outcomes, evidence examples, limitations, and non-advice disclaimer."
    test: "tests/unit/test_author_market_report.py::test_report_sections"
  - id: AC-2
    description: "Report refuses to render if required provenance for source documents or market snapshots is missing."
    test: "tests/unit/test_author_market_report.py::test_missing_provenance_blocks_report"
  - id: AC-3
    description: "Report separates explicit trade setup performance from broader market commentary behavior."
    test: "tests/unit/test_author_market_report.py::test_trade_and_commentary_metrics_separate"

Files:
  - src/signal_sandbox/reports/author_market.py
  - tests/unit/test_author_market_report.py
  - docs/pilot/reports/bablos79_AUTHOR_MARKET_REPORT_V0.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

### SAS-MI-017: Sellability And Scope Decision Gate ✅

Owner:      codex
Phase:      18
Type:       validation
Depends-On: SAS-MI-016

Objective: |
  Decide whether Author Market Report V0 should be sold, iterated internally,
  narrowed to one vertical, or paused. The decision must cite report quality,
  evidence coverage, customer feedback, and implementation risk.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/AUTHOR_MARKET_REPORT_DECISION.md` records verdict, evidence coverage, customer-feedback status, payment-signal status, and next action."
    test: "manual-evidence: decision artifact exists with required fields."
  - id: AC-2
    description: "If next work is approved, it names the exact bottleneck and forbids private scraping, live trading, broker integration, and public leaderboard expansion."
    test: "manual-evidence: next-scope section is present."
  - id: AC-3
    description: "Phase 18 deep review/archive/doc update is completed before Phase 19 begins."
    test: "manual-evidence: archive and audit index updated."

Files:
  - docs/pilot/AUTHOR_MARKET_REPORT_DECISION.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

---

## Phase 19 — Channel-Specific Modalities And Tools

### SAS-MI-018: Modality And Tooling Scope ADR ✅

Owner:      codex
Phase:      19
Type:       governance
Depends-On: SAS-MI-017

Objective: |
  Decide which channel-specific tools are justified by evidence: voice
  transcription, OCR/image annotation, news/catalyst linker, fund/equity data,
  reviewer UI/export improvements, or new channel lexicons.

Acceptance-Criteria:
  - id: AC-1
    description: "ADR lists candidate tools, measured channel/profile bottleneck, expected user value, cost/risk, and chosen next task."
    test: "manual-evidence: ADR exists with candidate table."
  - id: AC-2
    description: "No modality provider or external service is added in this ADR task."
    test: "manual-evidence: closeout states no provider dependency was added."
  - id: AC-3
    description: "Chosen next tool has a narrow acceptance-tested task before implementation."
    test: "manual-evidence: docs/tasks.md contains the selected follow-up task."

Files:
  - docs/adr/ADR-003-channel-specific-tools.md
  - docs/tasks.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Phase 19 is intentionally open-ended. Each tool must earn its way in through
  channel evidence and customer value, not through generic feature expansion.

---

### SAS-MI-019: Reviewer Coverage Export Pack ✅

Owner:      codex
Phase:      19
Type:       validation
Depends-On: SAS-MI-018

Objective: |
  Build the deterministic reviewer/export pack selected by ADR-003. The pack
  must show which `bablos79` source documents are ready for a customer sample,
  which are missing cited MarketIdea evidence, which are missing deterministic
  metric/outcome coverage, and which require human interpretation review.

Acceptance-Criteria:
  - id: AC-1
    description: "Exporter produces one deterministic row per SourceDocument with source_document_id, capture_id, source timestamp, MarketIdea/review status, evidence refs, deterministic metric/outcome status, missing fields, and reviewer_action."
    test: "tests/unit/test_review_coverage_export.py::test_export_rows_are_complete_and_deterministically_sorted"
  - id: AC-2
    description: "Exporter separates status buckets for needs_evidence_review, needs_metric_snapshot, needs_interpretation_review, and ready_for_customer_sample without writing approved ledger rows, reports, market data, or external provider calls."
    test: "tests/unit/test_review_coverage_export.py::test_status_buckets_do_not_mutate_truth_artifacts"
  - id: AC-3
    description: "`docs/pilot/bablos79_REVIEW_COVERAGE_PACK.md` records coverage for the 60 public captures and keeps reviewer_id pending for rows that are not customer-ready."
    test: "manual-evidence: coverage artifact exists with summary counts and no customer-facing claims."

Files:
  - src/signal_sandbox/market_ideas/review_coverage.py
  - tests/unit/test_review_coverage_export.py
  - docs/pilot/bablos79_REVIEW_COVERAGE_PACK.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This task is a deterministic local export improvement only. It must not add
  modality providers, external services, private scraping, broker integration,
  report publication, public leaderboard behavior, marketplace behavior, or
  forward-looking claims.

---

## Phase 20 — Telegram Media Evidence: Voice And Image/OCR Drafts

### SAS-MEDIA-001: Media Scope ADR And Legal Addendum ✅

Owner:      codex
Phase:      20
Type:       governance
Depends-On: SAS-MI-019

Objective: |
  Authorize the exact media evidence posture before any media provider code
  lands. The ADR must decide allowed Telegram media sources, operator-forwarded
  vs public-channel capture rules, raw media retention, transcript/OCR draft
  status, managed Whisper posture, OCR/image analysis posture, cost/approval
  gates, and rollback.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/adr/ADR-004-media-evidence-pipeline.md` exists and references the Dream_Motif_Interpreter voice pattern files used as implementation guidance."
    test: "manual-evidence: ADR includes reference section with file paths."
  - id: AC-2
    description: "`docs/legal_risk_memo.md` is updated with explicit voice/audio/image/OCR posture, allowed public/operator-forwarded media capture, forbidden private/authenticated sources, raw-media retention, and deletion triggers."
    test: "manual-evidence: legal memo §Media Evidence is present."
  - id: AC-3
    description: "ADR keeps runtime T0 and states that transcript/OCR outputs are draft evidence only, review-required, and cannot write approved ledger rows or customer-facing claims."
    test: "manual-evidence: ADR boundary section present."

Files:
  - docs/adr/ADR-004-media-evidence-pipeline.md
  - docs/legal_risk_memo.md
  - docs/pilot/MEDIA_MODALITY_DEVELOPMENT_PLAN.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Use Dream_Motif_Interpreter as a pattern reference for Telegram voice
  download, acknowledgement, transcription worker, and cleanup. Do not copy its
  domain model, database schema, or assistant behavior.

---

### SAS-MEDIA-002: MediaArtifact Schema And Manifest ✅

Owner:      codex
Phase:      20
Type:       validation
Depends-On: SAS-MEDIA-001

Objective: |
  Add a deterministic local schema for media artifacts linked to captures and
  source documents. The schema must represent voice/audio/images without adding
  Telegram, Whisper, OCR, or provider calls.

Acceptance-Criteria:
  - id: AC-1
    description: "`MediaArtifact` records media_id, source_id, capture_id, source_document_id, modality, original_url_or_file_id, local_path, media_sha256, mime_type, duration_seconds or image dimensions when available, retention_state, created_at_utc, and draft refs."
    test: "tests/unit/test_media_artifact.py::test_media_artifact_schema_requires_provenance"
  - id: AC-2
    description: "Manifest export writes deterministic Markdown/JSON rows sorted by source timestamp, source_document_id, and media_id."
    test: "tests/unit/test_media_artifact.py::test_media_manifest_is_deterministically_sorted"
  - id: AC-3
    description: "Schema rejects artifacts without capture/source linkage or checksum and does not create transcript/OCR/provider outputs."
    test: "tests/unit/test_media_artifact.py::test_media_artifact_rejects_unlinked_or_unhashed_media"

Files:
  - src/signal_sandbox/media/artifact.py
  - src/signal_sandbox/media/__init__.py
  - tests/unit/test_media_artifact.py
  - docs/specs/MEDIA_ARTIFACTS.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This is metadata only. Raw media files remain local operator-controlled
  inputs. No provider dependency is added in this task.

---

### SAS-MEDIA-003: Telegram Voice Acquisition Adapter ✅

Owner:      codex
Phase:      20
Type:       validation
Depends-On: SAS-MEDIA-002

Objective: |
  Adapt the proven Telegram voice download pattern for operator-authorized
  public evidence. The adapter downloads Telegram voice media to local
  temporary storage, records a `MediaArtifact`, and stops. It does not
  transcribe audio.

Acceptance-Criteria:
  - id: AC-1
    description: "Adapter accepts an injected Telegram client with `get_file(file_id)` and downloads voice `.ogg` to configured local media dir with deterministic event metadata and SHA-256."
    test: "tests/unit/test_telegram_voice_acquisition.py::test_downloads_voice_with_injected_client"
  - id: AC-2
    description: "Adapter rejects missing source/capture linkage, non-public or non-operator-authorized media, and missing legal media authorization."
    test: "tests/unit/test_telegram_voice_acquisition.py::test_rejects_unauthorized_or_unlinked_voice"
  - id: AC-3
    description: "Download failures return typed errors and do not persist partial artifacts."
    test: "tests/unit/test_telegram_voice_acquisition.py::test_download_failure_has_no_partial_artifact"

Files:
  - src/signal_sandbox/media/telegram_voice.py
  - tests/unit/test_telegram_voice_acquisition.py
  - docs/specs/MEDIA_ARTIFACTS.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Reference Dream_Motif_Interpreter `app/telegram/voice.py` and
  `app/telegram/handlers.py` for lifecycle shape. CI must use fake clients; no
  real Telegram network call is allowed in tests.

---

### SAS-MEDIA-004: Whisper Transcript Draft Adapter ✅

Owner:      codex
Phase:      20
Type:       validation
Depends-On: SAS-MEDIA-003

Objective: |
  Add a gated transcription adapter for local voice artifacts using managed
  Whisper-style transcription through an injected client. Transcripts are draft
  evidence only and must require human review before downstream use.

Acceptance-Criteria:
  - id: AC-1
    description: "Adapter requires both environment enablement and per-run approval before invoking the transcription client; disabled runs return an explicit skipped status."
    test: "tests/unit/test_whisper_transcript_adapter.py::test_double_gate_required"
  - id: AC-2
    description: "Successful transcription writes a draft transcript artifact with media_id, transcript_id, provider/model, transcript_sha256, source media checksum, status=draft_pending_review, and reviewer_id=pending."
    test: "tests/unit/test_whisper_transcript_adapter.py::test_transcript_preserves_media_provenance"
  - id: AC-3
    description: "Provider failure records a typed failure status, does not create an approved transcript, and leaves raw media cleanup decision to the retention policy."
    test: "tests/unit/test_whisper_transcript_adapter.py::test_provider_failure_is_not_truth"
  - id: AC-4
    description: "Successful transcription deletes or marks raw audio according to ADR-004 retention policy and logs no raw transcript text in logger extras."
    test: "tests/unit/test_whisper_transcript_adapter.py::test_success_follows_retention_and_logging_policy"

Files:
  - src/signal_sandbox/media/transcription.py
  - tests/unit/test_whisper_transcript_adapter.py
  - docs/specs/MEDIA_ARTIFACTS.md
  - docs/audit/MEDIA_EVAL.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Reference Dream_Motif_Interpreter `app/workers/transcribe.py` for provider
  boundary and cleanup thinking. Do not route transcripts directly to reports
  or approved MarketIdea rows.

---

### SAS-MEDIA-005: Image Evidence Inventory And OCR Scope ✅

Owner:      codex
Phase:      20
Type:       governance
Depends-On: SAS-MEDIA-002

Objective: |
  Inventory image/screenshot evidence needs for `bablos79` before implementing
  OCR or image annotation. Decide whether text OCR is enough or chart/image
  annotation is required.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_MEDIA_INVENTORY.md` lists known media gaps by source/capture, modality, blocker type, expected evidence value, and whether OCR/transcription/manual review is needed."
    test: "manual-evidence: inventory artifact exists with required columns."
  - id: AC-2
    description: "Inventory separates image text OCR from chart interpretation and forbids chart-derived trading claims without human review."
    test: "manual-evidence: inventory has OCR vs image-annotation decision section."
  - id: AC-3
    description: "If OCR is approved, the next OCR task has acceptance tests and does not add public report claims."
    test: "manual-evidence: docs/tasks.md OCR follow-up remains scoped."

Files:
  - docs/pilot/bablos79_MEDIA_INVENTORY.md
  - docs/tasks.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  This is a gate task. It may approve OCR draft extraction, but not autonomous
  chart interpretation or customer-facing claims.

---

### SAS-MEDIA-006: OCR Draft Adapter ✅

Owner:      codex
Phase:      20
Type:       validation
Depends-On: SAS-MEDIA-005

Objective: |
  Add review-required OCR draft extraction for local image artifacts when
  Phase 20 inventory shows image text blocks report coverage. OCR output is
  draft evidence only.

Acceptance-Criteria:
  - id: AC-1
    description: "Adapter accepts local image `MediaArtifact` rows and an injected OCR client; CI uses fake OCR client and no network/provider call."
    test: "tests/unit/test_ocr_draft_adapter.py::test_ocr_uses_injected_client"
  - id: AC-2
    description: "OCR output records media_id, ocr_id, provider/model, text_sha256, source media checksum, bounding metadata when available, status=draft_pending_review, and reviewer_id=pending."
    test: "tests/unit/test_ocr_draft_adapter.py::test_ocr_preserves_media_provenance"
  - id: AC-3
    description: "Adapter refuses chart interpretation labels, price levels, or trade claims unless they are stored as review-required notes, not approved truth."
    test: "tests/unit/test_ocr_draft_adapter.py::test_chart_claims_are_review_required"

Files:
  - src/signal_sandbox/media/ocr.py
  - tests/unit/test_ocr_draft_adapter.py
  - docs/specs/MEDIA_ARTIFACTS.md
  - docs/audit/MEDIA_EVAL.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Do not add OCR output to customer-facing reports until a later review task
  marks evidence as ready.

---

### SAS-MEDIA-007: Multimodal SourceDocument Join ✅

Owner:      codex
Phase:      20
Type:       validation
Depends-On: SAS-MEDIA-004, SAS-MEDIA-006

Objective: |
  Link reviewed or draft transcript/OCR artifacts into `SourceDocument`
  references and retrieval context without rewriting original capture text or
  hashes.

Acceptance-Criteria:
  - id: AC-1
    description: "Join helper returns enriched SourceDocument copies with transcript_refs and ocr_refs populated from media artifacts while preserving original text, evidence_url, and text_sha256 byte-identically."
    test: "tests/unit/test_multimodal_source_join.py::test_join_preserves_original_source_document"
  - id: AC-2
    description: "Join helper rejects transcript/OCR artifacts whose source media checksum or capture linkage does not match the SourceDocument."
    test: "tests/unit/test_multimodal_source_join.py::test_join_rejects_mismatched_media_refs"
  - id: AC-3
    description: "Retrieval context may cite transcript/OCR refs but cannot mutate approved MarketIdea rows, outcomes, or reports."
    test: "tests/unit/test_multimodal_source_join.py::test_join_has_no_truth_artifact_side_effects"

Files:
  - src/signal_sandbox/media/source_join.py
  - tests/unit/test_multimodal_source_join.py
  - docs/specs/SOURCE_CORPUS.md
  - docs/specs/MEDIA_ARTIFACTS.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Original text captures remain canonical. Media-derived text is additional
  draft evidence with separate provenance.

---

### SAS-MEDIA-008: Multimodal Coverage Pack And Decision Gate ✅

Owner:      codex
Phase:      20
Type:       validation
Depends-On: SAS-MEDIA-007

Objective: |
  Extend reviewer coverage to show text, transcript, and OCR readiness, then
  decide whether multimodal evidence now justifies a customer sample report.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_MULTIMODAL_COVERAGE_PACK.md` records text/transcript/OCR coverage counts, review-required rows, ready-for-customer-sample rows, and missing evidence reasons."
    test: "manual-evidence: multimodal coverage artifact exists with required sections."
  - id: AC-2
    description: "`docs/pilot/MEDIA_MODALITY_DECISION.md` decides continue/iterate/pause and cites media coverage, transcript/OCR quality, customer value, cost/risk, and next action."
    test: "manual-evidence: decision artifact exists with required fields."
  - id: AC-3
    description: "Phase 20 deep review/archive/doc update is completed before any Phase 21 task begins."
    test: "manual-evidence: archive and audit index updated."

Files:
  - docs/pilot/bablos79_MULTIMODAL_COVERAGE_PACK.md
  - docs/pilot/MEDIA_MODALITY_DECISION.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Customer-facing report use remains blocked unless the decision records
  reviewed evidence coverage and human approval.

---

## Phase 21 — Artifact-First Real Public-Source Report Validation

Phase 21 is the active artifact-first task graph opened after the 2026-05-11
operator decision. Warm demand/pre-order interest is assumed. The phase goal is
to produce one real public-source report artifact, manually validate the
evidence, and decide whether Signal Analytics Sandbox is ready for controlled
external pilot conversations.

Phase boundary:

- Phase 20 media tooling remains internal-only until real operator-authorized
  media exists and human review marks transcript/OCR evidence usable.
- Do not add marketplace, leaderboard, paid X/Twitter dependency, private
  scraping, or customer-facing media-backed claims in Phase 21.
- If no source/channel is selected, stop at SAS-AF-001 with a clear
  operator-input blocker.

### SAS-AF-001: Channel And Report Scope Lock ✅

Owner:      operator + codex
Phase:      21
Type:       validation
Depends-On: SAS-MEDIA-008
Status:     complete

Objective: |
  Define the first real Signal report before adding more automation: source,
  period, capture method, report type, language, outcome horizon, legal/public
  boundary, and allowed claim types.

Acceptance-Criteria:
  - id: AC-1
    description: "A scope note records source URL, period, public-only status, capture method, report type, language, and whether media is in scope."
    test: "manual-evidence: scope note exists."
  - id: AC-2
    description: "The scope note defines allowed claim types and explicitly blocks advice, future-profit, private-source, and unreviewed-media claims."
    test: "manual-evidence: claim boundary section exists."
  - id: AC-3
    description: "The note states whether existing bablos79 captures are sufficient or a fresh capture is required."
    test: "manual-evidence: source selection decision exists."

Files:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#3-phase-sas-af-0---channel-and-report-scope-lock
  - ../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md#phase-0---scope-lock-and-evidence-rules
  - docs/legal_risk_memo.md

Notes: |
  This task may be blocked on operator source selection. Do not substitute a new
  source without human approval.

### SAS-AF-002: Public Capture Pack ✅

Owner:      codex
Phase:      21
Type:       validation
Depends-On: SAS-AF-001
Status:     complete

Objective: |
  Build or register a traceable public-source capture pack for the selected
  source and period, including manifests, source refs, capture logs, and media
  inventory where applicable.

Acceptance-Criteria:
  - id: AC-1
    description: "Every report-eligible source item has source URL/ref, timestamp, source label, capture method, and provenance metadata."
    test: "manual-evidence or existing capture/source corpus tests."
  - id: AC-2
    description: "Capture manifest or source corpus preview is inspectable by the operator outside code."
    test: "manual-evidence: capture pack review."
  - id: AC-3
    description: "Missing captures, incomplete media, or capture limitations are recorded before extraction/reporting."
    test: "manual-evidence: limitations note exists."

Files:
  - src/signal_sandbox/capture/
  - src/signal_sandbox/sources/
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#4-phase-sas-af-1---public-capture-pack
  - docs/specs/SOURCE_CORPUS.md
  - docs/specs/MEDIA_ARTIFACTS.md

Notes: |
  Public-only posture is mandatory. If legal/terms coverage is unclear, block
  and update the legal/risk memo before capture expansion.

### SAS-AF-003: Human Review Queue Closure ✅

Owner:      operator + codex
Phase:      21
Type:       validation
Depends-On: SAS-AF-002
Status:     complete

Objective: |
  Convert draft extraction into reviewed evidence by closing the review queue
  for the selected source: approved, ambiguous, not market-related,
  insufficient evidence, duplicate, or needs media review.

Acceptance-Criteria:
  - id: AC-1
    description: "Reviewed export separates approved rows from ambiguous, rejected, duplicate, and media-needed rows."
    test: "manual-evidence: reviewed export exists."
  - id: AC-2
    description: "Customer-facing findings are based only on reviewed/approved rows; draft rows remain labeled draft."
    test: "manual-evidence: report-input review."
  - id: AC-3
    description: "Each approved row has source refs and enough evidence for the selected report type."
    test: "manual-evidence: row sample review."

Files:
  - src/signal_sandbox/extraction/
  - src/signal_sandbox/reports/
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#5-phase-sas-af-2---human-review-queue-closure
  - docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md

Notes: |
  Do not let an LLM silently decide truth. Human review remains part of the
  product promise for this phase.

### SAS-AF-004: Market Data Snapshot And Outcome Prep ✅

Owner:      codex
Phase:      21
Type:       validation
Depends-On: SAS-AF-003
Status:     complete

Objective: |
  Prepare outcome analysis only for reviewed rows with enough evidence:
  asset mapping, timestamp alignment, local market-data snapshot, horizons,
  and unresolved outcome register.

Acceptance-Criteria:
  - id: AC-1
    description: "Approved rows with measurable outcomes have asset mapping, event timestamp, direction/thesis where applicable, and horizon definition."
    test: "manual-evidence or existing outcome tests."
  - id: AC-2
    description: "Rows lacking asset, price, direction, or timestamp certainty are moved to an unresolved outcome register."
    test: "manual-evidence: unresolved register exists."
  - id: AC-3
    description: "Outcome language separates measured historical outcome from author behavior and does not imply future performance."
    test: "manual-evidence: claim-safety review."

Files:
  - src/signal_sandbox/prices/
  - src/signal_sandbox/outcomes/
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#6-phase-sas-af-3---market-data-snapshot-and-outcome-prep

Notes: |
  Missing market data is a limitation, not a reason to invent metrics.

### SAS-AF-005: First Real Source Report V1 ✅

Owner:      codex
Phase:      21
Type:       validation
Depends-On: SAS-AF-004
Status:     complete

Objective: |
  Generate the first complete real public-source report artifact from reviewed
  evidence, source coverage, outcome summaries where supported, limitations,
  and no-advice/no-future-performance boundaries.

Acceptance-Criteria:
  - id: AC-1
    description: "Report includes executive summary, source/period, corpus coverage, reviewed row counts, strongest findings, ambiguous/insufficient evidence counts, supported outcome metrics, limitations, and evidence appendix."
    test: "manual-evidence: report review."
  - id: AC-2
    description: "Every material claim links to reviewed evidence or is explicitly marked as a limitation."
    test: "manual-evidence: evidence trace review."
  - id: AC-3
    description: "Unreviewed media, transcript, OCR, or draft extraction output does not appear as customer-facing proof."
    test: "manual-evidence: media/draft boundary review."

Files:
  - src/signal_sandbox/reports/
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#7-phase-sas-af-4---first-real-source-report-v1

Notes: |
  If the selected source cannot support a meaningful report, produce a reject
  decision rather than a weak report.

### SAS-LIVE-001: Real Media Scope And Evidence Intake ✅

Owner:      operator + codex
Phase:      21
Type:       validation
Depends-On: SAS-AF-005
Status:     complete

Objective: |
  Convert the text-only report result into a real multimodal evidence intake
  plan. Select exact public/operator-authorized media items, link each item to
  source/capture/source-document IDs, and define the report question each media
  item is supposed to answer.

Acceptance-Criteria:
  - id: AC-1
    description: "A media intake plan lists every target voice/audio/image/screenshot item with source URL/ref, source/capture/source-document linkage, modality, public/operator authorization state, and expected report value."
    test: "manual-evidence: docs/pilot/bablos79_REAL_MEDIA_INTAKE.md exists with required columns."
  - id: AC-2
    description: "The plan explicitly excludes private, paywalled, login-walled, unlinked, or access-bypass media and records blockers for missing items."
    test: "manual-evidence: exclusion/blocker section exists."
  - id: AC-3
    description: "The plan maps media items to current report gaps: ambiguous rows, insufficient evidence rows, missing context, screenshot-only text, or voice-context gaps."
    test: "manual-evidence: every selected item has a report-gap field."

Files:
  - docs/pilot/bablos79_REAL_MEDIA_INTAKE.md
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-0---real-media-scope-and-evidence-intake
  - docs/pilot/bablos79_MEDIA_INVENTORY.md
  - docs/pilot/bablos79_OUTCOME_PREP.md
  - docs/legal_risk_memo.md#media-evidence

Notes: |
  Do not proceed to media acquisition until this plan names concrete public or
  operator-authorized media evidence. Channel-level "there is audio/images" is
  not enough.
  Completed intake result: no acquisition-ready media item exists yet. The
  plan records source-linked candidate blockers for `bablos79-10486` and
  `bablos79-10465`, excludes unlinked channel-level media, and blocks
  `SAS-LIVE-002` until the operator supplies exact public/operator-authorized
  media URL/file ID/local file rows with source/capture/source-document linkage.

### SAS-LIVE-002: Public Media Artifact Acquisition ✅

Owner:      codex
Phase:      21
Type:       validation
Depends-On: SAS-LIVE-001
Status:     complete

Objective: |
  Materialize approved media intake rows as local MediaArtifact metadata and
  local operator-controlled files where applicable. The task records what was
  successfully acquired, skipped, or blocked.

Acceptance-Criteria:
  - id: AC-1
    description: "Every acquired media item has a MediaArtifact row with media_id, source_id, capture_id, source_document_id, source timestamp, modality, original URL/file ID, local path, SHA-256, MIME type, retention state, and created_at_utc."
    test: "manual-evidence plus existing media artifact tests."
  - id: AC-2
    description: "Acquisition uses only public/operator-authorized inputs and records no private/authenticated collection path."
    test: "manual-evidence: acquisition log states authorization per item."
  - id: AC-3
    description: "Failed, missing, unlinked, or unauthorized media items are recorded with blocker reason and are not silently dropped."
    test: "manual-evidence: acquisition log has failed/blocked rows where applicable."

Files:
  - src/signal_sandbox/media/
  - docs/pilot/bablos79_REAL_MEDIA_ACQUISITION.md
  - docs/pilot/bablos79_MEDIA_MANIFEST.json
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-1---public-media-artifact-acquisition
  - docs/specs/MEDIA_ARTIFACTS.md
  - docs/adr/ADR-004-media-evidence-pipeline.md

Notes: |
  CI must use fake clients or local fixtures. Real network/provider use is an
  operator run, not a unit test. No transcription/OCR is performed in this task.
  Completed acquisition result: public `/s/` HTML yielded two concrete voice
  posts, `bablos79-10476` and `bablos79-10478`, acquired to
  `workspace/media/bablos79/` and registered in
  `docs/pilot/bablos79_MEDIA_MANIFEST.json`. `bablos79-10465` remains blocked
  because the promised follow-up video is not identified.

### SAS-LIVE-003: Voice Transcript Draft Run ✅

Owner:      codex
Phase:      21
Type:       validation
Depends-On: SAS-LIVE-002
Status:     complete

Objective: |
  Run the gated transcription path on acquired voice/audio artifacts and record
  draft transcript artifacts with provenance, provider/model metadata, checksum,
  review-required status, and retention action.

Acceptance-Criteria:
  - id: AC-1
    description: "Every attempted voice/audio item records transcript_id or skipped/provider_failed status, media_id, provider/model, transcript_sha256 when present, source media checksum, reviewer_id=pending, and review_required=true."
    test: "manual-evidence: transcript run log exists; unit tests for transcription adapter pass."
  - id: AC-2
    description: "Transcripts remain draft_pending_review and are not routed to approved MarketIdea rows, ledgers, outcomes, reports, or customer-facing claims."
    test: "manual-evidence: boundary section plus no approved output paths."
  - id: AC-3
    description: "Raw media retention/deletion action is recorded per ADR-004."
    test: "manual-evidence: retention action column populated."

Files:
  - src/signal_sandbox/media/transcription.py
  - docs/pilot/bablos79_TRANSCRIPT_RUN.md
  - docs/audit/MEDIA_EVAL.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-2---voice-transcript-draft-run
  - docs/specs/MEDIA_ARTIFACTS.md#whisper-transcript-drafts

Notes: |
  Managed transcription requires explicit enablement and per-run approval.
  Completed run result: two acquired public voice rows were attempted and both
  were recorded as `skipped_provider_not_configured`; no transcript text was
  invented, no draft transcript artifact was created, and raw media remained
  `retained_by_policy`.

### SAS-LIVE-004: Image OCR Draft Run ✅

Owner:      codex
Phase:      21
Type:       validation
Depends-On: SAS-LIVE-002
Status:     complete

Objective: |
  Run review-required OCR on acquired image/screenshot artifacts. Capture text
  and bounding metadata where available, while keeping chart interpretation and
  trading claims out of automated output.

Acceptance-Criteria:
  - id: AC-1
    description: "Every attempted image/screenshot item records OCR id or skipped/provider_failed status, media_id, provider/model, text_sha256 when present, source media checksum, reviewer_id=pending, and review_required=true."
    test: "manual-evidence: OCR run log exists; unit tests for OCR adapter pass."
  - id: AC-2
    description: "OCR output stores text only; chart labels/levels/trade interpretation remain review_required_notes and are not approved truth."
    test: "manual-evidence: chart-claim boundary section exists."
  - id: AC-3
    description: "OCR artifacts are linked back to source/capture/source-document IDs through MediaArtifact refs."
    test: "manual-evidence: every OCR row has linkage fields."

Files:
  - src/signal_sandbox/media/ocr.py
  - docs/pilot/bablos79_OCR_RUN.md
  - docs/audit/MEDIA_EVAL.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-3---image-ocr-draft-run
  - docs/specs/MEDIA_ARTIFACTS.md#ocr-drafts

Notes: |
  Do not implement autonomous chart interpretation in this task.
  Completed run result: no image/screenshot media artifacts were acquired, so
  the OCR run recorded two voice rows as `skipped_non_image_media`, created no
  OCR artifacts, and preserved the chart-claim boundary.

### SAS-LIVE-005: Human Media Evidence Review ✅

Owner:      operator + codex
Phase:      21
Type:       validation
Depends-On: SAS-LIVE-003, SAS-LIVE-004
Status:     complete

Objective: |
  Review transcript/OCR outputs against the original public media and mark each
  artifact usable, unusable, needs rework, or outside report scope before it can
  influence extraction, outcomes, or report wording.

Acceptance-Criteria:
  - id: AC-1
    description: "Review notes sample every transcript/OCR artifact and record usable/unusable/needs_rework/out_of_scope, reviewer_id, reviewed_at_utc, and issue notes."
    test: "manual-evidence: docs/pilot/bablos79_MEDIA_REVIEW.md exists."
  - id: AC-2
    description: "Artifacts with transcription/OCR errors, unclear speaker/image context, missing linkage, or chart interpretation risk are blocked from report claims."
    test: "manual-evidence: blocked artifact section exists."
  - id: AC-3
    description: "Only human-reviewed usable transcript/OCR refs are allowed into source-document joins for report context."
    test: "manual-evidence: usable refs list exists."

Files:
  - docs/pilot/bablos79_MEDIA_REVIEW.md
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-4---human-media-evidence-review
  - docs/legal_risk_memo.md#media-evidence

Notes: |
  This is the mandatory human gate before media can affect customer-visible
  report claims.
  Completed gate result: no transcript/OCR artifacts existed to review, so
  usable transcript refs and OCR refs are both zero. Raw voice media is blocked
  from report claims until a future transcript run and human review produce
  usable refs.

### SAS-LIVE-006: Reviewed Multimodal Source Join ✅

Owner:      codex
Phase:      21
Type:       rag:ingestion
Depends-On: SAS-LIVE-005
Status:     complete

Objective: |
  Join only reviewed-usable transcript/OCR refs into SourceDocument copies and
  produce a multimodal corpus preview that preserves original text, evidence
  URL, and text hash byte-identically.

Acceptance-Criteria:
  - id: AC-1
    description: "Multimodal SourceDocument preview includes only reviewed-usable media refs and preserves original capture text, evidence_url, and text_sha256."
    test: "tests/unit/test_multimodal_source_join.py plus manual preview."
  - id: AC-2
    description: "Mismatched media checksum, source ID, capture ID, source-document ID, transcript ref, or OCR ref is rejected."
    test: "existing join tests or added coverage."
  - id: AC-3
    description: "Preview records text-only, transcript, and OCR coverage counts and explicitly labels draft/reviewed evidence status."
    test: "manual-evidence: multimodal corpus preview exists."

Files:
  - src/signal_sandbox/media/source_join.py
  - docs/pilot/bablos79_MULTIMODAL_SOURCE_PREVIEW.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-5---reviewed-multimodal-source-join
  - docs/specs/SOURCE_CORPUS.md#multimodal-joins

Notes: |
  This task carries a RAG ingestion tag because it changes source-corpus context
  available to retrieval/report workflows. It does not approve truth artifacts.
  Completed join result: no reviewed-usable transcript/OCR refs existed, so the
  preview preserves all 60 text-only source documents and joins zero
  media-derived refs. Retrieval/source context semantics remain text-only.

### SAS-LIVE-007: Multimodal Extraction And Review Queue ✅

Owner:      operator + codex
Phase:      21
Type:       validation
Depends-On: SAS-LIVE-006
Status:     complete

Objective: |
  Re-run extraction/review over text plus reviewed transcript/OCR context,
  separating approved report candidates from ambiguous, insufficient, duplicate,
  not-market-related, media-needed, and media-blocked rows.

Acceptance-Criteria:
  - id: AC-1
    description: "Multimodal review export includes source refs, media refs where used, evidence spans, reviewed status, missing fields, and reviewer action for every row."
    test: "manual-evidence: multimodal review queue exists."
  - id: AC-2
    description: "Rows that depend on transcript/OCR cite only reviewed-usable media artifacts."
    test: "manual-evidence: media-backed rows cite reviewed artifact IDs."
  - id: AC-3
    description: "Draft LLM/parser output is never treated as final truth without operator final evaluation."
    test: "manual-evidence: final review status separated from draft status."

Files:
  - src/signal_sandbox/extraction/
  - src/signal_sandbox/market_ideas/
  - docs/pilot/bablos79_MULTIMODAL_REVIEW_QUEUE.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-6---multimodal-extraction-and-review-queue
  - docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.md

Notes: |
  If no media-backed row becomes report-eligible, preserve that as the result
  instead of forcing a metric.
  Completed queue result: no reviewed usable transcript/OCR refs exist, so the
  multimodal review queue has 0 media-backed report-eligible rows and carries
  forward the text-only queue counts.

### SAS-LIVE-008: Multimodal Outcome Prep ✅

Owner:      codex
Phase:      21
Type:       validation
Depends-On: SAS-LIVE-007
Status:     complete

Objective: |
  Prepare deterministic outcomes only for final reviewed multimodal rows with
  complete asset, timestamp, direction/thesis, horizon, and evidence support.
  Record every unresolved row before report generation.

Acceptance-Criteria:
  - id: AC-1
    description: "Every measurable row has asset mapping, source timestamp, direction/thesis where applicable, horizon, evidence refs, and market-data snapshot requirement."
    test: "manual-evidence or existing outcome tests."
  - id: AC-2
    description: "Rows lacking complete measurable fields are moved to an unresolved register with reason."
    test: "manual-evidence: multimodal unresolved outcome register exists."
  - id: AC-3
    description: "Market-data fetches happen only for measurable rows; unresolved rows do not trigger price snapshots."
    test: "manual-evidence: snapshot/fetch count matches measurable rows."

Files:
  - src/signal_sandbox/prices/
  - src/signal_sandbox/outcomes/
  - docs/pilot/bablos79_MULTIMODAL_OUTCOME_PREP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-7---multimodal-outcome-prep
  - docs/pilot/bablos79_OUTCOME_PREP.md

Notes: |
  Missing media/market data is a limitation. Do not infer outcomes from media
  context alone.
  Completed prep result: 0 media-backed measurable rows, 0 market-data fetches,
  and 0 outcome metrics.

### SAS-LIVE-009: Media-Backed Report V1 ✅

Owner:      codex
Phase:      21
Type:       validation
Depends-On: SAS-LIVE-008
Status:     complete

Objective: |
  Generate a revised report artifact that includes text, reviewed media
  evidence, outcome summaries where supported, limitations, and clear
  no-advice/no-future-performance boundaries.

Acceptance-Criteria:
  - id: AC-1
    description: "Report includes source/period, text/media coverage, reviewed row counts, media-backed evidence summary, outcome metrics only where supported, unresolved register summary, limitations, and evidence appendix."
    test: "manual-evidence: media-backed report exists."
  - id: AC-2
    description: "Every media-backed claim cites reviewed transcript/OCR/media artifact refs and source refs."
    test: "manual-evidence: evidence trace review."
  - id: AC-3
    description: "Report contains no unreviewed media claims, chart-derived automated claims, advice, future-profit claims, marketplace ranking, or leaderboard language."
    test: "manual-evidence: claim-safety review."

Files:
  - src/signal_sandbox/reports/
  - docs/pilot/reports/bablos79_MEDIA_BACKED_REPORT_V1.md
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-8---media-backed-report-v1
  - docs/pilot/reports/bablos79_SIGNAL_REPORT_V1.md

Notes: |
  If real media still does not create a useful report, produce a reject or
  limitation report instead of decorating weak evidence.
  Completed report result: reject/limitation report, not external-delivery
  ready, with no media-backed claims.

### SAS-AF-006: Manual Validity Review ✅

Owner:      operator + codex
Phase:      21
Type:       validation
Depends-On: SAS-LIVE-009
Status:     complete

Objective: |
  Manually verify sampled included, ambiguous, excluded, media-backed, and
  strongest-finding rows before external delivery.

Acceptance-Criteria:
  - id: AC-1
    description: "Manual review samples included rows, ambiguous rows, excluded rows, strongest findings, and all media-backed rows if media is used."
    test: "manual-evidence: validity notes list reviewed rows."
  - id: AC-2
    description: "Review checks source URL, timestamp/timezone, asset mapping, direction/thesis, outcome window, metric horizon, and report wording."
    test: "manual-evidence: checklist completed."
  - id: AC-3
    description: "Error register blocks external delivery for unresolved P0/P1 evidence or claim-safety issues."
    test: "manual-evidence: error register exists."

Files:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - docs/audit/

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#8-phase-sas-af-5---manual-validity-review
  - docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md#phase-9---manual-validity-review-and-delivery-gate

Notes: |
  Ambiguous content should stay ambiguous. Do not force a confident finding for
  presentation quality.
  Completed validity result: external delivery blocked by open Phase 21 error
  register items.

### SAS-AF-007: Report Polish And Internal Demo Pack ✅

Owner:      codex
Phase:      21
Type:       docs
Depends-On: SAS-AF-006
Status:     complete

Objective: |
  Package the validated source report as an internal demo/research product pack
  for warm conversations.

Acceptance-Criteria:
  - id: AC-1
    description: "Demo pack contains report, source manifest, reviewed extraction sample, outcome summary if valid, validation summary, limitations, talk track, and safe excerpts."
    test: "manual-evidence: demo pack review."
  - id: AC-2
    description: "The first page makes the buyer use case clear without implying advice, ranking marketplace, or future profitability."
    test: "manual-evidence: operator readability review."
  - id: AC-3
    description: "External-safe excerpts do not expose data outside public-source/legal boundaries."
    test: "manual-evidence: privacy/legal review."

Files:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md
  - docs/pilot/
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#9-phase-sas-af-6---report-polish-and-internal-demo-pack

Notes: |
  This task packages a report product, not a source leaderboard or SaaS.
  Completed pack result: internal-only reject-case demo pack; not buyer-ready.

### SAS-AF-008: External Pilot Ready Gate ✅

Owner:      operator + codex
Phase:      21
Type:       review
Depends-On: SAS-AF-007
Status:     complete

Objective: |
  Decide whether the Signal report artifact is ready for controlled external
  pilot use and record the paid research/report package scope.

Acceptance-Criteria:
  - id: AC-1
    description: "Ready-gate review states ready / needs fixes / reject source and cites evidence quality, legal boundary, unresolved findings, and claim safety."
    test: "manual-evidence: ready-gate review exists."
  - id: AC-2
    description: "Paid pilot package records source input, deliverables, turnaround, pricing hypothesis, and feedback questions."
    test: "manual-evidence: paid pilot package section exists."
  - id: AC-3
    description: "CODEX prompt, README, implementation journal, and audit index reflect the Phase 21 decision and next task."
    test: "manual/docs-review."

Files:
  - docs/archive/PHASE21_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - docs/IMPLEMENTATION_JOURNAL.md
  - README.md

Context-Refs:
  - docs/ARTIFACT_VALIDATION_ROADMAP.md#10-phase-sas-af-7---controlled-external-pilot-ready-gate
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is the gate for showing a bounded source research artifact to warm
  prospects. It does not approve marketplace, leaderboard, or automated advice.

## Phase 22 — Expanded Public Corpus

### SAS-DR-001: Deep Retrospective Scope Lock ✅

Owner:      operator + codex
Phase:      22
Type:       docs
Depends-On: SAS-AF-008

Objective: |
  Lock the expanded `bablos79` source/window scope and anti-cherry-pick rules
  before any new capture, media review, or market-outcome analysis starts.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_DEEP_SCOPE.md` records source URL, source ID, window length, inclusion/exclusion rules, capture method, media posture, report language, and claim boundary."
    test: "manual/docs-review"
  - id: AC-2
    description: "Scope explicitly fixes the window before market-outcome analysis to avoid selecting only good-looking posts."
    test: "manual/docs-review"
  - id: AC-3
    description: "Scope states that Phase 21 rejected external delivery for the narrow window but did not reject the channel as a whole."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_DEEP_SCOPE.md
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md
  - docs/DECISION_LOG.md
  - docs/IMPLEMENTATION_JOURNAL.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-22---expanded-public-corpus
  - docs/pilot/bablos79_EXTERNAL_PILOT_READY_GATE.md
  - docs/audit/PHASE21_ERROR_REGISTER.md

Notes: |
  Public/operator-authorized sources only. Do not use private Telegram groups.

### SAS-DR-002: Expanded Public Capture Manifest ✅

Owner:      codex
Phase:      22
Type:       validation
Depends-On: SAS-DR-001

Objective: |
  Capture or register the expanded public corpus and produce a stable manifest
  that preserves source ids, timestamps, source URLs, hashes, and media refs.

Acceptance-Criteria:
  - id: AC-1
    description: "Expanded manifest records every included public text capture with stable capture/document ids, timestamps, source URL, text hash, and source language."
    test: "manual-evidence plus existing capture validation tests where applicable"
  - id: AC-2
    description: "Manifest records excluded rows or capture gaps with reason instead of silently dropping them."
    test: "manual/docs-review"
  - id: AC-3
    description: "`docs/pilot/bablos79_EXPANDED_CAPTURE_PACK.md` summarizes corpus size, window, capture method, and coverage limitations."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_EXPANDED_CAPTURE_MANIFEST.json
  - docs/pilot/bablos79_EXPANDED_CAPTURE_PACK.md
  - workspace/captures/bablos79/
  - src/signal_sandbox/capture/

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-22---expanded-public-corpus

Notes: |
  If fresh network capture is not available in the environment, create the
  manifest from operator-supplied public captures and record the gap.

### SAS-DR-003: Expanded Media Inventory ✅

Owner:      codex
Phase:      22
Type:       validation
Depends-On: SAS-DR-002

Objective: |
  Build the media inventory for the expanded corpus, separating public,
  acquisition-ready, missing, excluded, and unsupported media items.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md` lists image/screenshot/chart/voice/video references by source document id and acquisition status."
    test: "manual/docs-review"
  - id: AC-2
    description: "Every media item has public/operator-authorization status or is excluded before OCR/transcription work."
    test: "manual/docs-review"
  - id: AC-3
    description: "Inventory flags likely chart/screenshot/image rows for Phase 23 OCR and manual review."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md
  - docs/pilot/bablos79_EXPANDED_CAPTURE_MANIFEST.json
  - docs/legal_risk_memo.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-22---expanded-public-corpus

Notes: |
  Do not claim image analysis yet. This task only inventories media.

### SAS-DR-004: Corpus Gap Register ✅

Owner:      codex
Phase:      22
Type:       docs
Depends-On: SAS-DR-003

Objective: |
  Record corpus completeness gaps before extraction so later report conclusions
  can explain missing evidence instead of hiding it.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_CORPUS_GAP_REGISTER.md` lists missing periods, inaccessible media, unsupported media types, timestamp ambiguities, and legal/source limitations."
    test: "manual/docs-review"
  - id: AC-2
    description: "Gap register marks each gap as blocking, acceptable limitation, or needs operator input."
    test: "manual/docs-review"
  - id: AC-3
    description: "No extraction or outcome task treats a known gap as evidence of author quality."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_CORPUS_GAP_REGISTER.md
  - docs/pilot/bablos79_EXPANDED_CAPTURE_PACK.md
  - docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-22---expanded-public-corpus

Notes: |
  A gap can be acceptable if it is disclosed.

### SAS-DR-005: Expanded Corpus Deep Review ✅

Owner:      codex
Phase:      22
Type:       review
Depends-On: SAS-DR-001, SAS-DR-002, SAS-DR-003, SAS-DR-004

Objective: |
  Run the Phase 22 boundary review and decide whether the expanded corpus is
  safe and complete enough for multimodal evidence work.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks anti-cherry-pick scope, public-source legality, capture integrity, media inventory, gap register, and no private scraping."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, handoff docs, and phase report are updated with final Phase 22 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any P0/P1 source legality, private scraping, or manifest integrity issue blocks Phase 23."
    test: "manual/review"

Files:
  - docs/archive/PHASE22_REVIEW.md
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md
  - ORCHESTRATOR_CHECKPOINT.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

---

## Phase 39 — Telegram Trader Intelligence Productization

### SAS-TTI-001: Product Frame And Buyer Promise

Owner:      codex
Phase:      39
Type:       docs
Depends-On: SAS-DR-022

Objective: |
  Reframe the sandbox as a buyer-readable Telegram Trader Intelligence product:
  source hygiene, claim quality, narrative drift, risk-signal behavior, and
  evidence-backed examples.

Acceptance-Criteria:
  - id: AC-1
    description: "Product docs define the buyer promise without prediction, leaderboard, investment advice, or best-channel claims."
    test: "manual/docs-review"
  - id: AC-2
    description: "The report surface separates evidence, interpretation, limitations, and operator verdict."
    test: "manual/docs-review"
  - id: AC-3
    description: "Boundaries prohibit private Telegram scraping, paid API dependency before demand, and automated trading decisions."
    test: "manual/docs-review"

Files:
  - docs/TELEGRAM_TRADER_INTELLIGENCE.md
  - README.md
  - docs/CODEX_PROMPT.md

### SAS-TTI-002: Signal Analysis Receipt Schema

Owner:      codex
Phase:      39
Type:       implementation
Depends-On: SAS-TTI-001

Objective: |
  Define a machine-readable `signal_analysis_receipt` that records source
  hashes, extracted claims, reviewer status, market-data references,
  limitations, and report verdict.

Acceptance-Criteria:
  - id: AC-1
    description: "Receipt schema records source ids, capture hashes, claim ids, extraction method, reviewer status, outcome references, and limitations."
    test: "unit/schema"
  - id: AC-2
    description: "A fixture receipt can be validated and rejected when required evidence fields are missing."
    test: "unit/schema"
  - id: AC-3
    description: "Receipt language avoids future-performance and advice claims."
    test: "unit/schema"

Files:
  - src/signal_sandbox/receipts.py
  - tests/unit/test_signal_analysis_receipt.py
  - docs/TELEGRAM_TRADER_INTELLIGENCE.md

### SAS-TTI-003: Referee Verdict Pack

Owner:      codex
Phase:      39
Type:       implementation
Depends-On: SAS-TTI-002

Objective: |
  Add a deterministic or human-reviewed referee verdict artifact that accepts,
  rejects, or marks as insufficient each report claim and lens output.

Acceptance-Criteria:
  - id: AC-1
    description: "Referee verdict schema supports accepted, rejected, insufficient, and needs-human-review states."
    test: "unit/schema"
  - id: AC-2
    description: "Verdicts link to receipt ids and source evidence instead of trusting generated prose."
    test: "unit/schema"
  - id: AC-3
    description: "Report generation can include referee verdict summaries."
    test: "integration/report"

Files:
  - src/signal_sandbox/referee.py
  - tests/unit/test_referee_verdict.py
  - tests/integration/test_referee_report_summary.py

### SAS-TTI-004: Diverse Analytical Lens Report Pack

Owner:      codex
Phase:      39
Type:       product
Depends-On: SAS-TTI-003

Objective: |
  Adapt the useful Gensyn-inspired pattern: generate several bounded analytical
  lenses, preserve their evidence, and let the referee verdict decide what is
  reportable.

Acceptance-Criteria:
  - id: AC-1
    description: "At least three lens types are defined, for example claim precision, narrative drift, risk posture, or source reliability."
    test: "manual/docs-review"
  - id: AC-2
    description: "Each lens output must cite receipt evidence and cannot become report text unless accepted or human-approved."
    test: "manual/docs-review"
  - id: AC-3
    description: "The pack states that distributed training, token incentives, and autonomous swarms are explicitly out of scope."
    test: "manual/docs-review"

Files:
  - docs/TELEGRAM_TRADER_INTELLIGENCE.md
  - docs/pilot/reports/

### SAS-TTI-005: Productization Readiness Review

Owner:      codex + operator
Phase:      39
Type:       review
Depends-On: SAS-TTI-004

Objective: |
  Decide whether Telegram Trader Intelligence is ready for a buyer demo,
  concierge pilot, or another evidence-hardening loop.

Acceptance-Criteria:
  - id: AC-1
    description: "Review records buyer-demo readiness, evidence gaps, legal boundaries, product promise, and resume/stop criteria."
    test: "manual/review"
  - id: AC-2
    description: "State docs point to the next task and do not open marketplace, leaderboard, advice, or private scraping scope."
    test: "manual/docs-review"
  - id: AC-3
    description: "The review includes cost/friction notes for manual, semi-automated, and automated report production."
    test: "manual/review"

Files:
  - docs/audit/TELEGRAM_TRADER_INTELLIGENCE_READINESS_REVIEW.md
  - docs/CODEX_PROMPT.md
  - README.md

---

## Phase 36 — Channel Impact Framework And Cross-Channel Completion

### SAS-IMPACT-001: Impact Rubric And Truth Model ✅

Owner:      codex + operator
Phase:      36
Type:       docs
Depends-On: SAS-NEXT-032

Objective: |
  Define the source-of-truth model and broad channel impact rubric used by the
  future dashboard and paid deep report. The rubric must include PnL-like
  signal performance, trend sense, insight depth, trading methodology, risk
  management, practical usefulness, creativity/differentiation, and evidence
  confidence.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/specs/CHANNEL_IMPACT_FRAMEWORK.md` defines author-statement truth, interpretation truth, market-outcome truth, and product-conclusion truth."
    test: "tests/unit/test_channel_impact_framework.py::test_impact_framework_defines_truth_layers"
  - id: AC-2
    description: "The framework lists non-PnL dimensions: trend sense, insight depth, methodology, risk management, practical usefulness, creativity, and evidence confidence."
    test: "tests/unit/test_channel_impact_framework.py::test_impact_framework_lists_non_pnl_dimensions"
  - id: AC-3
    description: "The framework separates dashboard fields from paid deep report content and blocks leaderboard/advice/future-profit framing."
    test: "tests/unit/test_channel_impact_framework.py::test_impact_framework_defines_dashboard_and_paid_report_boundary"

Files:
  - docs/specs/CHANNEL_IMPACT_FRAMEWORK.md
  - docs/tasks.md
  - docs/AI_DEVELOPMENT_PLAN_RU.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md
  - ORCHESTRATOR_CHECKPOINT.md
  - MEMORY.md
  - tests/unit/test_channel_impact_framework.py

Context-Refs:
  - docs/specs/CHANNEL_UTILITY_EVALUATION.md
  - docs/specs/CHANNEL_QUANT_METRICS_V2.md
  - docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md

Notes: |
  This task expands evaluation criteria. It does not change existing V1 metrics
  or approve external delivery.

### SAS-IMPACT-002: Cross-Channel Development Loop ✅

Owner:      codex + operator
Phase:      36
Type:       docs
Depends-On: SAS-IMPACT-001

Objective: |
  Turn the impact framework into a repeated development loop for `bablos79`,
  `nemphiscrypts`, and `pifagortrade`: source coverage, multimodal intake,
  claim normalization, truth mapping, impact scoring, and cross-channel
  comparison.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md` lists the same loop steps for all three channels."
    test: "tests/unit/test_channel_impact_framework.py::test_cross_channel_loop_covers_three_channels"
  - id: AC-2
    description: "The loop states dashboard output and paid deep report output separately."
    test: "tests/unit/test_channel_impact_framework.py::test_cross_channel_loop_separates_dashboard_and_paid_report"

Files:
  - docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md

### SAS-BABLOS-001: bablos79 Corpus Completion Scope And Gap Plan ✅

Owner:      codex + operator
Phase:      36
Type:       docs
Depends-On: SAS-IMPACT-002

Objective: |
  Apply the Phase 36 cross-channel loop to `bablos79` first. The task must make
  clear that the existing 90-day window is not fully captured, images/OCR did
  not run, audio is internal-only, and the small number of strict signals is an
  evidence-quality result rather than a product bug.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md` records the current text/audio/image coverage counts and explains why the current corpus cannot support a long-period multimodal author conclusion."
    test: "tests/unit/test_bablos79_phase36_scope.py::test_phase36_scope_records_current_bablos_limitations"
  - id: AC-2
    description: "The phase defines tasks for text recapture, media linkage, transcript acceptance, OCR/vision draft pass, claim recompute, proxy/outcome recompute, and external gate rerun."
    test: "tests/unit/test_bablos79_phase36_scope.py::test_phase36_scope_lists_recovery_tasks"
  - id: AC-3
    description: "The phase states that OCR/vision and transcript output are draft/internal until human/operator accepted."
    test: "tests/unit/test_bablos79_phase36_scope.py::test_phase36_scope_preserves_media_guardrails"

Files:
  - docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md
  - docs/tasks.md
  - docs/AI_DEVELOPMENT_PLAN_RU.md
  - docs/CODEX_PROMPT.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md
  - ORCHESTRATOR_CHECKPOINT.md
  - MEMORY.md
  - tests/unit/test_bablos79_phase36_scope.py

Context-Refs:
  - docs/pilot/bablos79_EXPANDED_CAPTURE_PACK.md
  - docs/pilot/bablos79_CORPUS_GAP_REGISTER.md
  - docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md
  - docs/pilot/bablos79_OCR_RUN_EXPANDED.md
  - docs/pilot/bablos79_TRANSCRIPT_LLM_REVIEW.md

Notes: |
  This task starts the per-channel `bablos79` recovery path but does not run public recapture, OCR,
  transcription, market-data fetch, or outcome recompute.

### SAS-BABLOS-002: Public Text Recapture Plan ✅

Owner:      codex + operator
Phase:      36
Type:       docs
Depends-On: SAS-BABLOS-001

Objective: |
  Plan the public Telegram `/s/` recapture for missing `bablos79` periods and
  missing message IDs without private scraping or guessing unavailable rows.

Acceptance-Criteria:
  - id: AC-1
    description: "The plan enumerates pre-seed and post-seed windows, missing IDs, capture method, and unavailable/deleted/media-only classification rules."
    test: "manual/docs-review"
  - id: AC-2
    description: "The plan states that absent rows are neither positive nor negative author evidence."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_PHASE36_TEXT_RECAPTURE_PLAN.md

Notes: |
  This task creates the plan only. It does not run public network recapture.

### SAS-BABLOS-003: Media Linkage Queue ✅

Owner:      codex + operator
Phase:      36
Type:       docs
Depends-On: SAS-BABLOS-002

Objective: |
  Build a queue for image/chart/audio candidates that records exact source
  URL, capture ID, source document ID, media file/checksum, and blocker status.

Acceptance-Criteria:
  - id: AC-1
    description: "Every image/chart/audio candidate has a source-linked artifact or explicit blocker."
    test: "tests/unit/test_bablos79_phase36_media_linkage_queue.py::test_phase36_media_linkage_queue_counts_and_gate"
  - id: AC-2
    description: "Chart rows require manual interpretation review before claim use."
    test: "tests/unit/test_bablos79_phase36_media_linkage_queue.py::test_phase36_media_linkage_queue_preserves_review_policy"

Files:
  - docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.md
  - docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.json
  - tests/unit/test_bablos79_phase36_media_linkage_queue.py

Notes: |
  Completed queue result: 8 candidates, 2 source-linked audio rows ready for
  transcript acceptance, 0 OCR-ready image/chart rows, and 0 customer-facing
  media claims allowed until review gates pass.

### SAS-BABLOS-004: Transcript Acceptance Pass ✅

Owner:      operator
Phase:      36
Type:       review
Depends-On: SAS-BABLOS-003

Objective: |
  Accept/reject/needs_context each transcript before it can create
  customer-facing claims.

Acceptance-Criteria:
  - id: AC-1
    description: "Each transcript ref has human/operator status and reason."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_transcript_acceptance_excludes_unaccepted_media"
  - id: AC-2
    description: "Rejected or needs_context transcript claims remain excluded from customer-facing metrics."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_transcript_acceptance_excludes_unaccepted_media"

Files:
  - docs/pilot/bablos79_PHASE36_TRANSCRIPT_ACCEPTANCE.md
  - docs/pilot/bablos79_PHASE36_TRANSCRIPT_ACCEPTANCE.json

Notes: |
  Completed with both transcript refs marked `needs_context`, not
  human/operator accepted. No transcript-backed customer-facing claims are
  allowed.

### SAS-BABLOS-005: OCR/Vision Draft Pass ✅

Owner:      codex + operator
Phase:      36
Type:       validation
Depends-On: SAS-BABLOS-003

Objective: |
  Run OCR/vision only on source-linked image/chart artifacts and keep output as
  draft evidence pending human/operator review.

Acceptance-Criteria:
  - id: AC-1
    description: "OCR artifacts record source linkage, checksum, provider/model, confidence/limitations, and draft status."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_ocr_drafts_are_blocked_without_source_linkage"
  - id: AC-2
    description: "No chart interpretation claim is approved without manual review."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_ocr_drafts_are_blocked_without_source_linkage"

Files:
  - docs/pilot/bablos79_PHASE36_OCR_DRAFTS.md
  - docs/pilot/bablos79_PHASE36_OCR_DRAFTS.json

Notes: |
  Completed as a blocked OCR pass: 0 source-linked image/chart artifacts,
  0 OCR drafts, 0 chart interpretations approved.

### SAS-BABLOS-006: Multimodal Claim Recompute ✅

Owner:      codex
Phase:      36
Type:       validation
Depends-On: SAS-BABLOS-004, SAS-BABLOS-005

Objective: |
  Recompute the `bablos79` claim ledger using text plus accepted transcript and
  accepted OCR evidence.

Acceptance-Criteria:
  - id: AC-1
    description: "The recomputed ledger separates text, accepted transcript, accepted OCR, rejected media, and blockers."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_claim_ledger_has_no_new_accepted_media_claims"
  - id: AC-2
    description: "Every deterministic candidate has asset, direction, horizon, and review state or explicit blocker."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_claim_ledger_has_no_new_accepted_media_claims"

Files:
  - docs/pilot/bablos79_PHASE36_CLAIM_LEDGER.md
  - docs/pilot/bablos79_PHASE36_CLAIM_LEDGER.json

Notes: |
  Completed with 0 accepted transcript claims, 0 accepted OCR claims, and
  0 deterministic outcome-ready rows.

### SAS-BABLOS-007: Proxy And Outcome Recompute ✅

Owner:      codex + operator
Phase:      36
Type:       validation
Depends-On: SAS-BABLOS-006

Objective: |
  Recompute market outcomes only for deterministic rows with approved
  provider/proxy mapping.

Acceptance-Criteria:
  - id: AC-1
    description: "Provider gaps are exclusions, not losses."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_outcomes_and_gate_reject_external_delivery"
  - id: AC-2
    description: "Outcome artifacts include source refs, provider refs, horizon, metric, and unsupported-row counts."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_outcomes_and_gate_reject_external_delivery"

Files:
  - docs/pilot/bablos79_PHASE36_OUTCOMES.md
  - docs/pilot/bablos79_PHASE36_OUTCOMES.json

Notes: |
  Completed with no market fetch and 0 computed outcomes. Unsupported rows and
  provider/proxy gaps remain exclusions, not losses.

### SAS-BABLOS-008: Phase 36 External Gate ✅

Owner:      operator + codex
Phase:      36
Type:       review
Depends-On: SAS-BABLOS-007

Objective: |
  Decide whether the completed `bablos79` retrospective is external-ready,
  internal-only, or still rejected.

Acceptance-Criteria:
  - id: AC-1
    description: "Gate records external-ready / internal-only / rejected with blockers, evidence coverage, media status, and no-advice boundary."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_outcomes_and_gate_reject_external_delivery"
  - id: AC-2
    description: "Gate does not approve external delivery if media review, provider coverage, or deterministic outcome quality remains insufficient."
    test: "tests/unit/test_bablos79_phase36_completion.py::test_phase36_outcomes_and_gate_reject_external_delivery"

Files:
  - docs/pilot/bablos79_PHASE36_EXTERNAL_READY_GATE.md
  - docs/archive/PHASE36_BABLOS79_DEEP_REVIEW.md

Notes: |
  Deep review completed for the `bablos79` Phase 36 pass. External delivery
  remains rejected/internal-only.

### SAS-IMPACT-003: nemphiscrypts Corpus Completion Scope ✅

Owner:      codex + operator
Phase:      36
Type:       docs
Depends-On: SAS-IMPACT-002

Objective: |
  Create the same corpus/media completion scope for `nemphiscrypts` that exists
  for `bablos79`, including text coverage, audio/image/chart status, claim
  count, provider gaps, and stop conditions.

Acceptance-Criteria:
  - id: AC-1
    description: "The scope records source coverage, media status, missing periods/IDs, and next capture/review steps."
    test: "tests/unit/test_phase36_other_channel_scopes.py::test_nemphiscrypts_phase36_scope_records_coverage_media_and_next_steps"
  - id: AC-2
    description: "The scope uses the same truth and impact dimensions defined in `CHANNEL_IMPACT_FRAMEWORK.md`."
    test: "tests/unit/test_phase36_other_channel_scopes.py::test_other_channel_scopes_use_same_impact_and_truth_model"

Files:
  - docs/pilot/nemphiscrypts_PHASE36_CORPUS_COMPLETION_SCOPE.md

### SAS-IMPACT-004: pifagortrade Corpus Completion Scope ✅

Owner:      codex + operator
Phase:      36
Type:       docs
Depends-On: SAS-IMPACT-002

Objective: |
  Create the same corpus/media completion scope for `pifagortrade`, including
  text coverage, audio/image/chart status, claim count, provider gaps, and stop
  conditions.

Acceptance-Criteria:
  - id: AC-1
    description: "The scope records source coverage, media status, missing periods/IDs, and next capture/review steps."
    test: "tests/unit/test_phase36_other_channel_scopes.py::test_pifagortrade_phase36_scope_records_coverage_media_and_next_steps"
  - id: AC-2
    description: "The scope uses the same truth and impact dimensions defined in `CHANNEL_IMPACT_FRAMEWORK.md`."
    test: "tests/unit/test_phase36_other_channel_scopes.py::test_other_channel_scopes_use_same_impact_and_truth_model"

Files:
  - docs/pilot/pifagortrade_PHASE36_CORPUS_COMPLETION_SCOPE.md

### SAS-IMPACT-005: Impact Claim Taxonomy Expansion ✅

Owner:      codex
Phase:      36
Type:       validation
Depends-On: SAS-IMPACT-001, SAS-BABLOS-006, SAS-IMPACT-003, SAS-IMPACT-004

Objective: |
  Expand normalized claim/idea taxonomy so trend sense, insight depth,
  methodology, risk management, practical usefulness, and creativity can be
  reviewed as first-class evidence, not forced into PnL-only signal rows.

Acceptance-Criteria:
  - id: AC-1
    description: "Taxonomy distinguishes explicit trade setup, trend/regime view, macro thesis, risk/process statement, watchlist, and non-market commentary."
    test: "tests/unit/test_phase36_final_impact_artifacts.py::test_impact_claim_taxonomy_distinguishes_pnl_and_non_pnl_claims"
  - id: AC-2
    description: "Non-PnL claims have review/evidence/confidence fields and cannot become win/loss rows without deterministic market mapping."
    test: "tests/unit/test_phase36_final_impact_artifacts.py::test_impact_claim_taxonomy_distinguishes_pnl_and_non_pnl_claims"

Files:
  - docs/specs/CHANNEL_IMPACT_CLAIM_TAXONOMY.md

### SAS-IMPACT-006: Dashboard Score Schema ✅

Owner:      codex + operator
Phase:      36
Type:       validation
Depends-On: SAS-IMPACT-005

Objective: |
  Define the dashboard-ready dataset and score schema for compact channel
  comparison with confidence labels and no universal leaderboard.

Acceptance-Criteria:
  - id: AC-1
    description: "Schema includes signal performance, trend sense, insight depth, methodology clarity, risk discipline, practical usefulness, creativity, evidence confidence, sample size, and external gate."
    test: "tests/unit/test_phase36_final_impact_artifacts.py::test_dashboard_schema_and_paid_boundary_preserve_product_guardrails"
  - id: AC-2
    description: "Schema forbids best-channel, future-profit, and investment-advice language."
    test: "tests/unit/test_phase36_final_impact_artifacts.py::test_dashboard_schema_and_paid_boundary_preserve_product_guardrails"

Files:
  - docs/specs/CHANNEL_DASHBOARD_SCORE_SCHEMA.md

### SAS-IMPACT-007: Paid Deep Report Boundary ✅

Owner:      codex + operator
Phase:      36
Type:       docs
Depends-On: SAS-IMPACT-006

Objective: |
  Define what stays in the paid deep report versus what can safely appear in a
  public/free dashboard.

Acceptance-Criteria:
  - id: AC-1
    description: "Boundary separates compact public metrics from paid evidence appendix, examples, counterexamples, methodology/risk notes, and source limitations."
    test: "tests/unit/test_phase36_final_impact_artifacts.py::test_dashboard_schema_and_paid_boundary_preserve_product_guardrails"
  - id: AC-2
    description: "Boundary preserves no-advice, no-future-profit, no-private-source, and external-gate rules."
    test: "tests/unit/test_phase36_final_impact_artifacts.py::test_dashboard_schema_and_paid_boundary_preserve_product_guardrails"

Files:
  - docs/specs/PAID_CHANNEL_REPORT_BOUNDARY.md

### SAS-IMPACT-008: Cross-Channel Impact Recompute And Gate ✅

Owner:      codex + operator
Phase:      36
Type:       review
Depends-On: SAS-BABLOS-008, SAS-IMPACT-003, SAS-IMPACT-004, SAS-IMPACT-006, SAS-IMPACT-007

Objective: |
  Recompute cross-channel comparison using the impact framework and decide what
  is dashboard-safe, paid-report-only, internal-only, or blocked.

Acceptance-Criteria:
  - id: AC-1
    description: "Comparison includes all three channels and uses confidence/sample-size caveats."
    test: "tests/unit/test_phase36_final_impact_artifacts.py::test_phase36_scorecard_and_gate_are_internal_only_and_three_channel"
  - id: AC-2
    description: "Gate explicitly decides dashboard-safe fields, paid-report-only fields, internal-only fields, and blocked claims."
    test: "tests/unit/test_phase36_final_impact_artifacts.py::test_phase36_scorecard_and_gate_are_internal_only_and_three_channel"

Files:
  - docs/pilot/three_channel_PHASE36_IMPACT_SCORECARD.md
  - docs/pilot/three_channel_PHASE36_EXTERNAL_READY_GATE.md
  - docs/archive/PHASE36_DEEP_REVIEW.md

## Phase 37 — Pre-Client Artifact Hardening

Goal: produce reliable internal artifacts for a future free dashboard and paid
deep reports before any client outreach, paid report sale, private-channel
analysis, partnership discussion, or public ranking. This phase is explicitly
pre-client: it can use public/operator-authorized sources, existing model
reviewer outputs, deterministic market APIs, and internal review gates, but it
must not claim customer validation or external approval.

### SAS-PRECLIENT-001: Product Artifact Contract And Reliability Bar ✅

Owner:      codex + operator
Phase:      37
Type:       docs
Depends-On: SAS-IMPACT-008

Objective: |
  Define the exact artifacts needed before client outreach: free source card,
  paid deep report, evidence appendix, human/model review ledger, outcome
  snapshot, safety gate, and demo pack. The contract must separate internal,
  dashboard-safe, paid-report-only, and blocked content.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md` lists every required artifact, owner, input dependencies, allowed audience, and reliability status enum."
    test: "tests/unit/test_preclient_task_graph.py::test_preclient_phase_lists_reliable_artifact_contract"
  - id: AC-2
    description: "Contract defines reliability levels `draft`, `model_reviewed`, `operator_reviewed`, `market_validated`, `dashboard_safe`, `paid_report_safe`, and `blocked`."
    test: "tests/unit/test_preclient_task_graph.py::test_preclient_phase_lists_reliable_artifact_contract"
  - id: AC-3
    description: "Contract states that model reviewers do not replace human/operator acceptance for customer-facing media claims."
    test: "tests/unit/test_preclient_task_graph.py::test_preclient_phase_preserves_customer_safety_gates"

Files:
  - docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md
  - docs/tasks.md
  - docs/AI_DEVELOPMENT_PLAN_RU.md
  - docs/CODEX_PROMPT.md
  - AGENT_NOTES.md
  - PHASE_HANDOFF.md
  - tests/unit/test_preclient_task_graph.py

Context-Refs:
  - docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md
  - docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md
  - docs/specs/CHANNEL_DASHBOARD_SCORE_SCHEMA.md
  - docs/specs/PAID_CHANNEL_REPORT_BOUNDARY.md

Notes: |
  Completed on 2026-05-23. The contract defines artifact inventory,
  reliability statuses, audience classes, artifact gates, dashboard/free card
  fields, paid report boundaries, done criteria, and explicit non-goals. It
  does not create customer-facing claims, sales copy, client promises,
  private-source workflows, or rankings.

### SAS-PRECLIENT-002: Model-Reviewed Candidate Review Packet ✅

Owner:      codex
Phase:      37
Type:       validation
Depends-On: SAS-PRECLIENT-001

Objective: |
  Convert media reviewer outputs into a compact operator review packet for all
  model-accepted and high-signal rows. The packet must include source URL,
  media ref, transcript/OCR text, model reviewer decision, arbiter decision,
  extracted setup fields, blocker reason, and recommended human action.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/preclient_MODEL_REVIEW_PACKET.md` and `.json` include all 9 arbiter-accepted internal candidates plus any mass-review accepted rows."
    test: "tests/unit/test_preclient_model_review_packet.py"
  - id: AC-2
    description: "Every packet row has source link, media_ref_id, modality, model decisions, evidence types, setup/RR fields when present, and `required_operator_action`."
    test: "tests/unit/test_preclient_model_review_packet.py"
  - id: AC-3
    description: "No packet row is marked customer-facing; all rows remain pending human/operator review or blocked."
    test: "tests/unit/test_preclient_model_review_packet.py"

Files:
  - docs/pilot/preclient_MODEL_REVIEW_PACKET.md
  - docs/pilot/preclient_MODEL_REVIEW_PACKET.json
  - docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json
  - docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json
  - tests/unit/test_preclient_model_review_packet.py

Context-Refs:
  - docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md

Notes: |
  Completed on 2026-05-23. The packet includes 9 unique rows: all 9
  arbiter-accepted candidates and the overlapping mass-review accepted row.
  Channel split is `bablos79` 1, `nemphiscrypts` 1, `pifagortrade` 7. All rows
  are `model_reviewed`, blocked from customer-facing metrics, and assigned a
  required operator action.

### SAS-PRECLIENT-003: Evidence Appendix Builder ✅

Owner:      codex
Phase:      37
Type:       code
Depends-On: SAS-PRECLIENT-002

Objective: |
  Build a deterministic evidence appendix artifact that joins source posts,
  media manifest rows, transcript/OCR drafts, model-review decisions,
  structured RR fields, market outcome references, and blockers into one
  reproducible appendix per channel.

Acceptance-Criteria:
  - id: AC-1
    description: "Appendix JSON and Markdown exist for all three channels and each row has source URL, evidence kind, artifact refs, checksum or text hash, review status, market-provider status, and blocker list."
    test: "tests/unit/test_preclient_evidence_appendix.py"
  - id: AC-2
    description: "Appendix distinguishes text-only claims, media-backed claims, post-factum rows, context-only rows, rejected noise, and provider gaps."
    test: "tests/unit/test_preclient_evidence_appendix.py"
  - id: AC-3
    description: "Appendix does not include raw media bytes and does not require private/authenticated source access."
    test: "tests/unit/test_preclient_evidence_appendix.py"

Files:
  - src/signal_sandbox/reports/evidence_appendix.py
  - docs/pilot/preclient_EVIDENCE_APPENDIX.json
  - docs/pilot/preclient_EVIDENCE_APPENDIX.md
  - tests/unit/test_preclient_evidence_appendix.py

Context-Refs:
  - docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json
  - docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json
  - docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json
  - docs/pilot/three_channel_V1_METRIC_RESULTS.json

Notes: |
  Completed on 2026-05-23. `preclient_EVIDENCE_APPENDIX` contains 301
  internal traceability rows across all three channels: 255 media-review rows,
  40 video/manual blockers, 3 text-only V1 metric summaries, and 3 provider-gap
  summaries. It distinguishes text-only claims, media-backed candidates,
  post-factum rows, context-only rows, rejected noise, provider gaps, and
  media-processing blockers. No raw media bytes or private/authenticated source
  access are included.

### SAS-PRECLIENT-004: Per-Channel Free Dashboard Card Dataset ✅

Owner:      codex + operator
Phase:      37
Type:       validation
Depends-On: SAS-PRECLIENT-003

Objective: |
  Create a compact free-dashboard dataset for `bablos79`, `nemphiscrypts`, and
  `pifagortrade`: what the source is about, primary markets, strengths,
  weaknesses, measurable history, setup/RR availability, media coverage,
  evidence confidence, and external gate state.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/preclient_FREE_DASHBOARD_CARDS.json` contains exactly one card per channel with stable fields from the dashboard score schema."
    test: "tests/unit/test_preclient_dashboard_cards.py"
  - id: AC-2
    description: "Each card includes `what_it_is`, `strengths`, `weaknesses`, `measurable_claims`, `media_coverage`, `rr_setup_status`, `evidence_confidence`, and `gate_status`."
    test: "tests/unit/test_preclient_dashboard_cards.py"
  - id: AC-3
    description: "Cards avoid leaderboard, best-channel, future-profit, and investment-advice wording."
    test: "tests/unit/test_preclient_dashboard_cards.py"

Files:
  - docs/pilot/preclient_FREE_DASHBOARD_CARDS.json
  - docs/pilot/preclient_FREE_DASHBOARD_CARDS.md
  - tests/unit/test_preclient_dashboard_cards.py

Context-Refs:
  - docs/specs/CHANNEL_DASHBOARD_SCORE_SCHEMA.md
  - docs/pilot/three_channel_PHASE36_IMPACT_SCORECARD.md
  - docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md

Notes: |
  Completed on 2026-05-23. `preclient_FREE_DASHBOARD_CARDS` contains exactly
  one internal draft card for each channel. Cards include compact V1 text
  metrics, media coverage, RR/setup status, strengths, weaknesses, evidence
  confidence, blockers, and gate status. All cards remain
  `internal_only_not_dashboard_safe`; media/RR fields are blocked pending
  review gates and no full evidence appendix is exposed.

### SAS-PRECLIENT-005: Per-Channel Internal Deep Report V0 ✅

Owner:      codex
Phase:      37
Type:       report
Depends-On: SAS-PRECLIENT-003, SAS-PRECLIENT-004

Objective: |
  Generate one internal deep report per channel using the same report outline:
  executive summary, source/period, source style, measurable claims, media
  findings, setup/RR findings, model-reviewed candidates, confirmed examples,
  contradicted examples, limitations, and gate status.

Acceptance-Criteria:
  - id: AC-1
    description: "Reports exist for `bablos79`, `nemphiscrypts`, and `pifagortrade` under `docs/pilot/reports/preclient/`."
    test: "tests/unit/test_preclient_channel_reports.py"
  - id: AC-2
    description: "Every report cites the evidence appendix and states `internal_only` until human/operator review and external gate pass."
    test: "tests/unit/test_preclient_channel_reports.py"
  - id: AC-3
    description: "Reports include strengths and weaknesses with at least one supporting source/evidence reference each when available."
    test: "tests/unit/test_preclient_channel_reports.py"

Files:
  - docs/pilot/reports/preclient/bablos79_DEEP_REPORT_V0.md
  - docs/pilot/reports/preclient/nemphiscrypts_DEEP_REPORT_V0.md
  - docs/pilot/reports/preclient/pifagortrade_DEEP_REPORT_V0.md
  - tests/unit/test_preclient_channel_reports.py

Context-Refs:
  - docs/specs/PAID_CHANNEL_REPORT_BOUNDARY.md
  - docs/pilot/preclient_EVIDENCE_APPENDIX.md

Notes: |
  Completed on 2026-05-23. Three internal-only deep reports now exist under
  `docs/pilot/reports/preclient/`. Each uses the same outline, cites the
  evidence appendix, records `internal_only` gate status, includes confirmed
  and contradicted examples from the V1 utility report, and supports strengths
  and weaknesses with evidence references. They are not customer-ready sales
  deliverables.

### SAS-PRECLIENT-006: Paid-Style Demo Report For Strongest Candidate ✅

Owner:      codex + operator
Phase:      37
Type:       report
Depends-On: SAS-PRECLIENT-005

Objective: |
  Produce one polished paid-style demo report for the strongest current
  candidate, expected to be `pifagortrade` unless the evidence appendix
  disproves that choice. The report must show the product promise without
  claiming external approval.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/reports/preclient/PAID_STYLE_DEMO_REPORT.md` names the selected channel and explains why it was selected from evidence, not taste."
    test: "tests/unit/test_preclient_paid_demo_report.py"
  - id: AC-2
    description: "Demo report includes locked/paid sections: evidence appendix preview, post-factum vs real-time distinction, setup/RR review, counterexamples, and limitations."
    test: "tests/unit/test_preclient_paid_demo_report.py"
  - id: AC-3
    description: "Demo report remains `internal_demo_only` and contains no pricing promise, future-profit claim, or private-source promise."
    test: "tests/unit/test_preclient_paid_demo_report.py"

Files:
  - docs/pilot/reports/preclient/PAID_STYLE_DEMO_REPORT.md
  - tests/unit/test_preclient_paid_demo_report.py

Context-Refs:
  - docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md
  - docs/pilot/preclient_FREE_DASHBOARD_CARDS.md

Notes: |
  Completed on 2026-05-23. The demo selects `pifagortrade` from evidence
  density, not taste: 107 V1 evaluable text claims, 7 model-reviewed packet
  candidates, setup/risk/post-factum material, and clear counterexamples. It
  includes locked paid-style sections for evidence preview, post-factum vs
  real-time distinction, setup/RR review, counterexamples, and limitations. It
  remains `internal_demo_only` with no external approval claim.

### SAS-PRECLIENT-007: Outcome And RR Recompute For Review Candidates ✅

Owner:      codex
Phase:      37
Type:       validation
Depends-On: SAS-PRECLIENT-002, SAS-PRECLIENT-003

Objective: |
  Recompute deterministic market outcomes and RR/setup status for model
  reviewer candidates where public timestamps, asset/proxy mapping, direction,
  entry, stop, target, and horizon are sufficient. Rows with missing fields
  remain blockers, not failures.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/preclient_CANDIDATE_OUTCOMES.json` records every reviewed candidate as evaluated, insufficient_fields, provider_gap, post_factum_only, or media_review_blocked."
    test: "tests/unit/test_preclient_candidate_outcomes.py"
  - id: AC-2
    description: "Outcome rows include provider/source refs and do not use bulk market-history storage."
    test: "tests/unit/test_preclient_candidate_outcomes.py"
  - id: AC-3
    description: "Post-factum screenshots are not treated as predictive calls unless source timing and forward-looking language are clear."
    test: "tests/unit/test_preclient_candidate_outcomes.py"

Files:
  - docs/pilot/preclient_CANDIDATE_OUTCOMES.json
  - docs/pilot/preclient_CANDIDATE_OUTCOMES.md
  - scripts/three_channel_media_reviewer.py
  - scripts/three_channel_multimodal_research.py
  - tests/unit/test_preclient_candidate_outcomes.py

Context-Refs:
  - docs/pilot/preclient_MODEL_REVIEW_PACKET.json
  - docs/specs/CHANNEL_QUANT_METRICS_V2.md

Notes: |
  Completed on 2026-05-23. `preclient_CANDIDATE_OUTCOMES` records all 9
  model-reviewed candidates: 1 provider gap with internal RR recompute, 4
  insufficient-field rows, and 4 post-factum-only rows. Market outcomes were
  not recomputed because no candidate has the full approved source-time,
  instrument/proxy, direction, entry, stop, target, and horizon set. No bulk
  market-history storage was used.

### SAS-PRECLIENT-008: Static Free Dashboard Prototype ✅

Owner:      codex
Phase:      37
Type:       frontend
Depends-On: SAS-PRECLIENT-004, SAS-PRECLIENT-005

Objective: |
  Build a static internal dashboard prototype that renders the free channel
  cards and links to internal reports. The dashboard must be utilitarian,
  scannable, and clearly marked internal-only.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/preclient_dashboard/index.html` renders all three channel cards from the dashboard dataset."
    test: "tests/unit/test_preclient_dashboard_static.py"
  - id: AC-2
    description: "Dashboard shows gate status, evidence confidence, measurable sample size, setup/RR status, media status, and no-advice disclaimer per channel."
    test: "tests/unit/test_preclient_dashboard_static.py"
  - id: AC-3
    description: "Dashboard contains no payment flow, public ranking, private-source promise, or future-profit claim."
    test: "tests/unit/test_preclient_dashboard_static.py"

Files:
  - docs/pilot/preclient_dashboard/index.html
  - docs/pilot/preclient_FREE_DASHBOARD_CARDS.json
  - tests/unit/test_preclient_dashboard_static.py

Context-Refs:
  - docs/specs/CHANNEL_DASHBOARD_SCORE_SCHEMA.md

Notes: |
  Completed on 2026-05-23. `docs/pilot/preclient_dashboard/index.html`
  renders all three free dashboard cards with gate status, evidence
  confidence, measurable sample, setup/RR status, media status, no-advice
  labels, internal report links, evidence appendix link, and candidate outcome
  link. It is static/internal-only and has no payment flow, public ranking,
  private-source promise, or future-profit claim.

### SAS-PRECLIENT-009: Report Safety, Language, And Gate Pass ✅

Owner:      codex + operator
Phase:      37
Type:       validation
Depends-On: SAS-PRECLIENT-005, SAS-PRECLIENT-006, SAS-PRECLIENT-008

Objective: |
  Run deterministic language and artifact safety checks across free dashboard
  cards, internal deep reports, and paid-style demo report. Decide which fields
  are dashboard-safe, paid-report-only, internal-only, or blocked.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md` records the decision for every pre-client artifact and cites blockers."
    test: "tests/unit/test_preclient_artifact_safety_gate.py"
  - id: AC-2
    description: "Safety scan blocks advice, future-profit claims, best-channel/ranking language, unsupported private-source claims, and unreviewed media claims."
    test: "tests/unit/test_preclient_artifact_safety_gate.py"
  - id: AC-3
    description: "Gate states whether the team may proceed to buyer conversations, and if yes, which artifacts can be shown and under what wording."
    test: "tests/unit/test_preclient_artifact_safety_gate.py"

Files:
  - docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md
  - docs/pilot/preclient_ARTIFACT_SAFETY_GATE.json
  - tests/unit/test_preclient_artifact_safety_gate.py

Context-Refs:
  - docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md
  - docs/specs/PAID_CHANNEL_REPORT_BOUNDARY.md

Notes: |
  Completed on 2026-05-23. `preclient_ARTIFACT_SAFETY_GATE` covers 14
  artifacts, records 0 forbidden phrase findings, and still holds buyer
  conversations until `SAS-PRECLIENT-010` deep review. No artifact is showable
  now. The static dashboard, free cards, and paid-style demo are only
  candidates after Phase 37 deep review; evidence appendices, model packet,
  candidate outcomes, and deep reports remain internal-only.

### SAS-PRECLIENT-010: Phase 37 Deep Review And Client-Readiness Decision ✅

Owner:      codex + operator
Phase:      37
Type:       review
Depends-On: SAS-PRECLIENT-001, SAS-PRECLIENT-002, SAS-PRECLIENT-003, SAS-PRECLIENT-004, SAS-PRECLIENT-005, SAS-PRECLIENT-006, SAS-PRECLIENT-007, SAS-PRECLIENT-008, SAS-PRECLIENT-009

Objective: |
  Run a phase-boundary deep review and decide whether the project is ready for
  first client conversations, requires more internal artifact hardening, or
  should pivot the buyer promise.

Acceptance-Criteria:
  - id: AC-1
    description: "Deep review checks artifact traceability, report fairness, dashboard safety, model/human review boundary, outcome correctness, and buyer-promise clarity."
    test: "manual/review"
  - id: AC-2
    description: "`docs/archive/PHASE37_PRECLIENT_REVIEW.md` records findings, open blockers, and final decision: proceed_to_client_discovery, continue_internal_hardening, or pivot_scope."
    test: "manual/docs-review"
  - id: AC-3
    description: "State files are updated with the next route only after the decision is recorded."
    test: "manual/docs-review"

Files:
  - docs/archive/PHASE37_PRECLIENT_REVIEW.md
  - docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md
  - docs/CODEX_PROMPT.md
  - AGENT_NOTES.md
  - PHASE_HANDOFF.md

Context-Refs:
  - prompts/ORCHESTRATOR.md
  - docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md

Notes: |
  Completed on 2026-05-23. The archived review decision is
  `continue_internal_hardening`, not client-ready. Phase 37 produced a valid
  internal diligence baseline, but buyer conversations, public dashboard use,
  and paid delivery remain blocked until operator acceptance, accepted-row
  market recompute, and redacted demo readiness are complete.

## Phase 38 — Client-Readiness Evidence Acceptance

Goal: turn the Phase 37 internal artifact stack into a defensible buyer-demo
candidate without outreach yet. This phase must produce human/operator media
decisions, recompute only accepted rows with approved public providers, redact a
small showable demo subset, and define discovery success criteria. It must not
start outreach, pricing, paid report delivery, private-channel analysis,
private-channel partnership, or public ranking.

### SAS-CLIENTREADY-001: Operator Media Acceptance Ledger ✅

Owner:      codex + operator
Phase:      38
Type:       validation
Depends-On: SAS-PRECLIENT-010

Objective: |
  Convert the 9 model-reviewed media candidates into an operator decision
  ledger with accepted, rejected, needs-context, or post-factum-only status.

Acceptance-Criteria:
  - id: AC-1
    description: "A ledger artifact records one row per `preclient_MODEL_REVIEW_PACKET` candidate with source URL, media ref, model decision, operator decision, and reason."
    test: "tests/unit/test_clientready_operator_ledger.py"
  - id: AC-2
    description: "No row can become dashboard-safe or paid-report-safe from model review alone."
    test: "tests/unit/test_clientready_operator_ledger.py"
  - id: AC-3
    description: "Post-factum-only rows remain blocked from predictive-call metrics."
    test: "tests/unit/test_clientready_operator_ledger.py"

Files:
  - docs/pilot/clientready_OPERATOR_MEDIA_LEDGER.md
  - docs/pilot/clientready_OPERATOR_MEDIA_LEDGER.json
  - tests/unit/test_clientready_operator_ledger.py

### SAS-CLIENTREADY-002: Accepted Candidate RR And Outcome Recompute ✅

Owner:      codex
Phase:      38
Type:       validation
Depends-On: SAS-CLIENTREADY-001

Objective: |
  Recompute RR and market outcomes only for operator-accepted rows that have
  sufficient public timestamp, asset/proxy, direction, entry, stop, target, and
  horizon fields.

Acceptance-Criteria:
  - id: AC-1
    description: "Every recomputed row cites public provider/proxy provenance and uses no bulk market-history storage."
    test: "tests/unit/test_clientready_accepted_outcomes.py"
  - id: AC-2
    description: "Rows with missing fields, provider gaps, or post-factum status remain exclusions, not wins/losses."
    test: "tests/unit/test_clientready_accepted_outcomes.py"
  - id: AC-3
    description: "The artifact reports counts for accepted, recomputed, excluded, and buyer-demo-safe rows."
    test: "tests/unit/test_clientready_accepted_outcomes.py"

Files:
  - docs/pilot/clientready_ACCEPTED_OUTCOMES.md
  - docs/pilot/clientready_ACCEPTED_OUTCOMES.json
  - tests/unit/test_clientready_accepted_outcomes.py

### SAS-CLIENTREADY-003: Redacted Buyer Demo Subset ✅

Owner:      codex + operator
Phase:      38
Type:       report
Depends-On: SAS-CLIENTREADY-002

Objective: |
  Build a minimal buyer-demo subset from the dashboard and paid-style demo that
  is safe to show in discovery if the gate approves it.

Acceptance-Criteria:
  - id: AC-1
    description: "The subset includes only approved compact fields, visible caveats, and source-linked examples; it does not expose the full evidence appendix."
    test: "tests/unit/test_clientready_redacted_demo.py"
  - id: AC-2
    description: "The subset contains no advice, future-profit, ranking, marketplace, payment, or private-source language."
    test: "tests/unit/test_clientready_redacted_demo.py"
  - id: AC-3
    description: "The subset declares whether it is showable now or still blocked."
    test: "tests/unit/test_clientready_redacted_demo.py"

Files:
  - docs/pilot/clientready_REDACTED_BUYER_DEMO.md
  - docs/pilot/clientready_REDACTED_BUYER_DEMO.json
  - tests/unit/test_clientready_redacted_demo.py

### SAS-CLIENTREADY-004: Discovery Gate And Success Criteria ✅

Owner:      codex + operator
Phase:      38
Type:       validation
Depends-On: SAS-CLIENTREADY-003

Objective: |
  Decide whether the redacted demo is ready for narrow discovery conversations
  and define what evidence is needed before charging for a report.

Acceptance-Criteria:
  - id: AC-1
    description: "A gate artifact records `ready_for_discovery`, `continue_internal_hardening`, or `pivot_scope` with explicit blockers."
    test: "tests/unit/test_clientready_discovery_gate.py"
  - id: AC-2
    description: "Success criteria are discovery-only and do not include pricing, paid delivery, private partnerships, or public launch."
    test: "tests/unit/test_clientready_discovery_gate.py"
  - id: AC-3
    description: "State files move to client discovery only if the gate says `ready_for_discovery`."
    test: "tests/unit/test_clientready_discovery_gate.py"

Files:
  - docs/pilot/clientready_DISCOVERY_GATE.md
  - docs/pilot/clientready_DISCOVERY_GATE.json
  - tests/unit/test_clientready_discovery_gate.py

## Phase 40 — Auto-Validation Evidence Contract

Goal: replace the current human-only media acceptance bottleneck with an
auditable auto-validation contract. The system may auto-accept only when
evidence bundles, deterministic validators, and policy gates all pass. Anything
ambiguous remains `needs_human`. This phase defines the proof surface; it does
not yet promote any current candidate to customer-facing use.

### SAS-AUTOVAL-001: Auto-Validation Architecture ADR And Contract ✅

Owner:      codex
Phase:      40
Type:       docs
Depends-On: SAS-CLIENTREADY-004

Objective: |
  Define the automation contract for validating media/chart candidates without
  treating model review as truth.

Acceptance-Criteria:
  - id: AC-1
    description: "An ADR or spec states that auto-accept requires independent proof checks for timing, OCR/levels, setup consistency, asset/proxy/provider eligibility, post-factum cues, and customer-facing policy."
    test: "tests/unit/test_auto_validation_task_graph.py"
  - id: AC-2
    description: "The contract defines auto_accepted, auto_rejected, excluded_provider_gap, needs_human, and blocked_customer_facing states."
    test: "tests/unit/test_auto_validation_task_graph.py"
  - id: AC-3
    description: "The contract states that any validator uncertainty routes to needs_human, not customer-facing metrics."
    test: "tests/unit/test_auto_validation_task_graph.py"

Files:
  - docs/adr/ADR-005-auto-validation-evidence-engine.md
  - docs/specs/AUTO_VALIDATION_EVIDENCE.md
  - tests/unit/test_auto_validation_task_graph.py

### SAS-AUTOVAL-002: Evidence Bundle Schema ✅

Owner:      codex
Phase:      40
Type:       implementation
Depends-On: SAS-AUTOVAL-001

Objective: |
  Create a machine-readable evidence bundle for each candidate that preserves
  source URL, source timestamp, media refs, media hashes, OCR/transcript refs,
  model extraction spans, proposed setup fields, and market-window refs.

Acceptance-Criteria:
  - id: AC-1
    description: "Evidence bundle schema requires source URL, timestamp, media ref/hash or text ref/hash, extracted fields, extraction evidence refs, and provenance version."
    test: "tests/unit/test_auto_validation_evidence_bundle.py"
  - id: AC-2
    description: "Bundle validation rejects missing source timestamp, missing evidence ref, missing media/text checksum, or unsupported source class."
    test: "tests/unit/test_auto_validation_evidence_bundle.py"
  - id: AC-3
    description: "Bundle JSON serialization is deterministic and suitable for audit logs."
    test: "tests/unit/test_auto_validation_evidence_bundle.py"

Files:
  - src/signal_sandbox/auto_validation/evidence.py
  - tests/unit/test_auto_validation_evidence_bundle.py

### SAS-AUTOVAL-003: Validation Result And Audit Log Schema ✅

Owner:      codex
Phase:      40
Type:       implementation
Depends-On: SAS-AUTOVAL-002

Objective: |
  Define validator outputs so every pass/fail/uncertain decision has evidence,
  confidence, blocker reasons, validator version, and reproducible inputs.

Acceptance-Criteria:
  - id: AC-1
    description: "Validation result schema records validator id/version, status, confidence, evidence refs, blocker reasons, and deterministic input hashes."
    test: "tests/unit/test_auto_validation_result_schema.py"
  - id: AC-2
    description: "Audit log can combine multiple validator results without losing individual evidence refs."
    test: "tests/unit/test_auto_validation_result_schema.py"
  - id: AC-3
    description: "A result with missing evidence refs or blank validator version is invalid."
    test: "tests/unit/test_auto_validation_result_schema.py"

Files:
  - src/signal_sandbox/auto_validation/results.py
  - tests/unit/test_auto_validation_result_schema.py

## Phase 41 — Auto-Validation Validator Stack

Goal: implement independent validators that can prove or block the exact
failure modes that currently require operator review: post-factum screenshots,
bad OCR/level reads, wrong asset/proxy mapping, inconsistent setup math, and
unsafe customer-facing promotion.

### SAS-AUTOVAL-004: Pre-Outcome Timing Validator ✅

Owner:      codex
Phase:      41
Type:       implementation
Depends-On: SAS-AUTOVAL-003

Objective: |
  Verify that a candidate was published before the relevant market move, target
  touch, stop touch, or post-factum evidence window.

Acceptance-Criteria:
  - id: AC-1
    description: "Validator compares source timestamp to approved public market-window refs and returns pass only when the setup precedes outcome evidence."
    test: "tests/unit/test_auto_validation_timing.py"
  - id: AC-2
    description: "If target/stop was already reached before source timestamp, validator returns failed_post_factum_or_late."
    test: "tests/unit/test_auto_validation_timing.py"
  - id: AC-3
    description: "Missing market data, missing timestamp, or unsupported provider returns uncertain_needs_human, not pass."
    test: "tests/unit/test_auto_validation_timing.py"

Files:
  - src/signal_sandbox/auto_validation/timing.py
  - tests/unit/test_auto_validation_timing.py

### SAS-AUTOVAL-005: OCR Level And Setup Consistency Validator ✅

Owner:      codex
Phase:      41
Type:       implementation
Depends-On: SAS-AUTOVAL-003

Objective: |
  Validate that entry, stop, target, direction, and RR fields are read with
  sufficient evidence and form one coherent trade setup.

Acceptance-Criteria:
  - id: AC-1
    description: "Validator requires OCR/model evidence refs or bounding-box refs for every accepted level."
    test: "tests/unit/test_auto_validation_setup_consistency.py"
  - id: AC-2
    description: "Long setups require stop < entry < target; short setups require target < entry < stop; violations fail validation."
    test: "tests/unit/test_auto_validation_setup_consistency.py"
  - id: AC-3
    description: "Ambiguous levels, mixed trades, low confidence, or conflicting targets return uncertain_needs_human."
    test: "tests/unit/test_auto_validation_setup_consistency.py"

Files:
  - src/signal_sandbox/auto_validation/setup_consistency.py
  - tests/unit/test_auto_validation_setup_consistency.py

### SAS-AUTOVAL-006: Asset Proxy And Provider Eligibility Validator ✅

Owner:      codex
Phase:      41
Type:       implementation
Depends-On: SAS-AUTOVAL-003

Objective: |
  Prove that a candidate's asset maps to an approved instrument/proxy/provider
  path before any recompute can run.

Acceptance-Criteria:
  - id: AC-1
    description: "Validator maps asset aliases to approved provider/proxy refs or explicit exclusion states."
    test: "tests/unit/test_auto_validation_provider_eligibility.py"
  - id: AC-2
    description: "Ambiguous aliases, unsupported markets, and unapproved quote scales return excluded_provider_gap or uncertain_needs_human."
    test: "tests/unit/test_auto_validation_provider_eligibility.py"
  - id: AC-3
    description: "No provider lookup stores bulk market history; output records only compact provenance refs."
    test: "tests/unit/test_auto_validation_provider_eligibility.py"

Files:
  - src/signal_sandbox/auto_validation/provider_eligibility.py
  - tests/unit/test_auto_validation_provider_eligibility.py

### SAS-AUTOVAL-007: Post-Factum And Closed-Position Cue Detector ✅

Owner:      codex
Phase:      41
Type:       implementation
Depends-On: SAS-AUTOVAL-003

Objective: |
  Detect screenshots or text that describe already-managed or already-closed
  positions instead of pre-outcome calls.

Acceptance-Criteria:
  - id: AC-1
    description: "Detector flags PnL, closed-position, take-profit-hit, already-managed, and retrospective language cues as post_factum_risk."
    test: "tests/unit/test_auto_validation_post_factum.py"
  - id: AC-2
    description: "High-confidence post-factum rows become auto_rejected_for_predictive_metrics, not wins/losses."
    test: "tests/unit/test_auto_validation_post_factum.py"
  - id: AC-3
    description: "Mixed or low-confidence cues return uncertain_needs_human with cited evidence spans."
    test: "tests/unit/test_auto_validation_post_factum.py"

Files:
  - src/signal_sandbox/auto_validation/post_factum.py
  - tests/unit/test_auto_validation_post_factum.py

## Phase 42 — Auto-Accept Decision Engine And Evaluation

Goal: combine validator outputs into a strict decision engine. Full automation
is allowed only when all required validators pass. The engine must produce an
audit trail and an evaluation report on the current 9 client-ready candidates
before any customer-facing metric can use auto-accepted rows.

### SAS-AUTOVAL-008: Auto-Validation Decision Engine ✅

Owner:      codex
Phase:      42
Type:       implementation
Depends-On: SAS-AUTOVAL-004, SAS-AUTOVAL-005, SAS-AUTOVAL-006, SAS-AUTOVAL-007

Objective: |
  Combine validator results into auto_accepted, auto_rejected,
  excluded_provider_gap, needs_human, or blocked_customer_facing decisions.

Acceptance-Criteria:
  - id: AC-1
    description: "Decision engine returns auto_accepted only when timing, setup consistency, provider eligibility, post-factum detector, and policy gate all pass."
    test: "tests/unit/test_auto_validation_decision_engine.py"
  - id: AC-2
    description: "Any uncertain validator result routes to needs_human with blocker reasons."
    test: "tests/unit/test_auto_validation_decision_engine.py"
  - id: AC-3
    description: "Auto-accepted decisions include validator result ids and audit-log refs."
    test: "tests/unit/test_auto_validation_decision_engine.py"

Files:
  - src/signal_sandbox/auto_validation/decision.py
  - tests/unit/test_auto_validation_decision_engine.py

### SAS-AUTOVAL-009: Customer-Facing Policy Gate ✅

Owner:      codex
Phase:      42
Type:       implementation
Depends-On: SAS-AUTOVAL-008

Objective: |
  Decide whether an auto-validated row can be used in dashboard or paid-report
  metrics without legal/reputation overclaim risk.

Acceptance-Criteria:
  - id: AC-1
    description: "Gate requires public source refs, accepted validation audit refs, recompute provenance, visible caveats, and no forbidden wording."
    test: "tests/unit/test_auto_validation_customer_policy_gate.py"
  - id: AC-2
    description: "Rows with private-source risk, missing audit refs, post-factum status, or provider gaps remain blocked_customer_facing."
    test: "tests/unit/test_auto_validation_customer_policy_gate.py"
  - id: AC-3
    description: "Gate output is separate from model review and cannot be bypassed by model confidence."
    test: "tests/unit/test_auto_validation_customer_policy_gate.py"

Files:
  - src/signal_sandbox/auto_validation/customer_policy.py
  - tests/unit/test_auto_validation_customer_policy_gate.py

### SAS-AUTOVAL-010: Evaluation On Current Media Candidates ✅

Owner:      codex
Phase:      42
Type:       validation
Depends-On: SAS-AUTOVAL-009

Objective: |
  Run the auto-validation stack against the 9 Phase 38 media candidates and
  compare auto decisions with current conservative operator-ledger states.

Acceptance-Criteria:
  - id: AC-1
    description: "Evaluation artifact records auto_accepted, auto_rejected, needs_human, and excluded counts for all 9 candidates."
    test: "tests/unit/test_auto_validation_eval_current_candidates.py"
  - id: AC-2
    description: "Every auto decision cites validator audit refs and blocker reasons."
    test: "tests/unit/test_auto_validation_eval_current_candidates.py"
  - id: AC-3
    description: "Customer-facing promotion remains blocked unless the customer-facing policy gate passes."
    test: "tests/unit/test_auto_validation_eval_current_candidates.py"

Files:
  - docs/pilot/clientready_AUTO_VALIDATION_EVAL.md
  - docs/pilot/clientready_AUTO_VALIDATION_EVAL.json
  - tests/unit/test_auto_validation_eval_current_candidates.py

### SAS-AUTOVAL-011: Auto-Validation Deep Review ✅

Owner:      codex
Phase:      42
Type:       review
Depends-On: SAS-AUTOVAL-010

Objective: |
  Review whether the auto-validation stack is trustworthy enough to reduce
  human review load and define the remaining manual-review boundary.

Acceptance-Criteria:
  - id: AC-1
    description: "Deep review checks false accept risk, validator coverage, audit log completeness, customer-facing policy, and legal/product boundaries."
    test: "manual/review"
  - id: AC-2
    description: "Review records whether auto-accepted rows may enter internal recompute, customer-facing demo, or remain internal-only."
    test: "manual/review"
  - id: AC-3
    description: "Audit index, state docs, and phase report are updated; buyer outreach remains blocked unless a later discovery gate explicitly approves it."
    test: "manual/docs-review"

Files:
  - docs/archive/PHASE42_AUTO_VALIDATION_REVIEW.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md

### SAS-AUTOVAL-012: Core Receipt Audit Export ✅

Owner:      codex
Phase:      43
Type:       implementation
Depends-On: SAS-AUTOVAL-003

Objective: |
  Wire the existing Signal auto-validation Core-compatible receipt builder
  into the product-local validation workflow by exporting a receipt next to
  each durable validation audit log.

Acceptance-Criteria:
  - id: AC-1
    description: "The audit export writes sibling `<audit-id>.audit.json` and `<audit-id>.receipt.json` artifacts using deterministic JSON."
    test: "tests/unit/test_auto_validation_core_receipt.py::test_export_writes_receipt_next_to_validation_audit_log"
  - id: AC-2
    description: "The receipt export reuses the existing `build_signal_auto_validation_receipt` adapter and records the audit hash, bundle hash, validator ids, and evidence refs."
    test: "tests/unit/test_auto_validation_core_receipt.py"
  - id: AC-3
    description: "Receipt wiring stays product-local and rejects path-like artifact stems; Core does not own market/provider/customer-policy logic."
    test: "tests/unit/test_auto_validation_core_receipt.py::test_export_rejects_pathlike_artifact_stem"

Files:
  - src/signal_sandbox/auto_validation/audit_export.py
  - src/signal_sandbox/auto_validation/core_receipt.py
  - tests/unit/test_auto_validation_core_receipt.py
  - docs/specs/AUTO_VALIDATION_EVIDENCE.md

## Phase 28 — External-Ready Review Sprint

### SAS-NEXT-001: Full-Corpus Human Review Queue

Owner:      codex + operator
Phase:      28
Type:       validation
Depends-On: SAS-V1-009
Status:     complete

Objective: |
  Turn the internal V1 corpus into a full human/operator review queue so every
  included and excluded candidate has a defensible review state before any
  external-ready attempt.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/three_channel_FULL_REVIEW_QUEUE.md` and `.json` list all V1 included claims, V1 exclusions, pending false negatives, provider gaps, and media-blocked rows."
    test: "tests/unit/test_full_review_queue_artifact.py"
  - id: AC-2
    description: "Every row has stable id, channel, source URL, evidence snippet, suggested claim type, current decision, required reviewer action, and blocker reason where applicable."
    test: "tests/unit/test_full_review_queue_artifact.py"
  - id: AC-3
    description: "Queue states external delivery remains blocked until full review is closed and gate reruns."
    test: "tests/unit/test_full_review_queue_artifact.py"

Files:
  - docs/pilot/three_channel_FULL_REVIEW_QUEUE.md
  - docs/pilot/three_channel_FULL_REVIEW_QUEUE.json
  - docs/pilot/three_channel_V1_METRIC_RESULTS.json
  - docs/pilot/three_channel_V1_EXTRACTION_REVIEW.md
  - docs/AI_DEVELOPMENT_PLAN_RU.md

Notes: |
  Completed on 2026-05-19. The full-corpus queue is internal-only and keeps
  external delivery blocked until operator review closure and gate rerun.

### SAS-NEXT-002: False-Negative Extraction Pass

Owner:      codex + operator
Phase:      28
Type:       validation
Depends-On: SAS-NEXT-001
Status:     complete
Status:     complete

Objective: |
  Resolve V1 false negatives by extracting them into structured claims or
  documenting why they remain unsupported.

Acceptance-Criteria:
  - id: AC-1
    description: "All false negatives from V1 review have status extracted, needs_provider, needs_context, or rejected with reason."
    test: "tests/unit/test_false_negative_extraction_pass.py"
  - id: AC-2
    description: "Extractor calibration is updated for accepted false-negative patterns."
    test: "tests/unit/test_false_negative_extraction_pass.py"
  - id: AC-3
    description: "Unsupported false negatives are exclusions, not wins/losses."
    test: "tests/unit/test_false_negative_extraction_pass.py"

Files:
  - docs/pilot/three_channel_FALSE_NEGATIVE_PASS.md
  - docs/pilot/three_channel_FALSE_NEGATIVE_PASS.json
  - docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md
  - src/signal_sandbox/claims/
  - tests/unit/test_false_negative_extraction_pass.py

Notes: |
  Completed on 2026-05-19. Five pending false negatives were reviewed:
  three extracted as structured drafts, two kept as `needs_context`, zero
  added to customer-facing win/loss metrics.

### SAS-NEXT-003: Report Language Safety Pass

Owner:      codex
Phase:      28
Type:       report
Depends-On: SAS-NEXT-002
Status:     complete

Objective: |
  Add deterministic report wording checks for advice, future-profit,
  unsupported ranking, marketplace, and overclaim language.

Acceptance-Criteria:
  - id: AC-1
    description: "Safety checks scan V1 report text for forbidden advice/future-profit/ranking wording."
    test: "tests/unit/test_report_language_safety_v2.py"
  - id: AC-2
    description: "Report includes limitations, evidence links, and gate status."
    test: "tests/unit/test_report_language_safety_v2.py"
  - id: AC-3
    description: "No unreviewed media/OCR/chart claim appears in customer-facing wording."
    test: "tests/unit/test_report_language_safety_v2.py"

Files:
  - src/signal_sandbox/reports/
  - docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md
  - docs/pilot/reports/three_channel_V1_REPORT_LANGUAGE_SAFETY.md
  - docs/pilot/reports/three_channel_V1_REPORT_LANGUAGE_SAFETY.json
  - tests/unit/test_report_language_safety_v2.py

Notes: |
  Completed on 2026-05-19. Deterministic report safety scanner passes for the
  V1 report and records no advice, future-profit, ranking, marketplace, or
  unreviewed-media wording findings.

### SAS-NEXT-004: External Gate Rerun

Owner:      operator + codex
Phase:      28
Type:       review
Depends-On: SAS-NEXT-003
Status:     complete

Objective: |
  Rerun the external-ready gate after full review and language safety updates.

Acceptance-Criteria:
  - id: AC-1
    description: "Gate records approve_external_delivery, approve_internal_only, or reject_external_delivery with blockers."
    test: "manual/operator-review"
  - id: AC-2
    description: "Gate cites review coverage, provider coverage, media posture, RR/setup coverage, and wording safety."
    test: "manual/docs-review"
  - id: AC-3
    description: "External delivery remains blocked unless all required gate checks pass."
    test: "manual/docs-review"

Files:
  - docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md
  - docs/pilot/three_channel_FULL_REVIEW_QUEUE.md
  - tests/unit/test_external_gate_rerun_v2.py

Notes: |
  Completed on 2026-05-19. Gate rerun remains `approve_internal_only` because
  review closure, provider/media coverage, and RR/setup quality remain
  incomplete.

## Phase 29 — Review UI And Operator Workflow

### SAS-NEXT-005: Review Decision Data Model

Owner:      codex
Phase:      29
Type:       code
Depends-On: SAS-NEXT-001

Objective: |
  Add durable review decision models for claim approval workflows.

Acceptance-Criteria:
  - id: AC-1
    description: "Review decision schema records reviewer, timestamp, status, reason, source URL, evidence span, and claim id."
    test: "tests/unit/test_review_decision_model.py"
  - id: AC-2
    description: "Allowed statuses include accepted, false_positive, false_negative, needs_context, unsupported_provider, and media_blocked."
    test: "tests/unit/test_review_decision_model.py"
  - id: AC-3
    description: "Decision objects are deterministic and JSON-serializable."
    test: "tests/unit/test_review_decision_model.py"

Files:
  - src/signal_sandbox/review/
  - tests/unit/test_review_decision_model.py

Notes: |
  Completed on 2026-05-19. `ReviewDecision`, `ReviewEvidenceSpan`, and
  `ReviewDecisionStatus` provide deterministic JSON-serializable operator
  closure decisions.

### SAS-NEXT-006: Review Queue API And Export

Owner:      codex
Phase:      29
Type:       code
Depends-On: SAS-NEXT-005
Status:     complete

Objective: |
  Provide deterministic import/export for review queues and decisions.

Acceptance-Criteria:
  - id: AC-1
    description: "Review queue loader reads JSON artifacts and validates required fields."
    test: "tests/unit/test_review_queue_export.py"
  - id: AC-2
    description: "Reviewed decisions export to stable JSON and Markdown."
    test: "tests/unit/test_review_queue_export.py"
  - id: AC-3
    description: "Exports preserve source links and evidence spans."
    test: "tests/unit/test_review_queue_export.py"

Files:
  - src/signal_sandbox/review/
  - tests/unit/test_review_queue_export.py

Notes: |
  Completed on 2026-05-19. Review queue loader validates required fields, and
  review decision exports preserve source links and evidence spans in stable
  JSON/Markdown.

### SAS-NEXT-007: Minimal Review UI

Owner:      codex
Phase:      29
Type:       app
Depends-On: SAS-NEXT-006
Status:     complete

Objective: |
  Build a local review UI or static HTML review surface for fast operator
  decisions.

Acceptance-Criteria:
  - id: AC-1
    description: "UI supports filters by channel, claim type, asset, provider status, and review status."
    test: "manual/ui-review"
  - id: AC-2
    description: "UI shows source text next to normalized claim fields."
    test: "manual/ui-review"
  - id: AC-3
    description: "UI can save accepted/rejected/needs-context decisions to deterministic artifact."
    test: "manual/ui-review"

Files:
  - src/signal_sandbox/review/
  - docs/pilot/review_ui/

Notes: |
  Completed on 2026-05-19. Static HTML review surface supports channel, claim
  type, asset, provider-status, and review-status filters, shows source text
  with normalized fields, and generates local deterministic decision artifacts.

### SAS-NEXT-008: Review Audit Trail

Owner:      codex
Phase:      29
Type:       validation
Depends-On: SAS-NEXT-007
Status:     complete

Objective: |
  Ensure every review decision has an auditable source and reason.

Acceptance-Criteria:
  - id: AC-1
    description: "Audit artifact lists all decisions and missing-review blockers."
    test: "tests/unit/test_review_audit_trail.py"
  - id: AC-2
    description: "No accepted customer-facing claim lacks reviewer, source URL, and evidence span."
    test: "tests/unit/test_review_audit_trail.py"
  - id: AC-3
    description: "Audit result blocks external gate when review coverage is incomplete."
    test: "tests/unit/test_review_audit_trail.py"

Files:
  - docs/pilot/three_channel_REVIEW_AUDIT.md
  - tests/unit/test_review_audit_trail.py

Notes: |
  Completed on 2026-05-19. Audit trail lists 1710 missing review decisions,
  verifies accepted-decision evidence requirements, and keeps the external
  gate blocked while review coverage is incomplete.

## Phase 30 — Provider And Proxy Expansion

### SAS-NEXT-009: US Equity And Fund Provider Path

Owner:      codex
Phase:      30
Type:       code
Depends-On: SAS-V1-006
Status:     complete

Objective: |
  Add approved or explicitly unsupported provider routes for US equities/funds.

Acceptance-Criteria:
  - id: AC-1
    description: "`SPY` and liquid US equity/fund symbols resolve to approved provider route or explicit unsupported status."
    test: "tests/unit/test_us_provider_proxy_path.py"
  - id: AC-2
    description: "Fetch planning stays on-demand and window-scoped."
    test: "tests/unit/test_us_provider_proxy_path.py"
  - id: AC-3
    description: "Provider gaps remain exclusions."
    test: "tests/unit/test_us_provider_proxy_path.py"

Files:
  - src/signal_sandbox/claims/provider_config.py
  - tests/unit/test_us_provider_proxy_path.py

Notes: |
  Completed on 2026-05-19. `SPY`, `QQQ`, `AAPL`, `MSFT`, `NVDA`, `TSLA`, and
  `AMD` route to gated `yfinance_dev`; ambiguous/unsupported US symbols remain
  exclusions.

### SAS-NEXT-010: FX Proxy Policy

Owner:      codex + operator
Phase:      30
Type:       docs
Depends-On: SAS-NEXT-009
Status:     complete

Objective: |
  Define FX proxy semantics for currency claims.

Acceptance-Criteria:
  - id: AC-1
    description: "FX policy defines pair, direction semantics, provider, horizon, and exclusions."
    test: "manual/docs-review"
  - id: AC-2
    description: "`CNY`/similar shorthand is not silently mapped without operator-approved pair."
    test: "manual/docs-review"

Files:
  - docs/specs/FX_PROXY_POLICY.md
  - src/signal_sandbox/claims/provider_config.py

Notes: |
  Completed on 2026-05-19. FX shorthand remains unscoreable without explicit
  pair, direction semantics, provider, horizon, and operator approval.

### SAS-NEXT-011: Futures And Commodity Proxy Policy

Owner:      codex + operator
Phase:      30
Type:       docs
Depends-On: SAS-NEXT-010
Status:     complete

Objective: |
  Define futures/commodity proxy, rollover, and provider rules.

Acceptance-Criteria:
  - id: AC-1
    description: "`BR`, `NG`, `GOLD`, `SI`, and index futures are approved with explicit contract/proxy rules or excluded."
    test: "manual/docs-review"
  - id: AC-2
    description: "No continuous futures proxy is used without rollover rule."
    test: "manual/docs-review"

Files:
  - docs/specs/FUTURES_COMMODITY_PROXY_POLICY.md
  - src/signal_sandbox/claims/provider_config.py

Notes: |
  Completed on 2026-05-19. Futures, commodity, and index shorthand remain
  unscoreable without explicit instrument, direction, rollover, provider, and
  horizon approval.

### SAS-NEXT-012: Benchmark-Relative Outcomes

Owner:      codex
Phase:      30
Type:       code
Depends-On: SAS-NEXT-011
Status:     complete

Objective: |
  Add deterministic benchmark-relative returns for approved benchmark mappings.

Acceptance-Criteria:
  - id: AC-1
    description: "Outcome engine computes claim return minus benchmark return when both snapshots exist."
    test: "tests/unit/test_benchmark_relative_outcomes.py"
  - id: AC-2
    description: "Missing benchmark data produces explicit exclusion."
    test: "tests/unit/test_benchmark_relative_outcomes.py"

Files:
  - src/signal_sandbox/claims/outcomes.py
  - tests/unit/test_benchmark_relative_outcomes.py

Notes: |
  Completed on 2026-05-19. Claim outcomes can compute benchmark-relative
  return when benchmark data exists and emit `missing_benchmark_data` when it
  does not.

## Phase 31 — Quant Metrics V2

### SAS-NEXT-013: Quant Metric Schema V2

Owner:      codex
Phase:      31
Type:       docs
Depends-On: SAS-V1-007
Status:     complete

Objective: |
  Define quant-grade channel utility metrics and formulas.

Acceptance-Criteria:
  - id: AC-1
    description: "Spec defines precision/recall, hit rate by type, MFE/MAE, RR, R multiple, benchmark-relative return, and drawdown."
    test: "tests/unit/test_quant_metrics_v2_spec.py"
  - id: AC-2
    description: "Spec defines sample-size and confidence warnings."
    test: "tests/unit/test_quant_metrics_v2_spec.py"

Files:
  - docs/specs/CHANNEL_QUANT_METRICS_V2.md
  - tests/unit/test_quant_metrics_v2_spec.py

Notes: |
  Completed on 2026-05-19. Quant Metrics V2 defines precision/recall,
  hit-rate by type, MFE/MAE, RR, R multiple, benchmark-relative return,
  drawdown, and required sample-size/confidence warnings.

### SAS-NEXT-014: Setup Outcome Expansion

Owner:      codex
Phase:      31
Type:       code
Depends-On: SAS-NEXT-013
Status:     complete

Objective: |
  Expand setup outcomes with entry fill, stop, target, timeout, and R multiple.

Acceptance-Criteria:
  - id: AC-1
    description: "Setup outcomes compute R multiple using entry/stop/target."
    test: "tests/unit/test_setup_outcome_expansion.py"
  - id: AC-2
    description: "Missing levels remain blockers, not inferred values."
    test: "tests/unit/test_setup_outcome_expansion.py"

Files:
  - src/signal_sandbox/claims/outcomes.py
  - tests/unit/test_setup_outcome_expansion.py

Notes: |
  Completed on 2026-05-19. Setup outcomes compute R multiple for target,
  stopped, and timeout exits while missing or invalid setup levels remain
  explicit blockers.

### SAS-NEXT-015: Channel Utility Score V2

Owner:      codex
Phase:      31
Type:       validation
Depends-On: SAS-NEXT-014
Status:     complete

Objective: |
  Build a scorecard that separates coverage, clarity, extraction quality,
  outcome quality, risk quality, and limitations.

Acceptance-Criteria:
  - id: AC-1
    description: "Scorecard separates all metric dimensions and does not produce leaderboard language."
    test: "tests/unit/test_channel_utility_score_v2.py"
  - id: AC-2
    description: "Scorecard includes confidence/sample-size warnings."
    test: "tests/unit/test_channel_utility_score_v2.py"

Files:
  - docs/pilot/three_channel_V2_SCORECARD.md
  - tests/unit/test_channel_utility_score_v2.py

Notes: |
  Completed on 2026-05-19. V2 scorecard separates coverage, clarity,
  extraction quality, outcome quality, risk quality, limitations, and
  confidence/sample-size warnings without composite score language.

### SAS-NEXT-016: Robustness Checks

Owner:      codex
Phase:      31
Type:       validation
Depends-On: SAS-NEXT-015
Status:     complete

Objective: |
  Add sensitivity checks for horizon, provider, and sample size.

Acceptance-Criteria:
  - id: AC-1
    description: "Report appendix shows sensitivity to horizon/provider assumptions."
    test: "tests/unit/test_metric_robustness_appendix.py"
  - id: AC-2
    description: "Small samples are flagged and not overclaimed."
    test: "tests/unit/test_metric_robustness_appendix.py"

Files:
  - docs/pilot/three_channel_V2_ROBUSTNESS_APPENDIX.md
  - tests/unit/test_metric_robustness_appendix.py

Notes: |
  Completed on 2026-05-19. Robustness appendix records horizon, provider, and
  sample-size sensitivity checks and keeps current V2 artifacts internal-only.

## Phase 32 — Multimodal Expansion

### SAS-NEXT-017: Media Acquisition Inventory Per Channel

Owner:      codex
Phase:      32
Type:       validation
Depends-On: SAS-V1-005
Status:     complete

Objective: |
  Inventory public audio/image/chart candidates for each pilot channel.

Acceptance-Criteria:
  - id: AC-1
    description: "Inventory records public media refs, blockers, checksums, and review status."
    test: "tests/unit/test_media_acquisition_inventory_v2.py"

Files:
  - docs/pilot/three_channel_V2_MEDIA_INVENTORY.md
  - tests/unit/test_media_acquisition_inventory_v2.py

Notes: |
  Completed on 2026-05-19. V2 media inventory records public refs, checksums,
  blockers, review status, and keeps all media-backed claims out of customer
  metrics until human/operator acceptance and gate approval.

### SAS-NEXT-018: Transcript Human Review Workflow

Owner:      codex + operator
Phase:      32
Type:       validation
Depends-On: SAS-NEXT-017
Status:     complete

Objective: |
  Add transcript acceptance workflow for customer-facing claim use.

Acceptance-Criteria:
  - id: AC-1
    description: "Transcript refs can be accepted/rejected with reviewer and reason."
    test: "tests/unit/test_transcript_human_review_workflow.py"

Files:
  - docs/pilot/three_channel_TRANSCRIPT_REVIEW.md
  - tests/unit/test_transcript_human_review_workflow.py

Notes: |
  Completed on 2026-05-19. Transcript workflow supports accepted, rejected,
  needs-context, and pending decisions with reviewer, reason, checksums,
  accepted scope, and external gate separation.

### SAS-NEXT-019: OCR And Chart Source-Link Policy

Owner:      codex + operator
Phase:      32
Type:       docs
Depends-On: SAS-NEXT-018
Status:     complete

Objective: |
  Define how OCR/chart claims become source-linked and reviewable.

Acceptance-Criteria:
  - id: AC-1
    description: "Policy blocks machine-only chart interpretation from customer-facing metrics."
    test: "manual/docs-review"

Files:
  - docs/specs/OCR_CHART_SOURCE_LINK_POLICY.md
  - tests/unit/test_ocr_chart_source_link_policy.py

Notes: |
  Completed on 2026-05-19. OCR/chart policy requires source links, checksums,
  reviewer decisions, accepted boundaries, and blocks machine-only chart
  interpretation from customer-facing metrics.

### SAS-NEXT-020: Multimodal Claim Recompute

Owner:      codex
Phase:      32
Type:       validation
Depends-On: SAS-NEXT-019
Status:     complete

Objective: |
  Recompute metrics with reviewed media claims included and unreviewed media
  excluded.

Acceptance-Criteria:
  - id: AC-1
    description: "Reviewed media claims enter V2 metrics with media provenance."
    test: "tests/unit/test_multimodal_claim_recompute_v2.py"
  - id: AC-2
    description: "Unreviewed media remains excluded."
    test: "tests/unit/test_multimodal_claim_recompute_v2.py"

Files:
  - docs/pilot/three_channel_V2_METRIC_RESULTS.json
  - tests/unit/test_multimodal_claim_recompute_v2.py

Notes: |
  Completed on 2026-05-19. V2 multimodal recompute defines media provenance
  inclusion schema, includes zero reviewed media claims because none are human
  accepted, and excludes all unreviewed/unlinked media rows.

## Phase 33 — Report Productization

### SAS-NEXT-021: Report Template System

Owner:      codex
Phase:      33
Type:       code
Depends-On: SAS-V1-008
Status:     complete

Objective: |
  Render the same report data to Markdown and HTML/PDF-ready output.

Acceptance-Criteria:
  - id: AC-1
    description: "Renderer produces stable Markdown and HTML-ready output from one data model."
    test: "tests/unit/test_report_template_system.py"

Files:
  - src/signal_sandbox/reports/
  - tests/unit/test_report_template_system.py

Notes: |
  Completed on 2026-05-19. Report template system renders Markdown and
  HTML-ready output from one strict data model and escapes HTML-visible values.

### SAS-NEXT-022: Evidence Appendix Generator

Owner:      codex
Phase:      33
Type:       code
Depends-On: SAS-NEXT-021
Status:     complete

Objective: |
  Generate source/provider/review appendix for every report metric.

Acceptance-Criteria:
  - id: AC-1
    description: "Every metric row links to source, provider, snapshot, and review decision."
    test: "tests/unit/test_evidence_appendix_generator.py"

Files:
  - src/signal_sandbox/reports/
  - tests/unit/test_evidence_appendix_generator.py

Notes: |
  Completed on 2026-05-19. Evidence appendix renderer links each metric row to
  source ref, provider, snapshot, review decision, and evidence URL.

### SAS-NEXT-023: Buyer Demo Pack

Owner:      codex
Phase:      33
Type:       docs
Depends-On: SAS-NEXT-022
Status:     complete

Objective: |
  Package report, methodology, limitations, talk track, and gate status for
  buyer discovery.

Acceptance-Criteria:
  - id: AC-1
    description: "Demo pack is internal-only unless gate approves external delivery."
    test: "tests/unit/test_buyer_demo_pack.py"

Files:
  - docs/pilot/three_channel_BUYER_DEMO_PACK.md
  - tests/unit/test_buyer_demo_pack.py

Notes: |
  Completed on 2026-05-19. Buyer demo pack packages artifacts, methodology,
  limitations, talk track, and gate status while staying internal-only until
  explicit external gate approval.

### SAS-NEXT-024: Customer-Safe Wording Library

Owner:      codex
Phase:      33
Type:       code
Depends-On: SAS-NEXT-023
Status:     complete

Objective: |
  Centralize allowed and forbidden report wording.

Acceptance-Criteria:
  - id: AC-1
    description: "Forbidden advice, future-profit, leaderboard, and overclaim phrases are blocked."
    test: "tests/unit/test_customer_safe_wording.py"

Files:
  - src/signal_sandbox/reports/wording.py
  - tests/unit/test_customer_safe_wording.py

Notes: |
  Completed on 2026-05-19. Customer-safe wording library centralizes allowed
  context phrases and blocks advice, future-profit, leaderboard, marketplace,
  and overclaim wording.

## Phase 34 — Pilot Operations

### SAS-NEXT-025: Pilot Buyer List

Owner:      operator + codex
Phase:      34
Type:       docs
Depends-On: SAS-NEXT-023
Status:     complete

Objective: |
  Define buyer profiles, pains, and likely pilot use cases.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/BUYER_DISCOVERY.md` lists 10-20 buyer profiles and use cases."
    test: "manual/operator-review"

Files:
  - docs/pilot/BUYER_DISCOVERY.md
  - tests/unit/test_buyer_discovery.py

Notes: |
  Completed on 2026-05-19. Buyer discovery plan lists 15 buyer profiles,
  pains, current behavior, likely pilot use cases, validation signals,
  disqualifiers, and pilot success criteria.

### SAS-NEXT-026: Demo Script

Owner:      codex
Phase:      34
Type:       docs
Depends-On: SAS-NEXT-025
Status:     complete

Objective: |
  Write a 15-minute demo script with clear limitations.

Acceptance-Criteria:
  - id: AC-1
    description: "Demo script explains value without claiming advice or future profit."
    test: "manual/docs-review"

Files:
  - docs/pilot/DEMO_SCRIPT.md
  - tests/unit/test_demo_script.py

Notes: |
  Completed on 2026-05-19. Demo script covers a 15-minute call, method,
  limitations, pilot shape, and guardrails without advice, future-profit, or
  external-ready claims.

### SAS-NEXT-027: Paid Pilot Offer

Owner:      operator + codex
Phase:      34
Type:       docs
Depends-On: SAS-NEXT-026
Status:     complete

Objective: |
  Define a bounded paid pilot offer.

Acceptance-Criteria:
  - id: AC-1
    description: "Offer includes scope, price hypothesis, turnaround, deliverables, and exclusions."
    test: "manual/operator-review"

Files:
  - docs/pilot/PAID_PILOT_OFFER.md
  - tests/unit/test_paid_pilot_offer.py

Notes: |
  Completed on 2026-05-19. Paid pilot offer defines bounded scope,
  deliverables, price hypothesis, turnaround, buyer commitments, exclusions,
  success gate, kill criteria, and external boundary.

### SAS-NEXT-028: Feedback Loop

Owner:      operator + codex
Phase:      34
Type:       validation
Depends-On: SAS-NEXT-027
Status:     complete

Objective: |
  Track buyer feedback, objections, willingness to pay, and next steps.

Acceptance-Criteria:
  - id: AC-1
    description: "Each demo records buyer role, objection, requested output, willingness to pay, and next action."
    test: "manual/operator-review"

Files:
  - docs/pilot/BUYER_FEEDBACK_LOG.md
  - tests/unit/test_buyer_feedback_log.py

Notes: |
  Completed on 2026-05-19. Feedback log template records buyer role,
  objection, requested output, willingness to pay, next action, owner, and
  follow-up rules without inventing demo records.

## Phase 35 — Reliability And Scaling

### SAS-NEXT-029: Run Manifest And Caching

Owner:      codex
Phase:      35
Type:       code
Depends-On: SAS-NEXT-024
Status:     complete

Objective: |
  Record report inputs, versions, hashes, providers, and outputs.

Acceptance-Criteria:
  - id: AC-1
    description: "Every report run has deterministic manifest and compact cache refs."
    test: "tests/unit/test_run_manifest_and_caching.py"

Files:
  - src/signal_sandbox/runs/
  - tests/unit/test_run_manifest_and_caching.py

Notes: |
  Completed on 2026-05-19. Run manifest package records input refs, provider
  refs, output refs, deterministic manifest hashes, and compact cache refs.

### SAS-NEXT-030: Retry And Provider Failure Handling

Owner:      codex
Phase:      35
Type:       code
Depends-On: SAS-NEXT-029
Status:     complete

Objective: |
  Model provider failures without corrupting outcomes.

Acceptance-Criteria:
  - id: AC-1
    description: "Provider errors produce retry/exclusion states, not wins/losses."
    test: "tests/unit/test_provider_failure_handling.py"

Files:
  - src/signal_sandbox/claims/provider_config.py
  - tests/unit/test_provider_failure_handling.py

Notes: |
  Completed on 2026-05-19. Provider fetch failures now produce retry or
  provider-failure exclusion states with error metadata instead of outcomes.

### SAS-NEXT-031: Regression Suite For Known Channels

Owner:      codex
Phase:      35
Type:       validation
Depends-On: SAS-NEXT-030
Status:     complete

Objective: |
  Add golden tests for known channel metrics and claim examples.

Acceptance-Criteria:
  - id: AC-1
    description: "Known claims and aggregate metrics do not drift unexpectedly."
    test: "tests/unit/test_known_channel_regressions.py"

Files:
  - tests/unit/test_known_channel_regressions.py

Notes: |
  Completed on 2026-05-19. Regression tests lock current V2 aggregate metrics
  and selected V1 kept claim examples against unexpected drift.

### SAS-NEXT-032: Cost And Time Instrumentation

Owner:      codex
Phase:      35
Type:       code
Depends-On: SAS-NEXT-031
Status:     complete

Objective: |
  Measure capture, review, market data, and report generation time/cost.

Acceptance-Criteria:
  - id: AC-1
    description: "Run metrics record step durations, provider calls, cache hits, and estimated cost where available."
    test: "tests/unit/test_run_cost_time_instrumentation.py"

Files:
  - src/signal_sandbox/runs/
  - tests/unit/test_run_cost_time_instrumentation.py

Notes: |
  Completed on 2026-05-19. Run operational metrics record step durations,
  provider calls, cache hits, estimated costs, deterministic totals, and a
  metrics hash.

## Phase 26 — Operator-Gated Evidence Repair

### SAS-ER-000: Public Corpus Repair Capture ✅

Owner:      codex
Phase:      26
Type:       validation
Depends-On: SAS-DR-022

Objective: |
  Expand the public `bablos79` corpus through the approved public Telegram
  `/s/` route and create an operator review queue without computing outcomes
  or creating external claims.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_EVIDENCE_REPAIR_CAPTURE_MANIFEST.json` records public pages fetched, text rows in window, fresh workspace captures, source boundary, and no private/login/paywalled source use."
    test: "tests/unit/test_evidence_repair_artifacts.py::test_evidence_repair_capture_manifest_expands_public_corpus"
  - id: AC-2
    description: "`docs/pilot/bablos79_EVIDENCE_REPAIR_REVIEW_QUEUE.json` records candidate rows and blocks market-data fetch/external eligibility until operator approval."
    test: "tests/unit/test_evidence_repair_artifacts.py::test_evidence_repair_review_queue_blocks_market_fetch_until_approval"
  - id: AC-3
    description: "`docs/pilot/bablos79_EVIDENCE_REPAIR_OPERATOR_ACTIONS.md` lists the operator decisions required before proxy mapping, market snapshots, outcomes, or external delivery can resume."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_EVIDENCE_REPAIR_CAPTURE_MANIFEST.json
  - docs/pilot/bablos79_EVIDENCE_REPAIR_CAPTURE_PACK.md
  - docs/pilot/bablos79_EVIDENCE_REPAIR_REVIEW_QUEUE.json
  - docs/pilot/bablos79_EVIDENCE_REPAIR_REVIEW_QUEUE.md
  - docs/pilot/bablos79_EVIDENCE_REPAIR_OPERATOR_ACTIONS.md
  - tests/unit/test_evidence_repair_artifacts.py

Notes: |
  This task may write local workspace capture JSON files from public `/s/`
  pages. It must not approve proxies, fetch market data, compute outcomes,
  accept transcripts, or create external claims.

### SAS-ER-002: Three-Channel Public Corpus Probe ✅

Owner:      codex
Phase:      26
Type:       validation
Depends-On: SAS-ER-000

Objective: |
  Run the same public Telegram `/s/` corpus probe for the three initial pilot
  sources (`bablos79`, `nemphiscrypts`, and `pifagortrade`) and produce a
  comparable readiness surface before operator-approved proxy/horizon work.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.json` records public-source boundary flags and confirms no private/login/paywalled source use, market-data fetches, outcomes, or external claims."
    test: "tests/unit/test_three_channel_probe_artifacts.py::test_three_channel_probe_records_public_boundary"
  - id: AC-2
    description: "The probe records comparable text-row and candidate-count summaries for all three pilot channels."
    test: "tests/unit/test_three_channel_probe_artifacts.py::test_three_channel_probe_has_comparable_candidate_counts"
  - id: AC-3
    description: "Review samples remain operator-gated with market-data fetch and external eligibility blocked."
    test: "tests/unit/test_three_channel_probe_artifacts.py::test_three_channel_review_samples_remain_operator_gated"

Files:
  - scripts/three_channel_public_probe.py
  - docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.json
  - docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.md
  - tests/unit/test_three_channel_probe_artifacts.py

Notes: |
  This task is a readiness probe, not a performance ranking. Candidate labels
  are draft review surfaces only. The next outcome-producing step still
  requires operator approval of evaluator type, proxy mapping, timestamp basis,
  horizons, and outcome method.

### SAS-ER-003: Channel Utility Evaluation Contract ✅

Owner:      codex
Phase:      26
Type:       validation
Depends-On: SAS-ER-002

Objective: |
  Codify the product rule that channel usefulness is measured from normalized,
  evidence-backed market claims extracted from text, audio transcripts, and
  image/OCR evidence, then validated through open/public market-data windows
  without maintaining a huge local market database.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/specs/CHANNEL_UTILITY_EVALUATION.md` requires text/audio/image evidence to converge into a normalized claim surface."
    test: "tests/unit/test_channel_utility_evaluation_spec.py::test_channel_utility_spec_requires_multimodal_normalization"
  - id: AC-2
    description: "The spec requires on-demand open/public API or operator-public-export validation windows instead of bulk market-history storage."
    test: "tests/unit/test_channel_utility_evaluation_spec.py::test_channel_utility_spec_uses_open_api_window_validation"
  - id: AC-3
    description: "The spec preserves operator gating, counterexamples, no-overclaim boundaries, and no future-profit claims."
    test: "tests/unit/test_channel_utility_evaluation_spec.py::test_channel_utility_spec_keeps_claims_operator_gated"

Files:
  - docs/specs/CHANNEL_UTILITY_EVALUATION.md
  - tests/unit/test_channel_utility_evaluation_spec.py

Notes: |
  This is a product-methodology contract. It does not compute outcomes or fetch
  market data. It defines the next implementation target: a three-channel
  approval matrix for evaluator type, claim types, proxy mapping, provider,
  horizons, strict trade rules, and exclusion statuses.

### SAS-ER-004: Three-Channel Metric Results V0 ✅

Owner:      codex
Phase:      26
Type:       validation
Depends-On: SAS-ER-003

Objective: |
  Produce the first end-to-end historical metric result for the three initial
  pilot channels by extracting normalized public market claims, validating
  supported assets through open/public OHLCV windows, and writing a comparison
  report with confirmed/contradicted examples and numeric channel metrics.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/three_channel_METRIC_RESULTS.json` records public Telegram source method, open/public market-data providers, 7d primary horizon, and no bulk market-history database or investment-advice posture."
    test: "tests/unit/test_three_channel_metric_results.py::test_three_channel_metric_results_use_open_public_windows"
  - id: AC-2
    description: "Metric results compare `bablos79`, `nemphiscrypts`, and `pifagortrade` with evaluable claims, confirmed hits, contradicted misses, and provider counts."
    test: "tests/unit/test_three_channel_metric_results.py::test_three_channel_metric_results_compare_all_channels"
  - id: AC-3
    description: "`docs/pilot/three_channel_METRIC_REPORT.md` includes channel comparison, confirmed/contradicted evidence examples, and explicit report limits."
    test: "tests/unit/test_three_channel_metric_results.py::test_three_channel_metric_report_contains_evidence_and_limits"

Files:
  - scripts/three_channel_metric_report.py
  - docs/pilot/three_channel_METRIC_RESULTS.json
  - docs/pilot/three_channel_METRIC_REPORT.md
  - tests/unit/test_three_channel_metric_results.py

Notes: |
  This is a V0 historical research run. It uses conservative rule extraction
  and daily OHLCV proxies. Results are useful for first comparison but still
  require operator/human review before customer-facing claims or paid delivery.

### SAS-ER-005: Three-Channel V1 Roadmap Task Graph ✅

Owner:      codex
Phase:      26
Type:       docs
Depends-On: SAS-ER-004

Objective: |
  Convert the post-V0 next steps into a concrete Phase 27 task graph and V1
  roadmap so the project can move from internal V0 research to reviewed V1
  channel utility reporting.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/tasks.md` contains Phase 27 tasks `SAS-V1-001..009` covering approval matrix, extraction review, structured extractor, level-aware outcomes, multimodal claims, provider expansion, V1 recompute, external gate, and deep review."
    test: "tests/unit/test_three_channel_v1_roadmap.py::test_phase_27_task_graph_lists_full_v1_flow"
  - id: AC-2
    description: "`docs/pilot/THREE_CHANNEL_V1_ROADMAP.md` records required V1 improvements over V0."
    test: "tests/unit/test_three_channel_v1_roadmap.py::test_phase_27_roadmap_covers_v1_required_improvements"
  - id: AC-3
    description: "The roadmap preserves no-private-scraping, no-bulk-market-history, no-future-profit, no-investment-advice, and no-unreviewed-media-claim boundaries."
    test: "tests/unit/test_three_channel_v1_roadmap.py::test_phase_27_roadmap_preserves_no_overclaim_boundaries"

Files:
  - docs/tasks.md
  - docs/pilot/THREE_CHANNEL_V1_ROADMAP.md
  - tests/unit/test_three_channel_v1_roadmap.py

Notes: |
  This task adds planning structure only. It does not implement V1 extraction
  or recompute metrics.

### ✅ SAS-ER-001: Candidate Review And Proxy/Horizon Approval

Owner:      operator + codex
Phase:      26
Type:       review
Depends-On: SAS-ER-000, SAS-ER-002, SAS-ER-003, SAS-ER-004, SAS-ER-005

Objective: |
  Review the evidence repair candidate queue and explicitly approve or reject
  candidate rows, proxy mappings, and horizon/outcome methods.

Acceptance-Criteria:
  - id: AC-1
    description: "Each `position_disclosure_candidate` is marked approved_for_proxy_mapping or rejected_as_context with reason."
    test: "tests/unit/test_evidence_repair_proxy_approvals.py::test_bablos79_proxy_approvals_cover_position_candidates"
  - id: AC-2
    description: "Approved rows have explicit asset/proxy, data source, timestamp basis, horizon, and outcome method."
    test: "tests/unit/test_evidence_repair_proxy_approvals.py::test_bablos79_proxy_approvals_define_provider_horizon_and_method"
  - id: AC-3
    description: "No market data fetch is allowed for rows lacking explicit operator approval."
    test: "tests/unit/test_evidence_repair_proxy_approvals.py::test_bablos79_proxy_approvals_block_unapproved_fetches_and_external_use"

Files:
  - docs/pilot/bablos79_EVIDENCE_REPAIR_REVIEW_QUEUE.md
  - docs/pilot/bablos79_EVIDENCE_REPAIR_OPERATOR_ACTIONS.md
  - docs/pilot/bablos79_EVIDENCE_REPAIR_PROXY_APPROVALS.md
  - tests/unit/test_evidence_repair_proxy_approvals.py

Notes: |
  Completed on 2026-05-19. The approval record is internal V1 research only:
  nine position rows have partial asset-level MOEX ISS proxy approvals, one row
  is rejected as context, unsupported assets remain do_not_fetch, primary
  horizon is 7d, and external/customer-facing use remains blocked.

### ✅ SAS-ER-006: Phase 26 Deep Review

Owner:      codex
Phase:      26
Type:       review
Depends-On: SAS-ER-000, SAS-ER-001, SAS-ER-002, SAS-ER-003, SAS-ER-004, SAS-ER-005

Objective: |
  Run the mandatory Phase 26 boundary review and archive the evidence-repair
  loop before Phase 27 V1 report work starts.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks public-source boundary, approval matrix, V0 metrics, no-bulk-market-history posture, and customer-facing blockers."
    test: "manual-review: docs/archive/PHASE26_REVIEW.md exists and records findings."
  - id: AC-2
    description: "Any P0/P1/P2 findings are reflected in `docs/tasks.md` before Phase 27 begins."
    test: "manual-review: review findings mapped to task graph or explicitly marked none."
  - id: AC-3
    description: "State files are updated for Phase 27 only after the review/archive is complete."
    test: "manual-review: CODEX prompt, README, handoff, checkpoint, and journal match Phase 26 closure state."

Files:
  - docs/archive/PHASE26_REVIEW.md
  - docs/tasks.md
  - docs/CODEX_PROMPT.md
  - README.md
  - MEMORY.md
  - AGENT_NOTES.md
  - PHASE_HANDOFF.md
  - ORCHESTRATOR_CHECKPOINT.md
  - docs/IMPLEMENTATION_JOURNAL.md

Notes: |
  Completed on 2026-05-19. Phase 26 review is archived at
  `docs/archive/PHASE26_REVIEW.md`; no P0/P1/P2 implementation findings were
  found. Phase 27 may start, but external delivery remains blocked until the V1
  gate.

## Phase 27 — Three-Channel V1 Metric Report

### ✅ SAS-V1-001: Three-Channel Approval Matrix

Owner:      operator + codex
Phase:      27
Type:       review
Depends-On: SAS-ER-001, SAS-ER-004

Objective: |
  Convert the V0 metric run into an explicit approval matrix for all three
  pilot channels before any V1 recomputation or customer-facing wording.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/three_channel_V1_APPROVAL_MATRIX.md` lists approved evaluator types, allowed claim types, default horizons, exclusion statuses, and provider/proxy rules for `bablos79`, `nemphiscrypts`, and `pifagortrade`."
    test: "tests/unit/test_three_channel_v1_approval_matrix.py::test_three_channel_v1_approval_matrix_covers_all_channels"
  - id: AC-2
    description: "Every V0 provider/proxy class used in `three_channel_METRIC_RESULTS.json` is marked approved, rejected, or needs_operator_input with rationale."
    test: "tests/unit/test_three_channel_v1_approval_matrix.py::test_three_channel_v1_approval_matrix_marks_v0_provider_classes"
  - id: AC-3
    description: "The matrix states that V0 numbers remain internal until false-positive review and V1 report gate complete."
    test: "tests/unit/test_three_channel_v1_approval_matrix.py::test_three_channel_v1_approval_matrix_blocks_external_v0_use"

Files:
  - docs/pilot/three_channel_V1_APPROVAL_MATRIX.md
  - docs/pilot/three_channel_METRIC_RESULTS.json
  - docs/specs/CHANNEL_UTILITY_EVALUATION.md

Notes: |
  Completed on 2026-05-19. The approval matrix is internal V1 research only.
  It approves V0 Binance crypto and MOEX ISS share provider classes for V1
  calibration, carries unsupported futures/FX/ETF/commodity/ambiguous aliases
  as needs_operator_input or rejected_until_mapped, and blocks external use
  until V1 review and gate complete.

### ✅ SAS-V1-002: False-Positive Review And Extractor Calibration Pack

Owner:      codex + operator
Phase:      27
Type:       validation
Depends-On: SAS-V1-001

Objective: |
  Review a stratified sample of V0 normalized claims and exclusions to measure
  extraction false positives/false negatives, then produce concrete extractor
  calibration rules for V1.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/three_channel_V1_EXTRACTION_REVIEW.md` reviews at least 20 V0 included claims and 20 excluded rows across all three channels."
    test: "tests/unit/test_three_channel_v1_extraction_review.py::test_v1_extraction_review_has_required_sample_sizes"
  - id: AC-2
    description: "Each reviewed row has status `accepted`, `false_positive`, `false_negative`, or `needs_context`, with reason and source link."
    test: "tests/unit/test_three_channel_v1_extraction_review.py::test_v1_extraction_review_uses_allowed_statuses_and_channels"
  - id: AC-3
    description: "`docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md` lists deterministic rule changes required before V1 recomputation."
    test: "tests/unit/test_three_channel_v1_extraction_review.py::test_v1_extractor_calibration_lists_required_rule_changes"

Files:
  - docs/pilot/three_channel_V1_EXTRACTION_REVIEW.md
  - docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md
  - docs/pilot/three_channel_METRIC_RESULTS.json
  - scripts/three_channel_metric_report.py

Notes: |
  Completed on 2026-05-19. The review covers 20 included V0 claims and 21
  excluded public-probe rows across all three channels. Calibration rules now
  require negation-aware direction parsing, trade-management linkage,
  conditional setup handling, alias expansion, non-asset token blocking, and
  provider/media boundaries before V1 recomputation.

### ✅ SAS-V1-003: Structured Claim Extractor V1

Owner:      codex
Phase:      27
Type:       code
Depends-On: SAS-V1-002

Objective: |
  Promote V0 rule extraction into a reusable structured claim extractor that
  emits claim type, asset/proxy, direction, entry, stop/invalidation, target,
  horizon, risk/reward fields, evidence spans, and ambiguity flags.

Acceptance-Criteria:
  - id: AC-1
    description: "A reusable extractor module emits structured claim rows for text `SourceDocument` inputs without network access."
    test: "tests/unit/test_structured_claim_extractor_v1.py"
  - id: AC-2
    description: "Extractor distinguishes `trade_setup`, `directional_thesis`, `position_disclosure`, `trade_management`, `risk_warning`, and `context_only` rows."
    test: "tests/unit/test_structured_claim_extractor_v1.py"
  - id: AC-3
    description: "Entry/stop/target/RR fields are populated only from evidence spans or deterministic rules; missing fields remain explicit nulls with blockers."
    test: "tests/unit/test_structured_claim_extractor_v1.py"

Files:
  - src/signal_sandbox/claims/
  - tests/unit/test_structured_claim_extractor_v1.py
  - docs/specs/CHANNEL_UTILITY_EVALUATION.md

Notes: |
  Completed on 2026-05-19. `src/signal_sandbox/claims/` adds a deterministic
  structured extractor for text `SourceDocument` inputs. It emits claim type,
  assets, direction, entry/stop/target/RR, horizons, evidence spans, ambiguity
  flags, and blockers without LLM or market API calls.

### ✅ SAS-V1-004: Level-Aware Outcome Engine V1

Owner:      codex
Phase:      27
Type:       code
Depends-On: SAS-V1-003

Objective: |
  Add deterministic V1 outcomes for strict setups and trade-management rows:
  entry-fill, stop/target/timeout, return %, MFE/MAE, RR, benchmark-relative
  return, and exclusion statuses.

Acceptance-Criteria:
  - id: AC-1
    description: "Outcome code evaluates entry/stop/target/timeout rows over immutable OHLCV snapshots and records deterministic provenance."
    test: "tests/unit/test_claim_outcomes_v1.py"
  - id: AC-2
    description: "Directional thesis rows continue to support fixed-horizon returns without requiring entry/stop/target."
    test: "tests/unit/test_claim_outcomes_v1.py"
  - id: AC-3
    description: "Trade-management fragments are excluded unless linked to an approved original setup."
    test: "tests/unit/test_claim_outcomes_v1.py"

Files:
  - src/signal_sandbox/claims/outcomes.py
  - tests/unit/test_claim_outcomes_v1.py
  - docs/specs/CHANNEL_UTILITY_EVALUATION.md

Notes: |
  Completed on 2026-05-19. `src/signal_sandbox/claims/outcomes.py` evaluates
  strict setup entry/stop/target/timeout rows, directional-thesis fixed-horizon
  rows, and trade-management exclusions over immutable OHLCV snapshots with
  deterministic provenance.

### ✅ SAS-V1-005: Multimodal Claim Extraction V1

Owner:      codex + operator
Phase:      27
Type:       validation
Depends-On: SAS-V1-003

Objective: |
  Include reviewed public audio transcript and image/OCR evidence in the same
  normalized claim surface used for text, while keeping unreviewed media
  internal-only.

Acceptance-Criteria:
  - id: AC-1
    description: "A three-channel media inventory identifies public audio/image/chart candidates and their authorization/review status."
    test: "manual/docs-review"
  - id: AC-2
    description: "Reviewed transcript/OCR artifacts can produce structured claim drafts with media provenance and source-document links."
    test: "tests/unit/test_multimodal_claim_extraction_v1.py"
  - id: AC-3
    description: "Unreviewed transcript/OCR/chart interpretations remain excluded from customer-facing metrics."
    test: "tests/unit/test_multimodal_claim_extraction_v1.py"

Files:
  - docs/pilot/three_channel_V1_MEDIA_INVENTORY.md
  - src/signal_sandbox/claims/
  - tests/unit/test_multimodal_claim_extraction_v1.py

Notes: |
  Completed on 2026-05-19. `three_channel_V1_MEDIA_INVENTORY.md` records the
  three-channel media posture. Reviewed transcript/OCR refs can produce
  structured claim drafts with media provenance, while unreviewed transcript,
  OCR, and chart claims remain excluded from customer-facing metrics.

### ✅ SAS-V1-006: Provider And Proxy Expansion V1

Owner:      codex
Phase:      27
Type:       code
Depends-On: SAS-V1-001

Objective: |
  Expand approved provider/proxy coverage for V1 while preserving on-demand
  fetching and compact immutable snapshot caching.

Acceptance-Criteria:
  - id: AC-1
    description: "Provider/proxy config maps approved crypto, MOEX, US equity/fund, futures/proxy, and benchmark symbols to deterministic provider paths or explicit unsupported statuses."
    test: "tests/unit/test_provider_proxy_config_v1.py"
  - id: AC-2
    description: "Market-data fetch planning requests only the approved asset/time windows needed for accepted claims."
    test: "tests/unit/test_provider_proxy_config_v1.py"
  - id: AC-3
    description: "Provider gaps are recorded as exclusions, not wins/losses."
    test: "tests/unit/test_provider_proxy_config_v1.py"

Files:
  - src/signal_sandbox/claims/provider_config.py
  - docs/pilot/three_channel_V1_APPROVAL_MATRIX.md
  - tests/unit/test_provider_proxy_config_v1.py

Notes: |
  Completed on 2026-05-19. `provider_config.py` maps approved Binance crypto
  and MOEX ISS share paths plus explicit unsupported/needs-operator provider
  classes. Fetch planning emits only approved on-demand windows and records
  provider gaps as exclusions, not wins/losses.

### ✅ SAS-V1-007: Three-Channel Metrics V1 Recompute

Owner:      codex
Phase:      27
Type:       validation
Depends-On: SAS-V1-004, SAS-V1-005, SAS-V1-006

Objective: |
  Recompute three-channel metrics using reviewed V1 extraction, level-aware
  outcomes, multimodal claims, approved providers, and explicit exclusions.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/three_channel_V1_METRIC_RESULTS.json` records coverage, clarity, hit rate, returns, MFE/MAE, RR where available, provider coverage, and exclusion counts by channel."
    test: "tests/unit/test_three_channel_metric_results_v1.py"
  - id: AC-2
    description: "`docs/pilot/three_channel_V1_SCORECARD.md` separates coverage, extraction quality, outcome quality, risk quality, and evidence limitations."
    test: "tests/unit/test_three_channel_metric_results_v1.py"
  - id: AC-3
    description: "V1 report includes deltas from V0 and explains changed counts due to false-positive review or provider expansion."
    test: "manual/docs-review"

Files:
  - docs/pilot/three_channel_V1_METRIC_RESULTS.json
  - docs/pilot/three_channel_V1_SCORECARD.md
  - scripts/three_channel_metric_report.py
  - tests/unit/test_three_channel_metric_results_v1.py

Notes: |
  Completed on 2026-05-19. V1 metrics apply `SAS-V1-002` calibration decisions
  to V0 evaluated claims, separate reviewed false positives/context rows from
  kept claims, count false negatives as pending extraction, exclude unreviewed
  media, and keep the scorecard internal until the external-ready gate passes.

### ✅ SAS-V1-008: Customer-Facing V1 Report And External Gate

Owner:      codex + operator
Phase:      27
Type:       report
Depends-On: SAS-V1-007

Objective: |
  Produce the first customer-facing candidate report and decide whether it is
  safe to use externally, with evidence links, limitations, and no future-profit
  claims.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md` presents metrics, confirmed examples, contradicted examples, exclusions, and methodology in customer-readable language."
    test: "manual/operator-review"
  - id: AC-2
    description: "`docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md` records `approve_external_delivery`, `approve_internal_only`, or `reject_external_delivery` with blockers."
    test: "manual/docs-review"
  - id: AC-3
    description: "Report contains no investment advice, no future-profit claims, no unreviewed transcript/OCR claims, and no unsupported ranking."
    test: "manual/docs-review"

Files:
  - docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md
  - docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md
  - docs/pilot/three_channel_V1_METRIC_RESULTS.json

Notes: |
  Completed on 2026-05-19. The V1 report is customer-readable but internal-only.
  The external-ready gate decision is `approve_internal_only`: useful for
  internal product validation, not approved for paid external delivery.

### ✅ SAS-V1-009: Phase 27 Deep Review

Owner:      codex
Phase:      27
Type:       review
Depends-On: SAS-V1-008

Objective: |
  Run the mandatory Phase 27 boundary review and archive the V1 report work.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks source legality, extraction calibration, provider/proxy approval, multimodal evidence posture, metric reproducibility, and report overclaim risk."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, handoff docs, and phase report are updated with final Phase 27 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any P0/P1 finding blocks external delivery until fixed."
    test: "manual/review"

Files:
  - docs/archive/PHASE27_REVIEW.md
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md
  - ORCHESTRATOR_CHECKPOINT.md

Notes: |
  Completed on 2026-05-19. Phase 27 review is archived at
  `docs/archive/PHASE27_REVIEW.md`; no P0/P1/P2 implementation findings were
  found. V1 is approved for internal product validation only; external delivery
  remains blocked by the V1 gate.

## Phase 23 — Image/OCR And Multimodal Evidence

### SAS-DR-006: Public Image Acquisition And Manifest ✅

Owner:      codex
Phase:      23
Type:       validation
Depends-On: SAS-DR-005

Objective: |
  Acquire or register public image/screenshot/chart artifacts from the expanded
  corpus with stable source linkage and checksums.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_IMAGE_MANIFEST.json` records image artifact id, source document id, media URL/ref, local path or external ref, checksum, acquisition status, and retention status."
    test: "manual-evidence plus unit tests where applicable"
  - id: AC-2
    description: "Image acquisition rejects media without public/operator authorization or source-document linkage."
    test: "tests/unit/test_media_manifest.py or manual evidence if no code path exists"
  - id: AC-3
    description: "Raw media storage policy is stated for local artifacts and no private media is committed."
    test: "manual/git-review"

Files:
  - docs/pilot/bablos79_IMAGE_MANIFEST.json
  - workspace/media/bablos79/
  - src/signal_sandbox/media/

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-23---imageocr-and-multimodal-evidence
  - docs/adr/ADR-004-media-evidence-pipeline.md

Notes: |
  Use Git LFS or external/local artifact storage later if raw media grows.

### SAS-DR-007: OCR Draft Run ✅

Owner:      codex
Phase:      23
Type:       validation
Depends-On: SAS-DR-006

Objective: |
  Run OCR over approved public images/screenshots/charts and record draft text
  with source refs and confidence/limitation notes.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_OCR_RUN_EXPANDED.md` records OCR provider/config, inputs, outputs, skipped items, failures, and draft-only status."
    test: "manual-evidence"
  - id: AC-2
    description: "OCR outputs are stored as draft artifacts and cannot approve claims, ledgers, outcomes, or report text without review."
    test: "manual/docs-review"
  - id: AC-3
    description: "Every OCR output cites image artifact id, source document id, and checksum."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_OCR_RUN_EXPANDED.md
  - docs/pilot/ocr/
  - src/signal_sandbox/media/

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-23---imageocr-and-multimodal-evidence

Notes: |
  If OCR provider is unavailable, record skipped status and exact blocker.

### SAS-DR-008: Image And Chart Review Queue ✅

Owner:      operator + codex
Phase:      23
Type:       validation
Depends-On: SAS-DR-007

Objective: |
  Review OCR/image/chart outputs and decide which media refs are usable for
  internal source joins and which require human/operator acceptance for external
  report claims.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_IMAGE_REVIEW_QUEUE.md` lists each OCR/image artifact with draft text, visible ticker/level/date evidence, review status, and reviewer action."
    test: "manual/docs-review"
  - id: AC-2
    description: "Chart interpretation is labeled as reviewed, ambiguous, unsupported, or excluded; uncertain chart claims are not outcome-ready."
    test: "manual/docs-review"
  - id: AC-3
    description: "Reviewed media refs are exported to `docs/pilot/bablos79_REVIEWED_MEDIA_EVIDENCE.md`."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_IMAGE_REVIEW_QUEUE.md
  - docs/pilot/bablos79_REVIEWED_MEDIA_EVIDENCE.md
  - docs/pilot/ocr/

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-23---imageocr-and-multimodal-evidence

Notes: |
  LLM/OCR output is not final truth.

### SAS-DR-009: Voice/Transcript Review Policy Update ✅

Owner:      operator + codex
Phase:      23
Type:       docs
Depends-On: SAS-DR-008

Objective: |
  Decide how managed Whisper and LLM-reviewed transcript refs can be used in
  internal vs external reports.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_TRANSCRIPT_ACCEPTANCE_POLICY.md` defines draft, LLM-reviewed internal, human/operator accepted, and external-claim statuses."
    test: "manual/docs-review"
  - id: AC-2
    description: "Policy states that LLM-reviewed transcript refs can support internal source joins but external delivery requires human/operator acceptance unless explicitly waived."
    test: "manual/docs-review"
  - id: AC-3
    description: "Existing Phase 21 transcript artifacts are reclassified under the policy without changing their evidence content."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_TRANSCRIPT_ACCEPTANCE_POLICY.md
  - docs/pilot/bablos79_TRANSCRIPT_LLM_REVIEW.md
  - docs/audit/PHASE21_ERROR_REGISTER.md

Context-Refs:
  - docs/pilot/bablos79_TRANSCRIPT_LLM_REVIEW.md
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-23---imageocr-and-multimodal-evidence

Notes: |
  This is a policy gate before external media-backed claims.

### SAS-DR-010: Multimodal Source Join V2 ✅

Owner:      codex
Phase:      23
Type:       validation
Depends-On: SAS-DR-009

Objective: |
  Build a second multimodal source preview joining expanded text, reviewed
  image/OCR evidence, and transcript evidence under the new acceptance policy.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_MULTIMODAL_SOURCE_PREVIEW_V2.md` summarizes text, voice, image/OCR, reviewed, draft, and excluded evidence counts."
    test: "manual/docs-review"
  - id: AC-2
    description: "Preview preserves original source document text/hash/url and cites joined media refs without changing source truth."
    test: "tests/unit/test_multimodal_source_join.py or equivalent"
  - id: AC-3
    description: "Preview separates internal-only refs from external-eligible refs."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_MULTIMODAL_SOURCE_PREVIEW_V2.md
  - src/signal_sandbox/media/
  - src/signal_sandbox/corpus/
  - tests/unit/test_multimodal_source_join.py

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-23---imageocr-and-multimodal-evidence

Notes: |
  This task changes modality scope; deep review is required at phase boundary.

### SAS-DR-011: Multimodal Evidence Deep Review ✅

Owner:      codex
Phase:      23
Type:       review
Depends-On: SAS-DR-006, SAS-DR-007, SAS-DR-008, SAS-DR-009, SAS-DR-010

Objective: |
  Run the Phase 23 boundary review and decide whether multimodal evidence is
  ready for claim-ledger extraction.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks public media authorization, OCR/transcript draft boundaries, image/chart review quality, source joins, and external-claim policy."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, handoff docs, and phase report are updated with final Phase 23 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "Any P0/P1 media-source, transcript/OCR, or external-claim issue blocks Phase 24."
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
  - ORCHESTRATOR_CHECKPOINT.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

## Phase 24 — Claim Ledger And Market Outcomes

### SAS-DR-012: Author Claim Taxonomy ✅

Owner:      codex
Phase:      24
Type:       docs
Depends-On: SAS-DR-011

Objective: |
  Define the taxonomy for author claims so extraction can distinguish
  measurable claims from broad market commentary and non-market content.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_CLAIM_TAXONOMY.md` defines macro context, event risk, directional bias, explicit trade setup, level/timing call, watchlist, non-market commentary, and unsupported media claim categories."
    test: "manual/docs-review"
  - id: AC-2
    description: "Taxonomy defines required fields for a claim to be deterministic-outcome-ready."
    test: "manual/docs-review"
  - id: AC-3
    description: "Taxonomy states that broad claims may be useful author insights even when they are not deterministic performance evidence."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_CLAIM_TAXONOMY.md
  - docs/specs/MARKET_IDEA_SCHEMA.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-24---claim-ledger-and-market-outcomes

Notes: |
  Do not force every post into a trade-signal frame.

### SAS-DR-013: Expanded Claim Ledger Draft ✅

Owner:      codex
Phase:      24
Type:       validation
Depends-On: SAS-DR-012

Objective: |
  Extract a reviewed draft claim ledger from the expanded multimodal corpus.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_CLAIM_LEDGER.json` and `.md` include claim id, source refs, media refs when used, timestamp, category, asset/proxy candidates, direction, horizon, review state, and measurability status."
    test: "manual/docs-review plus schema tests if implemented"
  - id: AC-2
    description: "Ledger includes non-market, ambiguous, unsupported, and weak claims instead of filtering them out."
    test: "manual/docs-review"
  - id: AC-3
    description: "If fewer than 30-50 reviewable claims exist, the ledger records an insufficient-corpus decision with reasons."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_CLAIM_LEDGER.json
  - docs/pilot/bablos79_CLAIM_LEDGER.md
  - src/signal_sandbox/market_ideas/
  - tests/unit/

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-24---claim-ledger-and-market-outcomes
  - docs/pilot/bablos79_CLAIM_TAXONOMY.md

Notes: |
  Draft extraction cannot create final truth without review status.

### SAS-DR-014: Market Proxy Map ✅

Owner:      operator + codex
Phase:      24
Type:       validation
Depends-On: SAS-DR-013

Objective: |
  Map measurable and broad-market claims to explicit public market proxies or
  mark them as non-measurable.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_MARKET_PROXY_MAP.md` records each measurable claim's asset/proxy, data source, timestamp basis, horizon, and unresolved reason when no proxy is safe."
    test: "manual/docs-review"
  - id: AC-2
    description: "Broad claims use approved proxy logic or remain non-measurable; no hidden proxy guessing is allowed."
    test: "manual/docs-review"
  - id: AC-3
    description: "Market-data fetch plan covers only measurable/proxy-approved claims."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_MARKET_PROXY_MAP.md
  - docs/pilot/bablos79_CLAIM_LEDGER.json
  - src/signal_sandbox/assets/
  - src/signal_sandbox/market_data/

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-24---claim-ledger-and-market-outcomes

Notes: |
  If the author says "market" broadly, do not invent a ticker unless the proxy
  is explicitly approved and disclosed.

### SAS-DR-015: Retrospective Outcome Evaluation ✅

Owner:      codex
Phase:      24
Type:       validation
Depends-On: SAS-DR-014

Objective: |
  Compute deterministic retrospective outcomes for measurable reviewed claims
  using approved public/local market data snapshots.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.json` and `.md` record outcome status, market data snapshot refs, horizons, returns, MFE/MAE where applicable, and unresolved reasons."
    test: "manual/docs-review plus outcome tests if implemented"
  - id: AC-2
    description: "Outcome evaluation separates confirmed, contradicted, unresolved, insufficient data, and non-measurable claims."
    test: "manual/docs-review"
  - id: AC-3
    description: "No outcome metric is computed for claims lacking reviewed evidence, source timestamp, approved proxy, or sufficient market data."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.json
  - docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.md
  - src/signal_sandbox/market_ideas/
  - src/signal_sandbox/market_data/
  - tests/unit/

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-24---claim-ledger-and-market-outcomes
  - docs/pilot/bablos79_MARKET_PROXY_MAP.md

Notes: |
  Retrospective outcomes are evidence, not future-performance claims.

### SAS-DR-016: Counterexample And Weak Evidence Register ✅

Owner:      codex
Phase:      24
Type:       docs
Depends-On: SAS-DR-015

Objective: |
  Preserve weak, contradicted, blocked, and non-measurable examples so the
  final author report is balanced.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_COUNTEREXAMPLES.md` includes contradicted, unresolved, ambiguous, non-measurable, and unsupported-media examples with source refs."
    test: "manual/docs-review"
  - id: AC-2
    description: "Register includes at least 5 weak/blocked/counter examples when available, or an explicit reason if fewer exist."
    test: "manual/docs-review"
  - id: AC-3
    description: "The report gate requires counterexamples to be considered before any positive author-strength conclusion."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_COUNTEREXAMPLES.md
  - docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.md
  - docs/pilot/bablos79_CLAIM_LEDGER.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#anti-cherry-pick-rule

Notes: |
  Good product evidence includes disconfirming evidence.

### SAS-DR-017: Claim Ledger Deep Review ✅

Owner:      codex
Phase:      24
Type:       review
Depends-On: SAS-DR-012, SAS-DR-013, SAS-DR-014, SAS-DR-015, SAS-DR-016

Objective: |
  Run the Phase 24 boundary review and decide whether the claim ledger and
  retrospective outcomes are strong enough for an author capability report.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks taxonomy, ledger evidence refs, media status, proxy mapping, outcome correctness, counterexamples, and no future-profit/advice claims."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, handoff docs, and phase report are updated with final Phase 24 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "If fewer than 30-50 claims or too few measurable outcomes exist, review decides whether to expand corpus again or produce an insufficient-evidence report."
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
  - ORCHESTRATOR_CHECKPOINT.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.

## Phase 25 — Author Capability Report

### SAS-DR-018: Author Capability Scorecard ✅

Owner:      codex
Phase:      25
Type:       docs
Depends-On: SAS-DR-017

Objective: |
  Build the author capability scorecard from reviewed claims, outcomes,
  examples, counterexamples, and limitations.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_AUTHOR_CAPABILITY_SCORECARD.md` scores or labels categories such as macro context, event risk, directional bias, explicit setup quality, timing/levels, media usefulness, and evidence measurability."
    test: "manual/docs-review"
  - id: AC-2
    description: "Every strength claim cites at least one supporting reviewed example and at least one limitation/counterexample when available."
    test: "manual/docs-review"
  - id: AC-3
    description: "Scorecard avoids leaderboard, marketplace, future-profit, advice, or best-channel language."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_AUTHOR_CAPABILITY_SCORECARD.md
  - docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.md
  - docs/pilot/bablos79_COUNTEREXAMPLES.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-25---author-capability-report

Notes: |
  This scorecard is retrospective evidence, not a ranking product.

### SAS-DR-019: Author Capability Report V1 ✅

Owner:      codex
Phase:      25
Type:       validation
Depends-On: SAS-DR-018

Objective: |
  Generate the buyer-readable author capability report from the validated
  ledger, outcomes, media evidence, scorecard, and limitations.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/reports/bablos79_AUTHOR_CAPABILITY_REPORT_V1.md` explains what the author appears good at, what is weak/non-measurable, and what happened later in public market data for measurable claims."
    test: "manual/docs-review"
  - id: AC-2
    description: "Report includes evidence appendix, source/media/market refs, examples, counterexamples, limitations, and no-advice boundary."
    test: "manual/docs-review"
  - id: AC-3
    description: "Report contains no buy/sell/hold recommendation, future-profit claim, marketplace ranking, leaderboard language, or unreviewed media claim."
    test: "manual/docs-review"

Files:
  - docs/pilot/reports/bablos79_AUTHOR_CAPABILITY_REPORT_V1.md
  - docs/pilot/bablos79_AUTHOR_CAPABILITY_SCORECARD.md
  - docs/pilot/bablos79_CLAIM_LEDGER.md
  - docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-25---author-capability-report

Notes: |
  If evidence remains weak, produce an insufficient-evidence report instead of
  forcing a positive narrative.

### SAS-DR-020: Deep Retrospective Demo Pack ✅

Owner:      codex
Phase:      25
Type:       docs
Depends-On: SAS-DR-019

Objective: |
  Package the author capability report into an internal demo pack suitable for
  warm conversations.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_DEEP_RETROSPECTIVE_DEMO_PACK.md` contains report summary, strongest examples, counterexamples, media evidence summary, market outcome summary, limitations, talk track, and buyer use case."
    test: "manual/docs-review"
  - id: AC-2
    description: "Demo pack makes clear whether it is external-ready, internal-only, or rejected."
    test: "manual/docs-review"
  - id: AC-3
    description: "Demo pack does not expose raw media beyond public/legal boundary and does not overstate transcript/OCR certainty."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_DEEP_RETROSPECTIVE_DEMO_PACK.md
  - docs/pilot/reports/bablos79_AUTHOR_CAPABILITY_REPORT_V1.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-25---author-capability-report

Notes: |
  Keep this pack concise enough for sales/user conversations.

### SAS-DR-021: Deep External Ready Gate ✅

Owner:      operator + codex
Phase:      25
Type:       review
Depends-On: SAS-DR-020

Objective: |
  Decide whether the deep `bablos79` retrospective can be shown externally or
  should remain internal-only/rejected.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot/bablos79_DEEP_EXTERNAL_READY_GATE.md` records ready / needs fixes / reject and cites evidence coverage, market outcomes, media review status, legal boundary, and claim safety."
    test: "manual/docs-review"
  - id: AC-2
    description: "Gate defines the paid report package scope, buyer promise, exclusions, and first feedback questions if ready."
    test: "manual/docs-review"
  - id: AC-3
    description: "Gate does not approve marketplace, leaderboard, automated advice, private scraping, or future-performance claims."
    test: "manual/docs-review"

Files:
  - docs/pilot/bablos79_DEEP_EXTERNAL_READY_GATE.md
  - docs/pilot/bablos79_DEEP_RETROSPECTIVE_DEMO_PACK.md
  - docs/pilot/reports/bablos79_AUTHOR_CAPABILITY_REPORT_V1.md

Context-Refs:
  - docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md#phase-25---author-capability-report

Notes: |
  Human/operator decision is required before external delivery.

### SAS-DR-022: Author Capability Report Deep Review ✅

Owner:      codex
Phase:      25
Type:       review
Depends-On: SAS-DR-018, SAS-DR-019, SAS-DR-020, SAS-DR-021

Objective: |
  Run the Phase 25 boundary review and close the deep channel retrospective
  loop.

Acceptance-Criteria:
  - id: AC-1
    description: "Review checks report evidence, scorecard fairness, examples/counterexamples, media claims, legal boundary, and external-ready gate."
    test: "manual/review"
  - id: AC-2
    description: "Audit index, CODEX prompt, README, handoff docs, and phase report are updated with final Phase 25 state."
    test: "manual/docs-review"
  - id: AC-3
    description: "If ready, next task is controlled external pilot feedback; if not ready, next task is the specific blocking fix or corpus expansion, not marketplace scope."
    test: "manual/review"

Files:
  - docs/archive/PHASE25_RETROSPECTIVE_REVIEW.md
  - docs/audit/REVIEW_REPORT.md
  - docs/audit/ARCH_REPORT.md
  - docs/audit/PHASE_REPORT_LATEST.md
  - docs/audit/AUDIT_INDEX.md
  - docs/CODEX_PROMPT.md
  - README.md
  - PHASE_HANDOFF.md
  - AGENT_NOTES.md
  - ORCHESTRATOR_CHECKPOINT.md

Context-Refs:
  - docs/prompts/ORCHESTRATOR.md

Notes: |
  This is a phase gate. Do not skip deep review.
