# Pilot Scope - Telegram Public Audit Loop

Дата: 2026-05-07
Статус: v0 для `SAS-PILOT-001`
Язык: русский

## Цель Пилота

Пилот проверяет, можно ли по публичной истории Telegram-источника сделать
защищаемый исторический audit report, который помогает заказчику принять
конкретное решение: платить за источник, отменить подписку, запросить второй
аудит, передать отчет другому трейдеру или отказаться от такого формата.

Отчет не выбирает "лучший" канал, не прогнозирует будущую доходность и не дает
торговых рекомендаций. Он показывает только исторически проверяемые сигналы,
исключения, спорные места, price provenance и ограничения методологии.

## Pilot Sources

Все три источника взяты из `docs/PILOT_LOG.md` и подтверждены в
`docs/legal_risk_memo.md` как public Telegram pilot sources.

| Source ID | Public URL | Source class | Pilot status | Legal/risk verdict |
|-----------|------------|--------------|--------------|--------------------|
| `bablos79` | `https://t.me/bablos79` | `telegram_public` | public Telegram pilot source | approved |
| `nemphiscrypts` | `https://t.me/nemphiscrypts` | `telegram_public` | public Telegram pilot source | approved |
| `pifagortrade` | `https://t.me/pifagortrade` | `telegram_public` | public Telegram pilot source | approved |

Twitter / X, Discord, private groups, login-walled and paywalled sources are not
part of this pilot.

## First Source

Первым аудируем `https://t.me/bablos79`.

Причина выбора:

- это первый источник в `docs/PILOT_LOG.md`, поэтому выбор не основан на
  ожидаемой доходности или субъективном предпочтении;
- legal/risk memo уже дает для него verdict `approved`;
- deterministic ordering снижает риск cherry-picking перед первым отчетом;
- если публичная история окажется недоступной или слишком мутной, это будет
  честный pilot signal, а не повод незаметно перейти к другому источнику.

Если `bablos79` нельзя защитимо разобрать публичным способом, следующий источник
берется только после записи blocker reason в capture/extraction log.

## Audit Window / Target Count

Default target для каждого источника: 30-50 defensible signal records, где они
доступны публично. Рабочий target для первого отчета: 40 defensible records или
вся доступная публичная история за выбранный bounded window, если 40 записей не
набираются.

Правило окна:

- начинать с последних публичных постов источника;
- двигаться назад по истории до достижения 30-50 defensible records;
- если за разумный bounded window не найдено 30 records, фиксировать фактическое
  число, причины дефицита и customer-facing limitation;
- не добирать count за счет ambiguous, screenshot-only, private или
  insufficient-fields записей.

Для Phase 9 logs использовать одинаковую цель по всем трем источникам:

| Source ID | Default target | Minimum useful count | If target is unavailable |
|-----------|----------------|----------------------|--------------------------|
| `bablos79` | 40 defensible records, acceptable band 30-50 | 30 defensible records | write blocker/limitation and continue only with explicit note |
| `nemphiscrypts` | 40 defensible records, acceptable band 30-50 | 30 defensible records | write blocker/limitation and continue only with explicit note |
| `pifagortrade` | 40 defensible records, acceptable band 30-50 | 30 defensible records | write blocker/limitation and continue only with explicit note |

## What Qualifies As A Signal

Запись может стать defensible signal record только если из публичного текста и
evidence reference можно извлечь минимум:

- asset / symbol;
- direction (`long` or `short`);
- source timestamp or defensible post timestamp;
- entry rule or entry price/range;
- stop or explicit invalidation rule;
- target or take-profit rule;
- public evidence URL or capture path;
- raw text hash and capture timestamp after capture task starts.

Записи без полной структуры не подгоняются вручную. Они получают отдельный
статус в extraction log.

## Ambiguous Records

Ambiguous records сохраняются как pilot evidence, но не считаются win/loss
статистикой. Примеры:

- несколько entry zones без понятного правила входа;
- target/stop указаны в follow-up posts, но связь с исходным call спорная;
- сигнал отредактирован или контекст публично непроверяем;
- пост дает market commentary, но не конкретный trade setup;
- частичные тейки, усреднение или перенос stop нельзя воспроизвести
  deterministic rule без дополнительных допущений.

## Scope Out

В этот pilot не входят:

- private Telegram groups or channels;
- paywalled sources;
- login-walled sources;
- OCR/screenshots;
- X/Twitter;
- Discord;
- bot ingestion;
- public leaderboard;
- marketplace;
- copy trading;
- broker integration;
- investment advice;
- future performance prediction;
- Entropy Core research feed or evidence contamination;
- LLM output as final truth.

## Customer Decision Supported

Первый отчет должен помочь заказчику ответить на один из практических вопросов:

- стоит ли платить за этот public Telegram source;
- стоит ли продлевать или отменять подписку;
- достаточно ли прозрачны публичные сигналы источника;
- нужен ли аудит второго/третьего источника;
- какие методологические ограничения делают источник непригодным для честной
  исторической оценки.

## Success Criteria

Пилот считается успешным только при customer behavior signal, а не при
технически красивом отчете.

Минимальные success criteria:

- по первому источнику создан report artifact или честный blocker memo;
- заказчик может назвать, какое решение отчет помог принять;
- есть payment signal: paid, deposit, written intent-to-pay, repeat request или
  referral;
- customer accepts that ambiguous/excluded records do not count in win/loss;
- отчет не требует private scraping, bot ingestion, прогнозов или советов;
- operator minutes per approved signal записаны для решения об автоматизации.

## Kill Criteria

Пилот нужно остановить или переформатировать, если:

- заказчик требует private/paywalled/login-walled источник;
- заказчик хочет прогноз, рекомендацию покупки/продажи или "самый прибыльный
  канал", а не historical audit;
- публичная история не дает хотя бы 30 defensible records и limitation не
  считается полезным customer artifact;
- большинство записей screenshot-only или требуют OCR, который сейчас deferred;
- customer не принимает исключение ambiguous records из statistics;
- нет payment/deposit/repeat/referral signal после delivery;
- отчет вызывает только "интересно", но не меняет решение заказчика.

## Next Step

Следующий task: `SAS-PILOT-002: Methodology V0`.

Он должен зафиксировать capture fields, extraction statuses, deterministic
outcome semantics, exclusion rules, price provenance и guardrail wording до
начала capture/extraction по `bablos79`.
