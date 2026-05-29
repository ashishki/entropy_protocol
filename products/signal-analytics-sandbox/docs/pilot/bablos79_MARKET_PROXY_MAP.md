# Market Proxy Map - bablos79

Date: 2026-05-15
Status: no_proxy_approved_no_market_fetch

This map reviews the 14 reviewable non-blocker rows in
`docs/pilot/bablos79_CLAIM_LEDGER.json` and decides whether any claim has a safe
market proxy for deterministic outcome evaluation. No proxy is approved in this
pass because every candidate is missing at least one required field: approved
review state, direction, horizon/event window, explicit asset/proxy, or
human/operator media acceptance.

## Summary

| Field | Count |
|---|---:|
| total ledger rows | 67 |
| reviewable non-blocker claim rows reviewed here | 14 |
| proxy-approved claims | 0 |
| market-data fetch rows | 0 |
| non-measurable/unresolved rows | 14 |
| hidden proxy guesses allowed | 0 |

## Proxy Decision Rules

| Rule | Decision |
|---|---|
| Named ticker plus direction but no horizon | Do not fetch; mark unresolved horizon. |
| Close/reduce/management without original setup | Do not reconstruct a trade; mark unresolved original setup. |
| Broad "market", "exchange", or macro claim | Do not invent a ticker; require explicit operator-approved proxy. |
| LLM-reviewed internal transcript claim | Internal context only; no external or deterministic metric without human/operator acceptance and proxy approval. |
| Watchlist/deferral language | Context only; no strict win/loss fetch. |
| Unsupported media blocker | Excluded from proxy mapping until source-linked and reviewed. |

## Candidate Proxy Rows

| claim_id | category | asset/proxy candidates | direction | horizon | proxy decision | unresolved reason | fetch plan |
|---|---|---|---|---|---|---|---|
| `claim_text_bablos79_10442` | `directional_bias` | `X5` | `unknown` | none | `unresolved_no_proxy` | Ticker candidate exists, but direction, horizon, entry, stop, and target are missing. | none |
| `claim_text_bablos79_10443` | `directional_bias` | `VTBR` | `unknown` | none | `unresolved_no_proxy` | Ticker candidate exists, but direction, horizon, entry, stop, and target are missing. | none |
| `claim_text_bablos79_10450` | `directional_bias` | `MAGN` | `negative` | none | `candidate_only_no_fetch` | Asset and negative historical short language exist, but current entry/stop/target and horizon are missing. | none |
| `claim_text_bablos79_10459` | `directional_bias` | `AMD` | `negative` | none | `context_only_no_fetch` | Author explicitly says he will not short yet; no current trade or deterministic horizon exists. | none |
| `claim_text_bablos79_10464` | `level_timing_call` | `X5` | `management` | none | `unresolved_no_proxy` | Close/re-entry language lacks original setup and evaluable levels. | none |
| `claim_text_bablos79_10465` | `macro_context` | none | `unknown` | none | `non_measurable_no_proxy` | Macro/geopolitical context has no approved market benchmark, direction, horizon, or outcome method. | none |
| `claim_text_bablos79_10470` | `watchlist` | none | `unknown` | none | `context_only_no_fetch` | Currency-market watch language says signs may appear later; no explicit pair/proxy or current call. | none |
| `claim_text_bablos79_10499` | `level_timing_call` | `SFIN` | `management` | none | `unresolved_no_proxy` | Close/exit language lacks original setup, entry, stop, target, and horizon. | none |
| `claim_text_bablos79_10500` | `level_timing_call` | `CHMF` | `management` | none | `unresolved_no_proxy` | Partial fixation and moved stop lack original setup fields and explicit outcome method. | none |
| `claim_text_bablos79_10501` | `level_timing_call` | `MAGN` | `management` | none | `unresolved_no_proxy` | Partial close and moved stop lack original setup fields and explicit outcome method. | none |
| `claim_text_bablos79_10504` | `directional_bias` | none | `management` | none | `unresolved_no_proxy` | Short-management language implies negative picture, but asset/proxy and horizon are absent. | none |
| `claim_transcript_bablos79_10476_claim1` | `macro_context` | `global geopolitics, US, UK, Russia` | `negative` | none | `non_measurable_internal_only` | Broad geopolitical thesis has no explicit asset/proxy or measurable outcome; transcript is LLM-reviewed internal only. | none |
| `claim_transcript_bablos79_10476_claim2` | `directional_bias` | `Московская биржа, широкий рынок активов` | `negative` | `майские праздники` | `operator_proxy_required_no_fetch` | A Russian exchange proxy might be possible only after explicit operator approval; transcript is not human/operator accepted. | none |
| `claim_transcript_bablos79_10478_claim1` | `event_risk` | `Российская биржа` | `negative` | `майские праздники` | `operator_proxy_required_no_fetch` | A Russian exchange proxy might be possible only after explicit operator approval and event-window definition; transcript is not human/operator accepted. | none |

## Broad Claim Proxy Policy

Broad claims may become useful author insights, but they do not receive hidden
proxy mappings. For example, "Russian exchange" could later be mapped to an
operator-approved benchmark such as a local Russian equity index only if Phase
24 records:

- exact proxy instrument and data source;
- timestamp basis;
- event/horizon window;
- claim wording preserved from the source;
- human/operator acceptance for transcript-backed external use if needed;
- outcome method before market data is fetched.

Until those fields exist, broad claims remain `non_measurable`,
`operator_proxy_required_no_fetch`, or `non_measurable_internal_only`.

## Market-Data Fetch Plan

| fetch_id | claim_id | asset/proxy | data source | timestamp basis | horizon | status |
|---|---|---|---|---|---|---|
| none | none | none | none | none | none | `no_fetch_allowed` |

No market data should be fetched for this source/window in the current state.
Every candidate either lacks required deterministic fields or requires explicit
operator proxy approval first.

## Next Gate

`SAS-DR-015` outcome evaluation must produce zero computed outcomes unless a
later task adds approved proxy rows with source timestamp, horizon, data source,
and market snapshot references.
