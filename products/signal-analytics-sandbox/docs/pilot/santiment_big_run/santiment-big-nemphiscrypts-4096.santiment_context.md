# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4096`
Source: `nemphiscrypts`
Asset: `ETH` / `ethereum`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-20T08:38:55Z`
Window: `2026-05-13T08:38:55Z` to `2026-05-27T08:38:55Z`
Artifact SHA-256: `70ce03b0bfa3a277ee21f20bf8c9b9cf361cac22583daedc2e2268681b5d39f4`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 2127.362664798115 | 2131.370076481668 | 4.007411683553 | 0.1883746363450117300326471101 | up_price_context_after_post |

## Metric Refs

- `santiment:ethereum:price_usd:2026-05-13T08:38:55Z:2026-05-27T08:38:55Z`: 15 points, sha256 `0e9b967ced62110accf2e332196c6d4c0089be50f425ff78b741768f206a6490`
- `santiment:ethereum:social_volume_total:2026-05-13T08:38:55Z:2026-05-27T08:38:55Z`: 0 points, sha256 `fd93ac97ecfbca1a6b63e228c9e88447e46123aa52e06fec3d4b0616e353fb3d`
- `santiment:ethereum:sentiment_weighted_total:2026-05-13T08:38:55Z:2026-05-27T08:38:55Z`: 0 points, sha256 `77f8424eb39e16391c7bc03d9eb8b7cad9695ebf2d07b1bf20efa158bcc4305b`
- `santiment:ethereum:daily_active_addresses:2026-05-13T08:38:55Z:2026-05-27T08:38:55Z`: 0 points, sha256 `f59360238de767f60175260d67777f0a9e415729b5c151e13ad3f1e867bdab7c`
- `santiment:ethereum:exchange_inflow_usd:2026-05-13T08:38:55Z:2026-05-27T08:38:55Z`: 0 points, sha256 `83cb5b109391f498abcc6de3bb0a536c1e0f569cc41de4aac75949a46b434c7c`
- `santiment:ethereum:exchange_outflow_usd:2026-05-13T08:38:55Z:2026-05-27T08:38:55Z`: 0 points, sha256 `2e2a209719b88fe72486627a6b85962dcf60d0cbbc454ebd6da4fe14e2b303dc`

## Blockers

- `missing_santiment_points:social_volume_total`
- `missing_santiment_points:sentiment_weighted_total`
- `missing_santiment_points:daily_active_addresses`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
