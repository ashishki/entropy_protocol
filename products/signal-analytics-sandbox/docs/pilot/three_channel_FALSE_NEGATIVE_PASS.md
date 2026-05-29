# Three-Channel False-Negative Pass

Date: 2026-05-19
Status: internal_false_negative_pass_external_blocked

## Scope

This artifact implements `SAS-NEXT-002`. It reviews the five
`excluded_pending_false_negative` rows from
`docs/pilot/three_channel_FULL_REVIEW_QUEUE.json` and decides whether each row
should become a structured claim draft, remain context-only, need provider work,
or be rejected.

This pass does not approve external delivery. None of the five rows is added as
a customer-facing win/loss metric in this step.

## Summary

| Metric | Count |
|---|---:|
| False-negative rows reviewed | 5 |
| Extracted structured drafts | 3 |
| Needs context | 2 |
| Needs provider | 0 |
| Rejected | 0 |
| Scoreable now | 0 |

## Decisions

| pass_id | channel | source | status | claim type | assets | direction | score policy | reason |
|---|---|---|---|---|---|---|---|---|
| fn-001 | `nemphiscrypts` | https://t.me/nemphiscrypts/3344 | `extracted` | `directional_thesis` | `BTC` | `long` | `link_to_existing_v1_included_claim_not_new_duplicate` | Direct author-side wording says the BTC 90k-95k zone is a long opportunity, not a short; BTC alias comes from Russian битк wording. |
| fn-002 | `nemphiscrypts` | https://t.me/nemphiscrypts/3352 | `needs_context` | `market_context` | `BTC`, `ETH` | `mixed_or_quoted_sentiment` | `do_not_score_until_author_side_and_asset_scope_are_separated` | The row contains BTC/ETH market sentiment and bull-run wording, but it is framed as influencer narratives at different BTC levels rather than a clean author-side call. |
| fn-003 | `pifagortrade` | https://t.me/pifagortrade/2298 | `needs_context` | `trade_setup` | - | `long` | `do_not_score_without_asset_proxy_and_numeric_or_chart-linked_level` | The row says the author will buy more alts when safety/trap lines are touched, but it gives no specific asset/proxy, exact level, or linked prior post evidence. |
| fn-004 | `pifagortrade` | https://t.me/pifagortrade/2510 | `extracted` | `trade_setup` | `BTC` | `conditional_long_above_short_below` | `structured_but_not_fixed_horizon_scoreable_until_trap_line_level_is_machine_readable` | BTCUSD maps to BTC, and the text explicitly defines above Trap line as long and below Trap line as short. |
| fn-005 | `pifagortrade` | https://t.me/pifagortrade/2578 | `extracted` | `trade_management` | `BTC` | `long` | `management_context_only_until_original_setup_link_exists` | The title asks when the author will close a BTC long, which is position-management evidence; SIGN-UP is noise and must stay blocked as an asset. |

## Evidence Review

### fn-001 — nemphiscrypts 3344

- Source: https://t.me/nemphiscrypts/3344
- Review reason: Text contains direct BTC long-zone wording and should be included through alias detection.
- Evidence: зона битка 90к-95к - это возможность для лонга, а не шорта. слушайте, дети, дядю муарыча. деп будет целее. а то опять эксперты видел побежали шортить биток. в этот раз на фоне чего там? «пауэлл ставку снижать не будет», «война пакистана с ...
- Decision: `extracted` / `directional_thesis`
- Next action: Close false-negative row by linking it to the existing V1 included BTC claim for this source post.
- Blockers: none

### fn-002 — nemphiscrypts 3352

- Source: https://t.me/nemphiscrypts/3352
- Review reason: "BTC at 75k" panic/long context should be reviewed by BTC alias rules.
- Evidence: инфлы при битке 75к: -лучше в стейблах быть -будем еще падать -биток по 60к будет, эфир ниже 1к -до осени нет смысла ждать роста -трамп тарифами сейчас обрушит фонду инфлы при битке 95к: -это была ловушка -повторяется 2017/2021 годы -начин...
- Decision: `needs_context` / `market_context`
- Next action: Keep out of win/loss metrics until a reviewer separates quoted sentiment from the author thesis and chooses a single asset/direction.
- Blockers: `quoted_or_contrasted_sentiment`, `multiple_assets`, `no_single_author_side_direction`

### fn-003 — pifagortrade 2298

- Source: https://t.me/pifagortrade/2298
- Review reason: Repeated safety/trap-line condition should become level-aware setup evidence.
- Evidence: Почти пришли! Говорил тут, тут Как коснемся линии safety trade и trap line докуплю альты как говорил тут
- Decision: `needs_context` / `trade_setup`
- Next action: Resolve the referenced prior posts and map the alt basket/proxy before extracting a scoreable setup.
- Blockers: `missing_asset_proxy`, `missing_trap_line_level`, `missing_prior_context_link`

### fn-004 — pifagortrade 2510

- Source: https://t.me/pifagortrade/2510
- Review reason: Above/below trap-line condition should become a structured BTC setup.
- Evidence: Ритейл инвесторы и трейдеры откупают от зоны своей средней цены. Для упрощения восприятия : закрытие ниже Trap line это шорт Выше это лонг https://www.tradingview.com/x/Oj58bdWX/ Индикатор - https://ru.tradingview.com/script/erIwNY5q-trap-...
- Decision: `extracted` / `trade_setup`
- Next action: Store as conditional BTC setup; keep out of fixed-horizon win/loss until chart/OCR or numeric trap-line level is accepted.
- Blockers: `missing_numeric_trap_line_level`, `conditional_mixed_direction`

### fn-005 — pifagortrade 2578

- Source: https://t.me/pifagortrade/2578
- Review reason: BTC position/closure wording should be extracted; `SIGN-UP` must be blocked as an asset.
- Evidence: 🎞 КОГДА ЗАКРОЮ ЛОНГ ПО BTC? Жду Новые Возможности! Всем привет! Рынок достиг зоны "экстремального страха (25)" по индексу Fear and Greed. Пока участники испытывают медвежьи настроения, крупные игроки откупили более 100,000 BTC на прошлой н...
- Decision: `extracted` / `trade_management`
- Next action: Store as BTC long management context, block SIGN-UP, and link to the original entry setup before any performance scoring.
- Blockers: `requires_original_setup_link`, `blocked_asset_token:SIGN-UP`

## Calibration Updates

- `cal-003`: trap-line and safety-line language creates a conditional
  `trade_setup`, but stays unscored until a numeric/chart-linked level is
  accepted.
- `cal-004`: Russian BTC aliases such as `битк` and plain uppercase `BTC` must
  map to BTC while avoiding embedded noise tokens such as `BTCPARSER`.
- `cal-005`: `SIGN-UP` is a blocked asset token and cannot become a tradable
  asset.
- `cal-006`: quoted/contrasted sentiment must not become an author-side call
  until the reviewer separates quote from thesis.

## External Boundary

External delivery remains blocked until these decisions are applied to the queue
closure workflow and `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md` is
rerun.
