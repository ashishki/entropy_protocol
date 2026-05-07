# Implementation Contract — Signal Analytics Sandbox

Status: **IMMUTABLE** — changes require an Architectural Decision Record filed in `docs/adr/`.
Version: 1.0
Effective date: 2026-05-07

Any agent (codex or review) may cite this document as the authority on implementation rules. A finding that this contract was violated is automatically P1 (or P0 where noted).

---

## Universal Rules

### SQL Safety

Not currently applicable — v1 has no SQL surface (local files only). If a future ADR introduces SQLite/DuckDB:

- All SQL is parameterized. Use named parameters: `text("SELECT ... WHERE id = :id")`.
- Never interpolate variables into SQL strings (no f-strings, no `%` formatting, no `+` concatenation).
- Never use string concatenation to build any part of a query, including table or column names.
- Violation: automatic P1.

### Async Redis

Not applicable — v1 has no Redis surface. If a future ADR introduces Redis:

- Redis access only in `async def` functions via `redis.asyncio`.
- No synchronous redis client in async code paths.
- Violation: automatic P1.

### Authorization

Not applicable in v1 — no API surface, single-operator local CLI. Future hosted/multi-user mode requires an ADR; rules will then apply.

### PII Policy

The system processes only public-author handles (channel names, X handles), evidence URLs, and capture text. None of these are PII in the regulatory sense, but the following rules apply to keep observability data minimal and the contract uniform with the playbook:

- No author-handle, raw-post text, evidence URL, or operator workspace path appears in log messages, span attributes, or metric labels.
- Where identifiers must appear in observability, use the dedup-key SHA-256 (T06) or the source_id alone.
- Captured raw post text is stored only in the workspace, never in logs.
- Violation: P2 (escalates to P1 at age cap).

### Credentials and Secrets

- No credentials, API keys, tokens, passwords, or secrets in source code.
- No credentials in comments.
- No credentials in test fixtures (use placeholder strings; real values come from env vars).
- All secrets come from environment variables documented in `docs/ARCHITECTURE.md §Runtime Contract`.
- `.env` files are in `.gitignore` and are never committed.
- Violation: automatic P1 (and a security incident).

### Shared Tracing Module

- One shared tracing module: `src/signal_sandbox/observability.py` exporting `get_tracer()`.
- All code that creates spans imports from this module.
- No inline noop span implementations in individual files.
- No copy-pasted tracer initialization in individual modules.
- Violation: P2 (escalates to P1 at age cap).

### CI Gate

- CI must pass before any PR is merged.
- A PR with failing CI is never merged, regardless of deadline pressure.
- If CI is flaky, the flakiness is fixed before the PR is merged — not bypassed.
- Violation: automatic P1.

### Observability

**OBS-1 — Instrumentation.** Every external call (price-data adapter, LLM adapter, file I/O at adapter boundary) is wrapped in a span with `trace_id` and `operation_name` via `get_tracer()`. Inline noop spans or copy-pasted tracer initializations are forbidden. Violation: P2 (escalates to P1 at age cap).

**OBS-2 — Metrics.** For each adapter call, emit a structured-log success/error event with `adapter_id`, `result`, and `latency_ms`. v1 does not require Prometheus/statsd; structured-log counters are sufficient. Violation: P2.

**OBS-3 — Health endpoint (CLI substitute).** `signal-sandbox status` is the v1 substitute for `GET /health`. It must:
- Exit 0 when configuration is valid and the workspace exists; non-zero with a clear error otherwise.
- Never log raw post text, evidence URLs, author handles, or API keys.
- Make zero network calls.
- Require zero authentication (it is a local CLI).

Violation: P1.

---

## Project-Specific Rules

The following rules are tailored to Signal Analytics Sandbox. They carry the same weight as the universal rules above.

### PSR-1 — Public-Source-Only

No code path may perform authenticated scraping, scrape private Telegram groups, bypass paywalls/login walls, impersonate a source, or fetch behind any access control. Every capture path is operator-supplied or fetches a documented public endpoint declared in `docs/ARCHITECTURE.md §External Integrations`. Source eligibility is enforced at `SourceManifest` (T04) and at the URL-pattern level by `private_patterns.py` (T05).

