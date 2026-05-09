# Channel Profile Registry

Version: 0.1
Date: 2026-05-09
Status: specification for `SAS-MI-007`

## Purpose

Channel profiles store source-specific lexicons, extraction hints, modality
flags, review rules, and parser boundaries. They are profile data, not
approved signal truth.

## Profile Fields

| Field | Required | Rule |
|-------|----------|------|
| `channel_id` | yes | Stable source/channel ID. |
| `source_urls` | yes | Public source URLs associated with the channel. |
| `profile_version` | yes | Versioned profile ID. |
| `accepted_draft_terms` | yes | Terms that may inform draft suggestions only. |
| `needs_review_terms` | yes | Terms that must route to human review before parser truth. |
| `excluded_terms` | yes | Terms that must not create positive signal candidates. |
| `modality_flags` | yes | Boolean flags for text, voice, OCR, image, or future modalities. |
| `review_rules` | yes | Human-readable parser/review boundaries. |

## Term Fields

| Field | Required | Rule |
|-------|----------|------|
| `term` | yes | Exact profile term. |
| `category` | yes | Source category such as `asset_alias` or `direction_short`. |
| `profile_state` | yes | `accepted_for_draft`, `needs_review`, or `excluded`. |
| `evidence_capture_ids` | yes | Captures supporting the profile term. |
| `evidence_excerpts` | yes | Evidence snippets from public captures. |
| `false_positive_risk` | yes | Why the term can mislead parser/runtime behavior. |
| `confidence` | yes | Draft discovery confidence, not approval. |

## bablos79 Import

`import_bablos79_profile()` imports
`workspace/lexicons/bablos79_lexicon_draft.json` into registry form while
preserving all `profile_state` values:

- 17 `accepted_for_draft`;
- 9 `needs_review`;
- 6 `excluded`.

## Registry Lookup

Unknown channel lookup returns `None`. It must not fall back to `bablos79` or
any other profile because channel-specific vocabulary is not generally safe to
reuse.

## Non-Goals

- No parser runtime behavior changes.
- No approved ledger writes.
- No embeddings, vector store, or retrieval API.
- No LLM call.
