# 15-Minute Demo Script

Date: 2026-05-19
Status: internal_only_demo_script
Gate: `approve_internal_only`

## Demo Boundary

This script is for internal discovery calls and controlled buyer interviews.
It must not be used as investment advice, a trading recommendation, a public
performance claim, or an externally approved report.

## 0:00-1:30 - Opening

Say:

"We help turn public market commentary into an evidence-backed research audit:
what was said, what could be normalized, what could be checked, what was
excluded, and how strong the evidence is."

Clarify:

- Current demo is internal-only.
- Current external gate is `approve_internal_only`.
- The goal of the call is to learn whether this audit would support a real
  internal decision.

## 1:30-3:30 - Buyer Pain

Say:

"Public trading channels create a lot of claims, but manual review is slow.
The hard part is not collecting posts; it is preserving evidence, normalizing
claims without assumptions, checking market outcomes where possible, and
showing exclusions honestly."

Ask:

- "Which public sources did your team manually check recently?"
- "What decision depended on that check?"
- "What made the review hard to trust?"

## 3:30-6:00 - Method Walkthrough

Show:

- public source capture;
- structured claim extraction;
- human review queue;
- provider/proxy approval;
- deterministic outcome computation;
- evidence appendix;
- language and external-ready gates.

Say:

"Unsupported rows do not become losses. They remain exclusions with reasons.
Unreviewed transcript, OCR, image, and chart evidence stays out of metrics."

## 6:00-9:00 - Three-Channel Internal Result

Show:

- `docs/pilot/three_channel_V2_SCORECARD.md`
- `docs/pilot/three_channel_V2_METRIC_RESULTS.json`
- `docs/pilot/three_channel_V2_ROBUSTNESS_APPENDIX.md`

Say:

"In this internal run, the system found 170 V2 evaluable text claims across
three channels. It also recorded provider gaps, review gaps, sparse setup/RR
coverage, and media blockers. The value is the audit trail, not a single
composite score."

Do not say:

- any channel is recommended;
- any channel is externally validated;
- any result predicts future performance;
- any unreviewed media claim is accepted.

## 9:00-11:00 - Limitations

Say:

"This is not externally deliverable yet. The current blocker list includes
review coverage, provider gaps, sparse setup/RR coverage, benchmark robustness,
and media acceptance."

Show:

- `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`
- `docs/pilot/three_channel_V2_MEDIA_INVENTORY.md`
- `docs/pilot/three_channel_TRANSCRIPT_REVIEW.md`

## 11:00-13:00 - Pilot Shape

Say:

"A useful pilot would use one fixed public source list, one fixed historical
window, and one decision the report should support. The deliverable would be an
internal research audit with evidence links, exclusions, and reproducibility
notes."

Ask:

- "Which source list would be worth auditing first?"
- "What time window would be fair?"
- "What exclusion would make the report unusable?"
- "Who would need to trust the output internally?"

## 13:00-15:00 - Close

Say:

"The next step is not scaling. The next step is one bounded pilot where we test
whether this saves review time or improves confidence in a real internal
decision."

Close with:

- confirm the source list owner;
- confirm the historical window;
- confirm the decision the report should support;
- confirm whether a paid bounded audit is worth discussing after review of the
  internal-only demo pack.

## Required Guardrails

- Do not provide buy, sell, hold, long, or short instructions.
- Do not promise future profit, performance, or accuracy.
- Do not describe the output as externally approved.
- Do not include unreviewed media-backed claims.
- Do not convert the three-channel comparison into a public source ordering.
