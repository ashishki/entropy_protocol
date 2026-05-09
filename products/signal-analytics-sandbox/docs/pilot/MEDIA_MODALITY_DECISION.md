# Media Modality Decision

Date: 2026-05-09
Status: decided
Decision: iterate internally; do not use media evidence in a customer sample yet

## Decision

Continue the Phase 20 media path internally, but do **not** create a
media-backed customer sample report yet.

## Evidence Cited

- `docs/adr/ADR-004-media-evidence-pipeline.md`
- `docs/legal_risk_memo.md §Media Evidence`
- `docs/pilot/bablos79_MEDIA_INVENTORY.md`
- `docs/pilot/bablos79_MULTIMODAL_COVERAGE_PACK.md`
- `docs/specs/MEDIA_ARTIFACTS.md`
- `docs/specs/SOURCE_CORPUS.md`
- `docs/audit/MEDIA_EVAL.md`

## Media Coverage

- Public text captures: 60
- Local media artifacts: 0
- Draft transcripts: 0
- Draft OCR artifacts: 0
- Multimodal source-document joins: 0
- Ready-for-customer-sample multimodal rows: 0

## Transcript/OCR Quality

Adapter quality is covered only by fake-client CI tests so far:

- Telegram voice acquisition: PASS in local unit tests
- Whisper-style draft transcription: PASS in local unit tests
- OCR draft extraction: PASS in local unit tests
- Multimodal source join: PASS in local unit tests

No real `bablos79` media transcript or OCR artifact exists yet, so real
transcript/OCR quality is **not measured**.

## Customer Value

Expected value remains plausible because operator feedback identified channel
images/screenshots and voice/audio as the next bottleneck. Actual customer
value is unproven until the operator supplies or authorizes real public media,
human review marks transcript/OCR evidence usable, and a sample row demonstrates
that media changed the report decision quality.

## Cost And Risk

Cost/risk is controlled:

- media providers are fake-client tested and disabled unless explicitly invoked;
- voice transcription is double-gated;
- raw media retention and deletion triggers are governed by ADR-004;
- OCR/chart interpretation cannot create approved trading claims;
- customer-facing use remains blocked without human review.

Remaining risk:

- real Telegram media has not been acquired;
- real managed transcription/OCR cost and quality are unmeasured;
- media-derived evidence has not been reviewed by a human;
- no customer has confirmed that media-backed rows improve buying or trust.

## Next Action

Pause Phase 21 expansion. The next product action is operator/media evidence
collection:

1. Operator supplies or authorizes public `bablos79` voice/image media linked to
   capture IDs and source-document IDs.
2. Run `MediaArtifact` creation/acquisition for those items.
3. Run gated draft transcription/OCR where applicable.
4. Human reviewer marks transcript/OCR evidence usable, unusable, or needs
   rework.
5. Rebuild multimodal coverage and decide whether one customer sample row is
   justified.

## Forbidden Until Review

- customer-facing report claims based on transcript/OCR output;
- chart-derived trading claims;
- approved ledger or MarketIdea writes from media drafts;
- Phase 21 expansion that assumes media value has been proven.