Violation: **automatic P0** (Stop-Ship). This is a hard product/legal boundary.

### PSR-2 — Reproducibility Contract

Given the same approved ledger Parquet and the same price snapshot:
- `signal-sandbox match` produces a byte-identical outcomes Parquet file.
- `signal-sandbox report` produces a byte-identical Markdown file.
- Re-running on the same inputs produces identical SHA-256 hashes for outcomes and report.

Anything that introduces non-determinism (per-write timestamps, unsorted iteration over sets, locale-dependent rendering, floating-point summation order) is a violation.

Violation: P1.

### PSR-3 — LLM Output Is Never Truth

No code path may write an LLM-sourced extraction record into the approved ledger without explicit human review. The `LLMExtractionAdapter` (T20) returns only `status="draft_pending_review"` records; `write_ledger` refuses records whose `extraction_metadata.adapter_id` starts with `llm/` unless `reviewer_id` is set. The deterministic outcome / aggregator / report stack is forbidden from invoking any LLM.

Violation: **automatic P0**.

### PSR-4 — Cost-Cap Enforcement

Adapters that incur paid cost (paid price provider, cloud LLM provider) track `cost_usd` cumulatively per run. Once cumulative cost exceeds `SIGNAL_SANDBOX_COST_CAP_USD`, the next call raises `CostCapExceeded` and aborts the run cleanly without partial state. A cost-cap of 0 disables paid adapters entirely.

Violation: P1.

### PSR-5 — Snapshot Immutability

Once persisted, a `PriceSnapshot` (T11) is immutable on disk. Re-saving the same snapshot is byte-identical and idempotent; saving a different snapshot to the same `snapshot_id` raises `SnapshotAlreadyExists`. The matcher and report verify the snapshot's SHA-256 against its metadata at load time.

Violation: P1.

### PSR-6 — Disclaimer Integrity

The Markdown report renderer (T14) imports the canonical disclaimer string from `src/signal_sandbox/reports/disclaimers.py:CANONICAL_DISCLAIMER` and verifies its presence in the rendered report. Modifications to the canonical disclaimer require an ADR. A render that does not contain the exact canonical string raises `DisclaimerMissing`.

Violation: **automatic P0**.

### PSR-7 — Outcome Rule Citation

Every `OutcomeRecord` cites a `rule_id` from `src/signal_sandbox/outcomes/rule_registry.py`. The registry is append-only; modifying an existing rule's behavior requires a new `rule_id`. The registry's semver string is recorded in the outcomes Parquet metadata so that re-runs can verify the rule version.

Violation: P1.

### PSR-8 — Evidence Field Preservation

Every `SignalRecord` produced by any extraction adapter preserves `evidence_url`, `capture_timestamp_utc`, and `text_sha256` byte-identically from the source `CapturedPost`. No adapter may rewrite these fields. The integration-test fixture for each adapter includes a "no evidence drift" assertion.

Violation: P1.

### PSR-9 — Append-Only Rule and Template Versioning

`outcomes.rule_registry`, `extraction.rule_templates`, and the canonical disclaimer string are append-only. Modifying an existing entry's behavior requires a new versioned entry. CI enforces this via a lint check on the registries.

Violation: P1.

### PSR-10 — Phase 0 Gate

Engineering tasks (T01+) must not begin until SAS-001 and SAS-002 are explicitly acknowledged in `docs/CODEX_PROMPT.md §Phase 0 Gate Status`. The Orchestrator refuses to dispatch any T01–T20 task while Phase 0 is unacknowledged.

Violation: P1 (and a process incident).

### PSR-11 — No Forward-Looking Claims

The aggregator, the report renderer, and any string template under `src/signal_sandbox/reports/` may not produce field names, headings, or sentences that imply prediction (e.g., "expected return", "projected win rate", "probability of next signal"). Allowed phrasing is explicitly historical (e.g., "historical win rate", "historical drawdown over evaluated signals"). CI runs a lint check (`tests/lint/test_no_forward_looking_strings.py`) over `src/signal_sandbox/reports/` and `src/signal_sandbox/outcomes/`.

