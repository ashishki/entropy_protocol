# Entropy Core Workspace

Purpose:

Maintain the governed protocol engine and reusable audit primitives without
weakening existing research discipline.

This workspace is not a separate commercial application. It is the protocol-safe
foundation that future product surfaces may call only through approved bridges.

## Scope In

- Core package code under `src/entropy/`.
- Core tests under `tests/`.
- Core migrations under `migrations/`.
- Trial Registry bridge design.
- Append-only audit event contracts.
- Deterministic report primitives.
- Risk policy and violation record contracts if validated by Trader Risk Audit.
- Human-gated hypothesis/backtest bridge design.

## Scope Out

- Live broker or exchange integration.
- Live capital.
- Public SaaS infrastructure.
- Signal scraping.
- AI-generated strategy execution.
- Any OOS or performance claim outside the root evaluation protocol.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/tasks.md`
3. `../../docs/PRODUCT_PORTFOLIO.md`
4. `docs/IMPLEMENTATION_CONTRACT.md`

## Local Commands

Run these from `products/entropy-core/`:

```bash
.venv/bin/python -m pytest -q tests/
.venv/bin/python -m ruff check src/entropy tests
.venv/bin/python -m pyright src/entropy
```

## Local AI Workflow

This workspace has its own `PLAYBOOK.md`, `prompts/`, `templates/`, `hooks/`,
`ci/`, and `.claude/` configuration. Do not rely on root-level workflow files
for core development.
