# CODEX_PROMPT.md — Signal Analytics Sandbox

Version: 2.51
Date: 2026-05-09
Phase: 17

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

- **Phase:** 17 (Bounded batch analyst)
- **Baseline:** 132 passing tests, 0 skipped
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
- **Orchestrator loop contract:** `docs/prompts/ORCHESTRATOR.md#phase-continuation-contract`

---

## Next Task

`SAS-MI-015: Internal Analyst Memo Export`

`SAS-MI-014` implemented the bounded batch analyst contract. The next
implementation task is `SAS-MI-015`.

Immediate instruction:
- Implement `SAS-MI-015` from `docs/tasks.md`.
- Export an internal analyst memo separating deterministic metrics, cited
  evidence, interpretation, limitations, and review queue.
- Every interpretive claim must cite retrieved source documents or deterministic
  metric IDs.
- Memo must remain internal and not customer-facing.

Closeout digest for the Orchestrator:
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

- 2026-05-07 — SAS-PILOT-001 Pilot Scope: created
  `docs/pilot/PILOT_SCOPE.md` for the three public Telegram pilot sources,
  selected the first source, defined target signal counts, scope exclusions,
  and customer-centered success/kill criteria. Baseline after: 84 passed,
  0 skipped. Review: skipped (doc-only patch per orchestrator review exception).
- 2026-05-07 — SAS-PILOT-002 Methodology V0: created
  `docs/pilot/METHODOLOGY_V0.md` with required capture fields, signal
  qualification rules, extraction statuses, ambiguity handling, deterministic
  outcome semantics, price provenance, and report guardrails. Baseline after:
  84 passed, 0 skipped. Review: skipped (doc-only patch per orchestrator review
  exception).
- 2026-05-07 — SAS-PILOT-003 First Source Capture Plan And Log: created
  `docs/pilot/CAPTURE_LOG.md` for `https://t.me/bablos79` with capture method,
  required evidence fields, captured/skipped/blocked/pending status definitions,
  skip/block reason codes, and a pending operator-input row because no real
  captures are present. Baseline after: 84 passed, 0 skipped. Review: skipped
  (doc-only patch per orchestrator review exception).
- 2026-05-07 — SAS-PILOT-004 First Source Manual Extraction Log: created
  `docs/pilot/EXTRACTION_LOG.md` for `https://t.me/bablos79` with required
  extraction fields, status counts, a pending capture row, explicit blocker on
  operator-supplied public captures, and no fabricated signal candidates.
  Baseline after: 84 passed, 0 skipped. Review: skipped (doc-only patch per
  orchestrator review exception).
- 2026-05-07 — SAS-PILOT-005 First Source Report V0: created
  `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md` because no real captures,
  extraction rows, approved ledger, price snapshot, or outcomes exist. The memo
  records source, planned audit window, zero counts, blocker, limitations, and
  non-advice / historical-only language. Baseline after: 84 passed, 0 skipped.
  Review: skipped (doc-only patch per orchestrator review exception).
- 2026-05-07 — SAS-PILOT-006 Customer Feedback And Payment Signal Log: created
  `docs/pilot/CUSTOMER_FEEDBACK.md` and `docs/pilot/PAYMENT_SIGNAL_LOG.md` with
  pending rows, past-behavior feedback questions, objection/status definitions,
  payment-signal categories, refusal reasons, and Telegram-delivery-as-format
  guardrails. Baseline after: 84 passed, 0 skipped. Review: skipped (doc-only
  patch per orchestrator review exception).
- 2026-05-07 — SAS-PILOT-007 Repeat Or Automate Decision: created
  `docs/pilot/PILOT_DECISION.md` and recorded D-014. Verdict:
  stop/defer automation until real public captures are supplied for the first
  source. No new engineering phase is approved. Baseline after: 84 passed,
  0 skipped. Review: Phase 9 deep review PASS.
- 2026-05-07 — Public Capture Parse for bablos79: parsed 60 public text posts
  from unauthenticated Telegram `/s/` pages into
  `workspace/captures/bablos79/`, wrote
  `docs/pilot/bablos79_CAPTURE_MANIFEST.json`, updated capture/extraction logs,
  and revised D-014 to continue manual extraction while deferring automation.
- 2026-05-07 — Auto Extraction Development Plan: created
  `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`, appended Phase 10
  `SAS-AUTO-001`, `SAS-AUTO-001B`, and `SAS-AUTO-002..005` to
  `docs/tasks.md`, and recorded D-015. Added `SAS-AUTO-001B` and D-016 for
  offline frontier-model author lexicon discovery. This seed-label-first shape
  was superseded by the 2026-05-08 machine-first roadmap below.
