# Architecture - Entropy Core

Version: 1.0
Last updated: 2026-05-07
Status: Draft after governance reset

---

## System Overview

Entropy Core is a governed systematic research engine and deterministic audit primitive layer for the Entropy Protocol product portfolio. It provides local, human-gated research workflows for registering research objects, binding data/code/policy hashes, running leakage-resistant historical evaluation where explicitly approved, generating deterministic evidence/report packets, and exposing protocol-safe primitives to product workspaces. It does not run live trading, broker integration, autonomous AI strategy execution, or unsupported OOS/performance claims.

## Capability Profiles

| Profile | Status | Declared in Phase | Evaluation Artifact | Justification |
|---------|--------|-------------------|---------------------|---------------|
| RAG | OFF | - | `docs/retrieval_eval.md` | The application runtime does not retrieve from a managed corpus to answer users. Text-only lookup over docs is a development continuity practice handled by `DECISION_LOG.md`, `IMPLEMENTATION_JOURNAL.md`, `EVIDENCE_INDEX.md`, and task `Context-Refs`, not a runtime RAG feature. |
| Tool-Use | OFF | - | `docs/tool_eval.md` | Runtime code uses deterministic Python libraries, PostgreSQL, DuckDB, Parquet, and CLI commands. No LLM calls external tools or MCP servers at inference time. |
| Agentic | OFF | - | `docs/agent_eval.md` | Application behavior is a human-gated workflow and deterministic state machine. No runtime agent loop observes, decides, acts, and iterates. |
| Planning | OFF | - | `docs/plan_eval.md` | The primary runtime deliverable is evidence/report artifacts, not generated plans consumed by downstream executors. Development orchestration is separate from application behavior. |
| Compliance | OFF | - | `docs/compliance_eval.md` | Core has internal governance and confidential research artifacts, but no named external compliance framework or attestation launch gate in v1. |

## Solution Shape

| Decision | Selection | Justification |
|----------|-----------|---------------|
| Primary shape | Hybrid: workflow orchestration plus deterministic subsystems | Core has ordered human-gated workflows, but the registry, hash, leakage, attribution, evidence, and governance checks must remain deterministic. |
| Governance level | Strict | False confidence, leakage, corrupted audit trails, or downstream unsafe primitive reuse can damage every product workspace. Strict phase gates, audit evidence, and no-claim boundaries are proportionate. |
| Runtime tier | T1 | Core needs a bounded local/CI runtime with PostgreSQL service dependency, DuckDB embedded analytics, Alembic migrations, and local filesystem artifacts. It does not need privileged workers, runtime shell mutation, or long-lived mutable agents. |

### Rejected Lower-Complexity Options

| Rejected option | Why it is insufficient |
|-----------------|------------------------|
| Deterministic library only | Human approval gates, evidence packets, phase transitions, and research-object admission require a workflow around deterministic code. |
| Simple script or notebook | A script cannot enforce append-only registry semantics, leakage evidence, hash binding, CI-reviewed tasks, and phase-gate audit history. |
| Bounded ReAct/tool-using agent | The system does not need runtime tool choice by an LLM; deterministic CLI commands and library calls are more auditable. |
| Higher-autonomy agent | Autonomous runtime behavior would conflict with preregistration, holdout locks, human approval, and no-live-capital boundaries. |

### Minimum Viable Control Surface

- Append-only registry and governance event writes.
- Human approval before research object admission, evaluation execution, holdout unlock, phase-gate acceptance, provider activation, product bridge activation, or runtime/language escalation.
- Deterministic dataset, code, policy, run, and report hashes.
- Leakage and holdout gates before any OOS/performance label.
- No-claim labels and report guards for archive-only or scaffold-only outputs.
- Evidence index rows that point to executable tests, reports, fixtures, or review artifacts.
- CI with pytest, ruff, format check, and pyright from `products/entropy-core/`.

### Human Approval Boundaries

