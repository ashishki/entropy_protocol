# Entropy Core Project Brief

Use this brief before running `prompts/STRATEGIST.md` or a product-local
bootstrap session inside `products/entropy-core/`.

---

## 1. Project

- **Project name:** Entropy Core
- **One-sentence summary:** Governed systematic research engine and deterministic
  audit primitive layer for the Entropy Protocol product portfolio.
- **Why this project exists:** The current codebase already contains serious
  research infrastructure: Trial Registry, strict IS/OOS separation,
  walk-forward evaluation, SimBroker, P&L attribution, governance state machine,
  phase-gate evidence, and append-only audit discipline. It must be continued
  into a usable research MVP without weakening the research firewall or turning
  into live trading infrastructure.
- **What success looks like in v1:** A local operator can run a complete,
  human-gated, non-live research workflow on real historical data: register a
  research object, bind data/code/policy hashes, run leakage-resistant
  evaluation where explicitly approved, generate deterministic evidence/report
  packets, and expose protocol-safe primitives for product workspaces.

## 2. Users and Workflows

- **Primary users / operators:** Founder/operator, internal research engineer,
  future product teams using protocol-safe primitives, and human reviewers.
- **Main workflow 1:** Human registers a hypothesis or research object in the
  Trial Registry before evaluation.
- **Main workflow 2:** Operator runs controlled historical evaluation with
  leakage checks, cost/slippage assumptions, and deterministic evidence output.
- **Main workflow 3:** Product teams reuse deterministic registry, policy,
  audit-log, and report primitives without importing live execution risk.

## 3. Scope

- **In scope for v1:** Existing core stabilization, local CLI workflows,
  registry hardening, deterministic evidence generation, report generation,
  data import contracts, phase-gate packets, risk policy/violation record
  primitives for Trader Risk Audit, and human-gated hypothesis/backtest bridge
  design.
- **Out of scope / non-goals:** Live feeds by default, broker/exchange
  integration, live capital, order blocking, autonomous AI trading,
  AI-generated strategies entering evaluation without human registration,
  production/capital-ready labels, unsupported OOS/performance claims, public
  SaaS, marketplace, signal scraping, and institutional compliance motion.

## 4. AI Scope

- **Where AI may be needed:** Developer assistance, research-assist drafts,
  documentation synthesis, structured hypothesis drafting before human
  approval, and optional report narrative summarization after deterministic
  facts are produced.
- **Where AI is explicitly not wanted:** Runtime trading path, strategy
  execution, live capital decisions, registry writes, gate decisions, OOS claims,
  metric computation, risk rule evaluation, or evidence truth generation.
- **Possible retrieval / RAG need:** Text-only retrieval over canonical docs,
  decisions, tasks, audit findings, evidence index, and implementation journal.
- **If retrieval is needed, is text-only likely sufficient or is multimodal evidence truly required:** Text-only is sufficient for v1.
- **If multimodal may be needed, which modalities and why:** Not needed for core
  v1. Chart/screenshot work belongs outside core unless an explicit future gate
  approves it.
- **Possible tool-use need:** Local filesystem, pytest, ruff, pyright, Alembic,
  DuckDB/Parquet tooling, PostgreSQL for integration tests.
- **Possible planning / agentic behavior need:** AI planning is allowed only as a
  development workflow. Application runtime remains human-gated and
  deterministic.

## 5. Deterministic Candidates

- **Validation / policy checks:** Trial readiness, registry completeness,
  leakage gates, holdout locks, no-claim labels, phase boundary checks.
- **Routing / decision rules:** State-machine transitions, approval gates,
  allowed/denied evaluation modes, append-only write permissions.
- **Calculations / transformations:** Hashing, dataset normalization, SimBroker
  fills/costs, walk-forward splits, attribution, report payload assembly.
- **Retries / idempotency / audit triggers:** Registry insert behavior, evidence
  packet creation, audit index updates, migration checks, report regeneration.

## 6. Human Approval Boundaries

- **What actions must require human approval:** Research object registration,
  evaluation execution, holdout unlock, phase-gate acceptance, protocol boundary
  changes, new data-provider activation, language/runtime escalation, any bridge
  from product workspace into core governance.
- **What can be automated safely:** Schema validation, hash computation,
  deterministic report assembly, local test execution, lint/type checks,
  read-only evidence lookup, non-claim metadata generation.
- **Why these boundaries matter:** Core credibility depends on preregistration,
  reproducibility, no leakage, no false performance claims, and no accidental
  path toward live trading.

## 7. Risk and Error Cost

- **What is expensive if the system is wrong:** False research confidence,
  corrupted audit trail, leakage, invalid OOS claims, product teams reusing
  unsafe primitives.
- **What is expensive if the system is slow:** Research iteration slows and
  product teams avoid the core primitives.
- **What is expensive if the system is inconsistent / variable:** Evidence
  packets lose audit value and future agents cannot reproduce decisions.
- **Blast radius if it fails badly:** Medium to high inside the project:
  downstream products may inherit bad governance. No live capital blast radius
  is allowed in v1.
