# Signal Analytics Sandbox Project Brief

Use this brief before running `prompts/STRATEGIST.md` or a product-local
bootstrap session inside `products/signal-analytics-sandbox/`.

---

## 1. Project

- **Project name:** Signal Analytics Sandbox
- **One-sentence summary:** Separate validation sandbox for public Telegram/X
  signal-source ledgers and historical outcome reports.
- **Why this project exists:** Traders often see public signal claims,
  screenshots, Telegram posts, and influencer performance narratives without a
  trustworthy independent ledger. This may be a strong wedge, but it is legally
  and technically messy and must not contaminate Entropy Core.
- **What success looks like in v1:** Given a public signal source and a defined
  historical window, the system produces a transparent, caveated signal ledger
  and report that a paying user finds useful enough to repeat or refer.

## 2. Users and Workflows

- **Primary users / operators:** Signal-channel subscribers, traders evaluating
  public signal sources, market researchers, and possibly small teams doing
  source due diligence.
- **Main workflow 1:** Operator identifies a public signal source and captures
  a bounded historical sample with timestamps and source links/screenshots when
  legally permitted.
- **Main workflow 2:** Signals are normalized into a ledger: asset, direction,
  entry, stop/target if present, timestamp, source reference, confidence flags,
  and extraction status.
- **Main workflow 3:** System produces a report with outcome counts,
  limitations, ambiguous cases, drawdown/equity-style summaries where defensible,
  and clear non-advice disclaimers.

## 3. Scope

- **In scope for v1:** Public-source-only manual/assisted signal collection,
  signal record schema, deterministic ledger, outcome matching against
  historical prices, uncertainty flags, report generation, legal/terms risk
  memo, and validation of willingness to pay.
- **Out of scope / non-goals:** Private Telegram group scraping, scraping behind
  access controls, paid X API dependence before validation, signal marketplace,
  investment advice, influencer ranking marketplace, Entropy Core evidence,
  live trading, auto-copy trading, broker/exchange integration, and claims that
  the report predicts future performance.

## 4. AI Scope

- **Where AI may be needed:** Assisting extraction of messy public posts into
  draft signal records, classifying ambiguous text, summarizing limitations,
  and drafting report explanations for human review.
- **Where AI is explicitly not wanted:** Final signal truth without human
  review, outcome calculations, trading recommendations, investment advice,
  private-source access, or live trading actions.
- **Possible retrieval / RAG need:** Text-only retrieval over collected public
  posts, source references, ledger decisions, extraction rules, and report
  caveats.
- **If retrieval is needed, is text-only likely sufficient or is multimodal evidence truly required:** Text-only/manual evidence is preferred for v1. Multimodal should be deferred unless public screenshots are unavoidable and paid demand is already proven.
- **If multimodal may be needed, which modalities and why:** OCR or image
  understanding for public chart screenshots may be useful later, but it
  increases error, cost, and review burden.
- **Possible tool-use need:** Public page/file ingestion, local filesystem,
  CSV/JSON ledger processing, historical price lookup from approved data source,
  report generation.
- **Possible planning / agentic behavior need:** No autonomous scraping agent in
  v1. AI may assist extraction inside a human-reviewed workflow.

## 5. Deterministic Candidates

- **Validation / policy checks:** Source eligibility, public-only status, terms
  risk flags, required signal fields, ambiguity status, duplicate detection.
- **Routing / decision rules:** Exclude ambiguous/private/incomplete signals,
  route partial records to human review, mark no-result cases separately.
- **Calculations / transformations:** Outcome matching, return calculation,
  max adverse/favorable excursion, drawdown/equity-style ledger summaries,
  source coverage stats.
- **Retries / idempotency / audit triggers:** Re-running the same ledger and
  historical data should produce identical outcomes and report artifacts.

## 6. Human Approval Boundaries

- **What actions must require human approval:** Source eligibility, legal/terms
  judgment, ambiguous signal interpretation, final report release, public claims,
  and any use of screenshots/OCR/multimodal extraction.
- **What can be automated safely:** Deterministic ledger validation, historical
  price matching, report table generation, reproducibility checks, duplicate
  detection.
- **Why these boundaries matter:** The product is exposed to reputational,
  legal, and data-rights risk. Incorrect extraction or overclaiming can make the
  product look like defamation, investment advice, or unauthorized scraping.

## 7. Risk and Error Cost

- **What is expensive if the system is wrong:** Misrepresenting a signal
  source, wrong outcome stats, missing ambiguous cases, or producing advice-like
  claims.
- **What is expensive if the system is slow:** Manual extraction may not scale,
  and the wedge may be unprofitable if reports take too long.
- **What is expensive if the system is inconsistent / variable:** Users will not
  trust repeated reports, and signal sellers/subscribers may dispute results.
- **Blast radius if it fails badly:** Medium. No live capital is touched, but
  legal/reputational risk can be high.
