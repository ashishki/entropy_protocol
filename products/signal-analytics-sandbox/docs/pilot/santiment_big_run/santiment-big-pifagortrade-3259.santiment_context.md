# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3259`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-05T15:31:05Z`
Window: `2026-04-28T15:31:05Z` to `2026-05-12T15:31:05Z`
Artifact SHA-256: `c6e521452af0f088f629a6b83de697f8df0a2b266231c5860c900ba7370e8317`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 80930.73814844475 | 81427.30524697408 | 496.56709852933 | 0.6135704552929158653743763908 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 4113 | 3919 | -194 | -4.71675176270362265985898371 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | -0.001084067165 | -0.009827838576 | -0.008743771411 | 806.571003467299002640671254 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 738000 | 723375 | -14625 | -1.981707317073170731707317073 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 3218316164.304626 | 3014227267.1142106 | -204088897.1904154 | -6.341480661658746872565358863 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 3177978216.0775104 | 2831647607.175005 | -346330608.9025054 | -10.89782828436034974084539651 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-28T15:31:05Z:2026-05-12T15:31:05Z`: 15 points, sha256 `df76e61291a430063ad7df7871b376a5083c7951e6466bb34d1a7353e86840d9`
- `santiment:bitcoin:social_volume_total:2026-04-28T15:31:05Z:2026-05-12T15:31:05Z`: 13 points, sha256 `b443f8a343a80902c62ec0fbc58c1d5e9d56a625d8be4df7b702d683e8790061`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-28T15:31:05Z:2026-05-12T15:31:05Z`: 13 points, sha256 `4cc25a6db56a8c987d587eee7c69b141e8689553703eb571b267f714de8b0ec7`
- `santiment:bitcoin:daily_active_addresses:2026-04-28T15:31:05Z:2026-05-12T15:31:05Z`: 15 points, sha256 `338cfb050ce0df5004badd968dd5628d92efefca69ee14afa3be5402acff1d31`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-28T15:31:05Z:2026-05-12T15:31:05Z`: 13 points, sha256 `d7763d6edd6dc21ed094d97254ad5f9c2c78fd68875d9a1fa46d9bc13e2cf6ac`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-28T15:31:05Z:2026-05-12T15:31:05Z`: 13 points, sha256 `595a334f652f2e5838f1aa131cb7186ff7e328ff1804602190fe02fe705d31a0`
