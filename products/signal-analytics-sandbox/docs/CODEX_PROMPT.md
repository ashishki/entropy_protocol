# CODEX_PROMPT.md — Signal Analytics Sandbox

Version: 2.57
Date: 2026-05-09
Phase: 20

---

## Phase 0 Gate Status

Engineering Phase 1 (T01+) may begin because both rows below are marked `acknowledged` by the operator.

| Gate | Status | Evidence | Acknowledged date |
|------|--------|----------|-------------------|
| SAS-001: Paid Pilot Demand Validation | acknowledged | `docs/PILOT_LOG.md` | 2026-05-07 |
| SAS-002: Public-Source Legal/Terms Memo | acknowledged | `docs/legal_risk_memo.md` | 2026-05-07 |

The operator acknowledged the initial pilot scope on 2026-05-07:
`https://t.me/bablos79`, `https://t.me/nemphiscrypts`, and
`https://t.me/pifagortrade`. Twitter / X and Discord are deferred until the
Telegram pilot validates the product hypothesis.

---

## Current State

- **Phase:** 20 (Telegram Media Evidence: Voice And Image/OCR Drafts)
- **Baseline:** 141 passing tests, 0 skipped
- **Ruff:** `ruff check src/ tests/` passes
- **Pyright:** `pyright` passes
- **Last CI run:** local CI-equivalent commands pass; GitHub run not yet observed
- **Last updated:** 2026-05-09
- **Session tokens (approx):** not yet tracked
- **Cumulative phase tokens (approx):** not yet tracked

---

## Continuity Pointers

- **Decision log:** `docs/DECISION_LOG.md`
- **Implementation journal:** `docs/IMPLEMENTATION_JOURNAL.md`
- **Evidence index:** deferred in v1 — heavy-task evidence lives in `docs/audit/HEAVY_T{NN}_EVIDENCE.md`
- **Project brief:** `templates/PROJECT_BRIEF.md` (canonical), `docs/PROJECT_BRIEF.md` (pointer)
- **Architecture:** `docs/ARCHITECTURE.md`
- **Spec:** `docs/spec.md`
- **Tasks:** `docs/tasks.md`
- **Implementation contract:** `docs/IMPLEMENTATION_CONTRACT.md`
- **Task-scoped context:** read `Context-Refs` in `docs/tasks.md` before broad searching
- **Legal/risk memo (SAS-002 output):** `docs/legal_risk_memo.md` (created by SAS-002)
- **Pilot log (SAS-001 output):** `docs/PILOT_LOG.md` (created by SAS-001)
- **Pilot development loop:** `docs/PILOT_DEVELOPMENT_LOOP_RU.md`
- **Audit-grade automation roadmap:** `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md`
- **Author Market Intelligence roadmap:** `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`
- **Media modality development plan:** `docs/pilot/MEDIA_MODALITY_DEVELOPMENT_PLAN.md`
- **Orchestrator loop contract:** `docs/prompts/ORCHESTRATOR.md#phase-continuation-contract`

---

## Next Task

`SAS-MEDIA-001: Media Scope ADR And Legal Addendum`

The operator identified channel media as the next bottleneck: `bablos79` has
images/screenshots and voice/audio that the current text-only path does not
analyze. Phase 20 has been added to `docs/tasks.md`.

Immediate instruction:
- Implement `SAS-MEDIA-001` from `docs/tasks.md`.
- Create `docs/adr/ADR-004-media-evidence-pipeline.md`.
- Update `docs/legal_risk_memo.md` with explicit voice/audio/image/OCR media
  posture, allowed public/operator-forwarded capture, forbidden private or
  authenticated sources, raw-media retention, and deletion triggers.
- Reference the Dream_Motif_Interpreter voice pattern for Telegram
  `voice.file_id` download, media event/status, Whisper transcription boundary,
  and cleanup; do not copy its domain model or assistant behavior.
- Keep transcript/OCR output as draft evidence only, review-required, and
  forbidden from writing approved ledger rows or customer-facing claims.

Closeout digest for the Orchestrator:
- Phase 20 planning added `docs/pilot/MEDIA_MODALITY_DEVELOPMENT_PLAN.md` and
  tasks `SAS-MEDIA-001..008` to `docs/tasks.md`. The phase is scoped to
  Telegram media evidence: media legal/ADR gate, MediaArtifact schema, Telegram
  voice acquisition, gated Whisper transcript drafts, image/OCR inventory, OCR
  draft adapter, multimodal SourceDocument join, and multimodal coverage/decision
  gate. Dream_Motif_Interpreter is the implementation reference for Telegram
  voice mechanics (`docs/VOICE_PIPELINE.md`, `app/telegram/voice.py`,
  `app/telegram/handlers.py`, `app/workers/transcribe.py`), adapted to this
  product's public-source and draft-evidence boundaries. No media provider code
  has been implemented yet.
