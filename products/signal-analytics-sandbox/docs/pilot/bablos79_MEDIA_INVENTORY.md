# bablos79 Media Inventory

Date: 2026-05-09
Status: internal scope gate for Phase 20

This artifact inventories known `bablos79` media gaps before OCR/image
implementation. It is not customer-facing and does not approve any transcript,
OCR text, chart interpretation, ledger row, metric, report, or trading claim.

## Inputs Checked

- `workspace/captures/bablos79/` — 60 public text captures
- `docs/pilot/bablos79_CAPTURE_MANIFEST.json`
- `docs/pilot/bablos79_REVIEW_COVERAGE_PACK.md`
- `docs/pilot/MEDIA_MODALITY_DEVELOPMENT_PLAN.md`
- operator direction that `bablos79` has image/screenshot and voice/audio
  material not covered by the text-only capture path

Current local evidence state:

- Local raw media files: none
- Local Telegram media file IDs: none
- Local transcript artifacts: none
- Local OCR artifacts: none
- Public text captures: 60

## Inventory Rows

| source/capture | modality | blocker type | expected evidence value | OCR needed | transcription needed | manual review needed | status |
|---|---|---|---|---|---|---|---|
| channel-level `bablos79` public Telegram media | image/screenshot | media not captured locally | Recover text embedded in screenshots, such as ticker lists, position notes, or market commentary that the text-only `/s/` capture misses. | yes | no | yes | approve draft OCR scope |
| channel-level `bablos79` public Telegram media | image/chart screenshot | chart interpretation risk | Preserve chart/image as evidence context without deriving support/resistance, entry, target, trend, or performance claims automatically. | maybe, text labels only | no | yes | chart-derived claims forbidden |
| channel-level `bablos79` public Telegram media | voice/audio | media not captured locally | Recover author commentary that may explain prior market thesis or trade-management context. | no | yes | yes | voice path already gated by `SAS-MEDIA-003..004` |
| `bablos79-10486` | voice reference in text | missing linked media artifact | Text says: "in the scope of my voice"; current capture has no voice file or transcript, so context may be incomplete. | no | yes, if linked public/operator-authorized voice exists | yes | pending media acquisition |
| `bablos79-10465` | video reference in text | missing linked media artifact | Text says: "I will record video"; current capture has no video/audio artifact. Treat as possible media gap, not evidence. | no | no for Phase 20 unless separate audio is supplied | yes | out of OCR scope |

## OCR Vs Image Annotation Decision

Approved next scope: **OCR draft extraction for image/screenshot text only**.

Rationale:

- The product gap is missing source evidence, not autonomous visual market
  analysis.
- OCR can recover visible written text from public/operator-authorized
  screenshots and attach it to review queues as draft evidence.
- OCR output must remain `draft_pending_review` with `reviewer_id="pending"`
  until a human confirms it against the source image.

Not approved:

- autonomous chart interpretation;
- automatic support/resistance, entry, stop, target, trendline, or pattern
  extraction from images;
- chart-derived trading claims;
- customer-facing claims based on OCR or image interpretation before human
  review;
- private or authenticated media capture.

Chart screenshots may be inventoried and linked as media artifacts, but any
market interpretation from the chart requires manual review and cannot be
computed or claimed by the OCR adapter.

## Follow-Up Scope For SAS-MEDIA-006

`SAS-MEDIA-006: OCR Draft Adapter` remains approved with this narrowed scope:

- input is local `MediaArtifact` rows with modality `image` or `screenshot`;
- provider/client is injected and fakeable in CI;
- output is draft OCR text only with media ID, provider/model, OCR text hash,
  source media checksum, `status="draft_pending_review"`, and
  `reviewer_id="pending"`;
- provider failures create no approved OCR artifact;
- raw image retention follows ADR-004;
- no public report claims, approved ledger rows, metrics, or chart-derived
  trading claims are created.

Acceptance-test requirement for `SAS-MEDIA-006` remains active in `docs/tasks.md`.
