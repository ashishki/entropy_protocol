# OCR And Chart Source-Link Policy

Status: internal policy
Date: 2026-05-19
Owner: codex + operator

## Purpose

This policy defines how OCR and chart/image evidence can become source-linked
and reviewable. It explicitly blocks machine-only chart interpretation from
customer-facing metrics, reports, and claims.

## Required Source Link Fields

Every OCR/chart candidate must preserve:

- `source_ref`
- `capture_id`
- `source_document_id`
- `media_id`
- `media_modality`
- `source_media_sha256`
- `ocr_artifact_ref`
- `ocr_text_sha256`
- `review_status`
- `reviewer_id`
- `reviewed_at_utc`
- `reason`
- `accepted_text_span`
- `accepted_claim_boundary`
- `external_claim_ready`

Rows missing source document linkage or checksum linkage remain excluded.

## Allowed Machine Output

Machine OCR may produce draft visible text only:

- visible labels;
- visible tickers;
- visible numbers;
- visible captions;
- visible prose that appears in the image.

Machine output must use `review_status="ocr_draft_pending_review"` until a
human/operator reviewer accepts or rejects it.

## Blocked Machine Output

Machine-only chart interpretation is forbidden for customer-facing metrics.
The system must not automatically create:

- support or resistance levels;
- trendline claims;
- breakout or breakdown claims;
- pattern labels;
- entry, stop, target, or invalidation levels;
- direction or performance claims;
- author skill claims based on chart shape.

If a chart image contains visible written text, OCR may draft that text for
review. The chart meaning remains `chart_context_only` until a human/operator
reviewer records an accepted claim boundary.

## Review Statuses

| status | meaning | allowed use | blocked use |
|---|---|---|---|
| `unlinked_media` | media exists only at channel level or lacks exact source document linkage | inventory and operator-linkage queue | OCR, extraction, metrics, reports |
| `ocr_draft_pending_review` | OCR text exists but no human/operator accepted it | review queue and QA | source joins, metrics, reports |
| `human_text_accepted` | reviewer accepted visible OCR text only | source join and claim-candidate drafting inside accepted span | chart meaning, outcomes, external claims without gate |
| `chart_context_only` | reviewer accepted image as context but not as a market claim | internal analyst context | deterministic claims, metrics, external claims |
| `human_claim_accepted` | reviewer accepted an exact media-backed claim boundary | internal extraction with media provenance | external delivery until gate approval |
| `rejected_unusable` | OCR/chart evidence is unusable or unsafe | exclusion note | source joins, metrics, reports |
| `external_claim_ready` | external gate approved the exact media-backed claim | customer-facing report use for that exact claim | broader claims, advice, unsupported metrics |

## Acceptance Rules

To accept OCR text:

- `source_ref`, `source_document_id`, `media_id`, `source_media_sha256`,
  `ocr_artifact_ref`, and `ocr_text_sha256` must be present;
- reviewer must record `reviewer_id`, `reviewed_at_utc`, `reason`, and
  `accepted_text_span`;
- accepted text cannot be converted into a market claim unless the reviewer also
  records `accepted_claim_boundary`.

To accept a chart-derived claim:

- machine-only interpretation is insufficient;
- reviewer must identify the exact visible evidence and the exact claim
  boundary;
- asset, direction, level, horizon, and proxy fields remain subject to normal
  claim review and provider approval;
- external use still requires `external_claim_ready`.

## Reporting Rules

- Unreviewed OCR/chart rows must be counted as blockers or exclusions.
- OCR text can support only the accepted visible text span.
- Chart screenshots can support context only unless a reviewer records an exact
  accepted claim boundary.
- Customer-facing metrics must exclude `unlinked_media`,
  `ocr_draft_pending_review`, `chart_context_only`, and `rejected_unusable`.
- No OCR/chart row may bypass the external-ready gate.

## Current Three-Channel Decision

Current accepted OCR/chart refs: 0.

Current customer-facing OCR/chart claims: 0.

Machine-only chart interpretation remains blocked.
