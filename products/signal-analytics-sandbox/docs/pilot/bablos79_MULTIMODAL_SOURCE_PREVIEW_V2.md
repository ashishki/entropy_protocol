# Multimodal Source Preview V2 - bablos79

Date: 2026-05-15
Status: internal_preview_external_blocked

This preview joins current text, voice/transcript, and image/OCR evidence under
the Phase 23 acceptance policy. It is a source-document preview only: it does
not change original source text, evidence URLs, text hashes, transcript content,
claim text, ledgers, outcomes, or customer-facing report sections.

## Inputs

| artifact | role |
|---|---|
| `docs/pilot/bablos79_EXPANDED_CAPTURE_MANIFEST.json` | 60 registered public text seed captures for the locked 90-day scope. |
| `docs/pilot/bablos79_LLM_REVIEWED_SOURCE_JOIN.json` | Existing source-document join rows for two public voice refs. |
| `docs/pilot/bablos79_TRANSCRIPT_ACCEPTANCE_POLICY.md` | Transcript status policy and internal/external boundary. |
| `docs/pilot/bablos79_TRANSCRIPT_LLM_REVIEW.md` | LLM review artifact for two transcript refs. |
| `docs/pilot/bablos79_REVIEWED_MEDIA_EVIDENCE.md` | Reviewed image/chart/OCR evidence export; currently empty/blocked. |

## Evidence Counts

| category | count | status |
|---|---:|---|
| registered text source rows | 60 | source text only |
| text-only rows with no joined media refs | 58 | source text only |
| source rows with voice media refs | 2 | joined internal preview |
| LLM-reviewed transcript refs | 2 | `llm_reviewed_internal` |
| human/operator accepted transcript refs | 0 | external blocked |
| reviewed usable image refs | 0 | none available |
| reviewed usable OCR refs | 0 | none available |
| blocked image/chart/OCR rows | 4 | excluded from source joins |
| external-eligible media-backed refs | 0 | external blocked |

## Text-Only Evidence

The 60 seed captures remain the text corpus. Rows without joined media refs are
text-only source documents and retain their original source URL and
`text_sha256` from `docs/pilot/bablos79_EXPANDED_CAPTURE_MANIFEST.json`.

No text row is upgraded to a customer-facing media-backed claim by this preview.

## Voice-Reviewed Internal Evidence

The two joined voice rows below are internal-only because the transcript policy
classifies them as `llm_reviewed_internal`, not
`human_operator_accepted` or `external_claim_ready`.

| document_id | text | evidence_url | text_sha256 | media_ref | transcript_ref | review_artifact | policy_status | external_delivery |
|---|---|---|---|---|---|---|---|---|
| `bablos79:bablos79-10476` | `Утреннее. Звонок.` | `https://t.me/bablos79/10476` | `fced0cd89e597531ae3082941397f7c9f0804a1b41779edfea295cb55c95b4fe` | `workspace/media/bablos79/bablos79-10476.ogg` | `docs/pilot/transcripts/transcript_57b6461001b54e10.json` | `docs/pilot/bablos79_TRANSCRIPT_LLM_REVIEW.json` | `llm_reviewed_internal` | no |
| `bablos79:bablos79-10478` | `Про майские` | `https://t.me/bablos79/10478` | `bcccb754e9c8fec7d32e8c2ea9852c2b24667fd490edd8863c232ee302c96718` | `workspace/media/bablos79/bablos79-10478.ogg` | `docs/pilot/transcripts/transcript_92ad5bf2e9088056.json` | `docs/pilot/bablos79_TRANSCRIPT_LLM_REVIEW.json` | `llm_reviewed_internal` | no |

Allowed use:

- internal source joins;
- internal analyst notes;
- internal draft reports labeled as LLM-reviewed transcript evidence;
- claim-candidate discovery for later human/operator review.

Blocked use:

- customer-facing media-backed claims;
- external author capability conclusions;
- deterministic outcome ledgers;
- investment advice, ranking, or future-profit claims.

## Image/OCR Evidence

No image, chart, or OCR refs are joined in this preview.

| source | status | preview action |
|---|---|---|
| `blocked_image_channel_level_screenshot` | `blocked_missing_source_linkage` | excluded |
| `blocked_chart_channel_level_screenshot` | `blocked_missing_source_linkage` | excluded |
| `blocked_gap_pre_seed_window_images` | `blocked_missing_capture_rows` | excluded |
| `blocked_gap_post_seed_window_images` | `blocked_missing_capture_rows` | excluded |

These rows remain blockers only. They do not create source joins, visible
ticker/level/date evidence, chart interpretation, OCR text, claims, or outcome
methods.

## Internal-Only Vs External-Eligible

| section | included refs | external eligible? | reason |
|---|---:|---|---|
| text-only source rows | 60 | no media-backed eligibility from this preview | Source text remains available as source corpus; report eligibility is handled later by claim ledger/review gates. |
| voice transcript joins | 2 | no | LLM review is internal-only until human/operator accepted or explicitly waived. |
| image/OCR joins | 0 | no | No reviewed image/OCR artifacts exist. |
| final/customer-facing media section | 0 | no | There are no `external_claim_ready` media-backed refs. |

## Preservation Checks

- Original `SourceDocument.text` values for joined rows are copied unchanged
  from `docs/pilot/bablos79_LLM_REVIEWED_SOURCE_JOIN.json`.
- Original `evidence_url` values remain
  `https://t.me/bablos79/10476` and `https://t.me/bablos79/10478`.
- Original `text_sha256` values remain
  `fced0cd89e597531ae3082941397f7c9f0804a1b41779edfea295cb55c95b4fe` and
  `bcccb754e9c8fec7d32e8c2ea9852c2b24667fd490edd8863c232ee302c96718`.
- Joined media refs are additive only and do not mutate source truth.
- Unreviewed OCR/transcript evidence is excluded from final/customer-facing
  sections.

## Next Gate

Phase 23 deep review must check that this preview keeps draft, internal,
reviewed, and external-eligible statuses separate before Phase 24 claim-ledger
work starts.
