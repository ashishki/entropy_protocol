# Decision Log - Entropy Core

Version: 1.0
Last updated: 2026-05-07

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

## Legacy Decision Carry-Forward

Durable pre-reset decisions D-027 and D-050 through D-058 are summarized in `docs/legacy/CORE_LEGACY_SUMMARY.md#durable-decisions-to-preserve`. Read the old full decision log only through scoped task `Context-Refs`.
