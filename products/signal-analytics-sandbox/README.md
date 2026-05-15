# Signal Analytics Sandbox Workspace

Report-product candidate for public Telegram/X-style source analytics. It is
separate from Entropy Core and Trader Risk Audit.

## Current Status

- Phase: 22 Expanded Public Corpus
- Next task: SAS-DR-001 Deep Retrospective Scope Lock
- Baseline: 166 passing tests, 0 skipped
- Current priority: expand the `bablos79` public corpus, add image/OCR
  coverage, build a reviewed claim ledger, and produce a balanced author
  capability retrospective

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
6. `docs/tasks.md` Phase 22, SAS-DR-001..005
7. `docs/legal_risk_memo.md`

## Implemented Surface

- source manifests and public capture workflows;
- signal/MarketIdea schemas and review queues;
- local market-data snapshots and deterministic horizon metrics;
- Author Market Intelligence flow;
- report exports;
- media artifact metadata, transcript/OCR draft paths, and multimodal source
  joins;
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

Active phase plan:

- Phase 22, SAS-DR-001..005: expanded public corpus, source-window lock,
  capture manifest, media inventory, corpus gap register, and deep review;
- Phase 23, SAS-DR-006..011: image acquisition, OCR draft run, image/chart
  review queue, transcript acceptance policy, multimodal source join v2, and
  deep review;
- Phase 24, SAS-DR-012..017: author claim taxonomy, expanded claim ledger,
  market proxy map, retrospective outcomes, counterexample register, and deep
  review;
- Phase 25, SAS-DR-018..022: author capability scorecard, report V1, demo
  pack, external ready gate, and deep review.

The current `bablos79` Phase 21 result is a narrow-window reject case, not a
final judgment on the channel.

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