Violation: P1.

---

## Control Surface and Runtime Boundaries

| Boundary | Rule |
|----------|------|
| Secrets scope | Adapter API keys (paid price, cloud LLM) are read from env at adapter construction; no secret persists outside process memory. |
| Network egress | Default config makes zero network calls. Network is opened only by an explicitly active adapter (exchange-public, paid price, cloud LLM). |
| Privileged actions | None. The CLI runs unprivileged on the operator's workstation. |
| Runtime mutation | None. No shell, package, or toolchain mutation at runtime. |
| Persistence | Local files in the operator workspace; no long-lived worker, no daemon. |
| Auditability | Every adapter call is logged via OBS-1/OBS-2; every report cites snapshot + ledger SHA-256. |

### Runtime Tier Guardrails

- Implement only within Runtime tier T0 declared in `docs/ARCHITECTURE.md`.
- Treat runtime-tier expansion as a governance change, not an implementation detail.
- The project must not silently acquire T1/T2/T3 behaviors (long-running daemons, container orchestration, persistent privileged worker, broad shell mutation).

T2/T3 conditional rules are not applicable to this project. Do not import the Hermes Agent T3 baseline.

---

## Continuity and Retrieval Rules

- Canonical authority remains: `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md` (this file), `docs/tasks.md`, `docs/CODEX_PROMPT.md`, ADRs, review reports, evaluation artifacts, code, tests.
- `docs/DECISION_LOG.md` and `docs/IMPLEMENTATION_JOURNAL.md` are retrieval aids. They summarize, index, and point; they do not overrule canonical files.
- `docs/EVIDENCE_INDEX.md` is deferred in v1 — heavy-task evidence is captured in `docs/audit/HEAVY_T{NN}_EVIDENCE.md` files referenced from each heavy task.
- A task with `Context-Refs` reads those references before implementation begins.
- Retrieval is mandatory when changing architecture, runtime, the public-source-only boundary, the reproducibility contract, the cost-cap mechanism, the disclaimer string, the outcome rule registry, or any open review finding.
- If a task supersedes a prior decision or invalidates evidence, update the retrieval artifact in the same task.

Violation: P2. Repeated violation becomes P1 at age cap.

---

## Mandatory Pre-Task Protocol

Every codex agent must execute these steps before writing any implementation code. No exceptions.

1. Read `docs/IMPLEMENTATION_CONTRACT.md` (this file) from top to bottom.
2. Read the full task in `docs/tasks.md`, including all acceptance criteria, the Depends-On list, and the Notes section.
3. Read all Depends-On tasks to understand the interface contracts your implementation must satisfy.
4. Read the task's `Context-Refs` and the relevant entries in `docs/DECISION_LOG.md` and `docs/IMPLEMENTATION_JOURNAL.md` when the task depends on prior decisions, proof, or findings.
5. Run `python -m pytest tests/ -q`. Record `{N passing, M failed}`. If M > 0, stop and report — you do not start on a broken baseline.
6. Run `ruff check src/ tests/`. Must exit 0. If not, create a separate commit with ruff fixes, then restart the pre-task protocol.
7. Confirm every acceptance criterion in the task will have a corresponding test before implementation is considered complete.

Skipping any step is a P1 finding in the next review cycle.

---

## Forbidden Actions

