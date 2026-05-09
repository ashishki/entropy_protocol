# Architecture — Signal Analytics Sandbox

Version: 1.1
Last updated: 2026-05-09
Status: Phase 10 complete; Phase 11 Author Market Intelligence architecture reset planned

---

## System Overview

Signal Analytics Sandbox is a public-source signal-source audit product. An operator points the system at a public Telegram channel, X account, or website ledger; the system turns messy historical trading calls into a structured signal ledger, deterministically matches them against historical market data, and produces an evidence-backed audit report showing what the source actually did historically. The product serves traders evaluating signal sources, market researchers, and small due-diligence teams. It is a local-first Python library + CLI in v1; it is not a trading bot, copy-trading system, scraper, investment-advice product, or evidence source for Entropy Core.

The system is structured as a deterministic core (schema validation, ledger normalization, outcome matching, return calculation, report generation) wrapped by adapters at two boundaries: the **price-data adapter layer** (operator-file, ccxt-style public exchange OHLCV, optional paid data, optional yfinance-prototype) and the **extraction adapter layer** (manual, rule/regex parser, optional gated LLM draft). The deterministic core is single-source-of-truth; adapters are replaceable and never mutate ledger or outcome semantics on their own.

Phase 11 expands the product target to **Author Market Intelligence**. The new
direction keeps the Phase 10 draft extraction work as the first channel profile
and adds a planned path toward source-corpus normalization, local retrieval,
market-idea extraction, deterministic thesis evaluation, and bounded batch
analysis. The first Phase 11 task (`SAS-MI-001`) must decide capability-profile
activation and runtime/storage choices through ADR before any RAG, vector store,
or agent-loop implementation begins.

See `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md` for the detailed
development roadmap.

---

## Required Decision Summary

### 1. Solution Shape Recommendation

**Hybrid** — deterministic core for ledger, outcome matching, and report generation; bounded workflow orchestration for the operator capture/extraction pipeline; LLM-assist as a gated, human-reviewed adapter (not a primary path).

### 2. Rejected Simpler Alternatives

| Rejected option | Why insufficient |
|-----------------|------------------|
| Pure deterministic, no LLM at all | Manual extraction does not scale once paid pilots prove demand; we want a pre-built escalation path so that "add LLM later" is a contract change, not a re-architecture. |
| Pure workflow with no deterministic core | Audit/explainability needs are very high — every reported signal must trace to a deterministic outcome rule, not a probabilistic judgment. |
| Bounded ReAct / tool-using agent | No multi-step decision loop is needed. A single-pass extraction draft per post, gated by human review, suffices. |
| Higher-autonomy agent | Forbidden by the brief — autonomous scraping, autonomous publication, and unsupervised LLM "truth" are explicit non-goals. |

### 3. Runtime Recommendation

**T0** — local Python library + CLI executed on the operator's workstation. No isolated runtime, no shell mutation, no privileged actions, no persistent worker, no network egress beyond declared adapters.

### 4. Runtime Justification

| Property | Reasoning |
|----------|-----------|
| Mutable runtime need | None — no shell, package, or toolchain mutation at runtime. |
| Privilege surface | None — no root, no privileged sockets, no system-state changes. |
| Persistence need | Local files (JSON/Parquet/Markdown) on the operator's disk; no long-lived worker state. |
| Recovery / rollback | Re-run from the same source ledger snapshot + price snapshot reproduces the report bit-for-bit. |
| Drift risk | Low — no auto-updating dependencies, no mutable runtime. Adapter changes are explicit code changes reviewed in the normal cycle. |
| Why not T1/T2/T3 | T1 (container) buys nothing for a local CLI. T2/T3 are reserved for autonomous mutation/persistent workers — neither applies here. |

### 5. Deterministic Decomposition

