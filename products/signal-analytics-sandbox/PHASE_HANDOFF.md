# PHASE_HANDOFF

Use this file only at a phase boundary, context rollover, or limit recovery.

## Current State

- Phase: 19 complete and archived.
- Active task: none defined.
- Branch: `codex/signal-analytics-sandbox-work`.
- Last validation: `.venv/bin/python -m pytest tests/ -q` -> 141 tests passed on 2026-05-09; `ruff check src/ tests/` and `.venv/bin/pyright` also pass.
- Git status summary: Phase 17, Phase 18, Phase 19, and current closeout docs are pending commit.

## Completed In This Phase

- Verified product-local setup from `RUNBOOK.md`.
- Acknowledged Phase 0 gates from operator-provided pilot sources and created `docs/PILOT_LOG.md` / `docs/legal_risk_memo.md`.
- Ran Phase 1 validator and wrote `docs/audit/PHASE1_AUDIT.md` with PASS.
- Completed T01 Project Skeleton with package, CLI stubs, dependency manifests, shared observability module, and tests.
- Completed T02 CI Setup with workflow/dependency contract tests and a repository-root workflow bridge for the monorepo.
- Completed T03 Phase 1 Smoke Tests with tracer singleton, JSON logger, and status smoke coverage.
- Completed T04 SourceManifest Pydantic Schema with eligibility validation and canonical JSON persistence.
- Completed T05 Capture Loader with checksum validation, private-source rejection, and deterministic ordering.
- Completed T06 SignalRecord Schema with direction validation, evaluability semantics, and canonical dedup-key computation.
- Completed T07 Ledger I/O (Parquet) with deterministic Parquet writes, canonical columns, duplicate handling, and empty ledger round-trip behavior.
- Completed T08 Dedup + Ambiguity Flagging with deterministic pure functions.
- Phase 3 deep review completed and archived at `docs/archive/PHASE3_REVIEW.md`.
- Accepted ADR-001 and completed T09 PriceDataProvider Abstract Interface.
- Completed T10 OperatorFilePriceProvider with local Parquet input loading,
  schema validation, deterministic snapshots, typed errors, and adapter-call
  logging.
- Completed T11 PriceSnapshot Persistence + Provenance with deterministic
  `ohlcv.parquet` and `metadata.json` persistence, immutable existing
  `snapshot_id` handling, and checksum-verifying load.
- Phase 4 deep review completed and archived at `docs/archive/PHASE4_REVIEW.md`.
- Completed T12 Outcome Matching Engine with deterministic matching,
  `OutcomeRecord`, append-only rule registry, Decimal rounding, outcomes
  Parquet metadata, and `docs/audit/HEAVY_T12_EVIDENCE.md`.
- Completed T13 Aggregator with deterministic outcomes Parquet aggregation,
  historical summary fields, win-rate exclusion semantics, Decimal summary math,
  and max drawdown ordering.
- Completed T14 Markdown Report Generator with deterministic report rendering,
  canonical disclaimer validation, provenance, evidence rows, prototype snapshot
  gating, excluded-signal separation, and `docs/audit/HEAVY_T14_EVIDENCE.md`.
- Phase 5 deep review completed and archived at `docs/archive/PHASE5_REVIEW.md`.
- Completed T15 ExtractionAdapter ABC with result status invariants and
  model-level evidence preservation checks.
- Completed T16 ManualExtractionAdapter with injected editor command, prefilled
  JSON templates, draft parsing, and missing-field defer reasons.
- Completed T17 RuleExtractionAdapter with versioned rule templates,
  `binance_spot_v1`, match/defer behavior, and locked template hash validation.
- Phase 6 deep review completed and archived at `docs/archive/PHASE6_REVIEW.md`.
- Completed T18 ExchangePublicOHLCVProvider with injected ccxt-style client,
  deterministic cache, public_exchange snapshots, rate-limit-aware ccxt
  construction, and no-partial-persistence failure behavior.
- Completed T19 YFinanceDevProvider with prototype status and
  `SIGNAL_SANDBOX_ALLOW_YFINANCE=1` construction gate.
- Phase 7 deep review completed and archived at `docs/archive/PHASE7_REVIEW.md`.
- Completed T20 LLMExtractionAdapter with double activation gate,
  fixed-client CI coverage, LLM adapter IDs, paid-call cost-cap enforcement,
  ledger rejection for unreviewed LLM records, and eval acceptance-rate
  baseline.
