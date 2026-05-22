# Three-Channel Review Audit

Date: 2026-05-19
Status: external_gate_blocked

## Summary

| Metric | Count |
|---|---:|
| Queue rows | 1710 |
| Review decisions | 0 |
| Missing review decisions | 1710 |
| Accepted decisions | 0 |
| Accepted decisions missing required evidence | 0 |

External gate blocked: `true`.

## Missing Review By Current Decision

| Current decision | Missing rows |
|---|---:|
| `covered_by_v1_included_claim` | 126 |
| `excluded_context_only` | 152 |
| `excluded_direction_or_asset_pending` | 454 |
| `excluded_needs_context` | 12 |
| `excluded_not_market` | 568 |
| `excluded_pending_false_negative` | 5 |
| `excluded_position_mapping_pending` | 15 |
| `excluded_provider_gap` | 174 |
| `excluded_review_false_positive` | 5 |
| `excluded_setup_parser_pending` | 8 |
| `included_primary_horizon_pending` | 2 |
| `included_v1_evaluable` | 170 |
| `media_blocked` | 4 |
| `reviewed_exclusion_accepted` | 15 |

## Missing Review Examples

| queue_id | channel | source | current decision | blocker |
|---|---|---|---|---|
| `frq-media-claim_media_blocked_gap_post_seed_window_images` | `bablos79` | missing_public_source_url | `media_blocked` | No source rows exist for this locked-window period. |
| `frq-media-claim_media_blocked_gap_pre_seed_window_images` | `bablos79` | missing_public_source_url | `media_blocked` | No source rows exist for this locked-window period. |
| `frq-media-claim_media_blocked_chart_channel_level_screenshot` | `bablos79` | missing_public_source_url | `media_blocked` | No exact public chart source linkage.; Chart interpretation remains manual-review-only. |
| `frq-media-claim_media_blocked_image_channel_level_screenshot` | `bablos79` | missing_public_source_url | `media_blocked` | No exact public source URL.; No capture ID, source-document ID, or checksumable media. |
| `frq-source-bablos79-10002` | `bablos79` | https://t.me/bablos79/10002 | `excluded_not_market` | not_market_candidate |
| `frq-source-bablos79-10003` | `bablos79` | https://t.me/bablos79/10003 | `excluded_direction_or_asset_pending` | fixed_horizon_directional_outcome_after_proxy_approval |
| `frq-source-bablos79-10005` | `bablos79` | https://t.me/bablos79/10005 | `reviewed_exclusion_accepted` | Gold/news context without approved commodity proxy. |
| `frq-source-bablos79-10006` | `bablos79` | https://t.me/bablos79/10006 | `excluded_direction_or_asset_pending` | fixed_horizon_directional_outcome_after_proxy_approval |
| `frq-source-bablos79-10007` | `bablos79` | https://t.me/bablos79/10007 | `excluded_not_market` | not_market_candidate |
| `frq-source-bablos79-10008` | `bablos79` | https://t.me/bablos79/10008 | `excluded_provider_gap` | GD: unsupported (no approved provider/proxy mapping); NKNC: unsupported (no approved provider/proxy mapping); PRMD: unsupported (no approved provider/proxy mapping) |
| `frq-source-bablos79-10009` | `bablos79` | https://t.me/bablos79/10009 | `excluded_provider_gap` | GD: unsupported (no approved provider/proxy mapping); NKNC: unsupported (no approved provider/proxy mapping); PRMD: unsupported (no approved provider/proxy mapping) |
| `frq-source-bablos79-10010` | `bablos79` | https://t.me/bablos79/10010 | `excluded_not_market` | not_market_candidate |
| `frq-source-bablos79-10011` | `bablos79` | https://t.me/bablos79/10011 | `reviewed_exclusion_accepted` | Political/economic context, not asset-level claim. |
| `frq-source-bablos79-10012` | `bablos79` | https://t.me/bablos79/10012 | `excluded_direction_or_asset_pending` | fixed_horizon_directional_outcome_after_proxy_approval |
| `frq-source-bablos79-10013` | `bablos79` | https://t.me/bablos79/10013 | `excluded_position_mapping_pending` | position/trade management rows require linked setup context |
| `frq-source-bablos79-10014` | `bablos79` | https://t.me/bablos79/10014 | `excluded_not_market` | not_market_candidate |
| `frq-source-bablos79-10015` | `bablos79` | https://t.me/bablos79/10015 | `excluded_direction_or_asset_pending` | fixed_horizon_directional_outcome_after_proxy_approval |
| `frq-source-bablos79-10016` | `bablos79` | https://t.me/bablos79/10016 | `excluded_direction_or_asset_pending` | fixed_horizon_directional_outcome_after_proxy_approval |
| `frq-source-bablos79-10017` | `bablos79` | https://t.me/bablos79/10017 | `excluded_provider_gap` | EUTR: unsupported (no approved provider/proxy mapping) |
| `frq-source-bablos79-10020` | `bablos79` | https://t.me/bablos79/10020 | `excluded_not_market` | not_market_candidate |

## Accepted Evidence Rule

No accepted customer-facing claim may lack reviewer, source URL, and evidence
span. Current accepted decisions missing required evidence:
`0`.

## Gate Decision

The external gate remains blocked while missing review decisions are greater
than zero.
