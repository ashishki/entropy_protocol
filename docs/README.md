# Entropy Protocol

**Status:** Product portfolio root
**Last updated:** 2026-05-15

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
2. `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
3. `docs/AI_DEVELOPMENT_OPERATING_MODEL.md`
4. `products/README.md`
5. Target workspace `README.md`
6. Target workspace `docs/CODEX_PROMPT.md`
7. Target workspace artifact roadmap when present
8. Target workspace `docs/tasks.md`

## Current Priority

Run artifact-first validation before broader product expansion. Current focus:

1. Trader Risk Audit: expand open-source/public/synthetic audit validation
   packs, then prepare private/operator-approved paid-pilot reports.
2. Signal Analytics Sandbox: expand the `bablos79` public corpus, add image/OCR
   and reviewed media evidence, build a claim ledger, and produce a balanced
   author capability retrospective.
3. Entropy Core: paused until Trader/Signal validation creates a concrete Core
   dependency or a human approves Core V2.

Payment and retention gates still matter, but the next operational blocker is
artifact correctness, readability, traceability, and claim safety.

## Boundaries

The current product direction does not approve:

- live broker or exchange integration;
- order blocking;
- live capital;
- autonomous AI trading;
- private Telegram group scraping;
- public marketplace;
- unsupported OOS/performance claims.
- Core V2 or public Core productization without a new human-approved roadmap.
