# Report Quality Scorecard

Status: active Phase 24 review aid
Date: 2026-05-15

This scorecard judges whether an audit report is clear, traceable,
reproducible, and safe enough for internal demo use. It is not a marketing
claim, customer outcome score, or PMF signal.

## Scoring Method

Score each category from 0 to 3:

| Score | Meaning |
|---:|---|
| 0 | Missing or unsafe. |
| 1 | Present but too vague for demo use. |
| 2 | Mostly clear; usable with review caveats. |
| 3 | Clear, traceable, and ready for demo use. |

Recommended demo threshold: 14+ of 18 with no fail condition.

## Categories

| Category | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Source traceability | No source refs or unverifiable provenance. | Source exists but key transformation/limits are unclear. | Source refs and row ids are present with minor caveats. | Source note, row ids, manifest, and transformation limits are clear. |
| Rule clarity | Rules are missing or ambiguous. | Rule ids appear but semantics/thresholds are hard to inspect. | Rule ids, thresholds, and main intent are understandable. | Rule ids, types, thresholds, and interpretation are clear without extra context. |
| Calculation clarity | Values cannot be checked or reconciliation is missing. | Main values appear but arithmetic or scope is unclear. | Core values are checkable with known limitations. | Violations, P&L, limitations, and reconciliation are easy to audit. |
| Limitation clarity | Material limitations are hidden or softened. | Limitations appear late or lack impact. | Limitations are present and mostly explain impact. | Material limitations are first-screen visible and tied to demo eligibility. |
| Claim safety | Advice, performance promise, or live-control implication appears. | Boundaries are present but easy to miss. | No unsafe claims; disclaimers are present. | No unsafe claims; artifact-only/customer-evidence boundaries are prominent. |
| Operator readability | Report is hard to scan or explain. | Operator needs substantial narration to make it useful. | Report can be explained with a short caveat. | Report is easy to narrate in a concise demo or review. |

## Fail Conditions

Any one of these blocks demo use regardless of total score:

- unresolved P0 or P1 finding in the current error register;
- missing source note, policy, manifest, reviewed report, run status, or
  reproducibility status for a runnable pack;
- report text gives trading advice, promises performance, implies live trade
  control, or claims customer/PMF evidence from open-source/demo packs;
- violation rows lack source-row traceability;
- P&L, drawdown, leverage, or causal-loss claims are made when the source does
  not support them;
- private/customer rows, account ids, credentials, handles, or private paths
  appear in committed artifacts;
- rejected/limitation cases are hidden from the dashboard or demo selection
  rationale.

## Reference Score - SEC Form 4 Reviewed Report

Reviewed report:
`demo/open_source_sec_form4_001/output/report_reviewed.md`

| Category | Score | Rationale |
|---|---:|---|
| Source traceability | 3 | Source note, row ids, manifest, and manual validation refs are explicit. |
| Rule clarity | 3 | Transaction-notional proxy, watchlist symbol, and unsupported leverage rule are named clearly. |
| Calculation clarity | 2 | Notional values are checkable; P&L is correctly zero but requires the source-ledger caveat. |
| Limitation clarity | 3 | First-screen operator summary says SEC rows are not a customer ledger and P&L/drawdown/leverage are unsupported. |
| Claim safety | 3 | Reviewed copy states no advice, no live control, and artifact-validation-only scope. |
| Operator readability | 3 | Operator summary, reviewed artifacts, findings, and next action are concise. |

Total: 17 / 18

Fail conditions: none.

Decision: internal reference demo eligible with the source-limitation caveat
visible. It is not customer, paid-pilot, PMF, or issuer/trading advice
evidence.

## Private Pilot Use

For private pilot reports, use this scorecard together with
`docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md`. A score above the demo
threshold does not override unresolved P0/P1 report-truth, privacy, policy
mapping, advice, live-control, or performance-claim blockers.
