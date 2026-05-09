# Implementation Journal — Signal Analytics Sandbox

Version: 1.0
Last updated: 2026-05-09
Status: append-only

This file is durable handoff context across agents and sessions. It records what changed, why, what evidence was collected, and what remains open. It is a retrieval surface, not authority.

---

## Journal Entry Template

```markdown
### YYYY-MM-DD — SESSION_OR_TASK_ID — SHORT_TITLE

- Scope: files / directories / task IDs
- Why this work happened: reason or trigger
- Decisions applied: Decision Log / ADR refs or "none"
- Evidence collected: tests / evals / review reports / manual checks
- Follow-ups: next task, open risk, or "none"
- Notes for next agent: only the context worth carrying forward
```

---

## Entries

### 2026-05-07 — Bootstrap — Phase 1 Governance Package

- Scope: `docs/ARCHITECTURE.md`, `docs/spec.md`, `docs/tasks.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/prompts/`, `docs/audit/`, `.github/workflows/ci.yml`, `.claude/commands/orchestrate.md`.
- Why this work happened: project bootstrap via the AI Workflow Playbook `/bootstrap-new` flow.
- Decisions applied: D-001..D-012 (initial decision log; see `docs/DECISION_LOG.md`).
- Evidence collected: brief is `templates/PROJECT_BRIEF.md`; operator answers locked the five bootstrap clarifying questions on 2026-05-07.
- Follow-ups: SAS-001 (paid pilot demand), SAS-002 (legal/risk memo) must complete and be acknowledged in `docs/CODEX_PROMPT.md §Phase 0 Gate Status` before T01 begins.
- Notes for next agent: Heavy tasks are T12 (outcome matcher), T14 (report renderer), T20 (LLM extraction adapter). The reproducibility contract (PSR-2) and the LLM-non-truth rule (PSR-3) are load-bearing — preserve at every adapter boundary.

### 2026-05-07 — Phase 9 Planning — Customer-Backed Telegram Pilot Loop

- Scope: `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`, `docs/PILOT_DEVELOPMENT_LOOP_RU.md`, `docs/pilot/README.md`.
- Why this work happened: the operator clarified that the three Telegram groups in `docs/PILOT_LOG.md` were provided by potential customers and the next loop will be run through `prompts/ORCHESTRATOR.md`, so the pilot must be represented in the orchestrator-readable task graph, not only in a strategy report.
- Decisions applied: D-013.
- Evidence collected: `STARTUP_PRESSURE_TEST_RU.md` pressure test; operator clarification in chat; existing pilot sources in `docs/PILOT_LOG.md`.
- Follow-ups: run `SAS-PILOT-001: Pilot Scope` next. Start with `docs/pilot/PILOT_SCOPE.md`, then `SAS-PILOT-002: Methodology V0`.
- Notes for next agent: Phase 9 is validation-first. Do not modify product code until the pilot decision gate identifies a measured bottleneck. Do not widen into Telegram bot, private scraping, public SaaS, leaderboard, marketplace, copy trading, broker integration, or Entropy Core feed.

### 2026-05-07 — SAS-PILOT-001 — Pilot Scope

- Scope: `docs/pilot/PILOT_SCOPE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `tests/test_workspace_validation.py`.
- Why this work happened: Phase 9 needed a concrete pilot scope before capture, extraction, or report work could start.
- Decisions applied: D-013; public-source-only and validation-first boundaries from `docs/IMPLEMENTATION_CONTRACT.md` and `docs/PILOT_DEVELOPMENT_LOOP_RU.md`.
- Evidence collected: pre-task baseline restored to 84 passed, 0 skipped after updating the phase-boundary guard test to match current Phase 9 state; `ruff check src/ tests/` passes.
- Follow-ups: run `SAS-PILOT-002: Methodology V0` next, using `docs/pilot/PILOT_SCOPE.md` as the first context reference.
- Notes for next agent: first source is `https://t.me/bablos79` by deterministic PILOT_LOG ordering, not expected performance. Default target is 30-50 defensible signal records where available. If public captures are missing or insufficient, write blocker/limitation rows instead of inventing posts or signals.

### 2026-05-07 — SAS-PILOT-002 — Methodology V0