- SAS-MI-019 added `src/signal_sandbox/market_ideas/review_coverage.py`,
  `tests/unit/test_review_coverage_export.py`, and
  `docs/pilot/bablos79_REVIEW_COVERAGE_PACK.md`. The exporter emits one
  deterministic row per `SourceDocument`, sorted by timestamp/document/capture
  ID, with MarketIdea review status, evidence refs, deterministic outcome
  status, missing fields, reviewer action, and reviewer ID. Status buckets are
  `needs_evidence_review`, `needs_metric_snapshot`,
  `needs_interpretation_review`, and `ready_for_customer_sample`. The pilot
  artifact records 60 public captures as internal review support with no
  customer-facing claims. Validation after task: 141 tests pass, ruff passes,
  and pyright passes. Phase 19 deep review archived at
  `docs/archive/PHASE19_REVIEW.md`; Cycle 19 Stop-Ship: No; P0: 0, P1: 0,
  P2: 0.
- SAS-MI-018 added `docs/adr/ADR-003-channel-specific-tools.md` and appended
  `SAS-MI-019: Reviewer Coverage Export Pack` to `docs/tasks.md`. ADR-003
  compares voice transcription, OCR/image annotation, news/catalyst linking,
  fund/equity data, reviewer UI/export improvements, and new channel lexicons
  against the measured bottleneck. It chooses reviewer/export improvements as a
  deterministic local task and adds no provider dependency or external service.
  Validation after task: 138 tests pass, ruff passes, and pyright passes.
  Review skipped as doc-only.
- SAS-MI-017 added `docs/pilot/AUTHOR_MARKET_REPORT_DECISION.md`. Verdict:
  iterate internally, do not sell V0 yet. The decision cites report quality,
  thin evidence coverage, pending customer feedback, no payment signal,
  controlled implementation risk, and the exact next bottleneck: reviewed
  evidence coverage across the 60 public `bablos79` captures. It approves only
  the Phase 19 scoping ADR and keeps private scraping, live trading, broker
  integration, public leaderboard expansion, marketplace expansion, and
  forward-looking claims forbidden. Validation after task: 138 tests pass,
  ruff passes, and pyright passes. Phase 18 deep review archived at
  `docs/archive/PHASE18_REVIEW.md`; Cycle 18 Stop-Ship: No; P0: 0, P1: 0,
  P2: 0.
- SAS-MI-016 added `src/signal_sandbox/reports/author_market.py`,
  `tests/unit/test_author_market_report.py`, and
  `docs/pilot/reports/bablos79_AUTHOR_MARKET_REPORT_V0.md`. The renderer
  includes channel overview, data coverage, idea taxonomy, deterministic
  outcomes, evidence examples, limitations, and the canonical non-advice
  disclaimer; refuses missing source-document or market-snapshot provenance;
  and separates explicit trade setup metrics from broader commentary behavior.
  Validation after task: 138 tests pass, ruff passes, and pyright passes.
  Light review passed.
- SAS-MI-015 added `src/signal_sandbox/batch_analyst/memo.py`,
  `tests/unit/test_analyst_memo_export.py`,
  `docs/pilot/BABLOS79_INTERNAL_MARKET_MEMO.md`, and
  `docs/audit/AGENTIC_EVAL.md`. The memo model separates scope, corpus
  coverage, retrieved evidence, deterministic metrics, interpretation,
  limitations, and review queue; validates every interpretive claim against
  retrieved document IDs or deterministic metric IDs; and rejects
  `internal_only=false`. Validation after task: 135 tests pass, ruff passes,
  and pyright passes. Phase 17 deep review found no P0/P1/P2 issues.
- SAS-MI-014 added `src/signal_sandbox/batch_analyst/`,
  `tests/unit/test_batch_analyst_contract.py`, and
  `docs/specs/BATCH_ANALYST.md`. The contract declares channel/time scope,
  allowed operations, max iterations, max retrieved documents, cost cap, and
  stop reasons. The deterministic runner stops on max iterations, missing data,
  cost cap, or completed memo and records retrieval, metric-read, prompt input,
  and memo checksums. No shell/network/broker/report publisher surface was
  added.
- Phase 16 deep review archived at `docs/archive/PHASE16_REVIEW.md`; Cycle 16
  Stop-Ship: No; P0: 0, P1: 0, P2: 0.
- SAS-MI-013 added `src/signal_sandbox/market_ideas/author_metrics.py` and
  `tests/unit/test_author_metrics.py`. The aggregator computes counts by idea
  type, asset type, horizon status, and review status; computes directional hit
  rate only for evaluable directional outcomes; and reports null/non-market
  rate separately from failed ideas.
- SAS-MI-012 added `src/signal_sandbox/market_ideas/outcomes.py` and
  `tests/unit/test_market_idea_outcomes.py`. The evaluator resolves candidate
  assets through the asset registry without guessing, preserves unresolved and
  ambiguous statuses, computes horizon outcomes via deterministic
  `SAS-MI-005` metrics when a matching snapshot exists, and records source
  document ID, market idea ID, asset ID, snapshot ID, and metric version.
- Phase 15 deep review archived at `docs/archive/PHASE15_REVIEW.md`; Cycle 15
  Stop-Ship: No; P0: 0, P1: 0, P2: 0.