- **Audit / explainability needs:** Very high. Every result must point to input
  data, code hash, policy hash, task/evidence references, and human gates.

## 8. Data

- **Primary data sources:** Historical OHLCV data, local fixtures, Parquet
  datasets, registry records, run records, governance events, evidence/audit
  docs, future product-provided policy and violation records.
- **Approximate data volume:** Small to medium in v1; local historical datasets
  and pilot artifacts, not institutional-scale data.
- **Does data change frequently:** Market data and pilot artifacts can change;
  registered evidence and governance records are append-only.
- **Sensitive / regulated data present:** Strategy specifications and product
  pilot artifacts are confidential. No user PII should be introduced by core v1.
- **Retention / deletion expectations:** Core governance records and evidence
  are append-only. Generated local data/artifacts may be ignored or archived
  according to explicit artifact policy.

## 8b. Continuity and Evidence

- **Which decisions are likely to be revisited later:** Whether to open
  holdout, whether to activate hypothesis/backtest bridge, whether to expose
  core primitives to Trader Risk Audit, whether to add real data providers, and
  whether to escalate beyond local CLI workflows.
- **What prior evidence or proof will future agents need to find quickly:** Task
  graph, decision log, implementation journal, evidence index, audit reports,
  phase-gate packets, canonical charter/protocol docs, and test baselines.
- **Will work span multiple sessions / agents / weeks:** Yes.
- **Any existing docs, ADRs, audits, or notes that should become retrieval anchors:** `docs/CODEX_PROMPT.md`, `docs/tasks.md`,
  `docs/IMPLEMENTATION_CONTRACT.md`, `docs/ARCHITECTURE.md`,
  `docs/EVIDENCE_INDEX.md`, `docs/DECISION_LOG.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/audit/REVIEW_REPORT.md`,
  `../../docs/PRODUCT_PORTFOLIO.md`.

## 9. Integrations

- **External APIs / services:** PostgreSQL locally/CI, DuckDB embedded, Parquet
  filesystem. No live broker/exchange APIs in v1.
- **Databases / storage:** PostgreSQL for registry/run/governance tables,
  filesystem/Parquet for datasets, Markdown/JSON artifacts for evidence.
- **Auth / identity provider:** None in v1; local single-operator workflow.
- **Webhooks / messaging / queues:** None in core v1.

## 10. Constraints

- **Preferred stack:** Python 3.12, Pydantic v2, Polars, PyArrow/Parquet,
  DuckDB, PostgreSQL 16, SQLAlchemy/Alembic, Typer/Rich, pytest, ruff, pyright.
  Python-first does not mean Python-only forever: hot paths must remain behind
  stable contracts so Rust or Go can be introduced by ADR if profiling proves a
  need.
- **Deployment target:** Local workspace and CI. No public deployment required
  for core v1.
- **Budget constraints:** High cost discipline. Prefer local deterministic
  tooling and no paid runtime dependencies by default.
- **Latency / throughput expectations:** Batch/local research workflows;
  correctness and reproducibility beat low latency. Set explicit thresholds
  before optimizing or changing language.
- **Compliance requirements:** Internal governance only; no SOC2/institutional
  compliance claim in v1.
- **Network / security restrictions:** No external network egress by default;
  secrets only through environment variables; no committed credentials.

## 11. Runtime and Operations

- **Should runtime stay simple (managed service / container) if possible:** Yes.
  Local CLI plus test/CI service dependencies are enough for v1.
- **Any need for shell, package, or toolchain mutation at runtime:** No.
  Development tooling may run shell commands; application runtime should not
  mutate toolchains.
- **Any need for privileged actions or long-lived isolated workers:** No.
- **Recovery / rollback expectations:** Re-run deterministic commands from
  registered inputs and hashes; migrations must be controlled and tested.
- **Language/runtime escalation expectation:** Any Rust, Go, C/C++, native
  extension, FFI, or second runtime service requires a benchmark, ADR,
  CI/toolchain plan, rollback plan, and human approval.

## 12. Model and Cost Expectations

- **Cost sensitivity:** medium
- **Latency sensitivity:** low
- **Expected request / task volume:** Low in v1; research and pilot workflows.
- **If AI is used, should the system prefer smaller / cheaper models by default:** Yes for documentation/summarization; stronger models only for complex design review.
- **Any required capabilities:** reasoning, structured output, long context for
  docs. No multimodal required in core v1.
- **Preview-model tolerance:** low for project docs; none for runtime behavior.

## 13. Success Metrics

- **Business success metric:** Core primitives support at least one validated
  product workflow without weakening protocol boundaries.
- **Quality metric:** Full local test suite, ruff, format check, pyright, and
  diff check pass from `products/entropy-core/`.
- **Latency metric:** End-to-end local pilot workflow completes fast enough for
  daily research iteration; exact target to be set after profiling.
- **Cost metric:** No required paid API/service for core v1 beyond local/CI
  infrastructure.
- **Operational metric:** A new agent can continue core work from
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, and evidence docs without rereading
  archives by default.
