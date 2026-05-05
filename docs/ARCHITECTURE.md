# Architecture — Entropy Protocol

Version: 1.0
Date: 2026-05-01
Status: Active

---

## System Overview

Entropy Protocol is a governed systematic capital-allocation research framework that builds leakage-resistant, auditable evaluation infrastructure before making any trading-edge claim. The system implements a fully deterministic research and evaluation pipeline — Trial Registry, SimBroker, walk-forward harness, P&L attribution, and a governance state machine — orchestrated by a human-gated workflow. There is no LLM in the application runtime path; AI is used exclusively at the development level (architecture review and implementation). The v1 milestone (Phase 0) succeeds when all evaluation infrastructure is operational with machine-checkable evidence and a complete leakage audit, with no live capital and no OOS performance claims.

### Current Phase 0.5 Reality

T01-T24 are complete as the implementation foundation baseline, but Phase 0 is
not gate-approved. The current stage is Phase 0.5 Foundation Closure and
Evidence Hardening.

The following surfaces are explicitly open:

- SimBroker bid/ask calibration evidence: future >=100 manually verified fills;
- data pipeline stability evidence: future >=90 continuous days monitoring;
- P4 labels: `P4-RBL-v1` must be implemented/evidenced before Phase 1;
- registered leakage/temporal-shuffling gate packet;
- Sharpe CI and Harvey-Liu helpers: provisional only under D-022;
- purge/embargo: T18 N-bar assumption is scaffold-only under D-023;
- F-30/F-31: future real-evidence gates, no synthetic closure.

Phase 1 remains stop-shipped until the Phase 0 gate is approved or a
charter-level review revises the relevant exit criteria.

---

## Solution Shape

| Attribute | Value |
|-----------|-------|
| Primary shape | Hybrid (Deterministic subsystem + Workflow orchestration) |
| Governance level | Standard |
| Runtime tier | T1 (container/bounded worker; CI requires PostgreSQL service; local workstation uses local services) |
| LLM in runtime path | NO — deterministic throughout |
| AI use | Development level only: Claude (architecture/audit/review), Codex (implementation) |

### Rejected Lower-Complexity Options

| Option | Reason rejected |
|--------|----------------|
| Pure deterministic subsystem (no workflow) | Human phase gates are required for trial admission, spec changes, and phase transitions; a flat script cannot enforce these boundaries |
| Higher-autonomy agent | All research machinery decisions are deterministic by protocol spec; introducing LLM autonomy would violate governance Non-Negotiable NN-3 and NN-5 |
| Simple notebook/script | No enforced append-only registry, no reproducibility hashes, no walk-forward harness leakage guarantees |

### Minimum Viable Control Surface

The following control points are the minimum required by the protocol spec. They are enforced in code, not by convention.

| Control Point | Mechanism |
|--------------|-----------|
| Trial preregistration gate | Trial Registry write path requires all hashes present before INSERT |
| OOS separation | Walk-forward harness raises LeakageError if OOS data accessed during IS computation |
| P&L stream boundary | Net Sharpe computation function accepts only streams (a)+(b)+(c); stream (d) is a separate parameter |
| Append-only registry | No UPDATE or DELETE allowed on trial_registry or governance_events tables |
| Hash determinism | Dataset hash computed from SHA-256(sorted rows + schema fingerprint) |

### Human Approval Boundaries

The following actions require explicit human approval. They cannot be auto-approved by any code path.

| Action | Gate |
|--------|------|
| Trial Registry admission | Human approval comment required in governance_events table before READY status |
| Any spec change to PROTOCOL_SPEC.md, CHARTER.md, GLOSSARY.md | Human approval required; recorded in governance_events |
| Frozen non-negotiables, kill criteria, phase exit criteria, metric thresholds, P&L attribution rules | Immutable without charter-level review |
| RBE activation above Step 0 | Charter-level review + trial registry preregistration |
| Transition from research artifact to admissible evaluation | Human registration in Trial Registry with family assignment + readiness review |
| Any live capital decision | Explicit human approval; blocked until Phase 0 exit gate passes |

### Deterministic vs LLM-Owned Subproblems

ALL subproblems are deterministic. There is no LLM in the application runtime path.

