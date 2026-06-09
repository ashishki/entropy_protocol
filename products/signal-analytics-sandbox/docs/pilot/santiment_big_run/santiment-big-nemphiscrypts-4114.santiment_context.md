# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4114`
Source: `nemphiscrypts`
Asset: `SOL` / `solana`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-21T10:24:25Z`
Window: `2026-05-14T10:24:25Z` to `2026-05-28T10:24:25Z`
Artifact SHA-256: `bd816e4e8d65a1ef2c77e8d3dc69d36c805f582de8c5f63728533ac8d8c584ce`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 87.15680740275 | 84.297500531924 | -2.859306870826 | -3.280646636829175798248890041 | down_price_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 2864753 | 2872075 | 7322 | 0.2555892253189018390067136678 | up_metric_context_after_post |

## Metric Refs

- `santiment:solana:price_usd:2026-05-14T10:24:25Z:2026-05-28T10:24:25Z`: 15 points, sha256 `4074b25de7844c4e13f6a4a7aa097d69c6c6df0b1ce1427881dfd4e87f184032`
- `santiment:solana:social_volume_total:2026-05-14T10:24:25Z:2026-05-28T10:24:25Z`: 0 points, sha256 `c6571a34b0b6b7be20d614770f900f1621fb6c253ee0c9c1d1cd3311285841cc`
- `santiment:solana:sentiment_weighted_total:2026-05-14T10:24:25Z:2026-05-28T10:24:25Z`: 0 points, sha256 `c807cffa02166e21c80281903818a472869bf33c32ada251bbcc1c1dbfd2d618`
- `santiment:solana:daily_active_addresses:2026-05-14T10:24:25Z:2026-05-28T10:24:25Z`: 15 points, sha256 `77a3b93431e8453dab865b12c9fea1c7469528a9d05be4bc7e2aea7b020a4726`
- `santiment:solana:exchange_inflow_usd:2026-05-14T10:24:25Z:2026-05-28T10:24:25Z`: 0 points, sha256 `9a41395938c59efb8565f216bada8007159e5073190c71494e42e7f954c127bf`
- `santiment:solana:exchange_outflow_usd:2026-05-14T10:24:25Z:2026-05-28T10:24:25Z`: 0 points, sha256 `0065ada4fa3c26b5881fe98c6dce32eebf4f1f13b44feb5f48d981c34d18a99e`

## Blockers

- `missing_santiment_points:social_volume_total`
- `missing_santiment_points:sentiment_weighted_total`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