- Heavy T20 evidence archived at `docs/audit/HEAVY_T20_EVIDENCE.md`.
- Phase 8 deep review completed and archived at `docs/archive/PHASE8_REVIEW.md`.
- Added validation coverage for `guard_phase_boundary.sh` so cross-phase `Next Task` advancement is blocked without archived review evidence.
- Updated `AGENT_NOTES.md` with investigation notes, decisions, risks, and minimal plan.
- Completed `SAS-PILOT-001: Pilot Scope`:
  - created `docs/pilot/PILOT_SCOPE.md`
  - selected `https://t.me/bablos79` first by deterministic `PILOT_LOG` order
  - set default 30-50 defensible signal record target where available
  - kept bot/SaaS/parser/private-source expansion out of scope
  - updated `docs/CODEX_PROMPT.md`, `docs/tasks.md`,
    `docs/IMPLEMENTATION_JOURNAL.md`, and `AGENT_NOTES.md`
- Completed `SAS-PILOT-002: Methodology V0`:
  - created `docs/pilot/METHODOLOGY_V0.md`
  - defined required capture fields, signal qualification rules, extraction
    statuses, ambiguity handling, deterministic outcome semantics, price
    provenance, and report guardrails
  - advanced `docs/CODEX_PROMPT.md` to `SAS-PILOT-003`
- Completed `SAS-PILOT-003: First Source Capture Plan And Log`:
  - created `docs/pilot/CAPTURE_LOG.md`
  - recorded public/operator-supplied-only capture method
  - added required evidence fields, capture statuses, and skip/block reasons
  - left current row as `pending-operator-input` because no real captures exist
  - advanced `docs/CODEX_PROMPT.md` to `SAS-PILOT-004`
- Completed `SAS-PILOT-004: First Source Manual Extraction Log`:
  - created `docs/pilot/EXTRACTION_LOG.md`
  - recorded required extraction fields and status counts
  - set `pending_capture=1` and all approved/ambiguous/excluded counts to 0
  - documented extraction blocker on operator-supplied public captures
  - advanced `docs/CODEX_PROMPT.md` to `SAS-PILOT-005`
- Completed `SAS-PILOT-005: First Source Report V0`:
  - created `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md`
  - recorded zero capture/extraction/approved/evaluable counts
  - documented missing approved ledger, price snapshot, and outcomes
  - preserved non-advice and historical-only language
  - advanced `docs/CODEX_PROMPT.md` to `SAS-PILOT-006`
- Completed `SAS-PILOT-006: Customer Feedback And Payment Signal Log`:
  - created `docs/pilot/CUSTOMER_FEEDBACK.md`
  - created `docs/pilot/PAYMENT_SIGNAL_LOG.md`
  - recorded pending rows because no customer review/payment behavior exists
  - added past-behavior questions, payment statuses, refusal reasons, and
    Telegram-delivery-as-format guardrails
  - advanced `docs/CODEX_PROMPT.md` to `SAS-PILOT-007`
- Completed `SAS-PILOT-007: Repeat Or Automate Decision`:
  - created `docs/pilot/PILOT_DECISION.md`
  - recorded D-014 in `docs/DECISION_LOG.md`
  - verdict: stop/defer automation until real public captures are supplied
  - no new engineering phase approved
- Phase 9 deep review completed:
  - wrote `docs/audit/META_ANALYSIS.md`
  - wrote `docs/audit/ARCH_REPORT.md`
  - wrote `docs/audit/REVIEW_REPORT.md`
  - archived `docs/archive/PHASE9_REVIEW.md`
  - updated `docs/audit/AUDIT_INDEX.md`
  - wrote `docs/audit/PHASE_REPORT_LATEST.md`
  - updated `README.md`, `docs/ARCHITECTURE.md`, and `docs/CODEX_PROMPT.md`
- Parsed public `bablos79` captures after operator instruction:
  - fetched unauthenticated `https://t.me/s/bablos79` pages only
  - created 60 capture JSON files in `workspace/captures/bablos79/`
  - wrote `docs/pilot/bablos79_CAPTURE_MANIFEST.json`
  - validated with `load_captures(Path("workspace"), "bablos79")` -> 60
  - updated capture/extraction logs and decision docs