| Subproblem | Ownership | Notes |
|-----------|-----------|-------|
| Trial Registry admission checks | Deterministic | Spec completeness check, hash presence check, no-duplicate check |
| Experiment Readiness Gate | Deterministic | Returns READY or structured list of failures |
| Research Firewall boundary | Deterministic | No AI-generated signal enters portfolio routing without human registration |
| Phase-gate checks | Deterministic | Machine-checkable evidence collection |
| Leakage checklist | Deterministic | PASS/FAIL per check, structured LeakageReport |
| P1 drawdown circuit breaker | Deterministic | Trips at threshold, resets on recovery, blocks new trades |
| P3 correlation trigger | Deterministic | Fires when 20-day average pairwise correlation crosses the protocol threshold, enforces ramp/recovery rules |
| P1–P4 precedence | Deterministic | Higher-priority signal always wins |
| RDL phase boundaries | Deterministic | Attestation query; no AI inference |
| Dataset hashing | Deterministic | SHA-256(sorted Parquet rows + schema fingerprint) |
| Bar aggregation | Deterministic | Polars computation |
| Timestamp normalization | Deterministic | UTC enforcement |
| Four-stream P&L | Deterministic | Streams (a)(b)(c)(d) computed separately |
| Net Sharpe | Deterministic | Only streams (a)+(b)+(c) |
| CI method (CI-SR-ACF-v1) | Deterministic scaffold | D-022: revise required before gate/report use |
| Harvey-Liu deflation | Deterministic scaffold | D-022: blocked for gate use until full family workflow exists |
| N_eff estimator | Deterministic scaffold | Simple K3 estimator exists; operational monitor evidence pending |
| CRR, CER, cost drag | Deterministic | Formula-based from fill logs |
| SimBroker cost components | Deterministic | Fixed commission + % commission + slippage (linear + sqrt impact) + borrow/funding |
| Data ingestion retries | Deterministic | Retry logic in DataProvider |
| Append-only registry writes | Deterministic | INSERT-only; enforced at DB layer |
| Immutable run IDs | Deterministic | UUID assigned at run creation, never mutated |
| Governance event logs | Deterministic | Append-only, timestamped |
| Report generation | Deterministic | Template-based from registry + hash artifacts |
| Evidence artifact creation | Deterministic | Leakage checklist runs → EVIDENCE_INDEX updated |

### Runtime and Isolation Model

- **Runtime tier T1:** Bounded worker. Application runs as a process on a local workstation or a small Linux VPS. No shell mutation, no privileged actions, no long-lived mutable worker state beyond PostgreSQL persistence.
- **CI:** GitHub Actions with PostgreSQL 16 service container. Tests run inside the CI job; no external network egress required for tests.
- **Local:** Local PostgreSQL 16 instance. DuckDB embedded (no service). Parquet files on disk in ENTROPY_DATA_DIR.
- **No container required for v1 local workstation deployment.** Optional containerization for VPS.
- **No privileged actions in application code.** Alembic migrations are the only schema-mutating operations and run explicitly.
- **Rollback/recovery:** Schema rollback uses Alembic downgrade to the prior or specified revision. Append-only tables (`trial_registry`, `governance_events`) are never data-rolled-back; corrections are recorded as new events. Process recovery is a bounded worker restart because no durable in-process state exists outside PostgreSQL and immutable Parquet files.

---

## Capability Profiles

| Profile | Status | Justification |
|---------|--------|---------------|
| RAG | OFF | Application processes structured market data (OHLCV Parquet) deterministically. There is no document corpus to retrieve from at runtime. All research artifacts are structured DB records, not unstructured text. |
| Tool-Use | OFF | No LLM tool calls in the application. All computations are deterministic Python functions. |
| Agentic | OFF | No agent loops in the application. The research lifecycle uses a human-gated workflow, not an autonomous agent. |
| Planning | OFF | No LLM-generated plans in the application. Task sequencing is encoded in docs/tasks.md and executed by human-directed orchestration. |
| Compliance | OFF | Single-tenant, internal governance only. No external compliance framework (HIPAA, SOC2, PCI) applies to v1. |

---

## Component Table

