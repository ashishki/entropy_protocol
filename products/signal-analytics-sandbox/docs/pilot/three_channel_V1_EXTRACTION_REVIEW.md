# Three-Channel V1 Extraction Review

Date: 2026-05-19
Status: internal_calibration_review

## Scope

This artifact completes the review surface for `SAS-V1-002`. It samples V0
included claims and public-probe excluded rows across `bablos79`,
`nemphiscrypts`, and `pifagortrade`.

This is an internal calibration pass, not customer-facing acceptance. Rows
marked `accepted` mean the reviewed V0 inclusion/exclusion decision is usable
for internal V1 calibration. Rows marked `false_positive`, `false_negative`, or
`needs_context` become extractor calibration inputs.

## Status Legend

| Status | Meaning |
|---|---|
| `accepted` | Current V0 include/exclude decision is acceptable for internal calibration. |
| `false_positive` | V0 included a row that should be excluded or typed differently. |
| `false_negative` | V0/probe excluded a row that should become a structured V1 claim. |
| `needs_context` | The row may be useful, but needs setup linkage, condition parsing, provider expansion, or human review. |

## Included V0 Claim Review

| review_id | channel | source | V0 asset | V0 type | status | reason |
|---|---|---|---|---|---|---|
| inc-001 | `bablos79` | [10114](https://t.me/bablos79/10114) | `LKOH` long | `directional_thesis` | `false_positive` | Text says the asset is in strong negative and "no buys"; V0 long direction is inverted. |
| inc-002 | `bablos79` | [10208](https://t.me/bablos79/10208) | `PHOR` short | `directional_thesis` | `accepted` | Direct short wording with supported MOEX asset. |
| inc-003 | `bablos79` | [10217](https://t.me/bablos79/10217) | `VTBR` long | `directional_thesis` | `needs_context` | Snippet is commentary around another trader; direct author-side signal needs stronger evidence span. |
| inc-004 | `bablos79` | [10250](https://t.me/bablos79/10250) | `BTC` long | `directional_thesis` | `accepted` | Direct buy wording for Bitcoin. |
| inc-005 | `bablos79` | [10257](https://t.me/bablos79/10257) | `SMLT` long | `trade_setup_or_management` | `needs_context` | Mentions long/levels/stops but lacks extractable entry/stop/target for fixed-horizon scoring. |
| inc-006 | `bablos79` | [10332](https://t.me/bablos79/10332) | `NVTK` short | `position_disclosure_or_management` | `false_positive` | "Closed short" is trade management, not a new short call. |
| inc-007 | `bablos79` | [10335](https://t.me/bablos79/10335) | `SBER` short | `trade_setup_or_management` | `needs_context` | Conditional "if there is an entry point" should not be scored as an immediate short. |
| inc-008 | `nemphiscrypts` | [3344](https://t.me/nemphiscrypts/3344) | `BTC` long | `directional_thesis` | `accepted` | Direct statement that the BTC zone is for long, not short. |
| inc-009 | `nemphiscrypts` | [3367](https://t.me/nemphiscrypts/3367) | `ETH` long | `position_disclosure_or_management` | `needs_context` | Rhetorical prompt around ETH price; side is implied but not a clean setup. |
| inc-010 | `nemphiscrypts` | [3372](https://t.me/nemphiscrypts/3372) | `ETH` long | `directional_thesis` | `accepted` | Explicit claim about ETH growth and dominance. |
| inc-011 | `nemphiscrypts` | [3376](https://t.me/nemphiscrypts/3376) | `BTC` long | `directional_thesis` | `accepted` | Repeats direct BTC long-zone wording. |
| inc-012 | `nemphiscrypts` | [3387](https://t.me/nemphiscrypts/3387) | `BTC` long | `trade_setup_or_management` | `false_positive` | Snippet references memes/agents and regret, not a directly evidenced BTC call. |
| inc-013 | `nemphiscrypts` | [3395](https://t.me/nemphiscrypts/3395) | `BTC` long | `directional_thesis` | `needs_context` | "Closed longs, waiting correction" is management/context, not a fresh long entry. |
| inc-014 | `nemphiscrypts` | [3405](https://t.me/nemphiscrypts/3405) | `BTC` long | `directional_thesis` | `needs_context` | Mentions expectation/chart; needs structured thesis span before scoring. |
| inc-015 | `pifagortrade` | [2334](https://t.me/pifagortrade/2334) | `BTC` long | `directional_thesis` | `needs_context` | Conditional "if above/test level" should become setup logic, not immediate fixed-horizon thesis. |
| inc-016 | `pifagortrade` | [2379](https://t.me/pifagortrade/2379) | `TON` long | `position_disclosure_or_management` | `false_positive` | Telegram monetization news, not a TON directional trade call. |
| inc-017 | `pifagortrade` | [2454](https://t.me/pifagortrade/2454) | `BTC` long | `directional_thesis` | `false_positive` | Text says the next 4-6 months are not bullish; V0 long direction is wrong. |
| inc-018 | `pifagortrade` | [2454](https://t.me/pifagortrade/2454) | `ETH` long | `directional_thesis` | `false_positive` | Same bearish/uncertain market thesis should not become ETH long. |
| inc-019 | `pifagortrade` | [2498](https://t.me/pifagortrade/2498) | `BTC` long | `directional_thesis` | `needs_context` | Uses custom safety/trap-line terms that require level-aware parsing. |
| inc-020 | `pifagortrade` | [2512](https://t.me/pifagortrade/2512) | `BTC` long | `position_disclosure_or_management` | `needs_context` | Position-management fragment links to a prior post and should not stand alone. |

## Excluded Public-Probe Row Review

| review_id | channel | source | probe category | assets | status | reason |
|---|---|---|---|---|---|---|
| exc-001 | `bablos79` | [10257](https://t.me/bablos79/10257) | `explicit_setup_candidate` | `SMLT` | `needs_context` | Should become a setup candidate only after entry/stop/target parser exists. |
| exc-002 | `bablos79` | [10335](https://t.me/bablos79/10335) | `explicit_setup_candidate` | `SBER` | `needs_context` | Conditional short requires entry-condition handling. |
| exc-003 | `bablos79` | [9972](https://t.me/bablos79/9972) | `directional_bias_candidate` | - | `accepted` | Broad macro commentary without asset/proxy. |
| exc-004 | `bablos79` | [9976](https://t.me/bablos79/9976) | `directional_bias_candidate` | `SI` | `needs_context` | Futures proxy not approved in V1 matrix. |
| exc-005 | `bablos79` | [10005](https://t.me/bablos79/10005) | `market_context_candidate` | - | `accepted` | Gold/news context without approved commodity proxy. |
| exc-006 | `bablos79` | [10011](https://t.me/bablos79/10011) | `market_context_candidate` | - | `accepted` | Political/economic context, not asset-level claim. |
| exc-007 | `bablos79` | [9969](https://t.me/bablos79/9969) | `not_market_candidate` | - | `accepted` | Not market evidence. |
| exc-008 | `nemphiscrypts` | [3380](https://t.me/nemphiscrypts/3380) | `explicit_setup_candidate` | `BRIAN` | `accepted` | Self-history/marketing long read; `BRIAN` is not an approved asset. |
| exc-009 | `nemphiscrypts` | [3384](https://t.me/nemphiscrypts/3384) | `explicit_setup_candidate` | `BNB` | `accepted` | Q&A/vault discussion, not a BNB trade call. |
| exc-010 | `nemphiscrypts` | [3344](https://t.me/nemphiscrypts/3344) | `directional_bias_candidate` | - | `false_negative` | Text contains direct BTC long-zone wording and should be included through alias detection. |
| exc-011 | `nemphiscrypts` | [3352](https://t.me/nemphiscrypts/3352) | `directional_bias_candidate` | - | `false_negative` | "BTC at 75k" panic/long context should be reviewed by BTC alias rules. |
| exc-012 | `nemphiscrypts` | [3345](https://t.me/nemphiscrypts/3345) | `market_context_candidate` | - | `needs_context` | ETH price prompt may be thesis/context; requires explicit side extraction. |
| exc-013 | `nemphiscrypts` | [3346](https://t.me/nemphiscrypts/3346) | `market_context_candidate` | - | `accepted` | Course/engagement text, not a scored claim. |
| exc-014 | `nemphiscrypts` | [3348](https://t.me/nemphiscrypts/3348) | `not_market_candidate` | - | `accepted` | Channel/community logistics. |
| exc-015 | `pifagortrade` | [2510](https://t.me/pifagortrade/2510) | `explicit_setup_candidate` | `BTCUSD` | `false_negative` | Above/below trap-line condition should become a structured BTC setup. |
| exc-016 | `pifagortrade` | [2578](https://t.me/pifagortrade/2578) | `explicit_setup_candidate` | `BTC`, `SIGN-UP`, `USDT` | `false_negative` | BTC position/closure wording should be extracted; `SIGN-UP` must be blocked as an asset. |
| exc-017 | `pifagortrade` | [2296](https://t.me/pifagortrade/2296) | `directional_bias_candidate` | - | `needs_context` | Custom line terminology needs parser support before scoring. |
| exc-018 | `pifagortrade` | [2298](https://t.me/pifagortrade/2298) | `directional_bias_candidate` | - | `false_negative` | Repeated safety/trap-line condition should become level-aware setup evidence. |
| exc-019 | `pifagortrade` | [2285](https://t.me/pifagortrade/2285) | `market_context_candidate` | - | `accepted` | General crypto-year forecast context, not a specific asset-level call. |
| exc-020 | `pifagortrade` | [2311](https://t.me/pifagortrade/2311) | `market_context_candidate` | - | `accepted` | Real-estate/general investing context, not approved market proxy. |
| exc-021 | `pifagortrade` | [2341](https://t.me/pifagortrade/2341) | `not_market_candidate` | - | `accepted` | Historical/social reference, not market evidence. |

## Review Totals

| Sample group | Rows | accepted | false_positive | false_negative | needs_context |
|---|---:|---:|---:|---:|---:|
| V0 included claims | 20 | 5 | 6 | 0 | 9 |
| Excluded public-probe rows | 21 | 10 | 0 | 5 | 6 |

## Calibration Implications

- V0 long/short direction extraction can invert negative wording; V1 must
  recognize "no buys", "not bullish", and similar negations.
- Trade-management rows such as closed positions must not become fresh calls
  unless linked to the original setup.
- Conditional level language belongs to `trade_setup`, not immediate
  fixed-horizon `directional_thesis`.
- Alias extraction must improve for BTC/Bitcoin/BTCUSD and ETH/Ether wording.
- Noise tokens such as `SIGN-UP`, person names, and marketing terms must be
  blocked as assets.
- Futures/FX/commodity/index proxies remain exclusions until provider/proxy
  expansion approves them.
