# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3255`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-02T12:09:53Z`
Window: `2026-04-25T12:09:53Z` to `2026-05-09T12:09:53Z`
Artifact SHA-256: `5bff2bf1f98f82fac328139d1b0633999ec68f7758c7ef86477f0eb1fd83d76f`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 78652.93562535982 | 78540.29035929906 | -112.64526606076 | -0.1432181331378560004172042199 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2632 | 2263 | -369 | -14.01975683890577507598784195 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.006629568941 | 0.028728163952 | 0.022098595011 | 333.3338141237680810475487595 | up_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 627342 | 583390 | -43952 | -7.006066866238829856760746132 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 1604121950.6718028 | 1902553115.941971 | 298431165.2701682 | 18.60401979694784888964021947 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 1638338154.1416204 | 1934793161.2106497 | 296455007.0690293 | 18.09486071722182976597074207 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-25T12:09:53Z:2026-05-09T12:09:53Z`: 15 points, sha256 `e6c42ce791d529ff62f97439ec5b2958b7e8f2e8cc9801c3a17c6ca8b6838efc`
- `santiment:bitcoin:social_volume_total:2026-04-25T12:09:53Z:2026-05-09T12:09:53Z`: 15 points, sha256 `a48fea54f0614d1711d184cf5e5f8cec66a1a7be40557da7e63b56afdcc99495`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-25T12:09:53Z:2026-05-09T12:09:53Z`: 15 points, sha256 `e852a51e8f1acaa537f2d2d1a3e8be708df80d4dfdbbe3ab98e0d086ba911d4d`
- `santiment:bitcoin:daily_active_addresses:2026-04-25T12:09:53Z:2026-05-09T12:09:53Z`: 15 points, sha256 `75b4e198a0970becdf525f427d8b047d0e9f3d1b11c595e3ab4a65f9c18199ef`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-25T12:09:53Z:2026-05-09T12:09:53Z`: 15 points, sha256 `01910ef54b014ccc6293730a846334c4ca5ecc50fc2174ba060803da2e9d6b0d`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-25T12:09:53Z:2026-05-09T12:09:53Z`: 15 points, sha256 `8edc166b4f84021f831379b1d68cf47dd282c23618e236f55e6e6491649dd858`
