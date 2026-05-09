# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-09
Phase: 13

Reset state for Entropy Core after archiving the old active workflow. Historical files are available under `docs/legacy/old-workflow/2026-05-07/` but are not read by default.

---

## Current Phase

- Phase: 13
- Name: Product Hypothesis Confirmation Decision
- Business goal: define the safest next validation step toward product hypothesis confirmation using local-only approval decision work.
- Phase gate: request, intake, validation-path decision, non-approval regression, validation plan, and review prove no production/capital/live/holdout path opens without explicit future approval.

## Current State

- Phase: 13
- Baseline: 489 passing tests, 20 skipped (T62 local verification on 2026-05-09)
- Ruff: clean on T62 local verification 2026-05-09
- Pyright: clean on T62 local verification 2026-05-09
- Last CI: product-local workflow configured; remote CI not yet observed after reset
- Holdout: locked
- Live capital: not approved
- Broker/exchange integration: not approved
- OOS/performance claims: not approved
- Last updated: 2026-05-09

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Legacy summary: `docs/legacy/CORE_LEGACY_SUMMARY.md`
- Old active workflow archive: `docs/legacy/old-workflow/2026-05-07/`
- Protocol docs: `docs/core/`
- Governance docs: `docs/governance/`

## Next Task

Checkpoint after Phase 13 Product Hypothesis Confirmation Decision.

Phase 11 Live-Feed Dry Run Readiness Review is complete through T50. Roadmap evaluation opened Phase 12 as sandbox-only broker/exchange execution risk audit work.

T35 Holdout Access Protocol Deny-By-Default Contract completed on 2026-05-09. T36 Holdout Approval Event Schema Contract completed on 2026-05-09. T37 Holdout Access Audit Logging Contract completed on 2026-05-09. T38 Holdout Leakage Guard Protocol Fixture completed on 2026-05-09. T39 Holdout Access Protocol Review completed on 2026-05-09. T40 Holdout Approval Request Packet Scaffold completed on 2026-05-09. T41 Holdout Approval Evidence Intake Contract completed on 2026-05-09. T42 Holdout Approval Absence Denial Packet completed on 2026-05-09. T43 Holdout Non-Approval Source Regression completed on 2026-05-09. T44 Holdout Decision No-Read Dry Run completed on 2026-05-09. T45 Holdout Approval Decision Review completed on 2026-05-09. T46 Live-Feed Boundary Contract completed on 2026-05-09. T47 Live-Feed Fixture Manifest completed on 2026-05-09. T48 Live-Feed Adapter Dry-Run Contract completed on 2026-05-09. T49 Live-Feed Observability Packet completed on 2026-05-09. T50 Live-Feed Dry Run Readiness Review completed on 2026-05-09. T51 Broker Sandbox Boundary Contract completed on 2026-05-09. T52 Broker Sandbox Fixture Manifest completed on 2026-05-09. T53 Execution Risk Control Contract completed on 2026-05-09. T54 Kill-Switch Audit Log Contract completed on 2026-05-09. T55 Sandbox Execution No-Capital Dry Run completed on 2026-05-09. T56 Broker Sandbox Readiness Review completed on 2026-05-09. T57 Product Hypothesis Confirmation Request Packet completed on 2026-05-09. T58 Product Validation Approval Intake Contract completed on 2026-05-09. T59 Product Hypothesis Validation Path Decision completed on 2026-05-09. T60 Production Capital Non-Approval Regression completed on 2026-05-09. T61 Local Next Validation Plan Packet completed on 2026-05-09. T62 Product Hypothesis Confirmation Decision Review completed on 2026-05-09. Phase 13 Product Hypothesis Confirmation Decision is closed. product hypothesis status: unconfirmed_pending_future_validation. Next human decision required: whether to authorize a future local broker sandbox no-capital replay extension task.

Archive Evidence Expansion block complete through T24, Phase 7 complete through T29, Phase 8 complete through T34, Phase 9 complete through T39, Phase 10 complete through T45, Phase 11 complete through T50, and Phase 12 complete through T56. Phase 11 is local-only live-feed dry-run readiness and is closed. Phase 12 is sandbox-only broker/exchange execution risk audit and is closed. Phase 13 is local-only approval decision work for defining the safest next validation step toward product hypothesis confirmation. No approval event currently exists. Do not execute real external side effects, holdout reads, holdout unlocks, live capital actions, live broker/exchange execution, live order placement, production credential loading, or credentialed production deployment. No live orders, no broker/exchange execution, no production credentials, no live capital, and no holdout access are approved.