| Boundary | Human approval required? | Why |
|----------|--------------------------|-----|
| Research object registration | Yes | Preregistration is the root governance boundary. |
| Evaluation execution beyond scaffold/probe mode | Yes | Prevents accidental claim surfaces and leakage. |
| Holdout unlock or read | Yes | Holdout access changes evidence status and claim risk. |
| Phase-gate acceptance | Yes | Phase progress is a human governance decision. |
| Protocol boundary change | Yes | Charter/protocol semantics must not drift by implementation. |
| New data-provider activation | Yes | Opens external egress and data provenance risk. |
| Product workspace bridge into Core | Yes | Downstream products must not inherit unsafe primitives. |
| Runtime/language escalation | Yes | Changes CI, packaging, maintenance, and runtime boundaries. |

### Deterministic vs LLM-Owned Subproblems

| Subproblem | Owner | Reason |
|------------|-------|--------|
| Registry completeness, append-only writes, and readiness checks | Deterministic | These are protocol gates and must be testable. |
| Dataset normalization, hash computation, provenance, and migrations | Deterministic | Reproducibility depends on stable outputs. |
| Walk-forward splits, embargo, leakage checks, and holdout locks | Deterministic | OOS validity cannot depend on model judgment. |
| SimBroker fills, costs, and P&L attribution | Deterministic | Metric and evidence truth require exact calculations. |
| Governance state machine and phase-gate packets | Deterministic with human approval gates | Code evaluates state; humans approve transitions. |
| Report assembly and no-claim labels | Deterministic templates | Reports must derive from evidence artifacts. |
| Documentation synthesis or hypothesis drafts | Optional development assist only | AI drafts cannot write registry truth or gate decisions. |

## Runtime and Isolation Model

| Property | Decision |
|----------|----------|
| Isolation boundary | T1 bounded local/CI process. PostgreSQL service is allowed in local/CI. DuckDB is embedded. |
| Persistence model | PostgreSQL for registry/run/governance metadata; local Parquet/Markdown/JSON artifacts for data and evidence. |
| Network model | No external network egress by default. PostgreSQL local/CI service only. Future provider APIs require ADR/task approval. |
| Secrets model | Environment variables only, primarily `DATABASE_URL`. No secrets in source, fixtures, logs, or comments. |
| Runtime mutation boundary | Application runtime may not install packages, mutate toolchains, manage services, or run privileged shell actions. Alembic migrations run explicitly by operator/CI. |
| Rollback / recovery model | Re-run deterministic commands from registered inputs and hashes. Schema changes use Alembic migrations; append-only records are corrected by new events, not mutation. |

## Inference / Model Strategy

No production LLM inference is part of v1. AI may assist development, documentation synthesis, and review outside runtime. Any future AI drafting helper must be human-gated and must not write registry records, gate decisions, metrics, risk rule truth, evidence truth, or OOS/performance claims.

## Retrieval / Embedding Strategy

Runtime retrieval is not active. Development continuity uses scoped text retrieval through canonical docs, decision log, implementation journal, evidence index, audit reports, and task `Context-Refs`. A runtime RAG feature would require an ADR, `docs/retrieval_eval.md`, separate ingestion/query tasks, and profile activation.

## Component Table