- Scope: `docs/pilot/METHODOLOGY_V0.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: the first source audit needed fixed capture, extraction, outcome, provenance, and report guardrails before any public posts are recorded.
- Decisions applied: D-013; PSR-1 public-source-only, PSR-2 reproducibility, PSR-3 LLM output is never truth, PSR-6 disclaimer integrity, and PSR-11 no forward-looking claims.
- Evidence collected: `docs/pilot/METHODOLOGY_V0.md` covers required capture fields, signal qualification, statuses, deterministic outcome/exclusion semantics, price provenance, and non-advice / historical-only guardrails. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-003: First Source Capture Plan And Log` next for `https://t.me/bablos79`.
- Notes for next agent: do not fabricate public posts. If the workspace has no real captures, create the capture log with `pending-operator-input` rows and explicit blocker/status definitions.

### 2026-05-07 — SAS-PILOT-003 — First Source Capture Plan And Log

- Scope: `docs/pilot/CAPTURE_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: the first source audit needed a public/operator-supplied capture structure before manual extraction could begin.
- Decisions applied: D-013; PSR-1 public-source-only boundary and `docs/pilot/METHODOLOGY_V0.md` capture field requirements.
- Evidence collected: no real `bablos79` captures are present in the workspace; `docs/pilot/CAPTURE_LOG.md` initializes the queue with `pending-operator-input`, status definitions, required evidence fields, and skip/block reason codes. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-004: First Source Manual Extraction Log` next. It should state extraction is blocked until the operator supplies real public captures.
- Notes for next agent: do not invent `public_url`, raw text, hashes, or signal candidates. Keep any rows without real evidence as `pending-operator-input`.

### 2026-05-07 — SAS-PILOT-004 — First Source Manual Extraction Log

- Scope: `docs/pilot/EXTRACTION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: the pilot needed a manual extraction log and blocker state before any report artifact could be produced.
- Decisions applied: D-013; `docs/pilot/METHODOLOGY_V0.md` extraction statuses and human-review boundaries.
- Evidence collected: `docs/pilot/CAPTURE_LOG.md` has no `captured` rows, so `docs/pilot/EXTRACTION_LOG.md` records `pending_capture=1`, all approved/ambiguous/excluded counts as 0, and an explicit blocker on operator-supplied public captures. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-005: First Source Report V0` next. Because no captures/extraction exist, write a blocked-report memo instead of report metrics.
- Notes for next agent: do not create outcomes, win/loss statistics, or signal examples without real captured public posts and human-reviewed extraction rows.

### 2026-05-07 — SAS-PILOT-005 — First Source Report V0

- Scope: `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 9 needed a customer-readable report artifact or honest blocker memo for the first source.
- Decisions applied: D-013; non-advice/historical-only and no-forward-looking boundaries from `docs/IMPLEMENTATION_CONTRACT.md`.
- Evidence collected: no captures, extraction rows, approved ledger, price snapshot, or outcomes exist. The blocked-report memo records zero counts, blocker, limitations, and next required operator inputs. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-006: Customer Feedback And Payment Signal Log` next. Since no customer-ready report was delivered, feedback/payment rows should be pending.
- Notes for next agent: do not record payment success, customer decision impact, or report acceptance without real customer behavior.

### 2026-05-07 — SAS-PILOT-006 — Customer Feedback And Payment Signal Log

- Scope: `docs/pilot/CUSTOMER_FEEDBACK.md`, `docs/pilot/PAYMENT_SIGNAL_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 9 needed customer feedback and payment-signal structures before the repeat/automation decision gate.
- Decisions applied: D-013; validation-first rule that customer/payment behavior, not engineering completion, decides next scope.
- Evidence collected: no customer review or payment signal exists because the first report is blocked on captures. Feedback/payment logs contain pending rows, past-behavior questions, payment status definitions, refusal reasons, and Telegram-delivery guardrails. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-007: Repeat Or Automate Decision` next. Current evidence should lead to "stop/defer until public captures are supplied"; no automation is justified.
- Notes for next agent: do not mark pilot success without paid/deposit/repeat/referral behavior or a real customer decision impact.

### 2026-05-07 — SAS-PILOT-007 — Repeat Or Automate Decision

