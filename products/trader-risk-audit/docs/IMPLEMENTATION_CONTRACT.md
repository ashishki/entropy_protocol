# Implementation Contract - Trader Risk Audit

Status: IMMUTABLE - changes require an ADR filed in `docs/adr/`.
Version: 1.0
Effective date: 2026-05-07

Any agent may cite this document as the authority on implementation rules. A verified violation of this contract is automatically a P1 finding unless a stricter severity is named.

---

## Universal Rules

These rules apply to every project using the AI Workflow Playbook. They are not changed without an ADR.

### SQL Safety

- All SQL is parameterized. Use `text()` with named params: `text("SELECT ... WHERE id = :id")`.
- Never interpolate variables into SQL strings.
- Never use string concatenation to build queries.

Violation: automatic P1.

### Multi-Tenant Systems

- Every database call is preceded by the appropriate tenant context (`SET LOCAL app.tenant_id = :tid` or equivalent RLS setup).
- No query executes without a tenant context in multi-tenant code paths.

Applicability: not active in v1 because Trader Risk Audit is a single-tenant local workflow. If multi-tenancy is added later, these rules become active before implementation.

Violation in any future multi-tenant code path: automatic P1.

### Async Redis

- Redis is accessed only in `async def` functions using `redis.asyncio`.
- Never import or call the synchronous redis client in async code paths.

Applicability: Redis is not part of v1. If Redis is added later, these rules apply.

Violation: automatic P1.

### Authorization

- Every new route handler enforces authorization (role check, JWT validation, or equivalent).
- Authorization is never deferred to "we'll add it later."

Applicability: there are no route handlers in v1. If an API or UI is added later, auth design requires an ADR before route implementation.

Violation: automatic P1.

### PII Policy

- No PII in log messages, span attributes, or metrics.
- Where identifiers must be logged, use hashes (SHA-256 or equivalent).
- This applies to all observability: logs, traces, and metrics.

Project PII and confidential fields include trader name, email, phone, Telegram handle, broker account id, internal account id, account balance, raw trade rows, free-text trader notes, source file contents, and paid pilot customer identifiers.

Violation: automatic P1.

### Credentials

- No credentials, API keys, or secrets in source code.
- Use environment variables.
- Document required env vars in `docs/ARCHITECTURE.md` under Runtime Contract.
- Exchange import credentials, if implemented under ADR-002, must be read-only,
  local-only, redacted in all output, and never persisted in manifests, logs,
  queue metadata, workspace metadata, reports, fixtures, or docs.

Violation: automatic P1 and a security incident.

### Tracing

- Shared tracing module: one `get_tracer()` function, imported everywhere.
- No inline noop span implementations scattered across files.
- All spans use the shared module.

Project shared tracing module: `trader_risk_audit/observability.py`.

Violation: P2, escalating to P1 at age cap.

### CI

- CI must pass before any PR is merged.
- No exceptions. No "merge now, fix CI later."

Violation: automatic P1.

## Observability

### OBS-1 - Instrumentation

Every external call (database, Redis, HTTP, LLM inference) must be wrapped in a span with `trace_id` and `operation_name`. Use `trader_risk_audit/observability.py`. Inline noop spans or copy-pasted tracer initializations are forbidden.

Applicability: core v1 has no external calls. The rule becomes active if a later task adds a database, HTTP API, Telegram bot, or LLM inference path.

Violation: P2, escalating to P1 at age cap.

### OBS-2 - Metrics

For each type of external call, emit a success/error counter and latency histogram once a metrics backend exists. Metrics labels must never contain PII or confidential trading data.

Applicability: metrics backend is not active in local v1.

Violation after metrics are introduced: P2.

### OBS-3 - Health Endpoint

`GET /health` returns `{"status": "ok"}` (HTTP 200) when the system is healthy. This endpoint must not log PII, must not count toward rate limits, and must not require authentication.

Applicability: no HTTP endpoint exists in v1. If an API is added later, this rule is mandatory.

Violation after an API is introduced: P1.

---

## Project-Specific Rules

The following rules are tailored to Trader Risk Audit and carry the same weight as universal rules.

### Deterministic Violation Truth

Final rule evaluation, P&L arithmetic, violation records, severity, report data values, and artifact hashes must be deterministic code paths. LLM output, natural-language inference, or unreviewed free-text interpretation must not determine violation truth.

Violation: automatic P1.

### Human Approval for Ambiguous Inputs

