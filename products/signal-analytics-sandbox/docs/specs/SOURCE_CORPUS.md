# Source Corpus Schema

Version: 0.1
Date: 2026-05-09
Status: specification for `SAS-MI-006`

## Purpose

`SourceDocument` normalizes public captures into a corpus shape that downstream
classification, extraction, and later retrieval can share. It preserves source
evidence identity and allows optional references to media, transcripts, and OCR
artifacts without introducing any transcription or OCR provider.

## Fields

| Field | Required | Rule |
|-------|----------|------|
| `document_id` | yes | Stable corpus ID, initially `<source_id>:<capture_id>`. |
| `capture_id` | yes | Original capture ID. |
| `source_id` | yes | Source/channel ID. |
| `author` | yes | Public author/channel handle or source ID. |
| `timestamp_utc` | yes | Source/capture timestamp in UTC. |
| `text` | yes | Captured public text, unchanged. |
| `evidence_url` | yes | Public evidence URL or local evidence reference. |
| `text_sha256` | yes | SHA-256 of `text`, preserved from capture. |
| `media_refs` | yes | Optional local media evidence references; defaults to empty list. |
| `transcript_refs` | yes | Optional transcript evidence references; defaults to empty list. |
| `ocr_refs` | yes | Optional OCR evidence references; defaults to empty list. |
| `metadata` | yes | String metadata for source type, loader version, or profile hints. |

## Conversion From CapturedPost

`from_captured_post()` converts the existing `CapturedPost` shape into
`SourceDocument` without changing:

- capture ID;
- source ID;
- evidence URL;
- captured text;
- text hash;
- timestamp.

The default author is the source ID unless the caller supplies a more specific
public author string.

## Non-Goals

- No transcription provider.
- No OCR provider.
- No embeddings.
- No vector store.
- No retrieval API.
- No approved ledger or market idea writes.

Voice/OCR fields are evidence links only. They make future modality work
representable without changing the base source-corpus schema.

## Multimodal Joins

`SAS-MEDIA-007` adds a pure join helper that returns enriched
`SourceDocument` copies with additive `media_refs`, `transcript_refs`, and
`ocr_refs`.

Rules:

- original `text`, `evidence_url`, and `text_sha256` are preserved
  byte-identically;
- media artifacts must match `source_id`, `capture_id`, and `document_id`;
- transcript/OCR artifacts must reference a known media ID and match that media
  artifact's checksum;
- transcript/OCR refs are additional draft evidence for review/retrieval
  context only;
- joins do not mutate approved `MarketIdea` rows, outcomes, ledgers, reports,
  market data, or customer-facing claims.
