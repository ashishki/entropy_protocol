# CODEX_PROMPT.md — Signal Analytics Sandbox

Version: 2.26
Date: 2026-05-07
Phase: 9

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

- **Phase:** 9 (Phase 10 draft automation scoped; phase boundary not advanced)
- **Baseline:** 84 passing tests, 0 skipped
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
- **Pilot development loop:** `docs/PILOT_DEVELOPMENT_LOOP_RU.md`

---

## Next Task

SAS-AUTO-001: Seed Labels For bablos79 Draft Parser

Phase 10 is a narrow deterministic draft-extraction assistant phase. The
Orchestrator should dispatch `SAS-AUTO-001` from `docs/tasks.md` next.
After seed labels, run `SAS-AUTO-001B` before implementing parser code so the
author-specific lexicon is discovered offline and human-approved.

Immediate instruction:
- Create `docs/pilot/BABLOS79_LABEL_SEED.md` with 10-15 representative rows
  sampled from `workspace/captures/bablos79/`.
- Do not implement parser code until the seed labels and
  `docs/pilot/bablos79_APPROVED_LEXICON.md` exist.
- Do not modify product code.
- Keep automation draft-only: no approved ledger writes without human review.
- Do not start bot/SaaS/private scraping/LLM-truth expansion. Frontier-model
  usage is allowed only as offline lexicon-candidate discovery in
  `SAS-AUTO-001B`; it must not become runtime extraction truth.

Closeout digest for the Orchestrator:
- T20 implemented the gated LLM extraction adapter with fixed mock clients in CI.
- Activation requires both `SIGNAL_SANDBOX_ENABLE_LLM=1` and per-run `llm_approved=True`.
- Every successful result is `draft_pending_review` with `adapter_id="llm/<provider>/<model>"`.
- Paid Claude-style calls enforce `SIGNAL_SANDBOX_COST_CAP_USD` before invoking once budget is exhausted.
- `write_ledger` rejects direct LLM-sourced records unless `reviewer_id` is present.
- Heavy-task evidence is archived at `docs/audit/HEAVY_T20_EVIDENCE.md`.
- Phase 8 archive is `docs/archive/PHASE8_REVIEW.md`.
- Phase 9 archive is `docs/archive/PHASE9_REVIEW.md`.

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

## Summary State

Phase 1 through Phase 8 are complete. The deterministic sandbox baseline is 84
passing tests, 0 skipped; `ruff check src/ tests/` and `pyright` pass locally.
The implemented surface includes:

- installable Python package and CLI skeleton;
- source manifest, capture loader, signal record schema, ledger I/O, dedup, and
  ambiguity handling;
- deterministic price provider interface, operator-file provider, exchange
  public provider, yfinance prototype provider, snapshot persistence, outcome
  matcher, aggregator, and Markdown report renderer;
- manual, rule, and gated LLM extraction adapters;
- Phase 4 through Phase 8 deep review archives and heavy-task evidence for
  T12, T14, and T20.

Phase 9 is now a validation-first Telegram pilot loop for the three
operator/customer-provided public Telegram sources in `docs/PILOT_LOG.md`.
Product-code expansion remains blocked until pilot evidence identifies a
measured bottleneck.

Current Phase 9 evidence update: `bablos79` has 60 public text captures in
`workspace/captures/bablos79/`, validated by `load_captures(Path("workspace"),
"bablos79")`. Manual extraction has not run yet.

---

## Completed Tasks

- 2026-05-07 — SAS-PILOT-001 Pilot Scope: created
  `docs/pilot/PILOT_SCOPE.md` for the three public Telegram pilot sources,
  selected the first source, defined target signal counts, scope exclusions,
  and customer-centered success/kill criteria. Baseline after: 84 passed,
  0 skipped. Review: skipped (doc-only patch per orchestrator review exception).
- 2026-05-07 — SAS-PILOT-002 Methodology V0: created
  `docs/pilot/METHODOLOGY_V0.md` with required capture fields, signal
  qualification rules, extraction statuses, ambiguity handling, deterministic
  outcome semantics, price provenance, and report guardrails. Baseline after:
  84 passed, 0 skipped. Review: skipped (doc-only patch per orchestrator review
  exception).
- 2026-05-07 — SAS-PILOT-003 First Source Capture Plan And Log: created
  `docs/pilot/CAPTURE_LOG.md` for `https://t.me/bablos79` with capture method,
  required evidence fields, captured/skipped/blocked/pending status definitions,
  skip/block reason codes, and a pending operator-input row because no real
  captures are present. Baseline after: 84 passed, 0 skipped. Review: skipped
  (doc-only patch per orchestrator review exception).
