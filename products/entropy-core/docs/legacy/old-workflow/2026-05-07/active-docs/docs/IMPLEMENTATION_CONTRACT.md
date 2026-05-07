# Implementation Contract — Entropy Protocol

Status: **IMMUTABLE** — changes to this document require an Architectural Decision Record filed in `products/entropy-core/docs/adr/`.
Version: 1.0
Effective date: 2026-05-01

Any agent (Codex or review) may cite this document as the authority on implementation rules. Any finding that this contract was violated is automatically P1.

---

## Universal Rules

These rules apply to every project using the AI Workflow Playbook. They are not negotiable and are not changed without an ADR.

### SQL Safety

- All SQL is parameterized. Use `text()` with named parameters: `text("SELECT ... WHERE id = :id")` with `{"id": value}`.
- Never interpolate variables into SQL strings. This includes f-strings, `%` formatting, and `+` concatenation.
- Never use string concatenation to build any part of a query, including table names, column names, or `ORDER BY` clauses.
- Violation: automatic P1.

### Multi-Tenant Systems

_Not applicable. Entropy Protocol is single-tenant. This section is intentionally omitted._

### Authorization

- Entropy Protocol v1 is single-tenant with no external authentication. All operations are performed by the solo researcher/operator.
- If a route or CLI command is intentionally unrestricted, document it explicitly with a comment citing this design decision.
- No auth deferral pattern is acceptable for any future multi-user or networked exposure of this system.
- Violation: automatic P1.

### PII Policy

- No PII in log messages (`logger.info`, `logger.warning`, `logger.error`, etc.).
- No PII in span attributes (OpenTelemetry or any other tracing system).
- No PII in metrics labels or metric values.
- No PII in error messages.
- Fields considered PII in this project: none (the system processes only market data — OHLCV prices, volumes, timestamps — and internal strategy artifacts). No user PII exists in Entropy Protocol v1.
- Violation: automatic P1.

### Credentials and Secrets

- No credentials, API keys, tokens, passwords, or secrets in source code.
- No credentials in comments.
- No credentials in test fixtures (use test-key or equivalent placeholder strings in tests; real values come from environment variables).
- All secrets come from environment variables. Document required env vars in `products/entropy-core/docs/ARCHITECTURE.md` under Runtime Contract.
- `.env` files are in `.gitignore` and are never committed.
- Violation: automatic P1 (and a security incident).

### Shared Tracing Module

- One shared tracing module: `src/entropy/tracing.py` with a single `get_tracer()` function.
- All code that creates spans imports from this module.
- No inline noop span implementations in individual files.
- No copy-pasted tracer initialization in individual modules.
- Violation: P2 (accumulates; becomes P1 at age cap).

### CI Gate

- CI must pass before any PR is merged.
- A PR with failing CI is never merged, regardless of deadline pressure.
- If CI is flaky (non-deterministic failures), the flakiness is fixed before the PR is merged — not bypassed.
- Violation: automatic P1.

### Observability

These rules ensure the system is observable in production. They apply to all projects and all profiles.

**OBS-1 — Instrumentation.** Every external call (database, DuckDB, HTTP) must be wrapped in a span with `trace_id` and `operation_name`. Use the shared tracing module (`src/entropy/tracing.py`). Inline noop spans or copy-pasted tracer initializations are forbidden (see §Shared Tracing Module). Violation: P2 (escalates to P1 at age cap).

**OBS-2 — Metrics.** For each type of external call, emit a success/error counter and a latency histogram. Tool choice is declared in `products/entropy-core/docs/ARCHITECTURE.md §Observability` and used consistently. In Entropy Protocol v1, all Capability Profiles are OFF; no profile-specific metrics are required. Violation for missing database call counters (when implemented): P2.

**OBS-3 — Health endpoint.** `entropy health` CLI command returns `{"status": "ok"}` (exit 0) when the system is healthy. This command must not log PII and must not require authentication. Staleness information (e.g., last ingest timestamp) is exposed here, not in application logs. Violation: P1.

---

## Project-Specific Rules