| Component | File / Directory | Responsibility |
|-----------|------------------|----------------|
| CLI | `src/entropy/cli.py` | Local operator command surface. |
| Tracing | `src/entropy/tracing.py` | Shared `get_tracer()` boundary. |
| Metrics | `src/entropy/metrics.py` | Metrics abstraction/stubs. |
| Registry | `src/entropy/registry/` | Trial/research object registration, readiness, append-only admission surfaces. |
| Models | `src/entropy/models/` | Pydantic domain models. |
| Database | `src/entropy/db/`, `migrations/` | SQLAlchemy/Alembic schema and database access. |
| Hashing | `src/entropy/hashing/` | Deterministic dataset/run/policy/report hashes. |
| Data | `src/entropy/data/` | Historical data contracts and local Parquet/DuckDB surfaces. |
| SimBroker | `src/entropy/simbroker/` | Deterministic cost/fill simulation. |
| Walk-forward | `src/entropy/walkforward/` | IS/OOS split, embargo, leakage, and run orchestration. |
| Attribution | `src/entropy/attribution/` | P&L stream decomposition and attribution metrics. |
| Governance | `src/entropy/governance/` | Phase/state-machine controls and events. |
| Evidence | `src/entropy/evidence/` | Evidence/report packet creation and index updates. |
| Baseline archive surfaces | `src/entropy/baseline/` | D-K archive-only baseline logic retained as current code surface. |
| Protocol docs | `docs/core/` | Charter, protocol spec, glossary, evolution docs. |
| Governance docs | `docs/governance/` | Research firewall, governor, readiness gate, portfolio monitor docs. |

## Data Flow - Primary Local Research Path

1. Human prepares a research object or hypothesis and supporting policy/config.
2. Registry validation checks required fields, hashes, family/scope, duplicate ids, and no-claim labels.
3. Human approval is recorded before any admissible evaluation state transition.
4. Historical data is loaded from local fixtures or approved local datasets and normalized to deterministic Parquet/DuckDB surfaces.
5. Hashing records dataset/code/policy provenance before evaluation.
6. Walk-forward and leakage controls run before any OOS/evaluation surface is exposed.
7. SimBroker and attribution modules compute deterministic fills, costs, streams, and reports where explicitly approved.
8. Evidence/report modules write Markdown/JSON packets and update `docs/EVIDENCE_INDEX.md`.
9. Phase-gate review reads evidence, open findings, and human approvals before any next phase opens.

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.12 | Matches current workspace runtime and existing `.venv`; strong ecosystem for local research tooling. |
| Data models | Pydantic v2 | Typed schemas for registry, evidence, and product bridge contracts. |
| Dataframe engine | Polars | Efficient local historical data processing. |
| Columnar storage | PyArrow/Parquet | Immutable, hashable local artifacts. |
| Analytics | DuckDB | Embedded SQL over local artifacts without a separate service. |
| Relational DB | PostgreSQL 16 | Durable registry/run/governance metadata and CI service support. |
| ORM/migrations | SQLAlchemy 2.x + Alembic | Explicit schema control and migration history. |
| CLI | Typer/Rich | Existing local operator command surface. |
| Observability | structlog + OpenTelemetry API | Structured logs and shared tracing boundary. |
| Lint/format | ruff | Fast lint and formatting. |
| Type checking | pyright | Static validation for typed package surfaces. |
| Tests | pytest | Existing test suite and fixtures. |
| CI | GitHub Actions | Product-local verification contract. |

## Security Boundaries

### Authentication

V1 is a local single-operator workflow with no HTTP API and no external auth provider. Any future shared service, API, UI, or multi-user path requires an ADR before route implementation.

### Tenant Isolation

V1 is single-tenant. Product workspaces may call Core only through approved bridge contracts; they do not create multi-tenant Core storage by default.

### PII and Confidential Data Policy

Core v1 should not introduce user PII. Strategy specs, product pilot artifacts, registry records, governance events, and evidence packets are confidential. Logs, spans, metrics, and fixtures must not include secrets, credentials, raw customer data, or confidential strategy payloads unless explicitly anonymized.

## Observability

| Dimension | Choice | Notes |
|-----------|--------|-------|
| Tracing | OpenTelemetry API/noop by default | Shared module: `src/entropy/tracing.py`. |
| Metrics | `src/entropy/metrics.py` stubs/local counters | No external metrics service in v1. |
| Logging | structlog | No secrets, credentials, PII, raw strategy payloads, or raw product pilot data. |
| Health | CLI health command | Checks local dependencies without exposing confidential data. |
| Alerting | N/A | Local/CI workflow only. |

