# CODEX_PROMPT.md

Version: 1.33
Date: 2026-05-11
Phase: Phase 16

This file is the compact session state for AI development. Do not paste long
history here; use links below.

## Current Phase

- Phase: Phase 16
- Name: Artifact-First Real Audit Validation
- Business goal: produce a real-data Trader Risk Audit report pack that the
  operator trusts before external delivery.
- Phase gate: real scope, safe intake, complete artifact pack, manual
  validation, report polish, demo pack, and external pilot ready decision.

## Current State

- Baseline: 176 passing tests
- Ruff: clean (`ruff check` and `ruff format --check`)
- Last CI: workflow configured; remote run not observed from this clone
- Last updated: 2026-05-11
- Open findings: none
- Current priority: artifact-first validation, not more feature expansion

## Read First

1. `docs/ARTIFACT_VALIDATION_ROADMAP.md`
2. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
3. `docs/tasks.md` Phase 16, T63-T69
4. task-specific `Context-Refs` in `docs/tasks.md`

Other useful links:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/IMPLEMENTATION_CONTRACT.md`
- `docs/STARTER_POLICY_PROFILES_RU.md` for `soft`, `medium`, and `hard`
  starter audit presets
- Supporting cross-product cognition vault on this VPS:
  `/srv/codex-entropy/repos/product-3/engineering-cognition-vault/10-projects/entropy-protocol.md`.
  Product-local docs remain authoritative.

## Next Task

T63 - Real Audit Scope Lock

Use `docs/tasks.md#t63-real-audit-scope-lock` as the source of truth for
acceptance criteria and file scope.

Immediate intent:

- define the first real audit before implementation or report generation;
- record trade source, period, timezone, policy/rules, privacy boundary,
  allowed artifacts, report language, and delivery format;
- decide whether CSV/export intake is enough or the real run needs the minimum
  safe read-only exchange import work;
- keep raw private/customer trade data out of git.

## Active Guardrails

- T56-T62 remain planned/deferred. Run only the subset required by the selected
  real audit artifact.
- ADR-001 keeps Telegram as constrained demo/intake/delivery only.
- ADR-002 allows local read-only historical fill ingestion only.
- No SaaS accounts, checkout, exchange write APIs, broker control, order
  blocking, signal analytics, AI advice, or live trading behavior.

## Historical Pointers

- Completed through T55; details are in `docs/IMPLEMENTATION_JOURNAL.md`,
  `docs/EVIDENCE_INDEX.md`, `docs/archive/`, and `docs/tasks.md`.
- Public sample and starter profile context lives in
  `docs/PUBLIC_SAMPLE_EVIDENCE_RU.md`,
  `docs/INTERNAL_VALIDATION_REVIEW_RU.md`, and
  `docs/STARTER_POLICY_PROFILES_RU.md`.
- Phase 16 supersedes the previous Binance next-task routing for now.

## Maintenance Rule

At every phase boundary update only:

- current phase;
- baseline and validation status;
- next task;
- open findings;
- links if canonical docs move.

Do not append long task logs here.
