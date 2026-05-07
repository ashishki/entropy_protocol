# PHASE_HANDOFF

Use this file only at a phase boundary, context rollover, or limit recovery.

## Current State

- Phase: 8 complete.
- Active task: none; `docs/tasks.md` task graph is complete through T20.
- Branch: `codex/signal-analytics-sandbox-work`.
- Last validation: `.venv/bin/python -m pytest tests/ -q` -> 84 tests passed on 2026-05-07; `ruff check src/ tests/`, `ruff format --check src/ tests/`, and `pyright` also pass.
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

## Remaining Work

- No pending implementation task remains in the current task graph.

## Blockers Or Human Decisions

- None.

## Resume Instruction

Continue this product from `RUNBOOK.md`, `AGENT_NOTES.md`, this
`PHASE_HANDOFF.md`, `docs/CODEX_PROMPT.md`, and `docs/tasks.md`.
Do not spawn nested Codex. Continue the orchestration loop from the next pending
task in the current product tmux window.
