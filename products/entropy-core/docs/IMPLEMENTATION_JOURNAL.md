# Implementation Journal - Entropy Core

Version: 1.0
Last updated: 2026-05-07
Status: append-only

This file records handoff context. It is not authority.

## Journal Entry Template

```markdown
### YYYY-MM-DD - TNN - Short Title

- Scope: files, directories, or task ids
- Why this work happened: reason or trigger
- Decisions applied: Decision Log or ADR refs, or "none"
- Evidence collected: tests, evals, review reports, or manual checks
- Follow-ups: next task, open risk, or "none"
- Notes for next agent: only context worth carrying forward
```

## Entries

### 2026-05-07 - T12 - Trader Risk Audit Bridge Contracts

- Scope: `docs/bridges/trader-risk-audit.md`, `src/entropy/bridges/`, `tests/integration/test_trader_risk_bridge_contract.py`
- Why this work happened: define deterministic Core-side bridge contracts for Trader Risk Audit without opening live trading, order-blocking, or unsupported research-claim surfaces
- Decisions applied: `docs/ARCHITECTURE.md#human-approval-boundaries`; `docs/IMPLEMENTATION_CONTRACT.md#product-bridge-boundary`
- Evidence collected: T12 acceptance tests passed (`8 passed`); full reset baseline `322 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T13 Hypothesis Backtest Bridge Design
- Notes for next agent: T12 adds schemas and guard functions only; it does not integrate with product runtime code, broker APIs, holdout reads, or Core registry/gate writes.

### 2026-05-07 - PHASE3 - Evaluation Safety Boundary

- Scope: T08-T11, `docs/audit/PHASE3_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`
- Why this work happened: Phase 3 tasks completed and the reset loop required a phase-boundary review, archive/index update, and handoff checkpoint
- Decisions applied: `D-RESET-001`, `D-RESET-004`, `D-RESET-005`; `docs/ARCHITECTURE.md#minimum-viable-control-surface`
- Evidence collected: Phase 3 boundary review PASS; full reset baseline `314 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T12 Trader Risk Audit Bridge Contracts
- Notes for next agent: no phase-boundary findings were opened; Phase 4 begins with product bridge contracts and must preserve no-live/no-claim boundaries.

### 2026-05-07 - T11 - Phase-Gate Evidence Packet

- Scope: `src/entropy/evidence/`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_phase_gate_packet_reset.py`
- Why this work happened: produce a reset-era phase-gate packet that binds baseline, required approvals, blocked claims, and canonical evidence rows without using old workflow state as authority
- Decisions applied: `docs/ARCHITECTURE.md#minimum-viable-control-surface`
- Evidence collected: T11 acceptance tests passed (`3 passed`); focused phase-gate/evidence slice `9 passed`; full reset baseline `314 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: run Phase 3 boundary review before starting T12
- Notes for next agent: T11 added `build_phase_gate_evidence_packet`, which verifies evidence-index artifact/test references and renders all claim surfaces blocked unless gate evidence exists.

### 2026-05-07 - T10 - Attribution Stream Boundary Audit

- Scope: `src/entropy/attribution/`, `tests/unit/test_attribution_reset.py`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: verify P&L stream separation and prevent archive-only attribution output from implying unsupported performance conclusions
- Decisions applied: `docs/core/PROTOCOL_SPEC.md#nn-2-four-stream-pl-attribution-permanent`
- Evidence collected: T10 acceptance tests passed (`3 passed`); full reset baseline `311 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T11 Phase-Gate Evidence Packet
- Notes for next agent: T10 added an archive-only attribution payload helper that serializes streams a/b/c/d separately and omits performance/OOS/phase-gate claim fields.

### 2026-05-07 - T09 - SimBroker and Cost Surface Regression

- Scope: `src/entropy/simbroker/`, `tests/unit/test_simbroker_reset.py`
- Why this work happened: verify deterministic SimBroker fill logs, separated cost fields, and no live broker/exchange imports after reset
- Decisions applied: `docs/ARCHITECTURE.md#non-goals-v1`
- Evidence collected: T09 acceptance tests passed (`3 passed`); focused SimBroker slice `28 passed`; full reset baseline `308 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T10 Attribution Stream Boundary Audit
- Notes for next agent: T09 changed tests only; existing SimBroker runtime behavior already satisfied the reset contract.

### 2026-05-07 - T08 - Data and Leakage Gate Verification

- Scope: `src/entropy/data/`, `src/entropy/walkforward/`, `src/entropy/hashing/`, `tests/unit/test_data_leakage_reset.py`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: heavy Evaluation Safety task to verify deterministic dataset hashing, leakage-gated OOS labels, and holdout lock checks before read access
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions`
- Evidence collected: T08 acceptance tests passed (`3 passed`); focused data/leakage/walk-forward slice `17 passed, 2 skipped`; full reset baseline `305 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T09 SimBroker and Cost Surface Regression
- Notes for next agent: T08 added explicit OOS label creation only from passing leakage reports and holdout read authorization that checks lock status before invoking a reader.

### 2026-05-07 - PHASE2 - Governance Integrity Boundary

- Scope: T04-T07, `docs/audit/PHASE2_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`
- Why this work happened: Phase 2 tasks completed and the reset loop required a phase-boundary review, archive/index update, and handoff checkpoint
- Decisions applied: `D-RESET-001`, `D-RESET-004`, `D-RESET-005`
- Evidence collected: Phase 2 boundary review PASS; full reset baseline `302 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T08 Data and Leakage Gate Verification
- Notes for next agent: no phase-boundary findings were opened.

