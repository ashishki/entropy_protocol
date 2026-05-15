# Multimodal Report Development Plan

Status: Active Phase 21 overlay
Date: 2026-05-12

This plan exists because the text-only `bablos79` report draft proved that the
current public text window has no complete customer-report-eligible metric rows.
The next development loop must therefore acquire and validate real public media
evidence before claiming that audio/image coverage was tested.

## Goal

Produce a media-backed public-source report artifact from real
operator-authorized Telegram media, with human-reviewed transcript/OCR evidence
and deterministic outcomes only where the evidence supports them.

## Non-Negotiable Boundary

- No private Telegram groups.
- No login-walled, paywalled, or access-bypass media.
- No customer-facing media claims before human transcript/OCR review.
- No autonomous chart interpretation.
- No advice, future-profit, marketplace, or leaderboard claims.
- No outcome metrics for rows missing asset, direction/thesis, timestamp,
  horizon, and reviewed evidence.

## Phase 0 - Real Media Scope And Evidence Intake

Output: `docs/pilot/bablos79_REAL_MEDIA_INTAKE.md`.

Define the exact public/operator-authorized voice/audio/image/screenshot items
to process. Each row must link to source/capture/source-document IDs, expected
report value, modality, authorization status, and blocker reason if missing.

## Phase 1 - Public Media Artifact Acquisition

Output:

- `docs/pilot/bablos79_REAL_MEDIA_ACQUISITION.md`
- `docs/pilot/bablos79_MEDIA_MANIFEST.json`

Acquire or register local operator-controlled media files and deterministic
`MediaArtifact` metadata. This phase records local path, SHA-256, MIME type,
retention state, source linkage, and failed/skipped/blocked items.

## Phase 2 - Voice Transcript Draft Run

Output: `docs/pilot/bablos79_TRANSCRIPT_RUN.md`.

Run the gated transcription adapter only for acquired voice/audio artifacts.
Transcript output remains `draft_pending_review` and cannot affect reports
until reviewed.

## Phase 3 - Image OCR Draft Run

Output: `docs/pilot/bablos79_OCR_RUN.md`.

Run OCR only for acquired image/screenshot artifacts. OCR extracts visible text;
chart interpretation and trading claims stay manual-review-only.

## Phase 4 - Human Media Evidence Review

Output: `docs/pilot/bablos79_MEDIA_REVIEW.md`.

Operator reviews each transcript/OCR artifact against the original public media
and marks it usable, unusable, needs rework, or out of scope.

## Phase 5 - Reviewed Multimodal Source Join

Output: `docs/pilot/bablos79_MULTIMODAL_SOURCE_PREVIEW.md`.

Join only reviewed-usable transcript/OCR refs into `SourceDocument` copies while
preserving original text, evidence URL, and text hash.

## Phase 6 - Multimodal Extraction And Review Queue

Output: `docs/pilot/bablos79_MULTIMODAL_REVIEW_QUEUE.md`.

Re-run extraction/review using text plus reviewed media context. Separate
approved candidates, ambiguous rows, insufficient rows, not-market-related rows,
media-needed rows, and media-blocked rows.

## Phase 7 - Multimodal Outcome Prep

Output: `docs/pilot/bablos79_MULTIMODAL_OUTCOME_PREP.md`.

Prepare deterministic outcomes only for complete final-reviewed rows. Record all
unresolved rows and fetch market data only for measurable rows.

## Phase 8 - Media-Backed Report V1

Output: `docs/pilot/reports/bablos79_MEDIA_BACKED_REPORT_V1.md`.

Render the revised report with media coverage, reviewed evidence refs, supported
outcomes, unresolved rows, limitations, and the canonical non-advice boundary.

## Phase 9 - Manual Validity Review And Delivery Gate

Outputs:

- manual validity notes;
- error register;
- internal demo pack;
- external pilot ready / needs fixes / reject decision.

Validate source URL, timestamp/timezone, media linkage, transcript/OCR quality,
asset mapping, direction/thesis, outcome window, metrics, and claim wording
before any external delivery.
