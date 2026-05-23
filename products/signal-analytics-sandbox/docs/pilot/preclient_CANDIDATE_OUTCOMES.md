# Pre-Client Candidate Outcomes

Date: 2026-05-23T15:30:00Z
Status: `internal_candidate_outcome_rr_recompute`

## Boundary

- Rows are internal-only and blocked from customer-facing metrics.
- No bulk market-history storage is used.
- Post-factum screenshots are not treated as predictive calls.

## Totals

- `candidate_count`: 9
- `by_candidate_status`: {'insufficient_fields': 4, 'post_factum_only': 4, 'provider_gap': 1}
- `rr_recomputed_internal_count`: 1
- `market_outcome_recomputed_count`: 0

## Rows

| channel | post | status | RR status | provider refs | reason | source |
|---|---:|---|---|---|---|---|
| `bablos79` | 10450 | `provider_gap` | `rr_recomputed_internal` | moex_iss_candidate_symbol=MAGN, provider_gap=unapproved_contract_or_quote_scale | RR math is internally computable, but the extracted MAGN-6.26/MMK notation needs an approved exact public provider/proxy before market outcome recompute. | [source](https://t.me/bablos79/10450) |
| `nemphiscrypts` | 3958 | `insufficient_fields` | `rr_not_recomputed` | binance_public_klines_candidate, provider_not_called_due_candidate_status | Missing target field prevents deterministic RR/outcome recompute. | [source](https://t.me/nemphiscrypts/3958) |
| `pifagortrade` | 3214 | `insufficient_fields` | `rr_not_recomputed` | binance_public_klines_candidate, provider_not_called_due_candidate_status | Missing target field prevents deterministic RR/outcome recompute. | [source](https://t.me/pifagortrade/3214) |
| `pifagortrade` | 3218 | `insufficient_fields` | `rr_not_recomputed` | binance_public_klines_candidate, provider_not_called_due_candidate_status | Extracted entry/stop values look like Fibonacci ratios rather than market prices. | [source](https://t.me/pifagortrade/3218) |
| `pifagortrade` | 3225 | `post_factum_only` | `rr_not_recomputed` | binance_public_klines_candidate, provider_not_called_due_candidate_status | Screenshot appears to describe managed or closed position state, not a clear source-time predictive call. | [source](https://t.me/pifagortrade/3225) |
| `pifagortrade` | 3234 | `insufficient_fields` | `rr_not_recomputed` | binance_public_klines_candidate, provider_not_called_due_candidate_status | Targets conflict with the inferred long direction and need operator classification. | [source](https://t.me/pifagortrade/3234) |
| `pifagortrade` | 3264 | `post_factum_only` | `rr_not_recomputed` | binance_public_klines_candidate, provider_not_called_due_candidate_status | Screenshot appears to describe managed or closed position state, not a clear source-time predictive call. | [source](https://t.me/pifagortrade/3264) |
| `pifagortrade` | 3274 | `post_factum_only` | `rr_not_recomputed` | binance_public_klines_candidate, provider_not_called_due_candidate_status | Screenshot appears to describe managed or closed position state, not a clear source-time predictive call. | [source](https://t.me/pifagortrade/3274) |
| `pifagortrade` | 3276 | `post_factum_only` | `rr_not_recomputed` | binance_public_klines_candidate, provider_not_called_due_candidate_status | Screenshot appears to describe managed or closed position state, not a clear source-time predictive call. | [source](https://t.me/pifagortrade/3276) |