The following rules are tailored to Entropy Protocol based on its protocol spec and governance constraints. They carry the same weight as the universal rules above.

### Registry Append-Only

All writes to the `trial_registry` and `governance_events` tables must be INSERT-only. No UPDATE or DELETE statement may be issued against these tables through any application code path.

Rationale: The append-only constraint is the technical enforcement of the protocol's preregistration integrity requirement. Any modification of a registered trial spec or governance event would invalidate the audit trail and undermine the reproducibility guarantee.

Enforcement: Application code must use INSERT-only ORM calls. Alembic migrations must not add UPDATE or DELETE triggers. Any code path that calls `.update()` or `.delete()` on these tables raises `RegistryMutationError` at the application layer.

Violation: P1.

### Run Reproducibility

Every RunRecord written to the `runs` table must include all five reproducibility fields: `trial_id`, `dataset_hash`, `code_hash`, `policy_hash`, and `simbroker_version`. A RunRecord with any of these fields absent or None is considered incomplete and must not be persisted.

Rationale: Reproducibility of every evaluation run is a core protocol requirement. A run without complete hashes cannot be independently verified or reproduced.

Enforcement: The walk-forward runner raises `IncompleteRunRecordError` before any DB write if any of the five fields is None. Unit tests must cover this rejection path.

Violation: P1.

### OOS Separation Enforcement

No code path may read OOS data during IS computation or feature engineering. The leakage detection checklist (T19) must run and pass on the IS window before any OOS evaluation begins.

Rationale: This is the technical implementation of protocol spec NN-3. Any leakage of OOS data into IS computation invalidates the OOS label and the reproducibility guarantee. The walk-forward runner enforces this by raising `LeakageBlockError` if the leakage check has not passed before OOS evaluation.

Enforcement: The `splitter.py` module raises `LeakageError` if IS data includes future features. The `runner.py` module raises `LeakageBlockError` if `run_checklist()` has not been called and returned PASS before `run_oos()` is called.

Violation: P0.

### Hash Determinism

The dataset hash must be computed from SHA-256 of sorted rows + schema fingerprint. The same dataset (identical rows, identical schema) must always produce the same hash regardless of row insertion order or invocation order.

Rationale: Hash determinism is the foundation of reproducibility. If the same dataset produces different hashes across ingestion runs, the registry integrity is broken and cross-run comparisons are invalid.

Enforcement: The hashing module sorts rows by all columns before computing the SHA-256. Tests verify that permuted row order produces the same hash. The schema fingerprint includes all column names and types in sorted order.

Violation: P1.

### Net Sharpe Stream Boundary

Net Sharpe is computed only from P&L streams (a)+(b)+(c). Stream (d) carry/funding must never be included in the net Sharpe computation. Stream (d) is reported separately in all performance reports, explicitly labeled.

Rationale: This is protocol spec Non-Negotiable NN-2. Blending stream (d) into the primary metric would mask the actual trading edge and violate the four-stream attribution requirement.

Enforcement: The `compute_net_sharpe()` function accepts only a `PnLStreams` object. The function internally uses only `.stream_a + .stream_b + .stream_c`. Passing `.stream_d` directly raises `StreamBoundaryError`. Tests verify this boundary with a worked example.

Violation: P1.

### Phase Gate Human Approval

No phase gate may be marked PASSED in code or documentation without a human approval comment in the `governance_events` table. The approval must reference the specific phase gate, the approver identity, and the date.

Rationale: The protocol spec requires human approval for phase transitions. Automated approval of phase gates would undermine the governance framework.

Enforcement: The phase gate evidence generator checks for a `GovernanceEvent` of type `PHASE_GATE` with status `APPROVED` before marking a gate as PASSED in the output report. Tests verify that the gate report reflects NOT_APPROVED if no matching event exists.

Violation: P1.

### Language Escalation Control

Python is the only active implementation language for Phase 0/1 unless a language-escalation ADR is approved before code is added.

Rationale: Introducing Rust, Go, C, C++, FFI, native extensions, or additional runtime services changes the build chain, CI surface, debugging model, packaging assumptions, and solo maintenance burden. Performance work is allowed only when a measured bottleneck exists.