| Component | Module | Purpose |
|-----------|--------|---------|
| Trial Registry | entropy/registry/ | Preregistration of trial specs before data examination; append-only; family tagging; hash locking |
| SimBroker | entropy/simbroker/ | Deterministic execution simulation: fee model, fill engine, borrow/funding hooks, fill logs |
| Walk-Forward Harness | entropy/walkforward/ | IS/OOS splitting with embargo bands; leakage detection; walk-forward runner |
| P&L Attribution Engine | entropy/attribution/ | Four-stream P&L decomposition; net Sharpe computation; DrawdownRecord |
| Governance State Machine | entropy/governance/ | P1 drawdown circuit breaker; P3 correlation trigger; state transitions; event logging |
| Data Pipeline | entropy/data/ | OHLCV ingestion; DataProvider abstraction; local Parquet store; data quality checks |
| Statistical Analysis | entropy/stats/ | Sharpe CI (CI-SR-ACF-v1); Harvey-Liu deflation stub; N_eff estimator stub |
| Phase Gate Evidence | entropy/evidence/ | Evaluation report generator; leakage audit evidence collection; EVIDENCE_INDEX updater |
| Database Layer | entropy/db/ | SQLAlchemy 2.x models; Alembic migrations; PostgreSQL 16 tables |
| CLI | entropy/cli/ | Typer/rich CLI entry point; commands for registry, ingestion, walk-forward, reporting |
| Models | entropy/models/ | Pydantic v2 domain models: market, registry, performance |
| Hashing | entropy/hashing/ | Deterministic SHA-256 hashing for datasets, runs, policies |
| Experiment Readiness Gate (ERG) | entropy/registry/gate.py | Deterministic pre-admission validation for registered trials; no DB writes |
| Research Firewall | docs/governance/research_firewall.md; entropy/registry/ | Governance boundary preventing discovery artifacts from becoming admissible evaluation without preregistration |
| Research Portfolio Monitor (RPM) | docs/governance/research_portfolio_monitor.md | Read-only governance dashboard specification; no runtime module in Phase 0 implementation yet |
| Protocol Governor | docs/governance/governor.md; entropy/governance/ | Governance gate for system-level changes and phase approvals |
| Research Discovery Layer (RDL) | docs/architecture/research_discovery_layer.md | Dormant/scaffolding-only through Phase 0-1; no application runtime module until an approved future phase |

---

## Data Flow — Primary Request Path

The Phase 0 evaluation run path is as follows:

1. **Register trial** — Researcher calls `entropy registry register` with a TrialSpec. The Trial Registry write path validates spec completeness, checks for duplicate trial IDs, verifies all hashes are present, assigns a family tag, and performs an INSERT-only write to the `trial_registry` table. Returns a TrialID. Human approval is recorded in `governance_events` before status transitions to READY.

2. **Ingest data** — `entropy data ingest` triggers the DataProvider adapter (local fixture or configured provider). OHLCV bars are written to versioned Parquet in `ENTROPY_DATA_DIR/market/`. The dataset hash (SHA-256 of sorted rows + schema fingerprint) is computed and stored in the DB alongside provenance metadata. Data quality checks (timestamp normalization, gap detection, OHLCV sanity) run before the dataset is marked usable.

3. **Run walk-forward** — `entropy run walk-forward --trial-id <id>` loads the registered trial spec and dataset. The IS/OOS splitter applies configurable embargo bands. Leakage detection runs on the IS window before any strategy computation. The strategy runs on IS data; then the leakage checklist runs again before OOS evaluation begins. OOS strategy results and fill logs are recorded via SimBroker. A RunRecord (including trial_id, dataset_hash, code_hash, policy_hash, simbroker_version) is written to the `runs` table.

4. **Compute P&L** — The P&L Attribution Engine decomposes fill logs into the protocol's four streams: (a) long position P&L, (b) short position P&L, (c) borrow/funding cost P&L, and (d) treasury yield P&L. Net Sharpe is computed only from (a)+(b)+(c). DrawdownRecords are generated. PerformanceMetrics are persisted.

5. **Generate report** — `entropy report generate --trial-id <id>` fetches the registry spec, dataset hash, code hash, and policy hash from the DB. It renders a reproducible Markdown evaluation report. The leakage audit evidence is appended to `docs/EVIDENCE_INDEX.md`. The Phase 0 gate report is produced when all T01–T24 tasks have passing tests.

---

