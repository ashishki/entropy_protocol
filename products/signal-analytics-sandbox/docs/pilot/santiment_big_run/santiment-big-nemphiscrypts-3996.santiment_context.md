# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-3996`
Source: `nemphiscrypts`
Asset: `SUI` / `sui`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-23T17:03:09Z`
Window: `2026-04-16T17:03:09Z` to `2026-04-30T17:03:09Z`
Artifact SHA-256: `4f5c5a9248c3cee1c2b62c01bc90434cd210be901484da15f3b338a64e53fc3f`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 0.946096659374 | 0.946190094741 | 0.000093435367 | 0.00987587960217754138458024036 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 23 | 21 | -2 | -8.695652173913043478260869565 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | -0 | 0 | 0 |  | flat_social_context_after_post |

## Metric Refs

- `santiment:sui:price_usd:2026-04-16T17:03:09Z:2026-04-30T17:03:09Z`: 15 points, sha256 `388528f9ecf3d9125c63ad4071770dbbd85e481d3878075956b4ae1a2011831d`
- `santiment:sui:social_volume_total:2026-04-16T17:03:09Z:2026-04-30T17:03:09Z`: 15 points, sha256 `dc84694997b838a946f175c921560de8b3b9f3e91cbef4aec9bdf6c589a5c90e`
- `santiment:sui:sentiment_weighted_total:2026-04-16T17:03:09Z:2026-04-30T17:03:09Z`: 15 points, sha256 `9280c744f8945cccb567cf5e99b5739403608867f56064ef55f5d527a2f2c777`
- `santiment:sui:daily_active_addresses:2026-04-16T17:03:09Z:2026-04-30T17:03:09Z`: 0 points, sha256 `a5d93faa4b947e213ec59478656d58d4cdd5530eda0e37c5c4a4c59afd2675a4`
- `santiment:sui:exchange_inflow_usd:2026-04-16T17:03:09Z:2026-04-30T17:03:09Z`: 0 points, sha256 `742a111eeee2fa21103c35e6a0e64445abb87a632a2572d18e75219c347a59d8`
- `santiment:sui:exchange_outflow_usd:2026-04-16T17:03:09Z:2026-04-30T17:03:09Z`: 0 points, sha256 `e6ea5ed63da09e84cb7f18ae476002df6cc979709142372d28e4090b701fe749`

## Blockers

- `missing_santiment_points:daily_active_addresses`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