- 2026-05-08 — Audit-Grade Automation Roadmap: added
  `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md` and realigned Phase 10 away
  from manual seed labeling toward machine-first pseudo-label bootstrap,
  deterministic validators, author profile discovery, and exception review.
  Next task: `SAS-AUTO-001: Machine-First Pseudo-Label Bootstrap`.
- 2026-05-08 — Continuous Orchestrator Loop: updated
  `docs/prompts/ORCHESTRATOR.md` so phase boundaries require deep review,
  archive, doc update, phase report, explicit next-task advancement, and then
  immediate continuation unless a concrete stop condition exists.
- 2026-05-08 — SAS-AUTO-001 Machine-First Pseudo-Label Bootstrap: created
  `docs/pilot/bablos79_PSEUDO_LABELS.md` and
  `workspace/extraction/bablos79_pseudo_labels.jsonl` with one draft-only
  pseudo-label row for each of the 60 `bablos79` captures. Suggested status
  distribution: 50 `not_a_signal`, 7 `insufficient_fields`, 3 `needs_review`;
  approved ledger rows created: 0. Baseline after: 84 passed, 0 skipped.
  Review: skipped (doc/workspace artifact plus state-coupled test update per
  orchestrator review exception).
- 2026-05-08 — SAS-AUTO-001B Author Lexicon And Draft Profile Discovery:
  created `docs/pilot/bablos79_AUTHOR_PROFILE.md` and
  `workspace/lexicons/bablos79_lexicon_draft.json` with 32 evidence-cited
  draft lexicon/profile candidates grouped by extraction category and
  classified as `accepted_for_draft`, `needs_review`, or `excluded`. No parser
  code or runtime LLM path was added. Baseline after: 84 passed, 0 skipped.
  Review: skipped (doc/workspace artifact patch per orchestrator review
  exception).
- 2026-05-08 — SAS-AUTO-002 Deterministic Validators And Draft Parser Library:
  created `src/signal_sandbox/extraction/draft_validation.py`,
  `src/signal_sandbox/extraction/draft_parser.py`,
  `tests/unit/test_draft_validation.py`, and
  `tests/unit/test_draft_parser.py`. The validator rejects unsupported
  pseudo-label evidence/candidate fields; the parser produces review-only
  deterministic drafts from static accepted profile terms, preserves evidence
  fields, and never maps directly to `approved`. Baseline after: 90 passed,
  0 skipped. Review: light PASS.
- 2026-05-08 — SAS-AUTO-003 Draft Export Artifact: created
  `src/signal_sandbox/extraction/draft_export.py`,
  `tests/unit/test_draft_export.py`, and
  `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`. The export contains 60
  deterministic draft-only rows sorted by source timestamp and capture_id, with
  suggested status, candidate fields, missing fields, reason codes, confidence,
  evidence_url, text_sha256, and reviewer_id=`pending`. No ledger files were
  created. Baseline after: 93 passed, 0 skipped. Review: light PASS.
- 2026-05-08 — SAS-AUTO-004 Exception Review Queue And Extraction Log Merge:
  updated `docs/pilot/EXTRACTION_LOG.md` with draft suggested status counts and
  one draft suggestion row per capture while keeping final statuses pending.
  Created `docs/pilot/bablos79_REVIEW_QUEUE.md` with 23 review rows selected by
  exception status, low confidence, customer-facing asset candidates,
  trade-management ambiguity, and deterministic non-signal sampling. Approved
  ledger rows created: 0. Baseline after: 93 passed, 0 skipped. Review:
  skipped (doc-only patch per orchestrator review exception).
- 2026-05-08 — SAS-AUTO-005 Draft Extraction Evaluation And Next Decision:
  created `docs/pilot/AUTO_EXTRACTION_EVAL.md` and updated
  `docs/pilot/PILOT_DECISION.md`. The eval records Date, Eval Source, row
  counts, suggested-status distribution, review-queue size, false-positive
  notes, and operator-review implications. Verdict: keep the draft helper for
  internal exception review only; no bot/private scraping/marketplace/copy
  trading/public leaderboard/LLM-truth expansion. Baseline after: 93 passed,
  0 skipped. Review: skipped (doc-only patch per orchestrator review exception).
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
- Active agent roles: planned bounded internal batch analyst in Phase 17
- Loop termination state: pending Phase 17 implementation; ADR-002 requires max iterations, fixed operations, audit log, and explicit stop reason
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

### Regression Thresholds

- Default: >15% regression → P0; >5% regression → P1; ≤5% → no finding.
- Apply to extraction acceptance rate (T20) once a baseline is recorded.

### Recorded Baselines

- 2026-05-07 — LLM extraction acceptance rate fixture baseline:
  `1.000000` (`3/3` drafts approved without modification) in
  `tests/eval/test_llm_extraction_quality.py`.

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
