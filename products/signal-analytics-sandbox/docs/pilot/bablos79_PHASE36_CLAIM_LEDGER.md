# Phase 36 Claim Ledger Recompute - bablos79

Date: 2026-05-22
Status: `recomputed_no_new_accepted_media_claims`

This recompute applies the Phase 36 transcript and OCR gates to the existing
`bablos79` claim ledger. It does not add media-backed claims to customer-facing
metrics because no transcript or OCR source reached accepted status.

## Summary

| Metric | Count |
| --- | ---: |
| Prior ledger rows | 67 |
| Text capture rows | 60 |
| Prior reviewable non-blocker claim rows | 14 |
| Phase 36 text reviewable rows retained | 11 |
| Accepted transcript claims added | 0 |
| Accepted OCR claims added | 0 |
| Excluded transcript claims | 3 |
| Rejected or blocked media rows | 6 |
| Deterministic outcome-ready rows | 0 |
| Customer-report eligible rows | 0 |

## Source Separation

| Group | Source modality | Count | Phase 36 status | Blocker |
| --- | --- | ---: | --- | --- |
| `text_prior_reviewable` | text | 11 | `retained_internal_reviewable` | Missing deterministic fields or approved proxy. |
| `accepted_transcript` | voice transcript | 0 | `none_accepted` | Both linked transcript refs are `needs_context`. |
| `accepted_ocr` | image/chart OCR | 0 | `none_available` | No source-linked image/chart artifacts exist. |
| `blocked_media` | audio/image/chart/gap | 6 | `excluded_from_customer_metrics` | Missing acceptance, source linkage, checksumable artifact, or capture rows. |

## Deterministic Candidate Result

No deterministic candidate is ready. Every prior candidate either lacks asset,
direction, horizon, setup fields, accepted media status, or approved proxy. No
market outcome recompute should run from this ledger state.