## Fix Queue

empty

## Open Findings

none after reset. Legacy D-K findings were closed in the prior workflow, but old findings are not active unless re-opened by a reset task or review.

## Completed Tasks

- 2026-05-07: T01 Existing Project Baseline Skeleton completed.
  - Acceptance tests: `tests/reset/test_reset_tooling.py` and `tests/reset/test_reset_skeleton.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `280 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean.
- 2026-05-07: T02 Product-Local CI Setup completed.
  - Acceptance tests: `tests/reset/test_ci_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `283 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T03 Reset Baseline Smoke Tests completed.
  - Acceptance tests: `tests/reset/test_reset_smoke.py` passed (`5 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `288 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean.
- 2026-05-07: T04 Registry Append-Only Audit completed.
  - Acceptance tests: `tests/unit/test_registry_append_only_reset.py` and `tests/integration/test_registry_append_only_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `291 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T05 Evidence Index and Journal Sync completed.
  - Acceptance tests: `tests/reset/test_evidence_index_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `294 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T06 No-Claim Report Boundary completed.
  - Acceptance tests: `tests/unit/test_no_claim_report_boundary.py` passed (`5 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `299 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T07 Governance Approval Gate Audit completed.
  - Acceptance tests: `tests/unit/test_governance_gate_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `302 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T08 Data and Leakage Gate Verification completed.
  - Acceptance tests: `tests/unit/test_data_leakage_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `305 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T09 SimBroker and Cost Surface Regression completed.
  - Acceptance tests: `tests/unit/test_simbroker_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `308 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T10 Attribution Stream Boundary Audit completed.
  - Acceptance tests: `tests/unit/test_attribution_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `311 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T11 Phase-Gate Evidence Packet completed.
  - Acceptance tests: `tests/integration/test_phase_gate_packet_reset.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `314 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T12 Trader Risk Audit Bridge Contracts completed.
  - Acceptance tests: `tests/integration/test_trader_risk_bridge_contract.py` passed (`8 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `322 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T13 Hypothesis Backtest Bridge Design completed.
  - Acceptance tests: `tests/integration/test_hypothesis_bridge_design.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `325 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T14 Reset Strategy Closure Review completed.
  - Acceptance tests: `tests/reset/test_reset_closure.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `328 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T15 First Research Candidate Registration Packet completed.
  - Acceptance tests: `tests/integration/test_first_research_packet.py` passed (`11 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `339 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T16 Archive Dataset Manifest and Hash Binding completed.
  - Acceptance tests: `tests/integration/test_first_research_packet.py` passed (`14 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `342 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T17 Archive Evaluation Harness Wiring completed.
  - Acceptance tests: `tests/integration/test_first_research_packet.py` passed (`17 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `345 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T18 First Research Evidence Packet completed.
  - Acceptance tests: `tests/integration/test_first_research_packet.py` passed (`20 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `348 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T19 First Research Packet Review completed.
  - Acceptance tests: `tests/reset/test_first_research_packet_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `351 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T20 Second Research Candidate Registration Packet completed.
  - Acceptance tests: `tests/integration/test_second_research_packet.py` passed (`11 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `362 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T21 Second Archive Dataset Manifest and Hash Binding completed.
  - Acceptance tests: `tests/integration/test_second_research_packet.py` passed (`14 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `365 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T22 Second Archive Evaluation Harness Wiring completed.
  - Acceptance tests: `tests/integration/test_second_research_packet.py` passed (`17 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `368 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T23 Second Research Evidence Packet completed.
  - Acceptance tests: `tests/integration/test_second_research_packet.py` passed (`20 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `371 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-07: T24 Archive Evidence Expansion Review completed.
  - Acceptance tests: `tests/reset/test_archive_evidence_expansion_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `374 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T25 Roadmap Governance Contract completed.
  - Acceptance tests: `tests/reset/test_roadmap_governance.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `377 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T26 Archive Packet Replay Contract completed.
  - Acceptance tests: `tests/integration/test_archive_replay.py` passed (`4 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `381 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T27 Evidence Hash Reproducibility Matrix completed.
  - Acceptance tests: `tests/reset/test_reproducibility_matrix.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `384 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T28 No-Claim Surface Regression Sweep completed.
  - Acceptance tests: `tests/reset/test_no_claim_roadmap_sweep.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `387 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T29 Archive Reproducibility Hardening Review completed.
  - Acceptance tests: `tests/reset/test_archive_reproducibility_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `390 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-08: T30 Archive Evidence Sufficiency Gap Matrix completed.
  - Acceptance tests: `tests/reset/test_phase_gate_readiness_gap_matrix.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `393 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T31 Phase-Gate Readiness Packet Scaffold completed.
  - Acceptance tests: `tests/reset/test_phase_gate_readiness_packet.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `396 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T32 Approval Boundary Checklist completed.
  - Acceptance tests: `tests/reset/test_approval_boundary_checklist.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `399 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T33 Readiness No-Holdout Dry Run completed.
  - Acceptance tests: `tests/reset/test_readiness_no_holdout_dry_run.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `402 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T34 Phase-Gate Readiness Review completed.
  - Acceptance tests: `tests/reset/test_phase_gate_readiness_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `405 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T35 Holdout Access Protocol Deny-By-Default Contract completed.
  - Acceptance tests: `tests/reset/test_holdout_access_protocol.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `408 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T36 Holdout Approval Event Schema Contract completed.
  - Acceptance tests: `tests/reset/test_holdout_approval_event_schema.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `411 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T37 Holdout Access Audit Logging Contract completed.
  - Acceptance tests: `tests/reset/test_holdout_audit_logging_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `414 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T38 Holdout Leakage Guard Protocol Fixture completed.
  - Acceptance tests: `tests/reset/test_holdout_leakage_guard_protocol.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `417 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T39 Holdout Access Protocol Review completed.
  - Acceptance tests: `tests/reset/test_holdout_access_protocol_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `420 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T40 Holdout Approval Request Packet Scaffold completed.
  - Acceptance tests: `tests/reset/test_holdout_approval_request_packet.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `423 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T41 Holdout Approval Evidence Intake Contract completed.
  - Acceptance tests: `tests/reset/test_holdout_approval_intake_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `426 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T42 Holdout Approval Absence Denial Packet completed.
  - Acceptance tests: `tests/reset/test_holdout_approval_absence_denial.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `429 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T43 Holdout Non-Approval Source Regression completed.
  - Acceptance tests: `tests/reset/test_holdout_non_approval_source_regression.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `432 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T44 Holdout Decision No-Read Dry Run completed.
  - Acceptance tests: `tests/reset/test_holdout_decision_no_read_dry_run.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `435 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T45 Holdout Approval Decision Review completed.
  - Acceptance tests: `tests/reset/test_holdout_approval_decision_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `438 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T46 Live-Feed Boundary Contract completed.
  - Acceptance tests: `tests/reset/test_live_feed_boundary_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `441 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T47 Live-Feed Fixture Manifest completed.
  - Acceptance tests: `tests/reset/test_live_feed_fixture_manifest.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `444 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T48 Live-Feed Adapter Dry-Run Contract completed.
  - Acceptance tests: `tests/reset/test_live_feed_adapter_dry_run_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `447 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T49 Live-Feed Observability Packet completed.
  - Acceptance tests: `tests/reset/test_live_feed_observability_packet.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `450 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T50 Live-Feed Dry Run Readiness Review completed.
  - Acceptance tests: `tests/reset/test_live_feed_readiness_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `453 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T51 Broker Sandbox Boundary Contract completed.
  - Acceptance tests: `tests/reset/test_broker_sandbox_boundary_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `456 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T52 Broker Sandbox Fixture Manifest completed.
  - Acceptance tests: `tests/reset/test_broker_sandbox_fixture_manifest.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `459 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T53 Execution Risk Control Contract completed.
  - Acceptance tests: `tests/reset/test_execution_risk_control_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `462 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T54 Kill-Switch Audit Log Contract completed.
  - Acceptance tests: `tests/reset/test_kill_switch_audit_log_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `465 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T55 Sandbox Execution No-Capital Dry Run completed.
  - Acceptance tests: `tests/reset/test_sandbox_execution_no_capital_dry_run.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `468 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T56 Broker Sandbox Readiness Review completed.
  - Acceptance tests: `tests/reset/test_broker_sandbox_readiness_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `471 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T57 Product Hypothesis Confirmation Request Packet completed.
  - Acceptance tests: `tests/reset/test_product_hypothesis_confirmation_request.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `474 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T58 Product Validation Approval Intake Contract completed.
  - Acceptance tests: `tests/reset/test_product_validation_approval_intake_contract.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `477 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T59 Product Hypothesis Validation Path Decision completed.
  - Acceptance tests: `tests/reset/test_product_hypothesis_validation_path_decision.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `480 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T60 Production Capital Non-Approval Regression completed.
  - Acceptance tests: `tests/reset/test_production_capital_non_approval_regression.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `483 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T61 Local Next Validation Plan Packet completed.
  - Acceptance tests: `tests/reset/test_local_next_validation_plan_packet.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `486 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.
- 2026-05-09: T62 Product Hypothesis Confirmation Decision Review completed.
  - Acceptance tests: `tests/reset/test_product_hypothesis_confirmation_decision_review.py` passed (`3 passed`).
  - Reset baseline: `.venv/bin/python -m pytest -q tests/` reported `489 passed, 20 skipped`.
  - Quality checks: ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean.

## Phase History

- 2026-05-07: Phase 1 Reset Foundation completed. Review artifact: `docs/audit/PHASE1_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Phase 2 Governance Integrity completed. Review artifact: `docs/audit/PHASE2_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Phase 3 Evaluation Safety completed. Review artifact: `docs/audit/PHASE3_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: Reset implementation block completed. Review artifact: `docs/audit/RESET_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: First Research Evidence Packet block opened by human decision after T14. Scope: T15-T19.
- 2026-05-07: First Research Evidence Packet block completed. Review artifact: `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-07: First Research Evidence Packet block complete through T19. Human decision required after T19 was satisfied by opening archive-only evidence expansion.
- 2026-05-07: T19 boundary state preserved: holdout, live feeds, broker/exchange, production, capital-ready, and OOS/performance remain unapproved.
- 2026-05-07: Archive Evidence Expansion block opened by human decision after T19. Scope: T20-T24.
- 2026-05-07: Archive Evidence Expansion block complete through T24. Review artifact: `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-08: Human decision required after T24 was satisfied by opening Phase 7 only.
- 2026-05-08: Historical T24 boundary preserved: holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, and OOS/performance remain unapproved at the T24 boundary.
- 2026-05-08: Forward roadmap recorded for phases 7 through 13 with autonomous roadmap evaluation and rollover required after every active phase.
- 2026-05-08: Phase 7 Archive Reproducibility Hardening opened by human decision after T24. Scope: T25-T29. Phases 8 through 13 remain planned only.
- 2026-05-08: T25 Roadmap Governance Contract completed. Next task: T26 Archive Packet Replay Contract.
- 2026-05-08: T26 Archive Packet Replay Contract completed. Next task: T27 Evidence Hash Reproducibility Matrix.
- 2026-05-08: T27 Evidence Hash Reproducibility Matrix completed. Next task: T28 No-Claim Surface Regression Sweep.
- 2026-05-08: T28 No-Claim Surface Regression Sweep completed. Next task: T29 Archive Reproducibility Hardening Review.
- 2026-05-08: Phase 7 Archive Reproducibility Hardening completed. Review artifact: `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-08: Roadmap evaluation kept planned Phase 8 Phase-Gate Readiness Review and opened T30 Archive Evidence Sufficiency Gap Matrix.
- 2026-05-08: T30 Archive Evidence Sufficiency Gap Matrix completed. Next task: T31 Phase-Gate Readiness Packet Scaffold.
- 2026-05-09: T31 Phase-Gate Readiness Packet Scaffold completed. Next task: T32 Approval Boundary Checklist.
- 2026-05-09: T32 Approval Boundary Checklist completed. Next task: T33 Readiness No-Holdout Dry Run.
- 2026-05-09: T33 Readiness No-Holdout Dry Run completed. Next task: T34 Phase-Gate Readiness Review.
- 2026-05-09: Phase 8 Phase-Gate Readiness Review completed. Review artifact: `docs/audit/PHASE_GATE_READINESS_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-09: Roadmap evaluation kept planned Phase 9 Holdout Access Protocol, modified to protocol-only design, and opened T35 Holdout Access Protocol Deny-By-Default Contract.
- 2026-05-09: T35 Holdout Access Protocol Deny-By-Default Contract completed. Next task: T36 Holdout Approval Event Schema Contract.
- 2026-05-09: T36 Holdout Approval Event Schema Contract completed. Next task: T37 Holdout Access Audit Logging Contract.
- 2026-05-09: T37 Holdout Access Audit Logging Contract completed. Next task: T38 Holdout Leakage Guard Protocol Fixture.
- 2026-05-09: T38 Holdout Leakage Guard Protocol Fixture completed. Next task: T39 Holdout Access Protocol Review.
- 2026-05-09: Phase 9 Holdout Access Protocol completed. Review artifact: `docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-09: Roadmap evaluation modified planned Phase 10 into Holdout Approval Decision Packet and opened T40 Holdout Approval Request Packet Scaffold.
- 2026-05-09: T40 Holdout Approval Request Packet Scaffold completed. Next task: T41 Holdout Approval Evidence Intake Contract.
- 2026-05-09: T41 Holdout Approval Evidence Intake Contract completed. Next task: T42 Holdout Approval Absence Denial Packet.
- 2026-05-09: T42 Holdout Approval Absence Denial Packet completed. Next task: T43 Holdout Non-Approval Source Regression.
- 2026-05-09: T43 Holdout Non-Approval Source Regression completed. Next task: T44 Holdout Decision No-Read Dry Run.
- 2026-05-09: T44 Holdout Decision No-Read Dry Run completed. Next task: T45 Holdout Approval Decision Review.
- 2026-05-09: Phase 10 Holdout Approval Decision Packet completed. Review artifact: `docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-09: Roadmap evaluation blocked the future approved holdout evaluation phase and opened Phase 11 Live-Feed Dry Run Readiness as local-only no-order work.
- 2026-05-09: T45 Holdout Approval Decision Review completed. Next task: T46 Live-Feed Boundary Contract.
- 2026-05-09: T46 Live-Feed Boundary Contract completed. Next task: T47 Live-Feed Fixture Manifest.
- 2026-05-09: T47 Live-Feed Fixture Manifest completed. Next task: T48 Live-Feed Adapter Dry-Run Contract.
- 2026-05-09: T48 Live-Feed Adapter Dry-Run Contract completed. Next task: T49 Live-Feed Observability Packet.
- 2026-05-09: T49 Live-Feed Observability Packet completed. Next task: T50 Live-Feed Dry Run Readiness Review.
- 2026-05-09: Phase 11 Live-Feed Dry Run Readiness completed. Review artifact: `docs/audit/LIVE_FEED_READINESS_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-09: Roadmap evaluation modified planned Phase 12 into sandbox-only broker/exchange execution risk audit work and opened T51 Broker Sandbox Boundary Contract.
- 2026-05-09: T50 Live-Feed Dry Run Readiness Review completed. Next task: T51 Broker Sandbox Boundary Contract.
- 2026-05-09: T51 Broker Sandbox Boundary Contract completed. Next task: T52 Broker Sandbox Fixture Manifest.
- 2026-05-09: T52 Broker Sandbox Fixture Manifest completed. Next task: T53 Execution Risk Control Contract.
- 2026-05-09: T53 Execution Risk Control Contract completed. Next task: T54 Kill-Switch Audit Log Contract.
- 2026-05-09: T54 Kill-Switch Audit Log Contract completed. Next task: T55 Sandbox Execution No-Capital Dry Run.
- 2026-05-09: T55 Sandbox Execution No-Capital Dry Run completed. Next task: T56 Broker Sandbox Readiness Review.
- 2026-05-09: Phase 12 Broker Sandbox and Execution Risk Audit completed. Review artifact: `docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md`. Result: PASS; Stop-Ship 0, P0 0, P1 0, P2 0.
- 2026-05-09: Roadmap evaluation blocked Phase 13 Production and Capital Gate pending explicit human approval and a local-only task rewrite. Checkpoint before production/capital work.
- 2026-05-09: Operator approved rewriting Phase 13 as local-only product hypothesis confirmation decision work with no live orders, no broker/exchange execution, no production credentials, no live capital, and no holdout access.
- 2026-05-09: T57 Product Hypothesis Confirmation Request Packet completed. Next task: T58 Product Validation Approval Intake Contract.
- 2026-05-09: T58 Product Validation Approval Intake Contract completed. Next task: T59 Product Hypothesis Validation Path Decision.
- 2026-05-09: T59 Product Hypothesis Validation Path Decision completed. Next task: T60 Production Capital Non-Approval Regression.
- 2026-05-09: T60 Production Capital Non-Approval Regression completed. Next task: T61 Local Next Validation Plan Packet.
- 2026-05-09: T61 Local Next Validation Plan Packet completed. Next task: T62 Product Hypothesis Confirmation Decision Review.
- 2026-05-09: Phase 13 Product Hypothesis Confirmation Decision completed. Review artifact: `docs/audit/PRODUCT_HYPOTHESIS_CONFIRMATION_DECISION_REVIEW.md`. product hypothesis status: unconfirmed_pending_future_validation. Next human decision required before further validation execution.
- 2026-05-08: Phase boundaries changed from stop points to autonomous rollover points: deep review, fix findings, validate, evaluate roadmap, rewrite future phases, open the next logical active phase, and continue.

## Profile State: RAG

- RAG Status: OFF
- Active corpora: n/a
- Retrieval baseline: n/a
- Open retrieval findings: none
- Index schema version: n/a
- Pending reindex actions: none
- Retrieval-related next tasks: none
- Retrieval-driven tasks: none

## Tool-Use State

- Tool-Use Profile: OFF
- Registered tool schemas: n/a
- Unsafe-action guardrails: n/a
- Open tool findings: none

## Agentic State

- Agentic Profile: OFF
- Active agent roles: n/a
- Loop termination contract version: n/a
- Cross-iteration state mechanism: n/a
- Open agent findings: none

## Planning State

- Planning Profile: OFF
- Plan schema version: n/a
- Plan validation method: n/a
- Open plan findings: none

## Compliance State

- Compliance Status: OFF
- Active frameworks: n/a
- Controls implemented: n/a
- Controls partial: n/a
- Controls not started: n/a
- Evidence artifact: n/a
- Open compliance findings: none

## Evaluation State

### Last Evaluation

- Profile: Product Hypothesis Confirmation Decision Review
- Task: T62 Product Hypothesis Confirmation Decision Review
- Date: 2026-05-09
- Eval Source: `tests/reset/test_product_hypothesis_confirmation_decision_review.py`
- Metric(s): review sections, confirmation status, audit/prompt state
- Score: `3 passed`; current baseline `489 passed, 20 skipped`
- Baseline: T61 local next validation plan packet `486 passed, 20 skipped`
- Delta: +3 passing tests
- Regression: none known

### Open Evaluation Issues

none

### Human Decision

Human approval after T24 opened Phase 7 Archive Reproducibility Hardening and recorded a dynamic roadmap for phases 7 through 13. Phase 7 roadmap evaluation opened Phase 8 readiness analysis. Phase 8 roadmap evaluation opened Phase 9 protocol-only holdout access design. Phase boundaries now roll over automatically after deep review, fixes, validation, and roadmap evaluation. Real external side effects, holdout reads, holdout unlocks, live capital actions, live broker/exchange execution, and credentialed production deployment remain blocked.

### Human Decision Point

Current active task is checkpoint after Phase 13 Product Hypothesis Confirmation Decision. Archive Evidence Expansion block is complete through T24, Phase 7 is complete through T29, Phase 8 is complete through T34, Phase 9 is complete through T39, Phase 10 is complete through T45, Phase 11 is complete through T50, Phase 12 is complete through T56, and Phase 13 is complete through T62. product hypothesis status: unconfirmed_pending_future_validation. Next human decision required before any further validation execution. No approval event currently exists. Real external side effects, holdout reads, holdout unlocks, live order placement, live capital actions, live broker/exchange execution, production credential loading, and credentialed production deployment remain blocked.

## Verification Defaults

Run from `products/entropy-core/`:

- `.venv/bin/python -m pytest -q tests/`
- `.venv/bin/python -m ruff check src/entropy tests`
- `.venv/bin/python -m ruff format --check src/entropy tests`
- `.venv/bin/python -m pyright src/entropy`
- `git diff --check`

## Instructions for Codex

1. Read `docs/IMPLEMENTATION_CONTRACT.md` before starting any task.
2. Read the full task definition in `docs/tasks.md` before writing code.
3. Read all Depends-On tasks to understand interface contracts.
4. Read task `Context-Refs` and relevant continuity artifacts when the task depends on prior decisions, evidence, findings, registry, governance, leakage, holdout, attribution, product bridges, migrations, or runtime/language boundaries.
5. Run the verification defaults needed for the task and capture the pre-task baseline.
6. Write tests before or alongside implementation. Every acceptance criterion has a passing test.
7. Update this file at every phase boundary with baseline, next task, and open findings.
8. Commit with format `type(scope): description` - one logical change per commit.
9. When done, return `IMPLEMENTATION_RESULT: DONE` with tests run, baseline, and files changed.
10. When blocked, return `IMPLEMENTATION_RESULT: BLOCKED` with the exact blocker.

## Phase 1 Validation

Phase 1 validation ran in the reset loop and wrote `docs/audit/PHASE1_AUDIT.md`.
Result: PASS, 100 checks passed, 0 blockers, 0 warnings.