| Forbidden Action | Reason |
|-----------------|--------|
| Authenticated scraping or scraping behind any access control | PSR-1; legal/ToS boundary; automatic P0 |
| Writing an LLM-sourced extraction record into the approved ledger without `reviewer_id` | PSR-3; automatic P0 |
| Removing or modifying the canonical non-advice disclaimer in `src/signal_sandbox/reports/disclaimers.py` without an ADR | PSR-6; automatic P0 |
| Modifying an existing entry in `outcomes.rule_registry` or `extraction.rule_templates` (instead of appending a new version) | PSR-7, PSR-9; P1 |
| Mutating a persisted `PriceSnapshot` on disk | PSR-5; P1 |
| Bypassing `SIGNAL_SANDBOX_COST_CAP_USD` enforcement | PSR-4; P1 |
| Field names or strings in `src/signal_sandbox/reports/` or `outcomes/` that imply prediction | PSR-11; P1 |
| String interpolation in any future SQL query | SQL injection (universal rule); P1 |
| Skipping the pre-task baseline capture (`pytest`) | Cannot verify the implementation did not break existing tests; P1 |
| Self-closing a review finding without showing the code change | Findings are verified by reading code, not by assertion; P1 |
| Modifying this document without an ADR | The contract is immutable by design; P1 |
| Deferring CI setup past Phase 1 | Every commit must be CI-verified; P1 |
| Merging a PR with failing CI | The CI gate is non-negotiable; P1 |
| Committing credentials or secrets of any kind | Irreversible exposure; P1 (security incident) |
| Treating `DECISION_LOG.md` or `IMPLEMENTATION_JOURNAL.md` as authority over canonical docs | Retrieval surfaces are convenience, not source of truth; P2 |
| Leaving commented-out code in a commit | Dead code; delete it; P3 |
| Adding a TODO without a task reference (`# TODO: see T-NN`) | Orphaned TODOs accumulate and are never addressed; P3 |
| Beginning any T01+ engineering task while Phase 0 (SAS-001/SAS-002) is unacknowledged in CODEX_PROMPT | PSR-10; P1 process incident |

---

## Quality Process Rules

### P2 Age Cap

Any P2 finding open for more than 3 consecutive review cycles must be:
- Closed (resolved with a code change and a passing test), OR
- Escalated to P1 (and resolved before the next phase gate), OR
- Formally deferred to v2 (with an ADR removing it from open findings)

A P2 finding cannot age silently.

### Commit Granularity

One logical change per commit. A task that includes a schema, a service, and tests is at minimum three commits. Never bundle unrelated changes. "Misc fixes" is not a commit message.

### Sandbox Isolation

Tests do not share mutable state. File-touching tests use `tmp_path` fixtures; tests that exercise the workspace use `tmp_path / "workspace"` and never share the operator's workspace.

### Evaluation Validity

Any evaluation entry (e.g., `docs/audit/HEAVY_T20_EVIDENCE.md` or future `docs/extraction_eval.md`) is **invalid** if either of the following is true:
- `Eval Source` (the exact command, script, or method) is absent or blank.
- `Date` / timestamp is absent or blank.

An invalid entry is treated as a missing evaluation. The task is not complete regardless of whether tests pass.

### Review Cycle Integrity

Review agents close findings only after verifying the fix in code. A finding is not closed because the codex agent claims it was fixed. It is closed because a review agent read the relevant code and confirmed the fix.

---

## Governing Documents

| Document | Path | Role |
|----------|------|------|
| Architecture | `docs/ARCHITECTURE.md` | System design authority — what the system is and why |
| Specification | `docs/spec.md` | Feature authority — what the system does |
| Task graph | `docs/tasks.md` | Implementation authority — what each agent builds |
| Session handoff | `docs/CODEX_PROMPT.md` | State authority — current baseline, open findings, next task |
| This document | `docs/IMPLEMENTATION_CONTRACT.md` | Rule authority — immutable implementation rules |
| Review reports | `docs/audit/CYCLE{N}_REVIEW.md` | Finding authority — official record of review cycles |
| ADRs | `docs/adr/ADR{NNN}.md` | Decision authority — architectural decisions and their rationale |
| Legal/risk memo | `docs/legal_risk_memo.md` (created by SAS-002) | Source-eligibility authority |
| Pilot log | `docs/PILOT_LOG.md` (created by SAS-001) | Demand-validation authority |
| Heavy-task evidence | `docs/audit/HEAVY_T{NN}_EVIDENCE.md` | Per-heavy-task proof index |

In case of conflict between documents, the precedence order is:
1. This document (IMPLEMENTATION_CONTRACT.md) — highest authority for rules
2. `docs/adr/` — overrides architecture and spec when a formal decision was made
3. `docs/ARCHITECTURE.md` — overrides spec for technical design
4. `docs/spec.md` — overrides tasks for feature scope
5. `docs/tasks.md` — overrides CODEX_PROMPT for task-level details
