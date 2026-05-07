# Implementation Contract - Entropy Core

Status: IMMUTABLE - changes require an ADR filed in `docs/adr/`.
Version: 1.0
Effective date: 2026-05-07

Any agent may cite this document as the authority on implementation rules. A verified contract violation is automatically P1 unless a stricter severity is named.

---

## Universal Rules

### SQL Safety

- All SQL is parameterized. Use `text()` with named params: `text("SELECT ... WHERE id = :id")`.
- Never interpolate variables into SQL strings.
- Never use string concatenation to build queries.

Violation: automatic P1.

### Multi-Tenant Systems

Entropy Core v1 is single-tenant. If multi-tenancy is introduced later, every tenant-scoped database call must enforce tenant context before any query and the architecture must be updated by ADR.

Violation in future multi-tenant code: automatic P1.

### Async Redis

Redis is not active in v1. If Redis is added later, use `redis.asyncio` in async code and never call synchronous Redis from async paths.

Violation after Redis is introduced: automatic P1.

### Authorization

V1 has no HTTP routes or external auth. If an API, UI, service, or multi-user workflow is added, authentication and authorization must be designed before route implementation. Auth is never deferred.

Violation after a network/user surface is introduced: automatic P1.

### PII Policy

- No PII in logs, span attributes, metrics, or error messages.
- Core v1 should not introduce user PII.
- Confidential strategy specs, registry records, governance events, product pilot data, secrets, raw customer artifacts, and non-public evidence payloads must not appear in logs or fixtures unless anonymized.

Violation: automatic P1.

### Credentials and Secrets

- No credentials, API keys, tokens, passwords, or secrets in source code.
- No credentials in comments.
- No credentials in fixtures.
- Secrets come from environment variables and are documented in `docs/ARCHITECTURE.md`.
- `.env` files are never committed.

Violation: automatic P1 and security incident.

### Shared Tracing Module

- One shared tracing module: `src/entropy/tracing.py` with `get_tracer()`.
- All code that creates spans imports from this module.
- No inline noop span implementations.
- No copy-pasted tracer initialization.

Violation: P2, escalating to P1 at age cap.

### CI Gate

- CI must pass before any PR is merged.
- Failing or flaky CI is fixed before merge.

Violation: automatic P1.

## Observability

- Every external call to PostgreSQL, DuckDB, HTTP/provider APIs, or future service dependencies must be wrapped in a span through `src/entropy/tracing.py`.
- Metrics must not include secrets, PII, raw strategy payloads, or raw customer/product pilot data.
- Health/status commands must not expose confidential payloads.

## Project-Specific Rules

### Registry Append-Only

`trial_registry`, governance events, and any reset-era append-only governance tables are INSERT-only through application code. Corrections are new events or records, not UPDATE/DELETE.

Violation: P1.

### Hash and Run Reproducibility

Registered/evaluation outputs must bind dataset hash, code hash, policy/config hash, and relevant run/report hashes before an evidence packet can be considered admissible.

Violation: P1.

### Leakage and Holdout Boundary

No OOS/performance label, holdout read, holdout unlock, or claim escalation may occur unless the explicit leakage/holdout gate passes and human approval is recorded where required.

Violation: P0 for holdout or leakage bypass; P1 for incomplete evidence.

### No Live Trading Boundary

Live broker/exchange APIs, live feeds by default, live capital, order blocking, production labels, and capital-ready labels are forbidden in v1 unless an explicit future gate and ADR change scope.

Violation: automatic P1.

### Deterministic Runtime Truth

Registry writes, gate decisions, metric computation, leakage status, risk rule truth, evidence truth, and report claim status are deterministic. LLM output may not own these values.

Violation: automatic P1.

### Product Bridge Boundary

Product workspaces may reuse Core only through approved bridge contracts. A bridge must list allowed primitives, forbidden calls, schemas, and human gates before implementation.

Violation: P1.

### Language Escalation Control

Python 3.12 is the active runtime. Any Rust, Go, C/C++, native extension, FFI, or second runtime service requires benchmark evidence, ADR, CI/toolchain plan, rollback plan, and human approval before code is added.

Violation: automatic P1.