- SAS-MI-011 added `src/signal_sandbox/market_ideas/export.py`,
  `tests/unit/test_market_idea_export.py`, and
  `docs/pilot/MARKET_IDEA_DRAFTS_BABLOS79.md`. The batch export creates one
  row per source document, separates draft approval state from final review
  status, records review queue reasons/evidence refs/candidate assets/horizons,
  and writes only a draft Markdown artifact. No approved ledger, outcome, or
  report side effects were added.
- SAS-MI-010 added `src/signal_sandbox/market_ideas/` and
  `tests/unit/test_market_idea_extractor.py`. The deterministic extractor
  classifies source documents into all MarketIdea categories, preserves direct
  evidence spans for assets, direction, horizon/targets, risk/invalidation, and
  catalysts when present, and always emits review-pending unapproved drafts. No
  ledger writer, market-data writer, metric writer, report writer, runtime LLM
  call, network path, or agent loop was added.
- Phase 14 deep review archived at `docs/archive/PHASE14_REVIEW.md`; Cycle 14
  Stop-Ship: No; P0: 0, P1: 0, P2: 0.
- SAS-MI-009 added `src/signal_sandbox/retrieval/query.py` and
  `tests/unit/test_retrieval_query.py`. The query API returns cited snippets
  with document_id, score, source timestamp, evidence URL, and text_sha256, and
  supports deterministic channel/time filtering. Result models reject uncited
  rows. No approved ledger, market-data, metric, report, network, LLM, or agent
  mutation path was added.
- SAS-MI-008 added `src/signal_sandbox/retrieval/` and
  `tests/unit/test_retrieval_store.py`. The local retrieval store ingests
  `SourceDocument` records into a DuckDB metadata catalog with deterministic
  vector sidecars, preserves stable document IDs/citations, records
  embedding/index metadata including deterministic fixture ID, and repeated
  ingestion is idempotent. No approved ledger or deterministic metric writer is
  imported or mutated.
- Phase 13 deep review archived at `docs/archive/PHASE13_REVIEW.md`; Cycle 13
  Stop-Ship: No; P0: 0, P1: 0, P2: 0.
- SAS-MI-007 added `src/signal_sandbox/profiles/`,
  `tests/unit/test_channel_profile.py`, and
  `docs/specs/CHANNEL_PROFILES.md`. The registry stores versioned channel
  profiles with source URLs, accepted draft terms, needs-review terms, excluded
  terms, modality flags, and review rules. `bablos79` imports the Phase 10
  lexicon with profile_state preserved, and unknown channels return no profile.
- SAS-MI-006 added `src/signal_sandbox/corpus/`,
  `tests/unit/test_source_document.py`, and `docs/specs/SOURCE_CORPUS.md`.
  `SourceDocument` preserves capture/source/author/timestamp/text/evidence/hash
  fields and optional media/transcript/OCR evidence links. Existing
  `CapturedPost` records convert without evidence URL or hash drift. No
  transcription/OCR provider, embeddings, vector store, or retrieval API was
  added.
- Phase 12 deep review archived at `docs/archive/PHASE12_REVIEW.md`; Cycle 12
  Stop-Ship: No; P0: 0, P1: 0, P2: 0.
- SAS-MI-005 added `src/signal_sandbox/market_data/metrics.py` and
  `tests/unit/test_horizon_metrics.py`. It computes deterministic 1d, 3d, 7d,
  and 30d returns plus MFE/MAE, and returns explicit statuses for unresolved
  asset, non-directional, and insufficient-data cases. No LLM/RAG/retrieval
  dependency was added.
- SAS-MI-004 added `src/signal_sandbox/market_data/`,
  `tests/unit/test_market_data_store.py`, and
  `docs/specs/MARKET_DATA_STORE.md`. The store supports immutable local
  `operator_file` snapshots, checksum verification, metadata listing, and
  overwrite rejection. No paid/network market-data provider was added.
- SAS-MI-003 added `src/signal_sandbox/assets/`, `tests/unit/test_asset_registry.py`,
  and `docs/specs/ASSET_UNIVERSE.md`. Alias resolution is exact-only and
  returns `exact`, `ambiguous`, or `unresolved` with evidence. Seed coverage
  includes BTC, ETH, SOL, SPY, QQQ, Phase 10 observed tickers, and an unresolved
  fallback. No market data was fetched.
- Phase 11 deep review archived at `docs/archive/PHASE11_REVIEW.md`; Cycle 11
  Stop-Ship: No; P0: 0, P1: 0, P2: 0.
- SAS-MI-002 created `docs/specs/MARKET_IDEA_SCHEMA.md`. The spec defines
  required/optional fields, enum values, approval states, evidence-span rules,
  deterministic horizons, metric outputs, draft-only fields, and review queue
  policy. No product code was added.
- SAS-MI-001 created `docs/adr/ADR-002-author-market-intelligence.md`, updated
  `docs/ARCHITECTURE.md`, and recorded D-021. ADR-002 activates RAG and
  bounded Agentic profiles, keeps Tool-Use and Planning OFF, keeps runtime T0,
  and selects local DuckDB plus local vector/index sidecar files as the first
  retrieval substrate. No vector storage, embeddings, market-data expansion,
  or batch-agent code was implemented.
- Phase 11+ planning created
  `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`, appended Phases 11-19
  and tasks `SAS-MI-001..018` to `docs/tasks.md`, updated the README and
  architecture pointers, and recorded D-019/D-020.
