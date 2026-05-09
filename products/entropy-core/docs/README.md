# Entropy Core Documentation

**Last updated:** 2026-05-09
**Status:** Active core workspace

This directory contains the original governed Entropy Protocol documentation:
core protocol docs, architecture, implementation contract, task graph, audit
surface, evidence index, historical archives, and practitioner briefs.

Global product strategy now lives at repository root:

- `docs/README.md`
- `docs/PRODUCT_PORTFOLIO.md`
- `docs/AI_DEVELOPMENT_OPERATING_MODEL.md`

## What This Workspace Is

Entropy Core is a systematic capital-allocation research governance framework.

It is not:

- a trading bot;
- a signal generator;
- live broker or exchange infrastructure;
- live capital infrastructure;
- autonomous AI trading.

It provides:

- walk-forward evaluation infrastructure with strict IS/OOS separation;
- Trial Registry and multiplicity control;
- SimBroker cost and slippage modeling;
- P&L attribution;
- governance state machine;
- phase-gate evidence;
- append-only governance and registry discipline.

## Documentation Map

| Area | Path | Purpose |
|---|---|---|
| Core protocol | `core/` | Charter, protocol spec, glossary, evolution |
| Architecture | `ARCHITECTURE.md`, `architecture/` | Active implementation architecture and layered system docs |
| Feature spec | `spec.md` | Current supported behavior and scope |
| Task graph | `tasks.md` | Core implementation task graph |
| Handoff | `CODEX_PROMPT.md` | Current core session state |
| Contract | `IMPLEMENTATION_CONTRACT.md` | Immutable implementation rules |
| Governance | `governance/` | Research firewall, readiness gate, governor |
| Approvals | `approvals/` | Human approval requests, intake contracts, and validation decisions |
| Protocol contracts | `protocols/` | Boundary contracts for broker sandbox, risk controls, and dry-run execution |
| Audit | `audit/` | Current audit prompts, findings, review reports |
| Archive | `archive/`, `audit/archive/` | Historical state and audit packets |
| Audience | `audience/` | External practitioner and architecture briefs |
| Research | `research/` | Literature-backed research reports |

## Reading Order

For core implementation work:

1. `CODEX_PROMPT.md`
2. `tasks.md`
3. `IMPLEMENTATION_CONTRACT.md`
4. Relevant architecture/spec/governance docs for the task

For product-level work, start from root `docs/README.md` and the target
workspace under `products/`.

## Current Boundary

Phase 13 Product Hypothesis Confirmation Decision is complete. The current
product hypothesis status is `unconfirmed_pending_future_validation`.

The only recommended next validation path is a future human-approved local
broker sandbox no-capital replay extension. Holdout, production/capital-ready
labels, live feeds, broker or exchange execution, production credential loading,
Growth/RDL/RBE activation, and OOS/performance claims remain blocked unless a
separate explicit core gate opens them.
