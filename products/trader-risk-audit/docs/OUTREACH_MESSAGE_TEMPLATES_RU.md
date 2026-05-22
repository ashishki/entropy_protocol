# Outreach Message Templates RU

Status: complete_for_operator_use
Date: 2026-05-19
Phase: 30

## Rules

Use these manually. Do not automate outreach from this repo.

Do not promise:

- trading advice;
- signals;
- performance improvement;
- live monitoring;
- broker or exchange control;
- order blocking;
- SaaS account;
- checkout;
- private report delivery before manual review.

## Cold/Warm Short Message

```text
Привет. Я проверяю маленький post-trade audit tool для трейдеров/операторов:
берем executed trades/export и written risk rules, а на выходе даем отчет,
где видно какие правила нарушались, на каких source rows, и какие ограничения
есть у данных.

Это не сигналы, не advice и не live trading. Я сейчас не продаю SaaS, а хочу
понять, как ты сейчас делаешь risk/rule review после торговой недели или
инцидента.

Могу задать 5-7 вопросов про твой текущий workflow?
```

## Report Review Ask

```text
У меня есть несколько demo/open-data отчетов. Они не являются customer case и
не доказывают market demand. Я хочу проверить только понятность формата:
видно ли что проверялось, где source rows, какие limitations, и был бы такой
report полезен в твоем review workflow.

Можешь посмотреть один отчет 10-15 минут и сказать, что в нем полезно,
непонятно или недостаточно достоверно?
```

## Export Willingness Ask

Use only after the person describes a real review pain.

```text
Если мы дадим redaction checklist и сохраним файл вне git/вне SaaS, ты смог бы
подготовить anonymized export за один период, чтобы мы вернули reviewed report?

Нам не нужны credentials, account ids, имена, email, screenshots или payment
details. Если каких-то полей нет, мы явно отметим limitations.
```

## Manual Pilot Ask

Use only after export willingness is credible.

```text
Следующий шаг - один manual audit по approved anonymized export и written rules.
Deliverable: reviewed report с source-row traceability, limitations и
claim-safe summary. Turnaround target 48-72 часа после complete input.

Это не SaaS, не advice, не live monitoring и не order blocking.

Хочешь пройти такой pilot?
```

## Follow-Up After No Reply

```text
Пингую один раз и больше не буду дергать. Мне не нужен приватный export на этом
этапе. Хочу понять только текущий workflow: как ты сейчас проверяешь rule/risk
breaches после торгов?
```

## Safe Outcome Tags

Record only safe tags:

- `reply_yes_interview`
- `reply_yes_report_review`
- `reply_no_time`
- `reply_no_pain`
- `reply_wants_signals`
- `reply_wants_saas`
- `reply_privacy_concern`
- `reply_export_possible`
- `reply_export_blocked`
- `reply_pilot_yes`
- `reply_pilot_no`

