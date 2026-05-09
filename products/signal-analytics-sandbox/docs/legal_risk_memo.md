# Public-Source Legal / Terms Memo

Date: 2026-05-07
Owner: operator
Status: acknowledged for Phase 0 gate SAS-002

This memo records the operator's source-risk decision for the initial pilot. It
is not a general legal opinion. The implementation contract remains stricter
than this memo: source handling must stay public-source-only, deterministic, and
operator-controlled.

## Allowed Source Classes

The following source classes are allowed for v1 manifests:

| Source class | Allowed in current pilot? | Conditions |
|--------------|---------------------------|------------|
| telegram_public | yes | Public Telegram source reachable through a public `https://t.me/...` URL. |
| x_public | deferred | Allowed by architecture, but not part of the initial pilot. Requires a later source-specific review before use. |
| website_public | deferred | Allowed by architecture, but not part of the initial pilot. Requires a later source-specific review before use. |

## Forbidden Source Classes

The following are forbidden for v1:

- private Telegram groups or channels
- paywalled sources
- login-walled sources
- sources behind access controls
- sources requiring impersonation, credential sharing, or bypassing platform controls
- automated scraping of private or restricted content

## Capture Mechanism

Initial capture is operator-supplied only. The operator provides public post text
or exports from approved public sources into the local workspace. Engineering v1
must not add authenticated scraping or private-source collection paths.

## Retention

Raw captures may be retained locally for the duration of the pilot plus up to 90
days for reproducibility and dispute resolution. Deletion is triggered by
operator request, pilot cancellation, or source eligibility being changed to
blocked. Evidence snapshots used in reports keep only the fields required by the
implementation contract: source id, public URL reference, capture timestamp, and
raw-text hash.

## Screenshots

Screenshot and OCR capture are deferred in v1. They may be reconsidered only if
the paid Telegram pilot proves that text-only capture is the bottleneck and a
follow-up memo explicitly authorizes screenshot/OCR handling.

## Media Evidence

Status: authorized for Phase 20 under `docs/adr/ADR-004-media-evidence-pipeline.md`.

Allowed media capture is limited to:

- voice/audio/image media attached to approved public Telegram sources;
- operator-forwarded Telegram media when the operator records that the media
  came from an approved public source and preserves source/capture linkage;
- local operator-supplied media files linked to an approved `SourceManifest`,
  capture ID, and source-document ID.

Forbidden media capture includes:

- private Telegram groups or channels;
- login-walled, paywalled, authenticated, or access-controlled media;
- media obtained through impersonation, credential sharing, bypassing platform
  controls, or private scraping;
- autonomous channel monitoring or background collection bots;
- media that cannot be linked to an approved public source/capture/document.

Raw media retention:

- raw audio/image files are temporary operational data stored only in the local
  operator workspace;
- successful transcription/OCR should delete raw operational copies after
  checksum and draft artifact creation unless the operator explicitly retains a
  local evidence snapshot;
- retained raw media follows the raw-capture retention limit: pilot duration
  plus up to 90 days;
- metadata, hashes, source linkage, draft transcript/OCR refs, review status,
  and deletion timestamps may be retained for auditability.

Deletion is triggered by operator request, pilot cancellation, source
eligibility changing to blocked, discovery that the media came from a forbidden
source class, orphaned temporary files surviving beyond the cleanup window, or
retention expiry.

Transcript and OCR output is review-required draft evidence only. It cannot
write approved ledger rows, approve `MarketIdea` rows, compute deterministic
metrics, create report claims, or appear in customer-facing samples until human
review marks the evidence usable.

## Per-Pilot Verdicts

| Pilot source | Source of interest | Verdict | Rationale |
|--------------|--------------------|---------|-----------|
| https://t.me/bablos79 | telegram_public | approved | Operator confirmed this as an initial public Telegram pilot source. |
| https://t.me/nemphiscrypts | telegram_public | approved | Operator confirmed this as an initial public Telegram pilot source. |
| https://t.me/pifagortrade | telegram_public | approved | Operator confirmed this as an initial public Telegram pilot source. |

## Expansion Notes

Twitter / X and Discord are not included in the initial pilot. They should be
handled through a later source-specific update before any implementation or
capture workflow depends on them.
