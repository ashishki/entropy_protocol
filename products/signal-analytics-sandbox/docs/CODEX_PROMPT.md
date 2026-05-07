# CODEX_PROMPT.md — Signal Analytics Sandbox

Version: 1.0
Date: 2026-05-07
Phase: 1 (pending Phase 0 acknowledgement)

---

## Phase 0 Gate Status

Engineering Phase 1 (T01+) MUST NOT begin until both rows below are marked `acknowledged` by the operator.

| Gate | Status | Evidence | Acknowledged date |
|------|--------|----------|-------------------|
| SAS-001: Paid Pilot Demand Validation | pending | `docs/PILOT_LOG.md` (not yet created) | — |
| SAS-002: Public-Source Legal/Terms Memo | pending | `docs/legal_risk_memo.md` (not yet created) | — |

To acknowledge a gate, the operator edits this block — replaces `pending` with `acknowledged`, references the evidence file, and dates the acknowledgement. The Orchestrator refuses to dispatch T01–T20 while either row is pending (per IMPLEMENTATION_CONTRACT §PSR-10).

---

## Current State

- **Phase:** 1 (queued — blocked by Phase 0)
- **Baseline:** 0 passing tests (pre-implementation)
- **Ruff:** not yet configured
- **Pyright:** not yet configured
- **Last CI run:** not yet configured
- **Last updated:** 2026-05-07
- **Session tokens (approx):** not yet tracked
- **Cumulative phase tokens (approx):** not yet tracked

---

## Continuity Pointers

- **Decision log:** `docs/DECISION_LOG.md`
- **Implementation journal:** `docs/IMPLEMENTATION_JOURNAL.md`
- **Evidence index:** deferred in v1 — heavy-task evidence lives in `docs/audit/HEAVY_T{NN}_EVIDENCE.md`
- **Project brief:** `templates/PROJECT_BRIEF.md` (canonical), `docs/PROJECT_BRIEF.md` (pointer)
- **Architecture:** `docs/ARCHITECTURE.md`
- **Spec:** `docs/spec.md`
- **Tasks:** `docs/tasks.md`
- **Implementation contract:** `docs/IMPLEMENTATION_CONTRACT.md`
- **Task-scoped context:** read `Context-Refs` in `docs/tasks.md` before broad searching
- **Legal/risk memo (SAS-002 output):** `docs/legal_risk_memo.md` (created by SAS-002)
- **Pilot log (SAS-001 output):** `docs/PILOT_LOG.md` (created by SAS-001)

---

## Next Task

**Phase 0 — SAS-001: Paid Pilot Demand Validation** (operator-owned, non-codex)

Engineering T01 is queued behind Phase 0. After both Phase 0 gates are acknowledged in the table above, the next task becomes:

**T01: Project Skeleton**

Inline digest for the Orchestrator (when T01 unblocks):
- Pyproject + console-script `signal-sandbox`; Python ≥ 3.12.
- Subpackages: sources/, capture/, extraction/, ledger/, prices/, outcomes/, reports/.
- Shared `get_tracer()` in `src/signal_sandbox/observability.py` (no inline noop spans).
- All subcommands except `status` exit code 2 with "not implemented".
- Files: see `docs/tasks.md::T01::Files`.
- Applicable rules: PSR-1 (no scraping code paths in stubs), Shared Tracing Module (universal), Pre-Task Protocol (universal).

Only send codex to the full ARCHITECTURE.md / IMPLEMENTATION_CONTRACT.md when a task is heavy or touches cross-cutting boundaries.

---

## Fix Queue

empty

<!--
The Fix Queue contains items that must be addressed before the next phase gate but
were deferred from the current task. Format:

- FQ-01: [T-NN] Description. Added: YYYY-MM-DD.
-->

---

## Open Findings

### Open ADRs (block specific phases)
- ADR-001 (`docs/adr/ADR-001-snapshot-serialization.md`) — research pending; **blocks Phase 4 (T09 onward)**. Must reach Status: ACCEPTED before T09 implementation begins.

### Findings from review cycles
none

<!--
### P1 Findings (block next phase gate)
- (none)

### P2 Findings (must resolve within 3 cycles)
- (none)

### P3 Findings (optional)
- (none)
-->

---

## Completed Tasks

none

---

## Profile State: RAG

- RAG Status: OFF
- Active corpora: n/a
- Retrieval baseline: n/a
- Open retrieval findings: none
- Index schema version: n/a
- Pending reindex actions: none
- Retrieval-related next tasks: none
- Retrieval-driven tasks: none

---

## Tool-Use State

- Tool-Use Profile: OFF
- Active tools: n/a
- Tool eval baseline: n/a
- Open tool findings: none

---

## Agentic State

- Agentic Profile: OFF
- Active agent roles: n/a
- Loop termination state: n/a
- Open agentic findings: none

---

## Planning State

- Planning Profile: OFF
- Plan schema version: n/a
- Open plan findings: none

---

## Compliance State

- Compliance Profile: OFF
- Active frameworks: none
- Compliance eval baseline: n/a
- Open compliance findings: none

---

## Evaluation State

### Regression Thresholds

- Default: >15% regression → P0; >5% regression → P1; ≤5% → no finding.
- Apply to extraction acceptance rate (T20) once a baseline is recorded.

### Recorded Baselines

- (none yet)

---

## Heavy-Task Evidence Index

Heavy tasks defined in `docs/tasks.md`:

| Task | Heavy reason | Evidence file (created at task close) |
|------|--------------|----------------------------------------|
| T12  | Outcome matching is the load-bearing reproducibility surface; floating-point determinism + rule-citation correctness must be auditable | `docs/audit/HEAVY_T12_EVIDENCE.md` |
| T14  | Markdown report is the user-facing artifact; disclaimer integrity, provenance, and per-signal evidence are P0 boundaries | `docs/audit/HEAVY_T14_EVIDENCE.md` |
| T20  | LLM extraction adapter introduces a non-deterministic source whose output must never become "truth"; cost-cap and review-gate are load-bearing | `docs/audit/HEAVY_T20_EVIDENCE.md` |

---

## Instructions for Codex

1. Read `docs/IMPLEMENTATION_CONTRACT.md` before starting any task.
2. Read the full task definition in `docs/tasks.md` before writing any code.
3. Read all Depends-On tasks to understand interface contracts.
4. Read the task's `Context-Refs` and the relevant entries in `docs/DECISION_LOG.md` and `docs/IMPLEMENTATION_JOURNAL.md` when the task depends on prior decisions, proof, or findings.
5. Run `python -m pytest tests/ -q` to capture the current baseline before making any changes.
6. Run `ruff check src/ tests/` — must exit 0 before starting. If not, fix in a separate commit, then restart.
7. Write tests before or alongside implementation. Every acceptance criterion has a passing test.
8. Update this file at every phase boundary (new baseline, next task, open findings).
9. Commit with format: `type(scope): description` — one logical change per commit. No `Co-Authored-By` from AI agents.
10. When done: return `IMPLEMENTATION_RESULT: DONE` with the new baseline and what changed.
11. When blocked: return `IMPLEMENTATION_RESULT: BLOCKED` with the exact blocker.
