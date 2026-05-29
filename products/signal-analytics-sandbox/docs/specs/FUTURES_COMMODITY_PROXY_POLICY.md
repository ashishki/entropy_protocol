# Futures And Commodity Proxy Policy

Date: 2026-05-19
Status: internal_policy_no_continuous_proxy_approved

## Scope

This policy controls futures, commodity, and broad-index shorthand such as
`BR`, `NG`, `GOLD`, `SI`, `MIX`, and `IMOEX`.

## Current Decision

No continuous futures, commodity, or index proxy is scoreable by default. The
current provider/proxy config keeps these symbols as `needs_operator_input`
until a specific contract/proxy route is approved.

## Required Approval Fields

| Field | Requirement |
|---|---|
| Instrument | Exact futures contract, spot instrument, ETF, index, or provider symbol. |
| Direction semantics | Define whether long/short applies to contract price, spread, ETF proxy, spot commodity, or index level. |
| Rollover rule | Required for any continuous futures proxy; must define roll schedule and price adjustment method. |
| Provider | Exact public provider route, provider symbol, timezone, candle interval, and retention policy. |
| Horizon | Approved scoring horizon and whether weekends/holidays are skipped. |
| Exclusions | Ambiguous shorthand remains provider-gap exclusion, not a win/loss row. |

## Symbol Decisions

| Symbol | Current status | Reason |
|---|---|---|
| `BR` | `needs_operator_input` | Oil futures shorthand lacks contract, rollover, and provider rule. |
| `NG` | `needs_operator_input` | Gas futures shorthand lacks contract, rollover, and provider rule. |
| `GOLD` | `needs_operator_input` | Could mean spot, futures, ETF, local futures, or macro context. |
| `SI` | `needs_operator_input` | Could mean silver, USD/RUB futures, or another local derivative. |
| `MIX` | `needs_operator_input` | Benchmark/index proxy needs provider and direction semantics. |
| `IMOEX` | `needs_operator_input` | Index benchmark route needs provider and benchmark-relative policy. |

## Stop Conditions

- Do not use continuous futures without a rollover rule.
- Do not map commodity shorthand to an ETF or futures contract by default.
- Do not score broad-index rows until benchmark-relative semantics are defined.
- Unsupported futures/commodity/index rows remain exclusions, not wins or
  losses.

