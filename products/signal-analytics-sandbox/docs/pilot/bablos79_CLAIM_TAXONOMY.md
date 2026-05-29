# Claim Taxonomy - bablos79

Date: 2026-05-15
Status: active_for_phase24_draft_ledger
Scope: `bablos79` expanded public corpus and reviewed/internal media evidence

This taxonomy defines claim categories for the `bablos79` deep retrospective.
It prevents the claim ledger from forcing every post into a trade-signal frame
and separates useful author insight from deterministic performance evidence.

## Category Summary

| category | market idea mapping | definition | deterministic-outcome default |
|---|---|---|---|
| `macro_context` | `market_regime` | Broad macro, geopolitical, liquidity, volatility, or market-regime commentary that may explain the author's worldview. | not ready unless mapped to a benchmark/proxy, direction, timestamp, and horizon |
| `event_risk` | `catalyst_reaction` or `risk_warning` | Claim about a concrete event, catalyst, attack, policy, sanctions, earnings, ETF, macro print, or other risk expected to affect a market. | conditional on event, proxy/asset, direction, and outcome window |
| `directional_bias` | `directional_thesis` | Bullish, bearish, downside, upside, risk-on/risk-off, or avoid/accumulate view without full entry/stop/target fields. | conditional on asset/proxy, direction, timestamp, and horizon |
| `explicit_trade_setup` | `trade_setup` | Actionable setup with enough fields to evaluate trade-like behavior after review. | ready only when all trade fields and market data are present |
| `level_timing_call` | `directional_thesis` or `trade_setup` | A call tied to a price level, support/resistance, timing window, bounce/drop sequence, or "before/after event" condition. | conditional on level/timing evidence, asset/proxy, direction, and horizon |
| `watchlist` | `watchlist` | Asset/topic to monitor, conditional setup, "wait for signs", or observation queue. | not strict win/loss; may support later context links |
| `non_market_commentary` | `non_market` | Promotion, stream notice, joke, operational note, education, unrelated politics without market linkage, or insufficient market content. | not applicable |
| `unsupported_media_claim` | excluded / queued | Claim that exists only in unaccepted transcript/OCR/image/chart/video evidence, unlinked media, or media with unresolved source linkage. | not ready; internal candidate only until source-linked and reviewed |

## Category Rules

### `macro_context`

Use for broad claims about geopolitics, liquidity, market regime, central banks,
war risk, sanctions, broad exchange tone, or cross-market pressure.

Required fields for deterministic outcome readiness:

- source timestamp;
- benchmark or proxy ID;
- direction or measurable condition;
- horizon or event window;
- evidence span;
- approved review state;
- deterministic outcome method.

Broad macro context can be useful author insight even when it is not
performance evidence. It may appear in internal author-profile notes and later
report limitations, but it must not be counted as a win/loss unless the proxy
and method are explicit.

### `event_risk`

Use for event-driven market claims: attacks, provocations, elections, sanctions,
ETF decisions, earnings, macro prints, exchange incidents, or policy changes.

Required fields for deterministic outcome readiness:

- event description and expected market effect;
- source timestamp;
- affected asset, sector, exchange, index, or proxy;
- direction;
- horizon tied to the event window;
- evidence span;
- approved review state;
- deterministic market-data snapshot and outcome method.

If the event is described but the affected market or horizon is ambiguous, mark
the claim as useful context or unresolved, not deterministic performance
evidence.

### `directional_bias`

Use for broad bullish/bearish statements without a full trade setup. Examples:
"negative continues", "market will likely fall", "bounce possible", "upside
still open".

Required fields for deterministic outcome readiness:

- source timestamp;
- asset/proxy ID;
- direction;
- horizon;
- evidence span;
- approved review state;
- outcome method and snapshot reference.

Directional bias can be evaluated as forward movement against a proxy only
after the proxy, direction, and horizon are defensible.

### `explicit_trade_setup`

Use only when the source provides a trade-like structure.

Required fields for deterministic outcome readiness:

- source timestamp;
- asset ID;
- direction;
- entry or deterministic entry rule;
- stop, invalidation, or risk rule;
- target, exit rule, or explicit timeout/horizon;
- evidence spans for the required fields;
- approved review state;
- deterministic market-data snapshot;
- strict trade outcome method.

