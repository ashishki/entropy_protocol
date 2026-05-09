# bablos79 Author Profile - Draft Lexicon

Date: 2026-05-08
Status: draft-only, unapproved profile discovery
Source: `bablos79` public Telegram captures
JSON artifact: `workspace/lexicons/bablos79_lexicon_draft.json`

## Boundary

This profile is an offline analysis artifact derived from local public captures and pseudo-labels. It does not add parser code, runtime LLM calls, CLI export behavior, approved ledger writes, or final extraction truth. Only `accepted_for_draft` terms may later inform deterministic draft suggestions, and even those terms cannot approve a signal without deterministic validation and human review.

## Profile State Policy

| profile_state | Parser/profile implication |
|---------------|----------------------------|
| `accepted_for_draft` | May be used only for future draft suggestions after deterministic parser implementation. Not sufficient for approval. |
| `needs_review` | Must stay out of automatic parser truth until a human or later validator resolves the risk. |
| `excluded` | Must not create positive parser signals; may only suppress/noise-classify if later explicitly implemented. |

## asset_alias

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `#AMD` | `accepted_for_draft` | `bablos79-10459` | По #AMD отбой. Пока не буду шортить его, может еще д | low for asset detection; the evidence row is explicitly a no-trade deferral. | 0.90 |
| `#CHMF` | `accepted_for_draft` | `bablos79-10500` | Зафиксировал часть #CHMF  Стоп перенес | low for asset detection; row is partial fixation without original setup. | 0.90 |
| `#GAZP` | `accepted_for_draft` | `bablos79-10489`, `bablos79-10490` | Во первых, это красиво! #GAZP | low for asset detection; examples are commentary, not author trade setup. | 0.90 |
| `#MAGN` | `accepted_for_draft` | `bablos79-10450`, `bablos79-10467`, `bablos79-10497`, `bablos79-10501` | #MAGN совет директоров порекомендовал не выплачива | low for asset detection, medium for signal detection because several mentions criticize other authors. | 0.93 |
| `#SBER` | `accepted_for_draft` | `bablos79-10492` |  и хочется взбодриться. ... юмором, то Ромка #SBER сегодня покупал 😁 | low for asset detection; example describes another person buying, so not signal truth. | 0.90 |
| `#SFIN` | `accepted_for_draft` | `bablos79-10499` | #SFIN закрыл почти в ноль. Продажи пошли. | low for asset detection; row is close/reduce management without original setup. | 0.90 |
| `#VKCO` | `accepted_for_draft` | `bablos79-10453` | про #VKCO | low for asset detection; ticker-only topic marker is not signal evidence. | 0.88 |
| `#VTBR` | `accepted_for_draft` | `bablos79-10443`, `bablos79-10446` | #VTBR похоже на грани срыва. У банка недостаток ли | low: explicit hashtag ticker; surrounding text may still be news/commentary. | 0.92 |
| `#X5` | `accepted_for_draft` | `bablos79-10442`, `bablos79-10458`, `bablos79-10464` | ☄️ По #X5 кто то жестко набирает, но мне очень кажется | low: explicit hashtag ticker; still only an asset candidate, not a signal. | 0.92 |

## close_or_reduce

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `закрыл` | `accepted_for_draft` | `bablos79-10464`, `bablos79-10499`, `bablos79-10501`, `bablos79-10504` | #X5  Конечно не так красиво, но пока закрыл. Фьючерсом перезайду может.  Был в отъезде б | medium: close/reduce marker, but requires linked original setup before any evaluable record. | 0.78 |
| `закрыл часть` | `accepted_for_draft` | `bablos79-10504` | Как вовремя я закрыл часть шортов.  Но это просто откат. Картина не мен | medium: partial close marker; missing asset in observed row. | 0.78 |
| `зафиксировал` | `accepted_for_draft` | `bablos79-10500` | Зафиксировал часть #CHMF  Стоп перенес | medium: profit-taking marker, not original entry evidence. | 0.82 |
| `часть закрыл` | `accepted_for_draft` | `bablos79-10501` | Это просто красиво #MAGN  Часть закрыл стоп подвинул | medium: partial close marker; cannot create approved record without original entry/stop/target. | 0.80 |

## direction_long

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `покупал` | `excluded` | `bablos79-10492` | одриться. ... юмором, то Ромка #SBER сегодня покупал 😁 | high: observed as third-party humorous reference, not author signal. | 0.28 |
| `покупать` | `needs_review` | `bablos79-10470` | По валюте пока негатив. Если буду покупать — будут знаки. | high: observed in conditional future phrase "Если буду покупать". | 0.35 |

