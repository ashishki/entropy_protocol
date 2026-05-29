# Three-Channel Transcript Human Review Workflow

Date: 2026-05-19
Status: internal_workflow_pending_operator_decisions

## Purpose

This workflow defines how transcript refs can become accepted or rejected by a
human/operator reviewer. It does not accept any current transcript by itself and
does not approve external delivery.

## Required Decision Fields

Every transcript decision must preserve:

- `transcript_ref`
- `transcript_id`
- `media_id`
- `source_ref`
- `source_media_sha256`
- `transcript_sha256`
- `decision_status`: one of `accepted`, `rejected`, `needs_context`,
  `pending_human_review`
- `reviewer_id`
- `reviewed_at_utc`
- `reason`
- `accepted_scope`
- `external_claim_ready`

Rules:

- `accepted` requires a non-`pending` `reviewer_id`, `reviewed_at_utc`, and
  reason explaining the accepted evidence boundary.
- `rejected` requires a non-`pending` `reviewer_id`, `reviewed_at_utc`, and
  reason explaining why the transcript cannot support evidence.
- `needs_context` requires a reason and the missing source/media link.
- `pending_human_review` cannot enter customer-facing metrics or report claims.
- `external_claim_ready` remains `false` until a separate external-ready gate
  approves the exact media-backed claim.

## Current Review Queue

| transcript_ref | transcript_id | media_id | source_ref | source_media_sha256 | transcript_sha256 | decision_status | reviewer_id | reason | accepted_scope | external_claim_ready |
|---|---|---|---|---|---|---|---|---|---|---|
| `docs/pilot/transcripts/transcript_57b6461001b54e10.json` | `transcript_57b6461001b54e10` | `public_voice_bablos79_10476` | `https://t.me/bablos79/10476` | `dc35f04c417d644b603c9336d96108d485682e467e88e1e476500b1add1e115c` | `4509a917e93f875642c246421f714c9011d92c3d4e44e0e0bcd27419ca1bb103` | `pending_human_review` | `pending` | human/operator has not accepted or rejected this transcript | none yet | `false` |
| `docs/pilot/transcripts/transcript_92ad5bf2e9088056.json` | `transcript_92ad5bf2e9088056` | `public_voice_bablos79_10478` | `https://t.me/bablos79/10478` | `87ae688d3e55e4ab0eed95c2e4ec3d6ec3aa8a8022acc37a70703b255d6e8b00` | `28d9d9744aa4490a21b6699e6f7d9c7509b56b7fc2708d2533ecca77d07f5561` | `pending_human_review` | `pending` | human/operator has not accepted or rejected this transcript | none yet | `false` |

## Decision Recording Template

Use this template when a reviewer makes a decision:

| transcript_ref | decision_status | reviewer_id | reviewed_at_utc | reason | accepted_scope | external_claim_ready |
|---|---|---|---|---|---|---|
| `<transcript json path>` | `accepted` or `rejected` | `<human/operator id>` | `<ISO-8601 UTC>` | `<why this transcript is accepted/rejected>` | `<exact claim/span boundary or none>` | `false` |

## Accepted Transcript Use

An `accepted` transcript can support:

- internal source joins;
- claim-candidate extraction with media provenance;
- external report drafting only inside the accepted span and only after the
  external-ready gate approves that claim.

It cannot by itself approve deterministic market outcomes, author scores,
investment advice, future-profit claims, or channel ordering.

## Rejected Transcript Use

A `rejected` transcript can support:

- exclusion notes;
- media quality diagnostics;
- follow-up acquisition requests.

It cannot support source joins, claim extraction, metrics, or report claims.

## Current Decision

Current human/operator accepted transcript refs: 0.

Current rejected transcript refs: 0.

Current pending transcript refs: 2.

No transcript-backed customer-facing claim is eligible.
