# bablos79 Review Queue - Draft Exceptions

Date: 2026-05-08
Status: draft-only, pending human review
Source artifact: `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`

## Boundary

This queue is for human exception review only. It does not approve records, write ledger rows, or create customer-facing performance claims. Every row remains reviewer_id=`pending` until a human reviewer records a final extraction status.

## Inclusion Policy

- include all `needs_review` and `insufficient_fields` draft statuses;
- include every low-confidence row with confidence `<0.50`;
- include close/reduce, uncertainty, or trade-management contexts that may require linked-post judgment;
- include every row with an asset candidate because those are likely customer-facing review candidates;
- include a deterministic sample of non-signal rows for quality control.

Total queue rows: 23 of 60.

## Queue Rows

| capture_id | suggested_status | inclusion_reasons | assets | direction | missing_fields | confidence | reviewer_id | evidence_url |
|------------|------------------|-------------------|--------|-----------|----------------|------------|-------------|--------------|
| `bablos79-10442` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | X5 | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10442 |
| `bablos79-10443` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | VTBR | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10443 |
| `bablos79-10446` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | VTBR | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10446 |
| `bablos79-10450` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | MAGN | short | entry, stop, target | 0.49 | `pending` | https://t.me/bablos79/10450 |
| `bablos79-10451` | `not_a_signal` | sampled_non_signal | - | unknown | asset_symbol, direction, entry, stop, target | 0.72 | `pending` | https://t.me/bablos79/10451 |
| `bablos79-10453` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | VKCO | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10453 |
| `bablos79-10458` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | X5 | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10458 |
| `bablos79-10459` | `needs_review` | exception_status, low_confidence, contradictory_or_management_context, customer_facing_candidate | AMD | short | entry, stop, target | 0.42 | `pending` | https://t.me/bablos79/10459 |
| `bablos79-10461` | `not_a_signal` | sampled_non_signal | - | unknown | asset_symbol, direction, entry, stop, target | 0.72 | `pending` | https://t.me/bablos79/10461 |
| `bablos79-10464` | `insufficient_fields` | exception_status, low_confidence, contradictory_or_management_context, customer_facing_candidate | X5 | close_or_reduce | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10464 |
| `bablos79-10467` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | MAGN | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10467 |
| `bablos79-10472` | `not_a_signal` | sampled_non_signal | - | unknown | asset_symbol, direction, entry, stop, target | 0.72 | `pending` | https://t.me/bablos79/10472 |
| `bablos79-10487` | `not_a_signal` | sampled_non_signal | - | unknown | asset_symbol, direction, entry, stop, target | 0.72 | `pending` | https://t.me/bablos79/10487 |
| `bablos79-10489` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | GAZP | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10489 |
| `bablos79-10490` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | GAZP | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10490 |
| `bablos79-10492` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | SBER | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10492 |
| `bablos79-10497` | `insufficient_fields` | exception_status, low_confidence, customer_facing_candidate | MAGN | unknown | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10497 |
| `bablos79-10498` | `not_a_signal` | sampled_non_signal | - | unknown | asset_symbol, direction, entry, stop, target | 0.72 | `pending` | https://t.me/bablos79/10498 |
| `bablos79-10499` | `insufficient_fields` | exception_status, low_confidence, contradictory_or_management_context, customer_facing_candidate | SFIN | close_or_reduce | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10499 |
| `bablos79-10500` | `insufficient_fields` | exception_status, low_confidence, contradictory_or_management_context, customer_facing_candidate | CHMF | close_or_reduce | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10500 |
| `bablos79-10501` | `insufficient_fields` | exception_status, low_confidence, contradictory_or_management_context, customer_facing_candidate | MAGN | close_or_reduce | direction, entry, stop, target | 0.44 | `pending` | https://t.me/bablos79/10501 |
| `bablos79-10504` | `insufficient_fields` | exception_status, low_confidence, contradictory_or_management_context | - | close_or_reduce | asset_symbol, direction, entry, stop, target | 0.39 | `pending` | https://t.me/bablos79/10504 |
| `bablos79-10508` | `not_a_signal` | sampled_non_signal | - | unknown | asset_symbol, direction, entry, stop, target | 0.72 | `pending` | https://t.me/bablos79/10508 |

## Rule-Template Candidates

- Hashtag asset detection is recurring and safe only as an asset-candidate rule.
- Close/reduce phrases (`закрыл`, `часть закрыл`, `зафиксировал`) recur, but require linked original setup context before they can become evaluable records.
- Uncertainty/cancellation phrases (`отбой`, `пока не буду`) should suppress automatic positive signal classification.
- Broadcast/noise markers (`стрим`, `разбор`) can become exclusion helpers, not positive signal rules.
