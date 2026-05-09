# Extraction Log - First Telegram Source

Дата: 2026-05-07
Статус: draft suggestions exported; final extraction still pending
First source: `bablos79` (`https://t.me/bablos79`)

## Current Extraction State

Draft parser suggestions now exist for all 60 captured public text posts from unauthenticated Telegram `/s/` pages. Final extraction status remains pending: no signal candidates are approved, rejected, or ledger-ready until human review records a final status.

The next step is exception review using `docs/pilot/bablos79_REVIEW_QUEUE.md` against `docs/pilot/METHODOLOGY_V0.md`.

## Required Extraction Fields

Every extraction row must contain these fields once real captures exist:

| Field | Required | Notes |
|-------|----------|-------|
| `capture_id` | yes | Must reference a `captured` row in `docs/pilot/CAPTURE_LOG.md`. |
| `evidence_url` | yes | Public evidence URL from the capture. |
| `asset_symbol` | required for approved | Extracted asset/pair. |
| `direction` | required for approved | `long` or `short`; `flat`/`unknown` are not evaluable. |
| `entry` | required for approved | Entry price, range, or deterministic entry rule. |
| `stop` | required for approved | Stop price or invalidation rule. |
| `target` | required for approved | Target/take-profit price or deterministic target rule. |
| `source_timestamp_utc` | required for approved | Public post timestamp or defensible source timestamp. |
| `text_sha256` | yes | Raw-text SHA-256 preserved from capture. |
| `status` | yes | One extraction status from `docs/pilot/METHODOLOGY_V0.md`, or `pending_manual_extraction` before review. |
| `ambiguity_flags` | yes | Empty list for unambiguous approved records; otherwise reason flags. |
| `reviewer_id` | required for approved | Human reviewer who approves final signal record. |
| `operator_minutes` | yes | Minutes spent extracting/reviewing this candidate. |
| `notes` | yes | Reason for exclusion, ambiguity, or approval caveat. |

## Extraction Status Counts

| Status | Count | Notes |
|--------|------:|-------|
| `approved` | 0 | Manual extraction has not run yet. |
| `ambiguous` | 0 | Manual extraction has not run yet. |
| `not_a_signal` | 0 | Manual extraction has not run yet. |
| `insufficient_fields` | 0 | Manual extraction has not run yet. |
| `duplicate` | 0 | Manual extraction has not run yet. |
| `needs_rule_template` | 0 | No repeated source format classified yet. |
| `pending_capture` | 0 | Public captures now exist. |
| `pending_manual_extraction` | 60 | Captured rows awaiting manual review. |

## Draft Suggestion Counts (Parser Output)

These counts are draft parser suggestions only. They are separate from final extraction status counts above; no final status is approved, rejected, or ledger-ready until human review.

| Draft suggested status | Count | Final-status impact |
|------------------------|------:|---------------------|
| `review_candidate` | 0 | none - reviewer_id remains `pending` |
| `needs_review` | 1 | none - reviewer_id remains `pending` |
| `insufficient_fields` | 16 | none - reviewer_id remains `pending` |
| `not_a_signal` | 43 | none - reviewer_id remains `pending` |
| `rejected_draft` | 0 | none - reviewer_id remains `pending` |

## Draft Suggestion Rows