| Subproblem | Owner | Reason |
|------------|-------|--------|
| Schema validation (signal records, sources) | Deterministic | Pydantic models enforce structure; no judgment. |
| Source eligibility / public-only checks | Deterministic | Allowlist-driven; SAS-002 memo defines policy. |
| Outcome matching (entry/stop/target evaluation) | Deterministic | Reproducibility is a hard requirement. |
| Return / MAE / MFE calculation | Deterministic | Pure arithmetic over price snapshots. |
| Aggregated win/loss/coverage stats | Deterministic | Pure aggregation over ledger + outcomes. |
| Report rendering (Markdown) | Deterministic | Template-driven; no LLM in v1 reports. |
| Deduplication and ambiguity flagging | Deterministic | Rule-based (timestamp + symbol + direction key). |
| Provenance/snapshot recording | Deterministic | Append-only metadata. |
| Extraction draft from messy text | LLM-optional | Adapter — manual + parser are default; LLM is a gated escalation. |

### 6. Human Approval Boundaries

| Boundary | Required? | Why |
|----------|-----------|-----|
| Source eligibility judgment (is this source legally collectable?) | Yes | Legal/ToS risk; misclassification can look like unauthorized scraping. |
| Final signal record before evaluation | Yes | LLM/parser drafts are never truth; human approves each record. |
| Public report release | Yes | Reputational and legal exposure on every published report. |
| Activating LLM extraction adapter (cost-capped) | Yes | Cost discipline + non-truth posture. |
| Activating a paid price-data provider | Yes | Cost discipline; brief forbids paid-API dependency before paid-pilot validation. |
| Re-running a deterministic report on existing approved ledger + snapshot | No | Pure reproducibility; no judgment. |

### 7. Minimum Viable Control Surface

- Source eligibility memo (SAS-002) cited from every report.
- Per-signal evidence reference (URL, capture timestamp, raw-text hash).
- Deterministic outcome rule cited per signal.
- Price snapshot SHA-256 + provider name + as-of timestamp recorded per report.
- Non-advice disclaimer rendered in every report.
- LLM adapter, if activated, cost-capped per run with explicit human-approval flag.

### 8. Cost / Risk Reasoning

- **Cost of error:** misrepresenting a source's historical performance is the primary risk → audit requires per-signal evidence + deterministic outcome rule + reproducible price snapshot.
- **Cost of variance:** users will dispute reports that change between runs → reproducibility is a hard contract (re-run with same inputs ⇒ identical outputs).
- **Latency:** low priority — pilot reports are batch.
- **Blast radius:** medium — no live capital, but reputational/legal risk on a wrong public report.
- **Auditability:** very high — required by both the brief and the product's value proposition.
- **Drift risk:** low — small footprint, no autonomous components.

### 9. Model Strategy

LLM is opt-in and gated. Default path is fully deterministic + manual/parser-based extraction.

| Workload | Deterministic alternative | Chosen model class | Why this class | Fallback / escalation | Validation metric |
|----------|---------------------------|---------------------|----------------|-----------------------|-------------------|
| Extraction draft from messy public text (Phase 6) | Manual extraction + rule/regex parsers (default) | Small structured-output model (e.g., Claude Haiku 4.5 or local Ollama small model) | Cost sensitivity is high; structured output is the only required capability; reasoning depth is low (extract one trade record from one post). | If model fails or is withdrawn, fall back to manual + parser adapters with no behavior change. | Extraction acceptance rate by human reviewer; cost per accepted record; defer-to-human rate. |
| Outcome calculation, returns, statistics, report rendering | Always deterministic | None | LLMs introduce variance; brief forbids LLM-derived "truth" in stats. | N/A | N/A |

Preview-model tolerance: low for extraction drafts, zero for any path that touches outcomes or report numbers.

---

## Solution Shape

