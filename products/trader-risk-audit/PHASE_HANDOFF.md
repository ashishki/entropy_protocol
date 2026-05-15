# Phase Handoff - Trader Risk Audit

Date: 2026-05-15

Use this file only for restart/context recovery. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/archive/`,
and `docs/tasks.md`.

## Current State

- Phase: 23 Open-Source Audit Case Bank
- Last completed: T93 CSV Friction Decision Gate
- Active task: T98 Open-Source Source Selection Protocol
- Baseline: 253 pass / 0 skip
- Ruff: clean
- Open findings: none
- Constraint state: T93 deferred real local read-only exchange fetching; Phase
  22 implementation tasks are blocked. Core is paused.
- Branch: product-local working branch

## Next Action

Read:

1. `docs/CODEX_PROMPT.md`
2. `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
3. `docs/tasks.md` Phase 23, T98-T103
4. `docs/AUTOMATED_PILOT_ROADMAP.md`
5. `docs/IMPLEMENTATION_CONTRACT.md`
6. `trader_risk_audit/policy/schema.py`
7. `docs/STARTER_POLICY_PROFILES_RU.md`
8. `docs/audit/PHASE_REPORT_LATEST.md`

Start T98. Create the open-source source selection protocol and case-bank
criteria before adding more packs. T94-T97 are blocked until future
privacy-safe market evidence reopens T93. Phase 17 added deterministic local
`intake_session.json`,
sanitized `schema_profile.json`, safe `intake_report.md`, and Cycle 22 deep
review/archive with no stop-ship items. T74 added
`trader_risk_audit/policy/rule_catalog.py` for supported deterministic rule
types, threshold units, safe descriptions, starter profile applicability, and
availability requirements. T75 added `trader_risk_audit/policy/builder.py`
and `policy build` for deterministic generated `policy.yaml`. T76 added
`policy flow` for structured local rule-builder input and unavailable-rule
explanations. T77 added `policy unsupported append` and
`trader_risk_audit/policy/unsupported_register.py` for sanitized manual-review
limitations. T78 archived Cycle 23 with no stop-ship findings. T79 added
`trader_risk_audit/audit_session/runner.py` and `audit-session run`, which
gates on runnable intake/policy status, runs the deterministic audit internals,
and writes safe complete/blocked `run_status.json` without raw rows in
status/stdout. T80 added `trader_risk_audit/audit_session/artifact_bundle.py`
and `audit-session bundle`, which writes/validates `bundle_index.json` with
safe refs, hashes, status, preview state, and limitation register refs. T81
added `trader_risk_audit/audit_session/reproducibility.py`, which reruns a
session in a separate output directory and writes safe
`reproducibility_status.json` before preview/delivery. T82 archived Cycle 24
with P0:0, P1:0, P2:0 and no stop-ship items.
T83 added `trader_risk_audit/preview/model.py` and `preview build`, which
renders claim-safe redacted previews from bundle refs without source-row ids,
symbols, raw rows, or private output paths in CLI stdout. T84 added eligible
manual paid-pilot CTA packaging without checkout/SaaS/payment processing. T85
added privacy-safe preview conversion events and summary. T86 added local
paid-unlock state transitions with manual evidence references only. T87
archived Cycle 25 with P0:0, P1:0, P2:0 and no stop-ship items. T88 added
`HypothesisFunnelEvent`, combined legacy/new evidence loading, and docs that
separate gate evidence from vanity/demo events.
T89 added `evidence hypothesis-dashboard`, which summarizes legacy and funnel
evidence locally with market/demo separation, ratios, gate status, blocker tags,
and privacy-safe next action output.
T90 added `evaluate_hypothesis_gate`, which returns proceed,
needs_more_evidence, or pivot with concrete reasons and next action.
T91 added `evidence export`, which writes aggregate-only CSV/Markdown evidence
summaries with gate decision, safe tags, source log names, and source log
hashes while rejecting identifiers, phone numbers, credentials, payment ids,
raw-row-like fields, and private paths.
T92 archived Cycle 26 with P0:0, P1:0, P2:0 and no stop-ship items. Do not
implement real exchange network fetching unless T93 explicitly returns proceed.
T93 returned defer because no market customer evidence log shows CSV/export
friction as the binding blocker.

## Guardrails

- Raw private/customer trade data must not be committed.
- Phase 14/15 exchange-import work is complete but should be used only when it
  directly supports the selected real audit artifact or the T93/T94 friction
  gate.
- ADR-002 allows only local read-only historical ingestion.
- No live exchange control, order placement, hosted uploads, hosted storage,
  checkout, order blocking, SaaS expansion, or trading advice.
- Open-source validation must preserve positive, limitation/reject, and
  edge-case examples to avoid cherry-picking.

## Historical Pointers

- Completed through T93. T94-T97 blocked. Active route is T98-T115.
- New active roadmap: `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`.
- Detailed validation command history is in `docs/IMPLEMENTATION_JOURNAL.md`.
- Prior review artifacts are in `docs/archive/`.
