# Three-Channel V2 Robustness Appendix

Date: 2026-05-19
Status: internal_v2_robustness_not_external_ready
Primary input: `docs/pilot/three_channel_V1_METRIC_RESULTS.json`

## Purpose

This appendix records sensitivity checks required before any stronger channel
utility conclusion. Current V1 metrics use one primary horizon and approved
provider paths available at the time of recompute. They are useful for internal
diagnostics, but not robust enough for external delivery.

## Current Robustness State

| Channel | Evaluable outcomes | Sample warning | Provider posture | Robustness status |
|---|---:|---|---|---|
| `bablos79` | 14 | thin_sample, small_type_bucket | mixed Binance/MOEX with 75 provider-gap rows | not_robust |
| `nemphiscrypts` | 49 | provisional_sample | Binance-only outcomes with 128 provider-gap rows | not_robust |
| `pifagortrade` | 107 | provider_coverage_warning | Binance-only outcomes with 162 provider-gap rows | not_robust |

## Horizon Sensitivity

Current reported outcomes use the V1 primary `7d` horizon. Before any stronger
claim, rerun each channel on at least these horizons:

- `1d`: checks whether calls were short-lived or immediately contradicted;
- `3d`: checks near-term follow-through;
- `7d`: current primary internal baseline;
- `14d`: checks whether slower theses reverse the 7d result.

Required horizon flags:

- `horizon_not_recomputed`: appendix exists but alternate horizons are not yet
  calculated;
- `horizon_instability`: hit rate or average return changes by more than 10
  percentage points between supported horizons;
- `horizon_sparse_bucket`: fewer than 30 evaluable outcomes for a channel or
  fewer than 10 for a claim type at a horizon.

No channel should be described as stable until the direction of the conclusion
survives the supported horizon set.

## Provider Sensitivity

Provider assumptions can move outcomes when assets, symbols, sessions,
corporate actions, futures rolls, or benchmark mappings differ.

Required provider checks:

- compare Binance spot/USDT crypto outcomes against any later approved crypto
  provider where the same asset and horizon are available;
- compare MOEX ISS equity outcomes against any later approved secondary source
  before external delivery;
- keep `yfinance_dev` US equity/fund rows internal-only until provider terms,
  symbol mapping, and corporate-action handling are documented;
- keep FX, futures, commodities, and index shorthand excluded until exact
  instrument, direction semantics, provider, rollover, and horizon are
  approved.

Provider flags:

- `provider_gap_material`: provider-gap rows exceed 20 percent of accepted or
  market-adjacent rows;
- `single_provider_only`: all evaluable outcomes for a channel depend on one
  provider family;
- `proxy_not_approved`: exact tradable proxy is not approved.

## Sample-Size Sensitivity

The Quant Metrics V2 confidence policy applies:

- `thin_sample`: fewer than 30 evaluable outcomes;
- `provisional_sample`: 30 to 99 evaluable outcomes;
- `small_type_bucket`: fewer than 10 evaluable outcomes for a claim type;
- `low_review_coverage`: extracted rows are not durably reviewed;
- `low_provider_coverage`: accepted rows are not mostly scoreable by approved
  providers.

Small samples must not be overclaimed:

- `bablos79` has only 14 V1 evaluable outcomes, so any hit-rate or return
  statement is descriptive only.
- `nemphiscrypts` has 49 V1 evaluable outcomes, so channel-level outcomes are
  provisional and claim-type splits are likely sparse.
- `pifagortrade` has 107 V1 evaluable outcomes, but provider gaps and review
  coverage still block durable conclusions.

## Minimum Robustness Gate

A channel can move from internal diagnostic to stronger validated reporting only
after all of these are true:

- at least 100 evaluable outcomes for channel-level outcome claims;
- no claim-type bucket reported as a rate with fewer than 10 evaluable rows;
- horizon sensitivity has been recomputed for 1d, 3d, 7d, and 14d where data
  exists;
- provider-gap rows are explicitly counted and not material to the conclusion;
- benchmark-relative rows have approved benchmark data when used;
- setup/RR rows use explicit entry, stop, target, fill, timeout, and R multiple;
- external-ready gate is rerun and approves delivery.

## Current Conclusion

Robustness decision: `not_robust_for_external_delivery`.

The current three-channel V2 artifacts can support internal product and
engineering decisions. They cannot support public sales claims, channel
ordering, investment advice, or durable performance claims.