- ADR-002 is the architecture gate result: RAG and bounded Agentic profiles are
  ON, Tool-Use and Planning remain OFF, and implementation remains deferred to
  scoped future tasks.
- Phase 10 deep review archived at `docs/archive/PHASE10_REVIEW.md`; Cycle 10
  Stop-Ship: No; P0: 0, P1: 0, P2: 0.
- SAS-AUTO-005 created `docs/pilot/AUTO_EXTRACTION_EVAL.md` and updated
  `docs/pilot/PILOT_DECISION.md`. Verdict: keep the draft helper for internal
  exception review only; no scope expansion. The exact remaining bottleneck is
  human review of 23 queued rows plus sampled verification of 37 non-queued
  rows. Review skipped as doc-only.
- SAS-AUTO-004 updated `docs/pilot/EXTRACTION_LOG.md` with draft suggested
  status counts and one draft suggestion row per capture while preserving final
  extraction status as `pending_manual_extraction`.
- SAS-AUTO-004 created `docs/pilot/bablos79_REVIEW_QUEUE.md` with 23 queue rows:
  all exception/low-confidence/customer-facing candidate rows plus a deterministic
  non-signal quality-control sample. Reviewer IDs remain `pending`; approved
  ledger rows created: 0. Review skipped as doc-only.
- SAS-AUTO-003 implemented `src/signal_sandbox/extraction/draft_export.py`,
  `tests/unit/test_draft_export.py`, and
  `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`. The export has one row per
  captured post, sorted by source timestamp and capture_id, with
  reviewer_id=`pending` on every row. Suggested status distribution:
  43 `not_a_signal`, 16 `insufficient_fields`, 1 `needs_review`.
- SAS-AUTO-003 validation: 93 tests pass, `ruff check src/ tests/` passes, and
  `.venv/bin/pyright` passes. No ledger files were created. Light review passed
  with no issues.
- SAS-AUTO-002 implemented `src/signal_sandbox/extraction/draft_validation.py`
  and `src/signal_sandbox/extraction/draft_parser.py` with focused unit tests.
  `validate_pseudo_label()` rejects unsupported spans/candidate fields, and
  `parse_draft()` preserves capture_id, evidence_url, and text_sha256 while
  returning review-only statuses. Complete candidates use `review_candidate`
  with `review_required=True`; no `approved` status is produced.
- SAS-AUTO-002 validation: 90 tests pass, `ruff check src/ tests/` passes, and
  `.venv/bin/pyright` passes. Light review passed with no issues.
- SAS-AUTO-001B generated `docs/pilot/bablos79_AUTHOR_PROFILE.md` and
  `workspace/lexicons/bablos79_lexicon_draft.json` with 32 candidate terms:
  17 `accepted_for_draft`, 9 `needs_review`, and 6 `excluded`.
- SAS-AUTO-001B validation confirmed every lexicon candidate includes term,
  category, evidence_capture_ids, evidence_excerpts, false_positive_risk,
  confidence, and profile_state. No parser code, runtime LLM calls, CLI export,
  ledger writes, or approved extraction truth were introduced.
- SAS-AUTO-001 generated `docs/pilot/bablos79_PSEUDO_LABELS.md` and
  `workspace/extraction/bablos79_pseudo_labels.jsonl` with 60 draft-only rows:
  50 `not_a_signal`, 7 `insufficient_fields`, and 3 `needs_review`.
- SAS-AUTO-001 validation confirmed the JSONL row count matches the 60 local
  captures, required fields are present, all rows are `draft_only=true` /
  `approval_state="unapproved"`, and all evidence-span text appears in the raw
  capture text.
- T20 implemented the gated LLM extraction adapter with fixed mock clients in CI.
- Activation requires both `SIGNAL_SANDBOX_ENABLE_LLM=1` and per-run `llm_approved=True`.
- Every successful result is `draft_pending_review` with `adapter_id="llm/<provider>/<model>"`.
- Paid Claude-style calls enforce `SIGNAL_SANDBOX_COST_CAP_USD` before invoking once budget is exhausted.
- `write_ledger` rejects direct LLM-sourced records unless `reviewer_id` is present.
- Heavy-task evidence is archived at `docs/audit/HEAVY_T20_EVIDENCE.md`.
- Phase 8 archive is `docs/archive/PHASE8_REVIEW.md`.
- Phase 9 archive is `docs/archive/PHASE9_REVIEW.md`.

Only send codex to the full ARCHITECTURE.md / IMPLEMENTATION_CONTRACT.md when a task is heavy or touches cross-cutting boundaries.

---

## Fix Queue

empty

<!--
The Fix Queue contains items that must be addressed before the next phase gate but
were deferred from the current task. Format:

- FQ-01: [T-NN] Description. Added: YYYY-MM-DD.
-->

---

## Open Findings

### Open ADRs (block specific phases)
- ADR-001 (`docs/adr/ADR-001-snapshot-serialization.md`) — accepted on 2026-05-07; deterministic Parquet snapshot bytes selected for T09/T11.

### Findings from review cycles
none

<!--
### P1 Findings (block next phase gate)
- (none)

