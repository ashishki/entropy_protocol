# Agent Notes - Signal Analytics Sandbox

Date: 2026-05-22

Restart-relevant state only. Historical detail lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Active State

- Phase: 36 bablos79 Corpus Completion And Media Recovery
- Active task: SAS-BABLOS-003 Media Linkage Queue
- Baseline: 295 pass / 0 skip
- External gate: `approve_internal_only`
- External delivery: not approved
- Core: paused

## Current Decision

Internal V1 channel utility validation is complete for three channels. Phase 36
is active because `bablos79` should not be presented as a full 90-day
text/audio/image retrospective: current validated coverage is only 60 text
captures over about 9 days, 2 internal-only audio refs, 0 source-linked
image/OCR artifacts, and too few deterministic claims.

## Next Action

`SAS-BABLOS-001..002` created the Phase 36 scope and public text recapture
plan. Continue with `SAS-BABLOS-003`: media linkage queue.

Read first:

1. `docs/CODEX_PROMPT.md`
2. `docs/AI_DEVELOPMENT_PLAN_RU.md`
3. `docs/tasks.md` Phase 36
4. `docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md`
5. `docs/pilot/bablos79_PHASE36_TEXT_RECAPTURE_PLAN.md`
6. `docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md`

## Canonical Links

- V1 report:
  `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`
- V1 gate:
  `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`
- Phase 27 review:
  `docs/archive/PHASE27_REVIEW.md`
- Follow-on plan:
  `docs/AI_DEVELOPMENT_PLAN_RU.md`
- Phase 36 scope:
  `docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md`
- State compaction archive:
  `docs/archive/POST_V1_STATE_COMPACTION_2026-05-19.md`

## Guardrails

- Public/operator-authorized sources only.
- No private scraping, access-control bypass, advice, future-profit claims, or
  leaderboard/marketplace framing.
- Unsupported providers/proxies are exclusions, not wins/losses.
- Unreviewed transcript/OCR/chart claims stay out of customer-facing metrics.
- Do not describe `bablos79` as full 90-day multimodal coverage until Phase 36
  closes evidence gaps.
