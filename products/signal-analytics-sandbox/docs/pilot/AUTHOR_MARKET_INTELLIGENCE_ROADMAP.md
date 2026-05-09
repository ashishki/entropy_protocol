# Author Market Intelligence Roadmap

Version: 0.1
Last updated: 2026-05-09
Status: planning baseline for Phase 11+

---

## Purpose

The product direction expands from "extract explicit trade signals from public
posts" to **Author Market Intelligence**: a local-first system that evaluates
how a public market author forms theses, names assets, frames risk, reacts to
news, and how the discussed ideas would have behaved against market data.

Phase 10 is not discarded. Its capture set, pseudo-labels, author profile,
lexicon draft, deterministic parser helpers, and review queue become the first
channel profile and the first evidence corpus. Future channels should add
channel-specific profiles and instruments instead of forcing every author into
one universal parser.

---

## Product Claim

For a public market-analysis channel, the system should answer:

- What assets, sectors, and narratives does the author discuss?
- Which posts contain explicit trade setups, softer directional ideas, or broad
  market regime commentary?
- What market context was available at the time?
- How did mentioned ideas behave over agreed horizons after publication?
- Where is the author useful: timing, risk framing, narrative filtering,
  watchlist generation, or general sentiment?
- Where is the author weak: late entries, unsupported conviction, unclear
  invalidation, noisy asset selection, or low follow-through?

The product must avoid claiming that an author gave investment advice unless
the reviewed evidence explicitly supports that interpretation.

---

## Architecture Direction

The desired architecture has four layers:

| Layer | Role | First implementation target |
|-------|------|-----------------------------|
| Source corpus | Normalize posts, images metadata, transcripts, and channel context into stable evidence documents. | `SourceDocument` schema over existing Telegram captures. |
| Channel profile | Store author/channel-specific vocabulary, extraction hints, risk-language patterns, and review rules. | Reuse `bablos79` Phase 10 profile as profile v0. |
| Retrieval context | Retrieve prior author statements, asset aliases, thesis history, and nearby market context for batch analysis. | Local RAG prototype after ADR approval. |
| Deterministic evaluation | Join extracted market ideas to OHLCV/fund/crypto data and compute horizon outcomes. | Local market-data store plus horizon metrics. |

The RAG layer should assist context assembly and analyst summaries only. It must
not produce final prices, returns, or outcome metrics.

---

## Reference Pattern From Dream Motif Interpreter

`https://github.com/ashishki/Dream_Motif_Interpreter` is a useful reference for
the next stage because it demonstrates a practical pattern for:

- normalized document ingestion before embedding;
- PostgreSQL/pgvector-style retrieval as an application substrate;
- a parser/profile layer before assistant response generation;
- voice/text intake as separate ingestion modalities;
- an assistant loop bounded by stored context rather than free-form browsing;
- feedback artifacts that can improve future classification.

This repository is a reference pattern, not a dependency. Phase 11 must decide
whether Signal Analytics Sandbox uses local files, DuckDB/LanceDB, or
PostgreSQL/pgvector for the first RAG store.

---

## Development Phases

### Phase 11 — Architecture Reset

Goal: turn the new product direction into explicit architecture, contracts, and
profile activation decisions before code expands.

Deliverables:

- ADR for Author Market Intelligence scope and RAG/runtime choice.
- Updated capability-profile status for RAG, Planning, and Agentic boundaries.
- `MarketIdea` schema specification for explicit trades, soft directional
  theses, market regime commentary, watchlist mentions, and news reactions.
- Metric contract defining which outcomes are deterministic and which outputs
  remain analyst summaries.

Exit criteria:

- Future code tasks can cite a schema and runtime decision.
- No RAG/vector/agent code is implemented before the ADR exists.

### Phase 12 — Asset Universe And Market Data Foundation

Goal: make assets and prices first-class enough to evaluate ideas across crypto,
funds, indices, equities, and macro proxies.

Deliverables:

- Asset alias registry with canonical IDs, source symbols, and instrument type.
- Market-data store contract with provider, timestamp, resolution, checksum,
  and licensing/provenance fields.
- Deterministic horizon metrics: immediate move, 1d/3d/7d/30d returns, max
  favorable excursion, max adverse excursion, volatility context, and benchmark
  comparison where data exists.

Exit criteria:

- A post that mentions BTC, ETH, SPY, QQQ, a fund, or an index can be linked to
  a canonical asset or explicitly marked unresolved.
- Outcome math remains independent from LLM/RAG output.

### Phase 13 — Universal Source Corpus

