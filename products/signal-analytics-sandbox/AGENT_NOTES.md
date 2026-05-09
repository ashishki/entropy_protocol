# Agent Notes — Signal Analytics Sandbox

Date: 2026-05-07
Agent: Codex

## Investigation Summary

- Product path inspected: `products/signal-analytics-sandbox/`.
- Current product state is planning/governance first, implementation not started.
- `docs/ARCHITECTURE.md` specifies a local-first Python 3.12 library + CLI named `signal-sandbox`.
- `docs/tasks.md` defines Phase 0 as human-owned gates and Phase 1 as the first engineering skeleton.
- `docs/CODEX_PROMPT.md §Phase 0 Gate Status` still marks both gates as `pending`:
  - SAS-001 paid pilot demand validation.
  - SAS-002 public-source legal / terms memo.
- `RUNBOOK.md` reports no package manager, build command, dev server, or CLI; the only supported validation command is the product-local unittest command.

## Setup Verification

Supported validation command after this session:

```bash
cd products/signal-analytics-sandbox && .venv/bin/python -m unittest discover -s tests -v
```

Result on 2026-05-07:

- 7 tests passed.
- No external package manager or network access required.

## Decisions

- Did not start T01 or any product implementation because `IMPLEMENTATION_CONTRACT.md §PSR-10` forbids engineering tasks until SAS-001 and SAS-002 are acknowledged by the operator.
- Added a product-local standard-library validation suite instead of adding runtime implementation.
- Fixed the safest validated issue found: `hooks/guard_phase_boundary.sh` did not recognize the product's current phase-line format with parenthetical text.
- Extended validation coverage for `hooks/guard_phase_boundary.sh` so it blocks cross-phase advancement through the `Next Task` pointer, not only direct phase-line edits.

## 2026-05-07 Update

- Operator acknowledged SAS-001 and SAS-002 for initial Telegram pilot sources:
  `https://t.me/bablos79`, `https://t.me/nemphiscrypts`, `https://t.me/pifagortrade`.
- Created `docs/PILOT_LOG.md` and `docs/legal_risk_memo.md`.
- Updated `docs/CODEX_PROMPT.md` gate state to `acknowledged`.
- Wrote `docs/audit/PHASE1_AUDIT.md` with PASS.
- Completed T01 Project Skeleton:
  - `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`
  - `src/signal_sandbox/` package and subpackages
  - click-based `signal-sandbox` console script
  - shared `src/signal_sandbox/observability.py:get_tracer()`
  - T01 unit/integration tests
- Validation after T01: 11 pytest passed; ruff check passed; ruff format check passed; pyright passed.
- Completed T02 CI Setup:
  - added `tests/unit/test_ci_workflow.py`
  - verified workflow trigger branches, Python 3.12, pip cache, CI command order, install command, and dev dependencies
  - added repository-root `.github/workflows/signal-analytics-sandbox-ci.yml` so GitHub can actually run this product's CI in the monorepo
  - validation after CI bridge: 18 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T03 Phase 1 Smoke Tests:
  - added `tests/unit/test_observability.py`
  - added structured JSON logger helpers in `src/signal_sandbox/observability.py`
  - extended `tests/integration/test_cli_smoke.py` with temp-workspace `status`
  - validation after T03/root CI bridge: 18 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 1 deep review completed and archived at `docs/archive/PHASE1_REVIEW.md`.
- `docs/audit/AUDIT_INDEX.md` has Cycle 1 / Phase 1 archive row.
- Completed T04 SourceManifest Pydantic Schema:
  - added `src/signal_sandbox/sources/manifest.py`
  - added `tests/unit/test_source_manifest.py`
  - validation after T04: 22 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T05 Capture Loader:
  - added `src/signal_sandbox/capture/loader.py`
  - added `src/signal_sandbox/sources/private_patterns.py`
  - added `tests/unit/test_capture_loader.py`
  - validation after T05: 26 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T06 SignalRecord Schema:
  - added `src/signal_sandbox/ledger/record.py`
  - added `tests/unit/test_signal_record.py`
  - validation after T06: 31 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 2 deep review completed and archived at `docs/archive/PHASE2_REVIEW.md`.