Ambiguous export mappings, ambiguous trader-written rules, unsupported rule types, new rule semantics, and paid report sends require explicit human approval before evaluation or delivery proceeds. The approval must be represented as a deterministic artifact or configuration value, not conversational memory.

Violation: automatic P1.

### Source-Row Traceability

Every violation record must include rule id, rule type, timestamp, source row id or row ids, evaluated value, threshold, severity, and message code. Report rows must preserve enough of these fields for a reviewer to trace each claim back to normalized input rows.

Violation: P1.

### Reproducibility

The same immutable export, policy file, configuration, and package version must produce identical normalized trade JSON, violation JSON, attribution JSON, report Markdown, delivery packet text, and deterministic content hashes. Generated timestamps may appear in manifests but must be excluded from deterministic content hash inputs.

Violation: P1 for evaluation/report drift; P2 for missing hash metadata.

### Confidential Data Handling

Pilot inputs and generated reports are local-only by default. Real customer exports, broker account ids, trader names, emails, Telegram handles, account balances, and notes must not be committed as fixtures. Logs and test output may include counts, rule ids, message codes, and hashes, but not raw trade data or source file contents.

Violation: automatic P1; committed real customer data is a security incident.

### Report Claim Boundaries

Reports may state deterministic violations, timestamps, thresholds, source-row evidence, and P&L attribution. Reports must not provide investment advice, promise profits, claim live trade control, present counterfactual returns, or assert that a behavior caused losses unless the claim is directly backed by deterministic fields and approved report language.

Violation: automatic P1.

### Runtime Boundary

Application runtime must not install packages, mutate shell state, manage services, call exchange write/control APIs, send Telegram messages without ADR-001 approval, or access credentials outside an approved local secret path. Development tasks and CI may install dependencies using declared files only. ADR-002 permits a future bounded read-only exchange import path for historical fills/executions only.

Violation: automatic P1 for exchange write/control/live-control paths; P2 for unapproved local runtime mutation.

---

## Control Surface and Runtime Boundaries

| Boundary | Rule |
|----------|------|
| Secrets scope | No secrets are required for core CSV audit. Optional future Telegram credentials must come from environment variables and remain disabled until approved. ADR-002 exchange import credentials must be read-only, local, and redacted. |
| Network egress | No network egress in core CSV audit. Telegram bot egress requires ADR/task approval. ADR-002 permits future bounded read-only exchange egress for historical fills/executions only; exchange write/control egress remains forbidden. |
| Privileged actions | Accepting rule interpretations, resolving ambiguous exports, adding new rule types, sending paid reports, and enabling any live integration require human approval. |
| Runtime mutation | Runtime may read local inputs and write local artifacts only. It may not install packages, modify toolchains, start services, or change credentials. |
| Persistence | Local artifacts are explicit files under operator-controlled directories. Persistent shared services are out of scope. |
| Auditability | Manifest hashes, decision log entries, implementation journal entries, tests, and audit reports are the evidence trail. |

### Runtime Tier Guardrails

- Implement only within Runtime T0 declared in `docs/ARCHITECTURE.md`.
- Treat runtime-tier expansion as a governance change, not an implementation detail.
- T0 code must not silently acquire T1/T2/T3 behaviors such as service containers, broad shell mutation, package installs at runtime, privileged runtime management, or long-lived mutable worker state.

---

## Continuity and Retrieval Rules

These rules define how prior context is retrieved without replacing canonical documents.

- Canonical authority remains: `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/spec.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, ADRs, review reports, evaluation artifacts, code, and tests.
- `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, and `docs/EVIDENCE_INDEX.md` are retrieval aids. They summarize, index, and point; they do not overrule canonical files.
- A task with `Context-Refs` must read those references before implementation begins.
- Retrieval is mandatory when changing architecture, runtime tier, auth, rule semantics, P&L attribution, report claim guardrails, retention/deletion behavior, or any open review finding.
- If work supersedes a prior decision or invalidates evidence, update the relevant retrieval artifact in the same task.

Violation: P2. Repeated violation becomes P1 at age cap.

---

## Mandatory Pre-Task Protocol

Every Codex agent must execute these steps before writing implementation code. No exceptions.

