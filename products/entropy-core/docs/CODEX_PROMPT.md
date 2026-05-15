# CODEX_PROMPT.md

Version: 2.7
Date: 2026-05-15
Phase: 27

This file is compact session state for Entropy Core. Historical detail belongs
in `docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/audit/`,
and `docs/tasks.md`.

## Current Phase

- Phase: 27
- Name: Core V1 Productization
- Business goal: freeze and document the Core V1 internal product kernel,
  runbooks, examples, and final review without public SaaS/compliance claims.
- Phase gate: Core is a documented, tested internal product kernel ready for
  V2 planning, with automatic roadmap expansion stopped after T122.

## Current State

- Phase: 27
- Baseline: 625 passing tests, 20 skipped
- Last local baseline detail: `.venv/bin/python -m pytest -q tests/` reported `625 passed, 20 skipped`
- Phase 16 baseline detail: `.venv/bin/python -m pytest -q tests/` reported `23 failed, 487 passed, 20 skipped` before T75; after reset/state-doc sync reported `525 passed, 20 skipped`
- Ruff: clean on Core V1 final verification 2026-05-14
- Pyright: scoped artifact/db source clean on Core V1 final verification 2026-05-14; full pyright still has pre-existing test import-resolution errors
- Holdout: locked
- Live capital: not approved
- Broker/exchange integration: not approved
- OOS/performance claims: not approved
- Last updated: 2026-05-15
- Product hypothesis status: `local_evidence_strengthened_not_confirmed`
- Artifact support status: Phase 15 complete through T74; Core remains hidden/internal.
- Core execution roadmap status: Core V1 complete through T122; automatic roadmap expansion stopped pending human-approved V2 roadmap.
- Portfolio pause: Trader Risk Audit and Signal Analytics Sandbox are the
  active validation tracks; Core remains paused unless they create a concrete
  dependency or a human approves Core V2.

## Read First

1. `docs/AI_LOOP_OPERATING_MODEL.md`
2. `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`
3. `docs/tasks.md` Phase 27, T119-T122
4. `docs/IMPLEMENTATION_CONTRACT.md`
5. task-specific `Context-Refs` in `docs/tasks.md`

Other useful links:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/core/`
- `docs/governance/`
- `docs/audit/`
- `docs/legacy/CORE_LEGACY_SUMMARY.md`

## Next Step

Human gate: approve or reject a Core V2 roadmap.

The T75-T122 execution roadmap is complete. Do not continue into new roadmap
tasks until a human approves a Core V2 roadmap.
Do not open Core work from portfolio/product validation discussions unless the
operator explicitly changes this pause.

## Active Guardrails

- T66-T68 remain pending but deferred by the 2026-05-11 artifact-support
  priority override.
- T69-T74 artifact-support docs are complete; this does not approve product
  workspace edits from Core, public SDK work, hosted service work, or
  product-specific report ownership.
- T75-T122 define the completed Core execution roadmap. Agents must not
  auto-open new roadmap tasks until a human approves a Core V2 roadmap.
- The only current approval is `local_broker_sandbox_no_capital_replay` with
  maximum effect `local_no_effect_only`.
- Real external side effects, holdout reads, holdout unlocks, live order
  placement, live capital actions, live broker/exchange execution, production
  credential loading, credentialed production deployment, and external sandbox
  order emission from code remain blocked.
- No public SDK, hosted service, holdout/OOS expansion, live execution path, or
  generic platform work without a new explicit human decision.
- Phase 26 audit readiness work must not claim SOC 2, regulatory
  certification, investment-advice compliance, enterprise SLA, hosted service,
  auth/RBAC, SSO, or tenant isolation by default.
- Phase 27 must stop automatic roadmap expansion after T122 until a human
  approves a Core V2 roadmap.

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
- T69 Shared Artifact Contract Freeze completed.
- T70 Report Validity Checklist completed.
- T71 Reproducibility Checklist completed.
- T72 Product Bridge Support Notes completed.
- T73 Internal Review Packet Templates completed.
- T74 Core Artifact Support Review And Platformization Gate completed.
- T75 Artifact Contract V1 Schema completed.
- T76 Artifact Loader And Validation Result completed.
- T77 Artifact Validate CLI completed.
- T78 Executable Artifact Validation Review completed.
- T79 Artifact Registry Model completed.
- T80 Artifact Register And Show CLI completed.
- T81 Artifact List And History CLI completed.
- T82 Artifact Registry Review completed.
- T83 Reproducibility Manifest Schema completed.
- T84 Artifact Hash Compare Runner completed.
- T85 Reproducibility CLI completed.
- T86 Reproducibility Runner Review completed.
- T87 Evidence Packet Schema completed.
- T88 Evidence Build And Inspect CLI completed.
- T89 Evidence Index Automation completed.
- T90 Evidence Pipeline Review completed.
- T91 Product Bridge Profile Model completed.
- T92 Profile-Aware Validation CLI completed.
- T93 Product-Shaped Artifact Fixtures completed.
- T94 Product Bridge Profile Review completed.
- T95 Artifact Governance State Model completed.
- T96 Governance Transition CLI completed.
- T97 Approval Event Binding completed.
- T98 Governance State Machine Review completed.
- T99 Research Artifact Schemas completed.
- T100 Research Artifact Adapter completed.
- T101 Research Artifact Validation Fixtures completed.
- T102 Research Evaluation Integration Review completed.
- T103 Artifact Metadata Migration completed.
- T104 Artifact Store Abstraction completed.
- T105 Metadata Repository completed.
- T106 Storage And Audit Backend Review completed.
- T107 Internal API Boundary ADR completed.
- T108 Internal Python API Facade completed.
- T109 Internal Job Model completed.
- T110 Internal API And Job Boundary Review completed.
- T111 CAF Artifact Vocabulary completed.
- T112 Allocation Decision Artifact Schema completed.
- T113 CAF Validation Fixtures completed.
- T114 CAF Decision Primitives Review completed.
- T115 Audit Bundle Schema completed.
- T116 Lineage Graph Builder completed.
- T117 Data Classification And Reviewer Role Model completed.
- T118 Enterprise Audit Readiness Review completed.
- T119 Core V1 Surface Freeze completed.
- T120 Operator Runbook And Examples completed.
- T121 Documentation And Test Alignment Sweep completed.
- T122 Core V1 Productization Review completed.

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
- Phase 15 artifact support mode is complete through T74.
- Core remains hidden/internal after Phase 15 artifact support review.
- Phase 16 Executable Artifact Validation complete through T78.
- Phase 17 Artifact Registry complete through T82.
- Phase 18 Reproducibility Runner complete through T86.
- Phase 19 Evidence Pipeline complete through T90.
- Phase 20 Product Bridge Profiles complete through T94.
- Phase 21 Governance State Machine complete through T98.
- Phase 22 Research Evaluation Integration complete through T102.
- Phase 23 Storage And Audit Backend complete through T106.
- Phase 24 Internal API And Job Boundary complete through T110.
- Phase 25 CAF Decision Primitives complete through T114.
- Phase 26 Enterprise Audit Readiness complete through T118.
- Phase 27 Core V1 Productization complete through T122.
- Core V1 checkpoint complete; automatic roadmap expansion stopped pending human-approved V2 roadmap.
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