- Created Phase 10 plan:
  - `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`
  - `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md`
  - `docs/tasks.md` Phase 10 `SAS-AUTO-001`, `SAS-AUTO-001B`, and
    `SAS-AUTO-002..005`
  - D-015, D-016, and D-017 in `docs/DECISION_LOG.md`
  - `docs/CODEX_PROMPT.md` next task set to `SAS-AUTO-001`
- Updated the orchestrator loop contract:
  - `docs/prompts/ORCHESTRATOR.md` now requires continuous phase advancement
    after deep review/archive/doc update/phase report.
  - D-018 records that phase review is a gate opener, not a stopping point.
- Completed Phase 10:
  - `SAS-AUTO-001..005` produced pseudo-labels, author profile, deterministic
    draft validation/parser/export helpers, review queue, and eval decision.
  - Phase 10 deep review archived at `docs/archive/PHASE10_REVIEW.md` with
    Stop-Ship No and P0/P1/P2 all 0.
- Planned Phase 11+ Author Market Intelligence stage:
  - created `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`
  - appended Phases 11-19 and tasks `SAS-MI-001..018` to `docs/tasks.md`
  - recorded D-019/D-020 in `docs/DECISION_LOG.md`
  - updated README, architecture, prompt, journal, memory, and notes for the
    new stage.
- Completed `SAS-MI-001: Author Market Intelligence Architecture ADR`:
  - created `docs/adr/ADR-002-author-market-intelligence.md`
  - updated `docs/ARCHITECTURE.md` capability profiles
  - recorded D-021 in `docs/DECISION_LOG.md`
  - RAG is ON for local cited context only
  - Agentic is ON for a bounded internal batch analyst only
  - Tool-Use and Planning remain OFF
  - runtime remains T0
  - first retrieval substrate is local DuckDB plus local vector/index sidecar
    files
- Completed `SAS-MI-002: MarketIdea Schema And Metrics Contract`:
  - created `docs/specs/MARKET_IDEA_SCHEMA.md`
  - defined required and optional fields, enum values, approval states,
    evidence-span rules, draft-only labels, deterministic horizons, metric
    outputs, review queue policy, examples, and SignalRecord compatibility
  - no product code, market-data fetch, embeddings, vector storage, approved
    ledger writes, or batch-agent code were added
- Phase 11 deep review completed and archived:
  - `docs/archive/PHASE11_REVIEW.md`
  - `docs/audit/AUDIT_INDEX.md` Cycle 11 row
  - Stop-Ship No; P0/P1/P2 all 0
- Completed `SAS-MI-003: Asset Universe And Alias Registry`:
  - created `src/signal_sandbox/assets/`
  - created `tests/unit/test_asset_registry.py`
  - created `docs/specs/ASSET_UNIVERSE.md`
  - resolution returns `exact`, `ambiguous`, or `unresolved` with evidence
  - seed assets cover BTC, ETH, SOL, SPY, QQQ, Phase 10 observed tickers, and
    unresolved fallback
  - no market data was fetched
- Completed `SAS-MI-004: Market Data Store Contract`:
  - created `src/signal_sandbox/market_data/`
  - created `tests/unit/test_market_data_store.py`
  - created `docs/specs/MARKET_DATA_STORE.md`
  - local snapshots preserve provider, canonical asset, provider symbol,
    timeframe, source range, captured_at, data_sha256, license, and provenance
  - identical rewrites are idempotent; different-byte overwrites are rejected
  - no paid/network market-data provider was added
- Completed `SAS-MI-005: Deterministic Horizon Metrics`:
  - created `src/signal_sandbox/market_data/metrics.py`
  - created `tests/unit/test_horizon_metrics.py`
  - computes 1d, 3d, 7d, and 30d returns plus MFE/MAE
  - returns explicit unresolved asset, non-directional, and insufficient-data
    statuses
  - no LLM, RAG, retrieval, or analyst-summary dependency was added
- Phase 12 deep review completed and archived:
  - `docs/archive/PHASE12_REVIEW.md`
  - `docs/audit/AUDIT_INDEX.md` Cycle 12 row
  - Stop-Ship No; P0/P1/P2 all 0
