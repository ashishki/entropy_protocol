# Customer Feedback Log - First Report

Дата: 2026-05-07
Статус: pending customer review
Source: `bablos79` (`https://t.me/bablos79`)

## Current State

Customer feedback has not been collected.

Reason: the first-source report is currently a blocked-report memo
(`docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md`) because no real public
captures were supplied. No customer decision impact can be claimed yet.

## Feedback Rows

| feedback_id | source_id | report_artifact | review_status | customer_decision_before | customer_decision_after | decision_impact | objections | useful_sections | confusing_sections | format_preference | next_requested_source | notes |
|-------------|-----------|-----------------|---------------|--------------------------|-------------------------|-----------------|------------|-----------------|--------------------|-------------------|-----------------------|-------|
| `feedback-pending-001` | `bablos79` | `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md` | `pending-customer-review` | pending | pending | pending | pending | pending | pending | pending | pending | Waiting for operator-supplied captures, real report delivery, and customer review. |

## Past-Behavior Questions

Use these questions after a real report is delivered. They ask about what the
customer did or decided, not what they hypothetically might do.

1. Когда вы в последний раз рассматривали оплату или продление signal source?
2. Какой конкретный источник вы проверяли до этого отчета?
3. Что вы уже сделали, чтобы проверить этот источник вручную?
4. Сколько времени вы потратили на проверку старых постов или сигналов?
5. Какое решение вы уже приняли до отчета: оплатить, не оплатить, продлить,
   отменить, подождать или проверить другой источник?
6. Что в отчете изменило или не изменило это решение?
7. Какой раздел вы реально прочитали до конца?
8. Какому выводу вы не доверяете и почему?
9. Какой формат вы фактически открыли и прочитали: Telegram message, Markdown,
   PDF-style document, spreadsheet, chart/table?
10. Какой следующий public source вы уже хотите проверить, если такой есть?

Avoid questions like "would you pay?" or "would you use this?" Record actual
payment, deposit, repeat request, referral, refusal, or changed decision in
`docs/pilot/PAYMENT_SIGNAL_LOG.md`.

## Objection Categories

| Objection | Meaning |
|-----------|---------|
| `no_real_report_yet` | Customer cannot evaluate value because only a blocker memo exists. |
| `needs_public_captures` | Customer/operator must supply public post evidence first. |
| `methodology_dispute` | Customer disputes extraction or deterministic outcome assumptions. |
| `wants_private_source` | Customer asks for private/paywalled/login-walled capture. |
| `wants_prediction` | Customer asks for future performance or trade recommendation. |
| `format_not_read` | Customer did not read the delivered artifact. |
| `not_actionable` | Report did not change subscribe/cancel/avoid/repeat decision. |

## Telegram Delivery

Telegram may be used as a delivery format for a private summary or report link
after a real report exists. Telegram delivery does not approve Telegram bot
ingestion, private scraping, autonomous monitoring, public leaderboard, or
marketplace behavior.

Record whether the customer actually opened/read the Telegram-delivered summary
or artifact. Do not treat "send it in Telegram" as payment evidence by itself.
