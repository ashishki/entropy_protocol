# Signal Analytics Sandbox Workspace

Report-product candidate for public Telegram/X-style source analytics. It is
separate from Entropy Core and Trader Risk Audit.

## Current Status

- Phase: 21 Artifact-First Real Public-Source Report Validation, archived
- Next task: decide whether the LLM-reviewed internal report is sufficient for
  demo or add operator/human acceptance for external delivery
- Baseline: 166 passing tests, 0 skipped
- Current priority: external delivery remains rejected for the current
  `bablos79` source/window until usable reviewed media evidence exists

## Promise

Analyze a public source/channel and produce a bounded research report covering
source evidence, reviewed market ideas/signals, ambiguity, historical outcomes
where supported, and limitations.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/ARTIFACT_VALIDATION_ROADMAP.md`
3. `docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md`
4. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
5. `docs/tasks.md` Phase 21
6. `docs/legal_risk_memo.md`

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
