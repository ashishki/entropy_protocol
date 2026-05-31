# Entropy Core Workspace

Internal governed protocol, artifact-validity, evidence, and audit-bundle
kernel. Core is not the market-facing product, public SDK, or hosted service.

## Current Status

- Phase: 31 V2 Internal Kernel Review
- Next task: none - human gate required for next bounded Core V2 phase
- Baseline: 625 passing tests, 20 skipped
- Current priority: wait for the next bounded Core V2 human decision

## Role

Core should provide:

- no-claim boundary discipline;
- executable artifact validation;
- artifact registry, reproducibility, evidence packet, and governance
  primitives;
- research, product-profile, CAF, lineage, and audit-bundle schemas;
- report validity checklist and operator runbook;
- narrow product bridge notes;
- shared review templates where useful.

Core should not become a public SDK, hosted service, live execution layer,
runtime RAG system, product report owner, or generic platform during Core V2
internal kernel review.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/AI_LOOP_OPERATING_MODEL.md`
3. `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`
4. `docs/tasks.md` Phase 31, T135-T138
5. `docs/IMPLEMENTATION_CONTRACT.md`

## Active Guardrails

- holdout remains locked;
- live capital is not approved;
- broker/exchange execution is not approved;
- production credentials are not approved;
- OOS/performance claims are not approved;
- T66-T68 replay continuation is deferred unless explicitly reactivated.

## Scope In

- `src/entropy/` core primitives;
- tests and migrations;
- append-only/evidence/no-claim contracts;
- artifact support contracts for product reports;
- product bridge docs when needed by Trader or Signal.
- artifact support review: `docs/audit/ARTIFACT_SUPPORT_REVIEW.md`.
- Core V1 surface freeze and runbook:
  `docs/core/CORE_V1_SURFACE_FREEZE.md`, `RUNBOOK.md`.

## Scope Out

- live broker/exchange integration;
- live capital;
- holdout reads or unlocks without explicit gate;
- public SaaS infrastructure;
- signal scraping;
- AI strategy execution;
- public Core productization;
- external compliance certification or enterprise SLA claims.

## Local Commands

Run from `products/entropy-core/`:

```bash
PYTHONPATH=src .venv/bin/python -m pytest tests -q --tb=short
.venv/bin/python -m ruff check src/entropy tests
.venv/bin/python -m ruff format --check src/entropy tests
.venv/bin/python -m pyright src/entropy
git diff --check
```