- Scope: `docs/pilot/PILOT_DECISION.md`, `docs/DECISION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 9 needed an explicit decision gate after pilot logs showed whether to repeat, automate, pivot, or stop.
- Decisions applied: D-014.
- Evidence collected: the decision cites scope, methodology, capture log, extraction log, blocked-report memo, customer feedback log, and payment signal log. Current evidence shows no real captures, no extraction, no customer decision impact, and no payment signal. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run Phase 9 deep review/archive. After that, wait for operator-supplied public captures before reopening the pilot loop.
- Notes for next agent: no new engineering phase is approved. Do not continue to remaining sources or automation until `bablos79` is unblocked or formally blocked with a concrete reason.

### 2026-05-07 — Public Capture Parse — bablos79

- Scope: `workspace/captures/bablos79/`, `docs/pilot/bablos79_CAPTURE_MANIFEST.json`, `docs/pilot/CAPTURE_LOG.md`, `docs/pilot/EXTRACTION_LOG.md`, `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md`, `docs/pilot/PILOT_DECISION.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`.
- Why this work happened: operator instructed Codex to parse the public first source instead of waiting for manually supplied capture files.
- Decisions applied: D-014 updated — continue manual extraction for the captured first-source batch; defer automation.
- Evidence collected: fetched public unauthenticated Telegram `/s/` HTML pages for `bablos79`, captured 60 text posts into `workspace/captures/bablos79/`, and validated them with `load_captures(Path("workspace"), "bablos79")` returning 60 posts with matching hashes.
- Follow-ups: manually classify the 60 captures in `docs/pilot/EXTRACTION_LOG.md`; do not generate approved records, outcomes, or report metrics until extraction and human review are complete.
- Notes for next agent: capture blocker is cleared for the first batch, but there is still no approved ledger and no customer/payment signal. Automation remains deferred.

### 2026-05-07 — Phase 10 Planning — Draft Extraction Assistant

- Scope: `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`.
- Why this work happened: operator approved building a clear parser/automatic extraction path after the first public capture batch existed.
- Decisions applied: D-015, D-016.
- Evidence collected: initial Phase 10 task graph required seed labels, offline frontier-model author lexicon discovery with human approval, deterministic parser implementation, draft export, extraction-log merge, and evaluation before any next automation decision.
- Follow-ups: superseded on 2026-05-08 by the machine-first pseudo-label bootstrap plan.
- Notes for next agent: this seed-label-first plan is historical context only; use the 2026-05-08 roadmap entry below.

### 2026-05-08 — Audit-Grade Automation Roadmap

- Scope: `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md`, `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`.
- Why this work happened: operator clarified that the next loop should avoid manual seed labeling and automate the first pass, while keeping audit-grade boundaries through validators and exception review.
- Decisions applied: D-017; D-015 superseded.
- Evidence collected: roadmap now defines phases A-M from data foundation through confidence-gated automation; Phase 10 now starts with `SAS-AUTO-001: Machine-First Pseudo-Label Bootstrap`.
- Follow-ups: run `SAS-AUTO-001` to create `docs/pilot/bablos79_PSEUDO_LABELS.md` and `workspace/extraction/bablos79_pseudo_labels.jsonl` for all 60 captures.
- Notes for next agent: do not start with `BABLOS79_LABEL_SEED.md`; manual work is now exception review, not seed labeling. Parser code starts after pseudo-labels and `docs/pilot/bablos79_AUTHOR_PROFILE.md` exist.

### 2026-05-08 — Continuous Phase Loop Contract

- Scope: `docs/prompts/ORCHESTRATOR.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`.
- Why this work happened: operator clarified that the AI development loop must not stop between phases after deep review; it should continue after review/archive/doc update.
- Decisions applied: D-018.
- Evidence collected: `docs/prompts/ORCHESTRATOR.md` now has a Phase Continuation Contract and `Step 6.7` requiring next-task advancement after phase review unless a concrete stop condition exists.
- Follow-ups: when Phase 10 finishes, run deep review, archive, update docs, then immediately advance to the next task/phase and continue the loop.
- Notes for next agent: do not leave the project in a "review complete, waiting" state unless a named blocker or explicit user pause exists.

### 2026-05-08 — SAS-AUTO-001 — Machine-First Pseudo-Label Bootstrap

- Scope: `docs/pilot/bablos79_PSEUDO_LABELS.md`, `workspace/extraction/bablos79_pseudo_labels.jsonl`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `tests/test_workspace_validation.py`.
- Why this work happened: Phase 10 starts with machine-first pseudo-labels over all 60 local public captures so manual review can focus on exceptions rather than seed-labeling every row.
- Decisions applied: D-017; draft-only / no-LLM-truth boundary from `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md` and `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`.
- Evidence collected: generated 60 JSONL pseudo-label rows matching `workspace/captures/bablos79/`; distribution is 50 `not_a_signal`, 7 `insufficient_fields`, and 3 `needs_review`. Validation confirmed required JSONL fields, `draft_only=true`, `approval_state="unapproved"`, matching capture IDs, and evidence-span text present in raw captures. Updated the phase-boundary guard test from Phase 9->10 to Phase 10->11 after advancing project state. Baseline remains 84 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-AUTO-001B: Author Lexicon And Draft Profile Discovery` next, using `docs/pilot/bablos79_PSEUDO_LABELS.md`, `workspace/extraction/bablos79_pseudo_labels.jsonl`, and `workspace/captures/bablos79/`.
- Notes for next agent: do not treat pseudo-labels as approved extraction truth. Parser implementation remains blocked until the author profile and lexicon draft exist.

