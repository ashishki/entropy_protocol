# Trader Risk Audit Project Brief

Use this brief before running `prompts/STRATEGIST.md` or a product-local
bootstrap session inside `products/trader-risk-audit/`.

---

## 1. Project

- **Project name:** Trader Risk Audit
- **One-sentence summary:** Upload/import-based trade review system that checks
  executed trades against self-defined risk rules and produces deterministic
  violation reports.
- **Why this project exists:** The strongest near-term wedge from the startup
  pressure test is not a full backtesting SaaS or trading bot. It is a painful,
  concrete trader workflow: traders break their own risk rules and need proof of
  which violations cost money.
- **What success looks like in v1:** A trader can provide a real trade export
  and written risk rules, receive an audit-grade violation report, pay for the
  result, and repeat the process without live broker/API integration.

## 2. Users and Workflows

- **Primary users / operators:** Active prop-style traders, funded-account
  traders, systematic retail traders with explicit risk rules, and small trading
  teams that review execution discipline.
- **Main workflow 1:** Trader uploads or sends executed trades plus written risk
  rules; operator normalizes them into a deterministic import/policy contract.
- **Main workflow 2:** System evaluates trades against rules such as max daily
  loss, cooldown after loss threshold, max position size, forbidden assets, max
  leverage, max drawdown, and strategy adherence.
- **Main workflow 3:** Trader receives a report showing violations, timestamps,
  repeated rule failures, violation-attributed P&L, and next review actions.

## 3. Scope

- **In scope for v1:** Concierge/manual audit pilot, trade export normalization,
  risk policy schema, deterministic rule checks, violation record model,
  violation-attributed P&L summary, Markdown report, Telegram-ready delivery
  packet, local CLI/script workflow, and anonymized fixture tests.
- **Out of scope / non-goals:** Live broker/exchange APIs, order blocking, live
  risk guard, full SaaS dashboard, mobile app, public marketplace, automatic
  strategy trading, AI-generated profitable strategies, institutional compliance
  tooling, and unsupported performance claims.

## 4. AI Scope

- **Where AI may be needed:** Drafting rule schema from trader-written rules,
  normalizing messy column names with human review, report narrative summaries,
  Telegram-friendly formatting, and internal development assistance.
- **Where AI is explicitly not wanted:** Final rule evaluation, P&L arithmetic,
  violation truth, trading advice, broker actions, risk lock enforcement, or
  any runtime trading path.
- **Possible retrieval / RAG need:** Text-only retrieval over user-provided rule
  documents, report templates, product decisions, and prior pilot findings.
- **If retrieval is needed, is text-only likely sufficient or is multimodal evidence truly required:** Text-only is sufficient for the first MVP.
- **If multimodal may be needed, which modalities and why:** Later screenshots
  of broker statements may appear, but v1 should avoid multimodal dependence.
- **Possible tool-use need:** CSV/XLSX parsing, local filesystem, report
  generation, optional Telegram delivery preparation, pytest/ruff/pyright.
- **Possible planning / agentic behavior need:** No runtime agent loop. AI can
  assist product planning and code development only.

## 5. Deterministic Candidates

- **Validation / policy checks:** Required trade columns, timestamp parsing,
  symbol/account normalization, rule schema validation, allowed rule types.
- **Routing / decision rules:** Which rule evaluator runs for each policy,
  severity classification, report section inclusion.
- **Calculations / transformations:** Daily P&L, drawdown, position size,
  leverage, cooldown window, violation attribution, aggregate summaries.
- **Retries / idempotency / audit triggers:** Re-running the same import and
  rule set should produce identical violation records and report hashes.

## 6. Human Approval Boundaries

- **What actions must require human approval:** Accepting a trader's written
  rule interpretation, resolving ambiguous exports, adding a new rule type,
  sending a paid report, claiming a behavior caused losses, and any future move
  toward live broker/exchange integration.
- **What can be automated safely:** Parsing supported export formats,
  deterministic rule evaluation, report assembly, fixture validation, local
  regression tests, anonymized sample generation.
- **Why these boundaries matter:** The product will be trusted only if traders
  believe the audit is strict and explainable, not AI-inferred blame or trading
  advice.

## 7. Risk and Error Cost

- **What is expensive if the system is wrong:** Incorrectly accusing a trader of
  rule violations, missing costly violations, bad P&L attribution, or producing
  advice-like claims.
- **What is expensive if the system is slow:** Paid pilot delivery becomes
  manual consulting without product leverage.
- **What is expensive if the system is inconsistent / variable:** Traders will
  stop trusting repeated audits and teams cannot use it for discipline review.
- **Blast radius if it fails badly:** Medium in v1 because it affects trader
  decisions and trust, but no live capital action is allowed.
- **Audit / explainability needs:** High. Every violation should show source
  trade rows, rule id, evaluated values, threshold, timestamp, and P&L impact.

