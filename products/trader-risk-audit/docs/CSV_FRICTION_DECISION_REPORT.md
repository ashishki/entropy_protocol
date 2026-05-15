# CSV Friction Decision Report

_Date: 2026-05-15_

## Verdict

Decision: defer real local read-only exchange network fetching.

T94-T97 remain blocked. Do not update ADR-002 for real fetching and do not
implement real exchange network calls until future market evidence explicitly
changes this decision.

## Evidence Source

Phase 21 built the local measurement infrastructure:

- safe funnel events;
- local hypothesis dashboard;
- explicit gate rules;
- privacy-safe evidence export.

No committed market customer evidence log is present in this repository. That
is intentional: private customer logs should remain local/operator-controlled.
Given the available repo evidence, all market evidence counts below are zero.

## Quantified Gate Inputs

| Input | Count | Interpretation |
|---|---:|---|
| Qualified market prospects | 0 | No local market log was supplied for this decision. |
| Valid exports/rules | 0 | No measured CSV/export completion evidence. |
| CSV/export blockers | 0 | No recorded blocker tags from market prospects. |
| Valid-export drop-off | 0/0 | Not measurable without qualified prospects and intake attempts. |
| API-request objections | 0 | No market API setup objection evidence. |
| CTA accepted / paid intent | 0 | No market paid-intent evidence supplied. |
| Paid reports delivered | 0 | No paid report evidence supplied. |
| Repeat/referral signals | 0 | No repeat or referral evidence supplied. |

## Safety Rationale

Real exchange network fetching would introduce credential handling, endpoint
allowlists, permission verification, rate-limit behavior, redaction risk, and
operator support burden. The current evidence does not show that CSV/export
friction is the binding blocker, so adding real fetching now would expand
runtime and security surface without validation.

## Commercial Rationale

The project still needs market evidence that prospects:

- qualify for the ICP;
- attempt intake;
- fail or struggle specifically because of CSV/export friction;
- accept/pay for the manual audit;
- ask for repeat audits or provide referrals.

Uploads, valid exports, API connection interest, demo usage, and open-source
artifact quality are supporting evidence only. They do not prove willingness to
pay or justify real network fetching by themselves.

## Required Evidence To Reopen

Reopen T94 only if a future privacy-safe evidence export shows:

- at least 10 qualified market prospects;
- measurable valid-export drop-off or repeated CSV/export blocker tags;
- API import requested as a solution by prospects, not inferred by the team;
- paid report or paid-intent evidence from the same ICP;
- no unresolved privacy/credential objections that would dominate the offer.

Until then, keep CSV fallback, fixture-backed exchange import, and local audit
automation as the supported paths.