- `docs/audit/AUDIT_INDEX.md` has Cycle 2 / Phase 2 archive row.
- Completed T07 Ledger I/O (Parquet):
  - added `src/signal_sandbox/ledger/io.py`
  - added `tests/unit/test_ledger_io.py`
  - validation after T07: 35 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T08 Dedup + Ambiguity Flagging:
  - added `src/signal_sandbox/ledger/dedup.py`
  - added `tests/unit/test_dedup.py`
  - validation after T08: 38 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 3 deep review completed and archived at `docs/archive/PHASE3_REVIEW.md`.
- Accepted ADR-001: deterministic Parquet snapshot bytes with rows sorted by asset/timestamp, fixed columns, zstd compression, and statistics disabled.
- Completed T09 PriceDataProvider Abstract Interface:
  - added `src/signal_sandbox/prices/base.py`
  - added `tests/unit/test_price_provider_base.py`
  - validation after T09: 41 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T10 OperatorFilePriceProvider:
  - added `src/signal_sandbox/prices/operator_file.py`
  - added `tests/integration/test_operator_file_provider.py`
  - validation after T10: 44 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T11 PriceSnapshot Persistence + Provenance:
  - added `src/signal_sandbox/prices/snapshot.py`
  - added `tests/unit/test_snapshot_persistence.py`
  - validation after T11: 47 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 4 deep review completed and archived at `docs/archive/PHASE4_REVIEW.md`.
- Completed T12 Outcome Matching Engine:
  - added `src/signal_sandbox/outcomes/matcher.py`
  - added `src/signal_sandbox/outcomes/rule_registry.py`
  - added `tests/integration/test_outcome_matcher.py`
  - wrote `docs/audit/HEAVY_T12_EVIDENCE.md`
  - validation after T12: 55 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T13 Aggregator:
  - added `src/signal_sandbox/outcomes/aggregate.py`
  - added `tests/unit/test_aggregator.py`
  - validation after T13: 59 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T14 Markdown Report Generator:
  - added `src/signal_sandbox/reports/disclaimers.py`
  - added `src/signal_sandbox/reports/markdown.py`
  - added `tests/integration/test_report_generator.py`
  - wrote `docs/audit/HEAVY_T14_EVIDENCE.md`
  - validation after T14: 65 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 5 deep review completed and archived at `docs/archive/PHASE5_REVIEW.md`.
- Completed T15 ExtractionAdapter ABC:
  - added `src/signal_sandbox/extraction/base.py`
  - added `tests/unit/test_extraction_base.py`
  - validation after T15: 68 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T16 ManualExtractionAdapter:
  - added `src/signal_sandbox/extraction/manual.py`
  - added `tests/unit/test_manual_extraction.py`
  - validation after T16: 70 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T17 RuleExtractionAdapter:
  - added `src/signal_sandbox/extraction/rule.py`
  - added `src/signal_sandbox/extraction/rule_templates.py`
  - added `tests/unit/test_rule_extraction.py`
  - added `tests/unit/test_rule_templates.py`
  - validation after T17: 72 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 6 deep review completed and archived at `docs/archive/PHASE6_REVIEW.md`.
- Completed T18 ExchangePublicOHLCVProvider:
  - added `src/signal_sandbox/prices/exchange_public.py`
  - added `tests/integration/test_exchange_public_provider.py`
  - validation after T18: 75 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T19 YFinanceDevProvider:
  - added `src/signal_sandbox/prices/yfinance_dev.py`
  - added `tests/unit/test_yfinance_provider.py`
  - updated dependency manifests with `yfinance`
  - validation after T19: 77 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 7 deep review completed and archived at `docs/archive/PHASE7_REVIEW.md`.
- Completed T20 LLMExtractionAdapter:
  - added double activation gate: `SIGNAL_SANDBOX_ENABLE_LLM=1` plus
    `llm_approved=True`
  - added fixed-client LLM extraction with `llm/<provider>/<model>` adapter IDs
  - added paid Claude-style cost-cap enforcement and zero-cap disabling
  - added ledger rejection for unreviewed LLM-sourced records
  - added fixed eval acceptance-rate baseline coverage
  - validation after T20: 84 pytest passed; ruff check passed; ruff format
    check passed; pyright passed
- Heavy T20 evidence written to `docs/audit/HEAVY_T20_EVIDENCE.md`.
- Phase 8 deep review completed and archived at `docs/archive/PHASE8_REVIEW.md`.
- Current task graph is complete through T20.

## Technical Risks

1. Live Ollama and Claude provider calls are not exercised in CI by design; the
   T20 contract is covered through injected fixed clients and provider shells.
2. LLM eval baseline is a deterministic fixture baseline, not a production
   quality measure. Treat any real-source expansion as a new eval/update task.
