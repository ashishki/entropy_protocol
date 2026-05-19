# Concierge Validation Execution Plan

Status: complete_for_operator_use
Date: 2026-05-19
Phase: 30

## Purpose

This plan converts Phase 29 from "prepared validation system" into an operator
execution loop. It defines who to contact, what to ask for, how to score the
conversation, and when to return to T116.

It does not approve SaaS, checkout, hosted uploads, live exchange control,
order blocking, trading advice, production readiness, PMF, or paid-pilot
readiness.

## Core Test

Can the operator find at least one real trading operator who has a recent
post-trade review pain and is willing to prepare an approved anonymized export
for one manual audit?

## Two-Week Execution Loop

| Day | Action | Target output |
|---|---|---|
| 1 | Select 20 potential contacts across 3 ICPs. | 20 scored prospects, no identifiers in git. |
| 2-4 | Send manual outreach in small batches. | 10-15 replies or follow-up attempts. |
| 3-8 | Run problem interviews. | 10-15 aggregate interview rows outside git. |
| 5-10 | Run report review sessions with existing demo/open-data reports. | 3-5 aggregate report-review rows outside git. |
| 8-12 | Ask export willingness after pain is established. | 3-5 export willingness tags. |
| 10-14 | Ask manual pilot next step after export willingness. | 3-5 pilot ask tags. |
| 14 | Summarize aggregate outcomes. | Decision: return to T116, continue validation, narrow ICP, revise offer, or pause/pivot. |

## ICP Priority

Start with people who already have a reason to care about post-trade rule
review.

| Rank | ICP | Why first | What to avoid |
|---:|---|---|---|
| 1 | Prop/funded trader or coach | Often has explicit rules, breach review, and repeat evaluation cadence. | People looking only for signals or strategy advice. |
| 2 | Solo discretionary crypto trader with written rules | May feel manual review pain and can move quickly. | People with no written rules or no export habit. |
| 3 | DAO/fund/treasury operator | Needs traceability and policy review, but scope may drift toward accounting/compliance. | Full accounting, tax, or governance platform requests. |

## Minimum Evidence Targets

| Evidence | Minimum target | Strong signal |
|---|---:|---|
| Problem interviews | 10 | At least 5 have a recent painful review incident or recurring manual review. |
| Report review sessions | 3 | At least 2 score usefulness 4/5 or higher. |
| Export willingness asks | 3 | At least 1 agrees to prepare approved anonymized export outside git. |
| Manual pilot asks | 3 | At least 1 accepts a concrete paid or free concierge audit next step. |

## Decision Rules

| Decision | Trigger |
|---|---|
| `return_to_t116` | One approved anonymized/private export exists outside git. |
| `continue_concierge_validation` | Pain exists, but export is not ready and no ICP dominates yet. |
| `narrow_icp` | One ICP clearly shows stronger pain, urgency, and export willingness. |
| `revise_offer` | Pain exists, but report framing, price, or delivery promise blocks next step. |
| `pause_or_pivot` | No urgent pain, no current workaround, and no concrete next step after 10-15 interviews. |

## Stop Conditions

Stop outreach or do not record the interaction if:

- the person asks for trading advice, signals, strategy generation, live alerts,
  or order blocking;
- the person wants to send credentials, account ids, screenshots, or raw rows
  into git-visible channels;
- the use case requires hosted upload, SaaS account, broker control, exchange
  write API, withdrawal, transfer, leverage/margin mutation, or live trading
  control;
- the only evidence is compliments with no past incident, no current workflow,
  and no next step.

