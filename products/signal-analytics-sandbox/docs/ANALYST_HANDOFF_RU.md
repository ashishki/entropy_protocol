# Handoff для аналитика

Дата: 2026-05-22
Статус: внутренний research / продуктовая валидация, не внешний отчет

## Что мы строили

Мы строили sandbox-систему, которая оценивает полезность публичных рыночных
каналов не по впечатлению, а по проверяемым утверждениям:

1. Берем публичные посты канала.
2. Извлекаем из текста, аудио, картинок и OCR рыночные утверждения.
3. Нормализуем их в единый claim/idea ledger.
4. Отделяем измеримые сделки/направления от шума, контекста и медиа без
   подтверждения.
5. Проверяем измеримые утверждения на исторических рыночных данных через
   публичные провайдеры/proxy, без хранения огромной базы market history.
6. Считаем метрики по каналу: hit rate, средний directional return, coverage,
   исключения, provider coverage, качество extraction и готовность к внешнему
   отчету.

Главная идея: система должна сравнивать разные каналы и авторов с разными
стилями, поэтому она не должна быть заточена только под одного автора.

## Что получилось

Сделан end-to-end internal V1 pipeline для сравнения трех публичных Telegram
каналов:

- `bablos79`
- `nemphiscrypts`
- `pifagortrade`

Ключевой результат лежит здесь:

- `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`
- `docs/pilot/three_channel_V1_METRIC_RESULTS.json`
- `docs/pilot/three_channel_V1_SCORECARD.md`
- `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`

На текущей V1-выборке получились такие customer-readable-candidate, но
internal-only метрики:

| Channel | V1 evaluable / V0 evaluable | 7d hit rate | Avg 7d directional return | Reviewed exclusions | Provider coverage |
|---|---:|---:|---:|---:|---|
| `bablos79` | 14 / 19 | 64.285714% | 0.742848% | 5 | Binance crypto, MOEX ISS shares |
| `nemphiscrypts` | 49 / 53 | 57.142857% | 0.434858% | 4 | Binance crypto |
| `pifagortrade` | 107 / 112 | 52.336449% | -0.153127% | 6 | Binance crypto |

Эти цифры нельзя трактовать как "лучший канал" или прогноз будущей прибыли.
Это только историческая проверка измеримых утверждений в рамках текущей
выборки и текущих правил исключения.

## Важный вывод

Система уже показывает, что можно:

- автоматически привести разнородные посты к единой структуре;
- отделить измеримые рыночные claims от комментариев и шума;
- посчитать сравнимые channel utility metrics;
- показать подтвержденные и опровергнутые примеры с source links;
- защититься от ложных побед через review exclusions и external gate.

Но отчет пока не готов для платной внешней доставки. Gate сейчас:

`approve_internal_only`

Причины:

- не вся review queue закрыта оператором;
- media/audio/OCR/chart claims пока не разрешены для customer-facing метрик;
- RR/setup rows сейчас фактически нулевые;
- provider/proxy coverage неполный для futures, FX, ETF/fund, commodities и
  broad indices;
- false-negative drafts найдены, но не добавлены в win/loss метрики без
  закрытия context/setup/provider blockers.

## Что считать главным контекстом

Аналитику достаточно читать эти файлы в таком порядке:

1. `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`
2. `docs/pilot/three_channel_V1_SCORECARD.md`
3. `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`
4. `docs/specs/CHANNEL_UTILITY_EVALUATION.md`
5. `docs/specs/CHANNEL_QUANT_METRICS_V2.md`
6. `docs/pilot/three_channel_FALSE_NEGATIVE_PASS.md`
7. `docs/AI_DEVELOPMENT_PLAN_RU.md`

Для детального аудита extraction/review дополнительно смотреть
`docs/pilot/three_channel_FULL_REVIEW_QUEUE.md` и JSON рядом с ним. Это не
обязательный файл для первичного аналитического handoff.

Если нужно понять историю конкретно `bablos79`, дополнительно:

1. `docs/pilot/bablos79_CLAIM_LEDGER.md`
2. `docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.md`
3. `docs/pilot/bablos79_AUTHOR_CAPABILITY_SCORECARD.md`
4. `docs/pilot/reports/bablos79_AUTHOR_CAPABILITY_REPORT_V1.md`

## Что не обязательно коммитить для передачи контекста

Для следующего аналитического агента не обязательно тащить весь массив
generated artifacts. Особенно осторожно с:

- `workspace/captures/bablos79/*.json` - 522 raw capture JSON;
- `__pycache__/` и `*.pyc` - точно не нужны;
- промежуточные draft/review artifacts, если агенту нужен только итоговый
  контекст, а не воспроизводимость полного pipeline;
- большие expanded capture packs, если не требуется аудит source-by-source.

Минимальный полезный commit scope для аналитика:

- этот файл: `docs/ANALYST_HANDOFF_RU.md`;
- итоговые three-channel отчеты и metric JSON;
- specs по метрикам и channel utility;
- внешний gate и language safety;
- опционально ключевые `bablos79` retrospective/claim-ledger файлы.

Полный reproducibility scope шире: тогда нужны review queues, capture packs,
test files и кодовые модули пайплайна.

## Что делать дальше

Практичный следующий шаг для аналитика:

1. Проверить, достаточно ли эти метрики отвечают на buyer question:
   "какой канал реально давал полезные рыночные сигналы исторически?"
2. Решить, какие claims должны стать customer-facing eligible.
3. Закрыть operator review queue по спорным rows.
4. Расширить provider/proxy coverage для неподдержанных классов активов.
5. Добавить RR/setup scoring только там, где в посте есть вход, стоп, цель или
   понятная зона.
6. После этого rerun external-ready gate.

Пока этот gate не стал external-approved, любые выводы формулировать как
"internal historical evidence-quality analysis", а не как инвестиционный
рейтинг или рекомендацию.
