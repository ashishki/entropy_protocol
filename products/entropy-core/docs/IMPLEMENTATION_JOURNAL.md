# Implementation Journal - Entropy Core

Version: 1.0
Last updated: 2026-05-08
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

### 2026-05-09 - T32 - Approval Boundary Checklist

- Scope: `docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md`, `tests/reset/test_approval_boundary_checklist.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: record explicit human approval boundaries, blocked status, evidence prerequisites, and non-approval sources before no-holdout dry-run validation
- Decisions applied: `docs/ARCHITECTURE.md#human-approval-boundaries`; `docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions`; `D-ROADMAP-001`
- Evidence collected: T32 acceptance tests passed (`3 passed`); full reset baseline `399 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T33 Readiness No-Holdout Dry Run
- Notes for next agent: checklist confirms roadmap phases, readiness docs, archive evidence, passing tests, and review recommendations are not approval sources. Prompt and handoff must keep external side effects, holdout reads, live capital, live broker/exchange execution, and credentialed production deployment blocked.

### 2026-05-09 - T31 - Phase-Gate Readiness Packet Scaffold

- Scope: `docs/readiness/PHASE_GATE_READINESS_PACKET.md`, `tests/reset/test_phase_gate_readiness_packet.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: scaffold a phase-gate readiness packet that assembles evidence, missing controls, limitations, and approval prerequisites without granting approval
- Decisions applied: `D-ROADMAP-001`; `docs/readiness/PHASE_GATE_GAP_MATRIX.md`; `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`
- Evidence collected: T31 acceptance tests passed (`3 passed`); full reset baseline `396 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T32 Approval Boundary Checklist
- Notes for next agent: readiness packet references the Phase 8 gap matrix and Phase 7 review, lists missing controls, and explicitly records all restricted approval flags as false or blocked.

### 2026-05-08 - T30 - Archive Evidence Sufficiency Gap Matrix

- Scope: `docs/readiness/PHASE_GATE_GAP_MATRIX.md`, `docs/EVIDENCE_INDEX.md`, `tests/reset/test_phase_gate_readiness_gap_matrix.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: map current archive evidence to readiness controls and missing prerequisites before any future human phase-gate discussion
- Decisions applied: `D-ROADMAP-001`; `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`; `docs/research/REPRODUCIBILITY_MATRIX.md`
- Evidence collected: T30 acceptance tests passed (`3 passed`); full reset baseline `393 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T31 Phase-Gate Readiness Packet Scaffold
- Notes for next agent: T30 records complete, partial, and blocked readiness controls. Holdout, OOS/performance, live feed, broker/exchange, production, capital-ready, and phase-gate approvals remain blocked.

### 2026-05-08 - T29 - Archive Reproducibility Hardening Review

- Scope: `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `tests/reset/test_archive_reproducibility_review.py`
- Why this work happened: close Phase 7 with deep review, audit archive entry, roadmap evaluation, and next active phase opening
- Decisions applied: `D-ROADMAP-001`; `docs/research/REPRODUCIBILITY_MATRIX.md`; `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`
- Evidence collected: T29 acceptance tests passed (`3 passed`); full reset baseline `390 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T30 Archive Evidence Sufficiency Gap Matrix
- Notes for next agent: Phase 8 is readiness analysis only. It may identify evidence gaps before any future phase-gate discussion, but it must not read holdout data or approve OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate claim surfaces.

### 2026-05-08 - T28 - No-Claim Surface Regression Sweep

- Scope: `tests/reset/test_no_claim_roadmap_sweep.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `docs/EVIDENCE_INDEX.md`, `AGENT_NOTES.md`
- Why this work happened: prove active archive evidence, bridge, phase plan, prompt, and handoff surfaces do not silently open restricted claim paths before Phase 7 review
- Decisions applied: `D-ROADMAP-001`; `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`; `docs/bridges/hypothesis-backtest.md`
- Evidence collected: T28 acceptance tests passed (`3 passed`); full reset baseline `387 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T29 Archive Reproducibility Hardening Review
- Notes for next agent: no-claim sweep scans active docs and replayed packets for concrete approval flags, confirms phases 8 through 13 remain planned roadmap direction, and preserves prompt/handoff boundary language.

### 2026-05-08 - T27 - Evidence Hash Reproducibility Matrix

- Scope: `docs/research/REPRODUCIBILITY_MATRIX.md`, `docs/EVIDENCE_INDEX.md`, `tests/reset/test_reproducibility_matrix.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: record concrete hash categories across existing archive-only evidence packets and prove the matrix rejects missing, unresolved, invalid, or duplicate rows
- Decisions applied: `D-ROADMAP-001`; T26 archive packet replay contract
- Evidence collected: T27 acceptance tests passed (`3 passed`); full reset baseline `384 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T28 No-Claim Surface Regression Sweep
- Notes for next agent: the matrix is evidence bookkeeping only. It records candidate, dataset, code, policy, parameter, evidence artifact, and replay JSON hashes for the first and second archive packets without ranking hypotheses or opening holdout, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate approvals.

### 2026-05-08 - T26 - Archive Packet Replay Contract

- Scope: `src/entropy/evidence/archive_replay.py`, `src/entropy/evidence/__init__.py`, `tests/integration/test_archive_replay.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: prove first and second archive-only evidence packets can be deterministically replayed from current fixtures and checked against stored packet/manifest artifacts
- Decisions applied: `D-ROADMAP-001`; T25 roadmap governance contract
- Evidence collected: T26 acceptance tests passed (`4 passed`); full reset baseline `381 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T27 Evidence Hash Reproducibility Matrix
- Notes for next agent: replay checks compare stable packet ids, candidate ids, no-claim labels, artifact references, deterministic packet hashes, and required manifest boundaries. They fail missing packet artifacts, dataset manifests, artifact references, or unresolved hash bindings without opening holdout, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate approvals.

### 2026-05-08 - T25 - Roadmap Governance Contract Opened

- Scope: `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `docs/DECISION_LOG.md`
- Why this work happened: record the forward roadmap requested after T24, open the first active roadmap phase, and make phase boundaries autonomous rollover points
- Decisions applied: `D-ROADMAP-001`; `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`
- Evidence collected: T25 acceptance tests passed (`3 passed`); full reset baseline `377 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: continue Phase 7 with T26 replay checks
- Notes for next agent: phases 8 through 13 are planned direction and may be promoted or rewritten by roadmap evaluation. After every active phase, deep-review, fix findings, validate, evaluate the roadmap, rewrite future phases/tasks if useful, open the next logical active phase, and continue automatically.

### 2026-05-07 - T24 - Archive Evidence Expansion Review

- Scope: `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `tests/reset/test_archive_evidence_expansion_review.py`
- Why this work happened: close the archive evidence expansion block with a review artifact, audit index row, validation record, limitations, and next human decision point
- Decisions applied: `docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md`; `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`
- Evidence collected: T24 acceptance tests passed (`3 passed`); full reset baseline `374 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: stop for human decision unless explicitly instructed to open a new research block or gate discussion
- Notes for next agent: archive evidence expansion is complete; holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, and OOS/performance remain unapproved.

### 2026-05-07 - T23 - Second Research Evidence Packet

- Scope: `src/entropy/evidence/first_research_packet.py`, `docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_second_research_packet.py`
- Why this work happened: generate a second deterministic archive-only research evidence packet from the second candidate, manifest, and evaluation outputs
- Decisions applied: `docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md`; `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`; T22 archive evaluation harness proof
- Evidence collected: T23 acceptance tests passed (`20 passed`); full reset baseline `371 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T24 Archive Evidence Expansion Review
- Notes for next agent: T23 parameterized packet id for the second packet and remains no-claim; no holdout, live, broker/exchange, production, capital-ready, phase-gate, or OOS/performance approval was introduced.

