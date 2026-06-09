# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3224`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-07T13:10:10Z`
Window: `2026-03-31T13:10:10Z` to `2026-04-14T13:10:10Z`
Artifact SHA-256: `f4c4eba62d1a5985092974229817f26e57746f79dfd7004ebc3b10dbfd6064ba`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 71913.6133848375 | 71115.12256459738 | -798.49082024012 | -1.110347238383207705733020319 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2134 | 2676 | 542 | 25.39831302717900656044985942 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.012792622241 | 0.036792538272 | 0.023999916031 | 187.607478583092477951331073 | up_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 638320 | 643069 | 4749 | 0.7439842085474370221832309813 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 1902889833.6419864 | 2140193036.746782 | 237303203.1047956 | 12.47067480783242819215218731 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 1811891994.3556254 | 2131820426.1113918 | 319928431.7557664 | 17.65714693549074209232767913 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-03-31T13:10:10Z:2026-04-14T13:10:10Z`: 15 points, sha256 `d17d7c40c2a7c87b82e27f06ee6236f6549323e4624a728ca1cd03724f593ae4`
- `santiment:bitcoin:social_volume_total:2026-03-31T13:10:10Z:2026-04-14T13:10:10Z`: 15 points, sha256 `1668818d31df0d404ebc5b7b092f740b164e4576c2d4991c9232490c516caa8c`
- `santiment:bitcoin:sentiment_weighted_total:2026-03-31T13:10:10Z:2026-04-14T13:10:10Z`: 15 points, sha256 `dfc3b7151902bfbc996b71b67552fc39990ef00c0a646b428f16ef21bc6c5f60`
- `santiment:bitcoin:daily_active_addresses:2026-03-31T13:10:10Z:2026-04-14T13:10:10Z`: 15 points, sha256 `14fa7cb842e6bcba59f65dd1e734c768acd542bb76a6f9dcfeca54c9f5cc5d0d`
- `santiment:bitcoin:exchange_inflow_usd:2026-03-31T13:10:10Z:2026-04-14T13:10:10Z`: 15 points, sha256 `e6e5ff4df20931ba533e5d4477100ce4a33075c7329589c29d052fd21cc11d65`
- `santiment:bitcoin:exchange_outflow_usd:2026-03-31T13:10:10Z:2026-04-14T13:10:10Z`: 15 points, sha256 `f9eb8d5d2b1aea07370991f9a08db6965d8e63d69b3a0619f9fe3d94fe8e32e8`