1. Read `docs/IMPLEMENTATION_CONTRACT.md` from top to bottom.
2. Read the full task in `docs/tasks.md`, including acceptance criteria, Depends-On, Files, Context-Refs, and Notes.
3. Read Depends-On tasks to understand interface contracts.
4. Read task `Context-Refs` and relevant entries in `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, and `docs/EVIDENCE_INDEX.md` when the task depends on prior decisions, proof, findings, rule semantics, attribution, retention, or report claims.
5. Run `pytest -q`. Record the output: `{N} passing, {M} failed`. If failures exist, stop and report the broken baseline.
6. Run `ruff check`. It must exit 0. If not, create a separate commit with ruff fixes, then restart the pre-task protocol.
7. Confirm every acceptance criterion in the task has a corresponding test before implementation is considered complete.

Skipping any step is a P1 finding in the next review cycle.

---

## Forbidden Actions

The following actions are never permitted. Violating these generates a P1 finding in the next review cycle unless a stricter severity is named.

| Forbidden Action | Reason |
|------------------|--------|
| String interpolation in SQL (`f"SELECT * FROM t WHERE id = {id}"`) | SQL injection; parameterized queries are unconditional. |
| Session-level `SET` in multi-tenant code paths | Leaks tenant context across requests. |
| Skipping the pre-task baseline capture | Cannot verify implementation did not break existing tests. |
| Running tests without recording the pre-change baseline | Baseline comparison is the primary correctness signal. |
| Self-closing a review finding without code verification | Findings are closed by reading code and tests, not by assertion. |
| Modifying this document without an ADR | The contract is immutable by design. |
| Deferring CI setup past Phase 1 | Every commit after Phase 1 must be CI-verified. |
| Merging a PR with failing CI | The CI gate is non-negotiable. |
| Committing credentials, secrets, real customer exports, or real broker account data | Irreversible exposure risk. |
| Expanding runtime tier or privilege surface without updating ARCHITECTURE.md and filing an ADR | Runtime escalation is a governance change. |
| Adding exchange write/control API calls, withdrawals, transfers, order placement/cancellation, leverage/margin mutation, or order-blocking behavior | Violates product scope and capital-control boundary. |
| Using AI output as final violation truth, P&L arithmetic, or report claim authority | Violates deterministic audit contract. |
| Treating retrieval aids as authority over canonical docs | Retrieval surfaces are convenience, not source of truth. |
| Leaving commented-out code in a commit | Dead code degrades readability; delete it. |
| Adding a TODO without a task reference | Orphaned TODOs accumulate and are not reviewable. |

---

## Quality Process Rules

### P2 Age Cap

Any P2 finding that remains open for more than 3 consecutive review cycles must be closed with code and tests, escalated to P1, or formally deferred to v2 with an ADR.

### Commit Granularity

One logical change per commit. If a task involves a schema, service implementation, and tests, split commits at logical boundaries. Do not use "misc fixes" commits.

### Sandbox Isolation

Tests do not share mutable state. Each test that touches the filesystem uses a temporary directory or fixture-owned path. Future database tests must use isolated temporary databases or rolled-back transactions.

### Heavy Task Evidence

Tasks with `Execution-Mode: heavy` are not complete until their Evidence artifacts exist, the verifier focus has been addressed, and `docs/EVIDENCE_INDEX.md` points to the proof.

### Evaluation Validity

Any future profile evaluation artifact entry is invalid if `Eval Source` or date is absent. "Ran evaluation" without a concrete command, script, or manual procedure is not evidence.

### Review Cycle Integrity

Review agents close findings only after verifying the fix in code and verifying a test exists that would fail without the fix.

---

## Governing Documents

| Document | Role | Mutability |
|----------|------|------------|
| `docs/ARCHITECTURE.md` | System design, runtime, capability profiles, and boundaries. | Updated through tasks; significant changes require ADR. |
| `docs/spec.md` | Product feature scope and acceptance criteria. | Human-approved scope changes only. |
| `docs/tasks.md` | Authoritative task graph and implementation contracts. | Active tasks may change before execution; completed task contracts are append-only. |
| `docs/CODEX_PROMPT.md` | Session state, baseline, next task, findings, and phase history. | Updated by orchestrator at phase boundaries and when findings change. |
| `docs/IMPLEMENTATION_CONTRACT.md` | Immutable implementation rules. | ADR required for changes. |
| `docs/DECISION_LOG.md` | Retrieval index for major decisions. | Append or mark superseded; not authority. |
| `docs/IMPLEMENTATION_JOURNAL.md` | Append-only implementation handoff notes. | Append-only. |
| `docs/EVIDENCE_INDEX.md` | Proof index for heavy tasks, reviews, and pilot evidence. | Updated when evidence is added or invalidated. |
| `docs/audit/` | Phase validation and review artifacts. | Append-only after each cycle report is finalized. |
| `docs/adr/` | Formal architectural decision records. | Append-only. |