| Decision | Selection | Justification |
|----------|-----------|---------------|
| Primary shape | Hybrid (deterministic core + bounded workflow + gated LLM-assist adapter) | Minimum sufficient — deterministic where reproducibility matters, LLM only as a gated extraction escalation. |
| Governance level | Lean | Local sandbox, single-operator, no live capital, low blast radius. Audit-heaviness is encoded as project-specific contract rules rather than as Standard-grade ceremony. |
| Runtime tier | T0 | Local Python; no isolation, mutation, or persistence requirements above what a normal CLI provides. |

### Rejected Lower-Complexity Options

| Rejected option | Why insufficient |
|-----------------|------------------|
| Deterministic-only | Manual extraction is the bottleneck for paid pilots. We want a contract-bound LLM escalation path now, even if v1 ships parser-first. |
| Workflow / human-in-the-loop assistant only | Outcome matching and report rendering must be deterministic, not workflow-orchestrated guesses. |
| Simple tool use without planning / loops | Adequate, but indistinguishable from "deterministic + adapter" — we name the latter explicitly because the LLM is an adapter, not an LLM-directed tool call at inference time. |

### Minimum Viable Control Surface

- Source eligibility memo (SAS-002) is cited by every report.
- Every signal record carries an evidence reference (URL or capture path, capture timestamp, raw-text SHA-256).
- Every report records the price snapshot's provider, as-of timestamp, and SHA-256.
- Every report includes a non-advice disclaimer block.
- LLM extraction, if activated, is cost-capped per run and gated by human approval.

### Human Approval Boundaries

| Boundary | Human approval required? | Why |
|----------|--------------------------|-----|
| Source eligibility | Yes | Legal/ToS risk per SAS-002. |
| Final signal record | Yes | Brief forbids treating extraction output as truth. |
| Public report release | Yes | Reputational/legal exposure. |
| Activating LLM extraction adapter | Yes | Cost discipline + non-truth posture. |
| Activating paid price-data adapter | Yes | Cost discipline (brief forbids paid-API before validation). |
| Re-running deterministic report on approved inputs | No | Pure reproducibility. |

### Deterministic vs LLM-Owned Subproblems

| Subproblem | Owner | Reason |
|------------|-------|--------|
| Schema validation, source eligibility, dedup, ambiguity flagging | Deterministic | Reproducible, rule-based. |
| Outcome matching, return / MAE / MFE / aggregated stats | Deterministic | Audit/correctness is a hard contract. |
| Report rendering (Markdown, including disclaimers and provenance) | Deterministic | Templated; no LLM in v1 reports. |
| Extraction draft from messy text | LLM-optional adapter | Manual + parser is default; LLM is a gated escalation only. |

### Runtime and Isolation Model

| Property | Decision |
|----------|----------|
| Isolation boundary | Process boundary on the operator's local workstation. |
| Persistence model | Local files (JSON, Parquet, Markdown) under a configurable workspace directory. |
| Network model | Adapters declare their own egress; default config makes zero network calls. |
| Secrets model | Adapter API keys (only paid-price or LLM adapters) read from environment variables; no secrets in source. |
| Runtime mutation boundary | None — no shell, package, or toolchain mutation at runtime. |
| Rollback / recovery model | Re-run from the same source ledger + price snapshot reproduces the report. Snapshots are immutable. |

T1/T2/T3 are not justified. A future long-running collector service or hosted SaaS would require an ADR and a separate runtime decision.

---

## Inference / Model Strategy

| Path / Task | Model class | Why this class | Fallback / escalation | Budget / latency constraint |
|-------------|-------------|----------------|-----------------------|-----------------------------|
| Extraction draft (Phase 6, opt-in) | small structured-output model (Claude Haiku 4.5 or local Ollama small model) | Lowest sufficient for one-post → one structured record; structured output is the only hard capability requirement. | Local Ollama small model as fallback if cloud provider is degraded or cost-capped; manual + parser as ultimate fallback. | Per-pilot run cost cap declared in `signal-sandbox` config; latency p95 ≤ 10 s per post is acceptable. |
| Any path that touches outcomes, returns, statistics, or report numbers | None — deterministic only | Brief forbids LLM-derived numerical "truth". | N/A | N/A |