### P2 Findings (must resolve within 3 cycles)
- (none)

### P3 Findings (optional)
- (none)
-->

---

## Summary State

Phase 1 through Phase 10 are complete. The deterministic sandbox baseline is 94
passing tests, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass locally.
The implemented surface includes:

- installable Python package and CLI skeleton;
- source manifest, capture loader, signal record schema, ledger I/O, dedup, and
  ambiguity handling;
- deterministic price provider interface, operator-file provider, exchange
  public provider, yfinance prototype provider, snapshot persistence, outcome
  matcher, aggregator, and Markdown report renderer;
- manual, rule, and gated LLM extraction adapters;
- draft pseudo-label, author-profile, deterministic draft validation/parser,
  draft export, exception-review queue, and draft-helper evaluation artifacts;
- Phase 4 through Phase 8 deep review archives and heavy-task evidence for
  T12, T14, and T20.

Phase 11 is now a planning/architecture reset for Author Market Intelligence.
The new roadmap keeps the signal-audit core and Phase 10 draft helper, then
adds gated work toward asset universe, market-data store, source corpus, RAG
context, market-idea extraction, deterministic thesis evaluation, bounded batch
analysis, and an Author Market Report V0.

Current pilot evidence update: `bablos79` has 60 public text captures in
`workspace/captures/bablos79/`, validated by `load_captures(Path("workspace"),
"bablos79")`. `SAS-AUTO-001` added draft-only pseudo-labels for every captured
post, `SAS-AUTO-001B` added a draft author lexicon/profile, `SAS-AUTO-002`
added pure deterministic draft validation/parser helpers, and `SAS-AUTO-003`
exported review-pending draft rows. `SAS-AUTO-004` added the exception review
queue and draft-vs-final counts. Manual approval / ledger extraction has not
run yet. These artifacts are now the first channel profile/corpus seed.

---

## Completed Tasks

- 2026-05-09 — Phase 11+ Author Market Intelligence Planning: created
  `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`, appended Phases 11-19
  and tasks `SAS-MI-001..018` to `docs/tasks.md`, updated README/architecture
  pointers, and recorded D-019/D-020. Validation after: 94 passed, 0 skipped;
  `ruff check src/ tests/` and `.venv/bin/pyright` pass. Review: skipped
  (planning/doc-only patch).
- 2026-05-09 — SAS-MI-001 Author Market Intelligence Architecture ADR:
  created `docs/adr/ADR-002-author-market-intelligence.md`, updated
  `docs/ARCHITECTURE.md` capability profiles, and recorded D-021. RAG is ON
  for local cited context only, Agentic is ON for a bounded internal batch
  analyst, Tool-Use and Planning remain OFF, runtime remains T0, and the first
  retrieval substrate is local DuckDB plus local vector/index sidecar files.
  Baseline after: 94 passed, 0 skipped. Review: skipped (doc-only architecture
  gate).
- 2026-05-09 — SAS-MI-002 MarketIdea Schema And Metrics Contract: created
  `docs/specs/MARKET_IDEA_SCHEMA.md` with MarketIdea field contract, enum
  values, evidence-span rules, approval states, deterministic horizon metrics,
  draft-only labels, review queue policy, examples, and SignalRecord
  compatibility rules. Baseline after: 94 passed, 0 skipped. Review: Phase 11
  deep review PASS; archive `docs/archive/PHASE11_REVIEW.md`.
- 2026-05-09 — SAS-MI-003 Asset Universe And Alias Registry: created
  `src/signal_sandbox/assets/registry.py`, `src/signal_sandbox/assets/__init__.py`,
  `tests/unit/test_asset_registry.py`, and `docs/specs/ASSET_UNIVERSE.md`.
  The registry defines `Asset`, `AssetAlias`, exact alias normalization,
  `exact` / `ambiguous` / `unresolved` resolution, seed coverage for BTC, ETH,
  SOL, SPY, QQQ, Phase 10 observed tickers, and an unresolved fallback. No
  market data was fetched. Baseline after: 97 passed, 0 skipped. Review: light
  PASS.
- 2026-05-09 — SAS-MI-004 Market Data Store Contract: created
  `src/signal_sandbox/market_data/store.py`,
  `src/signal_sandbox/market_data/__init__.py`,
  `tests/unit/test_market_data_store.py`, and
  `docs/specs/MARKET_DATA_STORE.md`. The store writes, loads, lists, and
  verifies immutable local OHLCV snapshots with provider, canonical asset ID,
  provider symbol, timeframe, source range, captured_at, checksum, license, and
  provenance metadata. Operator-file fixtures are supported; no paid/network
  provider was added. Baseline after: 102 passed, 0 skipped. Review: light PASS.
- 2026-05-09 — SAS-MI-005 Deterministic Horizon Metrics: created
  `src/signal_sandbox/market_data/metrics.py` and
  `tests/unit/test_horizon_metrics.py`. The evaluator computes 1d, 3d, 7d,
  and 30d returns plus MFE/MAE from local snapshots and returns explicit
  `unresolved_asset`, `non_directional`, and `insufficient_data` statuses.
  No LLM, RAG, retrieval, or analyst-summary dependency was added. Baseline
  after: 105 passed, 0 skipped. Review: Phase 12 deep review PASS; archive
  `docs/archive/PHASE12_REVIEW.md`.
