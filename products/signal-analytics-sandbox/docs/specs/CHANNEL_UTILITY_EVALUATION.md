# Channel Utility Evaluation Contract

Version: 0.1
Date: 2026-05-17
Status: specification for multimodal channel usefulness scoring

## Purpose

The product evaluates whether a public market channel is useful by validating
the channel's own historical market assertions against future market behavior.
It must not rank authors from vibes, follower count, style, or cherry-picked
examples.

The unit of work is a normalized, timestamped, evidence-backed market claim
extracted from public text, audio transcript, or image/OCR evidence.

## Core Rule

Any market claim, forecast, position disclosure, trade setup, risk warning, or
trade-management update can affect channel utility only after all of these are
true:

| Requirement | Rule |
|---|---|
| Public evidence | The source text, transcript, or OCR artifact is linked to a public source document and checksum/provenance is preserved. |
| Normalized claim | The claim is converted into a `MarketIdea`/claim-ledger row with asset/proxy, direction, timestamp, horizon, and outcome method where applicable. |
| Approval gate | Ambiguous or machine-extracted fields remain `queued_for_review` until an operator or documented confidence gate approves them. |
| Open market validation | Historical prices are fetched through an approved open/public provider or operator-provided public export only for the required asset/time window. |
| Deterministic metrics | Hit rate, return %, MFE/MAE, strict trade outcome, and benchmark-relative metrics are computed by deterministic code. |
| No overclaim | Non-evaluable claims remain visible in coverage/quality metrics but are excluded from performance metrics. |

## Storage Posture

The system should avoid maintaining a huge local market database.

Instead:

1. Store normalized source evidence, claim rows, approval decisions, proxy
   mappings, and compact market-data snapshots used for computed outcomes.
2. Fetch OHLCV windows on demand from approved open/public APIs after proxy and
   horizon approval.
3. Cache only immutable, provenance-rich snapshots needed to reproduce a
   computed metric.
4. Do not bulk-store unrelated market history.
5. Treat provider failures, missing coverage, delistings, and symbol ambiguity
   as explicit exclusion statuses rather than guessed outcomes.

Current provider posture:

| Provider path | Intended use | Boundary |
|---|---|---|
| `exchange-public/*` via ccxt-style public OHLCV | Crypto symbols such as BTC/USDT, ETH/USDT, SOL/USDT. | Public exchange data only; snapshot must record provider, exchange, timeframe, range, checksum. |
| `yfinance-dev` | Prototype/dev validation for listed assets where allowed. | Must be explicitly enabled and treated as prototype unless promoted by a later provider decision. |
| `operator_file` | Public/exported fixtures supplied by operator. | Must preserve source/provenance and checksum; useful when no stable public API is available. |

## Multimodal Extraction Pipeline

All modalities converge into the same normalized claim surface.

| Modality | Extraction path | Truth boundary |
|---|---|---|
| Public text | Telegram/public page capture to `SourceDocument.text`. | Text is source evidence; parser/LLM labels are drafts. |
| Audio | Public media artifact -> transcript draft -> source join. | Transcript is internal/draft until reviewed or accepted under transcript policy. |
| Image/chart | Public media artifact -> OCR/chart text draft -> source join. | OCR/chart interpretation is draft until reviewed; chart claims require source linkage. |

Pipeline:

1. Capture public source document with timestamp, URL, text hash, and optional
   media refs.
2. Transcribe/OCR media into draft artifacts with media checksum linkage.
3. Join text/transcript/OCR refs into `SourceDocument` without mutating source
   text or approved ledgers.
4. Extract candidate `MarketIdea`/claim rows with evidence spans.
5. Normalize fields: asset/proxy, direction, entry/stop/target when present,
   horizon, benchmark, timestamp basis, and claim type.
6. Queue ambiguous rows for operator review.
7. Fetch only the approved market-data window from open/public providers.
8. Compute deterministic outcomes and aggregate channel utility metrics.

## Claim Types And Evaluation

