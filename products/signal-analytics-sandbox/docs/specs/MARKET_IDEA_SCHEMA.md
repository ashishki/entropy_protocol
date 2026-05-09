# MarketIdea Schema And Metrics Contract

Version: 0.1
Date: 2026-05-09
Status: specification for `SAS-MI-002`

## Purpose

`MarketIdea` generalizes the existing strict `SignalRecord` model for Author
Market Intelligence. It represents public author commentary as reviewable ideas
without overstating weak evidence as a trade signal.

The schema separates:

- explicit trade setups that may become evaluable records after human approval;
- softer market ideas that may support author-behavior analysis;
- non-market or unsupported content that remains visible but excluded from
  performance metrics.

This specification is a contract for future implementation. It does not add
product code, embeddings, market-data expansion, approved ledger writes, or
batch-agent behavior.

## Deterministic Truth Boundary

`MarketIdea` drafts may be produced by manual work, deterministic parsers, RAG
context, or gated LLM assistance. Draft producers do not own final truth.

Only these sources may own deterministic outputs:

| Output | Source of truth |
|--------|-----------------|
| Approved idea state | Human reviewer or later documented confidence gate. |
| Prices and market data | Deterministic market-data snapshots. |
| Returns and horizon metrics | Deterministic metric code over immutable snapshots. |
| Customer-facing claims | Human-approved report text backed by source evidence and deterministic metrics. |
| Context snippets | Cited source-corpus documents; context is not truth by itself. |

RAG output is context-only and cannot produce final prices, returns, approved
records, or outcome metrics.

## Core Enum Values

### idea_type

| Value | Meaning | Evaluable by default? |
|-------|---------|-----------------------|
| `trade_setup` | Explicit actionable setup with asset, direction, entry/invalidation/target or deterministic rules. | yes, after approval and asset/price resolution |
| `directional_thesis` | Softer bullish/bearish view without full trade fields. | yes for horizon movement only after approval |
| `market_regime` | Broad market state comment such as risk-on/risk-off, liquidity, volatility, trend, or macro tone. | yes only against declared benchmark/proxy metrics |
| `watchlist` | Asset/topic to watch, conditional setup, or "wait for signs" statement. | no win/loss; may track subsequent movement as context |
| `catalyst_reaction` | News, earnings, sanctions, ETF, macro, or event reaction tied to an asset/sector/market. | yes only if asset/proxy and timestamp are resolvable |
| `risk_warning` | Warning, invalidation, uncertainty, cancellation, or no-trade language. | no win/loss; may track avoided-risk context |
| `non_market` | Promotion, stream notice, joke, education, unrelated content, or insufficient market content. | no |

### direction

| Value | Meaning |
|-------|---------|
| `long` | Author expresses upside bias or buy/hold/add thesis. |
| `short` | Author expresses downside bias, sell/short/avoid thesis. |
| `flat` | Author expresses neutral/range/no-action view. |
| `mixed` | Multiple conflicting directions are present. |
| `unknown` | Direction cannot be defensibly inferred. |

### approval_state

| Value | Meaning | May affect customer-facing metrics? |
|-------|---------|-------------------------------------|
| `draft` | Machine/manual draft not yet reviewed. | no |
| `queued_for_review` | Needs human decision before use. | no |
| `approved` | Reviewer approved the idea for deterministic evaluation/report use. | yes, within metric contract |
| `rejected` | Reviewer rejected it as unsupported or out of scope. | no |
| `excluded` | Valid row but excluded from metrics by policy. | no |

### extraction_source

| Value | Meaning |
|-------|---------|
| `manual` | Human-created draft. |
| `rule` | Deterministic parser/rule output. |
| `llm_draft` | Gated LLM draft, never truth. |
| `rag_context` | Context-derived suggestion, never truth. |
| `imported` | Migration/import from prior artifact. |

### resolution_state

| Value | Meaning |
|-------|---------|
| `resolved` | Asset/proxy and timestamp are sufficient for deterministic evaluation. |
| `ambiguous` | Multiple plausible assets/proxies or meanings exist. |
| `unresolved` | Required asset/proxy/timestamp evidence is missing. |
| `not_applicable` | Idea type is not meant to resolve to market data. |

## Field Contract

### Required Fields

