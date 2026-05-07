# Entropy Protocol

**Status:** Product portfolio root
**Last updated:** 2026-05-07

Entropy Protocol is being developed as a product portfolio around governed
trading research, audit discipline, and trader workflow validation.

The root of the repository contains only the global direction. Product-specific
code, tests, migrations, documentation, audits, archives, task graphs, and
environment contracts live inside their own workspaces under `products/`.

## Product Workspaces

| Workspace | Path | Role |
|---|---|---|
| Entropy Core | `products/entropy-core/` | Governed protocol engine, code, tests, migrations, original docs, audits, archives, and reusable audit primitives |
| Trader Risk Audit | `products/trader-risk-audit/` | Primary commercial MVP: trade upload plus deterministic risk-rule violation audit |
| Signal Analytics Sandbox | `products/signal-analytics-sandbox/` | Separate validation sandbox for public Telegram/X signal-source analytics |

## Strategic Direction

Read these first:

1. `docs/PRODUCT_PORTFOLIO.md`
2. `docs/AI_DEVELOPMENT_OPERATING_MODEL.md`
3. `products/README.md`
4. Target workspace `README.md`
5. Target workspace `docs/CODEX_PROMPT.md`
6. Target workspace `docs/tasks.md`

## Current Priority

Validate Trader Risk Audit before building more core infrastructure:

> 3 paid audit reports from 10 qualified prospects within 14 days.

## Boundaries

The current product direction does not approve:

- live broker or exchange integration;
- order blocking;
- live capital;
- autonomous AI trading;
- private Telegram group scraping;
- public marketplace;
- unsupported OOS/performance claims.
