# Media Artifacts

Date: 2026-05-09
Status: implemented by `SAS-MEDIA-002`

## Purpose

`MediaArtifact` records local metadata for voice/audio/image/screenshot evidence
without acquiring media, calling transcription/OCR providers, approving records,
or creating customer-facing claims.

The schema is the bridge between approved public/operator-authorized captures
and later draft transcript/OCR artifacts. It follows ADR-004:

- runtime remains T0;
- raw media is local operator-controlled operational data;
- media must link to approved source/capture/source-document identity;
- transcript/OCR refs are draft evidence only and require human review before
  customer-sample use.

## Required Fields

| Field | Meaning |
|-------|---------|
| `media_id` | Stable local media identifier. |
| `source_id` | Approved source manifest ID. |
| `capture_id` | Capture row that introduced the media. |
| `source_document_id` | Normalized `SourceDocument` identity. |
| `source_timestamp_utc` | Source/capture timestamp used for deterministic manifest sorting. |
| `modality` | `voice`, `audio`, `image`, `screenshot`, or `other`. |
| `original_url_or_file_id` | Public media URL, Telegram file ID, or operator-supplied original reference. |
| `local_path` | Operator-controlled local media path. |
| `media_sha256` | Lowercase SHA-256 of the local media bytes. |
| `mime_type` | Media MIME type. |
| `duration_seconds` | Optional duration for voice/audio. |
| `image_width_px` / `image_height_px` | Optional image dimensions. |
| `retention_state` | `temporary`, `retained_evidence_snapshot`, or `deleted`. |
| `created_at_utc` | Artifact metadata creation timestamp. |
| `draft_transcript_refs` | Draft transcript artifact refs; review-required. |
| `draft_ocr_refs` | Draft OCR artifact refs; review-required. |

## Manifest Export

`build_media_manifest()` returns rows sorted by:

1. `source_timestamp_utc`
2. `source_document_id`
3. `media_id`

The manifest can render Markdown for internal review and JSON for deterministic
machine-readable handoff. The manifest does not create media files, transcript
files, OCR files, approved ledgers, market-data snapshots, outcomes, reports,
provider requests, network calls, or customer-facing outputs.

## Rejection Rules

The schema rejects artifacts without source/capture/source-document linkage,
without a local path, or without a lowercase 64-character SHA-256 checksum.
Extra fields are forbidden so provider-specific output cannot be hidden in the
metadata contract.

## Telegram Voice Acquisition

`SAS-MEDIA-003` adds `acquire_telegram_voice_artifact()` for operator-authorized
public Telegram voice evidence.

Boundary:

- accepts an injected client with `get_file(file_id)`;
- downloads the returned file handle with `download_to_drive(custom_path=...)`;
- writes a temporary `.ogg.part` file and renames it only after checksum
  calculation succeeds;
- returns a `MediaArtifact` with modality `voice`, MIME type `audio/ogg`,
  source/capture/source-document linkage, duration when provided, SHA-256, and
  retention state `temporary`;
- rejects missing legal authorization and forbidden private/authenticated media
  authorization states;
- deletes partial/final local files on download failure;
- does not transcribe audio, call Whisper, call OCR, write provider outputs,
  approve ledgers, compute metrics, render reports, or create customer-facing
  claims.

CI must use fake clients. Real Telegram network calls are not allowed in tests.

## Whisper Transcript Drafts

`SAS-MEDIA-004` adds `run_whisper_transcription()` for gated managed
Whisper-style transcription over local voice `MediaArtifact` rows.

Activation requires both:

1. `SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION=1`
2. per-run approval from the caller

If either gate is missing, the adapter returns `status="skipped"` and does not
invoke the transcription client.

Successful transcription writes a draft JSON artifact containing:

- `transcript_id`
- `media_id`
- `provider`
- `model`
- `transcript_text`
- `transcript_sha256`
- `source_media_sha256`
- `status="draft_pending_review"`
- `reviewer_id="pending"`
- `review_required=true`
- `created_at_utc`
- `raw_media_retention_action`
- `artifact_path`

Provider failure returns `status="provider_failed"` with a typed error name,
creates no draft transcript, creates no approved transcript, and leaves raw
media cleanup to ADR-004 retention policy.

Successful transcription either deletes the raw local media file or records that
it was retained by policy. The adapter does not log raw transcript text and does
not route transcript output to reports, approved MarketIdea rows, ledgers,
metrics, or customer-facing claims.

## OCR Drafts

`SAS-MEDIA-006` adds `run_ocr_draft()` for review-required OCR over local
`MediaArtifact` rows whose modality is `image` or `screenshot`.

Boundary:

- accepts an injected OCR client with `extract_text(media_path, model=...)`;
- CI uses fake clients only;
- rejects non-image modalities;
- writes a draft JSON artifact with `media_id`, `ocr_id`, `provider`, `model`,
  OCR text, `text_sha256`, `source_media_sha256`, optional bounding metadata,
  `status="draft_pending_review"`, `reviewer_id="pending"`, and
  `review_required=true`;
- refuses approved chart claims;
- stores chart labels, price levels, or trade interpretations only as
  `review_required_notes`;
- does not write reports, approved MarketIdea rows, ledgers, metrics, or
  customer-facing claims.

## SourceDocument Join

`SAS-MEDIA-007` adds `join_multimodal_source_document()` to attach media,
transcript, and OCR refs to `SourceDocument` copies.

The join validates source/capture/document linkage and source media checksums
before adding refs. It preserves original capture text, evidence URL, and text
hash exactly. Media-derived refs remain draft evidence and do not mutate
approved MarketIdea rows, outcomes, ledgers, reports, metrics, or
customer-facing claims.
