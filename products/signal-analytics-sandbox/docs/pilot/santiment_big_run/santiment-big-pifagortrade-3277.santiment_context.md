# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3277`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-18T20:35:27Z`
Window: `2026-05-11T20:35:27Z` to `2026-05-25T20:35:27Z`
Artifact SHA-256: `922c6be0e1f1d5bc5495f45ae28b6954367a64b354b9b5c022bf1c69edf517e0`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 76947.12708782258 | 76750.2801751085 | -196.84691271408 | -0.2558210035436558853016955074 | down_price_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 636929 | 637425 | 496 | 0.07787367194773671790733347045 | up_metric_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-05-11T20:35:27Z:2026-05-25T20:35:27Z`: 15 points, sha256 `b879f3f859ca5a8753f26141129f43feed20b22f8d5676058bad38b3061528f0`
- `santiment:bitcoin:social_volume_total:2026-05-11T20:35:27Z:2026-05-25T20:35:27Z`: 0 points, sha256 `522d3b1a82d17ba60b526301a911093670418a8f558e1d77db4c8c4de2bc0d19`
- `santiment:bitcoin:sentiment_weighted_total:2026-05-11T20:35:27Z:2026-05-25T20:35:27Z`: 0 points, sha256 `ffcae3a6c4fa2eaaa4afb560c6277f1cfaccea70b7ccd623531891366051b45d`
- `santiment:bitcoin:daily_active_addresses:2026-05-11T20:35:27Z:2026-05-25T20:35:27Z`: 15 points, sha256 `e09614972fdc63beed935bdb9e22673b9d62e6edd7e3fbbbf805efc48304275b`
- `santiment:bitcoin:exchange_inflow_usd:2026-05-11T20:35:27Z:2026-05-25T20:35:27Z`: 0 points, sha256 `5717e2c50a4799cdbb7a76dadcfea4c5723afac9837bd6a13bd08eb80daae593`
- `santiment:bitcoin:exchange_outflow_usd:2026-05-11T20:35:27Z:2026-05-25T20:35:27Z`: 0 points, sha256 `b499b7b03a273467f046590a552c9c78ee22efeba64aeb43d4981ee9badfafaa`

## Blockers

- `missing_santiment_points:social_volume_total`
- `missing_santiment_points:sentiment_weighted_total`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