3. Hook behavior has targeted coverage for high-risk governance checks, but not
   exhaustive branch coverage.

## Minimal Improvement Plan

1. Use the completed sandbox against the three approved Telegram pilot sources.
2. Add real capture fixtures and reviewer outcomes before changing the LLM eval
   baseline.
3. Keep LLM outputs in draft review until `reviewer_id` is set.

## Unresolved Follow-Up

- Phase 9 is now active in `docs/tasks.md`.
- Completed `SAS-PILOT-001: Pilot Scope` with
  `docs/pilot/PILOT_SCOPE.md`.
- Completed `SAS-PILOT-002: Methodology V0` with
  `docs/pilot/METHODOLOGY_V0.md`.
- Completed `SAS-PILOT-003: First Source Capture Plan And Log` with
  `docs/pilot/CAPTURE_LOG.md`; no real captures are present yet.
- Completed `SAS-PILOT-004: First Source Manual Extraction Log` with
  `docs/pilot/EXTRACTION_LOG.md`; extraction is blocked on operator-supplied
  public captures.
- Completed `SAS-PILOT-005: First Source Report V0` with
  `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md`; report is blocked on
  missing captures/extraction.
- Completed `SAS-PILOT-006: Customer Feedback And Payment Signal Log` with
  `docs/pilot/CUSTOMER_FEEDBACK.md` and `docs/pilot/PAYMENT_SIGNAL_LOG.md`;
  both are pending real customer/payment behavior.
- Completed `SAS-PILOT-007: Repeat Or Automate Decision` with
  `docs/pilot/PILOT_DECISION.md`.
- Current verdict: stop/defer automation until real public captures are supplied
  for `https://t.me/bablos79`.
- Phase 9 deep review/archive completed at `docs/archive/PHASE9_REVIEW.md`;
  latest report is `docs/audit/PHASE_REPORT_LATEST.md`.
- Operator requested parsing the public source. Captured 60 public text posts
  from unauthenticated `https://t.me/s/bablos79` pages into
  `workspace/captures/bablos79/`; manifest:
  `docs/pilot/bablos79_CAPTURE_MANIFEST.json`.
- Validated captures with `load_captures(Path("workspace"), "bablos79")` -> 60.
- Updated capture/extraction logs and D-014. Current verdict: continue manual
  extraction for these 60 captures; automation remains deferred.
- Created `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md` and Phase 10
  `SAS-AUTO-001`, `SAS-AUTO-001B`, and `SAS-AUTO-002..005` in `docs/tasks.md`
  for a machine-first draft extraction assistant.
- Added `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md` with phases A-M from
  data foundation through confidence-gated automation.
- Recorded D-015/D-016 and D-017; D-017 supersedes the seed-label-first start
  with machine-first pseudo-label bootstrap plus exception review.
- Recorded D-016: a frontier model may be used only offline to propose
  author-specific lexicon/profile candidates with evidence.
- Recorded D-018: orchestrator phase review/archive/doc update must advance to
  the next task and continue unless a concrete stop condition exists.
- Phase 10 completed:
  - `SAS-AUTO-001` created pseudo-labels for all 60 captures.
  - `SAS-AUTO-001B` created the author profile and lexicon draft.
  - `SAS-AUTO-002` added deterministic draft validation/parser helpers.
  - `SAS-AUTO-003` exported 60 review-pending draft rows.
  - `SAS-AUTO-004` created a 23-row review queue and separated draft vs final
    status counts.
  - `SAS-AUTO-005` recorded the eval/decision: keep draft helper for internal
    exception review only; no scope expansion.
  - Phase 10 deep review archived at `docs/archive/PHASE10_REVIEW.md`; Stop-Ship
    No; P0/P1/P2 all 0.
- At Phase 10 close, the next product action was human exception review of
  `docs/pilot/bablos79_REVIEW_QUEUE.md`; the 2026-05-09 roadmap update below
  supersedes the "no next engineering task" state.