### 2026-05-07 - T22 - Second Archive Evaluation Harness Wiring

- Scope: `tests/integration/test_second_research_packet.py`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: prove repeat use of the archive-only evaluation harness on the second candidate without opening claim surfaces
- Decisions applied: `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`; `docs/audit/PHASE3_REVIEW.md`; T17 archive evaluation harness contract; T20-T21 second packet contracts
- Evidence collected: T22 acceptance tests passed (`17 passed`); full reset baseline `368 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T23 Second Research Evidence Packet
- Notes for next agent: T22 is heavy evidence; the second evaluation remains archive-only, refuses missing hashes, emits separated attribution streams, and does not produce OOS/performance, holdout, phase-gate, production, or capital-ready approval.

### 2026-05-07 - T21 - Second Archive Dataset Manifest and Hash Binding

- Scope: `docs/research/second-packet/DATASET_MANIFEST.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_second_research_packet.py`
- Why this work happened: bind the second research candidate to an archive-only dataset manifest with deterministic aggregate hashes and explicit holdout exclusion
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/IMPLEMENTATION_CONTRACT.md#leakage-and-holdout-boundary`; T16 manifest binding contract; T20 second candidate packet contract
- Evidence collected: T21 acceptance tests passed (`14 passed`); full reset baseline `365 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T22 Second Archive Evaluation Harness Wiring
- Notes for next agent: T21 reused the archive manifest boundary for ETH fixture paths; holdout paths remain rejected and T20 candidate fields remain unchanged by dataset binding.

### 2026-05-07 - T20 - Second Research Candidate Registration Packet

- Scope: `src/entropy/research/candidate.py`, `src/entropy/research/__init__.py`, `docs/research/second-packet/CANDIDATE_PACKET.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_second_research_packet.py`
- Why this work happened: human approval after T19 requested more evidence, so Phase 6 opens archive-only expansion with a second distinct candidate
- Decisions applied: `docs/governance/research_firewall.md`; `docs/governance/experiment_readiness_gate.md`; `docs/governance/hypothesis_families.md`; `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`
- Evidence collected: T20 acceptance tests passed (`11 passed`); full reset baseline `362 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T21 Second Archive Dataset Manifest and Hash Binding
- Notes for next agent: T20 is candidate-only and not registered or evaluated; it uses Structure Levels, distinct from the first Volatility Compression candidate, and preserves all no-claim/no-live/no-holdout boundaries.

