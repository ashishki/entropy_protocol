# Before/After Report Comparison RU

Назначение: показать, почему Trader Risk Audit полезнее raw trade export на
разговоре про paid pilot. Страница использует public sample data из
`demo/public_sample_001`; здесь no real customer data, no Telegram handles,
no broker account ids, no emails и no private exports.

## Before: Raw Trade Export

Raw trade export обычно показывает поля:

| Timestamp | Symbol | Side | Quantity | Price |
|---|---|---|---|---|
| public sample row | RISKY | buy | sample quantity | sample price |

Что raw export не объясняет:

- какое written rule было проверено;
- был ли rule breach deterministic;
- какие source rows подтверждают finding;
- была ли сделка после daily loss, drawdown, cooldown, position size или
  forbidden-asset rule;
- violation-attributed P&L для flagged row.

## After: Audit Report

Audit report добавляет deterministic rule checks, source row ids и
violation-attributed P&L:

| Raw export gap | Audit report output |
|---|---|
| Trade row не имеет rule context. | Rule ID и rule type показывают checked policy. |
| Row evidence сложно обсуждать. | Source row ids связывают flag с input row. |
| P&L не связан с discipline. | P&L impact показывает violation-attributed P&L. |
| Missing data можно пропустить. | Limitations явно показывают unsupported или missing fields. |
| Следующий шаг расплывчатый. | Next review checklist показывает, что проверить оператору. |

This audit is not investment advice and does not control live trading. Здесь
no performance promise, no broker APIs, no signal parsing, no order blocking и
no auto-advice.

## Paid Pilot CTA

Пришлите real trade export и written risk rules для одного paid pilot manual
audit. Deliverable - deterministic report с rule breaches, source rows, P&L
impact, limitations и next-review checklist. Цель - понять, стоит ли audit
оплаты, а не обсуждать новые features.