Rules:
- Per-workload selection. No global default model.
- Deterministic alternative (manual + parser) is always considered first and always implemented first.
- Stronger models are only justified by measured insufficient extraction acceptance rate.
- Cost is recorded per pilot run; a cost-cap breach aborts the run.

---

## Capability Profiles

| Profile    | Status | Declared in Phase | Notes |
|------------|--------|-------------------|-------|
| RAG        | OFF    | 1                 | No managed corpus, no ingestion pipeline; per-post extraction needs no retrieval. |
| Tool-Use   | OFF    | 1                 | Price-data adapters and LLM extraction are deterministic application code, not LLM-directed tool calls at inference time. |
| Agentic    | OFF    | 1                 | Single-pass extraction with human review; no decision loop. |
| Planning   | OFF    | 1                 | No structured plan output as primary deliverable. |
| Compliance | OFF    | 1                 | No named regulatory framework (HIPAA/SOC 2/PCI-DSS/GDPR) applies. ToS / non-advice / public-source rules are enforced as project-specific contract rules. |

**RAG OFF — Justification.** The system processes individual public posts and a finite per-pilot ledger. The knowledge needed to extract or evaluate a signal is contained in the post itself plus the price snapshot. There is no large document corpus, no citation requirement that needs retrieval (citations are simple URL/timestamp pairs), and no knowledge that changes faster than the code deploy cycle. Adding retrieval would be speculative complexity.

**Tool-Use OFF — Justification.** The LLM (when used) receives a post text and returns a structured record. It does not call tools, query APIs at inference time, or take side-effecting actions. Price providers and ledger I/O are deterministic application code paths invoked by the operator workflow, not LLM-directed.

**Agentic OFF — Justification.** Each post is processed in a single pass, output is human-reviewed, and there is no observe → decide → act → observe loop. Even the operator workflow is a fixed pipeline, not an agent.

**Planning OFF — Justification.** The system produces signal ledgers and audit reports, not structured plans consumed by downstream automation. No plan schema, no plan-to-execution contract.

**Compliance OFF — Justification.** No PHI, PII (beyond public-author handles), PAN, or government-classified data. No HIPAA/SOC 2/PCI/GDPR framework applies. ToS-respect, public-source-only, and non-advice-claim rules are encoded as project-specific contract rules in `docs/IMPLEMENTATION_CONTRACT.md`.

Phase 11 note: RAG, Planning, and Agentic profiles remain OFF until
`SAS-MI-001` records an ADR and updates this table. The roadmap intentionally
plans RAG and a bounded batch analyst, but implementation must not precede the
profile/runtime decision.

---

## Component Table

