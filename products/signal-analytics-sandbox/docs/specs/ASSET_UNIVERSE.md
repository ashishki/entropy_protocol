# Asset Universe And Alias Registry

Version: 0.1
Date: 2026-05-09
Status: specification for `SAS-MI-003`

## Purpose

The asset universe maps author text aliases to canonical asset IDs without
guessing. It is the first bridge between public source evidence and future
deterministic market-data metrics.

This task does not fetch market data.

## Schemas

### Asset

| Field | Required | Rule |
|-------|----------|------|
| `canonical_id` | yes | Stable ID such as `CRYPTO:BTC`, `US:SPY`, or `MOEX:MAGN`. |
| `instrument_type` | yes | `crypto`, `equity`, `fund`, `index`, `macro_proxy`, or `unresolved`. |
| `display_symbol` | yes | Human-readable symbol for reports and review queues. |
| `provider_symbols` | yes | Mapping from provider ID to provider-specific symbol; can be empty for unresolved fallback. |
| `aliases` | yes | Exact text aliases accepted for deterministic lookup. |
| `exchange` | no | Exchange where applicable, e.g. `NASDAQ`, `NYSEARCA`, `MOEX`. |
| `venue` | no | Coarser venue such as `crypto`, `us_equity`, or `equity`. |
| `provenance` | yes | Why the asset is in the seed registry. |

### AssetAlias

| Field | Required | Rule |
|-------|----------|------|
| `alias` | yes | Exact observed or configured alias. |
| `canonical_id` | yes | Target asset ID. |
| `source` | yes | Source of the alias rule, e.g. seed registry or channel profile. |
| `provenance` | yes | Evidence or rationale for including the alias. |

## Resolution Semantics

Resolution normalizes aliases by trimming whitespace, removing a leading `#` or
`$`, and uppercasing. It then performs exact lookup only.

| Status | Meaning |
|--------|---------|
| `exact` | One canonical asset matched. |
| `ambiguous` | More than one canonical asset matched; caller must review. |
| `unresolved` | No canonical asset matched; caller must preserve the evidence instead of guessing. |

Every resolution result includes the original query, normalized query, matched
assets, and evidence reference.

## Seed Coverage

The seed registry includes:

- crypto: BTC, ETH, SOL;
- funds: SPY, QQQ;
- Phase 10 observed public-capture tickers: AMD, CHMF, GAZP, MAGN, SBER, SFIN,
  VKCO, VTBR, X5;
- unresolved fallback marker.

The seed registry is not a market-data source and does not assert that provider
symbols are canonical for final pricing. Later market-data tasks must validate
provider coverage, licensing, timestamp semantics, and snapshot provenance.

## Non-Goals

- No market-data fetches.
- No price/provider validation.
- No fuzzy matching, semantic matching, or LLM alias guessing.
- No RAG/vector storage.
- No approved ledger or `MarketIdea` writes.

## Future Work

`SAS-MI-004` defines the market-data store contract. `SAS-MI-005` defines
deterministic horizon metrics. Those tasks may consume canonical IDs from this
registry but must not reinterpret unresolved aliases as resolved assets.
