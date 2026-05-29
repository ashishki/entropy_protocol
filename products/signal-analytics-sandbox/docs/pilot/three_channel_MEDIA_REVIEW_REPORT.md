# Three-Channel Media Reviewer Report

Date: 2026-05-22T17:20:18Z
Status: `internal_model_review_not_customer_facing`

## Models

- Mass reviewer: `gpt-4.1-mini`
- Arbiter reviewer: `gpt-4.1`

## Boundary

- Mass reviewer checks every transcript/OCR draft row.
- Arbiter reviewer checks only high-signal or disputed rows.
- Image rows include the source image; voice rows use the transcript draft.
- Model review is internal only and does not approve customer-facing metrics.

## Totals

- `mass_review_rows`: 255
- `arbiter_review_rows`: 35
- `accepted_internal_candidates`: 1
- `arbiter_accepted_internal_candidates`: 9
- `needs_human_review`: 177
- `context_only`: 4
- `reject_noise`: 66
- `unable_to_review`: 7

## Channel Comparison

| channel | mass rows | mass accepted | arbiter accepted | needs human | context only | reject noise | avg usefulness | top evidence types | arbiter rows |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| `bablos79` | 162 | 0 | 1 | 107 | 2 | 48 | 1.284 | macro_context:58, directional_thesis:47, non_market:36, methodology:18, explicit_trade_setup:13 | 18 |
| `nemphiscrypts` | 63 | 0 | 1 | 46 | 2 | 13 | 1.159 | directional_thesis:14, non_market:11, explicit_trade_setup:9, macro_context:8, watchlist:5 | 7 |
| `pifagortrade` | 30 | 1 | 7 | 24 | 0 | 5 | 1.833 | post_factum:11, explicit_trade_setup:10, directional_thesis:7, position_management:7, risk_management:5 | 10 |

## High-Signal Examples

| channel | post | modality | score | evidence types | summary |
|---|---:|---|---:|---|---|
| `pifagortrade` | [3225](https://t.me/pifagortrade/3225) | image | 4 | post_factum, position_management, risk_management | Закрытие лонг позиции по BTCUSDT с прибылью и указанием комиссий. |

## Arbiter-Accepted Examples

| channel | post | modality | score | evidence types | summary |
|---|---:|---|---:|---|---|
| `pifagortrade` | [3225](https://t.me/pifagortrade/3225) | image | 4 | post_factum, position_management, risk_management | Закрытие лонг позиции по BTCUSDT с прибылью, указаны комиссии и параметры сделки. |
| `pifagortrade` | [3214](https://t.me/pifagortrade/3214) | image | 3 | explicit_trade_setup, risk_management, position_management | Короткая позиция по BTC: вход 74266.15, стоп 72000, размер 4.1, ROI 30.51%. Явных целей тейк-профита нет. |
| `pifagortrade` | [3274](https://t.me/pifagortrade/3274) | image | 3 | explicit_trade_setup, post_factum | Показан результат шорт-позиции по BTCUSDT с входом, выходом и плечом, но отсутствует стоп и временной интервал. |
| `bablos79` | [10450](https://t.me/bablos79/10450) | image | 3 | directional_thesis, explicit_trade_setup | Короткий сигнал по MAGN с уровнями входа, стопа и цели, но без размера позиции и дополнительного контекста. |
| `nemphiscrypts` | [3958](https://t.me/nemphiscrypts/3958) | image | 3 | directional_thesis, explicit_trade_setup | Пост содержит идею свинг-лонга по CHZ-PERP с явными уровнями входа и стопа, но без целей и размера позиции. |
| `pifagortrade` | [3264](https://t.me/pifagortrade/3264) | image | 3 | post_factum, explicit_trade_setup | Постфактумный отчет по шорт-позиции BTCUSDT с входом и ROI, отсутствуют стоп и цели. |
| `pifagortrade` | [3276](https://t.me/pifagortrade/3276) | image | 3 | post_factum, explicit_trade_setup | Постфактум отчет по шорт-позиции BTCUSDT с входом, выходом и ROI, но без стоп-лосса и временного интервала. |
| `pifagortrade` | [3234](https://t.me/pifagortrade/3234) | image | 3 | directional_thesis, explicit_trade_setup, risk_management | Прогноз по BTC/USD: покупка выше 74371, стоп 66200, цели 69000 и 78000. Нет размера позиции и явного отношения риск/прибыль. |
| `pifagortrade` | [3218](https://t.me/pifagortrade/3218) | image | 3 | directional_thesis, explicit_trade_setup | Бычий сетап по Bitcoin с уровнями входа, стопа и целями, но нет размера позиции и расчёта риска/прибыли. |

## Gate

- Decision: `internal_research_only`.
- Reason: these are model reviews, not human/operator accepted evidence.