## 8. Data

- **Primary data sources:** Broker/exchange trade exports, manually provided
  risk rules, account/day metadata, optional notes/tags.
- **Approximate data volume:** Small in v1; hundreds to tens of thousands of
  rows per audit.
- **Does data change frequently:** New exports arrive per day/week. Historical
  audit inputs should be immutable once reported.
- **Sensitive / regulated data present:** Trading history is confidential.
  Avoid PII where possible; anonymize fixtures and examples.
- **Retention / deletion expectations:** Pilot data retention must be explicit.
  Default should be local-only storage, no unnecessary retention, and deletion
  on user request unless needed for paid report evidence.

## 8b. Continuity and Evidence

- **Which decisions are likely to be revisited later:** Primary ICP, supported
  export formats, rule taxonomy, pricing, Telegram delivery, when to productize
  beyond concierge, and whether live risk guard deserves a separate phase.
- **What prior evidence or proof will future agents need to find quickly:** Paid
  pilot evidence, real export samples, rule taxonomy decisions, report examples,
  customer objections, and kill/pivot thresholds.
- **Will work span multiple sessions / agents / weeks:** Yes.
- **Any existing docs, ADRs, audits, or notes that should become retrieval anchors:** `docs/CODEX_PROMPT.md`, `docs/tasks.md`,
  `docs/PROJECT_BRIEF.md`, `../../docs/PRODUCT_PORTFOLIO.md`,
  `../../docs/AI_DEVELOPMENT_OPERATING_MODEL.md`, and any future pilot reports.

## 9. Integrations

- **External APIs / services:** None required for v1. Telegram can be delivery
  surface manually or later via bot if validated.
- **Databases / storage:** Start with local files and deterministic artifacts.
  SQLite or DuckDB may be enough if productized; Postgres only if needed.
- **Auth / identity provider:** None for concierge/local v1. Do not build
  multi-user auth before validation.
- **Webhooks / messaging / queues:** None in v1. Telegram delivery is optional
  and should not become a platform dependency before demand is proven.

## 10. Constraints

- **Preferred stack:** Python, Pydantic, Polars or pandas, DuckDB/SQLite if
  useful, pytest, ruff, pyright, Markdown report generation. Reuse Entropy Core
  deterministic primitives only through explicit bridge contracts. Keep import,
  rule-evaluation, attribution, and report-generation boundaries stable so a
  high-load path can later move to Rust or Go without rewriting the product.
- **Deployment target:** Local/concierge workflow first; no public SaaS until
  payment and repeat-use gates pass.
- **Budget constraints:** High. Do not spend on infrastructure before paid pilot
  evidence.
- **Latency / throughput expectations:** Batch audits should complete within
  minutes for typical exports; human review will dominate early pilots. Set
  explicit thresholds before optimizing or changing language.
- **Compliance requirements:** Not investment advice, no live trading control,
  clear disclaimers, confidential data handling.
- **Network / security restrictions:** No broker credentials in v1. No live API
  keys. User data stays local unless explicit delivery/storage decision exists.

## 11. Runtime and Operations

- **Should runtime stay simple (managed service / container) if possible:** Yes.
  Local CLI/scripts plus generated reports are enough for first MVP.
- **Any need for shell, package, or toolchain mutation at runtime:** No.
- **Any need for privileged actions or long-lived isolated workers:** No.
- **Recovery / rollback expectations:** Re-run audit from same input export and
  rule file to reproduce identical output.
- **Language/runtime escalation expectation:** Start Python-first. Escalate only
  if profiling shows Python/Polars/DuckDB cannot meet a specific target. Rust is
  the likely path for parsers/rule kernels; Go only for long-running services or
  workers. Require ADR and rollback plan.

## 12. Model and Cost Expectations

- **Cost sensitivity:** high
- **Latency sensitivity:** medium
- **Expected request / task volume:** Low initially; 10 to 30 manual pilot audits
  before serious productization.
- **If AI is used, should the system prefer smaller / cheaper models by default:** Yes.
- **Any required capabilities:** Structured output for draft rule extraction,
  reasoning for internal review, long context for user rules. No runtime
  autonomous behavior.
- **Preview-model tolerance:** low for customer-facing text, none for rule truth.

## 13. Success Metrics

- **Business success metric:** 3 paid audit reports from 10 qualified prospects
  within 14 days, then at least 3 repeat audits within 30 days.
- **Quality metric:** Supported exports produce deterministic violation records
  with source-row traceability and passing regression tests.
- **Latency metric:** Typical report generation under 5 minutes after inputs are
  normalized; concierge review time tracked separately.
- **Cost metric:** No paid infrastructure dependency before repeat payment
  evidence.
- **Operational metric:** A new agent can run bootstrap, read the brief, and
  produce a phased plan without asking whether this is a bot, SaaS, or live
  broker tool.
