# Artifact-First Validation Roadmap

Status: Active operating overlay
Date: 2026-05-11

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
| Trader Risk Audit | First commercial wedge; validate a real trade audit report. | `products/trader-risk-audit/docs/tasks.md` Phase 16, T63-T69 |
| Signal Analytics Sandbox | Second report product; validate a real public-source research report. | `products/signal-analytics-sandbox/docs/tasks.md` Phase 21, SAS-AF-001..008 |
| Entropy Core | Internal artifact validity/reproducibility/no-claim support. | `products/entropy-core/docs/tasks.md` Phase 15, T69-T74 |

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
- Signal: `products/signal-analytics-sandbox/docs/ARTIFACT_VALIDATION_ROADMAP.md`
- Core: `products/entropy-core/docs/ARTIFACT_SUPPORT_ROADMAP.md`

## Done

This overlay is complete when Trader and/or Signal have manually validated real
report packs ready for controlled external conversations, and Core has only the
minimal shared validity support needed by those reports.