## External Integrations

| Integration | Purpose | Auth method | Rate limit / SLA |
|-------------|---------|-------------|------------------|
| PostgreSQL 16 | Registry, runs, governance metadata | `DATABASE_URL` env var | Local/CI service only. |
| DuckDB | Embedded analytics over local artifacts | None | In-process. |
| Parquet filesystem | Immutable local datasets/evidence | Filesystem permissions | Local only. |
| External data providers | Future historical data activation | TBD by ADR | Not active in v1 by default. |

## File Layout

```text
entropy-core/
|-- src/entropy/
|-- tests/
|-- migrations/
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- spec.md
|   |-- tasks.md
|   |-- CODEX_PROMPT.md
|   |-- IMPLEMENTATION_CONTRACT.md
|   |-- core/
|   |-- governance/
|   |-- audit/
|   |-- archive/
|   `-- legacy/
|-- prompts/
|-- templates/
|-- pyproject.toml
|-- pyrightconfig.json
`-- README.md
```

## Runtime Contract

| Variable | Description | Example value | Required |
|----------|-------------|---------------|----------|
| `DATABASE_URL` | PostgreSQL connection string for registry/run/governance metadata. | `postgresql://entropy:test@localhost:5432/entropy` | Yes for DB-backed commands/tests |
| `ENTROPY_DATA_DIR` | Root directory for local Parquet datasets. | `./data/market` | Yes for data workflows |
| `ENTROPY_REGISTRY_DIR` | Root directory for local registry/evidence artifacts. | `./artifacts/registry` | Yes for artifact workflows |
| `LOG_LEVEL` | Structured log level. | `INFO` | No |

## Continuity and Retrieval Model

### Canonical Truth

| Artifact | Authority |
|----------|-----------|
| `docs/ARCHITECTURE.md` | Architecture, runtime, capability profiles, and boundaries. |
| `docs/IMPLEMENTATION_CONTRACT.md` | Immutable implementation rules. |
| `docs/spec.md` | Product/runtime feature scope. |
| `docs/tasks.md` | Active task graph and acceptance criteria. |
| `docs/CODEX_PROMPT.md` | Session state, baseline, next task, and findings. |
| `docs/core/` | Charter, protocol spec, and glossary. |
| `docs/governance/` | Research firewall and governance specs. |
| `docs/adr/` | Formal architecture changes. |
| `docs/audit/` | Phase validation and review artifacts. |
| Code/tests/migrations | Executable behavior and proof. |

### Retrieval Convenience

| Artifact | Purpose | Required? |
|----------|---------|-----------|
| `docs/DECISION_LOG.md` | Index key reset and product decisions. | Yes |
| `docs/IMPLEMENTATION_JOURNAL.md` | Cross-session handoff notes. | Yes |
| `docs/EVIDENCE_INDEX.md` | Proof lookup for heavy tasks and phase gates. | Yes |
| `docs/legacy/CORE_LEGACY_SUMMARY.md` | Durable pre-reset summary. | Yes |

### Scoped Retrieval Rules

- Read legacy archives only when a task has a scoped `Context-Refs` pointer.
- Tasks that touch registry, governance, leakage, holdout, attribution, reports, product bridges, migrations, or runtime/language escalation must include `Context-Refs`.
- Retrieval aids summarize and index. They do not overrule canonical files.

## Non-Goals (v1)

- No live broker or exchange integration.
- No live feeds by default.
- No live capital, order blocking, production labels, or capital-ready labels.
- No autonomous AI trading or runtime LLM decision path.
- No unsupported OOS/performance claims.
- No holdout unlock without explicit human gate.
- No public SaaS, marketplace, or multi-user auth system.
- No signal scraping.
- No external compliance/institutional claim.
- No Rust, Go, C/C++, FFI, native extension, or second runtime service without benchmark evidence, ADR, CI/toolchain plan, rollback plan, and human approval.