Goal: normalize public channel content into a corpus that can support text,
transcript, and image-derived evidence without changing downstream schemas.

Deliverables:

- `SourceDocument` schema for post text, evidence URL, capture ID, media
  references, voice transcript references, OCR references, author, timestamp,
  and hash fields.
- Migration/export path from current `CapturedPost` records into corpus docs.
- Channel profile registry so each channel can add vocabulary and parsing rules
  without global parser churn.

Exit criteria:

- Existing 60 `bablos79` captures can be exported into normalized corpus docs.
- Voice/OCR are represented as optional evidence references, not required v0
  dependencies.

### Phase 14 — Local RAG Context Layer

Goal: provide retrieval over source corpus, author profiles, asset aliases, and
prior extracted ideas.

Deliverables:

- Storage ADR implementation selected in Phase 11.
- Embedding/index metadata that records model/provider/version/checksum.
- Retrieval API that returns cited source document IDs and confidence metadata.
- Tests proving retrieval never mutates approved ledgers or deterministic
  outcome data.

Exit criteria:

- Batch analysis can request "prior author context for asset X/time window Y"
  and receive cited corpus snippets.
- Retrieval output is marked context-only.

### Phase 15 — Market Idea Extraction

Goal: extract richer market ideas from posts, not only strict trade signals.

Deliverables:

- `MarketIdea` draft extractor for explicit trade setup, directional bias,
  market regime, watchlist, catalyst/news reaction, risk warning, and
  non-market content.
- Evidence-span validator for assets, direction, horizon, entry/exit language,
  risk/invalidation, and confidence wording.
- Batch artifact similar to Phase 10 draft export, with queueing rules for
  ambiguous or customer-facing claims.

Exit criteria:

- Drafts are useful for review, but no market idea becomes approved without a
  human boundary or an explicitly documented confidence gate in a later phase.

### Phase 16 — Deterministic Thesis Evaluation

Goal: evaluate extracted market ideas against actual market data.

Deliverables:

- Join layer from `MarketIdea` drafts/approved records to asset data windows.
- Outcome evaluator for horizons and risk windows.
- Aggregate metrics: coverage, resolvability, directional hit rate by horizon,
  drawdown-before-upside, volatility-adjusted move, benchmark-relative move,
  and null/unclear idea rate.

Exit criteria:

- The product can show how discussed assets moved after author commentary, with
  all numbers tied to deterministic market data.

### Phase 17 — Bounded Batch Analyst

Goal: use an agent only as a bounded batch analyst that plans, retrieves, drafts
summaries, and stops with auditable artifacts.

Deliverables:

- Batch-job contract with max iterations, fixed tools, no shell mutation, no
  autonomous publication, and explicit stop reasons.
- Audit log of each retrieval/evaluation/summary step.
- Summary prompt that separates evidence, deterministic metrics, and analyst
  interpretation.

Exit criteria:

- A batch run can process a channel slice and produce an internal analyst memo
  without modifying approved ledgers or publishing reports.

### Phase 18 — Author Market Report V0

Goal: produce a report that combines author behavior, evidence, and market
outcome metrics.

Deliverables:

- Markdown report template for channel profile, asset coverage, thesis types,
  deterministic outcomes, evidence examples, limitations, and non-advice
  language.
- Customer-facing boundaries: no private scraping, no live trading, no broker
  integration, no public leaderboard, no claims beyond reviewed evidence.
- Decision gate on whether the report is sellable, needs more data, or should
  remain internal.

Exit criteria:

- A reviewer can inspect the report and trace every metric or claim back to
  source documents, approved/extraction artifacts, and price snapshots.

### Phase 19 — Modalities And Channel-Specific Tooling

Goal: add instruments per channel only where observed evidence proves a need.

Candidate tools:

- voice transcription for author voice notes;
- OCR/image annotation for screenshots of chart levels;
- custom channel lexicons;
- news/catalyst linker;
- fund/equity/crypto data adapters;
- reviewer UI/export improvements.

Exit criteria:

- Each new tool cites the channel/profile bottleneck it solves and ships behind
  a narrow task with acceptance tests.

---

## Non-Goals For The New Stage

- No private Telegram group scraping.
- No trading bot, copy trading, broker integration, or investment advice.
- No public leaderboard before reviewed customer demand.
- No LLM-derived prices, returns, or outcome truth.
- No autonomous publication.
- No nested Codex, `codex exec`, or external product substitution in the
  orchestration loop.

---

## Immediate Next Task

Run `SAS-MI-001: Author Market Intelligence Architecture ADR` from
`docs/tasks.md`.