## direction_short

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `шорт` | `accepted_for_draft` | `bablos79-10450`, `bablos79-10459`, `bablos79-10504` | нды.  Теханализ опять опережает новости.  Мы шортили с текущих хаев. | medium: can occur in historical close/no-trade context; may draft a short direction only with negation/close guards. | 0.74 |
| `шортили` | `accepted_for_draft` | `bablos79-10450` | нды.  Теханализ опять опережает новости.  Мы шортили с текущих хаев. | medium: past-tense author trade language; not enough for current evaluable signal. | 0.72 |
| `шортить` | `needs_review` | `bablos79-10459` | По #AMD отбой. Пока не буду шортить его, может еще дать. | high: example is explicitly negated by "Пока не буду". | 0.45 |
| `шортов` | `needs_review` | `bablos79-10504` | Как вовремя я закрыл часть шортов.  Но это просто откат. Картина не меняется. | high: appears in close/management language with no asset symbol in the post. | 0.48 |

## entry_intent

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `набирает` | `needs_review` | `bablos79-10442` | ☄️ По #X5 кто то жестко набирает, но мне очень кажется, что зря… | high: can describe someone else accumulating rather than author entry. | 0.42 |
| `перезайду` | `needs_review` | `bablos79-10464` | но не так красиво, но пока закрыл. Фьючерсом перезайду может.  Был в отъезде без интернета | high: future/conditional re-entry, not current entry. | 0.44 |

## noise_or_promo

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `стрим` | `excluded` | `bablos79-10449`, `bablos79-10456`, `bablos79-10487`, `bablos79-10493` | В 19 мск стрим. Разбор рынков. Политота. | low: recurring broadcast/promo marker; not extraction signal. | 0.90 |

## stop_or_invalidation

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `стоп` | `needs_review` | `bablos79-10500`, `bablos79-10501` | Зафиксировал часть #CHMF  Стоп перенес | medium-high: observed as moved stop without numeric stop value. | 0.66 |
| `стоп перенес` | `needs_review` | `bablos79-10500` | Зафиксировал часть #CHMF  Стоп перенес | medium-high: stop-management phrase lacks a numeric level. | 0.64 |
| `стоп подвинул` | `needs_review` | `bablos79-10501` | Это просто красиво #MAGN  Часть закрыл стоп подвинул | medium-high: stop-management phrase lacks a numeric level. | 0.64 |

## uncertainty

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `отбой` | `accepted_for_draft` | `bablos79-10459` | По #AMD отбой. Пока не буду шортить его, может еще дать. | low: useful cancellation/deferral marker; should suppress signal approval. | 0.82 |
| `пока не буду` | `accepted_for_draft` | `bablos79-10459` | По #AMD отбой. Пока не буду шортить его, может еще дать. | low: explicit no-action/deferral marker; should force needs_review/not_a_signal. | 0.86 |
| `будут знаки` | `needs_review` | `bablos79-10470` | По валюте пока негатив. Если буду покупать — будут знаки. | medium: future-sign marker indicates watchlist, not current trade. | 0.50 |

## watch_or_commentary

| term | profile_state | evidence_capture_ids | short evidence excerpt | false-positive risk | confidence |
|------|---------------|----------------------|------------------------|---------------------|------------|
| `дивиденды` | `excluded` | `bablos79-10450` | вет директоров порекомендовал не выплачивать дивиденды.  Теханализ опять опережает новости.  Мы шор | low: news/commentary marker by itself. | 0.84 |
| `негатив` | `excluded` | `bablos79-10447`, `bablos79-10470`, `bablos79-10486` | Рынок с утра в понедельник тоже не растет. Негативный признак. Слишком много негативных сигнало | medium: sentiment marker, not direction/entry. | 0.74 |
| `прибыль` | `excluded` | `bablos79-10490` | Когда инвесторы #GAZP вышли в прибыль | medium: performance/commentary word, not author entry. | 0.72 |
| `разбор` | `excluded` | `bablos79-10449` | В 19 мск стрим. Разбор рынков. Политота. | low: analysis/broadcast context, not trade setup. | 0.76 |

## Exclusion And Review Guardrails

- `needs_review` terms cannot become automatic parser truth; they require exception-review routing or a later deterministic guard.
- `excluded` terms cannot produce positive signal candidates. They are documented to prevent broadcast, news, sentiment, or third-party mentions from being treated as trades.
- Asset hashtag terms are accepted only as asset candidates. They do not imply direction, entry, stop, target, or approval.
- Close/reduce and stop-management terms are draft hints only because the observed captures usually lack original entry, numeric stop, or target.

## Runtime LLM Boundary

No LLM call was added to parser runtime, CLI export, ledger writing, tests, or any always-on product path. This task produced only `docs/pilot/bablos79_AUTHOR_PROFILE.md` and `workspace/lexicons/bablos79_lexicon_draft.json`.
