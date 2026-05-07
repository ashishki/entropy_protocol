# Signal Analytics Sandbox - Pilot Development Loop

Дата: 2026-05-07
Статус: рабочий план следующего цикла
Язык: русский

## 1. Коротко

У нас уже есть 3 публичные Telegram-группы, которые дали потенциальные заказчики:

- `https://t.me/bablos79`
- `https://t.me/nemphiscrypts`
- `https://t.me/pifagortrade`

Значит следующий шаг - не искать абстрактную идею, а провести реальный пилот на этих трех источниках.

Цель пилота: понять, можно ли из публичных постов получить честный исторический отчет по сигналам, который заказчик считает полезным и готов оплачивать.

## 2. Что именно делаем

Мы берем каждую группу и проходим один и тот же путь:

1. Проверяем, что источник публичный и подходит под legal/ToS границы.
2. Берем ограниченный исторический период или последние N сигналов.
3. Сохраняем публичные посты как evidence: ссылка, время capture, текст, hash.
4. Вручную извлекаем торговые сигналы: asset, direction, entry, stop, target, timestamp.
5. Отмечаем мутные сигналы отдельно, а не притворяемся, что все понятно.
6. Берем исторические цены с provenance.
7. Детерминированно считаем outcomes: target hit, stop hit, timeout, excluded.
8. Делаем отчет по каждой группе.
9. Показываем отчет заказчикам.
10. Фиксируем, что им полезно, что спорно, за что они готовы платить.

## 3. Почему так

Потому что главный риск сейчас не технический. Техническое ядро уже во многом есть: ledger, snapshots, outcome matching, Markdown report, manual/rule/LLM draft extraction.

Главный риск другой: будут ли люди платить за такой аудит и доверять отчету.

Если мы сейчас начнем строить Telegram-бота, leaderboard или автоматический parser, можно потратить время на красивую оболочку до того, как доказано, что сам отчет нужен.

Поэтому порядок такой:

1. Сначала ручной пилот на реальных группах.
2. Потом отчет и customer feedback.
3. Потом автоматизация только тех мест, где реально больно.

## 4. Главный принцип

Не строим новый продукт, пока не доказали ценность отчета.

Разрешено:

- работать только с публичными Telegram-группами;
- делать manual capture;
- делать manual extraction;
- использовать существующее deterministic ядро;
- выпускать private Markdown/PDF report;
- отправлять отчет заказчику в Telegram вручную;
- собирать feedback и objections.

Запрещено сейчас:

- private Telegram scraping;
- login/paywall scraping;
- Telegram bot как основной продукт;
- public SaaS;
- influencer leaderboard;
- signal marketplace;
- copy trading;
- broker/exchange execution;
- investment advice;
- future performance prediction;
- LLM как финальная правда по сигналу;
- использовать эти отчеты как Entropy Core evidence.

## 5. Pilot Success Metric

Пилот считается успешным, если выполнены все условия:

1. По каждой из 3 групп можно извлечь хотя бы 30 защищаемых signal records или честно доказать, почему источник плохой/мутный.
2. Для каждого отчета есть per-signal evidence: ссылка, timestamp, text hash.
3. Outcomes воспроизводимы на том же ledger и price snapshot.
4. Заказчики читают отчет и говорят, какое решение он помогает принять.
5. Есть хотя бы один сильный payment signal: оплата, deposit, письменное intent-to-pay, repeat request или referral.

Если payment signal отсутствует, это не продуктовый успех, даже если технически отчет получился.

## 6. Рабочие фазы

### Phase P0 - Pilot Setup

Цель: зафиксировать рамки пилота.

Scope in:

- 3 Telegram-группы из `docs/PILOT_LOG.md`;
- публичный доступ;
- ограниченный historical window;
- private reports для заказчиков.

Scope out:

- X/Twitter;
- Discord;
- private groups;
- OCR/screenshots;
- bot;
- SaaS.

Артефакты:

- `docs/pilot/SOURCE_INTAKE.md`
- `docs/pilot/PILOT_SCOPE.md`
- `docs/pilot/METHODOLOGY_V0.md`

Exit criteria:

- для каждой группы выбран период или target count сигналов;
- legal/ToS memo не блокирует источники;
- заказчик понимает, что отчет historical, not advice.

Kill criteria:

- заказчик требует private/paywalled source;
- заказчик хочет прогноз или торговую рекомендацию, а не аудит.

### Phase P1 - Source Capture

Цель: собрать проверяемые публичные посты.

Что делаем:

- сохраняем raw text публичных постов;
- фиксируем evidence URL;
- фиксируем capture timestamp;
- считаем SHA-256 текста;
- не используем автоматический scraping за логином.

