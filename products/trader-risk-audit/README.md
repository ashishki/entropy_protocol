# Trader Risk Audit Workspace

Primary commercial wedge. A trader provides executed trades and written risk
rules; the product returns a deterministic post-trade audit report.

## Current Status

- Phase: 22 Conditional Real Read-Only Import deferred by T93
- Next task: none; T94-T97 are blocked until future market evidence reopens T93
- Baseline: 253 passing tests, 0 skipped
- Current priority: automate the pilot validation loop before hosted SaaS or
  checkout work
- Last completed: T93 CSV Friction Decision Gate

## Promise

Upload/export trades plus rules. Receive a report showing:

- which rules were violated;
- when violations happened;
- source rows behind each finding;
- P&L associated with violations;
- limitations and unsupported checks.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/AUTOMATED_PILOT_ROADMAP.md`
3. `docs/tasks.md` Phase 22, T93-T97
4. `docs/IMPLEMENTATION_CONTRACT.md`
5. `docs/PILOT_INTAKE_CONTRACT_RU.md`
6. `docs/ARTIFACT_VALIDATION_ROADMAP.md`
7. `docs/STARTER_POLICY_PROFILES_RU.md`

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
- Binance fixture-backed import path;
- exchange import runbooks, safety guidance, and evidence fields;
- automated local intake session, CSV schema profile, and intake report;
- structured rule catalog, generated policy builder, rule-builder flow, and
  unsupported-rule register;
- local audit session runner with safe run status;
- local artifact bundle index and safe bundle summary CLI;
- automated audit session reproducibility gate;
- claim-safe redacted report preview model and CLI;
- manual paid-pilot CTA, preview events, and local unlock boundary.
- hypothesis funnel event schema, legacy evidence loader, and local evidence
  dashboard CLI;
- privacy-safe hypothesis evidence export.

Historical detail lives in `docs/IMPLEMENTATION_JOURNAL.md`,
`docs/EVIDENCE_INDEX.md`, `docs/archive/`, and `docs/tasks.md`.

## Automated Pilot Work

Active phase plan:

- Phase 17, T70-T73: automated intake session, CSV schema profiler,
  actionable intake report, and deep review (complete);
- Phase 18, T74-T78: structured rule builder from supported deterministic
  rules (complete);
- Phase 19, T79-T82: one-click local audit runner and artifact bundle
  (complete);
- Phase 20, T83-T87: claim-safe preview and paid pilot CTA (complete);
- Phase 21, T88-T92: hypothesis evidence dashboard (complete);
- Phase 22, T93-T97: conditional real read-only import only if CSV friction
  evidence justifies it (T93 deferred; T94-T97 blocked).

Phase 16 SEC open-source artifact validation is complete and remains the demo
quality baseline, not paid/customer/PMF evidence.

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
