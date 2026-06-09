# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3213`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-03-27T14:00:15Z`
Window: `2026-03-20T14:00:15Z` to `2026-04-03T14:00:15Z`
Artifact SHA-256: `c83eb65db2bdee36a42b6b16abafe1efe76d4e1b8b877a3320b603789180cf42`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 66327.30936010739 | 66319.6918007053 | -7.61755940209 | -0.01148480086947652789928620309 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2831 | 2057 | -774 | -27.34016248675379724478982692 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.014898701902 | -0.027560956843 | -0.042459658745 | -284.9889810823063744792012552 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 644952 | 558679 | -86273 | -13.376654386683039978168918 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 3089894081.2079563 | 942504086.3530341 | -2147389994.8549222 | -69.49720405999892220361764761 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 2940295647.5768127 | 880865023.8985589 | -2059430623.6782538 | -70.0416172562610625250670463 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-03-20T14:00:15Z:2026-04-03T14:00:15Z`: 15 points, sha256 `a6b6d44427c56295585605e4226889e2fa7ff08a234f12fc9e0950133f6077f6`
- `santiment:bitcoin:social_volume_total:2026-03-20T14:00:15Z:2026-04-03T14:00:15Z`: 15 points, sha256 `a4d6cc1c0c2bb20ff62a389df9c6be8044d75472a427b55b5163921931d4434d`
- `santiment:bitcoin:sentiment_weighted_total:2026-03-20T14:00:15Z:2026-04-03T14:00:15Z`: 15 points, sha256 `38f820450d2a6569f4e06892825450dff142e6f4cd7418ea27ed26d0cf94f2dd`
- `santiment:bitcoin:daily_active_addresses:2026-03-20T14:00:15Z:2026-04-03T14:00:15Z`: 15 points, sha256 `9381345dcb29b73e1aceebe05bf8180579af9ddde2b5eaa4f641c491ca6c25d8`
- `santiment:bitcoin:exchange_inflow_usd:2026-03-20T14:00:15Z:2026-04-03T14:00:15Z`: 15 points, sha256 `dc1ee8fbac8c935c09ae9def051380280e13f3df608f6d5b7245d49ee5c63c53`
- `santiment:bitcoin:exchange_outflow_usd:2026-03-20T14:00:15Z:2026-04-03T14:00:15Z`: 15 points, sha256 `632402f356ad1f3127b6ef2f1c52a505158efaad1dc571c2eb5662b303113096`
