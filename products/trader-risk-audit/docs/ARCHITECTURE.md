# Architecture - Trader Risk Audit

Version: 1.0
Last updated: 2026-05-07
Status: Draft

---

## System Overview

Trader Risk Audit is a local-first, concierge audit workflow for traders who provide executed trade exports and written risk rules, then receive deterministic violation reports with source-row traceability and violation-attributed P&L. It serves active prop-style traders, funded-account traders, systematic retail traders, and small trading teams that need proof of where execution discipline broke down. The system is intentionally batch-oriented, reproducible, and local by default: it does not connect to broker APIs, block orders, make live trading decisions, or use AI to decide violation truth.

## Capability Profiles

| Profile | Status | Declared in Phase | Evaluation Artifact | Justification |
|---------|--------|-------------------|---------------------|---------------|
| RAG | OFF | - | `docs/retrieval_eval.md` | V1 consumes a small set of user-provided exports and rule documents per audit. The rule documents can be read directly during normalization and human review; there is no managed corpus, no query-time citation product, and no knowledge base too large for direct processing. |
| Tool-Use | OFF | - | `docs/tool_eval.md` | Runtime code uses ordinary deterministic application libraries for CSV/XLSX parsing, validation, reporting, and local file writes. No LLM is allowed to call external tools, APIs, MCP servers, or side-effecting functions at inference time. |
| Agentic | OFF | - | `docs/agent_eval.md` | The product has a fixed batch workflow and no observe-decide-act loop. Human operators approve ambiguous rule interpretations and report sends; no runtime agent delegates or persists state across loop iterations. |
| Planning | OFF | - | `docs/plan_eval.md` | The primary deliverable is an audit report, not a structured plan consumed by an executor. Any internal task planning belongs to the development workflow, not application behavior. |
| Compliance | OFF | - | `docs/compliance_eval.md` | The system handles confidential trading records but has no named regulatory framework or attestation gate in v1. Standard security, retention, and confidentiality controls are still mandatory through the implementation contract. |

## Solution Shape

| Decision | Selection | Justification |
|----------|-----------|---------------|
| Primary shape | Workflow orchestration | The product is a known sequence: import export, normalize trades, validate/approve risk policy, run deterministic evaluators, attribute P&L, generate report, package delivery. A workflow is the minimum shape that captures ordered steps and human gates without introducing runtime agency. |
| Governance level | Standard | Incorrect violations or P&L attribution can damage trader trust, but v1 has no live capital control, no public SaaS surface, and no formal compliance attestation. Standard governance with traceable tasks, tests, CI, audit docs, and one proof-first financial attribution task is proportionate. |
| Runtime tier | T0 | A local deterministic CLI/script workflow is enough for the first paid pilots. No shell mutation, service reconfiguration, privileged worker, long-lived runtime, broker credentials, or public deployment is needed. |

### Rejected Lower-Complexity Options

| Rejected option | Why it is insufficient |
|-----------------|------------------------|
| Deterministic subsystem only | The core evaluators are deterministic, but the product is more than a library call. It needs a reviewable workflow with human approval points for ambiguous exports, rule interpretation, and paid report release. |
| Simple human-in-the-loop assistant | A human-only or LLM-assisted narrative process would not produce reproducible violation records, source-row evidence, or regression-testable P&L attribution. |
| Bounded ReAct / tool-using agent | The steps are known in advance and tool choice is not an inference-time decision. Ordinary CLI commands and library calls are lower cost and easier to audit. |
| Higher-autonomy agent | There is no need for long-horizon planning, delegation, autonomous retries, runtime mutation, or persistent agent state. Adding those behaviors would increase trust and security risk without improving the v1 audit. |

### Runtime Recommendation

T0 is the selected tier. Runtime mutability is not required; package installation happens only during development or CI, not during audit execution. The workflow needs no privileged actions, no broker credentials, no service-to-service network, no persistent mutable worker, and no autonomous recovery path. Recovery is re-run based: the same export, policy file, and audit config must reproduce the same normalized trades, violation records, summary values, and artifact hash. No lower runtime tier exists beneath T0.

### Cost / Risk Reasoning

