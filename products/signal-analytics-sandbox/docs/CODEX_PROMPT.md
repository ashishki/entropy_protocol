# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 2.68
Date: 2026-05-15
Phase: 22

This file is compact session state. Detailed history belongs in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Phase 0 Gate Status

Engineering Phase 1 (T01+) may begin because both rows below are marked
`acknowledged` by the operator.

| Gate | Status | Evidence | Acknowledged date |
|------|--------|----------|-------------------|
| SAS-001: Paid Pilot Demand Validation | acknowledged | `docs/PILOT_LOG.md` | 2026-05-07 |
| SAS-002: Public-Source Legal/Terms Memo | acknowledged | `docs/legal_risk_memo.md` | 2026-05-07 |

Initial pilot sources acknowledged on 2026-05-07:
`https://t.me/bablos79`, `https://t.me/nemphiscrypts`,
`https://t.me/pifagortrade`.

## Current State

- Phase: 22 (Expanded Public Corpus)
- Baseline: 166 passing tests, 0 skipped
- Ruff: `ruff check src/ tests/` passes
- Pyright: `pyright` passes
- Last CI run: local CI-equivalent commands pass; GitHub run not yet observed
- Last updated: 2026-05-15
- Current priority: expand the `bablos79` public corpus for a deep channel
  retrospective with image/OCR, reviewed claim ledger, market outcomes, and
  balanced author capability report

## Read First

1. `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`
2. `docs/tasks.md` Phase 22, SAS-DR-001..005
3. `docs/ARTIFACT_VALIDATION_ROADMAP.md`
4. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
5. `docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md`
6. task-specific `Context-Refs` in `docs/tasks.md`

Other useful links:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/legal_risk_memo.md`
- `docs/PILOT_LOG.md`
- `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`
- `docs/pilot/MEDIA_MODALITY_DEVELOPMENT_PLAN.md`
- `docs/archive/PHASE20_REVIEW.md`

## Next Task

SAS-DR-001 Deep Retrospective Scope Lock

Immediate intent:

- do not over-polish the narrow Phase 21 report;
- lock a larger public `bablos79` source/window before outcome analysis;
- define anti-cherry-pick selection rules;
- keep external delivery blocked until a later ready gate passes.

## Active Guardrails

- Public/operator-authorized sources only.
- No private Telegram groups or access-control bypass.
- No paid X/Twitter dependency before Telegram/public-source artifact
  validation.
- Media evidence remains internal-only until transcript/OCR is human-reviewed.
- No marketplace, leaderboard, investment advice, or future-profit claims.
- Core is paused; do not open Core work from this product loop.
- The deep retrospective must retain strong examples, weak examples,
  non-measurable claims, and counterexamples.

## Evaluation State

### Last Evaluation

- Task: SAS-LIVE-006 - Reviewed Multimodal Source Join
- Date: 2026-05-14
- Eval Source: `.venv/bin/python -m pytest tests/unit/test_multimodal_source_join.py -q`, run 2026-05-14
- Artifact: `docs/retrieval_eval.md`
- Primary metric: source-join preservation pass rate
- Result: PASS, 100%

### Regression Thresholds

- P0: primary metric drop > 15% from baseline
- P1: primary metric drop > 5% from baseline

## Fix Queue

Empty.

## Open Findings

Open findings are product-gate blockers for external delivery of the current
source/window, not implementation stop-ship findings.

| ID | Severity | Summary | Canonical artifact |
|----|----------|---------|--------------------|
| P21-E02 | P1 | Two transcript refs are LLM-reviewed usable for internal source join; zero refs are human/operator accepted for external delivery. | `docs/audit/PHASE21_ERROR_REGISTER.md` |
| P21-E03 | P1 | Internal media-backed report has 3 LLM-reviewed broad-market claims but zero deterministic outcome-ready rows. | `docs/audit/PHASE21_ERROR_REGISTER.md` |
| P21-E04 | P2 | The exact follow-up video promised by `bablos79-10465` was not identified in the public window. | `docs/audit/PHASE21_ERROR_REGISTER.md` |

## Historical Pointers

- Phase 20 completed through SAS-MEDIA-008; details are in
  `docs/archive/PHASE20_REVIEW.md`, `docs/pilot/MEDIA_MODALITY_DECISION.md`,
  and `docs/pilot/bablos79_MULTIMODAL_COVERAGE_PACK.md`.
- Phase 21 scope is locked to `https://t.me/bablos79`, the existing
  2026-04-27..2026-05-06 public text capture window, and a text-only
  Russian-first public-source report boundary in
  `docs/ARTIFACT_VALIDATION_ROADMAP.md#sas-af-001-scope-lock-note`.
- Phase 21 capture pack is generated at `docs/pilot/bablos79_CAPTURE_PACK.md`
  and `docs/pilot/bablos79_CAPTURE_PACK.json` from 60 public text captures plus
  validated pseudo-labels: 50 `not_a_signal`, 7 `insufficient_fields`, and
  3 `needs_review`.
- Phase 21 review queue is closed at
  `docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.md` and
  `docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.json`: 50
  `rejected_not_market_related`, 7 `insufficient_evidence`, 3
  `ambiguous_needs_operator_review`, and 0 customer-report-eligible rows.
- Phase 21 outcome prep is at `docs/pilot/bablos79_OUTCOME_PREP.md` and
  `docs/pilot/bablos79_OUTCOME_PREP.json`: 0 market-data fetches, 0 outcome
  metrics, 50 not-applicable rows, 7 insufficient-evidence rows, and 3
  operator-review-required rows.
- Phase 21 report draft is at
  `docs/pilot/reports/bablos79_SIGNAL_REPORT_V1.md`.
- The text-only report is not the final target. It proved that real media
  acquisition was required before claiming audio/image analysis. The completed
  media route still rejects external delivery because no reviewed usable media
  refs exist.
- `SAS-LIVE-001` completed on 2026-05-14 at
  `docs/pilot/bablos79_REAL_MEDIA_INTAKE.md`.
- `SAS-LIVE-002..SAS-AF-008` completed on 2026-05-14. Two public voice files
  were acquired, but no transcript provider was configured, zero reviewed usable
  media refs exist, and the ready gate rejects this source/window for external
  delivery.
- Phase 21 deep review is archived at `docs/archive/PHASE21_REVIEW.md`.
- Phase 22 follows `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`.
- Current next task is `SAS-DR-001` in `docs/tasks.md`.
- Managed Whisper wiring was added on 2026-05-15 using the previously discussed
  `Dream_Motif_Interpreter` provider pattern. `signal-sandbox transcribe-media`
  produced two draft transcript artifacts under `docs/pilot/transcripts/`.
- LLM review was added on 2026-05-15 at
  `docs/pilot/bablos79_TRANSCRIPT_LLM_REVIEW.md`: OpenAI `gpt-4.1` marked both
  transcript refs usable for internal source join and extracted 3 media-backed
  broad-market claims. The internal report is
  `docs/pilot/reports/bablos79_MEDIA_BACKED_REPORT_V2_LLM_REVIEWED.md`.
- Latest validation: 166 passing tests, 0 skipped; ruff and pyright pass.
- Phase 19 review coverage details are in
  `docs/pilot/bablos79_REVIEW_COVERAGE_PACK.md`.
- Earlier phase history is in `docs/IMPLEMENTATION_JOURNAL.md`,
  `AGENT_NOTES.md`, and `docs/archive/`.

## Maintenance Rule

At every phase boundary update only:

- current phase;
- baseline and validation status;
- next task;
- open findings;
- links if canonical docs move.

Do not append long closeout digests here.
