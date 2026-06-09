# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3267`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-10T12:00:41Z`
Window: `2026-05-03T12:00:41Z` to `2026-05-17T12:00:41Z`
Artifact SHA-256: `43f4183ad7d006ca921c114c853890cd35d07f93c46fb0265456a8a9465a8fd0`

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

- `santiment:bitcoin:price_usd:2026-05-03T12:00:41Z:2026-05-17T12:00:41Z`: 15 points, sha256 `5d64a882eac90e26ad9008f6346a2536c4f34e54e440200b166273970a395c86`
- `santiment:bitcoin:social_volume_total:2026-05-03T12:00:41Z:2026-05-17T12:00:41Z`: 8 points, sha256 `27185c5cd2609118fe53528a1df59556366dcec2e0e3867aa1c7ab8eaf27060f`
- `santiment:bitcoin:sentiment_weighted_total:2026-05-03T12:00:41Z:2026-05-17T12:00:41Z`: 8 points, sha256 `4df03b130e7d4d946837b9c9529dea710d505693626eb1410baddf4f45b6a9ab`
- `santiment:bitcoin:daily_active_addresses:2026-05-03T12:00:41Z:2026-05-17T12:00:41Z`: 15 points, sha256 `53e1da03d83f623217e2cce862ac3317ad7f370abe1d4b4725a1ffaff7cf32b4`
- `santiment:bitcoin:exchange_inflow_usd:2026-05-03T12:00:41Z:2026-05-17T12:00:41Z`: 8 points, sha256 `820c8878dd396b1f67517c71989492f14f4fb91f63e97276e84f799a87a1abfc`
- `santiment:bitcoin:exchange_outflow_usd:2026-05-03T12:00:41Z:2026-05-17T12:00:41Z`: 8 points, sha256 `0b75ca056f1f3a1494831e018b1b4543ad8545753517c7e4e56b328e50585bf0`
