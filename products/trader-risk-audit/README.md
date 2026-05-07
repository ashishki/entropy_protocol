# Trader Risk Audit Workspace

Purpose:

Primary commercial MVP. A trader uploads executed trades and written risk rules.
The system reports deterministic rule violations and their P&L impact.

## Core Promise

Upload trades plus rules. Receive an audit report showing what rules were
violated, when they were violated, and how much damage violations created.

## Scope In

- Manual pilot reports.
- Trade export normalization.
- Risk policy input.
- Deterministic violation evaluation.
- Violation attribution.
- Markdown/PDF/Telegram-ready report packets.

## Scope Out

- Live broker/exchange APIs.
- Order blocking.
- Full SaaS dashboard.
- Strategy backtesting platform.
- AI-generated trading strategies.
- Public marketplace.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/tasks.md`
3. `../../docs/PRODUCT_PORTFOLIO.md`
4. `../../docs/AI_DEVELOPMENT_OPERATING_MODEL.md`

## Local AI Workflow

This workspace has its own `PLAYBOOK.md`, `prompts/`, `templates/`, `hooks/`,
`ci/`, and `.claude/` configuration. Do not rely on root-level workflow files
for Trader Risk Audit development.
