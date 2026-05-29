# Claim Ledger Draft - bablos79

Date: 2026-05-15
Status: draft_insufficient_reviewable_claims_external_blocked
Ledger: `bablos79-claim-ledger-draft-v1`

This draft ledger applies `docs/pilot/bablos79_CLAIM_TAXONOMY.md` to the
expanded `bablos79` seed corpus, LLM-reviewed internal transcript claims, and
Phase 23 blocked media rows. It is not final truth and does not create customer
report eligibility, deterministic outcomes, or investment advice.

## Summary

| Field | Count |
|---|---:|
| total ledger rows | 67 |
| text capture rows | 60 |
| LLM-reviewed transcript claim rows | 3 |
| unsupported media blocker rows | 4 |
| reviewable non-blocker claim rows | 14 |
| deterministic outcome-ready rows | 0 |
| customer-report-eligible rows | 0 |

External delivery status: `blocked_no_external_eligible_media_or_outcomes`

## Insufficient-Corpus Decision

The ledger records an insufficient-corpus decision for the 30-50 reviewable
claim target: `true`.

Reasons:

- Only 14 reviewable non-blocker claim rows are present, below the 30-50 target.
- The locked 90-day window is only partially represented by local seed captures.
- Two transcript refs are LLM-reviewed internal only and not external accepted.
- Zero reviewed image/OCR refs exist.
- All deterministic outcome-ready counts are zero pending proxy mapping and market data.


## Category Counts

| Category | Count |
|---|---:|
| `directional_bias` | 6 |
| `event_risk` | 1 |
| `level_timing_call` | 4 |
| `macro_context` | 2 |
| `non_market_commentary` | 49 |
| `unsupported_media_claim` | 4 |
| `watchlist` | 1 |

## Measurability Counts

| Measurability status | Count |
|---|---:|
| `ambiguous_or_insufficient` | 4 |
| `ambiguous_weak` | 1 |
| `context_only` | 1 |
| `insufficient_fields` | 4 |
| `non_measurable` | 1 |
| `non_measurable_internal_only` | 3 |
| `not_applicable` | 49 |
| `unsupported_media` | 4 |

## Boundary

- Draft extraction cannot create final truth without review status.
- LLM-reviewed transcript claims are internal-only until human/operator
  acceptance or explicit claim-level waiver.
- Unsupported image/chart/OCR rows remain blockers and are not source joins.
- Non-market, ambiguous, weak, unsupported, and blocker rows stay visible rather
  than being filtered out.
- Market proxy mapping and outcome computation have not run.

## Ledger Rows

