# Signal Analytics Sandbox Workspace

Report-product candidate for public Telegram/X-style source analytics. It is
separate from Entropy Core and Trader Risk Audit.

## Current Status

- Phase: 21 Artifact-First Real Public-Source Report Validation
- Next task: SAS-AF-001 Channel And Report Scope Lock
- Baseline: 157 passing tests, 0 skipped
- Current priority: validate one real public-source report artifact

## Promise

Analyze a public source/channel and produce a bounded research report covering
source evidence, reviewed market ideas/signals, ambiguity, historical outcomes
where supported, and limitations.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/ARTIFACT_VALIDATION_ROADMAP.md`
3. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
4. `docs/tasks.md` Phase 21, SAS-AF-001..008
5. `docs/legal_risk_memo.md`

## Implemented Surface

- source manifests and public capture workflows;
- signal/MarketIdea schemas and review queues;
- local market-data snapshots and deterministic horizon metrics;
- Author Market Intelligence flow;
- report exports;
- media artifact metadata, transcript/OCR draft paths, and multimodal source
  joins;
- reviewer coverage pack for existing `bablos79` corpus.

Historical detail lives in `docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`,
`AGENT_NOTES.md`, and `docs/tasks.md`.

## Artifact-First Work

Active phase tasks:

- SAS-AF-001 source/report scope lock;
- SAS-AF-002 public capture pack;
- SAS-AF-003 human review queue closure;
- SAS-AF-004 market data/outcome prep;
- SAS-AF-005 first real report;
- SAS-AF-006 manual validity review;
- SAS-AF-007 internal demo pack;
- SAS-AF-008 external pilot ready gate.

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
python -m pytest tests/ -q
```
