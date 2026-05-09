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
