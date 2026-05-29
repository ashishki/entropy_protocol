# Three-Channel V1 Extractor Calibration

Date: 2026-05-19
Status: internal_v1_rules

## Source

Calibration is derived from
`docs/pilot/three_channel_V1_EXTRACTION_REVIEW.md`.

## Required Deterministic Rule Changes

| Rule id | Change | Applies to | Reason |
|---|---|---|---|
| cal-001 | Add negation-aware direction parsing for phrases equivalent to "no buys", "not bullish", "not a long", and "not a short". | `directional_thesis` | Prevent inverted long/short outcomes. |
| cal-002 | Reclassify closed/reduced/moved-stop language as `trade_management` unless an approved original setup link is present. | `position_disclosure`, `trade_management` | Prevent management fragments from becoming new calls. |
| cal-003 | Put "if above/below", "if there is an entry", trap-line, safety-line, and similar conditional level language into `trade_setup`. | `trade_setup` | Enables level-aware outcome engine instead of immediate fixed-horizon scoring. |
| cal-004 | Expand asset aliases for BTC/Bitcoin/BTCUSD and ETH/Ether while preserving evidence spans. | crypto extraction | Reduces false negatives in informal Russian crypto text. |
| cal-005 | Block known non-asset tokens such as `SIGN-UP`, person names, channel names, and marketing nouns. | asset extraction | Reduces false assets from public text noise. |
| cal-006 | Require asset and direction evidence to appear in the same sentence or linked neighboring sentence unless the row is `needs_context`. | all claim types | Reduces source-context drift. |
| cal-007 | Keep futures, FX, US ETF/fund, commodity, and broad-index aliases excluded until provider/proxy expansion approves the exact mapping. | provider/proxy routing | Prevents unsupported rows from becoming wins/losses. |
| cal-008 | Treat transcript/OCR/chart-derived text as `internal_only_pending_review` unless a human/operator review artifact accepts the source. | multimodal claims | Preserves media review boundary. |
| cal-009 | Plain uppercase BTC/ETH/TON aliases require token boundaries so `BTC` matches but embedded noise like `BTCPARSER` does not. | crypto extraction | Closes false negatives without creating parser-token false positives. |

## V1 Extractor Acceptance Rules

| Claim type | Required fields | If missing |
|---|---|---|
| `directional_thesis` | source URL, timestamp, asset/proxy, direction, evidence span | `needs_context` or exclusion |
| `position_disclosure` | source URL, timestamp, asset/proxy, side, explicit position/holding/open wording | `needs_context` |
| `trade_setup` | source URL, timestamp, asset/proxy, conditional entry or level evidence; optional stop/target | structured setup with null missing fields |
| `trade_management` | source URL, timestamp, asset/proxy, action, linked original setup id | exclude unless linked |
| `market_context` | source URL, timestamp, context category | context only |
| `risk_warning` | source URL, timestamp, risk text | context only |

## Stop Conditions

- Do not infer missing prices, entry levels, stops, targets, or directions.
- Do not convert unsupported provider/proxy classes into market-data requests.
- Do not score unreviewed media/OCR/chart claims.
- Do not publish V1 metrics externally before the external-ready gate.

## False-Negative Pass Results

Derived from `docs/pilot/three_channel_FALSE_NEGATIVE_PASS.md`.

| pass_id | source | result | calibration effect |
|---|---|---|---|
| `fn-001` | `nemphiscrypts` 3344 | `extracted` BTC long directional thesis | close by linking to the existing V1 included BTC claim; do not duplicate metrics. |
| `fn-002` | `nemphiscrypts` 3352 | `needs_context` | quoted/contrasted sentiment needs author-side separation before scoring. |
| `fn-003` | `pifagortrade` 2298 | `needs_context` | safety/trap-line alt basket lacks exact asset, level, and prior context link. |
| `fn-004` | `pifagortrade` 2510 | `extracted` conditional BTC trap-line setup | structured setup only; not fixed-horizon scoreable until trap-line level is accepted. |
| `fn-005` | `pifagortrade` 2578 | `extracted` BTC trade management | context only until original setup link exists; `SIGN-UP` remains blocked. |
