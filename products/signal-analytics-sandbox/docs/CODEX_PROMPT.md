# CODEX_PROMPT.md — Signal Analytics Sandbox

Version: 2.9
Date: 2026-05-07
Phase: 6

---

## Phase 0 Gate Status

Engineering Phase 1 (T01+) may begin because both rows below are marked `acknowledged` by the operator.

| Gate | Status | Evidence | Acknowledged date |
|------|--------|----------|-------------------|
| SAS-001: Paid Pilot Demand Validation | acknowledged | `docs/PILOT_LOG.md` | 2026-05-07 |
| SAS-002: Public-Source Legal/Terms Memo | acknowledged | `docs/legal_risk_memo.md` | 2026-05-07 |

The operator acknowledged the initial pilot scope on 2026-05-07:
`https://t.me/bablos79`, `https://t.me/nemphiscrypts`, and
`https://t.me/pifagortrade`. Twitter / X and Discord are deferred until the
Telegram pilot validates the product hypothesis.

---

## Current State

- **Phase:** 6 (ready for T16)
- **Baseline:** 68 passing tests, 0 skipped
- **Ruff:** `ruff check src/ tests/` passes
- **Pyright:** `pyright` passes
- **Last CI run:** local CI-equivalent commands pass; GitHub run not yet observed
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

**T16: ManualExtractionAdapter**

Inline digest for the Orchestrator:
- Implement the manual extraction adapter using an injected editor command.
- Write a pre-filled template containing every required `SignalRecord` field plus evidence_url and text_sha256.
- Parse the saved template into `ExtractionResult(status="draft_pending_review", record=...)`.
- Return `defer_to_human` with missing-field reasons when required fields are blank.
- Files: see `docs/tasks.md::T16::Files`.
- Applicable rules: PII Policy, Human Approval Boundaries, Pre-Task Protocol.

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
- ADR-001 (`docs/adr/ADR-001-snapshot-serialization.md`) — accepted on 2026-05-07; deterministic Parquet snapshot bytes selected for T09/T11.

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

- 2026-05-07 — T01 Project Skeleton: created installable Python package
  `signal-sandbox`, console script `signal-sandbox`, package subdirectories,
  shared `get_tracer()`, CLI stubs, dependency manifests, and T01 tests.
  Baseline after: 11 passed, 0 skipped. Review: light PASS.
- 2026-05-07 — T02 CI Setup: verified product CI workflow contract with tests
  for trigger branches, Python 3.12, pip cache, command order, install command,
  dev dependencies, and the repository-root workflow bridge needed for GitHub
  to run this product's CI in the monorepo. Baseline after: 18 passed, 0 skipped.
  Review: light PASS.
- 2026-05-07 — T03 Phase 1 Smoke Tests: added tracer singleton test,
  structured JSON logger test, and `signal-sandbox status` temp-workspace smoke
  test. Recorded Phase 1 baseline. Baseline after: 18 passed, 0 skipped.
  Review: light PASS.
- 2026-05-07 — T04 SourceManifest Pydantic Schema: implemented strict
  Pydantic source manifest validation, source type and eligibility enums,
  canonical JSON persistence, and `load_source` rejection for non-approved
  sources. Baseline after: 22 passed, 0 skipped. Review: light PASS.
- 2026-05-07 — T05 Capture Loader: implemented captured post schema, raw-text
  SHA-256 verification, private-source URL rejection, and deterministic batch
  ordering. Baseline after: 26 passed, 0 skipped. Review: light PASS.
- 2026-05-07 — T06 SignalRecord Schema: implemented signal record schema,
  direction enum validation, evaluability semantics, and canonical SHA-256
  dedup-key computation. Baseline after: 31 passed, 0 skipped.
  Review: light PASS.
- 2026-05-07 — T07 Ledger I/O (Parquet): implemented deterministic Parquet
  ledger writes, canonical column order, duplicate dedup-key rejection/force
  flagging, and empty-ledger round-trip behavior. Baseline after: 35 passed,
  0 skipped. Review: light PASS.
- 2026-05-07 — T08 Dedup + Ambiguity Flagging: implemented deterministic
  deduplication and ambiguity flagging with set semantics. Baseline after:
  38 passed, 0 skipped. Review: light PASS.
- 2026-05-07 — T09 PriceDataProvider Abstract Interface: accepted ADR-001,
  implemented `PriceDataProvider`, `PriceSnapshot`, checksum validation, and
  deterministic Parquet snapshot bytes. Baseline after: 41 passed, 0 skipped.
  Review: light PASS.
- 2026-05-07 — T10 OperatorFilePriceProvider: implemented local operator-file
  OHLCV Parquet loading, schema validation, deterministic snapshot creation,
  typed missing/malformed errors, and low-cardinality adapter logging. Baseline
  after: 44 passed, 0 skipped. Review: light PASS.
- 2026-05-07 — T11 PriceSnapshot Persistence + Provenance: implemented
  deterministic snapshot persistence to `snapshots/<snapshot_id>/`, immutable
  re-save semantics, deterministic metadata JSON, and checksum-verifying load.
  Baseline after: 47 passed, 0 skipped. Review: light PASS. Phase 4 deep review:
  `docs/archive/PHASE4_REVIEW.md`.
- 2026-05-07 — T12 Outcome Matching Engine: implemented deterministic
  outcome matching, append-only rule registry, Decimal-based six-place
  banker's rounding, byte-identical outcomes Parquet with rule-registry
  metadata, and heavy evidence at `docs/audit/HEAVY_T12_EVIDENCE.md`.
  Baseline after: 55 passed, 0 skipped. Review: heavy/light PASS.
- 2026-05-07 — T13 Aggregator: implemented deterministic outcome aggregation,
  outcomes Parquet byte input, historical summary JSON bytes, win-rate exclusion
  semantics, Decimal mean/median, and chronological max drawdown. Baseline
  after: 59 passed, 0 skipped. Review: light PASS.
- 2026-05-07 — T14 Markdown Report Generator: implemented deterministic
  Markdown rendering, canonical disclaimer validation, provenance block,
  evidence-rich evaluated/excluded tables, prototype snapshot gating, and heavy
  evidence at `docs/audit/HEAVY_T14_EVIDENCE.md`. Baseline after: 65 passed,
  0 skipped. Review: heavy/light PASS. Phase 5 deep review:
  `docs/archive/PHASE5_REVIEW.md`.
- 2026-05-07 — T15 ExtractionAdapter ABC: implemented `ExtractionAdapter`,
  `ExtractionResult`, status invariants, and model-level evidence preservation
  between `CapturedPost` and draft `SignalRecord`. Baseline after: 68 passed,
  0 skipped. Review: light PASS.

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

- Compliance Status: OFF
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