## Tech Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | Python | 3.12 | Strong ecosystem for quant research, data processing, testing, and AI-assisted development |
| Package manager | uv | latest | Fast, reproducible dependency management with lockfile support |
| Data models | Pydantic | v2 | Typed validation for registry specs, run records, fills, and reports |
| DataFrame / analytics | Polars | latest stable | Efficient columnar batch operations for OHLCV and evaluation datasets |
| Columnar storage | PyArrow + Parquet | latest stable | Immutable, portable, hashable dataset artifacts |
| Local analytics | DuckDB | embedded, latest stable | SQL analytics over Parquet without adding a server dependency |
| Relational DB | PostgreSQL | 16 | Durable registry, governance, and run metadata with CI service support |
| ORM / migrations | SQLAlchemy + Alembic | 2.x | Explicit schema control and reversible migrations |
| Testing | pytest | latest stable | Standard Python test runner with fixture support for DB and filesystem isolation |
| Linting | ruff | latest stable | Fast lint and format checks suitable for every Codex task |
| Type checking | pyright | latest stable | Static validation for typed domain models and interfaces |
| CLI | Typer + Rich | latest stable | Clear local operator commands with readable structured output |
| Structured logging | structlog | latest stable | JSON-ready logs for auditability and reproducible troubleshooting |
| Tracing | OpenTelemetry (noop in v1) | latest stable | Stable instrumentation boundary without requiring an external collector in v1 |

### Language Escalation Policy

Python is the default implementation language for Phase 0 and Phase 1. Additional languages are not part of the active stack; they are escalation options that require measured evidence and an ADR before adoption.

| Language | Allowed Role | Entry Criteria | Notes |
|----------|--------------|----------------|-------|
| Python | Default for all Phase 0/1 implementation | Always allowed within the declared stack | Registry, SimBroker, walk-forward harness, data pipeline, reports, CLI, and governance logic stay Python unless an ADR proves otherwise |
| Rust | Performance-critical library or Python extension for hot paths | Profiling shows Python/Polars/DuckDB cannot meet an explicit runtime or memory target after optimization | Candidate for simulation loops, fill matching, rolling statistics, or numeric kernels; must expose a stable Python API |
| Go | Long-running operational service | A persistent ingestion, monitoring, or worker process is required and Python CLI/cron/systemd is insufficient | Candidate for feed collectors or monitoring workers; not used for core evaluation math by default |
| C/C++ | External native integration only | Required by a proven third-party library, hardware interface, or extreme low-level numeric path with no Rust/Python alternative | Highest maintenance burden; prohibited for speculative optimization |

Introducing any non-Python language requires all of the following before code is added:

1. A benchmark document with input data, current Python baseline, target threshold, candidate implementation result, and reproducible command.
2. A written ADR in `docs/adr/` explaining why Python/Polars/DuckDB are insufficient, why the chosen language is appropriate, affected modules, CI/toolchain impact, packaging strategy, and rollback plan.
3. Updates to `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, CI, and `docs/tasks.md`.
4. Human approval recorded before implementation begins.

No task may introduce Rust, Go, C, C++, FFI, native extensions, or a second runtime service as an incidental implementation detail.

### Performance Profiling Gates

Phase 0 stays Python-first until measured evidence proves otherwise. The first real profiling gate occurs after T20 Walk-Forward Runner because the system then has a representative end-to-end path: local fixture ingestion, deterministic dataset storage, Trial Registry, readiness gate, SimBroker surface, and walk-forward orchestration. Earlier micro-benchmarks may be used to debug a local regression, but they are not sufficient to justify a new implementation language.

The post-T20 profiling artifact must record the input dataset, command, Python/Polars/DuckDB baseline, runtime and memory target, observed bottleneck, and optimization attempted inside the Python stack. If the optimized Python stack misses an explicit target, a language-escalation ADR is required before any Rust, Go, C, C++, FFI, native extension, or second runtime service is introduced.

A second profiling gate occurs after the formula-bearing numerical tasks are implemented or explicitly waived, because T21/T23-style statistical and performance calculations may expose different hot paths than the walk-forward runner. This second gate follows the same benchmark and ADR requirements.

---

## Security Boundaries

- **Single-tenant.** No external authentication for v1. No multi-tenant isolation required.
- **Secrets in environment variables.** All credentials (DATABASE_URL, etc.) come from environment variables. No secrets in source code, comments, or test fixtures.
- **No PII in the application.** The system processes market data (OHLCV prices, volumes, timestamps). No user PII exists in this system. PII policy: no PII fields.
- **Confidential data:** Strategy specifications in `trial_registry` and `governance_events` are confidential. Registry data is local only; not transmitted to external services.
- **No external network egress in v1.** Data ingestion uses local fixture files in Phase 0. Any future provider adapter must be explicitly declared in this document before egress is opened.
- **Append-only tables.** `trial_registry` and `governance_events` are INSERT-only. No UPDATE or DELETE is permitted. This is enforced both by application code and, optionally, by PostgreSQL row-level policy.

---

## Observability

- **Structured logging:** structlog with JSON output. All application logs are structured. Log level controlled by `LOG_LEVEL` env var. No PII in log fields.
- **Tracing:** OpenTelemetry noop tracer in v1. A single shared tracing module at `entropy/tracing.py` exposes `get_tracer()`. All code that creates spans imports from this module. No inline noop spans in individual files. No external collector in v1.
- **Metrics:** No external metrics collection in v1. Counter/histogram stubs in `entropy/metrics.py` for future activation.
- **Health:** CLI command `entropy health` checks PostgreSQL connectivity and DuckDB availability. Returns structured JSON `{"status": "ok"}` or `{"status": "degraded", "checks": [...]}`.
- **No OBS-2 profile metrics required** (all profiles are OFF).

---

## External Integrations

| Integration | Type | Status | Notes |
|-------------|------|--------|-------|
| PostgreSQL 16 | Relational DB | Active | Local or VPS; connection via DATABASE_URL env var |
| DuckDB | Embedded analytics DB | Active | No service required; in-process |
| Parquet / PyArrow | Columnar file store | Active | Immutable dataset store; versioned by dataset hash |
| Data provider adapter | Abstract interface | Provider-neutral | Concrete adapter required before any real OHLCV fetch; local fixture adapter for Phase 0 |
| External data providers | HTTP / API | Not active in Phase 0 | Declared here when a provider is added; no egress in v1 |

The data provider abstraction (DataProvider base class) enforces a provider-neutral boundary. No hard-coded provider. Any concrete provider must implement `fetch_ohlcv`, `list_symbols`, and `check_health` before ingestion is permitted.

---

## File Layout

```
Entropy_Protocol/
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI
├── docs/
│   ├── ARCHITECTURE.md               # This file
│   ├── spec.md                       # Feature specification
│   ├── tasks.md                      # Task graph (T01–T24)
│   ├── CODEX_PROMPT.md               # Session state handoff
│   ├── IMPLEMENTATION_CONTRACT.md    # Implementation rules
│   ├── DECISION_LOG.md               # Decision index
│   ├── IMPLEMENTATION_JOURNAL.md     # Append-only session journal
│   ├── EVIDENCE_INDEX.md             # Proof lookup index
│   ├── core/
│   │   ├── PROTOCOL_SPEC.md          # Protocol specification (canonical)
│   │   ├── CHARTER.md                # Strategic charter
│   │   └── GLOSSARY.md               # Term definitions
│   ├── audit/
│   │   ├── AUDIT_INDEX.md            # Review cycle index
│   │   ├── PROMPT_0_META.md          # META analyst prompt
│   │   ├── PROMPT_1_ARCH.md          # Architecture reviewer prompt
│   │   ├── PROMPT_2_CODE.md          # Code reviewer prompt
│   │   └── PROMPT_3_CONSOLIDATED.md  # Consolidation agent prompt
│   └── prompts/
│       ├── ORCHESTRATOR.md           # Orchestrator system prompt (stub)
│       └── PROMPT_S_STRATEGY.md      # Strategy reviewer prompt
├── entropy/                          # Main application package
│   ├── __init__.py
│   ├── cli.py                        # Typer CLI entry point
│   ├── tracing.py                    # Shared tracing module (get_tracer())
│   ├── metrics.py                    # Metric stubs
│   ├── models/
│   │   ├── __init__.py
│   │   ├── market.py                 # OHLCV, Dataset, DatasetKey, Timeframe
│   │   ├── registry.py               # TrialSpec, RegistryEntry, RunRecord, FillLog, GovernanceEvent
│   │   └── performance.py            # PnLStreams, NetSharpe, DrawdownRecord, PerformanceMetrics
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py                 # SQLAlchemy table models
│   │   └── session.py                # DB session factory
│   ├── registry/
│   │   ├── __init__.py
│   │   ├── write.py                  # Trial Registry write path (T09)
│   │   ├── gate.py                   # Experiment Readiness Gate (T10)
│   │   └── read.py                   # Trial Registry read path (T11)
│   ├── hashing/
│   │   ├── __init__.py
│   │   └── hashing.py                # Deterministic hashing (T08)
│   ├── data/
│   │   ├── __init__.py
│   │   ├── provider.py               # DataProvider abstract base class (T12)
│   │   ├── fixture_adapter.py        # Local fixture adapter + Parquet store (T13)
│   │   └── quality.py                # Data quality checks (T14)
│   ├── simbroker/
│   │   ├── __init__.py
│   │   ├── costs.py                  # SimBroker cost model (T15)
│   │   ├── fills.py                  # SimBroker fill engine (T16)
│   │   └── calibration.py            # BidAskProvider stub (T17)
│   ├── walkforward/
│   │   ├── __init__.py
│   │   ├── splitter.py               # IS/OOS splitter (T18)
│   │   ├── leakage.py                # Leakage detection checklist (T19)
│   │   └── runner.py                 # Walk-forward runner (T20)
│   ├── attribution/
│   │   ├── __init__.py
│   │   └── engine.py                 # P&L Attribution Engine (T21)
│   ├── governance/
│   │   ├── __init__.py
│   │   └── state_machine.py          # P1/P3 Governance State Machine (T22)
│   ├── stats/
│   │   ├── __init__.py
│   │   └── analysis.py               # Statistical analysis stubs (T23)
│   └── evidence/
│       ├── __init__.py
│       └── artifacts.py              # Phase 0 exit artifacts (T24)
├── migrations/
│   ├── env.py                        # Alembic env
│   ├── alembic.ini                   # Alembic config
│   └── versions/                     # Migration files
├── tests/
│   ├── conftest.py                   # Fixtures: PostgreSQL, DuckDB, test data
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_hashing.py
│   │   ├── test_registry.py
│   │   ├── test_data_quality.py
│   │   ├── test_simbroker.py
│   │   ├── test_attribution.py
│   │   ├── test_governance.py
│   │   └── test_stats.py
│   ├── integration/
│   │   ├── test_walk_forward.py
│   │   ├── test_leakage.py
│   │   ├── test_registry_db.py
│   │   └── test_evidence.py
│   └── smoke/
│       └── test_smoke.py
├── data/
│   └── market/                       # Versioned Parquet datasets (ENTROPY_DATA_DIR)
├── pyproject.toml
└── .gitignore
```

---

## Runtime Contract

The following environment variables are required for the application to run. All are read from the environment; none are hardcoded.

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | PostgreSQL connection string | `postgresql://entropy:secret@localhost:5432/entropy` |
| `ENTROPY_DATA_DIR` | Yes | Root directory for versioned Parquet datasets | `/home/user/entropy_data` |
| `ENTROPY_REGISTRY_DIR` | Yes | Directory for registry artifacts (hashes, evidence) | `/home/user/entropy_registry` |
| `LOG_LEVEL` | No | Structured log level (default: INFO) | `WARNING` |