### 2026-05-08 — SAS-AUTO-001B — Author Lexicon And Draft Profile Discovery

- Scope: `docs/pilot/bablos79_AUTHOR_PROFILE.md`, `workspace/lexicons/bablos79_lexicon_draft.json`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needs an author-specific draft lexicon/profile before deterministic parser implementation can use pseudo-label evidence safely.
- Decisions applied: D-017; `SAS-AUTO-001B` contract that frontier-model/profile output is offline analysis only and cannot decide approved signal truth.
- Evidence collected: generated 32 evidence-cited candidates grouped by category. Profile-state distribution is 17 `accepted_for_draft`, 9 `needs_review`, and 6 `excluded`. Validation confirmed every candidate has term, category, evidence_capture_ids, evidence_excerpts, false_positive_risk, confidence, and profile_state with no invalid state values. Baseline remains 84 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-AUTO-002: Deterministic Validators And Draft Parser Library` next. Use only static `accepted_for_draft` entries for parser draft behavior; `needs_review` and `excluded` entries must not become automatic parser truth.
- Notes for next agent: the next task is the first Phase 10 product-code task. Keep it pure/local with no CLI wiring, network calls, runtime LLM calls, or ledger writes.

### 2026-05-08 — SAS-AUTO-002 — Deterministic Validators And Draft Parser Library

- Scope: `src/signal_sandbox/extraction/draft_validation.py`, `src/signal_sandbox/extraction/draft_parser.py`, `tests/unit/test_draft_validation.py`, `tests/unit/test_draft_parser.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needed pure/local code to verify pseudo-label evidence and turn static accepted profile terms into review-only draft suggestions before any export artifact is generated.
- Decisions applied: D-017; PSR-3 LLM output is never truth; PSR-8 evidence field preservation; T0 runtime boundary.
- Evidence collected: added `validate_pseudo_label()` with rejection tests for unsupported evidence/candidate fields and `parse_draft()` with tests for structured output, evidence preservation, deterministic repeated classification, and review-required complete candidates. Full validation: 90 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS.
- Follow-ups: run `SAS-AUTO-003: Draft Export Artifact` next to export parser suggestions for all captured `bablos79` posts into `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`.
- Notes for next agent: `draft_parser.py` intentionally does not approve records or write ledgers. Keep export rows reviewer_id=`pending` and deterministic.

### 2026-05-08 — SAS-AUTO-003 — Draft Export Artifact