### 2026-05-07 - T19 - First Research Packet Review

- Scope: `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `tests/reset/test_first_research_packet_review.py`
- Why this work happened: close the first research evidence packet block with a review artifact, audit index row, validation record, limitations, and next human decision point
- Decisions applied: `docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md`; `docs/audit/RESET_REVIEW.md`
- Evidence collected: T19 acceptance tests passed (`3 passed`); full reset baseline `351 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: stop for human decision unless explicitly instructed to open a new research block or gate discussion
- Notes for next agent: first packet block is complete; holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, and OOS/performance remain unapproved.

### 2026-05-07 - T18 - First Research Evidence Packet

- Scope: `src/entropy/evidence/first_research_packet.py`, `src/entropy/evidence/__init__.py`, `docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_first_research_packet.py`
- Why this work happened: generate the first deterministic archive-only research evidence packet from the candidate, manifest, and archive evaluation outputs
- Decisions applied: `docs/audit/RESET_REVIEW.md`; `docs/EVIDENCE_INDEX.md`; T11 phase-gate packet boundary; T17 archive evaluation harness
- Evidence collected: T18 acceptance tests passed (`20 passed`); full reset baseline `348 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T19 First Research Packet Review
- Notes for next agent: T18 creates a concrete packet artifact but remains no-claim; it fails missing referenced artifacts or unresolved hashes and preserves blocked holdout, OOS/performance, phase-gate, production, capital-ready, live-feed, and broker/exchange approvals.

### 2026-05-07 - T17 - Archive Evaluation Harness Wiring

- Scope: `src/entropy/research/evaluation.py`, `src/entropy/research/__init__.py`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_first_research_packet.py`
- Why this work happened: wire the first candidate and archive dataset manifest through a deterministic archive-only evaluation surface that records leakage, SimBroker, attribution, and no-claim evidence
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/audit/PHASE3_REVIEW.md`; T09 SimBroker evidence; T10 attribution boundary evidence; T15-T16 first packet contracts
- Evidence collected: T17 acceptance tests passed (`17 passed`); full reset baseline `345 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T18 First Research Evidence Packet
- Notes for next agent: T17 is heavy evidence and remains archive-only; the harness refuses unresolved dataset/code/policy/parameter hashes, does not create an OOS label, and emits separated attribution streams with no performance conclusion.

