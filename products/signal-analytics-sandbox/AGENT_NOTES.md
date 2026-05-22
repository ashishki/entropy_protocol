# Agent Notes - Signal Analytics Sandbox

Date: 2026-05-22

Restart-relevant state only. Historical detail lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Active State

- Phase: 36 Channel Impact Framework And Cross-Channel Completion
- Active task: Phase 36 complete; await operator decision
- Baseline: 326 pass / 0 skip
- External gate: `approve_internal_only`
- External delivery: not approved
- Core: paused

## Current Decision

Internal V1 channel utility validation is complete for three channels. Phase 36
now defines broader channel impact criteria and an equal evidence-completion
loop for `bablos79`, `nemphiscrypts`, and `pifagortrade`.

## Next Action

`SAS-IMPACT-001..002` created the impact framework and three-channel loop.
`SAS-BABLOS-001..008` closed the `bablos79` Phase 36 pass as internal-only:
0 human/operator accepted transcripts, 0 OCR drafts, 0 accepted media claims,
0 computed outcomes, external delivery rejected. `SAS-IMPACT-003..004` added
equivalent completion scopes for `nemphiscrypts` and `pifagortrade`.
`SAS-IMPACT-005..008` added taxonomy, dashboard schema, paid boundary,
scorecard, external gate, and deep review.
Two-month run `2026-03-22..2026-05-22` produced 526 text rows,
37 normalized claims, 28 7d evaluable, 19 confirmed, 9 contradicted.
Operator then clarified this was insufficient because the real question is
multimodal extraction and setup/RR quality, not post counts. A new two-month
multimodal pass now covers 570 public posts, 295 media refs, 70 voice
transcripts, 185 image/OCR drafts, 40 video/manual blockers, and 1 internal
RR-ready setup draft.
Model-reviewer pass now adds `gpt-4.1-mini` mass review over 255 media drafts
and `gpt-4.1` arbiter review over 35 high-signal rows; 9 arbiter candidates
are accepted for internal follow-up only.

Read first:

1. `docs/CODEX_PROMPT.md`
2. `docs/AI_DEVELOPMENT_PLAN_RU.md`
3. `docs/tasks.md` Phase 36
4. `docs/specs/CHANNEL_IMPACT_FRAMEWORK.md`
5. `docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md`
6. `docs/pilot/three_channel_PHASE36_IMPACT_SCORECARD.md`
7. `docs/pilot/three_channel_PHASE36_EXTERNAL_READY_GATE.md`
8. `docs/pilot/three_channel_2M_RUN_SUMMARY.md`
9. `docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md`
10. `docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json`
11. `docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`

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
- Two-month multimodal research:
  `docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md`
- Media reviewer pass:
  `docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`
- Phase 36 development loop:
  `docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md`
- Phase 36 bablos gate:
  `docs/pilot/bablos79_PHASE36_EXTERNAL_READY_GATE.md`
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