- Completed `SAS-MI-006: SourceDocument Corpus Schema`:
  - created `src/signal_sandbox/corpus/`
  - created `tests/unit/test_source_document.py`
  - created `docs/specs/SOURCE_CORPUS.md`
  - conversion from `CapturedPost` preserves evidence URL and text hash
  - optional media/transcript/OCR refs are evidence links only
  - no transcription/OCR provider, embeddings, vector store, or retrieval API
    was added
- Completed `SAS-MI-007: Channel Profile Registry`:
  - created `src/signal_sandbox/profiles/`
  - created `tests/unit/test_channel_profile.py`
  - created `docs/specs/CHANNEL_PROFILES.md`
  - preserved `bablos79` profile_state values from the Phase 10 lexicon
  - unknown channel lookup returns no profile instead of falling back
- Phase 13 deep review completed and archived:
  - `docs/archive/PHASE13_REVIEW.md`
  - `docs/audit/AUDIT_INDEX.md` Cycle 13 row
  - Stop-Ship No; P0/P1/P2 all 0
- Completed `SAS-MI-008: Local Retrieval Store Prototype`:
  - created `src/signal_sandbox/retrieval/`
  - created `tests/unit/test_retrieval_store.py`
  - added `duckdb` as the local retrieval metadata substrate
  - ingestion preserves stable `SourceDocument` IDs and citation metadata
  - deterministic vector sidecars and embedding/index metadata are recorded
  - repeated ingestion is idempotent
- Completed `SAS-MI-009` through `SAS-MI-015`:
  - cited retrieval API, MarketIdea extraction/export, outcome evaluator,
    author metrics, bounded batch analyst contract, and internal analyst memo
    export are complete
  - Phase 14, 15, 16, and 17 deep reviews are archived through
    `docs/archive/PHASE17_REVIEW.md`
  - current baseline is 135 passed, 0 skipped; ruff and pyright pass
- Completed `SAS-MI-016: Author Market Report Template`:
  - created `src/signal_sandbox/reports/author_market.py`
  - created `tests/unit/test_author_market_report.py`
  - created `docs/pilot/reports/bablos79_AUTHOR_MARKET_REPORT_V0.md`
  - renderer blocks missing source-document or market-snapshot provenance
  - explicit trade setup metrics are separated from broader commentary metrics
  - current baseline is 138 passed, 0 skipped; ruff and pyright pass
  - no approved ledger writer, market-data writer, metric writer, runtime LLM
    call, or network path was added
- Completed `SAS-MI-009: Cited Retrieval API`:
  - created `src/signal_sandbox/retrieval/query.py`
  - created `tests/unit/test_retrieval_query.py`
  - returns document_id, snippet, score, source timestamp, evidence URL, and
    text_sha256 for each result
  - deterministic channel/time filters are covered
  - uncited result models are rejected
  - no approved ledger writer, market-data writer, metric writer, report
    writer, runtime LLM call, network path, or agent loop was added
- Phase 14 deep review completed and archived:
  - `docs/archive/PHASE14_REVIEW.md`
  - `docs/audit/AUDIT_INDEX.md` Cycle 14 row
  - Stop-Ship No; P0/P1/P2 all 0
- Completed `SAS-MI-010: MarketIdea Draft Extractor`:
  - created `src/signal_sandbox/market_ideas/`
  - created `tests/unit/test_market_idea_extractor.py`
  - deterministic extractor classifies all required MarketIdea categories
  - direct evidence spans are preserved
  - drafts remain unapproved and review-pending
- Completed `SAS-MI-011: MarketIdea Batch Draft Export`:
  - created `src/signal_sandbox/market_ideas/export.py`
  - created `tests/unit/test_market_idea_export.py`
  - created `docs/pilot/MARKET_IDEA_DRAFTS_BABLOS79.md`
  - export contains one row per source document
  - draft approval state and final review status remain separate
  - no approved ledger, outcome, or report side effects were added
- Phase 15 deep review completed and archived:
  - `docs/archive/PHASE15_REVIEW.md`
  - `docs/audit/AUDIT_INDEX.md` Cycle 15 row
  - Stop-Ship No; P0/P1/P2 all 0