If any required trade field is missing, downgrade to `directional_bias`,
`level_timing_call`, or `watchlist` depending on the evidence.

### `level_timing_call`

Use when the claim depends on a price level, range, bounce/drop sequence,
support/resistance, or timing phrase such as "before May holidays" or "after
the attacks".

Required fields for deterministic outcome readiness:

- source timestamp;
- asset/proxy ID;
- level, range, timing condition, or event window;
- direction or measurable condition;
- horizon;
- evidence span;
- approved review state;
- deterministic outcome method.

Level/timing calls should preserve the stated condition. Do not rewrite them
as full trade setups unless entry, risk, and target fields are actually present.

### `watchlist`

Use for assets/topics the author says to monitor, wait on, or revisit.

Required fields for deterministic outcome readiness:

- none by default for win/loss metrics.

Watchlists can support later qualitative analysis, follow-up linking, and
coverage counts. They may track subsequent movement as context only if Phase 24
defines a separate non-win/loss method.

### `non_market_commentary`

Use for content that does not contain an auditable market idea.

Required fields for deterministic outcome readiness:

- not applicable.

These rows must remain visible in corpus coverage so the report does not
cherry-pick only market-looking posts.

### `unsupported_media_claim`

Use when a possible claim depends on media that is not source-linked, reviewed,
or accepted under the Phase 23 policy.

Required fields for deterministic outcome readiness:

- source-linked public media artifact;
- transcript/OCR/chart review status sufficient for the use case;
- human/operator acceptance for external claims;
- all normal category-specific outcome fields.

Current Phase 23 media state:

- two transcript refs are `llm_reviewed_internal`;
- zero transcript refs are human/operator accepted;
- zero reviewed image/OCR refs exist;
- zero media-backed refs are `external_claim_ready`.

Unsupported media claims may appear as internal candidates or blockers, but not
as final/customer-facing claims.

## Deterministic Outcome Ready Fields

A claim is deterministic-outcome-ready only when all required fields below are
present and review-accepted for the intended use.

| field | required rule |
|---|---|
| `claim_id` | Stable deterministic ID from source document, span, category, and version. |
| `source_id` / `capture_id` / `source_document_id` | Required for every claim. |
| `source_timestamp_utc` | Required; unresolved timestamps block deterministic horizons. |
| `evidence_url` | Required public evidence URL or recorded source ref. |
| `text_sha256` | Required for text claims; media claims also require media checksum. |
| `evidence_span` | Required for every market claim; exact source text or accepted transcript/OCR span. |
| `category` | One taxonomy category from this document. |
| `review_state` | Must be approved/review-accepted for deterministic outcomes. Draft or LLM-only rows are not enough. |
| `asset_or_proxy_id` | Required for measurable market outcomes unless category is non-applicable. |
| `direction_or_condition` | Required for directional or conditional outcome methods. |
| `horizon_or_event_window` | Required; vague horizons must be normalized or marked unresolved. |
| `outcome_method` | Required deterministic method: strict trade, forward return, benchmark-relative return, event-window move, or not applicable. |
| `market_data_snapshot_ref` | Required before computing outcome metrics. |
| `media_acceptance_status` | Required when media evidence supports the claim. External use requires `human_operator_accepted` or `external_claim_ready`. |

If any required field is missing, the claim must be marked `non_measurable`,
`unresolved`, `ambiguous`, `unsupported_media_claim`, or `not_applicable`
instead of being excluded from the ledger.

## Review And Report Boundary

- Draft extraction, parser output, LLM review, RAG context, OCR, and transcripts
  are not final truth.
- Broad claims may be valuable author insight even when non-measurable.
- Non-market, ambiguous, weak, blocked, unsupported, and counterexample rows
  must remain in coverage counts.
- Customer-facing claims require human/operator accepted evidence plus
  deterministic outcome support where performance is discussed.
- No claim category permits investment advice, future-profit language,
  marketplace ranking, leaderboard framing, or "best channel" conclusions.

## Phase 24 Ledger Guidance

The claim ledger should include each reviewable claim with its category,
measurability status, evidence refs, media refs when used, review state, and
reason for inclusion or exclusion from deterministic outcomes. If fewer than
30-50 reviewable claims exist, the ledger must record an insufficient-corpus
decision with reasons instead of stretching weak evidence into performance
claims.