| Component | File / Directory | Responsibility |
|-----------|-----------------|----------------|
| CLI entry point | `src/signal_sandbox/cli.py` | Console script `signal-sandbox`; thin dispatcher to subcommand modules. |
| Source manifest | `src/signal_sandbox/sources/manifest.py` | Pydantic models for source eligibility, ToS reference, capture metadata. |
| Capture loader | `src/signal_sandbox/capture/loader.py` | Load operator-captured raw posts (JSON/Markdown) from workspace. |
| Extraction interface | `src/signal_sandbox/extraction/base.py` | `ExtractionAdapter` ABC: post → draft `SignalRecord`. |
| Manual extraction | `src/signal_sandbox/extraction/manual.py` | CLI-driven manual entry; pre-fills evidence fields. |
| Rule extraction | `src/signal_sandbox/extraction/rule.py` | Regex/template adapters keyed by source format. |
| LLM extraction (opt-in) | `src/signal_sandbox/extraction/llm.py` | Gated, cost-capped LLM adapter; not active by default. |
| Draft validation | `src/signal_sandbox/extraction/draft_validation.py` | Deterministically verifies pseudo-label evidence spans and candidate fields against raw capture text. |
| Draft parser | `src/signal_sandbox/extraction/draft_parser.py` | Pure/local parser over `CapturedPost` plus static accepted author-profile terms; returns review-only draft statuses. |
| Draft export | `src/signal_sandbox/extraction/draft_export.py` | Deterministically renders review-pending draft rows; never writes approved ledger records. |
| Signal record schema | `src/signal_sandbox/ledger/record.py` | `SignalRecord` Pydantic model + validation rules. |
| Ledger I/O | `src/signal_sandbox/ledger/io.py` | Read/write ledger files (JSON for raw, Parquet for normalized); idempotent. |
| Dedup + ambiguity | `src/signal_sandbox/ledger/dedup.py` | Deterministic dedup keys; ambiguity flagging. |
| Price provider interface | `src/signal_sandbox/prices/base.py` | `PriceDataProvider` ABC; defines snapshot contract. |
| Operator-file price provider | `src/signal_sandbox/prices/operator_file.py` | Read OHLCV from operator-supplied CSV/Parquet. |
| Exchange-public price provider | `src/signal_sandbox/prices/exchange_public.py` | ccxt or named public-exchange OHLCV adapter. |
| Paid price provider (gated) | `src/signal_sandbox/prices/paid.py` | Optional paid adapter; activation requires human approval flag. |
| YFinance prototype provider | `src/signal_sandbox/prices/yfinance_dev.py` | Dev/prototype only — never canonical evidence without explicit approval. |
| Price snapshot recorder | `src/signal_sandbox/prices/snapshot.py` | Records price snapshot SHA-256, provider, as-of, range. |
| Outcome matcher | `src/signal_sandbox/outcomes/matcher.py` | Deterministic entry/stop/target evaluation per signal. |
| Returns / MAE / MFE | `src/signal_sandbox/outcomes/metrics.py` | Pure-function calculations over snapshots. |
| Aggregator | `src/signal_sandbox/outcomes/aggregate.py` | Win/loss/coverage/drawdown summaries. |
| Report generator | `src/signal_sandbox/reports/markdown.py` | Markdown report with disclaimers, provenance, and evidence links. |
| Config | `src/signal_sandbox/config.py` | Workspace path, adapter activation flags, cost caps. |
| Logging / tracing | `src/signal_sandbox/observability.py` | Shared `get_tracer()` (no-op tracer in v1) + structured logger. |
| Tests | `tests/` | unit/, integration/, eval/ (eval/ for any LLM/parser quality measurements). |

---

## Data Flow — Primary Path

End-to-end flow for a single pilot report (happy path):

1. Operator declares a public source in `<workspace>/sources/<source_id>.json` and updates `SourceManifest` (ToS reference, eligibility verdict per SAS-002).
2. Operator captures public posts into `<workspace>/captures/<source_id>/<capture_id>.{json,md}`. Each capture records URL, capture timestamp, raw text, and SHA-256.
3. Operator runs `signal-sandbox extract --source <source_id>`. The CLI loads captures and invokes the configured extraction adapter (manual, rule, or — if explicitly enabled — LLM). Each draft `SignalRecord` is written to `<workspace>/drafts/`.
4. Operator reviews drafts via `signal-sandbox review`. Approved records are written to `<workspace>/ledger/<source_id>.parquet`.
5. Operator runs `signal-sandbox snapshot --source <source_id> --provider <provider>`. The price provider produces a price snapshot and writes it (with SHA-256) to `<workspace>/snapshots/`.
6. Operator runs `signal-sandbox match --source <source_id> --snapshot <snapshot_id>`. The outcome matcher deterministically evaluates each signal against the snapshot and writes per-signal outcomes to `<workspace>/outcomes/`.
7. Operator runs `signal-sandbox report --source <source_id> --outcomes <outcomes_id>`. The report generator renders a Markdown report with provenance block (snapshot SHA, provider, as-of, ledger file SHA), per-signal evidence links, deterministic outcome rule citations, and a non-advice disclaimer.
8. Operator approves the report; the report is delivered manually to the pilot user.

