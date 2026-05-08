# Signal Analytics Sandbox Workspace

Purpose:

Validate whether public Telegram/X signal-source analytics is a paid product
wedge separate from Entropy Core and Trader Risk Audit.

## Current Status

- Phase 0 gates are acknowledged for the initial Telegram pilot sources.
- Engineering Phases 1-8 are complete through T20.
- Phase 9 pilot loop is complete; 60 public `bablos79` text captures now exist
  in `workspace/captures/bablos79/`.
- Current direction: Phase 10 machine-first draft extraction with pseudo-labels,
  deterministic validators, author profile discovery, and exception review.
- Package target: Python 3.12, installable as `signal-sandbox`.
- CLI status: `signal-sandbox` exists with stubs for the planned operator workflow.
- Tests: 84 passing; ruff and pyright pass locally.

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
5. `../../docs/PRODUCT_PORTFOLIO.md`
6. `../../docs/AI_DEVELOPMENT_OPERATING_MODEL.md`

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
