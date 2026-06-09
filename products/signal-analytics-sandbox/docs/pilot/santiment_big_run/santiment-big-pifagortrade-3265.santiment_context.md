# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3265`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-10T10:48:20Z`
Window: `2026-05-03T10:48:20Z` to `2026-05-17T10:48:20Z`
Artifact SHA-256: `fb5eeb82f244bf81da2f73e4d7389b4eae6295362e7582567ad508a817a2205b`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 82129.91042066542 | 81725.3525343078 | -404.55788635762 | -0.4925828900646477229323779666 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 1420 |  |  |  | insufficient_pre_or_post_points |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.089357317512 |  |  |  | insufficient_pre_or_post_points |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 524253 | 616618 | 92365 | 17.61840180218329699591609395 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 322447685.7786611 |  |  |  | insufficient_pre_or_post_points |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 376317801.19047683 |  |  |  | insufficient_pre_or_post_points |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-05-03T10:48:20Z:2026-05-17T10:48:20Z`: 15 points, sha256 `2879eeb463acec5770e1250fa7e7835401d0ab41e0ed7f57217046f4cb707c01`
- `santiment:bitcoin:social_volume_total:2026-05-03T10:48:20Z:2026-05-17T10:48:20Z`: 8 points, sha256 `a52574df8f24bba4253561565995eacc14ea8821f020506d8ea8f9e84218d4ae`
- `santiment:bitcoin:sentiment_weighted_total:2026-05-03T10:48:20Z:2026-05-17T10:48:20Z`: 8 points, sha256 `ddcd1ce29d63dc22bc71dc19d92c9f732c65bb8e17f892adf8e71c4d8d279142`
- `santiment:bitcoin:daily_active_addresses:2026-05-03T10:48:20Z:2026-05-17T10:48:20Z`: 15 points, sha256 `a4ba30df951be4085209aee7acd6c3d844d1ed7586b6a204314b33b838613c58`
- `santiment:bitcoin:exchange_inflow_usd:2026-05-03T10:48:20Z:2026-05-17T10:48:20Z`: 8 points, sha256 `ac001312222435fdb9e129d29cd2229ac4358e0e64d7afd521bbf1cae357e792`
- `santiment:bitcoin:exchange_outflow_usd:2026-05-03T10:48:20Z:2026-05-17T10:48:20Z`: 8 points, sha256 `b4e6969f812e9d98e313ef50ca27da01f1aa59780425aff5fb9c4eb2d154b294`
