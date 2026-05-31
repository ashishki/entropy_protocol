# Decision Log - Entropy Core

Version: 1.0
Last updated: 2026-05-29

This file is retrieval convenience only. Canonical documents win on conflict.

## Decision Index

| ID | Date | Status | Decision | Why it matters | Canonical source | Supersedes |
|----|------|--------|----------|----------------|------------------|------------|
| D-RESET-001 | 2026-05-07 | Active | Rebuilt the AI Workflow Playbook loop as a governance reset over existing code. | Old workflow state is archived; new docs are active authority. | `docs/legacy/RESET_PLAN.md` | old active workflow state |
| D-RESET-002 | 2026-05-07 | Active | Entropy Core uses Python 3.12 as the active runtime. | Aligns package/tooling with current workspace and portfolio products. | `pyproject.toml`; `docs/ARCHITECTURE.md#tech-stack` | Python >=3.10 / py310 config |
| D-RESET-003 | 2026-05-07 | Active | Capability profiles are OFF for runtime RAG, Tool-Use, Agentic, Planning, and Compliance. | Keeps application runtime deterministic; continuity retrieval remains docs-based. | `docs/ARCHITECTURE.md#capability-profiles` | prior compact profile table |
| D-RESET-004 | 2026-05-07 | Active | Runtime tier is T1 bounded local/CI process with PostgreSQL service dependency. | Matches existing DB/migration/test surface without privileged workers. | `docs/ARCHITECTURE.md#runtime-and-isolation-model` | none |
| D-RESET-005 | 2026-05-07 | Active | Legacy active workflow files moved under `docs/legacy/old-workflow/2026-05-07/`. | Prevents old prompts/logs from controlling the new loop while preserving evidence. | `docs/legacy/CORE_LEGACY_SUMMARY.md` | old active workflow |
| D-RESET-006 | 2026-05-07 | Active | Heavy-task evidence applies to leakage/holdout and attribution stream boundaries. | These are the highest false-claim risk surfaces. | `docs/tasks.md#t08-data-and-leakage-gate-verification`; `docs/tasks.md#t10-attribution-stream-boundary-audit` | none |
| D-ROADMAP-001 | 2026-05-08 | Active | Roadmap phases 7 through 13 are planned direction, and Phase 7 is active. After every phase, the loop must deep-review, fix findings, validate, evaluate and rewrite the roadmap, open the next logical active phase, and continue automatically. | Keeps development strategy visible while allowing pure AI development to proceed without human stops at every phase boundary. | `CODEX_LOOP.md#stop-policy`; `docs/tasks.md#roadmap-governance`; `docs/tasks.md#phase-plan`; `docs/CODEX_PROMPT.md#next-task` | none |
| D-CORE-V2-001 | 2026-05-29 | Active | Operator approved starting Core V2 work and instructed the loop to explicitly select T123 as the next task before continuing. | Lifts the post-T122 roadmap stop only for bounded Core V2 planning/task activation; restricted live, holdout, hosted, public SDK, compliance, and capital surfaces remain blocked. | user instruction 2026-05-29; `docs/tasks.md#t123-core-v2-roadmap-activation`; `docs/CODEX_PROMPT.md#next-step` | Core V1 post-T122 wait gate |

## Legacy Decision Carry-Forward

Durable pre-reset decisions D-027 and D-050 through D-058 are summarized in `docs/legacy/CORE_LEGACY_SUMMARY.md#durable-decisions-to-preserve`. Read the old full decision log only through scoped task `Context-Refs`.