Артефакты:

- `docs/pilot/CAPTURE_LOG.md`
- локальные capture files в operator workspace;
- список skipped/blocked posts с причиной.

Exit criteria:

- по каждой группе есть достаточный набор captured posts;
- каждый capture можно проверить по URL/timestamp/hash.

Kill criteria:

- посты недоступны публично;
- источник в основном состоит из картинок/скриншотов и без OCR нельзя извлечь смысл;
- история сильно удалена/изменена и отчет невозможен без недопустимого доступа.

### Phase P2 - Manual Signal Extraction

Цель: понять, сколько реальных сигналов можно честно извлечь.

Что делаем:

- вручную извлекаем сигналы;
- каждый сигнал получает статус:
  - `approved`;
  - `ambiguous`;
  - `not_a_signal`;
  - `insufficient_fields`;
  - `duplicate`;
  - `needs_rule_template`;
- LLM можно использовать только как draft helper, если это не нарушает legal memo и человек потом утверждает запись.

Артефакты:

- `docs/pilot/EXTRACTION_LOG.md`
- approved ledger по каждой группе;
- ambiguity notes;
- список повторяющихся форматов для future rule extraction.

Exit criteria:

- по каждой группе есть approved/ambiguous counts;
- понятно, сколько времени занимает extraction;
- понятно, какие форматы можно автоматизировать regex/rule template.

Kill criteria:

- меньше 30% постов с сигналами можно защитимо структурировать;
- большинство сигналов без entry/stop/target;
- customer не принимает исключение ambiguous сигналов из win/loss stats.

### Phase P3 - Price Snapshot And Outcome Matching

Цель: посчитать исторический результат без ручного подгона.

Что делаем:

- выбираем price source;
- создаем immutable price snapshot;
- считаем outcomes по существующим deterministic rules;
- отдельно показываем excluded signals.

Артефакты:

- `docs/pilot/PRICE_SOURCE_LOG.md`
- price snapshots;
- outcomes files;
- methodology notes по rule assumptions.

Exit criteria:

- каждый outcome связан с rule id и snapshot hash;
- повторный запуск дает тот же результат;
- known limitations записаны явно.

Kill criteria:

- price data нет или она слишком дорогая;
- intra-candle ambiguity делает большинство outcomes спорными;
- customer требует симуляцию, slippage, leverage или execution model до базового audit.

### Phase P4 - Report V0

Цель: сделать первый понятный отчет для заказчика.

Что должно быть в отчете:

- кто источник;
- какой период проверяли;
- сколько постов обработано;
- сколько сигналов найдено;
- сколько excluded и почему;
- win/loss/timeout только по evaluable signals;
- historical equity-style chart/table, если defensible;
- per-signal evidence;
- price snapshot provenance;
- limitations;
- non-advice disclaimer.

Артефакты:

- `docs/pilot/reports/<source_id>_REPORT_V0.md`
- `docs/pilot/REPORT_REVIEW_LOG.md`

Exit criteria:

- отчет можно показать заказчику без устного объяснения на 30 минут;
- negative/ambiguous results сформулированы аккуратно, без defamation language;
- customer понимает, что отчет не прогнозирует будущую доходность.

Kill criteria:

- отчет слишком технический и заказчик его не читает;
- отчет не помогает принять решение;
- customer просит только “скажи, какой канал даст прибыль”.

### Phase P5 - Customer Review

Цель: проверить реальную ценность.

Что спрашиваем после отчета:

- какое решение вы теперь примете;
- что было неожиданно;
- чему не доверяете;
- какой раздел был самым полезным;
- какой раздел лишний;
- какой формат удобнее: Telegram summary, PDF, Markdown, spreadsheet;
- заплатили бы за второй источник сейчас;
- кому еще это надо показать.

Артефакты:

- `docs/pilot/CUSTOMER_FEEDBACK.md`
- `docs/pilot/OBJECTION_LOG.md`
- `docs/pilot/PAYMENT_SIGNAL_LOG.md`

Exit criteria:

- есть clear decision impact;
- есть payment signal или documented refusal reason;
- понятно, что автоматизировать первым.

Kill criteria:

- заказчики говорят “интересно”, но не меняют решение;
- никто не готов платить/повторить;
- все хотят private scraping, copy trading или гарантии прибыли.

### Phase P6 - Automation Gate

Цель: решить, что строить дальше.

Автоматизируем только то, что доказано пилотом.

Возможные next engineering tasks:

- соединить CLI stubs в реальный operator workflow;
- сделать удобный source intake command;
- сделать batch capture loader для approved manual captures;
- улучшить manual extraction review;
- добавить rule templates для повторяющихся форматов;
- улучшить report packaging;
- добавить Telegram delivery wrapper.

Не автоматизируем:

- bot ingestion;
- private channels;
- public leaderboard;
- paid X;
- OCR;
- marketplace;
- execution.

Entry criteria:

- минимум 3 отчета доставлены или 1 отчет доставлен и 2 в работе с payment signal;
- extraction/reporting bottleneck измерен;
- customer feedback показывает, какой шаг реально мешает продаже.

Exit criteria:

- написан новый task graph только на validated automation;
- каждая engineering task связана с bottleneck из пилота.

Kill criteria:

- нет payment signal;
- bottleneck не в tooling, а в trust/sales/legal;
- users хотят другой продукт.

### Phase P7 - Product Decision

Цель: принять решение по продукту.

Варианты:

1. Продолжаем как manual audit service.
2. Делаем local-first operator CLI для ускорения отчетов.
3. Добавляем Telegram delivery, но не bot ingestion.
4. Переходим к monitoring subscription.
5. Pivot to seller verification.
6. Kill/defer product.

Артефакты:

- `docs/pilot/PILOT_CLOSEOUT.md`
- обновленный `docs/tasks.md` только если принято решение строить следующий validated phase;
- ADR, если меняются runtime, legal boundary, source types или delivery model.

Decision criteria:

- advance, если есть payment/repeat/referral;
- keep concierge, если платят, но workflow еще не понятен;
- pivot, если платят не subscribers, а sellers;
- kill/defer, если есть только интерес без оплаты.

## 7. Development Loop

Каждый цикл работы должен идти так:

1. Выбрать один источник.
2. Зафиксировать scope.
3. Собрать captures.
4. Извлечь сигналы.
5. Посчитать outcomes.
6. Собрать report.
7. Отдать заказчику.
8. Записать feedback.
9. Решить: повторить вручную, автоматизировать узкое место или остановить.

Нельзя перескакивать к автоматизации до customer review.

## 8. Первые 7 рабочих задач

### SAS-PILOT-001 - Pilot Scope

Результат: `docs/pilot/PILOT_SCOPE.md`.

Содержит:

- 3 источника;
- период проверки;
- target count сигналов;
- что считается сигналом;
- что считается ambiguous;
- что не входит в отчет.

### SAS-PILOT-002 - Methodology V0

Результат: `docs/pilot/METHODOLOGY_V0.md`.

Содержит:

- extraction rules;
- outcome rules;
- exclusion rules;
- price source policy;
- no-advice wording.

### SAS-PILOT-003 - Capture First Source

Результат: captures + `docs/pilot/CAPTURE_LOG.md`.

Берем первый источник и собираем достаточную историю.

### SAS-PILOT-004 - Extract First Source

Результат: first approved ledger + `docs/pilot/EXTRACTION_LOG.md`.

Главное измерение: minutes per approved signal.

### SAS-PILOT-005 - Match And Report First Source

Результат: first report V0.

Проверяем, что отчет можно объяснить и защитить.

### SAS-PILOT-006 - Customer Review First Report

Результат: feedback + objection log.

Главное измерение: changed decision / payment signal / repeat request.

### SAS-PILOT-007 - Repeat Or Automate Decision

Результат: решение:

- повторить вручную на 2 оставшихся группах;
- автоматизировать конкретный bottleneck;
- остановить/переформатировать отчет.

## 9. Что считать хорошим результатом первого источника

Хороший результат - не обязательно “канал прибыльный”.

Хороший результат:

- мы смогли честно разобрать источник;
- нашли понятные и мутные сигналы;
- показали, где статистика защищаемая, а где нет;
- заказчик понял ценность;
- заказчик готов продолжить на второй/третий источник или заплатить.

Если отчет показывает, что канал плохой или мутный, это тоже хороший продуктовый результат, если заказчик доверяет выводу.

## 10. Что делаем прямо сейчас

Следующий правильный шаг:

1. Создать `docs/pilot/PILOT_SCOPE.md`.
2. Создать `docs/pilot/METHODOLOGY_V0.md`.
3. Выбрать первый источник из трех.
4. Собрать по нему captures.
5. Сделать первый manual audit report.
6. Отдать заказчику.
7. Только после feedback решать, что автоматизировать.

## 11. Главное решение

Текущий продуктовый курс:

**Signal Analytics Sandbox становится pilot audit loop для трех публичных Telegram-источников, полученных от потенциальных заказчиков.**

Пока не доказана ценность отчетов, Telegram bot, public SaaS, leaderboard и marketplace остаются запрещенными расширениями.
