# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4091`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-17T17:41:19Z`
Window: `2026-05-10T17:41:19Z` to `2026-05-24T17:41:19Z`
Artifact SHA-256: `a65edb8d7be4f989b3f02a4ca4189c18e8363f35ee8163e7b7c47e25603dc9a2`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 77450.38534557966 | 76947.12708782258 | -503.25825775708 | -0.6497814768920353093319365823 | down_price_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 562754 | 636929 | 74175 | 13.18071484165372436268778187 | up_metric_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-05-10T17:41:19Z:2026-05-24T17:41:19Z`: 15 points, sha256 `af5220d8bd226d64d230f85247895dadaedc2a3eaf963cf113ba5365ee5fbb90`
- `santiment:bitcoin:social_volume_total:2026-05-10T17:41:19Z:2026-05-24T17:41:19Z`: 0 points, sha256 `7e213cac94e8e361a845d1cf5d10a79e6f765e11caa193ff11034af5849b2bfb`
- `santiment:bitcoin:sentiment_weighted_total:2026-05-10T17:41:19Z:2026-05-24T17:41:19Z`: 0 points, sha256 `a984ec41344461559e5dbc55d16c3b30ea6505adbda8ac1976f7b7a9bf397653`
- `santiment:bitcoin:daily_active_addresses:2026-05-10T17:41:19Z:2026-05-24T17:41:19Z`: 15 points, sha256 `70a1d51645a5cf77ec28f03a689703d385513369deb3851aa97af1290bbf59bf`
- `santiment:bitcoin:exchange_inflow_usd:2026-05-10T17:41:19Z:2026-05-24T17:41:19Z`: 0 points, sha256 `203fa9b03a6c2dbe1cacb1cc7b306beee808b2a7e1875499dbe0c8e6de4ee775`
- `santiment:bitcoin:exchange_outflow_usd:2026-05-10T17:41:19Z:2026-05-24T17:41:19Z`: 0 points, sha256 `ddcc9ad7df2575d31ee34abc775b9ca800864f265c929c59a9656aeb62b9eeec`

## Blockers

- `missing_santiment_points:social_volume_total`
- `missing_santiment_points:sentiment_weighted_total`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