### 2026-05-07 - T07 - Governance Approval Gate Audit

- Scope: `src/entropy/governance/`, `src/entropy/evidence/`, `tests/unit/test_governance_gate_reset.py`
- Why this work happened: verify human approval gates for phase gates, holdout access, and provider activation
- Decisions applied: `docs/ARCHITECTURE.md#human-approval-boundaries`; `docs/governance/governor.md`
- Evidence collected: T07 acceptance tests passed (`3 passed`); full reset baseline `302 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: run Phase 2 boundary review and start T08
- Notes for next agent: T07 added deterministic approval-gate helpers only; provider activation remains design-only unless future tasks approve a concrete provider.

### 2026-05-07 - T06 - No-Claim Report Boundary

- Scope: `src/entropy/evidence/`, `src/entropy/baseline/report.py`, `src/entropy/baseline/decision.py`, `tests/unit/test_no_claim_report_boundary.py`
- Why this work happened: verify report and decision surfaces remain archive-only/no-claim after reset and reject unsupported production, capital-ready, or OOS claim flags
- Decisions applied: `D-RESET-001`; `docs/legacy/CORE_LEGACY_SUMMARY.md#durable-boundaries`; `docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions`
- Evidence collected: T06 acceptance tests passed (`5 passed`); full reset baseline `299 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T07 Governance Approval Gate Audit
- Notes for next agent: T06 added an `oos_label` boolean guard to report payloads and rejects it before any no-claim research decision can be built.

### 2026-05-07 - T05 - Evidence Index and Journal Sync

- Scope: `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/tasks.md`, `tests/reset/test_evidence_index_contract.py`
- Why this work happened: make reset-era evidence and handoff records executable and scoped so future work can retrieve proof without reading old workflow logs by default
- Decisions applied: `D-RESET-001`, `D-RESET-005`
- Evidence collected: T05 acceptance tests passed (`3 passed`); full reset baseline `294 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T06 No-Claim Report Boundary
- Notes for next agent: T05 removed legacy summary from active `Files:` task scope and enforces legacy references only through scoped `Context-Refs`.

### 2026-05-07 - T04 - Registry Append-Only Audit

