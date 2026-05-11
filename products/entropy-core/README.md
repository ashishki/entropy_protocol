# Entropy Core Workspace

Internal governed protocol and artifact-validity foundation. Core is not the
market-facing product in the current cycle.

## Current Status

- Phase: 15 Artifact Support Mode
- Next task: T69 Shared Artifact Contract Freeze
- Baseline: 501 passing tests, 20 skipped
- Current priority: support Trader/Signal report validity with minimal shared
  contracts and checklists

## Role

Core should provide:

- no-claim boundary discipline;
- artifact/reproducibility conventions;
- report validity checklist;
- narrow product bridge notes;
- shared review templates where useful.

Core should not become a public SDK, hosted service, live execution layer, or
generic platform during artifact validation.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/ARTIFACT_SUPPORT_ROADMAP.md`
3. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
4. `docs/tasks.md` Phase 15, T69-T74
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

## Scope Out

- live broker/exchange integration;
- live capital;
- holdout reads or unlocks without explicit gate;
- public SaaS infrastructure;
- signal scraping;
- AI strategy execution;
- public Core productization.

## Local Commands

Run from `products/entropy-core/`:

```bash
PYTHONPATH=src .venv/bin/python -m pytest tests -q --tb=short
.venv/bin/python -m ruff check src/entropy tests
.venv/bin/python -m ruff format --check src/entropy tests
.venv/bin/python -m pyright src/entropy
git diff --check
```