- Scope: `src/signal_sandbox/extraction/draft_export.py`, `tests/unit/test_draft_export.py`, `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needed a reviewable export of parser suggestions for every captured post before exception review can replace full manual labeling.
- Decisions applied: D-017; draft-only boundary; no approved ledger writes before human review.
- Evidence collected: exported 60 rows sorted by source timestamp and capture_id. Suggested status distribution is 43 `not_a_signal`, 16 `insufficient_fields`, and 1 `needs_review`; every row has reviewer_id=`pending`. No ledger directory/files were created. Full validation: 93 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS.
- Follow-ups: run `SAS-AUTO-004: Exception Review Queue And Extraction Log Merge` next to update `docs/pilot/EXTRACTION_LOG.md` and create `docs/pilot/bablos79_REVIEW_QUEUE.md`.
- Notes for next agent: keep draft suggested statuses separate from final extraction statuses. Do not convert any row to `approved`.

### 2026-05-08 — SAS-AUTO-004 — Exception Review Queue And Extraction Log Merge

- Scope: `docs/pilot/bablos79_REVIEW_QUEUE.md`, `docs/pilot/EXTRACTION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needed to turn draft parser output into a targeted human review surface while preserving final extraction status as pending.
- Decisions applied: D-017; draft-only boundary; no approved ledger writes before human review.
- Evidence collected: `docs/pilot/EXTRACTION_LOG.md` now has separate draft suggested status counts and one draft suggestion row per capture. `docs/pilot/bablos79_REVIEW_QUEUE.md` has 23 rows selected by exception status, confidence `<0.50`, customer-facing asset candidates, trade-management ambiguity, and deterministic non-signal sampling. All reviewer IDs remain `pending`; final status counts remain 0 approved / 60 pending manual extraction. Baseline remains 93 passed, 0 skipped.
- Follow-ups: run `SAS-AUTO-005: Draft Extraction Evaluation And Next Decision` next.
- Notes for next agent: evaluation must cite row counts, review queue size, false-positive risks, and the automation boundary. Do not approve bot/private scraping/marketplace/copy-trading/LLM-truth expansion.

### 2026-05-08 — SAS-AUTO-005 — Draft Extraction Evaluation And Next Decision

- Scope: `docs/pilot/AUTO_EXTRACTION_EVAL.md`, `docs/pilot/PILOT_DECISION.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needed a decision gate to decide whether the machine-first draft helper should be kept, improved, discarded, or replaced by manual-only extraction.
- Decisions applied: D-017; no scope expansion without measured customer/payment evidence.
- Evidence collected: `docs/pilot/AUTO_EXTRACTION_EVAL.md` records Date, Eval Source, row counts, suggested-status distribution, 23-row review queue size, false-positive notes, useful suggestions, and operator-review implications. `docs/pilot/PILOT_DECISION.md` now says keep the draft helper for internal exception review only. Baseline remains 93 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 10 deep review/archive/doc update. There is no next engineering task in `docs/tasks.md`; the next product action after review is human exception review of 23 queued rows plus sampled verification of 37 non-queued rows.
- Notes for next agent: do not start a new engineering phase unless human review, report feedback, or payment evidence identifies a measured bottleneck.

### 2026-05-09 — Phase 11+ Planning — Author Market Intelligence Roadmap

- Why this work happened: operator review of the first `bablos79` group showed that the channel is not only explicit trade signals; it also contains broad market regime commentary, event/news analysis, voice-message analysis behavior, watchlists, and occasional visible trade entries. The product should evaluate how those ideas behaved against market data rather than force every post into the old signal-only model.
- Decisions applied: D-019 and D-020. Phase 10 artifacts remain useful and become the first channel profile/corpus seed. RAG, Planning, and Agentic work is planned but still gated by `SAS-MI-001` before implementation.
- Evidence collected: created `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`; appended Phases 11-19 and tasks `SAS-MI-001..018` to `docs/tasks.md`; updated `README.md`, `docs/ARCHITECTURE.md`, `docs/DECISION_LOG.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `MEMORY.md`, and `AGENT_NOTES.md` for the new stage. Validation after planning docs: 94 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-001: Author Market Intelligence Architecture ADR` next. Do not implement vector storage, embeddings, market-data expansion, or batch-agent code before the ADR updates capability profiles and runtime/storage boundaries.

### 2026-05-09 — SAS-MI-001 — Author Market Intelligence Architecture ADR

- Scope: `docs/adr/ADR-002-author-market-intelligence.md`, `docs/ARCHITECTURE.md`, `docs/DECISION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 11 needed an explicit architecture gate before RAG, vector storage, market-data expansion, or batch-agent work could begin.
- Decisions applied: D-021. ADR-002 activates RAG for local cited context only, activates Agentic only for a bounded internal batch analyst, keeps Tool-Use and Planning OFF, keeps runtime T0, and selects local DuckDB plus local vector/index sidecar files as the first retrieval substrate.
- Evidence collected: ADR-002 cites the Author Market Intelligence roadmap and Phase 10 `bablos79` artifacts as the initial corpus/profile seed. Architecture capability profiles now match the ADR. No product code, embeddings, vector storage, market-data expansion, approved ledger writes, or batch-agent code were added. Validation after doc gate: 94 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-002: MarketIdea Schema And Metrics Contract` next. Keep deterministic market data as the only source of prices, returns, approved records, and outcome metrics.

### 2026-05-09 — SAS-MI-002 — MarketIdea Schema And Metrics Contract

- Scope: `docs/specs/MARKET_IDEA_SCHEMA.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 11 needed a schema and deterministic metric contract before Phase 12 adds asset resolution code.
- Decisions applied: ADR-002 deterministic-truth boundary; RAG context-only boundary; existing `SignalRecord` and outcome matcher semantics remain the strict trade/evaluation baseline.
- Evidence collected: created `docs/specs/MARKET_IDEA_SCHEMA.md` with required and optional fields, enum values, evidence-span rules, approval states, draft-only labels, deterministic horizons, metric outputs, review queue policy, examples, and SignalRecord compatibility rules. No product code, market-data fetch, embeddings, vector storage, approved ledger writes, or batch-agent code were added. Validation after spec: 94 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 11 strategy/deep review/archive before implementing `SAS-MI-003: Asset Universe And Alias Registry`.

