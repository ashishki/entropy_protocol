# FX Proxy Policy

Date: 2026-05-19
Status: internal_policy_no_fx_proxy_approved

## Scope

This policy controls currency and FX shorthand claims in Signal Analytics
Sandbox reports. It applies to rows containing `CNY`, `CN`, fiat currency names,
or pair-like shorthand where the source text does not explicitly define the
tradable pair.

## Current Decision

No FX shorthand is scoreable by default. `CNY`, `CN`, and similar shorthand stay
`needs_operator_input` in provider/proxy routing until an operator approves all
required fields below.

## Required Approval Fields

| Field | Requirement |
|---|---|
| Pair | Exact pair such as `USDCNY`, `USDRUB`, or `EURUSD`; shorthand alone is insufficient. |
| Direction semantics | Define whether long means long base currency, long quote currency, or local-market proxy direction. |
| Provider | Exact public provider route and symbol. |
| Horizon | Approved evaluation horizon and candle interval. |
| Source wording | Evidence span must contain pair/direction linkage or a reviewed neighboring sentence. |
| Exclusions | Ambiguous macro/currency commentary remains context-only or provider-gap exclusion. |

## Direction Semantics

- Long `BASE/QUOTE`: score raw forward return of the approved pair.
- Short `BASE/QUOTE`: score negative raw forward return of the approved pair.
- Local shorthand such as `CNY` does not imply `USDCNY`, `CNYRUB`, or a basket.
- Currency macro commentary without a pair is not a win/loss row.

## Provider Policy

No FX provider is approved in this policy version. Future approval must name the
provider, provider symbol, timezone/candle convention, and whether the route is
prototype, internal-only, or production-eligible.

## Stop Conditions

- Do not silently map `CNY`, `CN`, `USD`, `EUR`, or similar shorthand to a pair.
- Do not infer direction from macro context alone.
- Do not score FX rows until pair, provider, and direction semantics are
  operator-approved.
- Unsupported FX rows remain exclusions, not wins or losses.