- Scope: `src/entropy/registry/`, `migrations/`, `tests/unit/test_registry_append_only_reset.py`, `tests/integration/test_registry_append_only_reset.py`
- Why this work happened: verify reset-era append-only behavior for Trial Registry and governance event surfaces
- Decisions applied: `D-RESET-001`; `docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules`; `docs/core/PROTOCOL_SPEC.md`
- Evidence collected: T04 acceptance tests passed (`3 passed`); full reset baseline `291 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T05 Evidence Index and Journal Sync
- Notes for next agent: T04 added static mutation-path checks, missing-hash-before-DB guard coverage, and migration append-only checks. Runtime code already satisfied the tested contracts.

### 2026-05-07 - PHASE1 - Reset Foundation Boundary

- Scope: T01-T03, `docs/audit/PHASE1_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`
- Why this work happened: Phase 1 tasks completed and the reset loop required a phase-boundary deep review, archive/index update, and handoff checkpoint
- Decisions applied: `D-RESET-001`, `D-RESET-002`, `D-RESET-004`, `D-RESET-005`
- Evidence collected: Phase 1 boundary review PASS; full reset baseline `288 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean
- Follow-ups: start T04 Registry Append-Only Audit
- Notes for next agent: no phase-boundary findings were opened.

### 2026-05-07 - T03 - Reset Baseline Smoke Tests

- Scope: `src/entropy/tracing.py`, `src/entropy/metrics.py`, `docs/CODEX_PROMPT.md`, `tests/reset/test_reset_smoke.py`
- Why this work happened: close Phase 1 with smoke coverage for tracing, metrics stubs, CLI health, reset baseline documentation, and legacy context scoping
- Decisions applied: `D-RESET-001`, `D-RESET-005`
- Evidence collected: `tests/reset/test_reset_smoke.py` passed (`5 passed`); full reset baseline `288 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean
- Follow-ups: run Phase 1 boundary review and archive update, then start T04
- Notes for next agent: the reset smoke tests scan source AST for tracing-boundary drift and active tasks for old workflow archive references.

### 2026-05-07 - T02 - Product-Local CI Setup

- Scope: `.github/workflows/ci.yml`, `tests/reset/test_ci_contract.py`
- Why this work happened: verify the product-local GitHub Actions workflow under the reset task graph
- Decisions applied: `D-RESET-002`, `D-RESET-004`
- Evidence collected: `tests/reset/test_ci_contract.py` passed (`3 passed`); full reset baseline `283 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T03 Reset Baseline Smoke Tests
- Notes for next agent: the CI workflow was already structurally aligned; this task added reset contract tests for the workflow.

### 2026-05-07 - T01 - Existing Project Baseline Skeleton

- Scope: `pyproject.toml`, `src/entropy/__init__.py`, `src/entropy/cli.py`, `tests/reset/test_reset_tooling.py`, `tests/reset/test_reset_skeleton.py`
- Why this work happened: complete the first reset foundation task by verifying Python 3.12 tooling, package import/version surface, and CLI help surface against current files
- Decisions applied: `D-RESET-001`, `D-RESET-002`
- Evidence collected: `tests/reset/test_reset_tooling.py tests/reset/test_reset_skeleton.py` passed (`3 passed`); full reset baseline `280 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean
- Follow-ups: start T02 Product-Local CI Setup
- Notes for next agent: T01 required no product-code patch in this segment; current files already satisfied the reset contract.

### 2026-05-07 - RESET - Governance Reset Bootstrap

- Scope: `docs/`, `.github/workflows/ci.yml`, `.claude/commands/orchestrate.md`, `pyproject.toml`
- Why this work happened: rebuild the AI Workflow Playbook loop over existing Entropy Core code
- Decisions applied: `D-RESET-001`, `D-RESET-002`, `D-RESET-003`, `D-RESET-004`, `D-RESET-005`, `D-RESET-006`
- Evidence collected: structural sanity checks pending; Phase 1 audit pending
- Follow-ups: run `/orchestrate` to execute Phase 1 validation, then start T01 if validation passes
- Notes for next agent: old active workflow files are in `docs/legacy/old-workflow/2026-05-07/`; do not read them by default.
