# Paid Pilot Ready Gate

Status: needs_fixes
Date: 2026-05-19
Audience: operator decision

## Decision

Trader Risk Audit is not yet approved as paid-pilot ready for external delivery.
The current gate status is `needs_fixes` because no operator-approved private or
anonymized audit report has been run and manually reviewed.

Allowed next action: prepare warm conversations using the open-source demo pack
and the paid-pilot package, but do not claim private report readiness,
production readiness, customer validation, PMF, or market demand. The operator
must supply or approve one private/anonymized run outside git before this gate
can move to `ready`.

## Evidence Review

| Evidence area | Artifact | Status | Gate impact |
|---|---|---|---|
| Open-source demo quality | `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md` | pass | Shows artifact quality, positive/limitation/reject examples, and safe buyer promise. |
| Multi-case report quality | `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md` | pass_with_caveats | Three controlled internal demo-quality packs; P0:0, P1:0, P2:3 accepted caveats. |
| Private intake safety | `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md` | pass | Local-only intake, redaction, deletion trigger, and forbidden-data rules exist. |
| Private report review gate | `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md` | pass | Manual delivery checklist exists and blocks unresolved P0/P1 issues. |
| Private run notes | `docs/private_pilot_runs/pilot_waiting_for_input_001.md` | blocked | No operator-approved private input supplied; no private report run or reviewed. |
| Paid-pilot package | `docs/PAID_PILOT_PACKAGE.md` | pass | Manual one-audit package, price hypothesis, turnaround, required input, and exclusions are explicit. |
| Feedback loop | `docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md` | pass | Captures safe usefulness, trust, clarity, objection, payment, repeat, and referral evidence. |
| Real open-data rehearsal | `demo/real_open_dex_swaps_001/`, `docs/audit/PHASE27_ERROR_REGISTER.md` | pass_for_development_only | Real public Uniswap V2 pair-level swaps exercise extraction/report workflow, but they are not private, paid-pilot, customer, PMF, market-demand, or willingness-to-pay evidence. Gate remains `needs_fixes`. |
| Account-scoped real-open rehearsal | `demo/real_open_dex_contract_sequence_001/`, `docs/audit/PHASE28_ERROR_REGISTER.md` | pass_for_development_only | Real public swaps filtered to a repeated contract recipient are more scoped than pair-level flow, but still not a verified trader ledger or private evidence. Gate remains `needs_fixes`. |
| Dune public wallet rehearsal | `demo/dune_public_wallet_dex_001/`, `docs/audit/PHASE32_ERROR_REGISTER.md` | pass_for_development_only | Real public Dune `dex.trades` rows filtered to one public submitter exercise Dune extraction and report review, but they are not private, paid-pilot, customer, PMF, market-demand, or willingness-to-pay evidence. Gate remains `needs_fixes`. |
| Pre-private hypothesis validation | `docs/HYPOTHESIS_VALIDATION_WITHOUT_PRIVATE_EXPORT_PLAN.md`, `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md`, `docs/PRE_PRIVATE_OUTREACH_EVIDENCE_REVIEW.md` | complete_warn_supporting_only | Phase 29 prepared the validation loop and reviewed the absence of aggregate market/report-review evidence. It does not approve private report delivery because no T116 evidence exists. Gate remains `needs_fixes`. |
| Concierge validation execution kit | `docs/CONCIERGE_VALIDATION_EXECUTION_PLAN.md`, `docs/archive/PHASE30_REVIEW.md` | complete_warn_execution_only | Phase 30 prepares operator outreach execution, but it does not create actual outreach responses, export willingness, paid evidence, or private run evidence. Gate remains `needs_fixes`. |

## Missing Evidence

Before this gate can become `ready`, record safe evidence for:

- one operator-approved private or anonymized export outside git;
- written rules or approved structured policy for that export;
- a local audit run status outside git;
- a reviewed report status from `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md`;
- privacy scan pass and claim-safety pass;
- delivery decision of `approved_for_manual_delivery` or explicit blocker;
- deletion trigger confirmed.

If the first private run remains blocked, keep the gate at `needs_fixes` and
record the blocker in `docs/private_pilot_runs/`.

## Exact First-User Ask

Use only after the operator accepts the current `needs_fixes` limitation:

> I can run one manual post-trade audit on an approved export and your written
> risk rules. The deliverable is a reviewed report with source-row traceability,
> limitation notes, a claim-safe summary, and reproducibility evidence when the
> local run supports it. It will not connect to live trading, place or block
> orders, provide investment advice, or promise improved performance.