Required before adding any non-Python implementation:

1. A reproducible benchmark showing the Python/Polars/DuckDB baseline, the target threshold, and the candidate language result.
2. An ADR in `products/entropy-core/docs/adr/` documenting the bottleneck, selected language, affected modules, CI/toolchain changes, packaging strategy, ownership burden, and rollback plan.
3. Updates to `products/entropy-core/docs/ARCHITECTURE.md`, CI, and `products/entropy-core/docs/tasks.md`.
4. Explicit human approval before implementation begins.

Prohibited without escalation: Rust crates, Go modules, C/C++ sources, FFI bindings, native extension build systems, second runtime services, or package manager/toolchain additions outside the Python stack.

Profiling gate timing:

- The first language-escalation profiling gate is after T20 Walk-Forward Runner, when a representative Phase 0 execution path exists.
- The second profiling gate is after formula-bearing numerical tasks are implemented or explicitly waived, because those tasks may introduce a different compute profile.
- Profiling before T20 may guide Python optimization only; it does not authorize another implementation language by itself.

Violation: P1.

---

## Control Surface and Runtime Boundaries

| Boundary | Rule |
|----------|------|
| Secrets scope | All secrets (DATABASE_URL) are in environment variables. Only the application process and CI runner may access them. No secrets in source code, comments, fixtures, or logs. |
| Network egress | No external network egress in Phase 0 v1. Data ingestion uses local fixture files only. Any future provider adapter must be declared in products/entropy-core/docs/ARCHITECTURE.md §External Integrations before egress is opened. |
| Privileged actions | Alembic migrations are the only schema-mutating actions and run explicitly by the operator. No application code runs DDL. No privileged shell actions. |
| Runtime mutation | No shell mutation, no package installation from application code, no service reconfiguration. The application is a bounded process on a local workstation. |
| Persistence | Trial registry and governance events are append-only in PostgreSQL. Run records are immutable after insertion. Parquet files are versioned and immutable (new hash = new file). |
| Auditability | All governance state transitions are logged as GovernanceEvents in the DB. The EVIDENCE_INDEX records proof artifacts for heavy tasks and phase gates. |

### Runtime Tier Guardrails

- Entropy Protocol is Runtime tier T1. All implementation must stay within T1 boundaries.
- No shell mutation, no ad-hoc package installs from application code, no privileged runtime management, no long-lived mutable worker state beyond PostgreSQL persistence.
- A T1 project must not silently acquire T2/T3 behaviors.

---

## Mandatory Pre-Task Protocol

Every Codex agent must execute these steps before writing any implementation code. No exceptions.

1. Read `products/entropy-core/docs/IMPLEMENTATION_CONTRACT.md` (this file) from top to bottom.
2. Read the full task in `products/entropy-core/docs/tasks.md`, including all acceptance criteria, the Depends-On list, and the Notes section.
3. Read all Depends-On tasks to understand the interface contracts your implementation must satisfy.
4. Read the task's `Context-Refs` and the relevant entries in `products/entropy-core/docs/DECISION_LOG.md`, `products/entropy-core/docs/IMPLEMENTATION_JOURNAL.md`, and `products/entropy-core/docs/EVIDENCE_INDEX.md` when the task depends on prior decisions, proof, or findings.
5. From `products/entropy-core/`, run `.venv/bin/python -m pytest -q tests/`. Record the output: `{N} passing, {M} failed`. If M > 0, stop and report — you do not start on a broken baseline.
6. From `products/entropy-core/`, run `.venv/bin/python -m ruff check src/entropy tests`. Must exit 0. If not, create a separate commit with ruff fixes, then restart the pre-task protocol.
7. Confirm that every acceptance criterion in the task will have a corresponding test before implementation is considered complete.

Skipping any step in this protocol is a P1 finding in the next review cycle.

---

## Forbidden Actions

The following actions are never permitted. Violating these generates a P1 finding in the next review cycle.

