# Implementation Journal — Signal Analytics Sandbox

Version: 1.0
Last updated: 2026-05-07
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
