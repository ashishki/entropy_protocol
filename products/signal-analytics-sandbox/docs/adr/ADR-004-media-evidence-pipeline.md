# ADR-004: Media Evidence Pipeline

Date: 2026-05-09
Status: accepted

## Context

The `bablos79` Telegram channel contains voice/audio messages and
image/screenshot material that the current text-only capture path does not
analyze. Phase 20 adds a media evidence path so the operator can inventory,
transcribe, OCR, review, and cite this material without weakening the existing
public-source-only and deterministic-truth boundaries.

This ADR authorizes scope before any Telegram, Whisper, OCR, or media provider
code lands. It is a governance gate for `SAS-MEDIA-002..008`.

## Reference Pattern

Use Dream_Motif_Interpreter only as an implementation mechanics reference for
Telegram voice ingress and managed transcription. Do not copy its domain model,
database schema, assistant behavior, or user-facing dream workflow.

Reference files:

- `docs/VOICE_PIPELINE.md` — voice lifecycle: update, validation, media event,
  download, acknowledgement, transcription job, and cleanup.
- `docs/adr/ADR-005-managed-transcription-first.md` — managed transcription
  first, with local Whisper deferred.
- `app/telegram/voice.py` — Telegram `voice.file_id` download to a local `.ogg`
  file under an explicit media directory.
- `app/telegram/handlers.py` — voice handler sequencing: persist media event,
  download, acknowledge, enqueue transcription, track task completion.
- `app/workers/transcribe.py` — managed Whisper boundary, provider failure
  handling, transcript storage, terminal status update, and raw-audio cleanup.
- `tests/unit/test_telegram_voice.py` — mocked voice ingress tests.
- `tests/unit/test_transcription_worker.py` — mocked transcription success and
  failure tests.

Adapted Signal Analytics Sandbox pattern:

1. Represent media as local `MediaArtifact` metadata linked to source,
   capture, and source-document IDs.
2. Acquire Telegram media only from public or operator-authorized evidence.
3. Treat raw media as temporary operational data unless retained under the
   policy below.
4. Produce transcript/OCR artifacts as draft evidence only.
5. Require human review before any transcript/OCR evidence supports approved
   rows, reports, or customer-facing claims.

## Decision

Approve a Phase 20 media evidence pipeline for Telegram voice/audio and
image/OCR drafts.

Allowed source paths:

- public Telegram posts reachable through public `https://t.me/...` or
  `https://t.me/s/...` URLs already allowed by the legal memo;
- operator-forwarded Telegram media where the operator attests the media came
  from an approved public source and records the original source/channel,
  capture timestamp, and public evidence reference when available;
- local operator-supplied media files that are linked to an approved
  `SourceManifest`, capture ID, and source-document ID.

Forbidden source paths:

- private Telegram groups or channels;
- login-walled, paywalled, authenticated, or access-controlled sources;
- media obtained through impersonation, credential sharing, bypassing platform
  controls, or private scraping;
- autonomous channel monitoring or background collection bots;
- media not linkable to an approved source/capture/document identity.

## Runtime And Capability Impact

Runtime remains **T0**.

The implementation remains a local Python library and CLI. Phase 20 may add
local media metadata, local temporary files, and explicit provider adapters, but
it must not add a hosted service, persistent worker requirement, container
runtime, shell mutation, privileged action, or autonomous collection loop.

Capability profile changes:

| Profile | Status after ADR | Reason |
|---------|------------------|--------|
| RAG | ON | Unchanged. Media transcript/OCR refs may become cited retrieval context only after explicit review/linking tasks. |
| Tool-Use | OFF | No LLM-directed tool calls are approved. Telegram/Whisper/OCR adapters are deterministic application code invoked by operator workflows. |
| Agentic | ON | Unchanged. The bounded internal analyst remains allowed, but it cannot collect media or treat media drafts as truth. |
| Planning | OFF | No plan schema or plan-execution subsystem is introduced. |
| Compliance | OFF | No named regulatory framework is activated. Public-source, retention, non-advice, and review rules remain project-specific controls. |

## Provider Strategy

Voice transcription starts with a managed Whisper-style provider behind explicit
operator approval and cost gates. A fake client must cover CI. Local Whisper is
deferred until privacy, cost, or reliability evidence justifies the packaging
and model-management overhead.

OCR/image text extraction may be added only after `SAS-MEDIA-005` inventories
the image evidence and confirms text extraction is the bottleneck. OCR output is
draft evidence, not chart truth, visual-performance truth, or customer-facing
interpretation.

Every paid or networked provider must:

- be disabled by default;
- require an explicit environment/config gate and per-run approval;
- enforce the existing cost-cap posture;
- record provider/model/version and source artifact checksum;
- use fake/mocked provider tests in CI;
- fail closed without writing approved ledger rows, deterministic metrics, or
  customer-facing report content.

## Draft-Evidence Boundary

Transcript and OCR outputs are **review-required draft evidence**.

They may support:

- internal review queues;
- source-document draft refs;
- retrieval context after review/linking rules are satisfied;
- internal analyst notes that cite draft status clearly.

They may not:

- write approved `SignalRecord` or `MarketIdea` rows;
- write approved ledger rows;
- compute prices, returns, deterministic outcome metrics, or author
  performance statistics;
- create customer-facing report claims;
- bypass human review because a provider returned high confidence.

Human review must mark whether transcript/OCR evidence is usable, unusable, or
needs rework before it can support customer-sample material.

## Retention And Deletion

Raw media is temporary operational data.

Default retention:

- raw voice/audio and image files are stored locally under operator-controlled
  workspace paths only while acquisition/transcription/OCR/review work needs
  them;
- successful transcription/OCR should delete raw operational copies after
  checksum and draft artifact creation unless the operator explicitly retains a
  local evidence snapshot;
- retained raw media may remain for the pilot plus up to 90 days, matching the
  raw-capture memo, unless a stricter task-specific policy is introduced;
- metadata, hashes, source links, transcript/OCR draft paths, review status,
  and deletion timestamps may be retained for auditability.

Deletion triggers:

- operator deletion request;
- pilot cancellation;
- source eligibility changes to `blocked`;
- media is found to be private, authenticated, paywalled, or otherwise outside
  allowed source classes;
- provider/capture failure leaves an orphaned temporary file beyond the
  configured cleanup window;
- retention window expires.

Deletion must leave an audit trace containing media ID, source/capture linkage,
checksum when available, deletion timestamp, and deletion reason. Logs must not
include raw transcript text, OCR text, author handles, evidence URLs, local
workspace paths, or credentials.

## Non-Goals

Out of scope:

- private Telegram scraping;
- authenticated scraping or scraping behind access controls;
- autonomous Telegram channel monitoring;
- customer-facing report publication from media drafts;
- approved ledger writes from transcript or OCR output;
- chart interpretation as deterministic market truth;
- live trading, broker integration, copy trading, public leaderboard, or
  marketplace expansion;
- investment advice or forward-looking claims.

## Rollback Plan

If media work creates unacceptable legal, cost, retention, or review burden,
disable provider gates, delete temporary raw media per policy, keep only
metadata/deletion audit rows, and continue with the text-only capture and review
workflow. Existing text captures, MarketIdea drafts, deterministic metrics, and
review coverage artifacts remain valid because media drafts do not own truth
state.

## Acceptance Notes

This ADR satisfies `SAS-MEDIA-001` by authorizing the media evidence posture,
referencing the Dream_Motif_Interpreter mechanics files, preserving runtime T0,
and stating that transcript/OCR outputs are draft evidence only,
review-required, and forbidden from writing approved ledger rows or
customer-facing claims.
