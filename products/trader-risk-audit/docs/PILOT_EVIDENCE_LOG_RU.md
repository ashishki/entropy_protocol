# Pilot Evidence Log RU

## Назначение

Этот validation artifact нужен, чтобы бизнес-доказательства не исчезли за
инженерной работой. Каждый qualified prospect и каждый audit offer должны быть
записаны в customer log без реальных имен, Telegram handles, emails, broker
account ids, exports, raw trade rows или payment identifiers.

## Required Fields

- `prospect_source` - откуда пришел prospect: warm network, coach referral,
  trading group, prior customer, outbound.
- `icp` - тип клиента: prop/funded trader, coach/team lead, crypto/futures
  trader, systematic retail trader.
- `call_date` - дата past-behavior call.
- `export_provided` - предоставил ли prospect trade export.
- `rules_provided` - предоставил ли written risk rules.
- `paid_amount` - оплаченная сумма за manual audit или `0`, если оплаты не было.
- `objections` - краткие non-sensitive objections: privacy, price, export mess,
  attribution dispute, wants live blocking, wants backtesting.
- `report_delivered` - был ли audit report delivered.
- `repeat_requested` - запросил или запланировал ли prospect повторный audit.
- `referral` - дал ли prospect referral к трейдеру, coach или team lead.

## Advancement Gate

Проект проходит дальше только если есть 3 paid audit reports from 10 qualified
prospects within 14 days, then at least 2 repeat audit commitments within
30 days.

Если gate не выполнен, приоритет - calls, objections и paid report delivery, а
не новые features, live broker/API lockout, Telegram signal analytics,
strategy/backtest generator или SaaS dashboard.

## Logging Rules

- Записывать только anonymized labels, counts, yes/no fields и non-sensitive
  objection categories.
- Не записывать real customer names, Telegram handles, emails, broker accounts,
  exports, raw trade rows, screenshots, payment identifiers или private notes.
- Payment evidence хранится отдельно у оператора; в CSV фиксируется только
  amount bucket/value без transaction id.
