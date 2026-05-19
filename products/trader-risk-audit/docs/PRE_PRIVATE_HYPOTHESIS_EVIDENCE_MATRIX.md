# Pre-Private Hypothesis Evidence Matrix

Status: active
Date: 2026-05-19

## Current Verdict

The technical hypothesis is partially supported by deterministic tests,
open-source case packs, and two real open-data rehearsals.

The business hypothesis is not yet proven. There is no repo-visible evidence of
private export willingness, paid reports, repeat commitments, or referrals.

## Evidence Inventory

| Evidence | Classification | Current artifact | Current status | Interpretation |
|---|---|---|---|---|
| Full deterministic test baseline | technical_evidence | test suite | pass | Core workflow is regression-covered. |
| Open-source case bank | technical_evidence | `docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md` | pass_with_caveats | Multiple packs exercise report shape, reproducibility, limitation handling, and claim safety. |
| Multi-case quality dashboard | technical_evidence | `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md` | pass_with_caveats | At least three packs are controlled internal demo-quality; P2 caveats remain visible. |
| Real pair-level DEX rehearsal | technical_evidence | `demo/real_open_dex_swaps_001/` | pass_for_development_only | Real public logs exercise extraction/report workflow but are not a trader ledger. |
| Contract-recipient scoped DEX rehearsal | technical_evidence | `demo/real_open_dex_contract_sequence_001/` | pass_for_development_only | More account-scoped than pair-level flow, still not verified trader private evidence. |
| Private intake checklist | product_evidence | `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md` | pass | The product has a safe intake boundary for future private data. |
| Private report review checklist | product_evidence | `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md` | pass | Delivery can be blocked or approved by a manual truth/privacy gate. |
| Paid-pilot package | product_evidence | `docs/PAID_PILOT_PACKAGE.md` | pass | The concierge offer is written, but not validated by payment or delivery. |
| Operator-approved private export | blocked_private_evidence | `docs/private_pilot_runs/pilot_waiting_for_input_001.md` | blocked | T116 cannot proceed until a real approved export exists outside git. |
| Report review by external domain people | market_evidence | not yet collected | missing | Need 3-5 review sessions. |
| Past-behavior problem interviews | market_evidence | not yet collected | missing | Need 10-15 conversations with safe aggregate notes. |
| Export willingness | market_evidence | not yet collected | missing | Need at least one approved anonymized export commitment. |
| Paid report | paid_evidence | not yet collected | missing | No willingness-to-pay evidence yet. |
| Repeat commitment or referral | paid_evidence | not yet collected | missing | No retention or referral evidence yet. |
| T126 outreach evidence review | market_evidence | `docs/PRE_PRIVATE_OUTREACH_EVIDENCE_REVIEW.md` | reviewed_no_aggregate_evidence | No privacy-safe aggregate interview/report-review rows were supplied; decision is `continue_concierge_validation`. |

## Evidence Gaps

| Gap | Severity | Why it matters | Fastest way to close |
|---|---|---|---|
| No private/anonymized export | High | Paid delivery readiness depends on a real operator-approved run. | Ask warm prospects/operators for one approved anonymized CSV outside git. |
| No buyer past-behavior evidence | High | Without past pain, report quality may be a solution looking for a problem. | Conduct 10-15 discovery calls focused on recent incidents and current workflow. |
| No report usefulness review | Medium | Technical correctness does not prove the report is useful or trusted. | Run 3-5 guided reviews using existing case-pack reports. |
| No paid/repeat/referral signal | High | The business model is still unproven. | Make a clear manual audit ask after pain/export fit is confirmed. |

## Phase 29 Review Outcome

Phase 29 is archived with WARN health because the planning, scripts, report
conversation pack, and evidence capture runbook are complete, but no aggregate
market/report-review evidence has been supplied yet.

Decision: `continue_concierge_validation`.

Next action: run the conversation loop outside git and resume T116 immediately
if one approved anonymized/private export becomes available.

## Current Safe Claim

Allowed:

> We have a deterministic local post-trade audit workflow with reproducible
> reports on open-source and real public rehearsal data. It is ready for
> founder-led discovery and controlled private-export collection.

Forbidden:

> The product has proven PMF, market demand, paid-pilot readiness, private
> report readiness, or production/SaaS readiness.
