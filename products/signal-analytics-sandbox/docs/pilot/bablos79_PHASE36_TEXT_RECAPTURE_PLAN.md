# Phase 36 Text Recapture Plan - bablos79

Date: 2026-05-22
Status: plan_ready_operator_or_capture_agent_next
Owner: codex + operator

## Purpose

This plan starts `SAS-BABLOS-002`. It defines how to fill or explicitly close
the missing public text coverage before any stronger `bablos79` author
capability conclusion.

The current state is partial:

- locked target window: `2026-02-15T00:00:00+00:00` through
  `2026-05-15T23:59:59+00:00`;
- validated seed coverage: `2026-04-27T07:12:22+00:00` through
  `2026-05-06T06:57:32+00:00`;
- validated seed text captures: 60;
- fresh records captured during Phase 22 seed registration: 0;
- missing public period before seed: about 71 days;
- missing public period after seed: about 9 days;
- non-contiguous seed message IDs: 7 known IDs.

## Public Source Boundary

Allowed:

- public Telegram `/s/bablos79` pages;
- operator-supplied public post URLs;
- operator-supplied media files only if tied to exact public post URLs and
  checksums.

Not allowed:

- private Telegram groups;
- login-walled or paywalled sources;
- access-control bypass;
- guessing timestamps, claims, deleted text, or media content;
- treating missing rows as wins, losses, weak evidence, or strong evidence.

## Capture Targets

| target_id | scope | current state | required action | output classification |
|---|---|---|---|---|
| `recapture-pre-seed-window` | `2026-02-15T00:00:00+00:00` -> `2026-04-27T07:12:22+00:00` | no local source rows | Attempt public `/s/` capture by message/page traversal or record source-specific unavailable reason. | captured / unavailable / deleted / outside-public-boundary |
| `recapture-post-seed-window` | `2026-05-06T06:57:32+00:00` -> `2026-05-15T23:59:59+00:00` | no local source rows | Attempt public `/s/` capture by message/page traversal or record source-specific unavailable reason. | captured / unavailable / deleted / outside-public-boundary |
| `recapture-missing-10462` | `https://t.me/bablos79/10462` | missing inside seed sequence | Open public post URL or `/s/` page and classify. | captured / deleted / media-only / unavailable |
| `recapture-missing-10473` | `https://t.me/bablos79/10473` | missing inside seed sequence | Open public post URL or `/s/` page and classify. | captured / deleted / media-only / unavailable |
| `recapture-missing-10474` | `https://t.me/bablos79/10474` | missing inside seed sequence | Open public post URL or `/s/` page and classify. | captured / deleted / media-only / unavailable |
| `recapture-missing-10480` | `https://t.me/bablos79/10480` | missing inside seed sequence | Open public post URL or `/s/` page and classify. | captured / deleted / media-only / unavailable |
| `recapture-missing-10481` | `https://t.me/bablos79/10481` | missing inside seed sequence | Open public post URL or `/s/` page and classify. | captured / deleted / media-only / unavailable |
| `recapture-missing-10484` | `https://t.me/bablos79/10484` | missing inside seed sequence | Open public post URL or `/s/` page and classify. | captured / deleted / media-only / unavailable |
| `recapture-missing-10494` | `https://t.me/bablos79/10494` | missing inside seed sequence | Open public post URL or `/s/` page and classify. | captured / deleted / media-only / unavailable |

## Output Schema

Each captured or classified row should produce a compact record:

| Field | Required | Notes |
|---|---|---|
| `capture_id` | yes | Stable ID such as `bablos79-10462`. |
| `source_url` | yes | Exact public URL or attempted URL. |
| `source_timestamp_utc` | yes if captured | Do not infer if absent. |
| `text_sha256` | yes if text exists | Hash normalized source text. |
| `media_refs` | yes | Empty list if none; blocker ref if media-only/unlinked. |
| `classification` | yes | `captured`, `deleted`, `media_only`, `unavailable`, `outside_public_boundary`. |
| `evidence_note` | yes | Short reason and source method. |
| `operator_required` | yes | `true` when public fetch cannot resolve the row. |

## Stop Conditions

Stop and keep the row unresolved if:

- Telegram public page does not expose the row;
- timestamp is missing or ambiguous;
- only media exists but no source-linked file/checksum is available;
- source requires login/private access;
- the row is only referenced indirectly by another post.

## What Happens After This Plan

The next task is `SAS-BABLOS-003 Media Linkage Queue`.

Inputs for that task:

- rows captured or classified from this plan;
- existing media inventory;
- known audio refs `10476` and `10478`;
- blocked media refs from `10465`, `10486`, image screenshots, chart
  screenshots, and coverage gaps.

No outcome metrics should be recomputed until the recapture output and media
linkage queue exist.
