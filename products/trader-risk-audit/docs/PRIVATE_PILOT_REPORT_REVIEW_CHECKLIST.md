# Private Pilot Report Review Checklist

Status: active Phase 25 checklist
Date: 2026-05-15
Audience: operator/reviewer

Use this checklist before any private pilot audit report or delivery packet is
sent externally. It is a manual delivery gate, not a public SaaS workflow, not
trading advice, not live exchange control, and not a performance promise.

## Delivery Status

| Status | Meaning | External delivery |
|---|---|---|
| `blocked_do_not_deliver` | Any P0/P1 truth, privacy, policy, or claim-safety issue is unresolved. | Forbidden |
| `needs_fix` | No P0/P1, but reviewer found a fixable P2 clarity or formatting issue. | Hold |
| `approved_for_manual_delivery` | All required checks pass and reviewer signed off. | Allowed manually |
| `delivered_manual` | Report was delivered manually after approval. | Completed |

Default status is `blocked_do_not_deliver` until every required check passes.

## Required Checks

| Area | Pass condition | Blocks delivery if |
|---|---|---|
| Source-row traceability | Every violation row includes rule id, timestamp, evaluated value, threshold, severity, and source row id or ids. | Any finding cannot be traced to normalized input artifacts. |
| Policy mapping | Policy file matches operator-approved written rules; unresolved review packet items are closed or excluded. | Ambiguous rule mapping, unsupported executable rule, or unapproved threshold remains. |
| Calculation review | P&L totals, violating/compliant/unclassified P&L, reconciliation delta, drawdown/daily-loss values, and limitation counts are checkable. | Reconciliation is missing/non-zero without explanation, arithmetic cannot be reviewed, or source does not support the claim. |
| Limitation wording | Unsupported fields, missing data, source-shape limits, and P2 caveats are visible before delivery. | Limitation is hidden, softened, or contradicted by the report summary. |
| Privacy review | Report, packet, manifest, bundle index, and any safe run note contain no raw rows, account ids, credentials, Telegram handles, payment ids, private paths, or unapproved screenshots. | Any private identifier or forbidden data appears in deliverable or committed summary. |
| Claim safety | `ensure_report_claims_valid` passes or reviewer records equivalent claim-guard pass; no advice, performance promise, live-control, counterfactual return, causal-loss, PMF, or customer-demand overclaim appears. | Claim guard fails or reviewer sees advice/performance/live-control/evidence-overclaim wording. |
| Reproducibility | Manifest and bundle refs exist; reproducibility status exists when required by the run plan. | Artifact refs are missing, hashes are unexplained, or drift blocks trust. |
| Operator readability | The reviewed copy can be explained in one short call without hiding limitations. | Reviewer needs unsupported narration to make the report seem valid. |

## Severity Gate

| Severity | Examples | Delivery decision |
|---|---|---|
| P0 | Wrong trader/account, private data leak, fabricated violation, unsafe live-control/advice claim. | Block; do not deliver. |
| P1 | Incorrect P&L/reconciliation, missing source traceability, unapproved policy mapping, missing required disclaimer. | Block; do not deliver. |
| P2 | Caveat placement, wording clarity, formatting issue, accepted source limitation. | Hold unless visible and signed off. |

Any unresolved P0/P1 issue sets status to `blocked_do_not_deliver`.

## Report Review Steps

1. Open the reviewed report copy, not the raw generated report.
2. Check the run status, manifest, bundle index, and reproducibility status.
3. Compare policy rules to the approved written rules and review packet.
4. Spot-check at least three violation rows against normalized artifacts by
   source row id.
5. Check P&L attribution totals and reconciliation.
6. Confirm limitations are first-screen visible when material.
7. Run or verify claim guard for report and delivery packet text.
8. Scan deliverables for forbidden private data.
9. Assign delivery status and complete signoff.

## Required Signoff Fields

| Field | Value |
|---|---|
| Pilot label | `<safe_pilot_label>` |
| Reviewer | `<operator_initials>` |
| Review date | `YYYY-MM-DD` |
| Report artifact label | `<safe_report_label>` |
| Delivery packet label | `<safe_packet_label>` |
| Scorecard total | `__/18` |
| Fail condition present | `yes/no` |
| P0 count | `0` required |
| P1 count | `0` required |
| P2 count and disposition | `<count + accepted/fix>` |
| Claim guard status | `passed/blocked` |
| Privacy scan status | `passed/blocked` |
| Reproducibility status | `passed/not_applicable/blocked` |
| External delivery status | `blocked_do_not_deliver/needs_fix/approved_for_manual_delivery/delivered_manual` |
| Deletion trigger confirmed | `yes/no` |
| Reviewer notes | `<safe summary only>` |

## Safe Reviewer Notes

Reviewer notes may include:

- safe pilot label;
- aggregate counts;
- rule ids;
- limitation ids;
- non-sensitive blocker tags;
- delivery status.

Reviewer notes must not include:

- raw private rows;
- source file private paths;
- account ids or balances;
- credentials or signatures;
- Telegram handles, emails, phone numbers, names, or payment details;
- screenshots unless explicitly approved and redacted.

## Delivery Rule

Deliver only when:

- status is `approved_for_manual_delivery`;
- P0 count is `0`;
- P1 count is `0`;
- claim guard status is `passed`;
- privacy scan status is `passed`;
- all P2 items are either fixed or accepted with visible caveats;
- deletion trigger is confirmed.

Manual delivery remains operator-owned. This checklist does not approve
checkout, public upload, automated sending, live exchange control, order
blocking, advice, or guaranteed trading improvement.