| Field | Type | Rule |
|-------|------|------|
| `idea_id` | string | Stable deterministic ID assigned by implementation; should be reproducible from source ID, capture ID, idea span, type, and version. |
| `source_id` | string | Source/channel ID, e.g. `bablos79`. |
| `capture_id` | string | Capture/source-document ID. |
| `evidence_url` | string | Public evidence URL or local evidence reference. |
| `text_sha256` | string | SHA-256 of the captured text or source-document text. |
| `source_timestamp_utc` | datetime | Public post timestamp when available; otherwise documented capture timestamp fallback. |
| `extracted_timestamp_utc` | datetime | Time the draft/record was extracted. |
| `idea_type` | enum | One of the `idea_type` values above. |
| `approval_state` | enum | One of the approval states above. |
| `extraction_source` | enum | One of the extraction sources above. |
| `evidence_spans` | list | At least one span for any non-`non_market` idea; see evidence-span rules. |
| `resolution_state` | enum | Asset/proxy resolution state. |
| `review_required` | bool | `true` for all draft, queued, LLM, RAG, ambiguous, high-impact, or customer-facing rows. |
| `metadata_version` | string | Schema/contract version, starting with `market_idea.v0.1`. |

### Optional Fields

| Field | Type | Draft allowed? | Rule |
|-------|------|----------------|------|
| `canonical_asset_id` | string | yes | Filled only after asset registry resolution; no guessing. |
| `asset_mentions` | list[string] | yes | Raw symbols/aliases observed in evidence spans. |
| `direction` | enum | yes | Defaults to `unknown` when unsupported. |
| `entry` | decimal/string rule | yes | Required for `trade_setup` evaluability; may be a deterministic rule reference. |
| `stop_or_invalidation` | decimal/string rule | yes | Required for `trade_setup` evaluability. |
| `target_or_horizon` | decimal/string rule | yes | Required for strict trade win/loss; softer idea types use horizon defaults. |
| `horizon_hint` | enum/list | yes | `intraday`, `1d`, `3d`, `7d`, `30d`, `unspecified`, or explicit timestamp. |
| `benchmark_id` | string | yes | Required for market-regime benchmark-relative metrics. |
| `confidence` | decimal | yes | Draft confidence from parser/LLM/RAG; cannot approve a row alone. |
| `ambiguity_flags` | list[string] | yes | Must exclude from strict win/loss until resolved. |
| `reviewer_id` | string | no | Required when `approval_state=approved` or `rejected`. |
| `review_notes` | string | no | Human-readable decision notes. |
| `linked_idea_ids` | list[string] | yes | Follow-up, close/reduce, thesis update, or cancellation links. |
| `rag_context_refs` | list[string] | yes | Source document IDs returned by retrieval; context-only. |

## Evidence-Span Rules

Each evidence span must contain:

| Field | Rule |
|-------|------|
| `span_id` | Stable ID within the idea record. |
| `source_document_id` | Capture/source-corpus document ID. |
| `start_char` / `end_char` | Character offsets into captured/source text when available. |
| `excerpt` | Exact text excerpt from the captured/source text. |
| `supports` | One of `asset`, `direction`, `entry`, `stop_or_invalidation`, `target_or_horizon`, `idea_type`, `risk`, `catalyst`, `non_market`, `uncertainty`. |
| `support_strength` | `explicit`, `implied`, or `weak`. Weak support cannot approve fields by itself. |

Rules:

- Evidence excerpts must be copied from captured/source text, not rewritten.
- A field with only weak support must stay draft or queued for review.
- `trade_setup` approval requires evidence for asset, direction, entry,
  stop/invalidation, target/horizon, and timestamp.
- `directional_thesis` approval requires asset/proxy, direction, and timestamp.
- `market_regime` approval requires benchmark/proxy and timestamp.
- `watchlist`, `risk_warning`, and `non_market` rows can be approved as
  classification records but remain excluded from win/loss metrics.

## Draft-Only Fields

The following fields are draft assistance and must not be treated as truth:

- `confidence`
- `rag_context_refs`
- `extraction_source=llm_draft`
- `extraction_source=rag_context`
- parser/LLM/RAG-proposed `idea_type`
- parser/LLM/RAG-proposed `direction`
- parser/LLM/RAG-proposed `canonical_asset_id`
- generated summaries or rationales

Human review or a later explicitly documented confidence gate is required before
these fields can affect approved records or reports.

## Deterministic Metric Contract

### Horizons

Default post-publication horizons:

| Horizon | Meaning |
|---------|---------|
| `0_to_1d` | Close-to-close or first available market window through 1 calendar day. |
| `0_to_3d` | First available market window through 3 calendar days. |
| `0_to_7d` | First available market window through 7 calendar days. |
| `0_to_30d` | First available market window through 30 calendar days. |

