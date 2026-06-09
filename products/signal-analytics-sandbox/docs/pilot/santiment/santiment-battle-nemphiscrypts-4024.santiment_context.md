# Santiment Context Artifact

Candidate: `santiment-battle-nemphiscrypts-4024`
Source: `nemphiscrypts`
Asset: `ETH` / `ethereum`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-01T13:59:04Z`
Window: `2026-04-24T13:59:04Z` to `2026-05-08T13:59:04Z`
Artifact SHA-256: `29ed7ad4f62d3ac7992137ec3417bac9498fa0c3323d427c7238c5eb01316d91`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 2294.990847883549 | 2316.095195313837 | 21.104347430288 | 0.9195830758867960282036354701 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 1404 | 1160 | -244 | -17.37891737891737891737891738 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.038549083144 | -0.031423629741 | -0.069972712885 | -181.515893967223844694821051 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 598311 | 439971 | -158340 | -26.46449756063318240847987084 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 495547135.22804654 | 156022096.28718546 | -339525038.94086108 | -68.51518549988480310615275831 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 485532339.52336717 | 141300240.4309037 | -344232099.09246347 | -70.89787251460654632730774332 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:ethereum:price_usd:2026-04-24T13:59:04Z:2026-05-08T13:59:04Z`: 15 points, sha256 `e8aa751533fd6e72cb0cb845f4ad0aa38b7f55b5404bd919eb8182f4f93985ee`
- `santiment:ethereum:social_volume_total:2026-04-24T13:59:04Z:2026-05-08T13:59:04Z`: 15 points, sha256 `617d4c45400e433948696994aab051818259122785688d7e5f31c22ed913f9ef`
- `santiment:ethereum:sentiment_weighted_total:2026-04-24T13:59:04Z:2026-05-08T13:59:04Z`: 15 points, sha256 `b5ae8e840b4fc696897ddfab8ef26b6edb4a3a6cee015522af6c3532a448427f`
- `santiment:ethereum:daily_active_addresses:2026-04-24T13:59:04Z:2026-05-08T13:59:04Z`: 15 points, sha256 `8c627d1bf47baa9e0328e3998466ce2355472512e52f27518cea64d2999b258f`
- `santiment:ethereum:exchange_inflow_usd:2026-04-24T13:59:04Z:2026-05-08T13:59:04Z`: 15 points, sha256 `22c33192b1551b088729c312b4b5f87da5e54d757d979ae6493a27044efc6c75`
- `santiment:ethereum:exchange_outflow_usd:2026-04-24T13:59:04Z:2026-05-08T13:59:04Z`: 15 points, sha256 `d0f9a97a295b2baa192f2c6b7a38eabc0e3e153e509ea0d8135f260b26de1df1`
