# Three-Channel Multimodal Research Report

Date: 2026-05-22T07:15:38Z
Status: `internal_multimodal_research_draft`

## Boundary

- Sources: public Telegram `/s/` HTML only.
- Media scope: public image/voice/audio refs visible in those pages.
- Raw media is stored under `workspace/` and is not intended for git commit.
- Transcript/OCR rows are `draft_pending_review`; they are not customer-facing metrics until human/operator accepted.
- RR fields are populated only from extracted evidence text; missing entry/stop/target/size remains explicit blocker.

## Artifacts

- Media manifest JSON: `docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json`
- Processing queue JSON: `docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json`
- RR draft JSON: `docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json`

## Totals

- `posts`: 570
- `text_rows`: 527
- `posts_with_media`: 272
- `media_rows`: 295
- `draft_transcript_or_ocr_rows`: 255
- `rr_drafts`: 549
- `rr_ready`: 1

## Channel Comparison

| channel | posts | text rows | posts with media | media rows | media by modality | draft transcript/OCR | RR drafts | RR ready | top RR blockers |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| `bablos79` | 382 | 341 | 194 | 196 | image:94, video:34, voice:68 | 162 | 362 | 1 | position_size_missing:362, missing_target:360, rr_not_computable:360, missing_stop:356, missing_entry:338 |
| `nemphiscrypts` | 133 | 132 | 51 | 63 | image:63 | 63 | 133 | 0 | position_size_missing:132, rr_not_computable:132, missing_stop:128, missing_target:127, missing_entry:121 |
| `pifagortrade` | 55 | 54 | 27 | 36 | image:28, video:6, voice:2 | 30 | 54 | 0 | position_size_missing:54, rr_not_computable:52, missing_entry:50, missing_target:47, missing_stop:43 |

## What This Means

- The previous two-month run measured text-only directional calls. This run adds media intake and draft extraction.
- A channel can have many useful media notes while still producing few RR-ready trades if author posts theses, regimes, screenshots, or voice commentary without explicit entry/stop/target.
- `rr_ready` is intentionally strict for internal quant review: it requires supported asset, single direction, entry, stop, target, and computable or explicit RR.
- Missing position size and media-review status are tracked separately because they matter for paid/customer-facing use but should not erase an otherwise measurable RR setup.
- `position_size_missing` is tracked separately because most public calls do not reveal actual allocation.

## Gate

- Decision: `internal_research_only`.
- Reason: transcript/OCR needs human/operator acceptance before any paid/customer-facing metric.