- Completed `SAS-MI-012: MarketIdea Outcome Evaluator`:
  - created `src/signal_sandbox/market_ideas/outcomes.py`
  - created `tests/unit/test_market_idea_outcomes.py`
  - resolves assets through the asset registry without guessing
  - computes horizon metrics through deterministic market-data metrics
  - records source document ID, market idea ID, asset ID, snapshot ID, and
    metric version
- Completed `SAS-MI-013: Author Metrics Aggregator`:
  - created `src/signal_sandbox/market_ideas/author_metrics.py`
  - created `tests/unit/test_author_metrics.py`
  - aggregates counts by idea type, asset type, horizon status, and review
    status
  - computes directional hit rate only for evaluable directional outcomes
  - reports null/non-market content separately
- Phase 16 deep review completed and archived:
  - `docs/archive/PHASE16_REVIEW.md`
  - `docs/audit/AUDIT_INDEX.md` Cycle 16 row
  - Stop-Ship No; P0/P1/P2 all 0
- Completed `SAS-MI-014: Batch Analyst Contract`:
  - created `src/signal_sandbox/batch_analyst/`
  - created `tests/unit/test_batch_analyst_contract.py`
  - created `docs/specs/BATCH_ANALYST.md`
  - contract declares scope, fixed allowed operations, max iterations,
    retrieval cap, cost cap, and stop reasons
  - audit log records retrieval, metric read, prompt input, and memo checksums
  - no shell/network/broker/report publisher surface was added

## Recent Phase 18 Closeout

- Completed `SAS-MI-016: Author Market Report Template`:
  - created `src/signal_sandbox/reports/author_market.py`
  - created `tests/unit/test_author_market_report.py`
  - created `docs/pilot/reports/bablos79_AUTHOR_MARKET_REPORT_V0.md`
  - renderer includes canonical non-advice disclaimer, provenance gates, and
    separated trade setup / commentary metrics
- Completed `SAS-MI-017: Sellability And Scope Decision Gate`:
  - created `docs/pilot/AUTHOR_MARKET_REPORT_DECISION.md`
  - verdict: iterate internally, do not sell V0 yet
  - exact bottleneck: reviewed evidence coverage across the 60 public
    `bablos79` captures, cited MarketIdea rows, deterministic outcome metrics,
    and customer/payment evidence
  - Phase 18 deep review archived at `docs/archive/PHASE18_REVIEW.md`
  - next task is `SAS-MI-018: Modality And Tooling Scope ADR`
- Completed `SAS-MI-018: Modality And Tooling Scope ADR`:
  - created `docs/adr/ADR-003-channel-specific-tools.md`
  - compared voice transcription, OCR/image annotation, news/catalyst linking,
    fund/equity data, reviewer UI/export improvements, and new lexicons
  - selected deterministic reviewer/export improvements
  - added `SAS-MI-019: Reviewer Coverage Export Pack` to `docs/tasks.md`
  - added no provider dependency or external service
- Completed `SAS-MI-019: Reviewer Coverage Export Pack`:
  - created `src/signal_sandbox/market_ideas/review_coverage.py`
  - created `tests/unit/test_review_coverage_export.py`
  - created `docs/pilot/bablos79_REVIEW_COVERAGE_PACK.md`
  - rows are deterministic and separate evidence, metric, interpretation, and
    customer-sample readiness buckets
  - Phase 19 deep review archived at `docs/archive/PHASE19_REVIEW.md`

## Remaining Work

- No implementation task is currently defined in `docs/tasks.md`.
- Human exception review of `docs/pilot/bablos79_REVIEW_QUEUE.md` remains a
  useful parallel product action, but it no longer blocks planning the broader
  architecture.

## Blockers Or Human Decisions

- Human review is required before any approved ledger rows, customer-facing
  claims, or final report interpretation.
- Phase 19 selected deterministic reviewer/export improvements. Do not add
  modality providers, external services, private scraping, broker paths, public
  leaderboard expansion, marketplace expansion, or forward-looking claims.
- Operator/product direction is required before adding another phase.

## Resume Instruction

Continue this product from `RUNBOOK.md`, `AGENT_NOTES.md`, this
`PHASE_HANDOFF.md`, `docs/CODEX_PROMPT.md`, and `docs/tasks.md`.
Do not spawn nested Codex. Stop until the operator adds or approves the next
task/phase. Do not write approved ledger records from draft/parser output
without human review. Do not add modality providers or external services
without a new scoped task and, where needed, an ADR.
