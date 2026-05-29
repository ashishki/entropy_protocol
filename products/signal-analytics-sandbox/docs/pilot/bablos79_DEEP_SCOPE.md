# Deep Retrospective Scope Lock - bablos79

Date: 2026-05-15
Status: locked_before_capture_and_outcome_analysis

This artifact locks the expanded public-source scope for the `bablos79` deep
channel retrospective. It exists before expanded capture, media review, claim
ledger work, market proxy mapping, or retrospective outcome analysis.

## Locked Source

| Field | Locked value |
|---|---|
| Source URL | `https://t.me/bablos79` |
| Source ID | `bablos79` |
| Source class | `telegram_public` |
| Public-only status | approved by `docs/legal_risk_memo.md` for public/operator-authorized source use |
| Expanded window ID | `bablos79-deep-2026-02-15-2026-05-15` |
| Source timestamp window | `2026-02-15T00:00:00+00:00` through `2026-05-15T23:59:59+00:00` |
| Window length | 90 calendar days |
| Prior seed subset | existing text capture window `2026-04-27T07:12:22+00:00` through `2026-05-06T06:57:32+00:00` |
| Capture method | public unauthenticated Telegram `/s/` HTML capture, plus operator-supplied files only when each file is tied to a public source URL/ref |
| Report language | Russian-first pilot report; English internal summaries are allowed only as operator notes |
| External delivery state | blocked until later ready gate passes |

## Scope Decision

The expanded retrospective uses a fixed 90-day public window ending on the
scope-lock date. The window is fixed before market-outcome analysis so the
report cannot be built only from posts that look good after outcomes are known.

Phase 21 rejected the narrow `2026-04-27` through `2026-05-06` source/window
for external delivery. That decision does not reject `bablos79` as a channel.
It means the narrow window had zero deterministic outcome-ready rows and no
human/operator accepted media evidence for external claims.

The next phases must evaluate the broader public corpus as evidence, including
strong examples, weak examples, ambiguous posts, non-measurable claims, and
counterexamples.

## Inclusion Rules

Include a row only when all required source fields can be recorded:

- source URL/ref under `https://t.me/bablos79/...` or public `/s/bablos79/...`;
- source timestamp inside the locked window;
- deterministic source/capture/document ID;
- capture timestamp;
- capture method;
- raw text hash when text is captured;
- media linkage fields when a public media item is present;
- authorization state of `public_telegram_source` or
  `operator_supplied_from_public_source`.

The existing 60 public text captures are included as the seed subset because
they fall inside the locked window. Newly captured public rows from the same
window must be registered in the expanded capture manifest before extraction.

## Exclusion Rules

Exclude and record in the gap register:

- private Telegram groups or access-controlled channels;
- login-walled, paywalled, or authenticated media;
- access-control bypass, impersonation, credential sharing, or private
  scraping;
- rows outside the locked timestamp window;
- unlinked channel-level media with no source/capture/source-document ID;
- media items whose public source URL/ref cannot be preserved;
- duplicate captures after canonical source ID normalization;
- rows whose timestamp cannot be resolved well enough for source ordering.

Exclusion is not a negative outcome. It is a coverage limitation.

## Media Posture

Media evidence remains internal-only until reviewed.

- Voice/audio/video/image/chart items may be registered only when public or
  operator-supplied from a public source and linked to an included source row.
- Transcript and OCR output are draft evidence until human/operator review or a
  later explicitly accepted review policy marks them usable.
- Chart interpretation is manual-review-only. OCR may extract visible text, but
  support/resistance, entry, target, trend, or performance interpretation must
  not be inferred automatically.
- Customer-facing claims cannot rely on unreviewed transcript, OCR, image,
  chart, voice, or video evidence.
- Raw media remains local operational evidence and does not approve ledgers,
  reports, or outcome metrics.

## Claim Boundary

Allowed claims:

- public corpus coverage counts;
- text/media coverage and gap counts;
- reviewed author claim categories;
- historical outcome statements only for measurable, reviewed claims with
  source timestamp, market proxy, horizon, and deterministic market data;
- explicit limitations for ambiguous, unresolved, contradicted, or
  non-measurable claims;
- source behavior observations tied to cited public evidence.

Blocked claims:

- investment advice or buy/sell/hold recommendations;
- future-profit, expected-return, or predictive-performance claims;
- marketplace, leaderboard, ranking, or "best channel" claims;
- claims based on private, paywalled, login-walled, or access-bypassed sources;
- customer-facing claims based on draft extraction, draft transcript, draft OCR,
  or unreviewed media evidence;
- treating broad commentary as a trade setup without explicit asset, thesis or
  direction, timestamp, horizon, and source evidence.

## Anti-Cherry-Pick Protocol

The following order is mandatory:

1. Lock this window and scope.
2. Build the expanded public capture manifest for the locked window.
3. Register text/media coverage and gaps.
4. Review evidence and build the claim ledger.
5. Map market proxies only after the claim ledger is frozen for review.
6. Compute deterministic retrospective outcomes only for measurable reviewed
   rows.

Later phases may mark a row as strong, weak, contradicted, unresolved, or
non-measurable, but they must not remove eligible weak or inconvenient rows from
the locked corpus to improve the final report.

## Phase 21 Carry-Forward

Carry forward these findings as limitations, not as a channel-level rejection:

- `docs/pilot/bablos79_EXTERNAL_PILOT_READY_GATE.md` rejects the narrow
  Phase 21 source/window for external delivery.
- `docs/audit/PHASE21_ERROR_REGISTER.md` keeps external blockers open for human
  media acceptance, deterministic outcome support, and the unidentified follow-up
  video promised by `bablos79-10465`.
- the internal LLM-reviewed media-backed report is usable only as internal
  validation context, not as external-ready evidence.

## Next Artifacts

`SAS-DR-002` must create the expanded capture manifest and pack for this locked
window before any claim extraction or outcome work starts.