| claim_id | source_type | capture_id | category | asset/proxy candidates | direction | horizon | review_state | measurability_status | media_refs | outcome_ready | blockers |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `claim_text_bablos79_10442` | `text_capture` | `bablos79-10442` | `directional_bias` | `X5` | `unknown` | none | `reviewed_insufficient_evidence` | `ambiguous_or_insufficient` | none | no | Missing fields: direction, entry, stop, target; Required deterministic outcome fields are missing or ambiguous. |
| `claim_text_bablos79_10443` | `text_capture` | `bablos79-10443` | `directional_bias` | `VTBR` | `unknown` | none | `reviewed_insufficient_evidence` | `ambiguous_or_insufficient` | none | no | Missing fields: direction, entry, stop, target; Required deterministic outcome fields are missing or ambiguous. |
| `claim_text_bablos79_10444` | `text_capture` | `bablos79-10444` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10445` | `text_capture` | `bablos79-10445` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10446` | `text_capture` | `bablos79-10446` | `non_market_commentary` | `VTBR` | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10447` | `text_capture` | `bablos79-10447` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10448` | `text_capture` | `bablos79-10448` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10449` | `text_capture` | `bablos79-10449` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10450` | `text_capture` | `bablos79-10450` | `directional_bias` | `MAGN` | `negative` | none | `reviewed_insufficient_evidence` | `ambiguous_or_insufficient` | none | no | Missing fields: entry, stop, target; Required deterministic outcome fields are missing or ambiguous. |
| `claim_text_bablos79_10451` | `text_capture` | `bablos79-10451` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10452` | `text_capture` | `bablos79-10452` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10453` | `text_capture` | `bablos79-10453` | `non_market_commentary` | `VKCO` | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10454` | `text_capture` | `bablos79-10454` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10455` | `text_capture` | `bablos79-10455` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10456` | `text_capture` | `bablos79-10456` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10457` | `text_capture` | `bablos79-10457` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10458` | `text_capture` | `bablos79-10458` | `non_market_commentary` | `X5` | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10459` | `text_capture` | `bablos79-10459` | `directional_bias` | `AMD` | `negative` | none | `ambiguous_needs_operator_review` | `ambiguous_or_insufficient` | none | no | Missing fields: entry, stop, target; Required deterministic outcome fields are missing or ambiguous. |
| `claim_text_bablos79_10460` | `text_capture` | `bablos79-10460` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10461` | `text_capture` | `bablos79-10461` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10463` | `text_capture` | `bablos79-10463` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10464` | `text_capture` | `bablos79-10464` | `level_timing_call` | `X5` | `management` | none | `reviewed_insufficient_evidence` | `insufficient_fields` | none | no | Missing fields: entry, stop, target; Required deterministic outcome fields are missing or ambiguous. |
| `claim_text_bablos79_10465` | `text_capture` | `bablos79-10465` | `macro_context` | none | `unknown` | none | `reviewed_context_only` | `non_measurable` | none | no | No benchmark/proxy, horizon, and outcome method approved yet. |
| `claim_text_bablos79_10466` | `text_capture` | `bablos79-10466` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10467` | `text_capture` | `bablos79-10467` | `non_market_commentary` | `MAGN` | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10468` | `text_capture` | `bablos79-10468` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10469` | `text_capture` | `bablos79-10469` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10470` | `text_capture` | `bablos79-10470` | `watchlist` | none | `unknown` | none | `ambiguous_needs_operator_review` | `context_only` | none | no | Missing fields: asset_symbol, entry, stop, target; Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10471` | `text_capture` | `bablos79-10471` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10472` | `text_capture` | `bablos79-10472` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10475` | `text_capture` | `bablos79-10475` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10476` | `text_capture` | `bablos79-10476` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10477` | `text_capture` | `bablos79-10477` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10478` | `text_capture` | `bablos79-10478` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10479` | `text_capture` | `bablos79-10479` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10482` | `text_capture` | `bablos79-10482` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10483` | `text_capture` | `bablos79-10483` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10485` | `text_capture` | `bablos79-10485` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10486` | `text_capture` | `bablos79-10486` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10487` | `text_capture` | `bablos79-10487` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10488` | `text_capture` | `bablos79-10488` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10489` | `text_capture` | `bablos79-10489` | `non_market_commentary` | `GAZP` | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10490` | `text_capture` | `bablos79-10490` | `non_market_commentary` | `GAZP` | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10491` | `text_capture` | `bablos79-10491` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10492` | `text_capture` | `bablos79-10492` | `non_market_commentary` | `SBER` | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10493` | `text_capture` | `bablos79-10493` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10495` | `text_capture` | `bablos79-10495` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10496` | `text_capture` | `bablos79-10496` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10497` | `text_capture` | `bablos79-10497` | `non_market_commentary` | `MAGN` | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10498` | `text_capture` | `bablos79-10498` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10499` | `text_capture` | `bablos79-10499` | `level_timing_call` | `SFIN` | `management` | none | `reviewed_insufficient_evidence` | `insufficient_fields` | none | no | Missing fields: entry, stop, target; Required deterministic outcome fields are missing or ambiguous. |
| `claim_text_bablos79_10500` | `text_capture` | `bablos79-10500` | `level_timing_call` | `CHMF` | `management` | none | `reviewed_insufficient_evidence` | `insufficient_fields` | none | no | Missing fields: entry, stop, target; Required deterministic outcome fields are missing or ambiguous. |
| `claim_text_bablos79_10501` | `text_capture` | `bablos79-10501` | `level_timing_call` | `MAGN` | `management` | none | `reviewed_insufficient_evidence` | `insufficient_fields` | none | no | Missing fields: entry, stop, target; Required deterministic outcome fields are missing or ambiguous. |
| `claim_text_bablos79_10502` | `text_capture` | `bablos79-10502` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10503` | `text_capture` | `bablos79-10503` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10504` | `text_capture` | `bablos79-10504` | `directional_bias` | none | `management` | none | `ambiguous_needs_operator_review` | `ambiguous_weak` | none | no | Missing fields: asset_symbol, entry, stop, target |
| `claim_text_bablos79_10505` | `text_capture` | `bablos79-10505` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10506` | `text_capture` | `bablos79-10506` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10507` | `text_capture` | `bablos79-10507` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_text_bablos79_10508` | `text_capture` | `bablos79-10508` | `non_market_commentary` | none | `unknown` | none | `reviewed_excluded_non_market` | `not_applicable` | none | no | Not a strict performance/outcome row by taxonomy. |
| `claim_transcript_bablos79_10476_claim1` | `voice_transcript_llm_review` | `bablos79-10476` | `macro_context` | `global geopolitics, US, UK, Russia` | `negative` | none | `llm_reviewed_internal` | `non_measurable_internal_only` | `workspace/media/bablos79/bablos79-10476.ogg` | no | No explicit asset or measurable outcome.; Claim is broad and speculative.; Transcript is LLM-reviewed internal, not human/operator accept... |
| `claim_transcript_bablos79_10476_claim2` | `voice_transcript_llm_review` | `bablos79-10476` | `directional_bias` | `Московская биржа, широкий рынок активов` | `negative` | `майские праздники` | `llm_reviewed_internal` | `non_measurable_internal_only` | `workspace/media/bablos79/bablos79-10476.ogg` | no | No explicit asset or trade setup.; No deterministic price or outcome specified.; Transcript is LLM-reviewed internal, not human/operator ... |
| `claim_transcript_bablos79_10478_claim1` | `voice_transcript_llm_review` | `bablos79-10478` | `event_risk` | `Российская биржа` | `negative` | `майские праздники` | `llm_reviewed_internal` | `non_measurable_internal_only` | `workspace/media/bablos79/bablos79-10478.ogg` | no | No explicit asset or deterministic outcome.; Claim is event-driven and speculative.; Transcript is LLM-reviewed internal, not human/opera... |
| `claim_media_blocked_image_channel_level_screenshot` | `media_blocker` | none | `unsupported_media_claim` | none | `unknown` | none | `blocked_missing_source_linkage` | `unsupported_media` | none | no | No exact public source URL.; No capture ID, source-document ID, or checksumable media. |
| `claim_media_blocked_chart_channel_level_screenshot` | `media_blocker` | none | `unsupported_media_claim` | none | `unknown` | none | `blocked_missing_source_linkage` | `unsupported_media` | none | no | No exact public chart source linkage.; Chart interpretation remains manual-review-only. |
| `claim_media_blocked_gap_pre_seed_window_images` | `media_blocker` | `gap:gap-pre-seed-window` | `unsupported_media_claim` | none | `unknown` | none | `blocked_missing_capture_rows` | `unsupported_media` | none | no | No source rows exist for this locked-window period. |
| `claim_media_blocked_gap_post_seed_window_images` | `media_blocker` | `gap:gap-post-seed-window` | `unsupported_media_claim` | none | `unknown` | none | `blocked_missing_capture_rows` | `unsupported_media` | none | no | No source rows exist for this locked-window period. |
