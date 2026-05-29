# Evidence Repair Review Queue - bablos79

Date: 2026-05-17T08:04:58Z
Status: operator_review_required_no_outcomes_computed

## Summary

- Candidate rows: 156
- Position disclosure candidates: 10
- Market-data fetches allowed now: 0
- External-eligible rows now: 0

## Category Counts

- `directional_bias_candidate`: 11
- `market_context_candidate`: 121
- `position_disclosure_candidate`: 10
- `trade_management_fragment`: 14

## Position Disclosure Candidates

These are the most promising rows because they disclose long/short sides and assets. They still need an operator-approved horizon/outcome method before market data can be fetched.

| capture_id | timestamp | long assets | short assets | source | blocker |
|---|---|---|---|---|---|
| `bablos79-10008` | `2026-02-19T18:04:22+00:00` | NKNC, PRMD, VTBR, WUSH | GD | [source](https://t.me/bablos79/10008) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10009` | `2026-02-19T18:19:49+00:00` | GD, NKNC, PRMD, VTBR, WUSH | - | [source](https://t.me/bablos79/10009) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10122` | `2026-03-06T15:01:32+00:00` | BR, CN, NKNC, PRMD, SI, VTBR, WUSH | - | [source](https://t.me/bablos79/10122) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10162` | `2026-03-13T07:30:36+00:00` | CNY, NG, NKNC, PRMD, SI, WUSH | SPY | [source](https://t.me/bablos79/10162) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10219` | `2026-03-20T14:08:33+00:00` | CN, NG, NKNC, PRMD, SI | PHOR, SPYF | [source](https://t.me/bablos79/10219) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10277` | `2026-03-27T15:46:33+00:00` | CNY, GOLD, NG, PRMD, SI | NVTK, SPYF, VTBR | [source](https://t.me/bablos79/10277) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10339` | `2026-04-11T06:11:51+00:00` | CNY, SI | SPYF, VTBR | [source](https://t.me/bablos79/10339) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10391` | `2026-04-17T16:06:13+00:00` | CNY | SBRF, SPYF | [source](https://t.me/bablos79/10391) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10526` | `2026-05-08T12:46:03+00:00` | NG | CHMF, GAZP, MAGN, X5 | [source](https://t.me/bablos79/10526) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |
| `bablos79-10576` | `2026-05-15T09:21:28+00:00` | NG | MIX | [source](https://t.me/bablos79/10576) | Position disclosure has timestamp, long/short sides, and assets, but outcome horizon/method must be operator-approved. |

## Other High-Priority Candidates

| capture_id | timestamp | category | assets | source | blocker |
|---|---|---|---|---|---|
| `bablos79-10013` | `2026-02-20T14:47:42+00:00` | `trade_management_fragment` | VTBR | [source](https://t.me/bablos79/10013) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10142` | `2026-03-09T14:17:17+00:00` | `trade_management_fragment` | VTBR | [source](https://t.me/bablos79/10142) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10257` | `2026-03-25T08:02:57+00:00` | `trade_management_fragment` | SMLT | [source](https://t.me/bablos79/10257) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10331` | `2026-04-10T07:20:43+00:00` | `trade_management_fragment` | GD | [source](https://t.me/bablos79/10331) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10332` | `2026-04-10T07:28:51+00:00` | `trade_management_fragment` | NVTK | [source](https://t.me/bablos79/10332) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10333` | `2026-04-10T07:44:50+00:00` | `trade_management_fragment` | NVTK | [source](https://t.me/bablos79/10333) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10335` | `2026-04-10T08:59:40+00:00` | `trade_management_fragment` | SBER | [source](https://t.me/bablos79/10335) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10352` | `2026-04-13T12:42:08+00:00` | `trade_management_fragment` | VTBR | [source](https://t.me/bablos79/10352) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10357` | `2026-04-14T05:48:52+00:00` | `trade_management_fragment` | CBOM | [source](https://t.me/bablos79/10357) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10380` | `2026-04-16T06:33:10+00:00` | `trade_management_fragment` | VTBR | [source](https://t.me/bablos79/10380) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10464` | `2026-04-28T16:04:15+00:00` | `trade_management_fragment` | X5 | [source](https://t.me/bablos79/10464) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10499` | `2026-05-05T08:31:27+00:00` | `trade_management_fragment` | SFIN | [source](https://t.me/bablos79/10499) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10500` | `2026-05-05T12:43:44+00:00` | `trade_management_fragment` | CHMF | [source](https://t.me/bablos79/10500) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10501` | `2026-05-05T12:55:18+00:00` | `trade_management_fragment` | MAGN | [source](https://t.me/bablos79/10501) | Management language references an asset, but original setup, horizon, or outcome method is missing. |
| `bablos79-10017` | `2026-02-22T04:47:04+00:00` | `directional_bias_candidate` | EUTR | [source](https://t.me/bablos79/10017) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10208` | `2026-03-20T08:56:19+00:00` | `directional_bias_candidate` | PHOR | [source](https://t.me/bablos79/10208) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10217` | `2026-03-20T10:43:57+00:00` | `directional_bias_candidate` | VTBR | [source](https://t.me/bablos79/10217) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10338` | `2026-04-10T12:16:29+00:00` | `directional_bias_candidate` | LENT | [source](https://t.me/bablos79/10338) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10386` | `2026-04-17T11:49:57+00:00` | `directional_bias_candidate` | SBER | [source](https://t.me/bablos79/10386) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10426` | `2026-04-24T12:54:03+00:00` | `directional_bias_candidate` | CHMF | [source](https://t.me/bablos79/10426) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10450` | `2026-04-27T11:16:37+00:00` | `directional_bias_candidate` | MAGN | [source](https://t.me/bablos79/10450) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10459` | `2026-04-28T06:44:46+00:00` | `directional_bias_candidate` | AMD | [source](https://t.me/bablos79/10459) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10510` | `2026-05-06T10:22:41+00:00` | `directional_bias_candidate` | MAGN | [source](https://t.me/bablos79/10510) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10579` | `2026-05-15T11:13:53+00:00` | `directional_bias_candidate` | SBER | [source](https://t.me/bablos79/10579) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-10580` | `2026-05-15T17:01:23+00:00` | `directional_bias_candidate` | MIX, NG | [source](https://t.me/bablos79/10580) | Directional/ticker language exists, but deterministic fields or proxy approval are incomplete. |
| `bablos79-9981` | `2026-02-16T10:43:17+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/9981) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-9990` | `2026-02-16T15:27:16+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/9990) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-9995` | `2026-02-18T06:40:28+00:00` | `market_context_candidate` | NVTK | [source](https://t.me/bablos79/9995) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-9999` | `2026-02-18T18:00:57+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/9999) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10007` | `2026-02-19T15:16:06+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10007) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10011` | `2026-02-20T06:28:52+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10011) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10016` | `2026-02-21T05:29:10+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10016) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10028` | `2026-02-27T14:08:49+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10028) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10031` | `2026-02-28T07:54:41+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10031) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10047` | `2026-03-02T06:35:59+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10047) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10049` | `2026-03-02T08:23:32+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10049) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10055` | `2026-03-02T18:11:11+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10055) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10059` | `2026-03-03T11:59:27+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10059) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10064` | `2026-03-03T18:34:25+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10064) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |
| `bablos79-10067` | `2026-03-04T07:08:59+00:00` | `market_context_candidate` | - | [source](https://t.me/bablos79/10067) | Market-adjacent context exists, but not enough deterministic outcome fields are present. |

## Operator Decisions Needed

1. Decide whether weekly position disclosure rows can use a fixed evaluation rule, for example next disclosure date or a fixed 5-trading-day horizon.
2. Approve explicit public market proxies for each asset class/instrument before any market data fetch.
3. Link trade-management fragments to original setup rows or reject them as non-evaluable management context.
4. Decide whether broad market/context rows are report context only or have an approved benchmark/horizon.
5. Keep transcript/image/OCR evidence external-blocked unless human/operator acceptance is recorded.

## Boundary

This queue is not a report and does not claim author capability. It is the review surface needed before proxy mapping, market data snapshots, outcomes, scorecard, report, or external delivery can be rerun.