No `.env` files are committed to the repository. A `.env.example` file documents required variables without values.

---

## Continuity and Retrieval Model

- **Canonical authority:** `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, review reports, code, tests.
- **Retrieval aids:** `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md` — these summarize and point; they do not overrule canonical files.
- **Session handoff:** `docs/CODEX_PROMPT.md` is the single source of truth for session state. Every agent reads it before starting work.
- **Phase gate evidence:** `docs/EVIDENCE_INDEX.md` tracks proof artifacts for heavy tasks (T16, T17, T21, T22) and phase gates. Evidence is required before a phase gate can be marked PASSED.

---

## Non-Goals (v1)

The following are explicitly out of scope for the v1 / Phase 0 milestone:

- **Live trading** — no capital deployment; no broker API integration
- **OOS performance claims** — no signal receives an OOS label before the Phase 0 gate is approved with registered leakage evidence
- **Phase 1+ features** — regime overlay (Phase 2), equity shorts (Phase 3), crypto perp shorts (Phase 4), treasury (Phase 5) are all deferred
- **Multi-user** — single-tenant; no user authentication, no role-based access
- **LLM in runtime path** — all runtime computations are deterministic; no LLM inference in the application
- **RAG / agent / planning profiles** — all Capability Profiles are OFF
- **External compliance framework** — no HIPAA, SOC2, PCI, or equivalent; internal governance only
- **External network egress** — no live data provider in Phase 0; local fixtures only
- **Notification channels** — no Slack/Telegram integration in v1; phase reports written to files only
- **VPS deployment** — local workstation first; VPS is optional and not required for Phase 0
- **Over-architecture** — no plugin systems, provider registries beyond the Phase 0 adapter boundary, extensibility frameworks, or abstraction layers beyond what is required to implement T01-T24. The selected architecture is the ceiling for Phase 0, not a starting point for speculative expansion.
