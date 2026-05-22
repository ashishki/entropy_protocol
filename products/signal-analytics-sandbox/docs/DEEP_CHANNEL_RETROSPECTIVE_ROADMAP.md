# Deep Channel Retrospective Roadmap

Status: active
Date: 2026-05-15

## Goal

Turn Signal Analytics Sandbox from a narrow source-window validation run into a
deep author/channel retrospective product.

The target artifact is not "this channel is good" by assertion. The target
artifact is a traceable report that explains:

- what the author talks about;
- what types of claims are measurable;
- where the author appears strong;
- where evidence is weak or non-measurable;
- how selected thoughts later showed up in public market data;
- which conclusions are blocked by missing data, ambiguity, or review status.

Operating sequence:

```text
expanded public corpus -> media inventory -> OCR/transcripts -> claim ledger ->
market proxy mapping -> deterministic retrospective outcomes -> author capability report
```

## Current Decision

The current `bablos79` Phase 21 source/window is rejected for external delivery,
but it is not enough evidence to judge the channel. The next loop expands the
public corpus and adds image/OCR analysis instead of trying to over-polish the
current narrow window.

Core is paused. Trader Risk Audit and Signal Analytics Sandbox are the active
product tracks.

## Phase Map

| Phase | Name | Purpose | Gate |
|---|---|---|---|
| 22 | Expanded Public Corpus | Expand the public Telegram source window and register text/media coverage without private scraping. | A larger anti-cherry-pick corpus exists with source manifests, capture logs, media inventory, and legal boundary notes. |
| 23 | Image/OCR And Multimodal Evidence | Add image/screenshot/chart OCR and reviewed media evidence paths. | Text, voice, and image-derived evidence are separated by draft/review/final status and can be joined to source documents. |
| 24 | Claim Ledger And Market Outcomes | Extract reviewable author claims and compare measurable claims to public market data. | A claim ledger with measurable, non-measurable, confirmed, contradicted, and unresolved statuses exists. |
| 25 | Author Capability Report | Produce a buyer-readable retrospective report about what the author is good at and where evidence is weak. | The report has examples, counterexamples, limitations, and a ready/reject external pilot gate. |

## Phase 22 - Expanded Public Corpus

Input:

- public/operator-authorized Telegram source pages;
- current `bablos79` seed artifacts;
- legal/terms memo and public-only boundary;
- proposed expanded window, default 60-120 days unless the operator narrows it.

Scope lock:

- `SAS-DR-001` locks `bablos79` to a 90-day public Telegram window:
  `2026-02-15T00:00:00+00:00` through `2026-05-15T23:59:59+00:00`.
- The scope is fixed before expanded capture, claim extraction, market proxy
  mapping, or outcome analysis.
- Phase 21 rejected the narrow source/window for external delivery, not the
  channel as a whole.

Capture registration:

- `SAS-DR-002` registers the available seed corpus in
  `docs/pilot/bablos79_EXPANDED_CAPTURE_MANIFEST.json` and
  `docs/pilot/bablos79_EXPANDED_CAPTURE_PACK.md`.
- Current registered coverage is 60 public text captures from
  `2026-04-27T07:12:22+00:00` through `2026-05-06T06:57:32+00:00`, with 2
  media-linked rows and 3 explicit gap entries for the larger locked window.
- No market outcome analysis has run for this expanded scope.

Media inventory:

- `SAS-DR-003` writes
  `docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md`.
- Current media state is 2 acquired public voice refs, 2 missing linked media
  refs, 2 unlinked channel-level image/chart candidates, and gap-window media
  blockers.
- No OCR, image analysis, chart interpretation, transcript acceptance, or
  customer-facing media claim is approved by the inventory.

Gap register:

- `SAS-DR-004` writes `docs/pilot/bablos79_CORPUS_GAP_REGISTER.md`.
- Current known gaps include missing locked-window periods, message-ID
  continuity, linked-media blockers, unlinked image/chart candidates, forbidden
  source classes, and unresolved timestamps.
- Gaps are limitations or operator-input needs; they are not evidence of author
  quality.

Build:

- anti-cherry-pick source-window protocol;
- expanded text capture manifest;
- media inventory for images/screenshots/charts/voice/video links where public;
- capture completeness summary;
- corpus gap register.

Outputs:

- `docs/pilot/bablos79_DEEP_SCOPE.md`;
- `docs/pilot/bablos79_EXPANDED_CAPTURE_MANIFEST.json`;
- `docs/pilot/bablos79_EXPANDED_CAPTURE_PACK.md`;
- `docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md`;
- `docs/pilot/bablos79_CORPUS_GAP_REGISTER.md`.

Gate:

- expanded public capture scope is locked before extraction;
- selection window is justified and not cherry-picked around known outcomes;
- every source row has stable source/capture/document ids;
- every media item is public/operator-authorized or excluded;
- private Telegram scraping remains blocked.

## Phase 23 - Image/OCR And Multimodal Evidence

Input:

- expanded media inventory;
- public image/screenshot/chart files or source-linked media references;
- existing voice/transcript path;
- managed OCR/transcription providers when explicitly enabled.

Build:

- image acquisition/register path with checksums and source linkage;
- OCR draft run log;
- chart/screenshot manual review queue;
- reviewed image evidence refs;
- updated transcript/voice review policy;
- multimodal source join v2.

Outputs:

- `docs/pilot/bablos79_IMAGE_MANIFEST.json`;
- `docs/pilot/bablos79_OCR_RUN_EXPANDED.md`;
- `docs/pilot/bablos79_IMAGE_REVIEW_QUEUE.md`;
- `docs/pilot/bablos79_REVIEWED_MEDIA_EVIDENCE.md`;
- `docs/pilot/bablos79_TRANSCRIPT_ACCEPTANCE_POLICY.md`;
- `docs/pilot/bablos79_MULTIMODAL_SOURCE_PREVIEW_V2.md`.

Gate:

- OCR/transcript output is draft until reviewed;
- image/chart claims are not customer-facing until source-linked and reviewed;
- chart interpretation is either manually confirmed or labeled uncertain;
- raw media handling follows retention and storage policy.

## Phase 24 - Claim Ledger And Market Outcomes

Input:

- expanded text corpus;
- reviewed voice/image evidence;
- channel profile and author lexicon;
- local/public market data snapshots.

Build:

- claim taxonomy for macro context, event risk, directional bias, explicit
  trade setup, level/timing call, watchlist, and non-market commentary;
- claim ledger with evidence refs and review states;
- market proxy mapping for broad-market claims;
- deterministic outcome windows;
- confirmed/contradicted/unresolved/non-measurable classification;
- counterexample register.

Outputs:

- `docs/pilot/bablos79_CLAIM_LEDGER.json`;
- `docs/pilot/bablos79_CLAIM_LEDGER.md`;
- `docs/pilot/bablos79_MARKET_PROXY_MAP.md`;
- `docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.json`;
- `docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.md`;
- `docs/pilot/bablos79_COUNTEREXAMPLES.md`.

Gate:

- at least 30-50 reviewed claims or an explicit insufficient-corpus decision;
- every measurable claim has source timestamp, market proxy, horizon, and
  outcome method;
- every broad/non-measurable claim is labeled as such;
- at least 5 strong examples and 5 weak/blocked/counter examples are retained
  for report balance when available.

## Phase 25 - Author Capability Report

Input:

- claim ledger;
- market outcomes;
- media evidence review;
- counterexample register;
- legal/claim-safety boundary.

Build:

- author capability scorecard;
- strongest supported patterns;
- weak/unverified patterns;
- retrospective examples with evidence;
- limitations and non-advice boundary;
- internal demo pack;
- external pilot ready gate.

Outputs:

- `docs/pilot/reports/bablos79_AUTHOR_CAPABILITY_REPORT_V1.md`;
- `docs/pilot/bablos79_AUTHOR_CAPABILITY_SCORECARD.md`;
- `docs/pilot/bablos79_DEEP_RETROSPECTIVE_DEMO_PACK.md`;
- `docs/pilot/bablos79_DEEP_EXTERNAL_READY_GATE.md`;
- `docs/audit/PHASE25_RETROSPECTIVE_REVIEW.md`.

Gate:

- report cites every claim to source/media/market artifacts;
- report includes both supporting examples and disconfirming/blocked examples;
- report does not rank the author as a trading signal provider;
- no future-profit, buy/sell/hold, leaderboard, or marketplace claim appears;
- operator decides ready / needs fixes / reject before external delivery.

## Success Criteria

Minimum useful readiness before showing the report:

- expanded public corpus captured and registered;
- image/OCR path exercised on real public media when available;
- voice/transcript path reviewed or explicitly excluded;
- 30-50 reviewed author claims, or an explicit finding that the corpus does not
  support that many measurable claims;
- deterministic retrospective outcomes for measurable claims;
- balanced examples and counterexamples;
- buyer-readable author capability report;
- external ready gate completed.

## Anti-Cherry-Pick Rule

Do not build the report only from the author's best-looking posts. The expanded
scope must be fixed before outcome analysis and must retain:

- non-market posts;
- ambiguous posts;
- strong examples;
- weak examples;
- contradicted or unresolved examples;
- unsupported media claims.

The product value is disciplined retrospective evidence, not promotional
channel ranking.