## Control Surface and Runtime Boundaries

| Boundary | Rule |
|----------|------|
| Secrets scope | Environment variables only; primarily `DATABASE_URL`. |
| Network egress | No external egress by default. Future providers require ADR/task approval. |
| Privileged actions | Alembic migrations run explicitly. App code does not run privileged DDL or shell mutation. |
| Runtime mutation | No package installs, service reconfiguration, toolchain mutation, or long-lived mutable workers from runtime. |
| Persistence | PostgreSQL metadata and local immutable artifacts. Append-only records are corrected by new records. |
| Auditability | Evidence index, audit reports, decision log, implementation journal, and tests. |

## Continuity and Retrieval Rules

- Canonical authority remains `docs/ARCHITECTURE.md`, this contract, `docs/spec.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/core/`, `docs/governance/`, ADRs, code, tests, migrations, and audit reports.
- `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, and `docs/legacy/CORE_LEGACY_SUMMARY.md` are retrieval aids only.
- Old workflow files under `docs/legacy/old-workflow/2026-05-07/` are historical. Read them only when a task has a scoped `Context-Refs` pointer.
- Retrieval is mandatory when changing registry, governance, leakage, holdout, attribution, report claims, migrations, product bridges, or runtime/language boundaries.

Violation: P2, repeated violation becomes P1.

## Mandatory Pre-Task Protocol

1. Read `docs/IMPLEMENTATION_CONTRACT.md`.
2. Read the current task in `docs/tasks.md`.
3. Read Depends-On tasks.
4. Read `Context-Refs` and scoped continuity artifacts for risky boundaries.
5. Run and record the pre-task baseline using relevant verification defaults from `docs/CODEX_PROMPT.md`.
6. Run ruff before implementation; fix unrelated ruff failures separately.
7. Ensure every acceptance criterion has a test.

Skipping any step is P1.

## Forbidden Actions

| Forbidden Action | Reason |
|------------------|--------|
| String interpolation in SQL | SQL injection risk. |
| UPDATE or DELETE on append-only registry/governance tables | Invalidates audit trail. |
| Skipping baseline capture | Cannot verify no regression. |
| Self-closing findings without code/test verification | Findings close by evidence, not assertion. |
| Modifying this contract without ADR | Immutable contract. |
| Deferring CI setup past Phase 1 | Every post-reset change needs CI. |
| Merging with failing CI | CI gate is mandatory. |
| Committing credentials or real confidential payloads | Security incident. |
| Reading/unlocking holdout without explicit approval | Claim/evidence boundary violation. |
| Creating OOS/performance/production/capital-ready labels without gate evidence | False claim risk. |
| Adding broker/exchange/live feed/live capital/order-blocking behavior in v1 | Scope violation. |
| Adding non-Python runtime/toolchain without escalation ADR | Runtime governance violation. |
| Treating legacy workflow files as current authority | Reset boundary violation. |
| Adding TODO without task reference | Untracked work. |

## Quality Process Rules

- P2 findings age out after 3 cycles: close, escalate to P1, or defer by ADR.
- One logical change per commit.
- Tests use isolated filesystem/database state.
- Heavy tasks must update `docs/EVIDENCE_INDEX.md` with real evidence artifacts.
- Review agents close findings only after reading code and confirming a test exists.

## Governing Documents

| Document | Role | Mutability |
|----------|------|------------|
| `docs/ARCHITECTURE.md` | Architecture and boundaries. | ADR for significant changes. |
| `docs/spec.md` | Feature scope. | Human-approved changes. |
| `docs/tasks.md` | Task contracts. | Active tasks editable; completed tasks append-only. |
| `docs/CODEX_PROMPT.md` | Session state. | Updated at phase boundaries. |
| `docs/IMPLEMENTATION_CONTRACT.md` | Immutable rules. | ADR required. |
| `docs/core/` | Charter/protocol/glossary. | Charter-level review for changes. |
| `docs/governance/` | Governance policy docs. | ADR/task review for changes. |
| `docs/audit/` | Validation and review evidence. | Append-only after finalization. |
| `docs/legacy/` | Historical context. | Retrieval only. |
