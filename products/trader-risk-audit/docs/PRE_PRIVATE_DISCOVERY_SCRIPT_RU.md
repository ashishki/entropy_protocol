# Pre-Private Discovery Script RU

Status: active
Date: 2026-05-19
Audience: founder/operator

## Цель

Проверить, есть ли у трейдера, оператора, coach, prop/funded команды, DAO или
fund/treasury реальная боль вокруг post-trade risk review.

Не продавать SaaS. Не обещать advice, live monitoring, order blocking,
улучшение доходности или подключение к бирже. Цель разговора - past behavior,
текущий workflow, доверие к отчету и готовность к approved anonymized export.

## Кого звать

Приоритет:

1. Люди, которые уже ведут journal, выгружают CSV, используют Dune/Excel/Python
   или вручную разбирают rule breaches.
2. Люди, у которых есть written rules, funded/prop ограничения, risk limits,
   governance policy или weekly/monthly review.
3. Люди, которые могут принять решение о ручном audit report или дать
   approved anonymized export.

Не тратить время на людей, которые:

- не имеют executed trades or transaction history;
- не имеют никаких правил или review workflow;
- хотят сигналы, прогнозы, стратегию, live alerts или order blocking;
- не могут обсуждать past behavior без раскрытия приватных данных.

## Opening

Короткая формулировка:

> Мы проверяем post-trade audit: вы даете executed trades/export и свои risk
> rules, а на выходе получаете reviewed report: какие правила были нарушены,
> где это видно в source rows, какие ограничения есть у данных. Это не advice,
> не live trading и не подключение к управлению счетом.

## Past-Behavior Questions

1. Когда последний раз вы разбирали сделку, день или неделю, где был risk/rule
   breach?
2. Что именно пошло не так: размер позиции, drawdown, daily loss, forbidden
   asset, cooldown, leverage, session/time rule, другое?
3. Как вы это проверили тогда: exchange dashboard, CSV, journal, Excel, Python,
   Dune, screenshots, manual notes?
4. Сколько времени занял review?
5. Кто смотрел результат: вы сами, coach, prop evaluator, partner, investors,
   DAO/fund stakeholders?
6. Что произошло, если breach был найден поздно или не был найден?
7. Какие поля в export нужны вам, чтобы доверять такому отчету: fees, realized
   P&L, leverage, margin, order ids, source rows, position ids?

## Current Workflow Questions

1. Как часто вы сейчас делаете post-trade/risk review?
2. Где сейчас живут ваши written rules или limits?
3. Какие проверки уже автоматизированы, а какие делаются вручную?
4. Что в текущем workflow самое неприятное: export friction, mapping columns,
   P&L reconciliation, trust, time, формат отчета, privacy?
5. Что должно быть в отчете, чтобы вы реально открывали его каждую неделю или
   после trading session?

## Report Review Questions

Показывать только open-source/demo reports с явной пометкой, что это не private
pilot evidence.

1. Понятно ли за 60 секунд, что проверялось и какие ограничения у данных?
2. Какие finding rows вы бы использовали в реальном review?
3. Где отчет выглядит недостоверным или слишком слабым?
4. Какие поля/разделы отсутствуют для вашего workflow?
5. Какой итоговый action вы ожидали бы после такого отчета?

## Export Willingness Ask

Использовать только после того, как есть реальная боль и workflow fit:

> Если мы дадим redaction checklist и сохраним файл вне git/вне SaaS, вы смогли
> бы подготовить anonymized export для одного периода, чтобы мы вернули
> reviewed report? Нам не нужны credentials, account ids, имена, email,
> screenshots или payment details.

Фиксировать ответ как safe aggregate:

- `export_willing_yes`
- `export_willing_later`
- `export_blocked_privacy`
- `export_blocked_effort`
- `export_blocked_no_rules`
- `export_blocked_no_value`

## Manual Pilot Ask

Использовать только если человек признал боль и export willingness:

> Следующий шаг - один manual audit report по approved anonymized export и
> written rules. Это не SaaS и не advice. Вы бы хотели пройти такой pilot, если
> turnaround 48-72 часа после complete input?

Допустимые safe tags:

- `pilot_yes_paid`
- `pilot_yes_free_first`
- `pilot_later`
- `pilot_no_price`
- `pilot_no_trust`
- `pilot_no_urgency`
- `pilot_needs_team_approval`

## What To Record

Записывать только safe aggregate notes:

- ICP label;
- past incident type;
- current workaround;
- review frequency;
- blocker tags;
- report usefulness score from 1 to 5;
- export willingness tag;
- pilot ask result tag;
- next action.

Не записывать:

- имя, email, Telegram handle, company, account id, wallet ownership, exchange
  account, exact P&L, private strategy, screenshots, raw trades, private paths,
  payment identifiers, credentials.