The highest error cost is false accusation, missed violation, bad P&L attribution, or advice-like language. Variance is expensive because traders must trust repeated audits on the same inputs. Latency sensitivity is medium: typical normalized audits should finish in under five minutes, while concierge review time is tracked separately. Blast radius is medium because v1 affects user decisions and trust but never controls live capital. Operational drift risk is low as long as the system remains local-first and deterministic.

### Minimum Viable Control Surface

- Canonical trade schema and risk policy schema with explicit validation errors.
- Deterministic rule evaluators only; no AI in violation truth or P&L arithmetic.
- Source-row traceability for every violation.
- Reproducible artifact manifest and report hash for each completed audit.
- Human approval before accepting ambiguous rule interpretations, sending paid reports, or adding new rule types.
- Local-only default data handling, anonymized fixtures, no confidential data in logs.
- CI with ruff, format check, and pytest before implementation work proceeds.

### Human Approval Boundaries

| Boundary | Human approval required? | Why |
|----------|--------------------------|-----|
| Accepting trader-written rule interpretation | Yes | Ambiguous policy language can change violation truth and must not be inferred silently. |
| Resolving ambiguous or unsupported export columns | Yes | Incorrect normalization can corrupt every downstream rule check. |
| Adding a new rule type or changing evaluator semantics | Yes | Rule semantics are the product's audit contract and require explicit review. |
| Sending a paid report or delivery packet | Yes | Reports may influence user decisions and must be checked for unsupported claims. |
| Claiming that a behavior caused losses | Yes | Attribution must remain evidence-backed and avoid investment-advice language. |
| Connecting to live broker or exchange APIs | Yes, plus ADR | This expands runtime, secrets, and capital-adjacent risk beyond v1. |
| Deterministic re-run of an already approved audit input set | No | Re-runs are reproducible checks over immutable local inputs. |

### Deterministic vs LLM-Owned Subproblems

| Subproblem | Owner | Reason |
|------------|-------|--------|
| Trade schema validation, timestamp parsing, symbol/account normalization | Deterministic | Input validity must be testable and reproducible. |
| Rule schema validation and allowed rule taxonomy | Deterministic with human approval for ambiguous mapping | The schema is the contract; human review handles interpretation before code evaluates it. |
| Rule routing and evaluator selection | Deterministic | Each policy rule maps to a known evaluator by type and version. |
| P&L, drawdown, position size, leverage, cooldown, and daily-loss calculations | Deterministic | Financial arithmetic must be exact, regression-tested, and source-traceable. |
| Violation severity and report section inclusion | Deterministic | Classification must be repeatable across re-runs. |
| Report narrative wording | Human-authored templates, optional LLM draft only after approval | Customer-facing truth must derive from violation records; AI text cannot add claims. |
| Telegram-ready formatting | Deterministic | Delivery formatting is a pure transformation of approved report content. |
| Audit manifest and artifact hashing | Deterministic | Reproducibility depends on stable hashes over canonical inputs and outputs. |

### Runtime and Isolation Model

| Property | Decision |
|----------|----------|
| Isolation boundary | T0 local process. Audits run from the product workspace or a local virtual environment controlled by the operator. |
| Persistence model | Local files only in v1: input exports, normalized artifacts, reports, manifests, and optional SQLite/DuckDB artifacts if later justified. |
| Network model | No network required for core v1. Telegram is manual or disabled unless a later ADR adds bot delivery. No broker/exchange egress. |
| Secrets model | No required secrets for core v1. Optional Telegram bot token is disabled by default and must come from environment variables if enabled later. |
| Runtime mutation boundary | Application runtime may not install packages, modify toolchains, create services, or mutate shell state. Development and CI dependency installation are outside runtime. |
| Rollback / recovery model | Re-run an audit from the same export, policy file, and config. Generated artifact hashes must identify output drift. |

## Inference / Model Strategy

No production LLM is required for v1. If a later task adds an optional drafting helper for rule extraction or report narrative, it must be human-gated and must not affect final rule evaluation, P&L arithmetic, violation truth, or report claims without deterministic evidence.

| Path / Task | Model class | Deterministic alternative considered | Fallback / escalation | Measurement |
|-------------|-------------|--------------------------------------|-----------------------|-------------|
| Draft rule extraction from trader-written rules | Small structured-output model only if human-approved feature is added | Manual mapping into `risk_policy.yaml` | Disable AI drafting and require manual policy entry | Draft acceptance rate after human review; zero accepted drafts that change evaluator truth without approval |
| Report narrative polishing | Small text model only if templates are insufficient | Markdown templates with deterministic summary values | Use deterministic templates only | Human edit rate; claim-guard test pass rate |