- 2026-05-09 — SAS-MI-006 SourceDocument Corpus Schema: created
  `src/signal_sandbox/corpus/document.py`, `src/signal_sandbox/corpus/__init__.py`,
  `tests/unit/test_source_document.py`, and `docs/specs/SOURCE_CORPUS.md`.
  `SourceDocument` preserves capture_id, source_id, author, timestamp, text,
  evidence_url, text_sha256, optional media/transcript/OCR refs, and metadata.
  `CapturedPost` conversion preserves evidence URL and text hash. No
  transcription/OCR provider, embedding, vector store, or retrieval API was
  added. Baseline after: 108 passed, 0 skipped. Review: light PASS.
- 2026-05-09 — SAS-MI-007 Channel Profile Registry: created
  `src/signal_sandbox/profiles/`, `tests/unit/test_channel_profile.py`, and
  `docs/specs/CHANNEL_PROFILES.md`. The registry stores versioned
  channel-specific lexicons, source URLs, accepted draft / needs-review /
  excluded terms, modality flags, and review rules. The Phase 10 `bablos79`
  lexicon imports with profile_state preserved, and unknown channels have no
  default fallback. Baseline after: 111 passed, 0 skipped. Review: Phase 13
  deep review PASS; archive `docs/archive/PHASE13_REVIEW.md`.
- 2026-05-09 — SAS-MI-008 Local Retrieval Store Prototype: created
  `src/signal_sandbox/retrieval/store.py`,
  `src/signal_sandbox/retrieval/__init__.py`, and
  `tests/unit/test_retrieval_store.py`; added `duckdb` as the local retrieval
  metadata substrate. The store writes a local DuckDB catalog and deterministic
  vector sidecars, preserves source document IDs and citation metadata, records
  embedding/index metadata including deterministic fixture ID, and repeated
  ingestion is idempotent. No approved ledger writer, market-data writer,
  deterministic metric writer, runtime LLM call, or network path was added.
  Baseline after: 114 passed, 0 skipped. Review: light PASS.
- 2026-05-09 — SAS-MI-009 Cited Retrieval API: created
  `src/signal_sandbox/retrieval/query.py` and
  `tests/unit/test_retrieval_query.py`. The API returns cited snippets with
  document_id, score, source timestamp, evidence URL, and text_sha256; supports
  deterministic channel/time filtering; and rejects uncited result models. No
  approved ledger writer, market-data writer, metric writer, report writer,
  runtime LLM call, network path, or agent loop was added. Baseline after:
  117 passed, 0 skipped. Review: Phase 14 deep review PASS; archive
  `docs/archive/PHASE14_REVIEW.md`.
- 2026-05-09 — SAS-MI-010 MarketIdea Draft Extractor: created
  `src/signal_sandbox/market_ideas/` and
  `tests/unit/test_market_idea_extractor.py`. The deterministic extractor uses
  channel profiles first, classifies trade setups, directional theses, market
  regime comments, watchlists, catalyst reactions, risk warnings, and
  non-market rows, preserves direct evidence spans, and always outputs
  unapproved review-pending drafts. Baseline after: 120 passed, 0 skipped.
  Review: light PASS.
- 2026-05-09 — SAS-MI-011 MarketIdea Batch Draft Export: created
  `src/signal_sandbox/market_ideas/export.py`,
  `tests/unit/test_market_idea_export.py`, and
  `docs/pilot/MARKET_IDEA_DRAFTS_BABLOS79.md`. The export writes one row per
  source document, separates draft approval state from final review status, and
  records parser status, review queue reasons, evidence refs, candidate assets,
  and horizons. No approved ledger, outcome, or report side effects were added.
  Baseline after: 123 passed, 0 skipped. Review: Phase 15 deep review PASS;
  archive `docs/archive/PHASE15_REVIEW.md`.
- 2026-05-09 — SAS-MI-012 MarketIdea Outcome Evaluator: created
  `src/signal_sandbox/market_ideas/outcomes.py` and
  `tests/unit/test_market_idea_outcomes.py`. The evaluator resolves candidate
  assets through the asset registry, preserves unresolved/ambiguous cases,
  computes deterministic horizon metrics from local snapshots, and records
  source document ID, market idea ID, asset ID, snapshot ID, and metric version.
  Baseline after: 126 passed, 0 skipped. Review: light PASS.
- 2026-05-09 — SAS-MI-013 Author Metrics Aggregator: created
  `src/signal_sandbox/market_ideas/author_metrics.py` and
  `tests/unit/test_author_metrics.py`. The aggregator computes counts by idea
  type, asset type, horizon status, and review status; computes directional hit
  rate only for evaluable directional outcomes; and reports null/non-market
  content separately. Baseline after: 129 passed, 0 skipped. Review: Phase 16
  deep review PASS; archive `docs/archive/PHASE16_REVIEW.md`.
