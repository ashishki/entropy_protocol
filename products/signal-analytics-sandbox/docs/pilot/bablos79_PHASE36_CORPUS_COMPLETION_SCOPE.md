# Phase 36 Scope - bablos79 Corpus Completion And Media Recovery

Date: 2026-05-22
Status: scope_complete_text_recapture_plan_started
Owner: codex + operator

## Why This Phase Exists

The current `bablos79` retrospective should not be described as a long-period
text/audio/image analysis. The locked window was 90 calendar days, but the
validated local seed corpus only covers `2026-04-27` through `2026-05-06`.

Current evidence state:

| Area | Current result | Product meaning |
|---|---:|---|
| Locked window | 90 days | Target period, not fully captured. |
| Validated text captures | 60 | Seed corpus only. |
| Actual text coverage | about 9 days | Partial coverage, not full retrospective. |
| Source-linked audio rows | 2 | Transcribed/LLM-reviewed internal only. |
| Transcript-derived claims | 3 | Broad macro/event claims, not deterministic signals. |
| Source-linked image/chart artifacts | 0 | OCR did not run. |
| Reviewable non-blocker claim rows | 14 | Below 30-50 target. |
| Deterministic outcome-ready rows | 0 in deep `bablos79` ledger | No strict per-author outcome metrics yet. |

This phase converts the limitation into a concrete recovery plan.

## Phase Goal

Build a fuller `bablos79` evidence corpus before judging author capability:

1. Fill or explicitly close missing public-source periods inside the 90-day
   window.
2. Resolve missing Telegram message IDs and classify unavailable/deleted/media
   rows.
3. Link image/chart artifacts to exact source documents before OCR.
4. Human/operator-review audio transcripts before they can create
   customer-facing claims.
5. Re-extract claims from text, accepted transcripts, and accepted OCR.
6. Recompute market outcomes only for rows with enough deterministic fields and
   approved provider/proxy mapping.

## Non-Negotiable Boundaries

- Public/operator-authorized sources only.
- No private Telegram scraping or access-control bypass.
- Missing source rows are not weak evidence against the author.
- OCR/vision output is draft evidence until human/operator accepted.
- Audio transcripts are internal-only until human/operator accepted.
- Chart interpretation is manual-review-only; machine OCR may recover visible
  text but cannot infer entries, stops, targets, support, resistance, or trend
  by itself.
- Provider gaps are exclusions, not losses.
- No customer-facing report until the external-ready gate is rerun.

## Task Plan

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-BABLOS-001 | Corpus completion scope and gap plan | this file | Current coverage, blockers, source rules, and stop conditions are explicit. |
| SAS-BABLOS-002 | Public text recapture plan | `docs/pilot/bablos79_PHASE36_TEXT_RECAPTURE_PLAN.md` | Missing periods and message IDs have capture commands, source URLs, or unavailable classifications. |
| SAS-BABLOS-003 | Media linkage queue | `docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.md/json` | Every image/chart/audio candidate has source URL, capture ID, source document ID, checksum/file ref, or explicit blocker. |
| SAS-BABLOS-004 | Audio transcript acceptance pass | transcript review artifact | Each transcript is accepted/rejected/needs_context by human/operator before external use. |
| SAS-BABLOS-005 | OCR/vision draft pass | OCR artifact | OCR runs only on source-linked images/charts; output remains draft pending review. |
| SAS-BABLOS-006 | Multimodal claim recompute | claim ledger update | Text + accepted transcript + accepted OCR claims are normalized with review state. |
| SAS-BABLOS-007 | Proxy and outcome recompute | outcome artifacts | Only deterministic rows with approved proxy/provider produce market metrics. |
| SAS-BABLOS-008 | Phase 36 external gate | gate artifact | Gate decides external-ready / internal-only / rejected with exact blockers. |

## Started Work

SAS-BABLOS-001 is complete by creating this scope. SAS-BABLOS-002 has started
with `docs/pilot/bablos79_PHASE36_TEXT_RECAPTURE_PLAN.md`.

No new network capture, OCR, transcription, market-data fetch, or metric
recompute has run in this task.

## Immediate Next Step

Execute or operator-review the text recapture plan for:

- `gap-001-pre-seed-window`: `2026-02-15T00:00:00+00:00` through
  `2026-04-27T07:12:22+00:00`;
- `gap-002-post-seed-window`: `2026-05-06T06:57:32+00:00` through
  `2026-05-15T23:59:59+00:00`;
- missing message IDs inside the seed capture:
  `10462`, `10473`, `10474`, `10480`, `10481`, `10484`, `10494`.

The plan makes it clear which rows can be obtained from public Telegram `/s/`
pages, which require operator-supplied public media files, and which remain
unavailable. The next implementation artifact should be the recapture output or
the media linkage queue.

Current media shorthand: `0 source-linked image/OCR artifacts`; therefore no
OCR-derived claim is eligible yet.

Current signal shorthand: `14 reviewable non-blocker rows` and
`0 deterministic deep-ledger outcome-ready rows`; therefore a stronger
author-capability report must wait for recapture, media linkage, review, and
proxy/outcome recompute.