Rules: AI-generated drafts are suggestions only, customer-facing truth comes from deterministic artifacts, and any model choice requires a task and ADR if it changes runtime behavior.

## Retrieval / Embedding Strategy

Retrieval mode is no retrieval for v1. User-provided rules and templates are loaded directly as files in the audit workflow. Text-only retrieval may be reconsidered only if pilots produce a document corpus too large for direct review or a product requirement for query-time evidence lookup. Multimodal retrieval is explicitly out of scope.

## Component Table

| Component | File / Directory | Responsibility |
|-----------|------------------|----------------|
| CLI entry point | `trader_risk_audit/cli.py` | Accept audit inputs, invoke workflow steps, and write artifact paths. |
| Configuration | `trader_risk_audit/config.py` | Load local paths and feature flags from environment variables with safe defaults. |
| Shared tracing/logging | `trader_risk_audit/observability.py` | Provide `get_tracer()` and logging helpers that avoid confidential data. |
| Trade schema | `trader_risk_audit/trades/schema.py` | Define canonical trade fields, validation rules, and normalized row identifiers. |
| Import normalizer | `trader_risk_audit/trades/importers.py` | Parse supported CSV/XLSX exports into canonical trade records. |
| Risk policy schema | `trader_risk_audit/policy/schema.py` | Define supported rule types, thresholds, units, account scope, and schema version. |
| Policy review packet | `trader_risk_audit/policy/review.py` | Produce deterministic human review artifacts for ambiguous policy mappings and apply approved deterministic fields. |
| Policy validator | `trader_risk_audit/policy/validation.py` | Produce explicit errors for unsupported, ambiguous, or missing rule fields. |
| Calendar and aggregation | `trader_risk_audit/evaluation/calendar.py`, `trader_risk_audit/evaluation/aggregates.py` | Build session/day groupings, daily P&L, equity curve, exposure, and drawdown inputs. |
| Rule evaluators | `trader_risk_audit/evaluation/rules.py` | Evaluate max daily loss, drawdown, cooldown, position size, forbidden assets, and leverage rules. |
| Violation model | `trader_risk_audit/evaluation/violations.py` | Store rule id, source rows, evaluated values, threshold, timestamps, severity, and attribution fields. |
| P&L attribution | `trader_risk_audit/evaluation/attribution.py` | Attribute compliant vs violating P&L without double counting. |
| Report model | `trader_risk_audit/reporting/model.py` | Build report sections from normalized trades, policies, violations, and summaries. |
| Markdown report generator | `trader_risk_audit/reporting/markdown.py` | Render deterministic reports from report models and templates. |
| Claim guard | `trader_risk_audit/reporting/claim_guard.py` | Block unsupported advice, performance, live-control, or causal claims in report text. |
| Artifact manifest | `trader_risk_audit/artifacts/manifest.py` | Write reproducible manifests and hashes for inputs, normalized data, violations, and reports. |
| Retention/delete workflow | `trader_risk_audit/storage/retention.py` | Delete or archive local pilot data according to explicit operator decisions. |
| Test fixtures | `tests/fixtures/` | Store anonymized exports, policies, and expected outputs for regression tests. |

## Data Flow - Primary Audit Path

