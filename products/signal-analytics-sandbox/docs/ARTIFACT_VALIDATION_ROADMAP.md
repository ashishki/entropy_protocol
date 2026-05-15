# Signal Analytics Sandbox Artifact Validation Roadmap

Status: Phase 21 archived; superseded for active routing by
`docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`
Date: 2026-05-15

This file gives strategic routing only. Detailed acceptance criteria and file
scope live in `docs/tasks.md` Phase 21. The active post-text-only route is
`SAS-LIVE-001..009`, followed by `SAS-AF-006..008`.

As of 2026-05-15, Phase 21 is archived and the current narrow `bablos79`
source/window remains rejected for external delivery. The active route is now
the deeper retrospective in `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`.

## Goal

Produce one real public-source research/report artifact, manually validate the
evidence, and decide whether it is ready for controlled external pilot use.

## Active Phase

| Task | Purpose | Output |
|---|---|---|
| SAS-AF-001 | Lock channel/source and report scope. | Source/report/legal/claim scope note. |
| SAS-AF-002 | Build public capture pack. | Source manifest, capture log, corpus preview. |
| SAS-AF-003 | Close human review queue. | Reviewed rows and ambiguity register. |
| SAS-AF-004 | Prepare market data/outcomes. | Asset mapping, snapshot refs, unresolved outcomes. |
| SAS-AF-005 | Generate first real source report. | Report, evidence appendix, limitations. |
| SAS-LIVE-001 | Lock exact real media evidence items. | Real media intake plan. |
| SAS-LIVE-002 | Acquire/register public media artifacts. | Media manifest and acquisition log. |
| SAS-LIVE-003 | Transcribe acquired voice/audio. | Draft transcript run log. |
| SAS-LIVE-004 | OCR acquired images/screenshots. | Draft OCR run log. |
| SAS-LIVE-005 | Human-review transcript/OCR output. | Media review notes and usable refs. |
| SAS-LIVE-006 | Join reviewed media into source context. | Multimodal source preview. |
| SAS-LIVE-007 | Re-run extraction/review with media context. | Multimodal review queue. |
| SAS-LIVE-008 | Prepare multimodal outcomes. | Multimodal outcome prep register. |
| SAS-LIVE-009 | Generate media-backed report. | Media-backed report V1. |
| SAS-AF-006 | Manually validate evidence. | Validation notes and error register. |
| SAS-AF-007 | Polish report/demo pack. | Internal demo pack and talk track. |
| SAS-AF-008 | Decide external pilot readiness. | Ready/needs-fix/reject decision and paid pilot scope. |

## Required Artifacts

- source/report scope note;
- public source manifest;
- capture pack;
- real media intake plan;
- media acquisition log and manifest;
- transcript and OCR draft run logs;
- media evidence review notes;
- multimodal source preview;
- reviewed extraction export;
- outcome-prep summary where supported;
- report artifact;
- manual validation notes;
- error register;
- external-safe demo excerpts;
- ready-gate review.

## Guardrails

- public/operator-authorized sources only;
- no private Telegram groups;
- no access-control bypass;
- no paid X/Twitter dependency before public-source artifact validation;
- no customer-facing media claims until transcript/OCR evidence is human-reviewed;
- no marketplace, leaderboard, or future-profit claim.

## SAS-AF-001 Scope Lock Note

Status: locked from current operator-approved pilot files on 2026-05-12.

### Source And Report Scope

| Field | Locked value |
|---|---|
| Source URL | `https://t.me/bablos79` |
| Source ID | `bablos79` |
| Source class | `telegram_public` |
| Public-only status | approved in `docs/legal_risk_memo.md` |
| Period | existing bounded capture window: `2026-04-27T07:12:22+00:00` through `2026-05-06T06:57:32+00:00` |
| Capture method | operator/public unauthenticated Telegram `/s/` HTML capture already stored under `workspace/captures/bablos79/` |
| Report type | bounded public-source author/source research report with evidence coverage, reviewed market ideas/signals, deterministic outcomes where supported, and limitations |
| Source language | Russian |
| Report language | Russian-first pilot report; English internal summaries are allowed only as operator notes |
| Media scope | out of scope for the first customer-safe artifact unless human-reviewed media evidence is later supplied |
| Outcome horizon | deterministic historical horizons only where evidence supports them; default candidate horizons remain 1d, 3d, 7d, and 30d from existing market-idea work |

Selection basis: `bablos79` is the already approved first pilot source in
`docs/pilot/PILOT_SCOPE.md`, has 60 existing public text captures, and avoids
cherry-picking a new source for the first artifact-first validation run.

