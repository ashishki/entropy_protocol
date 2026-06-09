# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3280`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-19T12:28:16Z`
Window: `2026-05-12T12:28:16Z` to `2026-05-26T12:28:16Z`
Artifact SHA-256: `829e246eac0580f4d9ddf1ae25d78602d296704cc8b18ebcb55eda1eec048503`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 76750.2801751085 | 77467.97569247894 | 717.69551737044 | 0.9351047523644110415049499381 | up_price_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 637425 | 629974 | -7451 | -1.168921833941247989959603091 | down_metric_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-05-12T12:28:16Z:2026-05-26T12:28:16Z`: 15 points, sha256 `bef6cf9757d498445e1cca87cc409ee1f4f1453fad0f2eb9a172cba94b924b27`
- `santiment:bitcoin:social_volume_total:2026-05-12T12:28:16Z:2026-05-26T12:28:16Z`: 0 points, sha256 `b28147ffb074d64b6e26b95ef6c7bc590f7cf180e70fe481ca894e2d6c60e7b9`
- `santiment:bitcoin:sentiment_weighted_total:2026-05-12T12:28:16Z:2026-05-26T12:28:16Z`: 0 points, sha256 `6fe5a98ed8479e34823d13976f2b09d122ae39509143c773ea751b340a5c2c82`
- `santiment:bitcoin:daily_active_addresses:2026-05-12T12:28:16Z:2026-05-26T12:28:16Z`: 15 points, sha256 `e1aecccc0f5d1cbaeaa82a5fb692c5227b45dc374e87872fd2267d6cb878d23b`
- `santiment:bitcoin:exchange_inflow_usd:2026-05-12T12:28:16Z:2026-05-26T12:28:16Z`: 0 points, sha256 `3e839b0c806176f433037529c73e41c239659713b1c2909ecf16c82e5a13ce00`
- `santiment:bitcoin:exchange_outflow_usd:2026-05-12T12:28:16Z:2026-05-26T12:28:16Z`: 0 points, sha256 `e944f807623d7cea4f36adec4dce6b9afc6ac3f54a527e0264cbfd3eb6b110f4`

## Blockers

- `missing_santiment_points:social_volume_total`
- `missing_santiment_points:sentiment_weighted_total`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
