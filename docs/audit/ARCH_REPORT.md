---
# ARCH_REPORT — Cycle 2
_Date: 2026-05-03_

---

## Scope Note

This report covers the Cycle 2, Step 2 (Architecture Review) scope as defined in META_ANALYSIS.md. Implementation status at review time: T01 (Project Skeleton), T02 (CI Setup), and T03 (Smoke Tests) are complete. All other components exist only as empty stub packages (`__init__.py` docstrings). The current code surface is therefore primarily structural — directory layout, package declarations, CLI skeleton, tracing module, metrics stubs, and model stubs. Reviews against contract rules are assessed against what exists; DRIFT and VIOLATION verdicts cite the specific gap. Stubs that correctly establish the right boundary are noted as PASS-STUB (compliant skeleton, no substantive code to violate yet).

No ADR files exist under `docs/adr/` at this time.

---

## Component Verdicts

| Component | Verdict | Note |
|-----------|---------|------|
| Trial Registry (`entropy/registry/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only; no logic to drift yet |
| SimBroker (`entropy/simbroker/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only |
| Walk-Forward Harness (`entropy/walkforward/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only |
| P&L Attribution Engine (`entropy/attribution/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only |
| Governance State Machine (`entropy/governance/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only |
| Data Pipeline (`entropy/data/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only |
| Statistical Analysis (`entropy/stats/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only |
| Phase Gate Evidence (`entropy/evidence/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only |
| Database Layer (`entropy/db/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only; no ORM models yet |
| CLI (`entropy/cli.py`) | PASS | Thin entry point only; `version` command delegates to `__version__`; no business logic present; correctly confined to CLI layer |
| Models (`entropy/models/`) | PASS-STUB | Three model files exist as empty stubs; Pydantic models not yet defined; correct placement |
| Hashing (`entropy/hashing/`) | PASS-STUB | Correct layer placement; `__init__.py` stub only |
| Tracing (`entropy/tracing.py`) | PASS | Shared tracing module exists at the declared path; `get_tracer()` function present; single module pattern enforced |
| Metrics (`entropy/metrics.py`) | PASS | Stub counters/histogram at declared path; no-op implementation correct for Phase 0 |
| Smoke Tests (`tests/smoke/test_smoke.py`) | PASS | Validates subpackage importability, CI shape, pyproject deps, .gitignore, PostgreSQL service declaration; no business-logic leakage into tests |
| Test Fixtures (`tests/conftest.py`) | PASS | `postgres_connection` fixture uses parameterized `text("SELECT 1")`; skips cleanly when `DATABASE_URL` unset; correct DB isolation pattern |

---

## Contract Compliance

| Rule | Verdict | Note |
|------|---------|------|
| SQL Safety — parameterized queries only | PASS | Only SQL in scope is `text("SELECT 1")` in conftest.py; correctly uses `text()` with no interpolation |
| Authorization — single-tenant; unrestricted paths documented | PASS | Single-tenant design reflected in code; no auth deferral introduced |
| PII Policy — no PII in logs, spans, metrics, errors | PASS | No logging present yet; no PII fields in any stub |
| Credentials and Secrets — env vars only; no secrets in source | PASS | `DATABASE_URL` read from `os.getenv()`; no hardcoded credentials; `.env` in `.gitignore` confirmed by smoke test |
| Shared Tracing Module — single `entropy/tracing.py`, `get_tracer()` only | PASS | `entropy/tracing.py` exists with single `get_tracer()` function; no inline noop tracers observed in any module |
| CI Gate — must pass before merge | PASS | `ci.yml` declares ruff, pyright, pytest pipeline; smoke test verifies required commands in order |
| OBS-1 — every external call wrapped in span | PASS-STUB | No external calls implemented yet; shared tracer module boundary is correctly in place |
| OBS-2 — success/error counters and latency histograms | PASS-STUB | `entropy/metrics.py` stubs present; activation deferred (all profiles OFF); acceptable for Phase 0 |
| OBS-3 — `entropy health` CLI command | DRIFT | `entropy health` command is not yet present in `entropy/cli.py`; only `version` command exists. ARCHITECTURE.md §Observability declares this command as required. It is not a Phase 0 exit criterion per tasks.md but is a declared architectural contract. |
| Registry Append-Only — INSERT-only on `trial_registry` and `governance_events` | PASS-STUB | DB layer not yet implemented; constraint not violated by stubs |
| Run Reproducibility — five-field RunRecord | PASS-STUB | Walk-forward runner not yet implemented |
| OOS Separation Enforcement — `LeakageError` / `LeakageBlockError` guard | PASS-STUB | Walk-forward harness not yet implemented |
| Hash Determinism — SHA-256(sorted rows + schema fingerprint) | PASS-STUB | Hashing module not yet implemented |
| Net Sharpe Stream Boundary — only (a)+(b)+(c); stream (d) excluded | PASS-STUB | Attribution engine not yet implemented |
| Phase Gate Human Approval — `GovernanceEvent` PHASE_GATE APPROVED required | PASS-STUB | Phase gate evidence generator not yet implemented |
| Language Escalation Control — Python only without ADR | PASS | Only Python present; no foreign language or FFI introduced |
| Mandatory Pre-Task Protocol — pytest + ruff before implementation | PASS | CODEX_PROMPT.md records baseline; protocol instructions present |
| Forbidden: string interpolation in SQL | PASS | No SQL string interpolation present |
| Forbidden: UPDATE/DELETE on append-only tables | PASS-STUB | DB layer not yet implemented |
| Forbidden: runtime tier escalation without ARCHITECTURE.md update | PASS | No tier escalation observed |
| Forbidden: TODO without task reference | PASS | No TODO comments found in any source file |
| Forbidden: commented-out code | PASS | No commented-out code found |
| Forbidden: OOS label before T19 leakage check | PASS-STUB | No OOS labeling implemented yet |
| Forbidden: writing to trial_registry without all hashes | PASS-STUB | Registry write path not yet implemented |
| Forbidden: modifying PROTOCOL_SPEC/CHARTER/GLOSSARY without human approval | PASS | No modifications to these files detected in this cycle |

---

## ADR Compliance

| ADR | Verdict | Note |
|-----|---------|------|
| (none) | N/A | `docs/adr/` directory does not exist; no ADRs filed. ARCHITECTURE.md and IMPLEMENTATION_CONTRACT.md both require an ADR before any language-escalation or IMPLEMENTATION_CONTRACT change. No escalation has occurred so the absence is not itself a violation, but the directory should be created to make the declared governance path operational. |

---

## Architecture Findings

### ARCH-1 [P2] — `entropy health` Command Missing from CLI

Symptom: `entropy/cli.py` does not implement the `entropy health` command declared in `docs/ARCHITECTURE.md §Observability` and `docs/IMPLEMENTATION_CONTRACT.md §OBS-3`.

Evidence: `entropy/cli.py:1-27` — only `version` command present; no `health` subcommand.

Root cause: T01 (Project Skeleton) established a minimal CLI scaffold. The `health` command was not included in the skeleton tasks T01-T03 scope. No tasks.md task currently owns its implementation.

Impact: OBS-3 contract violation when the system is deployed. The health check is also the declared mechanism for exposing staleness information (last ingest timestamp) rather than application logs. Until implemented, the observability contract is incomplete.

Fix: Add `entropy health` command to `entropy/cli.py` implementing PostgreSQL connectivity and DuckDB availability checks returning `{"status": "ok"}` or `{"status": "degraded", "checks": [...]}`. Assign to a task in tasks.md before Phase 0 exit gate.

---

### ARCH-2 [P2] — `docs/adr/` Directory Absent; ADR Governance Path Not Operational

Symptom: `docs/ARCHITECTURE.md §Language Escalation Policy` and `docs/IMPLEMENTATION_CONTRACT.md §Language Escalation Control` both require an ADR in `docs/adr/` before any non-Python language or IMPLEMENTATION_CONTRACT change. The directory does not exist.

Evidence: `find /home/gdev/entropy_protocol/docs/adr/` returns no such directory.

Root cause: No ADR has been needed yet; the directory was not created as part of T01-T03.

Impact: If a language-escalation ADR becomes needed, there is no canonical directory to place it. The governance path is declared but not bootstrapped. Agents following the contract who check for `docs/adr/` will find it absent, creating ambiguity.

Fix: Create `docs/adr/` directory (a `.gitkeep` or a README stub is sufficient) to make the declared governance path structurally present. No ADR content is needed until an escalation occurs.

---

### ARCH-3 [P1] — Phase Gate Inconsistency: Phase 1 Implementation Active While Protocol-Level P0 Findings Remain Open (Inherited from META_ANALYSIS MG-06)

Symptom: `docs/CODEX_PROMPT.md` records Phase: 1 with T01-T03 complete and T04 as next task. `docs/audit/REVIEW_REPORT.md` (Cycle 1) states "Phase 0 exit certification remains blocked" and "Phase 1 entry and later phases remain blocked until all P0 are remediated."

Evidence: `docs/CODEX_PROMPT.md:5` ("Phase: 1"); `docs/audit/META_ANALYSIS.md §MG-06`; `docs/audit/REVIEW_REPORT.md` P0 finding list (F-1, F-2, F-4, F-5, F-30, F-31 Inherited-Open or Partial-Mitigation).

Root cause: `docs/audit/PHASE1_AUDIT.md` (2026-05-01) passed a pre-implementation audit of the engineering documentation layer (ARCHITECTURE.md, spec.md, tasks.md, CODEX_PROMPT.md, IMPLEMENTATION_CONTRACT.md, ci.yml). This is a distinct audit scope from the protocol-specification audit. No document records a formal scope-separation decision or Spec Owner waiver permitting Phase 1 engineering to proceed while protocol-level P0 findings remain open.

Impact: Engineering implementation proceeds on scaffolding whose protocol-level correctness (kill criteria arithmetic, CI formulae, K3 trigger semantics) has not been formally confirmed. Any code that encodes a protocol formula (e.g., N_eff, BR_long, Sharpe CI, P1/P3 thresholds) may encode an incorrect or unresolved value. This is a governance integrity issue, not a code defect in the current stub state — but it will become a code defect at T04 and beyond.

Fix: Spec Owner must formally document one of: (a) scope separation decision — PHASE1_AUDIT.md scope is sufficient for Phase 1 engineering start; protocol P0 findings are a parallel track; or (b) resolution plan — P0 findings F-1, F-2, F-4, F-5, F-30, F-31 must be resolved before any task that encodes a protocol formula (approximately T08, T15, T21, T22, T23). Record the disposition in `docs/DECISION_LOG.md` and `docs/CODEX_PROMPT.md §Open Findings`.

---

### ARCH-4 [P2] — ARCHITECTURE.md File Layout Does Not Match Declared RDL / Governance Documents

Symptom: `docs/ARCHITECTURE.md §Component Table` and the File Layout tree do not include the RDL (Research Discovery Layer), Research Firewall, Experiment Readiness Gate, Research Portfolio Monitor, or Governor components — all of which are active in `docs/governance/` and declared in PROTOCOL_SPEC.md v1.5/v1.6.

Evidence: `docs/ARCHITECTURE.md:113-128` (Component Table); `docs/governance/` directory containing `research_firewall.md`, `experiment_readiness_gate.md`, `hypothesis_families.md`, `governor.md`, `research_portfolio_monitor.md`; META_ANALYSIS.md §MG-08.

Root cause: ARCHITECTURE.md was authored as the implementation architecture document and focuses on the software implementation layer (T01-T24). The protocol-level governance components (RDL, RPM, Research Firewall) are specified in `docs/governance/` and `docs/architecture/` but were not mapped into the implementation component table or the file layout. This creates a gap: a developer reading ARCHITECTURE.md will not see these components and will not know how they map to implementation modules.

Impact: Phase 1 tasks that implement Experiment Readiness Gate (`entropy/registry/gate.py`) and Governance State Machine (`entropy/governance/state_machine.py`) are already in the declared file layout — but their relationship to the protocol-level governance documents (Research Firewall boundary, RPM read-only constraint, RDL attestation) is not documented in ARCHITECTURE.md. This increases the risk that implementations will not enforce the Research Firewall boundary or the RPM non-write constraint.

Fix: Add a section to `docs/ARCHITECTURE.md` mapping protocol-level governance components to their implementation modules, noting which protocol constraints each module must enforce. Specifically: Research Firewall boundary → `entropy/registry/gate.py` + `entropy/evidence/`; RPM read-only constraint → documented as out-of-scope for v1 implementation with explicit note.

---

### ARCH-5 [P2] — ERA0_SPEC.md Authority Status Undefined (Inherited from META_ANALYSIS MG-09)

Symptom: `docs/core/ERA0_SPEC.md` exists in the core directory alongside CHARTER.md and PROTOCOL_SPEC.md but is not referenced anywhere in ARCHITECTURE.md, spec.md, README.md, CODEX_PROMPT.md, or any audit document.

Evidence: File confirmed present at `docs/core/ERA0_SPEC.md`; no cross-references found (META_ANALYSIS.md §MG-09).

Root cause: The file's origin, authority level, and relationship to the active spec set were never declared.

Impact: If ERA0_SPEC.md contains rules that differ from or extend PROTOCOL_SPEC.md v1.6, those rules are outside the audit pipeline and could silently conflict with implementation. Codex agents reading only the declared canonical sources will miss it.

Fix: Spec Owner must either: (a) add ERA0_SPEC.md to the canonical document set with declared authority and scope, or (b) move it to `docs/archive/` and record the disposition in `docs/DECISION_LOG.md`.

---

### ARCH-6 [P2] — README.md Phase Status Stale; ARCHITECTURE.md and spec.md Not in Documentation Map (Inherited from META_ANALYSIS MS-04, MG-10)

Symptom: `docs/README.md` states "Current Phase: Phase 0 (active)" while CODEX_PROMPT.md states Phase: 1. Additionally, `docs/ARCHITECTURE.md` and `docs/spec.md` — both authoritative implementation documents — are absent from README.md's Documentation Map table.

Evidence: `docs/README.md` Current Phase section; `docs/CODEX_PROMPT.md:5`; META_ANALYSIS.md §MS-04 and §MG-10.

Root cause: README.md was not updated when Phase 1 implementation began. The Documentation Map was written before ARCHITECTURE.md and spec.md existed.

Impact: Developers and AI agents loading context via README.md will not discover ARCHITECTURE.md or spec.md, and will incorrectly believe Phase 0 is still active. This is the primary entry point document.

Fix: Update README.md to: (a) set Current Phase to Phase 1, (b) add `docs/ARCHITECTURE.md` and `docs/spec.md` to the Documentation Map with their authority descriptions.

---

## Right-Sizing / Runtime Checks

| Check | Verdict | Note |
|-------|---------|------|
| Solution shape still appropriate | PASS | Hybrid (Deterministic subsystem + Workflow orchestration) remains correct for Phase 0/1 scope; no LLM in runtime path; no over-architecture introduced |
| Deterministic-owned areas remain deterministic | PASS | All stubs correctly establish deterministic boundaries; no LLM calls or non-deterministic logic introduced in any current file |
| Runtime tier unchanged / justified | PASS | T1 (bounded worker); no shell mutation, no privileged actions, no long-lived mutable state beyond PostgreSQL; conftest.py uses `os.getenv("DATABASE_URL")` — correct T1 pattern |
| Human approval boundaries still valid | PASS | Phase gate, trial admission, spec change, and RBE activation approval gates declared in ARCHITECTURE.md; not yet implemented in code (stubs); no boundary violation possible at current stub state |
| Minimum viable control surface still proportionate | PASS | Five declared control points (trial preregistration gate, OOS separation, P&L stream boundary, append-only registry, hash determinism) are all in scope for Phase 0; none have been relaxed or removed |
| Research Firewall boundary intact | PASS | No AI-generated signal enters any code path; all runtime computation is deterministic stub; Research Firewall is a design-time constraint not yet violated by implementation |

---

## Research Firewall Boundary

**Verdict: PASS**

At the current implementation state (T01-T03 complete, all domain components are empty stubs), no AI-generated signal can enter portfolio routing. No Trial Registry, no walk-forward runner, no attribution engine, and no OOS evaluation path exist in code. The Research Firewall boundary is structurally enforced by absence of implementation rather than by active code gates. The boundary will require active code enforcement beginning with T09 (Trial Registry write path) and T10 (Experiment Readiness Gate). ARCH-4 above flags the need to document the Research Firewall enforcement mapping in ARCHITECTURE.md before those tasks are implemented.

RDL scaffolding status: No RDL-specific code exists. The architecture correctly declares RDL attestation as deterministic and Phase 0 RDL activity as scaffolding-only (no signal generation, no OOS claims, no portfolio routing). This constraint is respected by the current stub state.

---

## Capability Architecture Checks

**Retrieval architecture** — SKIP. RAG Status = OFF.

**Tool-Use architecture** — SKIP. Tool-Use Status = OFF.

**Agentic architecture** — SKIP. Agentic Status = OFF.

**Planning architecture** — SKIP. Planning Status = OFF.

---

## Doc Patches Needed

| File | Section | Change |
|------|---------|--------|
| `docs/README.md` | Current Phase | Update from "Phase 0 (active)" to "Phase 1 (active)" |
| `docs/README.md` | Documentation Map | Add `docs/ARCHITECTURE.md` and `docs/spec.md` with authority descriptions |
| `docs/ARCHITECTURE.md` | Component Table or new section | Add protocol-level governance component mapping (Research Firewall, ERG, RPM, RDL) to implementation modules |
| `docs/ARCHITECTURE.md` | (implied) | Add `docs/adr/` to File Layout tree once directory is created |
| `docs/CODEX_PROMPT.md` | Open Findings | Record ARCH-3 (phase gate inconsistency) as an open finding pending Spec Owner disposition |
| `docs/adr/` | (directory) | Create directory with `.gitkeep` or index stub to make the declared ADR governance path operational |

---

## Governance Escalation Required

**MG-06 / ARCH-3 — Phase Gate Inconsistency** is a P1 finding requiring Spec Owner disposition before this report is accepted. The finding is not a code defect at the current stub state but will become one at T04 and beyond if protocol-level P0 arithmetic findings (BR_long, Sharpe CI derivation, K3 trigger semantics) remain unresolved when the corresponding implementation tasks are executed.

The Spec Owner must record a written disposition in `docs/DECISION_LOG.md` addressing: whether PHASE1_AUDIT.md scope is formally accepted as sufficient for Phase 1 engineering start, and what conditions gate implementation of formula-encoding tasks (T08, T15, T21, T22, T23).

---

*Cycle: 2 | Step: 2 (Architecture Review) | Pipeline: v1.0 | Date: 2026-05-03*
*Spec-of-record: PROTOCOL_SPEC.md v1.6, CHARTER.md v5.1*
*Implementation state: T01-T03 complete; T04 next*
*ADRs: none filed*
*Output: `docs/audit/ARCH_REPORT.md`*