Future implementation may add intraday windows only after the market-data store
records resolution, provider, range, and timestamp semantics for that window.

### Metric Outputs

| Metric | Applies to | Rule |
|--------|------------|------|
| `forward_return_pct` | approved resolved ideas with asset/proxy | Deterministic percentage move from first eligible post-publication price to horizon close. |
| `max_favorable_excursion_pct` | directional approved ideas | Best move in the idea's direction within the horizon. |
| `max_adverse_excursion_pct` | directional approved ideas | Worst move against the idea's direction within the horizon. |
| `benchmark_relative_return_pct` | ideas with benchmark/proxy | Idea asset return minus benchmark return for the same horizon. |
| `directional_hit` | `trade_setup`, `directional_thesis`, eligible `catalyst_reaction` | Deterministic label derived from direction and forward return sign after thresholds are specified. |
| `strict_trade_outcome` | `trade_setup` only | Existing target/stop/timeout semantics when entry, stop, and target are approved. |
| `coverage_status` | all ideas | `evaluated`, `excluded_ambiguous`, `excluded_no_price`, `excluded_not_applicable`, or `excluded_unapproved`. |

All metric code must:

- use immutable market-data snapshots;
- cite provider, range, as-of timestamp, and checksum;
- use Decimal-compatible rounding rules defined by implementation;
- exclude draft, rejected, unresolved, ambiguous, and non-applicable rows from
  performance aggregates;
- keep excluded rows visible in coverage/limitation counts.

## Review Queue Policy

Queue a row for human review when any of the following is true:

| Trigger | Examples |
|---------|----------|
| Ambiguous asset/proxy | ticker collision, unsupported market, asset-only hashtag without clear thesis. |
| Ambiguous direction | mixed long/short language, irony, third-party reference, unknown speaker. |
| Missing evaluability fields | missing entry, stop/invalidation, target/horizon, timestamp, or evidence. |
| High-impact claim | customer-facing performance claim, strong directional conclusion, named author quality judgment. |
| Unsupported generated field | parser/LLM/RAG proposed a field without direct evidence span support. |
| Close/reduce/management context | "closed", "moved stop", "partial take profit" without original setup link. |
| Low confidence | confidence below the task's documented threshold. |
| RAG/LLM assisted | any non-manual, non-deterministic suggestion that would affect report language. |
| Quality-control sample | deterministic sample of excluded/non-market rows. |

The Phase 10 `bablos79` review queue is the seed policy: include all
`needs_review` / `insufficient_fields`, low-confidence rows, asset-bearing
customer-facing candidates, close/reduce or uncertainty contexts, and a
deterministic non-signal sample.

## Examples

### Explicit Trade Setup

```json
{
  "idea_type": "trade_setup",
  "asset_mentions": ["MAGN"],
  "canonical_asset_id": "pending_asset_registry",
  "direction": "short",
  "entry": "current highs",
  "stop_or_invalidation": "pending_review",
  "target_or_horizon": "pending_review",
  "approval_state": "queued_for_review",
  "resolution_state": "ambiguous",
  "review_required": true
}
```

### Directional Thesis

```json
{
  "idea_type": "directional_thesis",
  "asset_mentions": ["VTBR"],
  "direction": "short",
  "horizon_hint": "unspecified",
  "approval_state": "queued_for_review",
  "resolution_state": "unresolved",
  "review_required": true
}
```

### Watchlist / No-Action Context

```json
{
  "idea_type": "watchlist",
  "asset_mentions": ["AMD"],
  "direction": "short",
  "approval_state": "queued_for_review",
  "resolution_state": "resolved",
  "ambiguity_flags": ["explicit_no_action"],
  "review_required": true
}
```

### Non-Market Content

```json
{
  "idea_type": "non_market",
  "asset_mentions": [],
  "direction": "unknown",
  "approval_state": "excluded",
  "resolution_state": "not_applicable",
  "review_required": false
}
```

## Compatibility With SignalRecord

`SignalRecord` remains the strict approved-trade ledger model. A `MarketIdea`
may be converted to a `SignalRecord` only when:

- `idea_type=trade_setup`;
- `approval_state=approved`;
- asset, direction, entry, stop/invalidation, target, timestamp, evidence URL,
  and text hash are all present;
- ambiguity flags are empty or explicitly resolved;
- reviewer ID is present.

Softer idea types must not be forced into `SignalRecord`; they use the
deterministic horizon metric contract instead.
