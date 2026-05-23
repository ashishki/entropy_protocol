# Agent Notes - Signal Analytics Sandbox

Date: 2026-05-23

Restart-relevant state only. Historical detail lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Active State

- Phase: 37 Pre-Client Artifact Hardening
- Active task: `SAS-PRECLIENT-010`
- Baseline: 359 pass / 0 skip
- External gate: `approve_internal_only`
- External delivery: not approved
- Core: paused

## Current Decision

Internal V1 and Phase 36 validation are complete for three channels. Phase 37
turns current evidence into reliable pre-client artifacts before outreach.

## Next Action

`SAS-IMPACT-001..008` completed the Phase 36 framework, scorecard, paid
boundary, and gate. External delivery remains blocked/internal-only.
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
`SAS-PRECLIENT-001..009` are complete: contract, packet, appendix, cards,
reports, demo, candidate outcomes, static internal dashboard prototype, and
artifact safety gate. The gate found 0 forbidden phrase findings but keeps all
buyer conversations on hold until Phase 37 deep review.
Next task is `SAS-PRECLIENT-010` Phase 37 deep review and client-readiness
decision.

Read first:

1. `docs/CODEX_PROMPT.md`
2. `docs/tasks.md` Phase 37
3. `docs/AI_DEVELOPMENT_PLAN_RU.md`
4. `docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md`
5. `docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`
6. `docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md`
7. `docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md`
8. `docs/pilot/preclient_EVIDENCE_APPENDIX.md`, `docs/pilot/reports/preclient/`

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
- Pre-client artifacts:
  `docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md`,
  `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`,
  `docs/pilot/preclient_EVIDENCE_APPENDIX.md`,
  `docs/pilot/preclient_FREE_DASHBOARD_CARDS.md`,
  `docs/pilot/preclient_CANDIDATE_OUTCOMES.md`,
  `docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md`,
  `docs/pilot/preclient_dashboard/index.html`,
  `docs/pilot/reports/preclient/`
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
