# Retrospective Outcomes Draft - bablos79

Date: 2026-05-15
Status: no_computed_outcomes_no_approved_proxies
Artifact: `bablos79-retrospective-outcomes-draft-v1`

This artifact records the retrospective outcome state after the Phase 24 claim
ledger and proxy map. It computes no market metrics because
`docs/pilot/bablos79_MARKET_PROXY_MAP.md` approved 0 proxies and 0 market-data
fetch rows.

## Summary

| Field | Count |
|---|---:|
| total claim rows | 67 |
| computed metric rows | 0 |
| confirmed rows | 0 |
| contradicted rows | 0 |
| unresolved rows | 13 |
| insufficient-data rows | 0 |
| non-measurable rows | 5 |
| not-applicable rows | 49 |
| unsupported-media rows | 4 |
| market-data snapshots used | 0 |
| approved proxy rows | 0 |

## Status Counts

| Outcome status | Count |
|---|---:|
| `non_measurable` | 2 |
| `non_measurable_internal_only` | 3 |
| `not_applicable_non_market` | 49 |
| `unresolved_no_approved_proxy` | 9 |
| `unresolved_unsupported_media` | 4 |

## Evaluation Boundary

- No market data was fetched.
- No return, MFE, MAE, confirmed, or contradicted metric was computed.
- Claims without reviewed evidence, approved proxy, horizon, source timestamp,
  or market snapshot remain unresolved or non-measurable.
- Non-market, unsupported media, and internal-only transcript claims remain
  visible in coverage counts.

## Outcome Rows

| outcome_id | claim_id | category | outcome_status | market_data_snapshot | approved_proxy | horizon | metric_computed | unresolved reason |
|---|---|---|---|---|---|---|---|---|
| `outcome_text_bablos79_10442` | `claim_text_bablos79_10442` | `directional_bias` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10443` | `claim_text_bablos79_10443` | `directional_bias` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10444` | `claim_text_bablos79_10444` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10445` | `claim_text_bablos79_10445` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10446` | `claim_text_bablos79_10446` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10447` | `claim_text_bablos79_10447` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10448` | `claim_text_bablos79_10448` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10449` | `claim_text_bablos79_10449` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10450` | `claim_text_bablos79_10450` | `directional_bias` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10451` | `claim_text_bablos79_10451` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10452` | `claim_text_bablos79_10452` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10453` | `claim_text_bablos79_10453` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10454` | `claim_text_bablos79_10454` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10455` | `claim_text_bablos79_10455` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10456` | `claim_text_bablos79_10456` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10457` | `claim_text_bablos79_10457` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10458` | `claim_text_bablos79_10458` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10459` | `claim_text_bablos79_10459` | `directional_bias` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10460` | `claim_text_bablos79_10460` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10461` | `claim_text_bablos79_10461` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10463` | `claim_text_bablos79_10463` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10464` | `claim_text_bablos79_10464` | `level_timing_call` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10465` | `claim_text_bablos79_10465` | `macro_context` | `non_measurable` | none | none | none | no | Claim is useful context but lacks approved proxy/outcome method. |
| `outcome_text_bablos79_10466` | `claim_text_bablos79_10466` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10467` | `claim_text_bablos79_10467` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10468` | `claim_text_bablos79_10468` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10469` | `claim_text_bablos79_10469` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10470` | `claim_text_bablos79_10470` | `watchlist` | `non_measurable` | none | none | none | no | Claim is useful context but lacks approved proxy/outcome method. |
| `outcome_text_bablos79_10471` | `claim_text_bablos79_10471` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10472` | `claim_text_bablos79_10472` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10475` | `claim_text_bablos79_10475` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10476` | `claim_text_bablos79_10476` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10477` | `claim_text_bablos79_10477` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10478` | `claim_text_bablos79_10478` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10479` | `claim_text_bablos79_10479` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10482` | `claim_text_bablos79_10482` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10483` | `claim_text_bablos79_10483` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10485` | `claim_text_bablos79_10485` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10486` | `claim_text_bablos79_10486` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10487` | `claim_text_bablos79_10487` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10488` | `claim_text_bablos79_10488` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10489` | `claim_text_bablos79_10489` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10490` | `claim_text_bablos79_10490` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10491` | `claim_text_bablos79_10491` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10492` | `claim_text_bablos79_10492` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10493` | `claim_text_bablos79_10493` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10495` | `claim_text_bablos79_10495` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10496` | `claim_text_bablos79_10496` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10497` | `claim_text_bablos79_10497` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10498` | `claim_text_bablos79_10498` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10499` | `claim_text_bablos79_10499` | `level_timing_call` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10500` | `claim_text_bablos79_10500` | `level_timing_call` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10501` | `claim_text_bablos79_10501` | `level_timing_call` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10502` | `claim_text_bablos79_10502` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10503` | `claim_text_bablos79_10503` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10504` | `claim_text_bablos79_10504` | `directional_bias` | `unresolved_no_approved_proxy` | none | none | none | no | Claim lacks approved proxy, horizon, or complete evaluability fields. |
| `outcome_text_bablos79_10505` | `claim_text_bablos79_10505` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10506` | `claim_text_bablos79_10506` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10507` | `claim_text_bablos79_10507` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_text_bablos79_10508` | `claim_text_bablos79_10508` | `non_market_commentary` | `not_applicable_non_market` | none | none | none | no | Row is retained for coverage but excluded from performance outcomes. |
| `outcome_transcript_bablos79_10476_claim1` | `claim_transcript_bablos79_10476_claim1` | `macro_context` | `non_measurable_internal_only` | none | none | none | no | Transcript claim is LLM-reviewed internal only and has no approved proxy. |
| `outcome_transcript_bablos79_10476_claim2` | `claim_transcript_bablos79_10476_claim2` | `directional_bias` | `non_measurable_internal_only` | none | none | `майские праздники` | no | Transcript claim is LLM-reviewed internal only and has no approved proxy. |
| `outcome_transcript_bablos79_10478_claim1` | `claim_transcript_bablos79_10478_claim1` | `event_risk` | `non_measurable_internal_only` | none | none | `майские праздники` | no | Transcript claim is LLM-reviewed internal only and has no approved proxy. |
| `outcome_media_blocked_image_channel_level_screenshot` | `claim_media_blocked_image_channel_level_screenshot` | `unsupported_media_claim` | `unresolved_unsupported_media` | none | none | none | no | Media/source linkage or review acceptance is missing. |
| `outcome_media_blocked_chart_channel_level_screenshot` | `claim_media_blocked_chart_channel_level_screenshot` | `unsupported_media_claim` | `unresolved_unsupported_media` | none | none | none | no | Media/source linkage or review acceptance is missing. |
| `outcome_media_blocked_gap_pre_seed_window_images` | `claim_media_blocked_gap_pre_seed_window_images` | `unsupported_media_claim` | `unresolved_unsupported_media` | none | none | none | no | Media/source linkage or review acceptance is missing. |
| `outcome_media_blocked_gap_post_seed_window_images` | `claim_media_blocked_gap_post_seed_window_images` | `unsupported_media_claim` | `unresolved_unsupported_media` | none | none | none | no | Media/source linkage or review acceptance is missing. |
