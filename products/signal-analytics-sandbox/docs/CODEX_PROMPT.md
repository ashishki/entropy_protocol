# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 3.13
Date: 2026-05-31
Phase: 41
Compact restart state only. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Current State

- Phase: 41 (Auto-Validation Validator Stack)
- Baseline: 391 pass / 0 skip
- Ruff: `ruff check src/ tests/ scripts/` passes
- Format: `ruff format --check src/ tests/ scripts/` passes
- Pyright: `.venv/bin/pyright` passes
- Latest completed: `Phase 40 Deep Review`
- Phase 37 decision: `continue_internal_hardening`
- Engineering Phase 1 (T01+) may begin.
- | SAS-001: Paid Pilot Demand Validation | acknowledged |
- | SAS-002: Public-Source Legal/Terms Memo | acknowledged |
- External gate: `approve_internal_only`
- External delivery: not approved
- Current priority: implement independent validator stack.

## Next Task

Active route: Phase 41 auto-validation validator stack.

- Phase 37 baseline: 9 model-reviewed internal candidates, 301-row appendix,
  0 customer-facing rows, buyer conversations blocked.
- Phase 38 outputs: ledger 0 accepted / 5 needs-context / 4 post-factum-only;
  accepted outcomes 0 recomputed / 9 excluded / 0 buyer-demo-safe; redacted
  demo showable_now=false; discovery gate continue_internal_hardening.
- Phase 38 deep review archived at `docs/archive/PHASE38_REVIEW.md`;
  P0/P1/P2 findings: 0/0/0.
- New route: Phases 40-42 build evidence bundles, independent validators,
  strict auto-accept decisions, customer-facing policy gate, and evaluation on
  the current 9 media candidates.
- Completed: Phase 40 evidence contract, evidence bundle schema, validation
  result schema, audit log schema, and deep review.
- Next task: `SAS-AUTOVAL-004` pre-outcome timing validator.
- buyer outreach remains blocked until a later discovery gate explicitly
  approves it.

Read first: `docs/tasks.md` Phases 40-42,
`docs/specs/AUTO_VALIDATION_EVIDENCE.md`, `docs/archive/PHASE40_AUTO_VALIDATION_REVIEW.md`,
`docs/adr/ADR-005-auto-validation-evidence-engine.md`, and Phase 38 clientready artifacts.

## Canonical Artifacts

- Phase 37 review: `docs/archive/PHASE37_PRECLIENT_REVIEW.md`
- Phase 38 review: `docs/archive/PHASE38_REVIEW.md`
- Pre-client packet/appendix/cards/outcomes/gate:
  `docs/pilot/preclient_*`
- Phase 38 artifacts: `docs/pilot/clientready_OPERATOR_MEDIA_LEDGER.md`,
  `docs/pilot/clientready_ACCEPTED_OUTCOMES.md`,
  `docs/pilot/clientready_REDACTED_BUYER_DEMO.md`,
  `docs/pilot/clientready_DISCOVERY_GATE.md`
- Auto-validation contract/schema: `docs/specs/AUTO_VALIDATION_EVIDENCE.md`,
  `src/signal_sandbox/auto_validation/evidence.py`,
  `src/signal_sandbox/auto_validation/results.py`
- Phase 40 review: `docs/archive/PHASE40_AUTO_VALIDATION_REVIEW.md`

## Key Product Facts

- V1 evaluable claims: `bablos79` 14, `nemphiscrypts` 49, `pifagortrade` 107.
- Safety gate covers 14 artifacts, 0 forbidden phrase findings, 0 showable now.
- Model packet has 9 internal candidates and 0 customer-facing rows.
- Candidate outcomes: 4 insufficient fields, 4 post-factum-only, 1 provider gap,
  1 internal RR recompute, 0 market outcomes recomputed.
- Operator media ledger: 0 accepted, 5 needs-context, 4 post-factum-only,
  0 dashboard-safe rows, 0 paid-report-safe rows.
- Accepted outcomes: 0 accepted, 0 recomputed, 9 excluded,
  0 buyer-demo-safe rows.
- Redacted demo: showable_now=false, blocked_internal_only.
- Discovery gate: continue_internal_hardening; ready_for_discovery=false.
- Phase 38 review: Stop-Ship No; P0 0, P1 0, P2 0.
- Main blockers: 0 operator-accepted media claims, 0 dashboard-safe RR rows,
  0 market-outcome recomputed candidates.
- Automation rule: auto-accept requires independent validator proof; model
  review alone remains triage.
- Evidence/result schemas: strict Pydantic contracts with public source class,
  timestamps, checksums, evidence refs, validator versions, deterministic input
  hashes, canonical JSON, and SHA-256 audit hashes.

## Active Guardrails

- Public/operator-authorized sources only.
- No private scraping, access-control bypass, advice, future-profit claims,
  unsupported ranking, marketplace framing, payment flow, or private-source
  promise.
- Unsupported providers/proxies are exclusions, not wins/losses.
- Unreviewed transcript/OCR/chart claims stay out of customer-facing metrics.
- Every buyer-facing artifact requires an explicit gate.
