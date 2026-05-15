# Artifact-First Validation Roadmap

Status: Active operating overlay
Date: 2026-05-15

This is the portfolio-level routing document for the next AI development loop.
It keeps the active context small; detailed task scope lives in each product's
`docs/tasks.md`.

## Decision

Warm demand/pre-order interest exists. The next blocker is not abstract demand
validation. The next blocker is proving that real reports are correct,
readable, traceable, and safe enough for the operator to show externally.

Operating sequence:

```text
real input -> deterministic artifact -> manual validation -> polished pack -> controlled pilot
```

## Product Roles

| Product | Active Role | Active Task Source |
|---|---|---|
| Trader Risk Audit | First commercial wedge; expand open-source/public audit validation, then private-pilot readiness. | `products/trader-risk-audit/docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`; `products/trader-risk-audit/docs/tasks.md` Phase 23, T98-T103 |
| Signal Analytics Sandbox | Second report product; deep public-channel retrospective with media/OCR, claim ledger, and outcomes. | `products/signal-analytics-sandbox/docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`; `products/signal-analytics-sandbox/docs/tasks.md` Phase 22, SAS-DR-001..005 |
| Entropy Core | Paused internal artifact validity/reproducibility/no-claim support. | No active task; wait for concrete Trader/Signal dependency or human-approved Core V2 roadmap. |

## Phase Map

| Phase | Purpose | Output |
|---|---|---|
| 0 | Lock real input scope and evidence rules. | Scope note, privacy boundary, allowed claims. |
| 1 | Intake real data/public sources safely. | Manifest/source refs, unsupported-field register. |
| 2 | Generate first real artifact. | Report, manifest, delivery packet or source pack. |
| 3 | Manually validate truth. | Validation notes and error register. |
| 4 | Polish report and claim language. | Operator-trusted report pack. |
| 5 | Package internal demo. | Safe excerpts, talk track, pilot-ready pack. |
| 6 | Controlled external pilot. | Feedback log and paid pilot decision. |

## Guardrails

Do not add these before artifact validity is proven:

- public SaaS UI;
- live broker/exchange control;
- order placement, order blocking, withdrawals, transfers, leverage/margin mutation;
- private Telegram scraping;
- paid X/Twitter dependency;
- signal marketplace or leaderboard;
- AI trading advice or future-performance claims;
- public Core SDK or hosted Core service.

## Read Order For AI Sessions

1. `docs/README.md`
2. `docs/PRODUCT_PORTFOLIO.md`
3. this file
4. target product `README.md`
5. target product `docs/CODEX_PROMPT.md`
6. target product artifact roadmap
7. target product `docs/tasks.md`

## Product Roadmap Links

- Trader: `products/trader-risk-audit/docs/ARTIFACT_VALIDATION_ROADMAP.md`
- Trader active route:
  `products/trader-risk-audit/docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
- Signal: `products/signal-analytics-sandbox/docs/ARTIFACT_VALIDATION_ROADMAP.md`
- Signal active route:
  `products/signal-analytics-sandbox/docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`
- Core: `products/entropy-core/docs/ARTIFACT_SUPPORT_ROADMAP.md`

## 2026-05-15 Focus Update

The active development focus is Product 1 and Product 2 only:

- Product 1 / Trader Risk Audit needs more open-source/public validation packs
  and then safe private/operator-approved pilot reports.
- Product 2 / Signal Analytics Sandbox needs a larger `bablos79` corpus,
  image/OCR coverage, reviewed media evidence, claim ledger, market outcomes,
  and a balanced author capability report.
- Product 3 / Entropy Core is paused. Do not reopen Core roadmap work unless a
  product validation task creates a concrete Core dependency or a human approves
  Core V2.

## Done

This overlay is complete when Trader and/or Signal have manually validated real
report packs ready for controlled external conversations, and Core has only the
minimal shared validity support needed by those reports.
