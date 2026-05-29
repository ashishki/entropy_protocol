# Channel Impact Claim Taxonomy

Date: 2026-05-22
Status: `phase36_taxonomy_v1`

This taxonomy normalizes channel statements for impact scoring. It separates
PnL-testable market calls from non-PnL evidence such as trend sense, insight
depth, methodology, risk management, practical usefulness, creativity, and
evidence confidence.

## Core Claim Types

| Claim type | Definition | Default scoring lane |
| --- | --- | --- |
| `explicit_trade_setup` | Entry/trigger plus direction and at least one risk, target, invalidation, or exit condition. | signal performance |
| `trend_regime_view` | Market regime, risk-on/risk-off, trend continuation, reversal, liquidity, volatility, or sector rotation view. | trend sense |
| `macro_thesis` | Causal market worldview tied to macro, geopolitics, policy, flows, or cross-market relationships. | insight depth |
| `risk_process_statement` | Stop, invalidation, sizing, loss control, stale-signal handling, or process discipline. | risk management |
| `methodology_statement` | Repeatable analytical method, indicator use, setup selection, follow-up routine, or playbook logic. | methodology |
| `watchlist` | Asset/topic to monitor, conditional setup, or wait-for-confirmation statement. | practical usefulness |
| `creative_synthesis` | Differentiated but checkable synthesis, scenario map, unusual proxy, or original framing. | creativity |
| `non_market_commentary` | Operational note, promotion, joke, unrelated politics, or insufficient market content. | coverage only |
| `unsupported_media_claim` | Claim depends on unlinked or unaccepted audio/image/chart/OCR/transcript evidence. | blocked/internal only |

## Required Review Fields

Every normalized claim needs:

- `claim_id`
- `source_id`
- `source_url`
- `source_timestamp_utc`
- `source_document_id`
- `evidence_span`
- `claim_type`
- `impact_dimensions`
- `author_statement_truth_status`
- `interpretation_truth_status`
- `market_outcome_truth_status`
- `product_conclusion_status`
- `review_status`
- `evidence_confidence`
- `customer_facing_allowed`
- `blocker_reason`

## Non-PnL Evidence Fields

Non-PnL claims cannot become win/loss rows unless deterministic market mapping
is added later. They still need reviewable evidence:

| Field | Purpose |
| --- | --- |
| `dimension_score_candidate` | Which dimension the row can support. |
| `evidence_quality` | source-linked, transcript accepted, OCR accepted, text-only, or blocked. |
| `confidence_label` | high, medium, low, or blocked. |
| `reviewer_reason` | Why the row supports or fails the dimension. |
| `counterexample_link` | Optional contradiction, stale view, or invalidation. |
| `deterministic_mapping_status` | not_applicable, missing_proxy, missing_horizon, ready, blocked. |

## Win/Loss Boundary

Only `explicit_trade_setup` and selected `trend_regime_view` rows may enter
win/loss or return metrics, and only after asset/proxy, direction, timestamp,
horizon, outcome method, and market-data snapshot are approved.

All other categories are scored as qualitative or confidence-weighted evidence.
They can improve a deep report, but they must not be silently converted into
profit claims.

## Blocked Uses

- no investment advice;
- no future-profit language;
- no universal best-channel ranking;
- no private/paywalled/login-walled evidence;
- no unaccepted media claims;
- no provider gap counted as a loss.