Reproducibility contract: given the same `ledger/<source_id>.parquet` and the same `snapshots/<snapshot_id>` files, steps 6–7 produce a byte-identical Markdown report.

---

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.12 | Consistent with Entropy Core and the existing workspace; brief mandates 3.12. |
| Packaging | `pyproject.toml` (PEP 621) + setuptools or hatchling | Standard Python packaging; console script entry. |
| Data validation | Pydantic v2 | Brief specifies Pydantic; v2 has fast validators and strict mode. |
| Tabular | Polars (primary) + pandas (interop where needed) | Brief specifies both; Polars is faster and Parquet-native, pandas is the ecosystem interop layer. |
| Storage | Local files: JSON for raw captures and source manifests, Parquet for ledger and outcomes, Markdown for reports | Brief: "JSON/CSV/Parquet ledgers and Markdown reports. SQLite/DuckDB only if useful." |
| Crypto OHLCV (when activated) | `ccxt` | De facto standard for public exchange OHLCV; multi-exchange. |
| Equities OHLCV (dev/prototype only) | `yfinance` | Dev/prototype adapter; never canonical evidence without explicit approval per brief. |
| Optional paid price data | TBD per ADR | Adapter interface allows substitution without core changes. |
| LLM adapter (opt-in) | Local Ollama small model (default fallback) or Claude Haiku 4.5 | Cost-sensitivity-first; structured output the only hard capability requirement. |
| Lint / format | ruff | Single tool, zero configuration drift. |
| Type-check | pyright | Brief specifies pyright. |
| Tests | pytest | Brief specifies pytest. |
| CI | GitHub Actions | Standard for the workspace. |
| Deployment | Local CLI on operator workstation | Brief: "Local/manual sandbox first, not public SaaS." |

---

## Security Boundaries

### Authentication

**Not applicable in v1.** This is a local CLI run by a single operator on their own workstation. There is no API surface and no authentication. Activating any future hosted/multi-user mode requires an ADR and is out of scope for v1.

### Tenant Isolation

**Single-tenant.** No tenant isolation requirement. Operator-level isolation is provided by the operating system's file permissions on the workspace directory.

### PII Policy

The system handles only public-author handles (Telegram channel name, X handle) — these are public identifiers, not PII in the regulatory sense. Even so:

- No author-handle, raw-post text, or evidence URL appears in log messages, span attributes, or metrics labels.
- Where identifiers must be referenced in observability, the ledger row's deterministic dedup key (SHA-256 of `{source_id, timestamp, symbol, direction}`) is used.
- Captured raw post text is stored only in the workspace, never in logs.

### Public-Source-Only and ToS Posture

- Forbidden in code: any code path that performs authenticated scraping, scrapes private Telegram groups, bypasses paywalls or login walls, impersonates a source, or fetches behind any access control. Every capture path is operator-supplied or fetches a documented public endpoint.
- Every source must have a SourceManifest entry citing SAS-002 source-eligibility verdict.
- Violation: automatic P0.

---

## Observability

| Dimension | Choice | Notes |
|-----------|--------|-------|
| Tracing | No-op tracer in v1 | Shared `get_tracer()` in `src/signal_sandbox/observability.py`; reserved for OBS-1 contract; emits structured-log span enter/exit when verbose mode is set. |
| Metrics | Structured-log counters in v1 (no Prometheus / statsd) | Required event labels: `subcommand`, `source_id` (hashed if needed), `result`. |
| Logging | Python `logging` + JSON formatter | Required fields: `timestamp`, `subcommand`, `result`, `dedup_key_hash`. |
| Health endpoint | Adapted to CLI: `signal-sandbox status` | Returns config summary + version + workspace path; never includes raw post text or evidence URLs. |
| Alerting | N/A — local sandbox | Re-evaluated if v2 introduces a hosted runtime. |

