# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 3.21
Date: 2026-05-31
Phase: 43
Compact restart state only. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Current State

- Phase: 43 (MVP Value Assessment)
- Baseline: 435 pass / 0 skip
- Ruff: `ruff check src/ tests/ scripts/` passes
- Format: `ruff format --check src/ tests/ scripts/` passes
- Pyright: `.venv/bin/pyright` passes
- Latest completed: `MVP Value Run - 2026-05-31`
- Phase 37 decision: `continue_internal_hardening`
- Engineering Phase 1 (T01+) may begin.
- | SAS-001: Paid Pilot Demand Validation | acknowledged |
- | SAS-002: Public-Source Legal/Terms Memo | acknowledged |
- External gate: `approve_internal_only`
- External delivery: not approved

## Next Task

Active route: post-Phase-42 MVP value assessment.

- Phase 37 baseline: 9 model-reviewed internal candidates, 301-row appendix,
  0 customer-facing rows, buyer conversations blocked.
- Phase 38 outputs: ledger 0 accepted / 5 needs-context / 4 post-factum-only;
  accepted outcomes 0 recomputed; demo showable_now=false; gate hardening.
- Phase 38 deep review archived at `docs/archive/PHASE38_REVIEW.md`;
  P0/P1/P2 findings: 0/0/0.
- New route: Phases 40-42 build evidence bundles, independent validators,
  strict auto-accept decisions, customer-facing policy gate, and evaluation on
  the current 9 media candidates.
- Completed: Phases 40-42 auto-validation contract, validators, decision engine,
  policy gate, evaluation, and deep review.
- Completed: MVP value run over pre-client/client-ready artifacts.
- Next task: validate buyer demand through bounded concierge source-diligence
  discovery or collect operator acceptance for at least one media row.

Read first: `docs/tasks.md` Phases 40-42, auto-validation spec/ADR, Phase 40
review, Phase 38 clientready artifacts, and the MVP value run.

## Canonical Artifacts

- Phase 37 review: `docs/archive/PHASE37_PRECLIENT_REVIEW.md`
- Phase 38 review: `docs/archive/PHASE38_REVIEW.md`
- Pre-client packet/appendix/cards/outcomes/gate:
  `docs/pilot/preclient_*`
- Phase 38 artifacts: `docs/pilot/clientready_*`
- Auto-validation contract/schema: `docs/specs/AUTO_VALIDATION_EVIDENCE.md`,
  `src/signal_sandbox/auto_validation/`
- Phase 40 review: `docs/archive/PHASE40_AUTO_VALIDATION_REVIEW.md`
- Phase 41 review: `docs/archive/PHASE41_AUTO_VALIDATION_VALIDATORS_REVIEW.md`
- Phase 42 review: `docs/archive/PHASE42_AUTO_VALIDATION_REVIEW.md`
- Auto-validation eval: `docs/pilot/clientready_AUTO_VALIDATION_EVAL.md`
- MVP value run: `docs/pilot/MVP_VALUE_RUN_2026-05-31.md`

## Key Product Facts

- V1 evaluable claims: `bablos79` 14, `nemphiscrypts` 49, `pifagortrade` 107.
- Safety gate covers 14 artifacts, 0 forbidden phrase findings, 0 showable now.
- Model packet has 9 internal candidates and 0 customer-facing rows.
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
- Validators: timing, setup consistency, provider eligibility, and post-factum
  detection are deterministic; ambiguity routes to human review.
- Decision engine: auto_accepted only when required validators and policy pass.
- Policy gate: customer-facing use requires public refs, audit refs, recompute
  provenance, caveats, safe wording, and an auto_accepted decision.
- Evaluation: 9 candidates, 0 auto_accepted, 4 auto_rejected, 5 needs_human,
  0 customer-facing rows.
- MVP value verdict: valuable as an internal diligence/evidence-quality product;
  not ready as a customer-facing paid metrics MVP.
- Recommended product route: concierge source-diligence validation before any
  public dashboard, paid metric, ranking, or customer-facing performance claim.

Cross-product cognition vault:
`/srv/codex-entropy/repos/product-3/engineering-cognition-vault/10-projects/entropy-protocol.md`; product-local docs remain authoritative.

## Active Guardrails

- Public/operator-authorized sources only.
- No private scraping, access-control bypass, advice, future-profit claims,
  unsupported ranking, marketplace framing, payment flow, or private-source
  promise.
- Unsupported providers/proxies are exclusions, not wins/losses.
- Unreviewed transcript/OCR/chart claims stay out of customer-facing metrics.
- Every buyer-facing artifact requires an explicit gate.
