# Audit Workspace Runbook RU

## Назначение

Этот runbook описывает локальную folder convention для ручного pilot audit.
Workspace нужен, чтобы intake request, входные файлы, operator notes,
generated artifacts и final output были предсказуемо разложены. No database,
SaaS surface, hosted storage, multi-tenant auth, and no network dependency.

## Intake Methods

Оператор может принять audit input двумя разными способами:

1. **CSV upload / file export** - stable path для большинства pilots. Trader
   передает готовый `.csv` export и written risk rules. Риск ниже: нет API
   credentials, нет exchange connection setup, нет permission review.
2. **Read-only API import** - optional path для Binance/Bybit historical
   fills/executions. Trader создает read-only key, отключает trading/order,
   withdrawal, transfer, leverage/margin и account-mutation permissions,
   preferably включает IP allowlisting, а оператор запускает local import.

Эти методы нельзя смешивать в metadata как один source. Укажите intake method
явно: `csv_export`, `bybit_read_only_api` или `binance_read_only_api`.
Если trader не хочет создавать API key, используйте CSV upload path.

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

For read-only API import, `metadata.json` may store only non-sensitive local
references such as `intake_method`, `exchange`, `market`, `symbols`,
`time_range`, `raw_snapshot_path`, `normalized_trades_path`, and
`import_manifest_path`. It must not store API keys, API secrets, signatures,
request headers, exchange account ids, balances, or raw rows.

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

For read-only API import, before step 5 the operator must verify:

- key is read-only where the exchange exposes metadata;
- trading/order, withdrawal, transfer, leverage/margin and account mutation
  permissions are disabled;
- IP allowlisting is preferred and documented if available;
- credentials are entered only through the approved local secret path;
- CSV upload remains the fallback if permission status is unclear or user does
  not want an API key.

The import command writes `raw_snapshot.json`, `normalized_trades.csv`, and
`import_manifest.json`; the existing `audit` command consumes
`normalized_trades.csv`.

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

## Boundary Reminders

Read-only API import is not live trading. It must not place, amend, cancel, or
manage orders; withdraw or transfer funds; change leverage or margin settings;
block orders; parse signals; produce trading advice; or collect credentials
through Telegram. It is only an optional local intake method for historical
executed fills.

## Operator CLI

Локальный operator workflow может быть запущен без database, hosted queue,
background workers или network services:

```bash
.venv/bin/python -m trader_risk_audit operator prepare \
  --queue-file pilot_queue.json \
  --workspace-root pilot_workspaces \
  --audit-id audit_demo_001 \
  --trades input/trades.csv \
  --policy input/policy.yaml \
  --profile hard

.venv/bin/python -m trader_risk_audit operator run \
  --queue-file pilot_queue.json \
  --workspace-root pilot_workspaces \
  --audit-id audit_demo_001
```

`operator prepare` показывает только audit id, status, selected policy profile,
safe input file references и next operator action. `operator run` запускает
локальный deterministic audit, записывает report, delivery packet и manifest
references в queue, затем переводит request в `ready_for_review`. Команды не
печатают raw trade rows.