### 2026-05-07 - T16 - Archive Dataset Manifest and Hash Binding

- Scope: `src/entropy/research/manifest.py`, `src/entropy/research/__init__.py`, `docs/research/first-packet/DATASET_MANIFEST.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_first_research_packet.py`
- Why this work happened: bind the first research candidate to an archive-only dataset manifest with deterministic aggregate hashes and explicit holdout exclusion
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/IMPLEMENTATION_CONTRACT.md#leakage-and-holdout-boundary`; T08 dataset/hash and holdout guard evidence; T15 candidate packet contract
- Evidence collected: T16 acceptance tests passed (`14 passed`); full reset baseline `342 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T17 Archive Evaluation Harness Wiring
- Notes for next agent: T16 added manifest binding only; it excludes holdout paths and preserves the T15 hypothesis text, family, and frozen parameters when replacing the candidate dataset hash placeholder with the aggregate archive dataset hash.

### 2026-05-07 - T15 - First Research Candidate Registration Packet

- Scope: `src/entropy/research/`, `docs/research/first-packet/CANDIDATE_PACKET.md`, `tests/integration/test_first_research_packet.py`
- Why this work happened: create the first narrow archive-only preregistration candidate for the Phase 5 research evidence packet block
- Decisions applied: `docs/governance/research_firewall.md`; `docs/governance/experiment_readiness_gate.md`; `docs/governance/hypothesis_families.md`; `docs/bridges/hypothesis-backtest.md`
- Evidence collected: T15 acceptance tests passed (`11 passed`); full reset baseline `339 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T16 Archive Dataset Manifest and Hash Binding
- Notes for next agent: T15 is candidate-only and not registered or evaluated; hash placeholders are present for dataset, code, policy, and parameter binding, and no holdout, live feed, broker/exchange, production, capital-ready, or OOS/performance surface is approved.

### 2026-05-07 - PHASE5 - First Research Evidence Packet Block Opened

- Scope: `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: human decision after T14 opened a new block focused on a concrete research result rather than a faster product MVP
- Decisions applied: `docs/audit/RESET_REVIEW.md`; `docs/core/PROTOCOL_SPEC.md`; `docs/governance/research_firewall.md`
- Evidence collected: documentation contract update; validation pending for first implementation task T15
- Follow-ups: start T15 First Research Candidate Registration Packet
- Notes for next agent: Phase 5 target is one registered, hash-bound, archive-only, leakage-checked research evidence packet; it must remain no-claim and cannot approve holdout, live feeds, broker integration, production, capital-ready, or OOS/performance labels.

### 2026-05-07 - T14 - Reset Strategy Closure Review

- Scope: `docs/audit/RESET_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `tests/reset/test_reset_closure.py`
- Why this work happened: close the reset implementation block with a strategy review, audit index update, and next-block recommendation grounded in current evidence
- Decisions applied: `docs/EVIDENCE_INDEX.md`; `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence collected: T14 acceptance tests passed (`3 passed`); full reset baseline `328 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: reset implementation awaits human decision after T14
- Notes for next agent: no open findings remain; no holdout, live feed, broker, production, capital-ready, or OOS/performance claim surface is approved by this closure.

### 2026-05-07 - T13 - Hypothesis Backtest Bridge Design

- Scope: `docs/bridges/hypothesis-backtest.md`, `tests/integration/test_hypothesis_bridge_design.py`
- Why this work happened: define a design-only bridge from research-assist hypothesis drafts to registered, hash-bound, leakage-safe evaluation objects without enabling autonomous strategy execution
- Decisions applied: `docs/governance/research_firewall.md`; `docs/core/CHARTER.md`
- Evidence collected: T13 acceptance tests passed (`3 passed`); full reset baseline `325 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T14 Reset Strategy Closure Review
- Notes for next agent: T13 is documentation-only; drafts remain research-only until human registration, hash binding, readiness, leakage, holdout, and no-claim boundaries are satisfied.

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
