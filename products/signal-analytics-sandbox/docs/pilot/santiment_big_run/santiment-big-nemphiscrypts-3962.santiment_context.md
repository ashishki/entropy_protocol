# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-3962`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-07T06:40:03Z`
Window: `2026-03-31T06:40:03Z` to `2026-04-14T06:40:03Z`
Artifact SHA-256: `f5de6184ea3d31b84b59413e0fc49ba00521adc8154192453f3c712c00cf73f4`

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

- `santiment:bitcoin:price_usd:2026-03-31T06:40:03Z:2026-04-14T06:40:03Z`: 15 points, sha256 `aa163dee9d1b2887c3193c7ee3d2e37d6c78c4c49ebe5557a243655ebeda5c16`
- `santiment:bitcoin:social_volume_total:2026-03-31T06:40:03Z:2026-04-14T06:40:03Z`: 15 points, sha256 `2ebcb91372e0ef54ee2e4b89d289c349d8cd65a580c5c5489464a74b245eb3df`
- `santiment:bitcoin:sentiment_weighted_total:2026-03-31T06:40:03Z:2026-04-14T06:40:03Z`: 15 points, sha256 `789404388e9d42b5b4953712b13301df92b6b53b3fdc1ed4add90b0ec30b83cd`
- `santiment:bitcoin:daily_active_addresses:2026-03-31T06:40:03Z:2026-04-14T06:40:03Z`: 15 points, sha256 `510e2a1005a890eed9938c6a9cbf19127ae6e9913ade391190e31190de3942cc`
- `santiment:bitcoin:exchange_inflow_usd:2026-03-31T06:40:03Z:2026-04-14T06:40:03Z`: 15 points, sha256 `8ef70c6e1b6ed0cfacd2bbc4818730a583d33830d2ebaccf544842271b1863bd`
- `santiment:bitcoin:exchange_outflow_usd:2026-03-31T06:40:03Z:2026-04-14T06:40:03Z`: 15 points, sha256 `0e7d70db4ec70e7f36d524a72cc68e6a4aef412dc5ad172811cd6be74d689032`