| Claim type | Example | Evaluation |
|---|---|---|
| `trade_setup` | long BTC from 90k, stop 86k, target 105k | Strict entry/stop/target/timeout plus return %, MFE, MAE, RR. |
| `directional_thesis` | BTC should go higher from here | Fixed-horizon direction hit, return %, MFE, MAE. |
| `position_disclosure` | holding longs in ETH/SOL, short market | Position/proxy basket return over approved horizon or next disclosure window. |
| `trade_management` | moved stop, took partial profit | Links to original approved setup; otherwise excluded as fragment. |
| `market_regime` | risk-on, altseason, liquidity improving | Benchmark/proxy-relative outcome only after benchmark and horizon approval. |
| `risk_warning` | do not long here, breakdown risk | Avoided-loss or directional warning metric only after explicit rule approval. |
| `watchlist/context` | watching SUI, waiting for setup | Coverage/context only unless a later explicit trigger is linked. |

## Channel Utility Metrics

A useful channel is not just profitable in a cherry-picked sample. The report
must separate coverage, clarity, and outcomes.

| Metric group | What it answers |
|---|---|
| Coverage | How many posts are market-related, measurable, approved, non-evaluable, or rejected? |
| Clarity | How often does the author give asset, direction, horizon, levels, and risk? |
| Directional skill | Hit rate and forward returns for approved directional claims. |
| Trade quality | Strict setup outcomes, average return %, MFE/MAE, RR, stop/target behavior. |
| Risk usefulness | Whether warnings avoided drawdowns or reduced bad exposure. |
| Consistency | Performance by claim type, asset class, horizon, and time period. |
| Honesty of evidence | Counterexamples, misses, ambiguous rows, deleted/missing evidence, and non-market content remain visible. |

## Structured Claim Extractor V1

`SAS-V1-003` adds a deterministic text extractor that converts
`SourceDocument` inputs into structured claim rows. The extractor is rule-only:
it does not call LLMs, market APIs, or network resources.

Each structured row records:

- claim type: `trade_setup`, `directional_thesis`, `position_disclosure`,
  `trade_management`, `risk_warning`, or `context_only`;
- asset/proxy mentions and direction;
- entry, stop, target, RR, and horizon fields only when evidence spans or
  deterministic rules support them;
- evidence spans for asset, direction, levels, RR, and horizon;
- ambiguity flags and blockers such as `missing_entry`,
  `requires_original_setup_link`, or `blocked_asset_token:*`.

Missing structured fields remain explicit nulls with blockers. They are not
inferred from market data or surrounding unstated assumptions.

## Level-Aware Outcome Engine V1

`SAS-V1-004` evaluates structured claims over immutable OHLCV snapshots.

- `trade_setup` rows require entry, stop, target, and direction. Outcomes are
  entry not filled, stopped, target hit, timeout, insufficient data, or missing
  required fields.
- `directional_thesis` rows continue to use fixed-horizon deterministic returns
  without requiring entry, stop, or target.
- `trade_management` rows are excluded unless linked to an approved original
  setup.
- Outcome rows preserve claim id, snapshot id, canonical asset id, metric
  version, timestamps, return %, MFE, MAE, RR, and exclusion reason.

## Report Boundary

The report may say:

- how many claims were reviewed;
- how many were measurable;
- how many were confirmed, contradicted, unresolved, or excluded;
- what conditional return and risk metrics were produced from approved rows;
- where evidence is too weak to judge.

The report must not say:

- that a channel will make money in the future;
- that a channel is universally good or bad based on unapproved examples;
- that a machine-extracted transcript/OCR/chart claim is final truth;
- that missing market data implies a win or loss.

## Next Implementation Target

The next implementation step is an operator approval matrix for the three pilot
channels:

1. evaluator type per channel;
2. allowed claim types;
3. asset/proxy mapping rules;
4. approved open/public market-data provider per asset class;
5. horizon defaults and strict trade rules;
6. exclusion statuses for ambiguous or unsupported rows.
