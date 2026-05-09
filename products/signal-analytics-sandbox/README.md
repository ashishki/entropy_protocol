# Signal Analytics Sandbox Workspace

Purpose:

Validate whether public Telegram/X signal-source analytics is a paid product
wedge separate from Entropy Core and Trader Risk Audit.

## Current Status

- Phase 0 gates are acknowledged for the initial Telegram pilot sources.
- Engineering Phases 1-19 are complete through `SAS-MI-019`.
- Phase 20 is planned for Telegram media evidence: voice/audio transcription
  drafts and image/OCR drafts.
- Phase 9 pilot loop is complete; 60 public `bablos79` text captures exist in
  `workspace/captures/bablos79/`.
- Phase 10 produced draft-only pseudo-labels, an author profile, deterministic
  draft validation/parser/export helpers, a 60-row draft export, a 23-row
  exception review queue, and an evaluation decision to keep the helper only
  for internal exception review.
- Author Market Intelligence is active. Phase 10 artifacts remain the first
  channel profile/corpus seed; implemented work now includes asset registry,
  immutable local market-data store, deterministic horizon metrics, source
  corpus, channel profiles, local retrieval, MarketIdea extraction/export,
  deterministic thesis evaluation, author metrics, bounded internal analyst
  memo export, Author Market Report V0, the sellability decision gate,
  ADR-003, and the reviewer coverage export pack.
- Current next engineering task: `SAS-MEDIA-001: Media Scope ADR And Legal Addendum`.
- Package target: Python 3.12, installable as `signal-sandbox`.
- CLI status: `signal-sandbox` exists with stubs for the planned operator workflow.
- Tests: 141 passing; ruff and pyright pass locally.

## Scope In

- Public source ledger.
- Manual signal extraction.
- Timestamped signal record.
- Historical signal outcome report.
- Legal/terms risk memo.

Initial pilot sources:

- https://t.me/bablos79
- https://t.me/nemphiscrypts
- https://t.me/pifagortrade

## Scope Out

- Private Telegram group scraping.
- Scraping behind access controls.
- Paid X API dependence before validation.
- Signal marketplace.
- Claims that signals are investment advice.
- Contamination of Entropy Core evidence.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/tasks.md`
3. `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md`
4. `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`
5. `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`
6. `docs/pilot/MEDIA_MODALITY_DEVELOPMENT_PLAN.md`
7. `../../docs/PRODUCT_PORTFOLIO.md`
8. `../../docs/AI_DEVELOPMENT_OPERATING_MODEL.md`

## Local AI Workflow

This workspace has its own `PLAYBOOK.md`, `prompts/`, `templates/`, `hooks/`,
`ci/`, prompts, hooks, and Codex tmux operating materials. Do not rely on root-level workflow files or legacy nested-agent assumptions
for Signal Analytics Sandbox development.

## Local Commands

```bash
python -m pip install -r requirements-dev.txt -e .
signal-sandbox --help
python -m pytest tests/ -q
```

## CI

- Product workflow template: `.github/workflows/ci.yml`
- Repository-root GitHub workflow bridge:
  `../../.github/workflows/signal-analytics-sandbox-ci.yml`
