# Channel Dashboard Score Schema

Date: 2026-05-22
Status: `phase36_schema_v1_internal`

The dashboard schema is a compact, confidence-aware view of channel impact. It
is not a leaderboard and does not produce investment advice.

## Channel Score Record

| Field | Type | Meaning |
| --- | --- | --- |
| `source_id` | string | Channel identifier. |
| `public_text_rows` | integer | Public text rows captured for the evaluated scope. |
| `measurable_claims` | integer | Claims with deterministic market outcome support. |
| `sample_size_label` | enum | high, medium, low, or blocked. |
| `signal_performance` | object | Hit rate, avg return, MFE/MAE, benchmark-relative fields where available. |
| `trend_sense` | object | Regime/trend view evidence and confidence. |
| `insight_depth` | object | Causal thesis evidence and confidence. |
| `methodology_clarity` | object | Process/playbook evidence and confidence. |
| `risk_discipline` | object | Invalidation, stops, sizing, loss handling, stale-signal handling. |
| `practical_usefulness` | object | Clarity, follow-up, actionability, noise ratio. |
| `creativity` | object | Differentiated, evidence-backed framing. |
| `evidence_confidence` | object | Source, review, media, provider, and false-negative confidence. |
| `external_gate` | enum | external_ready, internal_only, rejected, blocked. |

## Required Confidence Fields

Each dimension object must include:

- `score_label`: high, medium, low, blocked, or not_enough_data;
- `evidence_count`;
- `positive_examples_count`;
- `counterexamples_count`;
- `main_limitations`;
- `customer_facing_allowed`.

## Forbidden Dashboard Language

The schema forbids:

- `best_channel`;
- `guaranteed_profit`;
- `future_profit`;
- `investment_advice`;
- `follow_this_author`;
- unsupported ranking or marketplace framing.

## Public Vs Internal

Internal dashboard prototype may show low-confidence rows with blockers. A
public/free dashboard may only show fields approved by the latest external gate.
Paid report details stay behind `PAID_CHANNEL_REPORT_BOUNDARY.md`.
