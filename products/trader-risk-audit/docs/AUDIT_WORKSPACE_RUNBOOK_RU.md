# Audit Workspace Runbook RU

## Назначение

Этот runbook описывает локальную folder convention для ручного pilot audit.
Workspace нужен, чтобы intake request, входные файлы, operator notes,
generated artifacts и final output были предсказуемо разложены. No database,
SaaS surface, hosted storage, multi-tenant auth, and no network dependency.

## Layout

Для каждого audit id оператор создает отдельную директорию:

```text
pilot_workspaces/
  audit_YYYYMMDD_label/
    input/
    output/
    operator_notes/
    artifacts/
    metadata.json
```

- `input/` - trade export, written risk rules, intake request и privacy
  acknowledgement.
- `output/` - final report, delivery packet и файлы, которые можно показать
  клиенту после operator approval.
- `operator_notes/` - внутренние заметки оператора, review decisions и список
  unresolved questions.
- `artifacts/` - normalized trades, violations, attribution summary, manifest и
  промежуточные deterministic artifacts.
- `metadata.json` - audit id, created timestamp, status и non-sensitive file
  references.

`metadata.json` не должен содержать raw trade rows, account balances, реальные
имена, email, Telegram handles, broker account ids, free-text notes или source
file contents.

## Manual Handoff

1. Intake: оператор получает заполненный `templates/intake_request.yaml`,
   written risk rules и trade export.
2. Workspace setup: оператор создает локальный workspace для audit id и кладет
   исходные файлы в `input/`.
3. Review: оператор проверяет timezone, session fields, broker/platform,
   account currency, audit period и ambiguous rules.
4. Approval: ambiguous export mappings, ambiguous rules и report delivery
   фиксируются как deterministic approval artifact в `operator_notes/`.
5. Audit run: локальный audit workflow пишет normalized artifacts, violations,
   attribution и manifest в `artifacts/` или `output/`.
6. Report review: оператор проверяет claim boundaries, limitations и source-row
   traceability.
7. Delivery: approved report и copy-ready delivery text переносятся в `output/`
   для ручной доставки.

## Status Values

- `intake_received`
- `needs_operator_review`
- `ready_to_run`
- `audit_generated`
- `delivery_approved`
- `delivered`
- `closed`

Status updates остаются локальными metadata changes. Они не создают hosted
state, user accounts, external queues или Telegram automation.