### 2026-05-09 — SAS-MI-003 — Asset Universe And Alias Registry

- Scope: `src/signal_sandbox/assets/`, `tests/unit/test_asset_registry.py`, `docs/specs/ASSET_UNIVERSE.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 12 needed deterministic asset identity and alias resolution before market-data store and horizon metrics work.
- Decisions applied: ADR-002 T0/local-first boundary; `MARKET_IDEA_SCHEMA.md` resolution states; no guessing and no market-data fetches in this task.
- Evidence collected: added `Asset`, `AssetAlias`, `AliasResolution`, and `AssetRegistry`; resolution normalizes aliases and returns `exact`, `ambiguous`, or `unresolved` with evidence. Seed registry covers BTC, ETH, SOL, SPY, QQQ, Phase 10 observed tickers (AMD, CHMF, GAZP, MAGN, SBER, SFIN, VKCO, VTBR, X5), and an unresolved fallback. Validation after task: 97 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass. No market data was fetched.
- Follow-ups: run `SAS-MI-004: Market Data Store Contract` next.

### 2026-05-09 — SAS-MI-004 — Market Data Store Contract

- Scope: `src/signal_sandbox/market_data/`, `tests/unit/test_market_data_store.py`, `docs/specs/MARKET_DATA_STORE.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 12 needed immutable local OHLCV snapshot storage before horizon metric evaluation.
- Decisions applied: ADR-002 T0/local-first boundary; no paid/network provider expansion; snapshot immutability and checksum discipline from the existing price snapshot contract.
- Evidence collected: added `MarketDataSnapshotMetadata`, `MarketDataSnapshot`, `MarketDataStoreProtocol`, `LocalMarketDataStore`, and `make_operator_file_snapshot()`. Snapshots persist under `workspace/market_data/snapshots/<snapshot_id>/` with deterministic metadata and OHLCV bytes, load verifies checksum, list returns sorted metadata, and different-byte overwrite raises `SnapshotAlreadyExists`. Validation after task: 102 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass. No paid or network market-data provider was added.
- Follow-ups: run `SAS-MI-005: Deterministic Horizon Metrics` next.

### 2026-05-09 — SAS-MI-005 — Deterministic Horizon Metrics

- Scope: `src/signal_sandbox/market_data/metrics.py`, `tests/unit/test_horizon_metrics.py`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 12 needed deterministic horizon metrics over local snapshots before source corpus/retrieval work begins.
- Decisions applied: ADR-002 deterministic-truth boundary; `MARKET_IDEA_SCHEMA.md` metric contract; no LLM/RAG/retrieval/analyst dependency.
- Evidence collected: added `evaluate_horizon_metrics()` with 1d, 3d, 7d, and 30d returns, MFE, MAE, and explicit `unresolved_asset`, `non_directional`, and `insufficient_data` statuses. Decimal rounding is deterministic. Validation after task: 105 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 12 deep review/archive and continue to `SAS-MI-006: SourceDocument Corpus Schema`.

