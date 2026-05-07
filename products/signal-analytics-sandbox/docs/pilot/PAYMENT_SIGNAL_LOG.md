# Payment Signal Log - Telegram Pilot

Дата: 2026-05-07
Статус: pending real customer/payment signal

## Current State

No payment signal is recorded yet.

Reason: the first source report is blocked on missing operator-supplied public
captures, so no real customer report delivery or feedback has occurred.

## Signal Status Definitions

| Status | Counts as strong payment signal? | Meaning |
|--------|----------------------------------|---------|
| `paid` | yes | Customer paid for the report or next report. |
| `deposit` | yes | Customer paid a deposit before or during report production. |
| `written_intent_to_pay` | yes, if specific | Customer wrote a concrete intent with amount/source/timing. |
| `repeat_request` | yes, if tied to delivery | Customer asked for another source after reviewing a report. |
| `referral` | yes, if concrete | Customer introduced another qualified buyer or named prospect. |
| `no-payment` | no | Customer did not pay or commit after review. |
| `false-positive_enthusiasm` | no | Customer said the idea was interesting but gave no behavior signal. |
| `pending-customer-review` | no | Report has not been reviewed by customer yet. |
| `pending-operator-input` | no | Operator has not supplied captures/report inputs yet. |

## Payment Signal Rows

| signal_id | source_id | report_artifact | status | amount | currency | customer_action_date | evidence_reference | decision_impact | next_requested_source | notes |
|-----------|-----------|-----------------|--------|--------|----------|----------------------|-------------------|-----------------|-----------------------|-------|
| `payment-pending-001` | `bablos79` | `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md` | `pending-operator-input` | pending | pending | pending | pending | pending | pending | Waiting for public captures, real report delivery, and customer review. |

## Refusal Reasons

If the customer refuses to pay or continue, record one or more:

- `report_blocked_no_captures`;
- `too_many_ambiguous_records`;
- `wants_private_or_paywalled_source`;
- `wants_prediction_or_recommendation`;
- `methodology_not_trusted`;
- `report_too_technical`;
- `not_decision_relevant`;
- `price_too_high`;
- `just_curious_no_budget`;
- `format_not_read`.

## Telegram Delivery Signal

Telegram delivery is a format preference only. It may be useful if the customer
actually reads the private summary or report there, but it does not authorize:

- Telegram bot ingestion;
- private-source scraping;
- continuous monitoring;
- marketplace or leaderboard;
- copy trading;
- investment advice.

Record delivery format separately from payment status. A request for Telegram
delivery without paid/deposit/repeat/referral behavior is not a payment signal.