### Claim Boundary

Allowed claims:

- source/corpus coverage counts from captured public evidence;
- reviewed market-idea or signal counts by status;
- historical deterministic outcomes only for rows with reviewed evidence,
  asset/time/direction support, and valid market-data snapshots;
- ambiguity, insufficiency, unresolved-outcome, and media-coverage limitations;
- source behavior observations tied to cited public evidence.

Blocked claims:

- investment advice or buy/sell/hold recommendations;
- future-profit, expected-return, or predictive-performance claims;
- private-source, paywalled, login-walled, or access-bypass claims;
- marketplace, leaderboard, or "best channel" rankings;
- customer-facing claims based on unreviewed transcript, OCR, image, or voice
  evidence;
- claims based on draft extraction rows that have not passed human review.

### Source Selection Decision

Existing `bablos79` text captures are sufficient to begin `SAS-AF-002` public
capture-pack registration. They are not yet sufficient for a customer-facing
report until human review closes the queue and the report records every
limitation. No fresh capture is required for the first text-only scope unless
the operator explicitly expands the period or adds reviewed media.

## SAS-AF-002 Capture Pack

Status: generated on 2026-05-12.

Artifacts:

- `docs/pilot/bablos79_CAPTURE_PACK.md`
- `docs/pilot/bablos79_CAPTURE_PACK.json`

The pack joins 60 existing public text captures from `workspace/captures/bablos79/`
with validated pseudo-labels from
`workspace/extraction/bablos79_pseudo_labels.jsonl`. Every pseudo-label evidence
span is validated against the corresponding raw capture text before it appears
in the pack.

Summary:

- captured rows: 60;
- source timestamp range: `2026-04-27T07:12:22+00:00` through
  `2026-05-06T06:57:32+00:00`;
- capture method: `public_telegram_s_html`;
- media status: text-only, no local media/transcript/OCR artifacts;
- pseudo-label statuses: 50 `not_a_signal`, 7 `insufficient_fields`,
  3 `needs_review`;
- approved ledger rows created: 0;
- customer-facing claims created: 0.

Limitations before extraction/reporting:

- no media-backed rows are available;
- no row is an approved ledger record yet;
- rows with missing entry, stop, target, direction, or asset fields remain
  ineligible for deterministic outcome metrics until the review queue closes;
- final operator evaluation is still required before external delivery.

## SAS-AF-003 Review Queue Closure

Status: generated on 2026-05-12.

Artifacts:

- `docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.md`
- `docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.json`

The queue closure uses `docs/pilot/bablos79_CAPTURE_PACK.json` as input and
maps validated pseudo-label statuses into report-input categories. It treats the
LLM/pseudo-label result as valid draft classification for operator evaluation,
but it does not approve ledgers, compute outcomes, or create customer-facing
claims.

Summary:

- rows reviewed: 60;
- `rejected_not_market_related`: 50;
- `insufficient_evidence`: 7;
- `ambiguous_needs_operator_review`: 3;
- customer-report-eligible rows: 0;
- approved ledger rows created: 0;
- customer-facing claims created: 0.

Outcome implication:

The current text-only batch is strong evidence that this capture window does
not contain complete report-eligible trade setup rows under the current
pseudo-label result. `SAS-AF-004` should therefore produce an unresolved outcome
register and avoid market-data fetches unless the operator reclassifies rows as
complete measurable candidates.

## SAS-AF-004 Outcome Prep

Status: generated on 2026-05-12.

Artifacts:

- `docs/pilot/bablos79_OUTCOME_PREP.md`
- `docs/pilot/bablos79_OUTCOME_PREP.json`

Summary:

- rows assessed: 60;
- market-data fetches required now: 0;
- deterministic outcome metrics computed: 0;
- `not_applicable_not_market_related`: 50;
- `unresolved_insufficient_evidence`: 7;
- `unresolved_operator_review_required`: 3.

Outcome language boundary:

Current unresolved rows are limitations, not failed trades. No market snapshot
is fetched and no historical outcome metric is computed until a row has complete
measurable fields and final operator evaluation.

## SAS-AF-005 First Real Source Report V1

Status: generated on 2026-05-12.

Artifact:

- `docs/pilot/reports/bablos79_SIGNAL_REPORT_V1.md`

Report result:

The first real report artifact is a text-only negative/limitation report. It
states that the current `bablos79` capture window contains 60 public Telegram
text captures but no complete customer-report-eligible trade setup rows under
the validated pseudo-label result. It includes coverage counts, review queue
counts, unresolved outcome counts, limitations, evidence appendix links, and the
canonical non-advice disclaimer. It does not include performance metrics,
future-profit claims, media claims, or investment advice.