### Observability Invariants

- No raw post text, evidence URL, or operator filename in log messages, span attributes, or metric labels.
- `signal-sandbox status` is the OBS-3 substitute and must not require authentication, must not log identifiers, and must not perform network calls.
- All adapter calls (price providers, LLM) are wrapped in a span with `operation_name` and a stable `provider_id`.

---

## External Integrations

| Integration | Purpose | Auth method | Rate limit / SLA | Activation |
|-------------|---------|-------------|------------------|------------|
| Public exchange OHLCV (ccxt) | Crypto historical price data | None / public endpoint | Per-exchange public-rate-limit; respect via ccxt defaults | Opt-in adapter; off by default. |
| `yfinance` | Equity historical price data — **dev/prototype only** | None | Best-effort, may break | Opt-in adapter; never canonical evidence without explicit operator approval. |
| Paid price-data provider (TBD) | Higher-quality historical OHLCV | API key (env var) | Per-vendor SLA | Opt-in adapter; activation gated by human approval flag in config. |
| LLM extraction adapter (Anthropic Claude / local Ollama) | Extraction draft from messy text | API key (env var) for cloud; none for local | Per-vendor rate limit | Opt-in adapter; off by default; cost-capped per run. |

There are no other external integrations. No webhooks, no message queues, no databases beyond local files in v1.

---

## File Layout

```
signal-analytics-sandbox/
├── src/
│   └── signal_sandbox/
│       ├── __init__.py
│       ├── cli.py                       # console-script entry
│       ├── config.py
│       ├── observability.py             # shared get_tracer(), JSON logger
│       ├── sources/
│       │   ├── __init__.py
│       │   └── manifest.py              # SourceManifest + eligibility validation
│       ├── capture/
│       │   ├── __init__.py
│       │   └── loader.py                # load operator-captured posts
│       ├── extraction/
│       │   ├── __init__.py
│       │   ├── base.py                  # ExtractionAdapter ABC
│       │   ├── manual.py
│       │   ├── rule.py
│       │   └── llm.py                   # gated, off by default
│       ├── ledger/
│       │   ├── __init__.py
│       │   ├── record.py                # SignalRecord Pydantic model
│       │   ├── io.py                    # JSON/Parquet I/O
│       │   └── dedup.py
│       ├── prices/
│       │   ├── __init__.py
│       │   ├── base.py                  # PriceDataProvider ABC
│       │   ├── operator_file.py
│       │   ├── exchange_public.py
│       │   ├── paid.py                  # gated
│       │   ├── yfinance_dev.py          # prototype only
│       │   └── snapshot.py
│       ├── outcomes/
│       │   ├── __init__.py
│       │   ├── matcher.py
│       │   ├── metrics.py
│       │   └── aggregate.py
│       └── reports/
│           ├── __init__.py
│           └── markdown.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── eval/                            # adapter-quality measurements (extraction, parser)
├── docs/
│   ├── ARCHITECTURE.md                  # this file
│   ├── spec.md
│   ├── tasks.md
│   ├── CODEX_PROMPT.md
│   ├── IMPLEMENTATION_CONTRACT.md
│   ├── DECISION_LOG.md
│   ├── IMPLEMENTATION_JOURNAL.md
│   ├── PROJECT_BRIEF.md
│   ├── audit/
│   ├── adr/
│   └── prompts/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .claude/
│   └── commands/
│       └── orchestrate.md
├── hooks/                               # already present
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Runtime Contract

These environment variables are read at startup. The application must fail fast with a clear error message if a required variable is malformed; absent optional variables disable the corresponding adapter.

| Variable | Description | Example value | Required |
|----------|-------------|---------------|----------|
| `SIGNAL_SANDBOX_WORKSPACE` | Absolute path to operator workspace directory | `/home/op/sas-workspace` | Yes |
| `SIGNAL_SANDBOX_LOG_LEVEL` | Logging level | `INFO` | No (default: `INFO`) |
| `SIGNAL_SANDBOX_COST_CAP_USD` | Per-run cost cap for paid adapters (price + LLM combined). 0 disables paid adapters. | `5.00` | No (default: `0.00`) |
| `SIGNAL_SANDBOX_ENABLE_LLM` | Master switch for LLM extraction adapter | `0` or `1` | No (default: `0`) |
| `ANTHROPIC_API_KEY` | Cloud LLM provider key (only when `SIGNAL_SANDBOX_ENABLE_LLM=1` and adapter is `claude`) | (real key in operator env) | Conditional |
| `OLLAMA_HOST` | Local Ollama endpoint (only when LLM adapter is `ollama`) | `http://localhost:11434` | Conditional |
| `SIGNAL_SANDBOX_ENABLE_PAID_PRICE` | Master switch for paid price-data adapter | `0` or `1` | No (default: `0`) |
| `SIGNAL_SANDBOX_PAID_PRICE_API_KEY` | API key for the active paid price-data adapter | (real key in operator env) | Conditional |