| Forbidden Action | Reason |
|-----------------|--------|
| String interpolation in SQL (`f"SELECT * FROM t WHERE id = {id}"`) | SQL injection; parameterized queries are unconditional |
| UPDATE or DELETE on trial_registry or governance_events | Registry append-only rule; see §Registry Append-Only |
| Skipping the pre-task baseline capture | Cannot verify implementation did not break existing tests |
| Self-closing a review finding without showing the code change | Findings are verified by reading code, not by assertion |
| Modifying this document without an ADR | The contract is immutable by design |
| Adding Rust, Go, C, C++, FFI, native extensions, or another runtime service without a language-escalation ADR | Multi-language implementation changes CI, packaging, runtime, and maintenance burden |
| Deferring CI setup past Phase 1 | Every commit must be CI-verified |
| Merging a PR with failing CI | The CI gate is non-negotiable |
| Committing credentials or secrets of any kind | Irreversible exposure |
| Expanding runtime tier or privilege surface without updating ARCHITECTURE.md / ADRs | Runtime escalation is a governance change |
| Treating `DECISION_LOG.md`, `IMPLEMENTATION_JOURNAL.md`, or `EVIDENCE_INDEX.md` as authority over canonical docs | Retrieval surfaces are convenience, not source of truth |
| Leaving commented-out code in a commit | Dead code degrades readability; delete it |
| Adding a TODO without a task reference | Orphaned TODOs accumulate and are never addressed |
| Labeling a result as OOS before T19 leakage check passes on a registered run | Violates protocol spec NN-3 and OOS Separation rule |
| Writing to trial_registry without all required hashes present | Violates Run Reproducibility and Registry Append-Only rules |
| Modifying PROTOCOL_SPEC.md, CHARTER.md, or GLOSSARY.md without human approval | These documents require charter-level review for any change |

---

## Continuity and Retrieval Rules

### Canonical vs Retrieval Boundary

Canonical documents define authority and must be read directly before implementation decisions:

| Authority Type | Canonical Source |
|----------------|------------------|
| Implementation rules | `products/entropy-core/docs/IMPLEMENTATION_CONTRACT.md` |
| Technical architecture | `products/entropy-core/docs/ARCHITECTURE.md` |
| Feature scope | `products/entropy-core/docs/spec.md` |
| Task scope and acceptance criteria | `products/entropy-core/docs/tasks.md` |
| Session state | `products/entropy-core/docs/CODEX_PROMPT.md` |
| Protocol governance | `products/entropy-core/docs/core/PROTOCOL_SPEC.md`, `products/entropy-core/docs/core/CHARTER.md`, `products/entropy-core/docs/core/GLOSSARY.md` |
| Review findings | `products/entropy-core/docs/audit/archive/phase_reviews/PHASE1_AUDIT.md` and subsequent review reports |

Retrieval aids are indexes and memory surfaces only:

| Retrieval Aid | Allowed Use | Not Allowed |
|---------------|-------------|-------------|
| `products/entropy-core/docs/DECISION_LOG.md` | Find decisions and their canonical source | Override a canonical document |
| `products/entropy-core/docs/IMPLEMENTATION_JOURNAL.md` | Recover recent session context and handoff notes | Authorize implementation changes |
| `products/entropy-core/docs/EVIDENCE_INDEX.md` | Locate tests, reports, and proof artifacts | Declare a finding closed without verification |

If a retrieval aid conflicts with a canonical source, the canonical source wins and the retrieval aid must be corrected.

### Required Lookup Triggers

An agent must read continuity artifacts before proceeding when any of the following are true:

- The task has non-empty `Depends-On` entries.
- The task lists `Context-Refs`.
- The task touches registry, governance, evidence, walk-forward, leakage, SimBroker, attribution, or phase-gate code.
- A prior review finding, audit report, or implementation note is referenced by the task.
- The agent is resuming work after an interrupted or incomplete session.
- The proposed change modifies a file listed in `products/entropy-core/docs/EVIDENCE_INDEX.md`.

