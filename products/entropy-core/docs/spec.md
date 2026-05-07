# Specification - Entropy Core

Version: 1.0
Last updated: 2026-05-07
Status: Draft after governance reset

---

## Overview

Entropy Core provides a local, human-gated, deterministic research and audit primitive layer. It stabilizes the existing registry, data, leakage, SimBroker, attribution, governance, and evidence/report surfaces so product workspaces can reuse protocol-safe primitives without importing live execution or unsupported claim risk.

## User Roles

| Role | Capabilities |
|------|--------------|
| Founder/operator | Runs local commands, approves gates, manages registry/evidence, and decides phase transitions. |
| Internal research engineer | Implements deterministic research/evidence features under task contracts. |
| Product workspace developer | Consumes approved Core primitives through bridge contracts only. |
| Reviewer | Checks code, tests, evidence, no-claim boundaries, and phase-gate readiness. |

## Feature Area 1 - Existing Codebase Baseline

Description: Establish the reset baseline over current `src/entropy`, `tests`, `migrations`, Python 3.12 tooling, and product-local CI.

Acceptance criteria:

1. The package imports under Python 3.12.
2. `pyproject.toml` requires Python 3.12 and configures ruff for py312.
3. Local verification commands for pytest, ruff, ruff format, and pyright are documented in `docs/CODEX_PROMPT.md`.
4. The first reset task records the actual test baseline.

Out of scope for v1:

- Rewriting package layout.
- Deleting historical evidence.

## Feature Area 2 - Registry and Governance Integrity

Description: Preserve and harden append-only registry/governance behavior, readiness checks, human approval gates, and no-mutation rules.

Acceptance criteria:

1. Trial/research object writes reject missing hashes before persistence.
2. Registry and governance event tables have no application UPDATE or DELETE path.
3. Human approval is required before admissible state transitions.
4. Readiness failures return named structured reasons.

Out of scope for v1:

- Multi-user auth.
- Public registry service.

## Feature Area 3 - Data and Leakage Controls

Description: Keep historical data workflows deterministic, locally reproducible, and blocked from claim escalation until leakage/holdout gates pass.

Acceptance criteria:

1. Data hashes are deterministic across row-order changes.
2. Local data workflows do not require external egress by default.
3. Leakage checks block OOS/performance labels when required evidence is absent.
4. Holdout read/unlock remains human-gated.

Out of scope for v1:

- Live feeds by default.
- Broker/exchange integration.

## Feature Area 4 - SimBroker and Attribution

Description: Preserve deterministic cost/fill simulation and P&L attribution while preventing unsupported performance conclusions.

Acceptance criteria:

1. SimBroker costs and fills are reproducible for identical inputs.
2. P&L streams remain separated according to protocol rules.
3. Reports mark scaffold/archive-only outputs with no-claim labels.
4. Attribution evidence references tests, fixtures, and report artifacts.

Out of scope for v1:

- Live order routing.
- Capital-ready labels.

## Feature Area 5 - Evidence and Reports

Description: Generate deterministic evidence/report packets that connect inputs, code, policy, data, run ids, hashes, tests, and human gates.

Acceptance criteria:

1. Evidence packets include input hashes, code hash, policy hash, relevant task ids, and report artifact paths.
2. `docs/EVIDENCE_INDEX.md` points to real artifacts and does not claim authority over canonical proof.
3. Reports avoid OOS/performance/production/capital-ready claims unless a specific gate authorizes them.

Out of scope for v1:

- Customer-facing SaaS dashboards.
- External attestation products.

## Feature Area 6 - Product Bridge Contracts

Description: Define safe contracts for product workspaces, especially Trader Risk Audit, to reuse Core primitives without opening live trading or claim surfaces.

Acceptance criteria:

1. Bridge contracts identify allowed Core primitives, forbidden calls, input/output schemas, and human approval boundaries.
2. Trader Risk Audit risk policy and violation record primitives are deterministic and do not depend on runtime LLM behavior.
3. Product bridge tests prove downstream imports do not bypass no-live/no-claim boundaries.

Out of scope for v1:

- Direct product workspace database access without a bridge.
- Live risk guard or broker control.

## Feature Area 7 - Hypothesis/Backtest Bridge Design

Description: Design, but do not silently activate, a human-gated path from research drafts to admissible registry/evaluation objects.

Acceptance criteria:

1. Draft hypotheses cannot enter evaluation without human registration.
2. No AI-generated strategy can write registry truth or gate decisions.
3. Bridge design records holdout, leakage, and claim boundaries.

Out of scope for v1:

- Autonomous strategy discovery.
- Runtime agent planning.