### 2026-05-09 — SAS-MI-006 — SourceDocument Corpus Schema

- Scope: `src/signal_sandbox/corpus/`, `tests/unit/test_source_document.py`, `docs/specs/SOURCE_CORPUS.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 13 needed a normalized source-corpus document shape before channel profiles and retrieval implementation.
- Decisions applied: ADR-002 RAG context-only boundary; public-source evidence preservation; no embeddings/vector/retrieval implementation in this task.
- Evidence collected: added `SourceDocument` and `from_captured_post()`. The schema preserves capture ID, source ID, author, timestamp, text, evidence URL, text SHA-256, optional media/transcript/OCR references, and metadata. Conversion from `CapturedPost` preserves evidence URL and text hash. Validation after task: 108 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass. No transcription/OCR provider, embedding, vector store, or retrieval API was added.
- Follow-ups: run `SAS-MI-007: Channel Profile Registry` next.

### 2026-05-09 — SAS-MI-007 — Channel Profile Registry

- Scope: `src/signal_sandbox/profiles/`, `tests/unit/test_channel_profile.py`, `docs/specs/CHANNEL_PROFILES.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 13 needed versioned channel-specific profile state before local retrieval can use author/channel context.
- Decisions applied: ADR-002 RAG context-only boundary; Phase 10 `bablos79` lexicon remains draft/profile evidence and cannot approve signal truth.
- Evidence collected: added `ProfileTerm`, `ChannelProfile`, `ChannelProfileRegistry`, and `import_bablos79_profile()`. The importer preserves `accepted_for_draft`, `needs_review`, and `excluded` states from `workspace/lexicons/bablos79_lexicon_draft.json`, records modality flags and review rules, and returns no default profile for unknown channels. Validation after task: 111 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 13 deep review/archive, then continue to `SAS-MI-008: Local Retrieval Store Prototype`.

### 2026-05-09 — SAS-MI-008 — Local Retrieval Store Prototype

- Scope: `src/signal_sandbox/retrieval/`, `tests/unit/test_retrieval_store.py`, `pyproject.toml`, `requirements.txt`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 14 needed the ADR-approved local retrieval ingestion substrate before query APIs can return cited context.
- Decisions applied: ADR-002 RAG context-only boundary; local DuckDB plus vector/index sidecar substrate; retrieval cannot mutate approved ledgers, market data, deterministic metrics, or report truth artifacts.
- Evidence collected: added `LocalRetrievalStore`, `EmbeddingMetadata`, `IndexedSourceDocument`, deterministic test embeddings, local DuckDB metadata catalog, and deterministic vector sidecar files. Ingestion preserves stable document IDs and citation metadata, records embedding/index metadata including fixture ID, and repeated ingestion is idempotent. Validation after task: 114 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-009: Cited Retrieval API` next.

### 2026-05-09 — SAS-MI-009 — Cited Retrieval API

- Scope: `src/signal_sandbox/retrieval/query.py`, `tests/unit/test_retrieval_query.py`, `src/signal_sandbox/retrieval/store.py`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 14 needed a cited retrieval API for batch analysis before market-idea extraction and later analysis tasks can use local context.
- Decisions applied: ADR-002 RAG context-only boundary; retrieval results must cite source document IDs and evidence hashes and cannot mutate deterministic truth artifacts.
- Evidence collected: added `CitedRetrievalResult`, `RetrievalQueryFilters`, and `query_retrieval_store()`. Results include document_id, snippet, score, source timestamp, evidence URL, and text_sha256; filters for channel and timestamp are deterministic; uncited result models are rejected. Validation after task: 117 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 14 deep review/archive, then continue to `SAS-MI-010: MarketIdea Draft Extractor`.

### 2026-05-09 — SAS-MI-010 — MarketIdea Draft Extractor

- Scope: `src/signal_sandbox/market_ideas/`, `tests/unit/test_market_idea_extractor.py`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 15 needed deterministic source-document to MarketIdea draft extraction before batch export.
- Decisions applied: `MARKET_IDEA_SCHEMA.md`; ADR-002 deterministic-truth boundary; Phase 10/13 channel profile states remain draft hints only.
- Evidence collected: added `MarketIdeaDraft`, `EvidenceSpan`, and `MarketIdeaDraftExtractor`. The extractor classifies fixtures into all required MarketIdea categories, uses channel profiles for asset aliases before fallback token matching, preserves direct evidence spans for asset/direction/horizon-risk-catalyst fields when present, and always emits `queued_for_review` unapproved drafts. Validation after task: 120 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-011: MarketIdea Batch Draft Export` next.

