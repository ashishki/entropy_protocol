# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 2.59
Date: 2026-05-11
Phase: 21

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

- Phase: 21 (Artifact-First Real Public-Source Report Validation)
- Baseline: 157 passing tests, 0 skipped
- Ruff: `ruff check src/ tests/` passes
- Pyright: `pyright` passes
- Last CI run: local CI-equivalent commands pass; GitHub run not yet observed
- Last updated: 2026-05-11
- Current priority: one real public-source report artifact, manually validated

## Read First

1. `docs/ARTIFACT_VALIDATION_ROADMAP.md`
2. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
3. `docs/tasks.md` Phase 21, SAS-AF-001..008
4. task-specific `Context-Refs` in `docs/tasks.md`

Other useful links:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/legal_risk_memo.md`
- `docs/PILOT_LOG.md`
- `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`
- `docs/pilot/MEDIA_MODALITY_DEVELOPMENT_PLAN.md`
- `docs/archive/PHASE20_REVIEW.md`

## Next Task

SAS-AF-001 - Channel And Report Scope Lock

Use `docs/tasks.md#sas-af-001-channel-and-report-scope-lock` as the source of
truth for acceptance criteria and file scope.

Immediate intent:

- select or confirm the first real public channel/source;
- define report type, period, capture method, language, media scope, and claim
  boundary;
- if no source/channel is selected, record the operator-input blocker and stop;
- do not add generic extraction features before scope is locked.

## Active Guardrails

- Public/operator-authorized sources only.
- No private Telegram groups or access-control bypass.
- No paid X/Twitter dependency before Telegram/public-source artifact
  validation.
- Media evidence remains internal-only until transcript/OCR is human-reviewed.
- No marketplace, leaderboard, investment advice, or future-profit claims.

## Historical Pointers

- Phase 20 completed through SAS-MEDIA-008; details are in
  `docs/archive/PHASE20_REVIEW.md`, `docs/pilot/MEDIA_MODALITY_DECISION.md`,
  and `docs/pilot/bablos79_MULTIMODAL_COVERAGE_PACK.md`.
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