1. Operator receives a trader export and written risk rules through a human-approved concierge channel.
2. Operator stores the export and rule file in local input directories outside source control.
3. CLI command receives `--trades`, `--policy`, `--output-dir`, and optional `--timezone`.
4. Import normalizer parses the export, maps known columns, and emits canonical trade records or explicit validation errors.
5. Policy validator loads the risk policy schema and rejects unsupported or ambiguous rule definitions.
6. Aggregation builds session/day groupings, daily P&L, equity curve, exposure, and drawdown inputs.
7. Rule evaluators run deterministic checks and emit violation records with source row references.
8. Attribution module calculates compliant versus violating P&L and rule-level summaries.
9. Report model assembles violation tables, repeated patterns, worst days, and next-review checklist.
10. Claim guard verifies report text avoids investment advice, live-control claims, unsupported causal claims, and performance promises.
11. Markdown generator writes the report and Telegram-ready summary packet.
12. Manifest writer records input hashes, policy hash, normalized artifact hash, violation hash, report hash, tool version, and generated paths.

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.12 | Matches Entropy Core's runtime, fits the local CLI/data workflow, and keeps future bridge contracts from carrying cross-version friction. |
| CLI framework | argparse | A CLI is sufficient for concierge pilots; argparse keeps Phase 1 dependency cost at zero and is pinned by the implemented package skeleton. |
| Dataframe engine | Polars preferred, pandas acceptable behind adapter | Polars is fast for batch trade exports and memory efficient for tens of thousands of rows; an adapter keeps migration possible. |
| Validation | Pydantic | Versioned schemas and explicit validation errors match the audit contract. |
| Storage | Local files; SQLite or DuckDB only if needed by a later task | Local artifacts minimize infrastructure cost before paid repeat-use evidence. |
| Reporting | Markdown templates | Markdown is reviewable, diffable, and can become PDF or Telegram text later. |
| Observability | Stdlib logging plus shared noop tracer initially | Local CLI needs structured enough diagnostics without adding infrastructure. A shared module prevents later tracing drift. |
| Lint / format | ruff | Single tool for lint and format checks with low setup cost. |
| Type checking | pyright | The brief prefers pyright; it can be added once the skeleton is stable. |
| Test framework | pytest | Rich fixture support for anonymized exports and golden expected outputs. |
| CI | GitHub Actions | Repository-native verification for ruff, format, and pytest before merges. |
| Deployment | Local operator machine in v1 | Paid validation should not require public SaaS or infrastructure spend. |

## Security Boundaries

### Authentication

There are no HTTP routes or multi-user sessions in v1. The local CLI assumes the operator already controls the local workspace. If a web UI, API, or shared storage path is added later, authentication and authorization must be designed in an ADR before implementation.

### Tenant Isolation

V1 is single-tenant per local audit workspace. Each audit input set is isolated by directory and manifest. Multi-tenant storage, shared SaaS accounts, and row-level security are out of scope until a future productization ADR.

### PII and Confidential Data Policy

No confidential trade data, trader identity, broker account identifier, account balance, raw export row, free-text note, Telegram handle, or contact detail may appear in logs, span attributes, metrics labels, committed fixtures, or error messages returned by future APIs. Where an identifier is necessary for diagnostics, use a stable SHA-256 hash. Test fixtures must be anonymized and must not contain real accounts or customer data.

## Observability

| Dimension | Choice | Notes |
|-----------|--------|-------|
| Tracing | Shared noop tracer initially | Shared module: `trader_risk_audit/observability.py`. Replace only through ADR or task. |
| Metrics | None in local v1 | Batch runtime can print non-confidential summary counts. No metrics labels may include confidential values. |
| Logging | Python stdlib logging | Logs may include counts, file basenames, hashes, rule ids, and non-sensitive error codes only. |
| Dashboards | N/A | No hosted runtime in v1. |
| Alerting | N/A | Operator reviews command exit status and generated manifest. |

### Observability Invariants

- No confidential trading data or PII in logs, traces, metrics, or test output.
- All future external calls must be wrapped through the shared tracing module.
- If a web/API surface is added, `GET /health` must return `{"status": "ok"}` and must not expose confidential data.

## External Integrations

| Integration | Purpose | Auth method | Rate limit / SLA |
|-------------|---------|-------------|------------------|
| None in core v1 | Local imports and local reports do not require external APIs. | N/A | N/A |
| Telegram delivery, optional later | Prepare or send a concise report packet where traders already communicate. | Manual copy in v1; bot token by env var only if enabled by ADR/task. | Not a dependency for core audit generation. |

## File Layout

