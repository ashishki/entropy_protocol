# Entropy Core Workspace

Purpose:

Maintain the governed protocol engine and reusable audit primitives without
weakening existing research discipline.

This workspace is not a separate commercial application. It is the protocol-safe
foundation that future product surfaces may call only through approved bridges.

## Current Status

Phase 14 Local Broker Sandbox No-Capital Replay Extension is active.

The product hypothesis status is `local_evidence_strengthened_not_confirmed`.
The current approval is scoped only to `local_broker_sandbox_no_capital_replay`
with maximum effect `local_no_effect_only`. This workspace has no approval for
live orders, broker or exchange execution, production credentials, live capital,
holdout reads, external sandbox order emission from code, or OOS/performance
claims.

## Scope In

- Core package code under `src/entropy/`.
- Core tests under `tests/`.
- Core migrations under `migrations/`.
- Trial Registry bridge design.
- Append-only audit event contracts.
- Deterministic report primitives.
- Risk policy and violation record contracts if validated by Trader Risk Audit.
- Human-gated hypothesis/backtest bridge design.
- Local-only approval decision packets and audit reviews.
- Broker sandbox fixture, execution risk, kill switch, and no-capital dry-run
  contracts.

## Scope Out

- Live broker or exchange integration.
- Live capital.
- Production credential loading.
- Holdout reads or unlocks without an explicit gate.
- Public SaaS infrastructure.
- Signal scraping.
- AI-generated strategy execution.
- Product hypothesis confirmation claims without future validation evidence.
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
.venv/bin/python -m ruff format --check src/entropy tests
.venv/bin/python -m pyright src/entropy
git diff --check
```

## Local AI Workflow

This workspace has its own `PLAYBOOK.md`, `prompts/`, `templates/`, `hooks/`,
`ci/`, and `.claude/` configuration. Do not rely on root-level workflow files
for core development.

Before continuing orchestration work, read `CODEX_LOOP.md` and
`prompts/ORCHESTRATOR.md`. Keep work local to this product workspace and do not
use nested Codex sessions or `codex exec`.
