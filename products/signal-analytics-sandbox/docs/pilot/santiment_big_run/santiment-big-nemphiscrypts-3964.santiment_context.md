# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-3964`
Source: `nemphiscrypts`
Asset: `SUI` / `sui`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-07T07:24:20Z`
Window: `2026-03-31T07:24:20Z` to `2026-04-14T07:24:20Z`
Artifact SHA-256: `39d97050b86d479052c25a8008dd19eba5dea6037c4ce8394ff3d9ed464d88c0`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 0.959957959694 | 0.913844154037 | -0.046113805657 | -4.803731787556552921330331168 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 34 | 50 | 16 | 47.05882352941176470588235294 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.035013722472 | -0.004770171778 | -0.03978389425 | -113.623720762094466857634034 | down_social_context_after_post |

## Metric Refs

- `santiment:sui:price_usd:2026-03-31T07:24:20Z:2026-04-14T07:24:20Z`: 15 points, sha256 `36a1f1af245c22b6520c7798b50c21e2517070df58e9f41eadea9c2ad98669a9`
- `santiment:sui:social_volume_total:2026-03-31T07:24:20Z:2026-04-14T07:24:20Z`: 15 points, sha256 `aa8f59c869c1cb3b112180991d62b15848a2b923f21641f2199256b71fd7f078`
- `santiment:sui:sentiment_weighted_total:2026-03-31T07:24:20Z:2026-04-14T07:24:20Z`: 15 points, sha256 `4c7c25951e84da856435ff58decb4c86cf59f788f55a57e797185d0d73d2c5ee`
- `santiment:sui:daily_active_addresses:2026-03-31T07:24:20Z:2026-04-14T07:24:20Z`: 0 points, sha256 `33d99aec1688eda82dac517c7d59263665977c1686644f9995f56dcc5afe1085`
- `santiment:sui:exchange_inflow_usd:2026-03-31T07:24:20Z:2026-04-14T07:24:20Z`: 0 points, sha256 `c599c053351ec62ad6ea99005a1c7f39f8e920146f1a6ea9f977e2318e6b23db`
- `santiment:sui:exchange_outflow_usd:2026-03-31T07:24:20Z:2026-04-14T07:24:20Z`: 0 points, sha256 `ef8ff1691f12b0ddd5cb2292f42aa99135d17daadc3d6c0f2efc261f695366ff`

## Blockers

- `missing_santiment_points:daily_active_addresses`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
