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
- `docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md`
- `docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json`
- `docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json`
- `docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json`
- `docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`
- `docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json`

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

После этого был выполнен отдельный двухмесячный multimodal-pass за
`2026-03-22..2026-05-22`, потому что text-only метрики не отвечали на вопрос
про картинки, voice/audio, стопы, цели, RR и размер позиции. Результат:

| Channel | Posts | Media refs | Draft transcript/OCR | Video/manual blockers | Internal RR-ready setups |
|---|---:|---:|---:|---:|---:|
| `bablos79` | 382 | 196 | 162 | 34 | 1 |
| `nemphiscrypts` | 133 | 63 | 63 | 0 | 0 |
| `pifagortrade` | 55 | 36 | 30 | 6 | 0 |

Итого по трем каналам: 570 public posts, 527 text rows, 295 media refs,
70 voice transcripts, 185 image/OCR/vision drafts, 40 video rows blocked for
manual review. RR-ready internal draft найден только один:
`bablos79` post `10450`, `MAGN` short, entry `28400`, stop `28600`,
target `26364`, computed RR `10.18`. Он не customer-facing, потому что
доказательство пришло через media/OCR draft и требует human/operator review.

Поверх этого добавлен model-reviewer pass:

- mass reviewer: `gpt-4.1-mini`, 255 transcript/OCR draft rows;
- arbiter reviewer: `gpt-4.1`, 35 high-signal rows;
- model review не является human/operator acceptance и остается internal-only.

Что нашли reviewers:

| Channel | Mass rows | Mass accepted | Arbiter accepted | Needs human | Main evidence types |
|---|---:|---:|---:|---:|---|
| `bablos79` | 162 | 0 | 1 | 107 | macro context, directional thesis, methodology, setup candidates |
| `nemphiscrypts` | 63 | 0 | 1 | 46 | directional thesis, setup candidates, watchlist |
| `pifagortrade` | 30 | 1 | 7 | 24 | post-factum trades, setup candidates, position/risk management |

Главные arbiter candidates: `pifagortrade` posts `3214`, `3225`, `3234`,
`3264`, `3274`, `3276`, `3218`; `bablos79` post `10450`; `nemphiscrypts`
post `3958`. Все они требуют человеческой проверки перед customer-facing
метриками.

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
- RR/setup rows почти нулевые: один internal RR-ready draft после multimodal
  pass, но он заблокирован для customer-facing метрик до review;
- provider/proxy coverage неполный для futures, FX, ETF/fund, commodities и
  broad indices;
- false-negative drafts найдены, но не добавлены в win/loss метрики без
  закрытия context/setup/provider blockers.

## Что считать главным контекстом

Аналитику достаточно читать эти файлы в таком порядке:

1. `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`
2. `docs/pilot/three_channel_V1_SCORECARD.md`
3. `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`
4. `docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md`
5. `docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`
6. `docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json`
7. `docs/specs/CHANNEL_UTILITY_EVALUATION.md`
8. `docs/specs/CHANNEL_QUANT_METRICS_V2.md`
9. `docs/pilot/three_channel_FALSE_NEGATIVE_PASS.md`
10. `docs/AI_DEVELOPMENT_PLAN_RU.md`

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
