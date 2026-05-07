# PHASE_HANDOFF

Use this file only at a phase boundary, context rollover, or limit recovery.

## Current State

- Phase: 9 active; Phase 10 draft automation is scoped but the phase boundary
  is not advanced.
- Active task: `SAS-AUTO-001: Seed Labels For bablos79 Draft Parser`. Phase 9
  tasks are complete and archived; 60 public `bablos79` captures exist; Phase
  10 draft-extraction assistant plan is now in `docs/tasks.md`.
- Branch: `codex/signal-analytics-sandbox-work`.
- Last validation: `.venv/bin/python -m pytest tests/ -q` -> 84 tests passed on 2026-05-07; `.venv/bin/python -m ruff check src/ tests/` and `.venv/bin/python -m pyright` also pass.
- Git status summary: product-local modified docs/hooks/prompts plus untracked `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `RUNBOOK.md`, and `tests/`.

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
  - `docs/tasks.md` Phase 10 `SAS-AUTO-001`, `SAS-AUTO-001B`, and
    `SAS-AUTO-002..005`
  - D-015 and D-016 in `docs/DECISION_LOG.md`
  - `docs/CODEX_PROMPT.md` next task set to `SAS-AUTO-001`

## Remaining Work

- Run `SAS-AUTO-001`: create `docs/pilot/BABLOS79_LABEL_SEED.md` with 10-15
  representative labeled captures before parser implementation.
- Then run `SAS-AUTO-001B`: create `docs/pilot/bablos79_LEXICON_DRAFT.md`,
  `docs/pilot/bablos79_APPROVED_LEXICON.md`, and
  `workspace/lexicons/bablos79_lexicon_draft.json`.
- Then run `SAS-AUTO-002` deterministic draft parser library.
- Keep parser output draft-only and human-reviewed.

## Blockers Or Human Decisions

- None.

## Resume Instruction

Continue this product from `RUNBOOK.md`, `AGENT_NOTES.md`, this
`PHASE_HANDOFF.md`, `docs/CODEX_PROMPT.md`, and `docs/tasks.md`.
Do not spawn nested Codex. Resume from `SAS-AUTO-001`. Do not implement parser
code until seed labels and the approved author lexicon exist. Frontier-model
output may propose vocabulary only; it is not final extraction truth. Do not
write approved ledger records from parser output without human review.