- **Audit / explainability needs:** Very high. Each signal result must link to
  source evidence, extraction notes, price data, outcome rule, and ambiguity
  status.

## 8. Data

- **Primary data sources:** Public Telegram posts/channels, public X/Twitter
  posts, public web pages, manually captured public screenshots where permitted,
  historical OHLCV/price data.
- **Approximate data volume:** Small in v1; dozens to hundreds of signals per
  report.
- **Does data change frequently:** Public posts can be edited/deleted; capture
  timestamp and evidence snapshot policy matter.
- **Sensitive / regulated data present:** Avoid private user data. Do not ingest
  private groups, paywalled material, or personal account data.
- **Retention / deletion expectations:** Store only evidence required for the
  report, with explicit source references and deletion policy. Avoid hoarding
  scraped content.

## 8b. Continuity and Evidence

- **Which decisions are likely to be revisited later:** Whether this becomes a
  product or stays a sandbox, whether to use Telegram bot delivery, whether to
  support X, whether multimodal extraction is justified, and whether the legal
  risk is acceptable.
- **What prior evidence or proof will future agents need to find quickly:** Paid
  report evidence, source eligibility memos, extraction rule decisions, sample
  ledgers, disputed cases, and kill/pivot thresholds.
- **Will work span multiple sessions / agents / weeks:** Yes.
- **Any existing docs, ADRs, audits, or notes that should become retrieval anchors:** `docs/CODEX_PROMPT.md`, `docs/tasks.md`,
  `docs/PROJECT_BRIEF.md`, `../../docs/PRODUCT_PORTFOLIO.md`,
  `../../docs/AI_DEVELOPMENT_OPERATING_MODEL.md`, and future legal/risk memos.

## 9. Integrations

- **External APIs / services:** None required for v1. Avoid paid X API
  dependency before validation. Public-source capture can be manual initially.
- **Databases / storage:** Start with local JSON/CSV/Parquet ledgers and
  Markdown reports. SQLite/DuckDB only if useful.
- **Auth / identity provider:** None for sandbox v1.
- **Webhooks / messaging / queues:** None in v1. Telegram delivery may be tested
  manually if users insist on Telegram-first UX.

## 10. Constraints

- **Preferred stack:** Python, Pydantic, Polars/pandas, local files, Markdown
  report generation, pytest, ruff, pyright. Optional OCR/multimodal only after
  explicit gate. Keep source capture, extraction, ledger normalization, outcome
  matching, and report generation behind stable contracts so later scale work
  can replace one component without rewriting the sandbox.
- **Deployment target:** Local/manual sandbox first, not public SaaS.
- **Budget constraints:** High. Do not pay for scraping/API infrastructure
  before paid demand is proven.
- **Latency / throughput expectations:** Batch report generation; extraction
  time is likely the bottleneck. Set explicit throughput targets before
  introducing another runtime or paid API dependency.
- **Compliance requirements:** Public-source-only, non-advice disclaimers,
  terms-of-service review, no private-source scraping.
- **Network / security restrictions:** No credentials for private groups, no
  bypassing access controls, no scraping behind login/paywall in v1.

## 11. Runtime and Operations

- **Should runtime stay simple (managed service / container) if possible:** Yes.
  Local scripts and reports are enough for first validation.
- **Any need for shell, package, or toolchain mutation at runtime:** No.
- **Any need for privileged actions or long-lived isolated workers:** No.
- **Recovery / rollback expectations:** Re-run from the same source ledger and
  historical price data to reproduce the report.
- **Language/runtime escalation expectation:** Start Python-first. Rust is only
  justified for proven parsing/OCR-adjacent or matching hot paths; Go is only
  justified for a future long-running collector service after legal and demand
  gates. Require benchmark, ADR, CI/toolchain plan, rollback plan, and approval.

## 12. Model and Cost Expectations

- **Cost sensitivity:** high
- **Latency sensitivity:** low to medium
- **Expected request / task volume:** Low initially; manual pilot reports.
- **If AI is used, should the system prefer smaller / cheaper models by default:** Yes for extraction drafts and summaries.
- **Any required capabilities:** Structured output, reasoning over ambiguous
  text, maybe OCR/multimodal later. No autonomous browsing/scraping in v1.
- **Preview-model tolerance:** low for extraction drafts, none for final stats.

## 13. Success Metrics

- **Business success metric:** At least 3 paid or strongly committed pilot
  reports from reachable signal subscribers/research users before building
  automated scraping or public SaaS.
- **Quality metric:** Each reported signal has source evidence, extraction
  status, deterministic outcome rule, and ambiguity flag.
- **Latency metric:** Manual pilot report can be produced within a bounded
  operator time budget; exact threshold set after first 3 pilots.
- **Cost metric:** No paid API dependency before repeated paid demand.
- **Operational metric:** Sandbox remains separate from Entropy Core evidence
  and does not introduce private-source scraping or investment-advice claims.
