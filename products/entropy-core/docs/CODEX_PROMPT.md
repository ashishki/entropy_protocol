# CODEX_PROMPT.md

Version: 1.2
Date: 2026-05-11
Phase: 15

This file is compact session state for Entropy Core. Historical detail belongs
in `docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/audit/`,
and `docs/tasks.md`.

## Current Phase

- Phase: 15
- Name: Artifact Support Mode
- Business goal: support real report artifact validation for Trader Risk Audit
  and Signal Analytics Sandbox through minimal shared contracts, checklists,
  reproducibility guidance, bridge notes, and templates.
- Phase gate: Core improves product artifact trust without becoming a public
  product, hosted service, SDK, live execution path, holdout/OOS workflow, or
  broad platform distraction.

## Current State

- Phase: 15
- Baseline: 501 passing tests, 20 skipped
- Last local baseline detail: `.venv/bin/python -m pytest -q tests/` reported `501 passed, 20 skipped`
- Ruff: clean on T65 local verification 2026-05-09
- Pyright: clean on T65 local verification 2026-05-09
- Holdout: locked
- Live capital: not approved
- Broker/exchange integration: not approved
- OOS/performance claims: not approved
- Last updated: 2026-05-11
- Product hypothesis status: `local_evidence_strengthened_not_confirmed`

## Read First

1. `docs/ARTIFACT_SUPPORT_ROADMAP.md`
2. `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
3. `docs/tasks.md` Phase 15, T69-T74
4. task-specific `Context-Refs` in `docs/tasks.md`

Other useful links:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/core/`
- `docs/governance/`
- `docs/audit/`
- `docs/legacy/CORE_LEGACY_SUMMARY.md`

## Next Task

T69 Shared Artifact Contract Freeze.

Use `docs/tasks.md#t69-shared-artifact-contract-freeze` as the source of truth
for acceptance criteria and file scope.

Current active task is T69 Shared Artifact Contract Freeze.

## Active Guardrails

- T66-T68 remain pending but deferred by the 2026-05-11 artifact-support
  priority override.
- The only current approval is `local_broker_sandbox_no_capital_replay` with
  maximum effect `local_no_effect_only`.
- Real external side effects, holdout reads, holdout unlocks, live order
  placement, live capital actions, live broker/exchange execution, production
  credential loading, credentialed production deployment, and external sandbox
  order emission from code remain blocked.
- No public SDK, hosted service, holdout/OOS expansion, live execution path, or
  generic platform work without a new explicit human decision.

## Historical Anchors

This compact section intentionally keeps only phrases that state tests and
orchestrators use as anchors. Full detail is in the linked docs above.

- T14 Reset Strategy Closure Review completed.
- T19 First Research Packet Review completed.
- Human decision required after T19.
- T24 Archive Evidence Expansion Review completed.
- Human decision required after T24.
- First Research Evidence Packet block complete through T19.
- Archive Evidence Expansion block complete through T24.
- T26 Archive Packet Replay Contract completed.
- T27 Evidence Hash Reproducibility Matrix completed.
- T28 No-Claim Surface Regression Sweep completed.
- T29 Archive Reproducibility Hardening Review completed.
- T30 Archive Evidence Sufficiency Gap Matrix completed.
- T31 Phase-Gate Readiness Packet Scaffold completed.
- T32 Approval Boundary Checklist completed.
- T33 Readiness No-Holdout Dry Run completed.
- T34 Phase-Gate Readiness Review completed.
- T35 Holdout Access Protocol Deny-By-Default Contract completed.
- T36 Holdout Approval Event Schema Contract completed.
- T37 Holdout Access Audit Logging Contract completed.
- T38 Holdout Leakage Guard Protocol Fixture completed.
- T39 Holdout Access Protocol Review completed.
- T40 Holdout Approval Request Packet Scaffold completed.
- T41 Holdout Approval Evidence Intake Contract completed.
- T45 Holdout Approval Decision Review completed.
- T46 Live-Feed Boundary Contract completed.
- T50 Live-Feed Dry Run Readiness Review completed.
- T51 Broker Sandbox Boundary Contract completed.
- T56 Broker Sandbox Readiness Review completed.
- T62 Product Hypothesis Confirmation Decision Review completed.
- T63 Local Broker Sandbox Replay Approval Event completed.
- T64 Broker Sandbox No-Capital Replay Primitive completed.
- T65 Broker Sandbox Replay Evidence Packet completed.

Phase anchors:

- Phase 8 is complete through T34.
- Phase 8 Phase-Gate Readiness Review.
- Phase 9 complete through T39.
- Phase 9 is protocol-only holdout access design.
- Phase 9 Holdout Access Protocol.
- Phase 10 complete through T45.
- Phase 10 Holdout Approval Decision Packet.
- Phase 11 is local-only live-feed dry-run readiness.
- Phase 11 Live-Feed Dry Run Readiness.
- Phase 12 is sandbox-only broker/exchange execution risk audit.
- Phase 12 Broker Sandbox and Execution Risk Audit.
- Phase 13 is local-only approval decision work.
- Phase 14 replay work is complete through T65.
- Phase 15 is artifact support mode for product report validation.
- product hypothesis status: unconfirmed_pending_future_validation.
- no approval event currently exists.
- no holdout, no broker/exchange execution, no order placement, no live capital,
  and no production credentials are approved.
- no holdout access is approved.
- live order placement is blocked.
- production credential loading is blocked.
- capital-ready claims are blocked.
- the only current approval is local_broker_sandbox_no_capital_replay.
- holdout, live feeds, broker/exchange, production, capital-ready, and OOS/performance remain unapproved.
- holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, and OOS/performance remain unapproved.

## Maintenance Rule

At every phase boundary update only:

- current phase;
- baseline and validation status;
- next task;
- open findings;
- guardrail changes;
- links if canonical docs move.

Do not append long completed-task logs here.
