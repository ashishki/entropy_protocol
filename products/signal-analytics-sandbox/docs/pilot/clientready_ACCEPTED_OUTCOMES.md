# Client-Ready Accepted Outcomes

Date: 2026-05-29
Status: `clientready_accepted_outcome_recompute`
Source ledger: `docs/pilot/clientready_OPERATOR_MEDIA_LEDGER.json`

## Boundary

- This artifact recomputes only rows with explicit `operator_decision:
  accepted`.
- The current operator ledger has 0 accepted rows.
- Therefore no RR or market outcome row is recomputed in this pass.
- Exclusions are not wins, losses, dashboard-safe rows, or paid-report-safe
  rows.
- No bulk market-history storage is used.

## Counts

- `candidate_count`: 9
- `operator_accepted_rows`: 0
- `recomputed_rows`: 0
- `excluded_rows`: 9
- `buyer_demo_safe_rows`: 0
- `wins`: 0
- `losses`: 0
- `excluded_operator_not_accepted`: 5
- `excluded_post_factum_only`: 4

## Rows

| channel | post | source | operator decision | prior status | recompute status | provider/proxy provenance | buyer demo safe |
|---|---:|---|---|---|---|---|---:|
| `bablos79` | 10450 | [source](https://t.me/bablos79/10450) | `needs_context` | `provider_gap` | `excluded_operator_not_accepted` | `moex_iss_candidate_symbol=MAGN`; `provider_gap=unapproved_contract_or_quote_scale` | false |
| `nemphiscrypts` | 3958 | [source](https://t.me/nemphiscrypts/3958) | `needs_context` | `insufficient_fields` | `excluded_operator_not_accepted` | `binance_public_klines_candidate`; `provider_not_called_due_candidate_status` | false |
| `pifagortrade` | 3214 | [source](https://t.me/pifagortrade/3214) | `needs_context` | `insufficient_fields` | `excluded_operator_not_accepted` | `binance_public_klines_candidate`; `provider_not_called_due_candidate_status` | false |
| `pifagortrade` | 3218 | [source](https://t.me/pifagortrade/3218) | `needs_context` | `insufficient_fields` | `excluded_operator_not_accepted` | `binance_public_klines_candidate`; `provider_not_called_due_candidate_status` | false |
| `pifagortrade` | 3225 | [source](https://t.me/pifagortrade/3225) | `post_factum_only` | `post_factum_only` | `excluded_post_factum_only` | `binance_public_klines_candidate`; `provider_not_called_due_candidate_status` | false |
| `pifagortrade` | 3234 | [source](https://t.me/pifagortrade/3234) | `needs_context` | `insufficient_fields` | `excluded_operator_not_accepted` | `binance_public_klines_candidate`; `provider_not_called_due_candidate_status` | false |
| `pifagortrade` | 3264 | [source](https://t.me/pifagortrade/3264) | `post_factum_only` | `post_factum_only` | `excluded_post_factum_only` | `binance_public_klines_candidate`; `provider_not_called_due_candidate_status` | false |
| `pifagortrade` | 3274 | [source](https://t.me/pifagortrade/3274) | `post_factum_only` | `post_factum_only` | `excluded_post_factum_only` | `binance_public_klines_candidate`; `provider_not_called_due_candidate_status` | false |
| `pifagortrade` | 3276 | [source](https://t.me/pifagortrade/3276) | `post_factum_only` | `post_factum_only` | `excluded_post_factum_only` | `binance_public_klines_candidate`; `provider_not_called_due_candidate_status` | false |

## Result

There are no accepted rows to recompute. Rows with missing fields, provider
gaps, unresolved operator context, or post-factum status remain exclusions, not
wins or losses. The buyer-demo-safe count remains 0.
