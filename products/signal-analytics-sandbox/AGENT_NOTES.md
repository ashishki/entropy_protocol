# Agent Notes - Signal Analytics Sandbox

Date: 2026-05-22

Restart-relevant state only. Historical detail lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Active State

- Phase: 36 Channel Impact Framework And Cross-Channel Completion
- Active task: SAS-BABLOS-004 Transcript Acceptance Pass
- Baseline: 306 pass / 0 skip
- External gate: `approve_internal_only`
- External delivery: not approved
- Core: paused

## Current Decision

Internal V1 channel utility validation is complete for three channels. Phase 36
now defines broader channel impact criteria and an equal evidence-completion
loop for `bablos79`, `nemphiscrypts`, and `pifagortrade`.

## Next Action

`SAS-IMPACT-001..002` created the impact framework and three-channel loop.
`SAS-BABLOS-001..003` created the first per-channel recovery path and media
queue. Continue with `SAS-BABLOS-004`: accept/reject/needs_context the two
linked public voice transcripts. Keep OCR blocked until source-linked
image/chart artifacts exist.

Read first:

1. `docs/CODEX_PROMPT.md`
2. `docs/AI_DEVELOPMENT_PLAN_RU.md`
3. `docs/tasks.md` Phase 36
4. `docs/specs/CHANNEL_IMPACT_FRAMEWORK.md`
5. `docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md`
6. `docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md`
7. `docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.md`

## Canonical Links

- V1 report:
  `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`
- V1 gate:
  `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`
- Phase 27 review:
  `docs/archive/PHASE27_REVIEW.md`
- Follow-on plan:
  `docs/AI_DEVELOPMENT_PLAN_RU.md`
- Phase 36 impact framework:
  `docs/specs/CHANNEL_IMPACT_FRAMEWORK.md`
- Phase 36 development loop:
  `docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md`
- Phase 36 media queue:
  `docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.md`
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
