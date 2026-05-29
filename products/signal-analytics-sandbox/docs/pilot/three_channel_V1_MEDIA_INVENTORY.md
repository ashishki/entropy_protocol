# Three-Channel V1 Media Inventory

Date: 2026-05-19
Status: internal_media_inventory

## Scope

This inventory supports `SAS-V1-005`. It records the public audio, transcript,
image, chart, and OCR posture for the three pilot channels before V1
multimodal claim extraction.

## Channel Inventory

| Channel | Public audio refs | Transcript status | Image/chart candidates | OCR status | Customer metric eligibility |
|---|---:|---|---:|---|---|
| `bablos79` | 2 acquired public voice refs | `llm_reviewed_internal`, not human/operator external accepted | 4 blocked candidates from prior review | no reviewed OCR refs | excluded until human/operator accepts transcript/OCR/chart refs |
| `nemphiscrypts` | 0 acquired in current V1 workspace | no transcript refs | 0 reviewed source-linked chart refs | no reviewed OCR refs | text-only for V1 until media is acquired and reviewed |
| `pifagortrade` | 0 acquired in current V1 workspace | no transcript refs | 0 reviewed source-linked chart refs | no reviewed OCR refs | text-only for V1 until media is acquired and reviewed |

## Reviewed Media Rules

| Media state | V1 extraction decision | Customer-facing decision |
|---|---|---|
| human/operator accepted transcript ref | may produce structured claim draft with media provenance | eligible after V1 gate |
| `llm_reviewed_internal` transcript ref | internal-only source join | excluded from customer-facing metrics |
| unreviewed transcript ref | excluded | excluded |
| reviewed OCR/chart text ref | may produce structured claim draft with media provenance | eligible after V1 gate |
| unreviewed OCR/chart interpretation | excluded | excluded |
| missing/private/login-walled media | excluded | excluded |

## Current Decision

No media-backed claim is customer-facing eligible yet. The V1 code path can
extract structured drafts from accepted transcript/OCR refs, but current
three-channel reporting must keep unreviewed transcript/OCR/chart claims out of
metrics and report language.
