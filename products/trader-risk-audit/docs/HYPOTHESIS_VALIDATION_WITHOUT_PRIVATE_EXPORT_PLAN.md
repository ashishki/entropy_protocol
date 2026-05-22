# Hypothesis Validation Without Private Export Plan

Status: complete_for_docs_active_for_operator_loop
Date: 2026-05-19
Audience: operator and product loop

## Purpose

This plan defines what can strengthen the Trader Risk Audit hypothesis before
one operator-approved private/anonymized export is available.

It does not replace T116. A private/anonymized local run and manually reviewed
private report are still required before the paid-pilot ready gate can move
from `needs_fixes` to `ready`.

## Core Hypothesis

Target users with real trading operations will value a deterministic post-trade
risk audit report enough to share an approved export, use the findings in their
review workflow, and eventually pay for a reviewed manual audit.

## Evidence Ladder

| Evidence layer | Strength | What it can prove | What it cannot prove |
|---|---:|---|---|
| Reproducible real open-data case packs | Medium | The audit workflow handles real public data, preserves provenance, and produces claim-safe reports. | Private report readiness, customer demand, or willingness to pay. |
| Account-like public sequences | Medium | The workflow can analyze scoped sequences that are closer to account behavior than market-wide flow. | That the sequence is a verified trader ledger, or that fees/P&L/leverage are complete. |
| Manual domain review of sample reports | Medium-High | Traders/operators understand the report, trust or reject the findings, and identify missing fields. | That a buyer will pay or share private data. |
| Problem interviews with past-behavior evidence | High | The target user has a real review pain, current workaround, cost of failure, and buyer language. | That the current product output is sufficient. |
| Concierge audit request with approved anonymized export | Very High | A real operator is willing to overcome export/redaction friction for the report. | Repeatability or willingness to pay unless pricing is tested. |
| Paid manual pilot | Highest | The product solves a problem valuable enough for payment under current constraints. | Scalable SaaS readiness or broader PMF. |

## Phase 29 Scope

Phase 29 is a pre-private validation phase that runs while T116 is blocked. It
has three goals:

1. Turn existing real open-data and open-source reports into a disciplined
   conversation pack.
2. Collect evidence from real people about past review behavior, current
   workflow, trust objections, and export willingness.
3. Decide whether the next operator action should be private-export collection,
   ICP narrowing, offer changes, or no further product build.

## Required Outputs

| Output | Owner | Location | Completion criteria |
|---|---|---|---|
| Evidence matrix | codex | `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md` | Every evidence type is classified as technical, product, market, paid, or blocked. |
| Discovery script | codex | `docs/PRE_PRIVATE_DISCOVERY_SCRIPT_RU.md` | Questions focus on past behavior, current workaround, and export willingness. |
| Report conversation pack | codex | `docs/PRE_PRIVATE_REPORT_CONVERSATION_PACK.md` | Existing validated reports are packaged for calls without claiming PMF or private readiness. |
| Evidence capture runbook | codex | `docs/PRE_PRIVATE_EVIDENCE_CAPTURE_RUNBOOK.md` | Safe fields and forbidden fields are explicit; no private identifiers or raw rows. |
| Gate review | codex + operator | `docs/archive/PHASE29_REVIEW.md` | Summarizes collected evidence and next decision. |

## ICP Tests

Phase 29 should test at least three ICP hypotheses:

| ICP | Why it might care | Fast signal to look for | Disconfirming signal |
|---|---|---|---|
| Solo discretionary crypto trader | May lack disciplined post-trade rule review. | Has recent rule breaches, tracks risk manually, agrees to anonymized CSV review. | Uses no written rules and sees post-trade audit as low value. |
| Prop/funded trader or coach | May need repeatable evidence for trader discipline. | Reviews rule breaches weekly, already asks for screenshots/exports. | Existing platform dashboard is enough and export friction blocks sharing. |
| DAO/fund/treasury operator | Needs governance-visible transaction review and policy compliance. | Already performs manual wallet/transaction reviews and wants traceable findings. | Needs accounting/compliance scope beyond current trade audit model. |

## Fast Tests

Run these tests before building more product surface:

| Test | Target count | Pass signal | Fail signal |
|---|---:|---|---|
| Problem interviews | 10-15 | At least 5 have a recent painful review incident or recurring manual review. | Most users cannot name a past incident or current workaround. |
| Report review sessions | 3-5 | At least 3 can explain a finding and name one workflow use. | Reports are confusing, untrusted, or irrelevant. |
| Export willingness ask | 3-5 | At least 1 agrees to prepare an approved anonymized export. | Everyone refuses export sharing even after redaction boundary is explained. |
| Manual pilot ask | 3-5 | At least 1 accepts a clear paid or free concierge audit next step. | Users compliment the idea but avoid any concrete next step. |

## Evidence Classification

Use these labels consistently:

- `technical_evidence`: reproducibility, deterministic outputs, validation
  coverage, report truth, source traceability.
- `product_evidence`: report usefulness, clarity, trust, missing fields,
  workflow fit.
- `market_evidence`: qualified prospect, past incident, current workaround,
  export willingness, paid/manual audit interest.
- `paid_evidence`: accepted paid report, paid delivery, repeat commitment,
  referral.
- `blocked_private_evidence`: T116 private export not yet supplied.

## Rules

- Do not count open-source or demo artifacts as PMF, customer validation,
  market demand, paid-pilot evidence, or private report readiness.
- Do not record names, emails, handles, account ids, wallet ownership claims,
  payment identifiers, private paths, raw rows, screenshots, or notes that
  identify a person or account.
- Do not promise SaaS, checkout, hosted upload, live monitoring, order
  blocking, exchange control, broker control, trading advice, or performance
  improvement.
- Do not build new product automation until Phase 29 evidence shows the
  blocker is product surface rather than trust, ICP, or export willingness.

## Decision Gate

At the end of Phase 29, choose one decision:

| Decision | Criteria | Next action |
|---|---|---|
| `return_to_t116` | At least one operator/prospect is willing to provide an approved anonymized export. | Run T116 outside git. |
| `continue_concierge_validation` | Interviews show pain, but no export is ready yet. | Keep conversations manual; no new automation. |
| `narrow_icp` | One ICP shows much stronger pain/export willingness than others. | Rewrite offer/demo around that ICP before more outreach. |
| `revise_offer` | Pain exists, but the report/price/delivery promise is not compelling. | Adjust package and report framing before another batch. |
| `pause_or_pivot` | Users have no urgent past pain, no workaround, and no concrete next step. | Stop building and revisit problem selection. |