### 2026-05-09 — SAS-MI-011 — MarketIdea Batch Draft Export

- Scope: `src/signal_sandbox/market_ideas/export.py`, `tests/unit/test_market_idea_export.py`, `docs/pilot/MARKET_IDEA_DRAFTS_BABLOS79.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 15 needed a reviewable batch export surface before deterministic thesis evaluation.
- Decisions applied: `MARKET_IDEA_SCHEMA.md`; draft-only and human-review boundaries; no approved ledger or outcome/report side effects.
- Evidence collected: added `MarketIdeaExportRow`, `MarketIdeaBatchExport`, `export_market_idea_drafts()`, and Markdown rendering. The export creates one row per source document, separates `draft_approval_state` from `final_review_status`, records parser status, review queue reasons, evidence refs, candidate assets, and suggested horizons, and writes only a draft Markdown artifact. Validation after task: 123 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 15 deep review/archive, then continue to `SAS-MI-012: MarketIdea Outcome Evaluator`.

### 2026-05-09 — SAS-MI-012 — MarketIdea Outcome Evaluator

- Scope: `src/signal_sandbox/market_ideas/outcomes.py`, `tests/unit/test_market_idea_outcomes.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 16 needed deterministic thesis evaluation over MarketIdea drafts/reviewed rows.
- Decisions applied: `MARKET_IDEA_SCHEMA.md`; deterministic-truth boundary; `SAS-MI-005` horizon metric contract.
- Evidence collected: added `MarketIdeaOutcome`, `IdeaOutcomeStatus`, and `evaluate_market_idea_outcome()`. The evaluator resolves assets through the asset registry, returns unresolved/ambiguous/no-snapshot statuses without guessing, computes horizon metrics through `evaluate_horizon_metrics()` when a matching local snapshot exists, and records source document ID, market idea ID, asset ID, snapshot ID, and metric version. Validation after task: 126 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-013: Author Metrics Aggregator` next.

### 2026-05-09 — SAS-MI-013 — Author Metrics Aggregator

- Scope: `src/signal_sandbox/market_ideas/author_metrics.py`, `tests/unit/test_author_metrics.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 16 needed author/channel aggregates over deterministic MarketIdea outcomes.
- Decisions applied: `MARKET_IDEA_SCHEMA.md`; deterministic aggregation boundary; non-market/null content must be separate from failed directional ideas.
- Evidence collected: added `AuthorMetrics` and `aggregate_author_metrics()`. The aggregator computes counts by idea type, asset type, horizon status, and review status; directional hit rate only over evaluable long/short outcomes; and null/non-market count/rate separately. Validation after task: 129 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 16 deep review/archive, then continue to `SAS-MI-014: Batch Analyst Contract`.

### 2026-05-09 — SAS-MI-014 — Batch Analyst Contract

- Scope: `src/signal_sandbox/batch_analyst/`, `tests/unit/test_batch_analyst_contract.py`, `docs/specs/BATCH_ANALYST.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 17 needed a bounded agentic contract before any internal memo export.
- Decisions applied: ADR-002 bounded Agentic profile; fixed operations, max iterations, cost cap, audit log, explicit stop reason, and no mutation/publication authority.
- Evidence collected: added `BatchAnalystJob`, `BatchAnalystRunner`, stop reasons, allowed operation enum, and audit log models. Tests cover schema fields, stop reasons, and checksums for retrieval, metric reads, prompt input, and generated memo. Validation after task: 132 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass. Strict agent-trigger review found no shell, network collector, broker, report publisher, ledger mutation, or package/runtime mutation surface.
- Follow-ups: run `SAS-MI-015: Internal Analyst Memo Export` next.