- 2026-05-09 — SAS-MI-014 Batch Analyst Contract: created
  `src/signal_sandbox/batch_analyst/`,
  `tests/unit/test_batch_analyst_contract.py`, and
  `docs/specs/BATCH_ANALYST.md`. The bounded contract declares input scope,
  allowed operations, max iterations, retrieval cap, cost cap, and stop reasons.
  Runner audit logs record retrieval, metric read, prompt input, and generated
  memo checksums. No shell, network collector, broker, or report publisher
  surface was added. Baseline after: 132 passed, 0 skipped. Review:
  agent-trigger strict review PASS.
- 2026-05-09 — SAS-MI-015 Internal Analyst Memo Export: created
  `src/signal_sandbox/batch_analyst/memo.py`,
  `tests/unit/test_analyst_memo_export.py`,
  `docs/pilot/BABLOS79_INTERNAL_MARKET_MEMO.md`, and
  `docs/audit/AGENTIC_EVAL.md`. The memo export separates required sections,
  validates interpretive-claim citations against retrieved source documents or
  deterministic metric IDs, and enforces internal-only usage. Baseline after:
  135 passed, 0 skipped. Review: Phase 17 deep review PASS; archive
  `docs/archive/PHASE17_REVIEW.md`.
- 2026-05-09 — SAS-MI-016 Author Market Report Template: created
  `src/signal_sandbox/reports/author_market.py`,
  `tests/unit/test_author_market_report.py`, and
  `docs/pilot/reports/bablos79_AUTHOR_MARKET_REPORT_V0.md`. The renderer
  outputs the required report sections, includes the canonical non-advice
  disclaimer, blocks missing source-document or market-snapshot provenance, and
  separates trade setup metrics from broader commentary metrics. Baseline
  after: 138 passed, 0 skipped. Review: light PASS.
- 2026-05-09 — SAS-MI-017 Sellability And Scope Decision Gate: created
  `docs/pilot/AUTHOR_MARKET_REPORT_DECISION.md`. Verdict: iterate internally,
  do not sell Author Market Report V0 yet. The decision cites report quality,
  thin evidence coverage, pending customer feedback, no payment signal,
  controlled implementation risk, exact next bottleneck, and forbidden
  expansion scope. Baseline after: 138 passed, 0 skipped. Review: Phase 18
  deep review PASS; archive `docs/archive/PHASE18_REVIEW.md`.
- 2026-05-09 — SAS-MI-018 Modality And Tooling Scope ADR: created
  `docs/adr/ADR-003-channel-specific-tools.md` and appended
  `SAS-MI-019: Reviewer Coverage Export Pack` to `docs/tasks.md`. The ADR
  chooses deterministic reviewer/export improvements over voice, OCR, news,
  fund/equity, and lexicon expansion because the current bottleneck is reviewed
  evidence coverage across the 60 public `bablos79` captures. Baseline after:
  138 passed, 0 skipped. Review: skipped as doc-only.
- 2026-05-09 — SAS-MI-019 Reviewer Coverage Export Pack: created
  `src/signal_sandbox/market_ideas/review_coverage.py`,
  `tests/unit/test_review_coverage_export.py`, and
  `docs/pilot/bablos79_REVIEW_COVERAGE_PACK.md`. The exporter creates one
  deterministic coverage row per source document, separates evidence/metric/
  interpretation/customer-sample status buckets, and avoids ledger, report,
  market-data, provider, or customer-claim side effects. Baseline after:
  141 passed, 0 skipped. Review: Phase 19 deep review PASS; archive
  `docs/archive/PHASE19_REVIEW.md`.

---

## Completed Task Archive

Older detailed task entries were compacted on 2026-05-07 after reaching the
orchestrator compaction threshold. Full task definitions remain in
`docs/tasks.md`; review archives remain in `docs/archive/`.

| Range | Summary | Final baseline / archive |
|-------|---------|--------------------------|
| T01-T03 | Project skeleton, CI setup, and smoke-test baseline. | 18 passed, 0 skipped; `docs/archive/PHASE1_REVIEW.md` |
| T04-T06 | Source manifest, capture loader, and signal record schema. | 31 passed, 0 skipped; `docs/archive/PHASE2_REVIEW.md` |
| T07-T08 | Ledger I/O, deterministic deduplication, and ambiguity flagging. | 38 passed, 0 skipped; `docs/archive/PHASE3_REVIEW.md` |
| T09-T11 | Price provider interface, operator-file provider, and immutable snapshot persistence. | 47 passed, 0 skipped; `docs/archive/PHASE4_REVIEW.md` |
| T12-T14 | Outcome matching, aggregation, and deterministic Markdown reports. | 65 passed, 0 skipped; `docs/archive/PHASE5_REVIEW.md`; heavy evidence T12/T14 |
| T15-T17 | Extraction adapter ABC, manual extraction, and rule extraction templates. | 72 passed, 0 skipped; `docs/archive/PHASE6_REVIEW.md` |
| T18-T19 | Public exchange OHLCV provider and yfinance prototype provider. | 77 passed, 0 skipped; `docs/archive/PHASE7_REVIEW.md` |
| T20 | Gated LLM extraction adapter with cost cap and human-review ledger guard. | 84 passed, 0 skipped; `docs/archive/PHASE8_REVIEW.md`; heavy evidence T20 |
| Phase 9 pilot loop | Pilot scope, methodology, capture/extraction/report blocker logs, customer/payment logs, repeat-or-automate decision, and later public `bablos79` capture parse. | 84 passed, 0 skipped; `docs/archive/PHASE9_REVIEW.md`; 60 public text captures |
| Phase 10 draft assistant | Machine-first pseudo-labels, author lexicon/profile, deterministic draft validation/parser, draft export, review queue, and draft-helper evaluation. | 93 passed, 0 skipped; `docs/archive/PHASE10_REVIEW.md` |
| Transition planning | Author Market Intelligence roadmap, continuous orchestrator loop update, and Phase 11+ task graph. | 94 passed, 0 skipped; D-018/D-019/D-020 |