## Real Media-Backed Route

Status: planned and active after the text-only report result on 2026-05-12.

Why this route exists:

- the generated text-only report shows 0 customer-report-eligible metric rows;
- operator expects real audio/image evidence to be acquired and analyzed;
- Phase 20 implemented media adapters but did not run them on real media;
- the AI loop must not claim audio/image analysis until real public media exists,
  transcript/OCR output is generated, and a human review gate marks it usable.

Canonical plan:

- `docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md`

Task sequence:

1. `SAS-LIVE-001` - real media scope and evidence intake;
2. `SAS-LIVE-002` - public media artifact acquisition;
3. `SAS-LIVE-003` - voice transcript draft run;
4. `SAS-LIVE-004` - image OCR draft run;
5. `SAS-LIVE-005` - human media evidence review;
6. `SAS-LIVE-006` - reviewed multimodal source join;
7. `SAS-LIVE-007` - multimodal extraction and review queue;
8. `SAS-LIVE-008` - multimodal outcome prep;
9. `SAS-LIVE-009` - media-backed report V1;
10. `SAS-AF-006..008` - manual validity review, demo pack, external pilot gate.

Do not skip directly from Phase 20 adapters to report claims. The real media
route requires concrete public/operator-authorized media inputs and reviewable
artifacts at every step.

## SAS-LIVE-001 Real Media Intake

Status: superseded by completed media route as of 2026-05-14.

Artifact:

- `docs/pilot/bablos79_REAL_MEDIA_INTAKE.md`

Result:

The current workspace has no acquisition-ready media item: no raw media files,
no Telegram media file IDs, no transcript artifacts, no OCR artifacts, and no
reviewed media evidence refs. The intake plan records two source-linked media
references from the text corpus:

- `bablos79-10486` references the author's voice context but has no linked
  public voice media URL/file ID/local file;
- `bablos79-10465` says a video will be recorded, but the actual follow-up
  video URL/file is not identified.

Channel-level image/screenshot/chart/voice media remains excluded until each
item has exact source/capture/source-document linkage and public/operator
authorization. The subsequent `SAS-LIVE-002` pass found two concrete public
voice rows and acquired them.

## SAS-LIVE-002 Through SAS-AF-008 Media Route Result

Status: completed with reject decision on 2026-05-14.

Artifacts:

- `docs/pilot/bablos79_REAL_MEDIA_ACQUISITION.md`
- `docs/pilot/bablos79_MEDIA_MANIFEST.json`
- `docs/pilot/bablos79_TRANSCRIPT_RUN.md`
- `docs/pilot/bablos79_OCR_RUN.md`
- `docs/pilot/bablos79_MEDIA_REVIEW.md`
- `docs/pilot/bablos79_MULTIMODAL_SOURCE_PREVIEW.md`
- `docs/pilot/bablos79_MULTIMODAL_REVIEW_QUEUE.md`
- `docs/pilot/bablos79_MULTIMODAL_OUTCOME_PREP.md`
- `docs/pilot/reports/bablos79_MEDIA_BACKED_REPORT_V1.md`
- `docs/audit/PHASE21_VALIDITY_REVIEW.md`
- `docs/audit/PHASE21_ERROR_REGISTER.md`
- `docs/pilot/bablos79_INTERNAL_DEMO_PACK.md`
- `docs/pilot/bablos79_EXTERNAL_PILOT_READY_GATE.md`

Result:

The public `/s/` route yielded two concrete voice media artifacts:
`bablos79-10476` and `bablos79-10478`. Both were acquired as local OGG files
and registered in the media manifest. The local run did not have a configured
transcription provider, so both transcript attempts were recorded as skipped,
OCR had no image/screenshot inputs, human media review produced 0 usable refs,
multimodal source join preserved text-only context, multimodal review/outcome
prep produced 0 media-backed eligible rows and 0 market-data fetches, and the
media-backed report is a reject/limitation artifact.

External pilot readiness decision:

- Decision: reject this source/window for external delivery.
- Reason: 0 reviewed usable media refs, 0 report-eligible rows, 0 outcome
  metrics, and open Phase 21 evidence/readiness findings.
- Safe use: internal demo of evidence discipline and delivery gating only.

## Read Order

1. `docs/CODEX_PROMPT.md`
2. this file
3. repo-root `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
4. `docs/tasks.md` SAS-AF-001..008
5. task-specific `Context-Refs`