Minimum lookup set for these cases: relevant rows in `products/entropy-core/docs/DECISION_LOG.md`, latest entries in `products/entropy-core/docs/IMPLEMENTATION_JOURNAL.md`, and relevant rows in `products/entropy-core/docs/EVIDENCE_INDEX.md`.

### Write-Side Rules

- Append to `products/entropy-core/docs/DECISION_LOG.md` when a technical decision affects architecture, runtime boundaries, data model shape, provider strategy, migration strategy, or task sequencing. Every entry must point to a canonical source or ADR.
- Append to `products/entropy-core/docs/IMPLEMENTATION_JOURNAL.md` after each implementation session that changes code, tests, migrations, CI, or generated project governance files. Include date, task ID, files changed, tests run, and unresolved follow-ups.
- Update `products/entropy-core/docs/EVIDENCE_INDEX.md` when adding or changing a test, report, migration check, phase-gate artifact, or audit evidence artifact used by acceptance criteria.
- Do not overwrite historical continuity entries. Corrections are new dated entries that reference the corrected prior entry.

---

## Quality Process Rules

### P2 Age Cap

Any P2 finding that remains open for more than 3 consecutive review cycles must be:
- Closed (resolved with a code change and a passing test), OR
- Escalated to P1 (and resolved before the next phase gate), OR
- Formally deferred to v2 (with an ADR filed in `products/entropy-core/docs/adr/`, removing it from open findings)

A P2 finding cannot be silently aged out. The Age Cap rule prevents the finding backlog from becoming a graveyard.

### Commit Granularity

One logical change per commit. If a task involves a database migration, a service implementation, and tests, that is at minimum three commits. Never bundle unrelated changes in a single commit. "Misc fixes" is not a commit message.

### Sandbox Isolation

Tests do not share state. Each test that touches the database uses a transaction that is rolled back at the end of the test (or uses a fresh database per test run). Tests that share mutable state produce non-deterministic results and are treated as broken tests.

### Evaluation Validity

An evaluation artifact entry is **invalid** if either of the following is true:

- `Eval Source` is absent or blank — every metrics entry must identify the exact command, script, or method that produced the numbers.
- `Date` / timestamp is absent or blank.

An invalid entry is treated as a missing evaluation. The task is not complete regardless of whether tests pass.

### Review Cycle Integrity

Review agents close findings only after verifying the fix in code. A finding is not closed because the Codex agent claims it was fixed. It is closed because a review agent read the relevant code and confirmed the fix is present and correct.

---

## Governing Documents

| Document | Path | Role |
|----------|------|------|
| Architecture | `products/entropy-core/docs/ARCHITECTURE.md` | System design authority — what the system is and why |
| Specification | `products/entropy-core/docs/spec.md` | Feature authority — what the system does |
| Task graph | `products/entropy-core/docs/tasks.md` | Implementation authority — what each agent builds |
| Session handoff | `products/entropy-core/docs/CODEX_PROMPT.md` | State authority — current baseline, open findings, next task |
| This document | `products/entropy-core/docs/IMPLEMENTATION_CONTRACT.md` | Rule authority — immutable implementation rules |
| Review reports | `products/entropy-core/docs/audit/CYCLE{N}_REVIEW.md` | Finding authority — official record of review cycles |
| ADRs | `products/entropy-core/docs/adr/ADR{NNN}.md` | Decision authority — architectural decisions and their rationale |
| Protocol spec | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` | Protocol authority — canonical research governance rules |
| Charter | `products/entropy-core/docs/core/CHARTER.md` | Strategic authority — frozen non-negotiables and kill criteria |

In case of conflict between documents, the precedence order is:
1. This document (IMPLEMENTATION_CONTRACT.md) — highest authority for implementation rules
2. products/entropy-core/docs/core/PROTOCOL_SPEC.md — overrides architecture and spec for protocol-level rules
3. products/entropy-core/docs/adr/ — overrides architecture and spec when a formal decision was made
4. products/entropy-core/docs/ARCHITECTURE.md — overrides spec for technical design
5. products/entropy-core/docs/spec.md — overrides tasks for feature scope
6. products/entropy-core/docs/tasks.md — overrides CODEX_PROMPT for task-level details