---

## Profile State: RAG

- RAG Status: ON
- Active corpora: Phase 13 `SourceDocument` schema plus Phase 10 `bablos79`
  captures/profile artifacts as the first seed
- Retrieval baseline: `SAS-MI-009` local ingestion + cited query API; 117 tests passed,
  0 skipped
- Open retrieval findings: none
- Index schema version: `retrieval-index-v1`
- Pending reindex actions: none until Phase 14
- Retrieval-related next tasks: none active until downstream extraction/analysis uses retrieval context
- Retrieval-driven tasks: none active

---

## Tool-Use State

- Tool-Use Profile: OFF
- Active tools: n/a
- Tool eval baseline: n/a
- Open tool findings: none

---

## Agentic State

- Agentic Profile: ON
- Active agent roles: bounded internal batch analyst implemented for Phase 17
- Loop termination state: `SAS-MI-014` runner enforces max iterations, fixed
  operations, audit log, and explicit stop reason; `SAS-MI-015` memo export
  enforces internal-only cited interpretation
- Open agentic findings: none

---

## Planning State

- Planning Profile: OFF
- Plan schema version: n/a
- Open plan findings: none; ADR-002 keeps Planning OFF because batch job contracts are workflow configuration, not a plan-as-deliverable subsystem

---

## Compliance State

- Compliance Status: OFF
- Compliance Profile: OFF
- Active frameworks: none
- Compliance eval baseline: n/a
- Open compliance findings: none

---

## Evaluation State

### Last Evaluation

- Date: 2026-05-09
- Task: `SAS-MI-015`
- Profile: Agentic
- Eval Source: `.venv/bin/python -m pytest tests/unit/test_analyst_memo_export.py -q`, run 2026-05-09
- Artifact: `docs/audit/AGENTIC_EVAL.md`
- Primary metric: memo guard test pass rate = `1.000000` (`3/3`)
- Result: PASS; first recorded agentic memo-export baseline, no regression.

### Regression Thresholds

- Default: >15% regression → P0; >5% regression → P1; ≤5% → no finding.
- Apply to extraction acceptance rate (T20) once a baseline is recorded.

### Recorded Baselines

- 2026-05-07 — LLM extraction acceptance rate fixture baseline:
  `1.000000` (`3/3` drafts approved without modification) in
  `tests/eval/test_llm_extraction_quality.py`.
- 2026-05-09 — Agentic memo guard fixture baseline:
  `1.000000` (`3/3` memo export guard tests passed) in
  `tests/unit/test_analyst_memo_export.py`.

---

## Heavy-Task Evidence Index

Heavy tasks defined in `docs/tasks.md`:

| Task | Heavy reason | Evidence file (created at task close) |
|------|--------------|----------------------------------------|
| T12  | Outcome matching is the load-bearing reproducibility surface; floating-point determinism + rule-citation correctness must be auditable | `docs/audit/HEAVY_T12_EVIDENCE.md` |
| T14  | Markdown report is the user-facing artifact; disclaimer integrity, provenance, and per-signal evidence are P0 boundaries | `docs/audit/HEAVY_T14_EVIDENCE.md` |
| T20  | LLM extraction adapter introduces a non-deterministic source whose output must never become "truth"; cost-cap and review-gate are load-bearing | `docs/audit/HEAVY_T20_EVIDENCE.md` |

---

## Instructions for Codex

1. Read `docs/IMPLEMENTATION_CONTRACT.md` before starting any task.
2. Read the full task definition in `docs/tasks.md` before writing any code.
3. Read all Depends-On tasks to understand interface contracts.
4. Read the task's `Context-Refs` and the relevant entries in `docs/DECISION_LOG.md` and `docs/IMPLEMENTATION_JOURNAL.md` when the task depends on prior decisions, proof, or findings.
5. Run `python -m pytest tests/ -q` to capture the current baseline before making any changes.
6. Run `ruff check src/ tests/` — must exit 0 before starting. If not, fix in a separate commit, then restart.
7. Write tests before or alongside implementation. Every acceptance criterion has a passing test.
8. Update this file at every phase boundary (new baseline, next task, open findings).
9. Commit with format: `type(scope): description` — one logical change per commit. No `Co-Authored-By` from AI agents.
10. When done: return `IMPLEMENTATION_RESULT: DONE` with the new baseline and what changed.
11. When blocked: return `IMPLEMENTATION_RESULT: BLOCKED` with the exact blocker.