## Delivery Promise

Promise only:

- one reviewed manual report for one approved audit period;
- source-row traceability for deterministic findings;
- P&L attribution when supported by the source data;
- visible unsupported-data limitations;
- claim-safe delivery summary after manual review;
- 48-72 hour target turnaround after complete approved inputs.

Do not promise:

- guaranteed discovery of every risk issue;
- prevention of losses;
- improvement in trading performance;
- live risk prevention;
- automated order control;
- report delivery before manual review.

## Exclusions

This gate does not approve:

- SaaS accounts;
- checkout or payment processor integration;
- hosted uploads or hosted storage;
- live exchange control, broker control, or exchange write APIs;
- order placement, cancellation, blocking, withdrawal, transfer, or
  leverage/margin mutation;
- trading advice, strategy recommendations, signals, or guaranteed outcomes;
- public marketing claims based on open-source artifacts;
- unreviewed private delivery.

## Readiness Criteria

| Criterion | Current status |
|---|---|
| Private data intake checklist exists | pass |
| Private report review checklist exists | pass |
| Paid-pilot package exists | pass |
| Feedback log template exists | pass |
| At least one private/anonymized run exists outside git | blocked |
| At least one private/anonymized report manually reviewed | blocked |
| External delivery decision recorded safely | blocked |
| Operator go/no-go decision signed | pending |

## Operator Decision Record

| Field | Value |
|---|---|
| Gate decision | `needs_fixes` |
| Decision date | `2026-05-15` |
| Decider | `operator_required` |
| Ready for private report delivery | `no` |
| Ready for production/SaaS | `no` |
| Ready for checkout/payment processing | `no` |
| Required fix | `run_and_review_one_operator_approved_private_or_anonymized_pack_outside_git` |

## Next Action

If an operator-approved private or anonymized export is available, collect it
outside git, run the local audit workflow, complete the private report review
checklist, and update a safe run note. Re-open this gate only after that
evidence exists.

If no approved export is available yet, run Phase 29 pre-private hypothesis
validation: problem interviews, report review sessions, export willingness
asks, and safe aggregate evidence capture. This can inform ICP, offer, and
concierge validation decisions, but it cannot move this gate to `ready`.

## Development Rehearsal Note

Phase 27 added `real_open_dex_swaps_001`, a real public Ethereum Uniswap V2
WETH/USDC pair-level swap pack. It is useful development evidence because it is
real, public, non-synthetic, reproducible, and manually reviewed.

It does not change this gate because:

- it is pair-level market-flow data, not one trader account ledger;
- no operator-approved private/anonymized export was supplied;
- no private report was reviewed or approved for delivery;
- no paid user, repeat, referral, or customer validation signal exists.

The gate remains `needs_fixes`.

Phase 28 added `real_open_dex_contract_sequence_001`, which narrows real public
Uniswap V2 WETH/USDC swaps to one repeated public contract recipient. It is
useful no-breach/control rehearsal evidence, but it still does not change this
gate because the contract recipient is not a verified trader account ledger and
no operator-approved private/anonymized export was supplied.

## Pre-Private Validation Note

Phase 29 adds an evidence ladder and discovery/review kit for situations where
T116 is blocked. It is useful because it can reveal whether the report is
understandable, whether the pain is real, and whether prospects are willing to
prepare an approved anonymized export.

It does not change this gate unless it produces the missing T116 input or later
paid/manual evidence. The gate remains `needs_fixes`.

T126 reviewed the current repo-visible evidence and found no supplied aggregate
problem interviews, report review sessions, export willingness commitments, or
manual pilot asks. The Phase 29 decision is `continue_concierge_validation`.

Phase 30 added the execution kit for that concierge validation loop. It still
does not change this gate because templates, rubrics, and aggregate-log formats
are not customer evidence by themselves.

## Dune Rehearsal Note

Phase 32 added `dune_public_wallet_dex_001`, a real public Dune `dex.trades`
case pack scoped to one public Ethereum `tx_from` submitter. It produced 80
canonical rows, 76 deterministic max-position findings, a reviewed report, and
passed reproducibility/case-pack validation.

It does not change this gate because:

- Dune public submitter rows are not an operator-approved private/anonymized
  export;
- wallet ownership and private account identity are not verified;
- gas, LP fees, slippage/MEV, leverage, balances, and verified realized P&L are
  unsupported;
- no paid user, repeat, referral, customer validation, or willingness-to-pay
  signal exists.