- 2026-05-07 — SAS-PILOT-004 First Source Manual Extraction Log: created
  `docs/pilot/EXTRACTION_LOG.md` for `https://t.me/bablos79` with required
  extraction fields, status counts, a pending capture row, explicit blocker on
  operator-supplied public captures, and no fabricated signal candidates.
  Baseline after: 84 passed, 0 skipped. Review: skipped (doc-only patch per
  orchestrator review exception).
- 2026-05-07 — SAS-PILOT-005 First Source Report V0: created
  `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md` because no real captures,
  extraction rows, approved ledger, price snapshot, or outcomes exist. The memo
  records source, planned audit window, zero counts, blocker, limitations, and
  non-advice / historical-only language. Baseline after: 84 passed, 0 skipped.
  Review: skipped (doc-only patch per orchestrator review exception).
- 2026-05-07 — SAS-PILOT-006 Customer Feedback And Payment Signal Log: created
  `docs/pilot/CUSTOMER_FEEDBACK.md` and `docs/pilot/PAYMENT_SIGNAL_LOG.md` with
  pending rows, past-behavior feedback questions, objection/status definitions,
  payment-signal categories, refusal reasons, and Telegram-delivery-as-format
  guardrails. Baseline after: 84 passed, 0 skipped. Review: skipped (doc-only
  patch per orchestrator review exception).
- 2026-05-07 — SAS-PILOT-007 Repeat Or Automate Decision: created
  `docs/pilot/PILOT_DECISION.md` and recorded D-014. Verdict:
  stop/defer automation until real public captures are supplied for the first
  source. No new engineering phase is approved. Baseline after: 84 passed,
  0 skipped. Review: Phase 9 deep review PASS.
- 2026-05-07 — Public Capture Parse for bablos79: parsed 60 public text posts
  from unauthenticated Telegram `/s/` pages into
  `workspace/captures/bablos79/`, wrote
  `docs/pilot/bablos79_CAPTURE_MANIFEST.json`, updated capture/extraction logs,
  and revised D-014 to continue manual extraction while deferring automation.
- 2026-05-07 — Auto Extraction Development Plan: created
  `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`, appended Phase 10
  `SAS-AUTO-001`, `SAS-AUTO-001B`, and `SAS-AUTO-002..005` to
  `docs/tasks.md`, and recorded D-015. Added
  `SAS-AUTO-001B` and D-016 for offline frontier-model author lexicon discovery
  with human approval before parser implementation. Next task: seed labels.

---

## Completed Task Archive

Older detailed task entries were compacted on 2026-05-07 after reaching the
orchestrator compaction threshold. Full task definitions remain in
`docs/tasks.md`; review archives remain in `docs/archive/`.

| Range | Summary | Final baseline / archive |
|-------|---------|--------------------------|
| T01-T03 | Project skeleton, CI setup, and smoke-test baseline. | 18 passed, 0 skipped; `docs/archive/PHASE1_REVIEW.md` |
| T04-T06 | Source manifest, capture loader, and signal record schema. | 31 passed, 0 skipped; `docs/archive/PHASE2_REVIEW.md` |
| T07-T08 | Ledger I/O, deterministic deduplication, and ambiguity flagging. | 38 passed, 0 skipped; `docs/archive/PHASE3_REVIEW.md` |
| T09-T11 | Price provider interface, operator-file provider, and immutable snapshot persistence. | 47 passed, 0 skipped; `docs/archive/PHASE4_REVIEW.md` |
| T12-T14 | Outcome matching, aggregation, and deterministic Markdown reports. | 65 passed, 0 skipped; `docs/archive/PHASE5_REVIEW.md`; heavy evidence T12/T14 |
| T15-T17 | Extraction adapter ABC, manual extraction, and rule extraction templates. | 72 passed, 0 skipped; `docs/archive/PHASE6_REVIEW.md` |
| T18-T19 | Public exchange OHLCV provider and yfinance prototype provider. | 77 passed, 0 skipped; `docs/archive/PHASE7_REVIEW.md` |
| T20 | Gated LLM extraction adapter with cost cap and human-review ledger guard. | 84 passed, 0 skipped; `docs/archive/PHASE8_REVIEW.md`; heavy evidence T20 |

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

- 2026-05-07 — LLM extraction acceptance rate fixture baseline:
  `1.000000` (`3/3` drafts approved without modification) in
  `tests/eval/test_llm_extraction_quality.py`.

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
