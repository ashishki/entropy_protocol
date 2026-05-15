# Trader Risk Audit Workspace

Primary commercial wedge. A trader provides executed trades and written risk
rules; the product returns a deterministic post-trade audit report.

## Current Status

- Phase: 16 Artifact-First Real Audit Validation
- Next task: T63 Real Audit Scope Lock
- Baseline: 176 passing tests, 0 skipped
- Current priority: validate one real audit report artifact before more feature
  expansion

## Promise

Upload/export trades plus rules. Receive a report showing:

- which rules were violated;
- when violations happened;
- source rows behind each finding;
- P&L associated with violations;
- limitations and unsupported checks.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/ARTIFACT_VALIDATION_ROADMAP.md`
3. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
4. `docs/tasks.md` Phase 16, T63-T69
5. `docs/STARTER_POLICY_PROFILES_RU.md`

## Implemented Surface

- local deterministic audit CLI;
- canonical trade schema and CSV import;
- risk policy schema and policy review packet;
- rule evaluation and violation records;
- P&L attribution;
- Markdown report generator;
- claim guard and artifact manifest;
- Telegram-ready local delivery packet;
- pilot/demo artifacts and operator runbook;
- fixture-backed read-only exchange import core;
- Bybit fixture-backed import path;
- Binance signing helper through current tested state.

Historical detail lives in `docs/IMPLEMENTATION_JOURNAL.md`,
`docs/EVIDENCE_INDEX.md`, `docs/archive/`, and `docs/tasks.md`.

## Artifact-First Work

Active phase tasks:

- T63 real audit scope lock;
- T64 real data intake and policy mapping;
- T65 first real audit artifact run;
- T66 manual calculation validation;
- T67 report polish and claim safety;
- T68 internal demo pack;
- T69 external pilot ready gate.

## Starter Profiles

`docs/STARTER_POLICY_PROFILES_RU.md` defines `soft`, `medium`, and `hard`
starter profiles. They are customizable internal validation defaults, not
trading advice.

## Scope In

- manual/concierge pilot reports;
- local trade export normalization;
- written risk policy input;
- deterministic violation evaluation;
- traceable report artifacts;
- local read-only historical import only when needed for the artifact.

## Scope Out

- live broker/exchange control;
- order placement/cancellation;
- withdrawals, transfers, leverage/margin mutation;
- order blocking;
- trading advice;
- strategy generation;
- full SaaS dashboard;
- signal analytics.

## Local Commands

```bash
.venv/bin/python -m pytest tests -q --tb=short
.venv/bin/ruff check trader_risk_audit tests
.venv/bin/ruff format --check trader_risk_audit tests
```
