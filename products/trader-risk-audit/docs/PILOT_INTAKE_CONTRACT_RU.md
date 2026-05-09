# Pilot Intake Contract RU

## Назначение

Этот intake contract описывает минимальный набор данных, который трейдер должен
передать оператору до ручного Trader Risk Audit. Цель - получить проверяемый
trade export и written risk rules, чтобы оператор мог подготовить локальный
детерминированный audit report.

Это не SaaS onboarding, не создание user account и не автоматическая отправка
отчета. Текущий стабильный intake использует файлы; ADR-002 отдельно планирует
будущий read-only exchange import для исторических сделок, но не разрешает
broker/exchange control, trading, withdrawals, transfers или live account
management. Передача файлов и итогового report остается ручным pilot workflow.

## Required Files

1. Trade export за audit period.
   Поддерживаемые типы: `.csv`; `.xlsx` принимается только как candidate export
   для ручной проверки, если CSV недоступен.
2. Written risk rules в свободной форме или по шаблону
   `templates/risk_rules_template_ru.md`.
3. Заполненный intake request по структуре `templates/intake_request.yaml`.

Не передавайте API keys, passwords, seed phrases, broker tokens, screenshots с
личными данными, паспортные данные или платежные документы через обычный intake.
Если read-only exchange import будет включен по ADR-002, ключи должны вводиться
только локально через утвержденный secret path.

## Required Metadata

- `trader_label` - псевдоним без реального имени или handle.
- `broker_or_platform` - брокер, prop platform или trading platform, из которой
  получен export.
- `export_file_name` - имя файла export.
- `export_file_type` - `csv` или `xlsx_candidate`.
- `account_currency` - валюта счета, например `USD`, `EUR`, `USDT`.
- `timezone` - timezone для интерпретации trading day, например `UTC` или
  `Europe/Berlin`.
- `session_start` и `session_end` - границы торговой сессии.
- `audit_period_start` и `audit_period_end` - даты периода аудита.
- `risk_rules_file` - файл или текстовый блок с written risk rules.
- `known_export_limitations` - что может быть неполным в export, если известно.

## Written Risk Rule Requirements

Правила должны быть написаны в языке трейдера, но достаточно конкретно, чтобы
оператор мог перевести их в deterministic policy только после проверки.

Для каждого правила желательно указать:

- правило действовало раньше, действует сейчас или было изменено;
- точный threshold, например max daily loss, max drawdown, max position size;
- unit: money, percent, contracts/lots, minutes, symbols;
- когда правило применяется: session/day/week/account/instrument;
- что считается нарушением;
- примеры исключений, если они есть.

Ambiguous rules, unsupported export columns, new rule semantics и paid report
delivery требуют явного operator approval до evaluation или delivery. Approval
должен быть зафиксирован как deterministic artifact/configuration, а не как
память из переписки.

## Operator Checklist

- Файлы получены и сохранены локально в operator-controlled workspace.
- Export type поддерживается или помечен как candidate для ручной проверки.
- Audit period, timezone, session fields, broker/platform и account currency
  заполнены.
- Trader подтвердил, что export не содержит API secrets или лишние PII.
- Written risk rules получены и спорные места вынесены на operator approval.
- Перед запуском audit workflow нет unresolved policy review items.
- Перед delivery оператор проверил report claim boundaries и limitations.

## Privacy and Disclaimer Summary

Pilot inputs and generated reports are local-only by default. Trader Risk Audit
не является investment advice, не управляет broker/exchange account, не
управляет live orders и не блокирует сделки.