- 2026-05-09: Planned the next stage as Author Market Intelligence:
  - Created `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`.
  - Appended Phases 11-19 and tasks `SAS-MI-001..018` to `docs/tasks.md`.
  - Updated `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`,
    `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`,
    `PHASE_HANDOFF.md`, and `MEMORY.md`.
  - Recorded D-019/D-020: Phase 10 remains the first channel profile/corpus
    seed; RAG/Planning/Agentic implementation requires `SAS-MI-001` ADR first.
  - Completed `SAS-MI-001: Author Market Intelligence Architecture ADR`:
    created `docs/adr/ADR-002-author-market-intelligence.md`, updated
    `docs/ARCHITECTURE.md`, and recorded D-021.
  - ADR-002 activates RAG for local cited context only and Agentic for a
    bounded internal batch analyst only; Tool-Use and Planning remain OFF;
    runtime remains T0; first retrieval substrate is local DuckDB plus local
    vector/index sidecar files.
  - Completed `SAS-MI-002: MarketIdea Schema And Metrics Contract`: created
    `docs/specs/MARKET_IDEA_SCHEMA.md` with field contract, enum values,
    evidence-span rules, deterministic horizons, review queue policy, examples,
    and SignalRecord compatibility.
  - Phase 11 deep review archived at `docs/archive/PHASE11_REVIEW.md` with
    Stop-Ship No and P0/P1/P2 all 0.
  - Completed `SAS-MI-003: Asset Universe And Alias Registry` with
    `src/signal_sandbox/assets/`, focused tests, and
    `docs/specs/ASSET_UNIVERSE.md`.
  - Completed `SAS-MI-004: Market Data Store Contract` with
    `src/signal_sandbox/market_data/`, focused tests, and
    `docs/specs/MARKET_DATA_STORE.md`.
  - Completed `SAS-MI-005: Deterministic Horizon Metrics` with
    `src/signal_sandbox/market_data/metrics.py` and focused tests.
  - Phase 12 deep review archived at `docs/archive/PHASE12_REVIEW.md` with
    Stop-Ship No and P0/P1/P2 all 0.
  - Completed `SAS-MI-006: SourceDocument Corpus Schema` with
    `src/signal_sandbox/corpus/`, focused tests, and
    `docs/specs/SOURCE_CORPUS.md`.
  - Completed `SAS-MI-007: Channel Profile Registry` with
    `src/signal_sandbox/profiles/`, focused tests, and
    `docs/specs/CHANNEL_PROFILES.md`.
  - Phase 13 deep review archived at `docs/archive/PHASE13_REVIEW.md` with
    Stop-Ship No and P0/P1/P2 all 0.
  - Completed `SAS-MI-008: Local Retrieval Store Prototype` with
    `src/signal_sandbox/retrieval/`, focused tests, and local DuckDB plus
    deterministic vector sidecars.
  - Completed `SAS-MI-009: Cited Retrieval API` with cited snippets, scores,
    source timestamps, evidence URLs, text hashes, and deterministic
    channel/time filters.
  - Phase 14 deep review archived at `docs/archive/PHASE14_REVIEW.md` with
    Stop-Ship No and P0/P1/P2 all 0.
  - Completed `SAS-MI-010: MarketIdea Draft Extractor` with
    `src/signal_sandbox/market_ideas/`, focused tests, all required idea
    categories, preserved evidence spans, and unapproved review-pending drafts.
  - Completed `SAS-MI-011: MarketIdea Batch Draft Export` with one row per
    source document, separate draft/final review states, queue reasons,
    candidate assets, horizons, and no approved ledger/outcome/report writes.
  - Phase 15 deep review archived at `docs/archive/PHASE15_REVIEW.md` with
    Stop-Ship No and P0/P1/P2 all 0.
  - Completed `SAS-MI-012: MarketIdea Outcome Evaluator` with asset resolution,
    unresolved/ambiguous preservation, deterministic horizon metrics, and
    required outcome provenance.
  - Completed `SAS-MI-013: Author Metrics Aggregator` with counts by type,
    asset type, horizon status, review status, directional hit rate limited to
    evaluable directional outcomes, and separate null/non-market rate.
  - Phase 16 deep review archived at `docs/archive/PHASE16_REVIEW.md` with
    Stop-Ship No and P0/P1/P2 all 0.
  - Completed `SAS-MI-014: Batch Analyst Contract` with fixed allowed
    operations, max iterations, retrieval cap, cost cap, stop reasons, and audit
    checksums; no shell/network/broker/report publisher surface was added.
  - Next task is `SAS-MI-015: Internal Analyst Memo Export`.
- The three pilot sources are customer/potential-customer provided and should
  be handled through the Phase 9 validation loop before any additional
  automation.
- Do not build bot/SaaS/private scraping/copy trading/broker/public leaderboard
  expansion. Do not implement retrieval, embeddings, market-data expansion, or
  batch-agent code outside the active scoped task.
