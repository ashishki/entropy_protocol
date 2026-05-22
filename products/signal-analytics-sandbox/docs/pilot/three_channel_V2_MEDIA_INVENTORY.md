# Three-Channel V2 Media Inventory

Date: 2026-05-19
Status: internal_media_inventory_not_external_ready

## Scope

This inventory supports `SAS-NEXT-017`. It records public audio, image, chart,
checksum, blocker, and review status for the three pilot channels. It does not
approve transcript/OCR/chart evidence for customer-facing metrics.

## Inputs

- `docs/pilot/three_channel_V1_MEDIA_INVENTORY.md`
- `docs/pilot/bablos79_REAL_MEDIA_ACQUISITION.md`
- `docs/pilot/bablos79_MEDIA_REVIEW.md`
- `docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md`
- `docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.md`

## Channel Summary

| Channel | Public audio refs | Public image/chart refs | Checksum posture | Review status | Customer metric status |
|---|---:|---:|---|---|---|
| `bablos79` | 2 acquired voice refs | 2 unlinked channel-level candidates | acquired voice SHA-256 recorded; blocked rows have no checksum | `llm_reviewed_internal`, human/operator external review missing | excluded |
| `nemphiscrypts` | 0 acquired | 0 source-linked reviewed candidates | no media checksum because no media acquired | `not_acquired` | text-only until media is acquired and reviewed |
| `pifagortrade` | 0 acquired | 0 source-linked reviewed candidates | no media checksum because no media acquired | `not_acquired` | text-only until media is acquired and reviewed |

## Inventory Rows

| inventory_id | channel | source ref | source_document_id | modality | acquisition status | SHA-256 | blocker | review status |
|---|---|---|---|---|---|---|---|---|
| `media-v2-001` | `bablos79` | `https://t.me/bablos79/10476` | `bablos79:bablos79-10476` | voice/audio | `acquired_public` | `dc35f04c417d644b603c9336d96108d485682e467e88e1e476500b1add1e115c` | none for internal storage; human external acceptance missing | `llm_reviewed_internal` |
| `media-v2-002` | `bablos79` | `https://t.me/bablos79/10478` | `bablos79:bablos79-10478` | voice/audio | `acquired_public` | `87ae688d3e55e4ab0eed95c2e4ec3d6ec3aa8a8022acc37a70703b255d6e8b00` | none for internal storage; human external acceptance missing | `llm_reviewed_internal` |
| `media-v2-003` | `bablos79` | `https://t.me/bablos79/10486` | `bablos79:bablos79-10486` | voice/audio reference | `blocked_missing_linked_media` | `not_acquired_no_checksum` | exact referenced voice URL/file ID is not linked to the source text | `pending_operator_linkage` |
| `media-v2-004` | `bablos79` | `https://t.me/bablos79/10465` | `bablos79:bablos79-10465` | video/audio reference | `blocked_missing_followup_media` | `not_acquired_no_checksum` | post promises a later video, but exact follow-up media is unidentified | `pending_operator_linkage` |
| `media-v2-005` | `bablos79` | channel-level public media | `unlinked-channel-level:image-screenshot` | image/screenshot | `blocked_source_document_linkage` | `not_acquired_no_checksum` | no exact post URL, capture ID, source-document ID, or local file | `pending_operator_linkage` |
| `media-v2-006` | `bablos79` | channel-level public media | `unlinked-channel-level:chart-screenshot` | chart screenshot | `blocked_source_document_linkage` | `not_acquired_no_checksum` | no exact post linkage; chart-derived claims forbidden without manual review | `pending_operator_linkage` |
| `media-v2-007` | `nemphiscrypts` | current V1 workspace | `none` | audio/image/chart | `not_acquired` | `not_acquired_no_checksum` | no source-linked public media ref acquired in current workspace | `not_acquired` |
| `media-v2-008` | `pifagortrade` | current V1 workspace | `none` | audio/image/chart | `not_acquired` | `not_acquired_no_checksum` | no source-linked public media ref acquired in current workspace | `not_acquired` |

## Review Rules

- `llm_reviewed_internal` can support internal source joins only.
- `pending_operator_linkage` cannot enter transcript/OCR extraction.
- `not_acquired` cannot enter transcript/OCR extraction.
- Chart screenshots can preserve evidence context after linkage, but cannot
  create automatic support, resistance, entry, target, trend, or performance
  claims.
- Customer-facing media-backed claims require human/operator acceptance and a
  rerun external-ready gate.

## Next Processing Queue

| Queue | Rows | Next action |
|---|---:|---|
| Transcript human review | 2 | Review `media-v2-001` and `media-v2-002` for accepted/rejected transcript use. |
| Operator linkage needed | 4 | Link exact public media rows for `media-v2-003` through `media-v2-006`. |
| Media acquisition needed | 2 | Acquire source-linked public media only if `nemphiscrypts` or `pifagortrade` rows are identified. |

## Current Decision

No V2 media-backed claim is customer-facing eligible. The only acquired media
rows are `bablos79` voice/audio artifacts with checksums, and they remain
internal until human/operator review accepts the exact transcript span.
