# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4094`
Source: `nemphiscrypts`
Asset: `ETH` / `ethereum`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-20T08:01:57Z`
Window: `2026-05-13T08:01:57Z` to `2026-05-27T08:01:57Z`
Artifact SHA-256: `44f3a746268e8a90c6e8060746994b40f5f5791833a0ab8d0331720ef8cd4492`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 2127.362664798115 | 2131.370076481668 | 4.007411683553 | 0.1883746363450117300326471101 | up_price_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 588675 | 571201 | -17474 | -2.968361150040344842230432752 | down_metric_context_after_post |

## Metric Refs

- `santiment:ethereum:price_usd:2026-05-13T08:01:57Z:2026-05-27T08:01:57Z`: 15 points, sha256 `13a3dd91ae90fc03be5c55a66b70bc8654bc0c5a49c18c4e9c01d22bb0810c75`
- `santiment:ethereum:social_volume_total:2026-05-13T08:01:57Z:2026-05-27T08:01:57Z`: 0 points, sha256 `274d55c4de4397cddf3a4af6b2f26f743f06820fe7e796c2328e1b9189963680`
- `santiment:ethereum:sentiment_weighted_total:2026-05-13T08:01:57Z:2026-05-27T08:01:57Z`: 0 points, sha256 `aaa35e0713f1339f29a0cfc381ccbe497c402819c33e6cac2e866da3080a87e8`
- `santiment:ethereum:daily_active_addresses:2026-05-13T08:01:57Z:2026-05-27T08:01:57Z`: 15 points, sha256 `2019cc5157b9428d16480d228097b7db9c0338dbe9883e04a14685467a463551`
- `santiment:ethereum:exchange_inflow_usd:2026-05-13T08:01:57Z:2026-05-27T08:01:57Z`: 0 points, sha256 `b44ca96ccfd6c955238274c773a74f642508412f659ba3b41e6b87427662a492`
- `santiment:ethereum:exchange_outflow_usd:2026-05-13T08:01:57Z:2026-05-27T08:01:57Z`: 0 points, sha256 `20fb23a754a62a950bc6e4dfaf0a50003b62e5d470ee75ba3c566a9b0177b599`

## Blockers

- `missing_santiment_points:social_volume_total`
- `missing_santiment_points:sentiment_weighted_total`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
