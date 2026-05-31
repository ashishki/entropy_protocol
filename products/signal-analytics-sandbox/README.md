# Signal Analytics Sandbox Workspace

Report-product candidate for public Telegram/X-style source analytics. It is
separate from Entropy Core and Trader Risk Audit.

## Current Status

- Phase: 42 Auto-Accept Decision Engine And Evaluation
- Next task: `SAS-AUTOVAL-009`
- Baseline: 422 passing tests, 0 skipped
- Current priority: automate candidate validation with evidence bundles,
  independent validators, strict thresholds, and customer-facing policy gates

## Promise

Analyze a public source/channel and produce a bounded research report covering
source evidence, reviewed market ideas/signals, ambiguity, historical outcomes
where supported, and limitations.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`
3. `docs/ARTIFACT_VALIDATION_ROADMAP.md`
4. `docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md`
5. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
6. `docs/tasks.md` Phase 35
7. `docs/AI_DEVELOPMENT_PLAN_RU.md`
8. `docs/pilot/THREE_CHANNEL_V1_ROADMAP.md`
9. `docs/legal_risk_memo.md`

## Implemented Surface

- source manifests and public capture workflows;
- signal/MarketIdea schemas and review queues;
- local market-data snapshots and deterministic horizon metrics;
- Author Market Intelligence flow;
- report exports;
- media artifact metadata, transcript/OCR draft paths, and multimodal source
  joins;
- transcript acceptance policy for internal vs external media-backed use;
- reviewer coverage pack for existing `bablos79` corpus.
- artifact-first capture/review/outcome/report pack for current text-only
  `bablos79` evidence.

Historical detail lives in `docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`,
`AGENT_NOTES.md`, and `docs/tasks.md`.

## Artifact-First Work

Completed Phase 21 tasks:

- SAS-AF-001 source/report scope lock;
- SAS-AF-002 public capture pack;
- SAS-AF-003 human review queue closure;
- SAS-AF-004 market data/outcome prep;
- SAS-AF-005 first real report;
- SAS-LIVE-001..009 real public media-backed report route;
- SAS-AF-006 manual validity review after media-backed report;
- SAS-AF-007 internal demo pack;
- SAS-AF-008 external pilot ready gate.

Decision: keep current `bablos79` source/window as an internal LLM-reviewed
media-backed result, not external delivery. Two public voice files were acquired,
managed Whisper produced draft transcripts, and OpenAI `gpt-4.1` marked both
transcript refs usable for internal source join; deterministic outcome-ready
rows remain zero.

## Deep Channel Retrospective Work

Current deep retrospective state:

- Phase 22, SAS-DR-001..005: complete and archived at
  `docs/archive/PHASE22_REVIEW.md`;
- Phase 23, SAS-DR-006..011: image acquisition, OCR draft run, image/chart
  review queue, transcript acceptance policy, multimodal source join v2, and
  deep review. Phase 23 is archived at `docs/archive/PHASE23_REVIEW.md`;
- Phase 24, SAS-DR-012..017: author claim taxonomy, expanded claim ledger,
  market proxy map, retrospective outcomes, counterexample register, and deep
  review. Phase 24 is archived at `docs/archive/PHASE24_REVIEW.md`;
- Phase 25, SAS-DR-018..022: author capability scorecard, report V1, demo
  pack, external ready gate, and deep review. `SAS-DR-018` is complete at
  `docs/pilot/bablos79_AUTHOR_CAPABILITY_SCORECARD.md`; `SAS-DR-019` is
  complete at
  `docs/pilot/reports/bablos79_AUTHOR_CAPABILITY_REPORT_V1.md`; `SAS-DR-020`
  is complete at `docs/pilot/bablos79_DEEP_RETROSPECTIVE_DEMO_PACK.md`;
  `SAS-DR-021` is complete at
  `docs/pilot/bablos79_DEEP_EXTERNAL_READY_GATE.md`; `SAS-DR-022` is complete
  at `docs/archive/PHASE25_RETROSPECTIVE_REVIEW.md`.

The current `bablos79` Phase 21 result is a narrow-window reject case, not a
final judgment on the channel. Phase 24 found insufficient evidence for
positive author capability claims: 14 reviewable non-blocker claim rows, 0
approved proxies, 0 market snapshots, 0 computed outcomes, and 0 confirmed or
contradicted examples.

Final Phase 25 decision: `bablos79` deep retrospective is internal-only and
rejected for external delivery. Next work, if any, should repair evidence:
public corpus coverage, accepted media, explicit proxies, and market outcome
prerequisites.

Phase 26 evidence repair has started. `SAS-ER-000` expanded public `/s/`
coverage to 522 text rows, wrote 462 fresh workspace captures, and queued 156
market-adjacent candidates at
`docs/pilot/bablos79_EVIDENCE_REPAIR_REVIEW_QUEUE.md`. The next blocker is
operator approval of candidate rows, proxies, horizons, and outcome methods.

`SAS-ER-002` added a same-method public `/s/` probe for the three initial pilot
channels at `docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.md`: 1,534 text rows,
963 market-adjacent candidates, 64 explicit setup candidates, and 114
position/trade-language candidates. No market data, outcomes, or external
claims were created.

`SAS-ER-003` codified the channel utility method at
`docs/specs/CHANNEL_UTILITY_EVALUATION.md`: public text, audio transcripts, and
image/OCR evidence normalize into one claim/MarketIdea surface; approved rows
are validated through open/public API or operator-public-export windows on
demand; only compact reproducibility snapshots are cached.

`SAS-ER-004` produced the first historical metric comparison at
`docs/pilot/three_channel_METRIC_REPORT.md`: 187 normalized asset-level claims,
184 7d-evaluable claims, 102 confirmed hits, and 82 contradicted misses across
the three pilot channels. Market validation used Binance public klines and MOEX
ISS daily candles only.

`SAS-ER-005` added the Phase 27 V1 roadmap. `docs/tasks.md` now defines
`SAS-V1-001..009`, from approval matrix and false-positive review through
structured extraction, level-aware outcomes, multimodal claims, provider
expansion, V1 recompute, customer-facing gate, and deep review.

`SAS-ER-001` recorded the internal V1 proxy/horizon approval matrix at
`docs/pilot/bablos79_EVIDENCE_REPAIR_PROXY_APPROVALS.md`: nine `bablos79`
position rows have partial MOEX ISS asset-level approvals, one row is rejected
as context, unsupported assets remain `do_not_fetch`, and external use remains
blocked.

`SAS-ER-006` closed Phase 26 at `docs/archive/PHASE26_REVIEW.md`: no P0/P1/P2
implementation findings were found. Phase 27 may start, but V0 metrics remain
internal research until V1 review and gate complete.

`SAS-V1-001` created
`docs/pilot/three_channel_V1_APPROVAL_MATRIX.md`: all three pilot channels now
have explicit evaluator, claim-type, horizon, provider/proxy, and exclusion
rules for internal V1 work.

`SAS-V1-002` created `docs/pilot/three_channel_V1_EXTRACTION_REVIEW.md` and
`docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md`: V1 now has reviewed
false-positive/false-negative examples and deterministic calibration rules.

`SAS-V1-003` added `src/signal_sandbox/claims/`: a deterministic structured
claim extractor for text `SourceDocument` rows.

`SAS-V1-004` added deterministic V1 claim outcomes for strict trade setups,
directional theses, and trade-management exclusions.

`SAS-V1-005` added a three-channel media inventory and a reviewed
transcript/OCR to structured-claim draft path; unreviewed media remains
excluded.

`SAS-V1-006` added provider/proxy config and approved fetch planning.
`SAS-V1-007` produced internal V1 metric results and scorecard.
`SAS-V1-008` produced the V1 report and external gate. `SAS-V1-009` archived
Phase 27. Internal V1 validation is complete; external delivery is not approved.

## Scope In

- public source ledger;
- manual/reviewed extraction;
- timestamped signal or MarketIdea records;
- historical outcome reports where evidence supports them;
- legal/terms risk boundary.

## Scope Out

- private Telegram scraping;
- access-control bypass;
- paid X/Twitter dependency before validation;
- marketplace/leaderboard;
- investment advice or future-profit claims;
- contamination of Entropy Core evidence.

## Local Commands

```bash
python -m pip install -r requirements-dev.txt -e .
signal-sandbox --help
SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION=1 signal-sandbox transcribe-media --media-manifest docs/pilot/bablos79_MEDIA_MANIFEST.json --output-dir docs/pilot/transcripts --approve
python -m pytest tests/ -q
```