No real secrets in source. Example values document format only.

---

## Continuity and Retrieval Model

### Canonical Truth

| Artifact | Authority |
|----------|-----------|
| `docs/ARCHITECTURE.md` | Architecture, capability profiles, runtime, model strategy. |
| `docs/IMPLEMENTATION_CONTRACT.md` | Immutable rules. |
| `docs/tasks.md` | Task graph and acceptance criteria. |
| `docs/CODEX_PROMPT.md` | Live session state, baseline, open findings. |
| `docs/adr/` | Formal decision changes. |
| `docs/audit/` | Review history. |

### Retrieval Convenience

| Artifact | Purpose | Required? |
|----------|---------|-----------|
| `docs/DECISION_LOG.md` | Quick recall of major decisions; points to canonical source per row. | Yes |
| `docs/IMPLEMENTATION_JOURNAL.md` | Cross-session implementation handoff. | Yes |
| `docs/EVIDENCE_INDEX.md` | Proof lookup. | No (deferred) — current evidence volume is small; revisit when first heavy task ships. |

### Scoped Retrieval Rules

- Tasks tagged heavy (currently T12 outcome matcher, T14 report renderer, T20 LLM adapter) must include `Context-Refs` to the SAS-002 legal memo, the relevant ADR (if any), and the previous heavy-task evidence.
- Other tasks include `Context-Refs` only when they touch architecture, runtime, the public-source-only boundary, or an open finding.
- Retrieval surfaces summarize and index. They do not overrule canonical files.
- `docs/EVIDENCE_INDEX.md` is omitted in v1 because the evidence volume is operator-managed Markdown reports + workspace snapshots; we add it when heavy-task evidence accumulates beyond what `docs/audit/` and `docs/IMPLEMENTATION_JOURNAL.md` can index in-place.

---

## Non-Goals (v1)

- No private Telegram-group scraping, no scraping behind login or paywall, no source impersonation. Hard contract — violation is a P0.
- No live trading, copy-trading, broker integration, or order-routing.
- No investment-advice claims; every report carries an explicit non-advice disclaimer.
- No autonomous scraping agent or autonomous publication path.
- No paid X API dependency before paid pilot validation (SAS-001).
- No multimodal/OCR extraction in v1; deferred until a paid pilot proves screenshots are the bottleneck and SAS-002 covers screenshot capture.
- No public SaaS surface, no hosted deployment, no multi-tenant runtime.
- No contribution to Entropy Core's phase-gate evidence — Signal Analytics Sandbox is a separate validation product.
- No T1/T2/T3 runtime in v1; runtime escalation requires an ADR.
- No RAG, Tool-Use, Agentic, Planning, or Compliance profile is active until an
  ADR updates the capability table. Phase 11 is the next ADR gate for Author
  Market Intelligence.