```text
trader-risk-audit/
├── trader_risk_audit/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── observability.py
│   ├── trades/
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   └── importers.py
│   ├── policy/
│   │   ├── __init__.py
│   │   ├── review.py
│   │   ├── schema.py
│   │   └── validation.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── aggregates.py
│   │   ├── attribution.py
│   │   ├── calendar.py
│   │   ├── rules.py
│   │   └── violations.py
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── claim_guard.py
│   │   ├── markdown.py
│   │   └── model.py
│   ├── artifacts/
│   │   ├── __init__.py
│   │   └── manifest.py
│   └── storage/
│       ├── __init__.py
│       └── retention.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   ├── unit/
│   └── integration/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── spec.md
│   ├── tasks.md
│   ├── CODEX_PROMPT.md
│   ├── IMPLEMENTATION_CONTRACT.md
│   ├── DECISION_LOG.md
│   ├── IMPLEMENTATION_JOURNAL.md
│   ├── EVIDENCE_INDEX.md
│   ├── audit/
│   ├── prompts/
│   └── adr/
├── .github/workflows/ci.yml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

## Runtime Contract

| Variable | Description | Example value | Required |
|----------|-------------|---------------|----------|
| `TRA_ENV` | Runtime environment label used in logs and manifests. | `local` | No, default `local` |
| `TRA_UPLOAD_DIR` | Local directory where operator stores input exports outside source control. | `./data/uploads` | No, default `./data/uploads` |
| `TRA_REPORT_DIR` | Local directory where reports and manifests are written. | `./artifacts/reports` | No, default `./artifacts/reports` |
| `TRA_LOG_LEVEL` | Logging level for local CLI diagnostics. | `INFO` | No, default `INFO` |
| `TRA_DATABASE_URL` | Optional SQLite or DuckDB URL if a later task adds local query storage. | `sqlite:///./local.sqlite3` | No |
| `TRA_TELEGRAM_DELIVERY_ENABLED` | Feature flag for future Telegram bot delivery. Must remain `false` until approved. | `false` | No, default `false` |
| `TRA_TELEGRAM_BOT_TOKEN` | Optional Telegram token if bot delivery is later approved. Example shows format only. | `123456:placeholder` | No |
| `TRA_TELEGRAM_CHAT_ID` | Optional Telegram chat id if bot delivery is later approved. | `123456789` | No |
| `TRA_LIVE_BROKER_API_ENABLED` | Explicit guard flag; live broker APIs are forbidden in v1. | `false` | No, must be `false` |
| `TRA_ORDER_BLOCKING_ENABLED` | Explicit guard flag; order blocking is forbidden in v1. | `false` | No, must be `false` |

## Continuity and Retrieval Model

### Canonical Truth

| Artifact | Authority |
|----------|-----------|
| `docs/ARCHITECTURE.md` | Architecture, profile, runtime, security, and boundary decisions. |
| `docs/IMPLEMENTATION_CONTRACT.md` | Immutable implementation rules. |
| `docs/spec.md` | Product feature scope and acceptance criteria. |
| `docs/tasks.md` | Task graph and agent execution contracts. |
| `docs/CODEX_PROMPT.md` | Live session state, baseline, next task, findings, and phase history. |
| `docs/adr/` | Formal changes to architecture, runtime, profiles, or immutable contract rules. |
| `docs/audit/` | Phase validation, review reports, and proof history. |
| Code and tests | Actual behavior and executable evidence. |

### Retrieval Convenience

| Artifact | Purpose | Required? |
|----------|---------|-----------|
| `docs/DECISION_LOG.md` | Quick index of key architecture and policy decisions. | Yes |
| `docs/IMPLEMENTATION_JOURNAL.md` | Durable cross-session handoff notes. | Yes |
| `docs/EVIDENCE_INDEX.md` | Index of proof artifacts, especially the heavy P&L attribution task and future pilot evidence. | Yes |

### Scoped Retrieval Rules

- Tasks that change architecture, runtime, rule semantics, P&L attribution, report claims, retention, or open findings must include `Context-Refs`.
- Agents read task `Context-Refs` first, then the linked canonical documents or proof artifacts.
- Retrieval convenience artifacts summarize and index. They do not overrule canonical files, tests, ADRs, or audit reports.
- If real pilot evidence changes the product direction, update `docs/DECISION_LOG.md` and add an ADR when architecture or scope changes.

## Non-Goals (v1)

- No live broker or exchange API integration.
- No order blocking, live risk guard, or capital-control path.
- No automated strategy trading or AI-generated profitable strategies.
- No full SaaS dashboard, public marketplace, mobile app, or multi-tenant auth system.
- No institutional compliance tooling or formal attestation workflow.
- No multimodal retrieval and no managed RAG corpus.
- No runtime agent loop, autonomous planner, or LLM-owned violation truth.
- No performance, profit, investment-advice, or causal-loss claims beyond deterministic audit evidence.
- No paid infrastructure dependency before paid pilot and repeat-use evidence justify it.
