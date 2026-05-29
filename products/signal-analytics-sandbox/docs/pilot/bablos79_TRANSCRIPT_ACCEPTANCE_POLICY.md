# Transcript Acceptance Policy - bablos79

Date: 2026-05-15
Status: active_internal_policy
Scope: `bablos79` Phase 21/23 voice and managed Whisper transcript artifacts

This policy defines how managed Whisper transcript artifacts and LLM-reviewed
transcript refs may be used in internal joins, analyst drafts, and external
media-backed claims. It reclassifies existing transcript artifacts by review
status only; it does not change transcript text, extracted claims, source media
checksums, or evidence content.

## Status Definitions

| status | owner | definition | allowed use | blocked use |
|---|---|---|---|---|
| `draft_pending_review` | transcription provider / deterministic pipeline | A provider transcript exists, but no LLM, human, or operator review has accepted it for evidence use. | Storage, checksum tracking, review queue input, provider-quality debugging. | Internal source joins, customer-facing report claims, deterministic outcome ledgers, author scoring. |
| `llm_reviewed_internal` | LLM review adapter | An LLM reviewer marked the transcript coherent, source-bound, and usable for internal analysis under a recorded prompt/model/review artifact. | Internal source joins, internal analyst notes, internal draft reports, claim-candidate discovery with explicit LLM-review labeling. | External delivery, customer-facing media-backed claims, approved signal records, deterministic outcome truth, author capability scoring. |
| `human_operator_accepted` | human/operator reviewer | A human or explicitly authorized operator accepted the transcript or reviewed media evidence as faithful enough for the stated claim boundary. | External-delivery preparation, customer-facing report drafting, internal and external source joins, claim support within the accepted boundary. | Deterministic outcome claims unless the claim also has measurable asset, horizon, market proxy, and outcome-method support. |
| `external_claim_ready` | report gate | Claim-level status confirming the transcript is human/operator accepted, source-linked, checksum-tracked, safely worded, non-advice, and compatible with the external report boundary. | External report inclusion for the specific accepted claim. | Any broader claim than the accepted span, unsupported outcome metrics, investment advice, leaderboard/ranking language. |
| `rejected_unusable` | reviewer | Transcript or audio evidence is too ambiguous, unsupported, unrelated, or unsafe to use. | Gap/register note and exclusion rationale. | Internal source joins, external claims, outcome ledgers. |

## External Delivery Rule

LLM-reviewed transcript refs can support internal source joins when they are
recorded as `llm_reviewed_internal` and cite their review artifact. External
delivery requires `human_operator_accepted` status before any media-backed claim
can appear in customer-facing material, unless an explicit waiver is recorded in
the same report gate and names the exact claim, reviewer, rationale, and risk
owner.

No waiver exists for the current `bablos79` transcript refs.

## Reclassified Phase 21 Transcript Refs

| media_id | transcript_id | provider_status | llm_review_decision | policy_status | internal_source_join | external_delivery | outcome_ready | required_next_action |
|---|---|---|---|---|---|---|---|---|
| `public_voice_bablos79_10476` | `transcript_57b6461001b54e10` | `draft_pending_review` | `usable_internal` | `llm_reviewed_internal` | yes | no | no | Human/operator acceptance or explicit waiver before external use. |
| `public_voice_bablos79_10478` | `transcript_92ad5bf2e9088056` | `draft_pending_review` | `usable_internal` | `llm_reviewed_internal` | yes | no | no | Human/operator acceptance or explicit waiver before external use. |

## Claim Boundary

- Internal source joins may cite the LLM review artifact and the draft
  transcript artifact together.
- External report sections must exclude these refs until they reach
  `human_operator_accepted` or a claim-specific waiver is recorded.
- Broad market commentary remains non-deterministic unless later mapped to an
  explicit asset/proxy, timestamp, horizon, and outcome method.
- Transcript acceptance does not approve investment advice, signal records,
  author rankings, or future-profit claims.

## Content Preservation

This policy is a classification layer. Existing Phase 21 transcript files,
LLM-review rows, media-backed claim text, checksums, and source refs remain
unchanged.
