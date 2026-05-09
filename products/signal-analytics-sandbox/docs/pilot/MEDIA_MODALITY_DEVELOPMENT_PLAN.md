# Media Modality Development Plan

Date: 2026-05-09
Status: in progress

## Why This Phase Exists

The `bablos79` channel contains image/screenshot and voice/audio material that
the current text-only capture path does not analyze. Phase 19 deliberately
deferred modality providers, but the operator has now identified media as the
next product bottleneck. The next phase should add media evidence support while
preserving the existing audit boundaries:

- public-source-only;
- local-first T0 runtime;
- raw media is temporary operational data unless explicitly retained as an
  evidence snapshot;
- OCR/transcription output is draft evidence, not truth;
- all customer-facing claims still require reviewed evidence and deterministic
  market metrics.

## Reference Implementation

Use `https://github.com/ashishki/Dream_Motif_Interpreter` as the implementation
reference for Telegram voice mechanics, not as a domain model to copy.

Relevant reference files:

- `docs/VOICE_PIPELINE.md` — lifecycle: voice update, validation, media event,
  download, acknowledgement, transcription job, cleanup.
- `docs/adr/ADR-005-managed-transcription-first.md` — managed transcription
  first, local Whisper deferred.
- `app/telegram/voice.py` — Telegram `voice.file_id` download to local `.ogg`.
- `app/telegram/handlers.py` — voice handler orchestration and acknowledgement.
- `app/workers/transcribe.py` — OpenAI Whisper transcription boundary and raw
  audio cleanup after success.
- `tests/unit/test_telegram_voice.py` and
  `tests/unit/test_transcription_worker.py` — fake/mocked provider tests.

Signal Analytics Sandbox must adapt the pattern differently:

- the product analyzes public market-author evidence, not personal dream data;
- voice/image media must link back to `SourceDocument` and `capture_id`;
- Telegram bot ingestion is allowed only for operator-forwarded or otherwise
  authorized public evidence, never private group scraping;
- transcription/OCR outputs must remain review-required draft artifacts.

## Phase 20 Goal

Add a safe multimodal evidence path for Telegram voice notes and images:
inventory first, then local media artifact metadata, then gated draft
transcription/OCR, then join those draft outputs into source documents and the
review coverage pack.

## Proposed Task Order

1. `SAS-MEDIA-001: Media Scope ADR And Legal Addendum` — done
   Decide exact allowed media sources, retention, provider strategy, and
   approval gates before code lands.

2. `SAS-MEDIA-002: MediaArtifact Schema And Manifest` — done
   Represent local voice/image files, checksums, source linkage, modality,
   retention state, and draft-output refs without adding providers.

3. `SAS-MEDIA-003: Telegram Voice Acquisition Adapter` — done
   Adapt the proven Telegram `voice.file_id` download pattern for
   operator-authorized public evidence. No transcription yet.

4. `SAS-MEDIA-004: Whisper Transcript Draft Adapter` — done
   Add gated managed Whisper transcription with fake-client CI coverage,
   cost/approval gates, transcript provenance, and raw-audio cleanup.

5. `SAS-MEDIA-005: Image Evidence Inventory And OCR Scope` — done
   Inventory image/screenshot captures and decide whether OCR or richer image
   annotation is needed for this channel.

6. `SAS-MEDIA-006: OCR Draft Adapter` — done
   Add review-required OCR/image text extraction over local image artifacts,
   with no customer-facing claims and no chart-level truth without review.

7. `SAS-MEDIA-007: Multimodal SourceDocument Join` — done
   Link transcript/OCR refs into `SourceDocument` records and retrieval context
   without overwriting original capture text or hashes.

8. `SAS-MEDIA-008: Multimodal Coverage Pack And Decision Gate` — done
   Extend the reviewer coverage pack to show text/transcript/OCR coverage and
   decide whether a media-backed customer sample is now justified.

## Hard Boundaries

- No private Telegram group scraping.
- No authenticated scraping behind access controls.
- No autonomous channel monitoring bot.
- No approved ledger writes from OCR/transcription output.
- No LLM-derived market outcomes or performance claims.
- No raw audio/image retention beyond the policy accepted in
  `SAS-MEDIA-001`.
- No customer-facing report use until human review marks the evidence ready.

## Expected End State

At the end of Phase 20, the product should be able to say, for each public
`bablos79` media item:

- what file was captured and from which public source/capture;
- whether it is voice, image, screenshot, or other media;
- whether it has a draft transcript/OCR artifact;
- whether a human reviewed it;
- which MarketIdea/evidence rows it supports;
- whether it is safe to use in a customer sample.