| capture_id | draft_suggested_status | parser_confidence | reviewer_id | parser_notes |
|------------|------------------------|-------------------|-------------|--------------|
| `bablos79-10442` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10443` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10444` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10445` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10446` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10447` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10448` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10449` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10450` | `insufficient_fields` | 0.49 | `pending` | asset_alias_detected, direction_short_term, missing_entry, missing_stop, missing_target |
| `bablos79-10451` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10452` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10453` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10454` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10455` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10456` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10457` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10458` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10459` | `needs_review` | 0.42 | `pending` | asset_alias_detected, direction_short_term, uncertainty_marker_detected, missing_entry, missing_stop |
| `bablos79-10460` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10461` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10463` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10464` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, close_or_reduce_term, close_or_reduce_requires_original_setup, missing_direction, missing_entry |
| `bablos79-10465` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10466` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10467` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10468` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10469` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10470` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10471` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10472` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10475` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10476` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10477` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10478` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10479` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10482` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10483` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10485` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10486` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10487` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10488` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10489` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10490` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10491` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10492` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10493` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10495` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10496` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10497` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10498` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10499` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, close_or_reduce_term, close_or_reduce_requires_original_setup, missing_direction, missing_entry |
| `bablos79-10500` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, close_or_reduce_term, close_or_reduce_requires_original_setup, missing_direction, missing_entry |
| `bablos79-10501` | `insufficient_fields` | 0.44 | `pending` | asset_alias_detected, close_or_reduce_term, close_or_reduce_requires_original_setup, missing_direction, missing_entry |
| `bablos79-10502` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10503` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10504` | `insufficient_fields` | 0.39 | `pending` | close_or_reduce_term, close_or_reduce_requires_original_setup, missing_asset_symbol, missing_direction, missing_entry |
| `bablos79-10505` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10506` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10507` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |
| `bablos79-10508` | `not_a_signal` | 0.72 | `pending` | missing_asset_symbol, missing_direction, missing_entry, missing_stop, missing_target |

## Extraction Rows

| capture_id | evidence_url | asset_symbol | direction | entry | stop | target | source_timestamp_utc | text_sha256 | status | ambiguity_flags | reviewer_id | operator_minutes | notes |
|------------|--------------|--------------|-----------|-------|------|--------|----------------------|-------------|--------|-----------------|-------------|------------------|-------|
| `bablos79-10442` | `https://t.me/bablos79/10442` | pending | pending | pending | pending | pending | `2026-04-27T07:12:22+00:00` | `b3efd9207df62a8bc98381986770a9856d6a895fd6eba5d1d845a235ec50bb39` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10443` | `https://t.me/bablos79/10443` | pending | pending | pending | pending | pending | `2026-04-27T07:37:49+00:00` | `e8cc076d6964b735e01793ea6306204aa895ffa5817f3656d8547d9ec7bc54c0` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10444` | `https://t.me/bablos79/10444` | pending | pending | pending | pending | pending | `2026-04-27T08:12:53+00:00` | `c785dddfdda0d6930af3bbfadddf809c8be0d5b408571a850bb086b8ca94e420` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10445` | `https://t.me/bablos79/10445` | pending | pending | pending | pending | pending | `2026-04-27T08:22:42+00:00` | `7240bc06c96033184438ba48ba40c034c36d48d1a7b58b48350014b510b52e24` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10446` | `https://t.me/bablos79/10446` | pending | pending | pending | pending | pending | `2026-04-27T09:35:58+00:00` | `cf0691306ee1a12f6c7afb6bf6fbefd21b9fe4375c707d4b8a73d9d8bb7981a6` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10447` | `https://t.me/bablos79/10447` | pending | pending | pending | pending | pending | `2026-04-27T10:03:37+00:00` | `4c1b16c3073103c7fa2112eb38cfdfc2fac847bb74223db72855b12f6c0a07a1` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10448` | `https://t.me/bablos79/10448` | pending | pending | pending | pending | pending | `2026-04-27T11:06:10+00:00` | `0149b7b2ee6d9efb9ca18961423c3f2dd0cd4370b1c695734d0863417d93575b` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10449` | `https://t.me/bablos79/10449` | pending | pending | pending | pending | pending | `2026-04-27T11:09:24+00:00` | `72e56d34e32a4e31b0b02ea09c6457df57d825190b53483ecbe10f0557ac91a8` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10450` | `https://t.me/bablos79/10450` | pending | pending | pending | pending | pending | `2026-04-27T11:16:37+00:00` | `f0de04a2127086f91c07862f86b26fe3568a1410c5ede6c824992f27d7f447d4` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10451` | `https://t.me/bablos79/10451` | pending | pending | pending | pending | pending | `2026-04-27T11:23:25+00:00` | `6cae57c6496b8c2551106790e961ebc8854ee996b6683a048420dabd191b7f3d` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10452` | `https://t.me/bablos79/10452` | pending | pending | pending | pending | pending | `2026-04-27T12:58:04+00:00` | `3a843c2ba81a9d72443a6c792b6b04741b02857052952b259a009c51d19e8754` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10453` | `https://t.me/bablos79/10453` | pending | pending | pending | pending | pending | `2026-04-27T15:08:57+00:00` | `be89906be98d4bc265d665e31dfc6523a957f2d417925c14d195b5128831feae` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10454` | `https://t.me/bablos79/10454` | pending | pending | pending | pending | pending | `2026-04-27T15:26:58+00:00` | `6a62902462312b50342e131ddfce6a815df27f781ca51b6e97e32aaf54239cbd` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10455` | `https://t.me/bablos79/10455` | pending | pending | pending | pending | pending | `2026-04-27T15:40:05+00:00` | `29a9f48d84913fa017f621e4e00216d3629426f24ac10388387ede56f2d75291` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10456` | `https://t.me/bablos79/10456` | pending | pending | pending | pending | pending | `2026-04-27T16:15:32+00:00` | `4f57ce3fde201a68de82ce2b258f8a963b988f08b4bdeec0169de3b3a32aaae7` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10457` | `https://t.me/bablos79/10457` | pending | pending | pending | pending | pending | `2026-04-28T06:05:11+00:00` | `981135b1151f5e7ade7a45b77974d91953e6df0a743783f576d0d66bdec68650` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10458` | `https://t.me/bablos79/10458` | pending | pending | pending | pending | pending | `2026-04-28T06:35:35+00:00` | `314619c54cb8df0aad973401084b0a32c0ba2b8282c2be4c5f9f04a2e3014330` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10459` | `https://t.me/bablos79/10459` | pending | pending | pending | pending | pending | `2026-04-28T06:44:46+00:00` | `5e4d38246fc612f4537539c758291acbd91d2c0763e6d0c9b9ca8414be95b471` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10460` | `https://t.me/bablos79/10460` | pending | pending | pending | pending | pending | `2026-04-28T06:54:17+00:00` | `2994d72d218ae1ae294241527ae0c863c958b4e292dd68dfbd86ad9cd0d5c360` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10461` | `https://t.me/bablos79/10461` | pending | pending | pending | pending | pending | `2026-04-28T07:18:30+00:00` | `bcd28f0ae86c9e4e82c2c26e1886c87ae367f0c0862f4126fe4d36cb98d6eb16` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10463` | `https://t.me/bablos79/10463` | pending | pending | pending | pending | pending | `2026-04-28T14:16:30+00:00` | `587105d1433275166f7d649a4d16bbbaaa90c2639760f42c012d6ff19348a8e6` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10464` | `https://t.me/bablos79/10464` | pending | pending | pending | pending | pending | `2026-04-28T16:04:15+00:00` | `375b7806d8438cd0f640e31038bb0a6e8366ace2d11d51d60f9b9c527201ff4e` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10465` | `https://t.me/bablos79/10465` | pending | pending | pending | pending | pending | `2026-04-29T07:30:41+00:00` | `b26087182a1d71069e57e2dd5e739c9427414e5f96934fd3a037b07e1dc966c2` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10466` | `https://t.me/bablos79/10466` | pending | pending | pending | pending | pending | `2026-04-29T09:31:05+00:00` | `22a52915b201add32224fe70b2d4bd20f51b5b25d0a1443d0d17e3066e5bda0b` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10467` | `https://t.me/bablos79/10467` | pending | pending | pending | pending | pending | `2026-04-29T09:44:27+00:00` | `81cc2fcf0ddacc3511b991e6e3953235fbc452dc4001a893a94fd91c73e25410` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10468` | `https://t.me/bablos79/10468` | pending | pending | pending | pending | pending | `2026-04-29T10:10:07+00:00` | `c89e9cd6a04c988cdd6ed2efb30505cb64536a894fbc4c559932431cec027298` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10469` | `https://t.me/bablos79/10469` | pending | pending | pending | pending | pending | `2026-04-29T10:34:29+00:00` | `0b5aa688f63697610fe62dc5c368856762d9541ed17e475691785255add216ee` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10470` | `https://t.me/bablos79/10470` | pending | pending | pending | pending | pending | `2026-04-29T10:49:41+00:00` | `54790a51f20dc62a35d9c1c5d267ac627302015633850a412b362e860a12960d` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10471` | `https://t.me/bablos79/10471` | pending | pending | pending | pending | pending | `2026-04-29T12:13:40+00:00` | `e5d93244a7998d1c34889d863e3c164f95c22e29b828021962cfd1a1f6030c84` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10472` | `https://t.me/bablos79/10472` | pending | pending | pending | pending | pending | `2026-04-29T13:40:03+00:00` | `1ee4fcb3aa2f8026adb30e4fc0f9b7af506f1dc17e63e267be4bba931be17ea0` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10475` | `https://t.me/bablos79/10475` | pending | pending | pending | pending | pending | `2026-04-29T18:36:49+00:00` | `dce8cdd67a81f02d5173f19b90cb8f9298afc16180edd64be985a10629fb27ae` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10476` | `https://t.me/bablos79/10476` | pending | pending | pending | pending | pending | `2026-04-30T07:34:30+00:00` | `fced0cd89e597531ae3082941397f7c9f0804a1b41779edfea295cb55c95b4fe` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10477` | `https://t.me/bablos79/10477` | pending | pending | pending | pending | pending | `2026-04-30T07:57:35+00:00` | `4029171bf7202547ef279d8a62e02cd80abc139fd2c93a6dac24b7770315b563` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10478` | `https://t.me/bablos79/10478` | pending | pending | pending | pending | pending | `2026-04-30T09:46:50+00:00` | `bcccb754e9c8fec7d32e8c2ea9852c2b24667fd490edd8863c232ee302c96718` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10479` | `https://t.me/bablos79/10479` | pending | pending | pending | pending | pending | `2026-04-30T10:42:21+00:00` | `da772f0d9e752d072dddf0f41915513405e67cc67202c3ec35019d381e655b8c` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10482` | `https://t.me/bablos79/10482` | pending | pending | pending | pending | pending | `2026-05-02T06:42:00+00:00` | `a4b8fd5c114751814fcfe35e3a5fc6e15b9e9d92996a7216a10887d3a669c24f` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10483` | `https://t.me/bablos79/10483` | pending | pending | pending | pending | pending | `2026-05-02T13:00:12+00:00` | `5667c87486143ec8e10631c52de30e2ba5219d6f6550de9829e60bb917287a32` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10485` | `https://t.me/bablos79/10485` | pending | pending | pending | pending | pending | `2026-05-04T08:13:14+00:00` | `30cd37eac992847668be9edd79d432a78aad9e7e7819312a3d1cd1a168629645` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10486` | `https://t.me/bablos79/10486` | pending | pending | pending | pending | pending | `2026-05-04T09:20:20+00:00` | `664beec95f743f383930f568f677d93b233b54d06ef24d16d2b19547df789fd0` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10487` | `https://t.me/bablos79/10487` | pending | pending | pending | pending | pending | `2026-05-04T11:05:13+00:00` | `cfaad0156d0f44ee79710ad5d08ca07546672797fbe59fe8032998cb94ffe9a0` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10488` | `https://t.me/bablos79/10488` | pending | pending | pending | pending | pending | `2026-05-04T11:13:39+00:00` | `23ca9bd011c477dd2be12f72f5402757e81bb2c7bda84cfade4c305e5736362d` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10489` | `https://t.me/bablos79/10489` | pending | pending | pending | pending | pending | `2026-05-04T12:45:53+00:00` | `d49d71e85992e6da607784cc21fd15c1fa999d194e26fa2ac187bd3aaf066fbf` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10490` | `https://t.me/bablos79/10490` | pending | pending | pending | pending | pending | `2026-05-04T13:56:36+00:00` | `683f1e126ea775817f58016fe45d22ef07d1cce3ee2a4b9bec64bbea2e17b008` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10491` | `https://t.me/bablos79/10491` | pending | pending | pending | pending | pending | `2026-05-04T14:33:46+00:00` | `24f1b54621d697fb0de9461c36f599d1604645fe7610caa79989da3c237b066e` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10492` | `https://t.me/bablos79/10492` | pending | pending | pending | pending | pending | `2026-05-04T15:20:20+00:00` | `83b4068532e725a76133aa315f663dcfdb82effc7d62725a52215e550c15ec46` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10493` | `https://t.me/bablos79/10493` | pending | pending | pending | pending | pending | `2026-05-04T16:11:44+00:00` | `34e43305e8f08d4a1e3551e4855ca41ca86d39dbecd1f88f773648862b16bca6` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10495` | `https://t.me/bablos79/10495` | pending | pending | pending | pending | pending | `2026-05-05T05:06:35+00:00` | `7544545bea2fccbf781da94d9c908d757013464cd17bf9c2c68f8d287fea82ba` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10496` | `https://t.me/bablos79/10496` | pending | pending | pending | pending | pending | `2026-05-05T07:11:04+00:00` | `8a182b4496f304dc9675a3181be7052000305da5419ec11e53ac3c70cf91f31d` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10497` | `https://t.me/bablos79/10497` | pending | pending | pending | pending | pending | `2026-05-05T08:06:18+00:00` | `0167db24e8bf4e9e016c5cbf4da9f00342263525bda1fa8980f1ef216eaa8ed5` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10498` | `https://t.me/bablos79/10498` | pending | pending | pending | pending | pending | `2026-05-05T08:25:36+00:00` | `627ad313c6a7a1a67498b5f096741bc767c3c6023e21a07627531a4bf9ee9415` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10499` | `https://t.me/bablos79/10499` | pending | pending | pending | pending | pending | `2026-05-05T08:31:27+00:00` | `884b974dda969c24208324a6ca27a3e6274e44485a389ab5dd107816c6f0cb51` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10500` | `https://t.me/bablos79/10500` | pending | pending | pending | pending | pending | `2026-05-05T12:43:44+00:00` | `d83aa742b3b62cc11c256c20b1e48388d4a3f2cddfcef217d0339fce9d339dbb` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10501` | `https://t.me/bablos79/10501` | pending | pending | pending | pending | pending | `2026-05-05T12:55:18+00:00` | `ab0d4d95c21c133f8fa8faa77e3be944d0dc1bd153bed5c069182d645dd341fd` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10502` | `https://t.me/bablos79/10502` | pending | pending | pending | pending | pending | `2026-05-05T13:15:14+00:00` | `53150f5b948c504706a6341bf2bc83c4f5fb05ae3b79f362d65909f187dbd1fa` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10503` | `https://t.me/bablos79/10503` | pending | pending | pending | pending | pending | `2026-05-05T13:16:37+00:00` | `19b3a107864a752f4f13395a96ae49e47a32d9c7a71a54f78fa25649dac453e7` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10504` | `https://t.me/bablos79/10504` | pending | pending | pending | pending | pending | `2026-05-05T15:29:49+00:00` | `fb3f5b4c48c0909d6d869a5349ec07e1733d07a94f35e9722e036438c406c299` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10505` | `https://t.me/bablos79/10505` | pending | pending | pending | pending | pending | `2026-05-05T18:21:20+00:00` | `072ba1c45b4f5a50ee655c6e3d86484ca1238e3237105bbf17259568463ae545` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10506` | `https://t.me/bablos79/10506` | pending | pending | pending | pending | pending | `2026-05-06T06:15:03+00:00` | `d6878e9eb042da2aa11fe3e13d5827482da014176a6e8d6a27820a5cff3d5d2e` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10507` | `https://t.me/bablos79/10507` | pending | pending | pending | pending | pending | `2026-05-06T06:27:27+00:00` | `6e8bdea5257f67dfdc94a2fd5210b75bcc929eb45197513c5ef5f71c6b746617` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |
| `bablos79-10508` | `https://t.me/bablos79/10508` | pending | pending | pending | pending | pending | `2026-05-06T06:57:32+00:00` | `64110f41bea0d2341261991d60d733023f5f67a415f68fe33bc11de8076f7ede` | `pending_manual_extraction` | `[]` | pending | 0 | Awaiting manual extraction/reviewer classification. |

## Blocker

There is no capture blocker anymore for the first batch. The current blocker is
manual extraction/reviewer classification: each captured post must be classified
as `approved`, `ambiguous`, `not_a_signal`, `insufficient_fields`, `duplicate`,
or `needs_rule_template` before report metrics can be produced.

Do not use LLM output as truth. Do not approve records without asset, direction,
entry, stop, target, timestamp, evidence reference, and reviewer approval.

## Future Rule-Template Candidates

None observed yet.

Rule-template candidates may be added only after real captured posts show a
repeated format that would reduce manual extraction time without weakening
human review or evidence preservation.
