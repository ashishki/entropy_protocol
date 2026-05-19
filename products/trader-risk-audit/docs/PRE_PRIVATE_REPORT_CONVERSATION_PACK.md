# Pre-Private Report Conversation Pack

Status: draft
Date: 2026-05-19

## Purpose

This pack tells the operator which existing reports to use in discovery and
review conversations while no private/anonymized export is available.

Every report in this pack is technical/product evidence only. It must not be
described as PMF, customer validation, private report readiness, paid-pilot
readiness, or market demand.

## Recommended Sequence

| Step | Artifact | Why use it | Boundary to say aloud |
|---|---|---|---|
| 1 | `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md` | High-level demo narrative with positive, limitation, and reject examples. | Internal demo pack, not customer evidence. |
| 2 | `demo/risk_audit_case_001/output/report_reviewed.md` | Strong positive report shape with source-row traceability. | Controlled demo-quality pack, not private data. |
| 3 | `demo/real_open_dex_contract_sequence_001/output/report_reviewed.md` | Real public account-scoped rehearsal with no-breach/control flavor. | Public contract-recipient sequence, not verified trader ledger. |
| 4 | `demo/real_open_dex_swaps_001/output/report_reviewed.md` | Real public pair-level DEX flow with visible limitations. | Pair-level market flow, not account ledger. |
| 5 | `demo/synthetic_schema_reject_missing_price_001/output/run_status.json` | Shows reject behavior when required data is missing. | Rejection/control artifact only. |

## Conversation Goals

Use these reports to learn:

- whether the prospect understands the report without a long explanation;
- which findings map to their current review workflow;
- which fields they require before trusting a report;
- whether visible limitations increase or reduce trust;
- whether the next step should be an approved anonymized export.

## Safe Talk Track

Allowed:

> These examples show the report shape, source traceability, limitations, and
> deterministic workflow. They are not private customer reports. We use them to
> test whether the output would be useful before asking for an approved export.

Forbidden:

> These reports prove demand, PMF, paid-pilot readiness, or that we can audit any
> trader account without additional data review.

## Review Score

After each report review, record only:

| Field | Allowed values |
|---|---|
| `icp_label` | `solo_crypto`, `prop_funded`, `coach`, `dao_treasury`, `fund_operator`, `other_safe_label` |
| `report_understood` | `yes`, `partial`, `no` |
| `usefulness_score` | `1`, `2`, `3`, `4`, `5` |
| `trust_blocker` | `missing_fees`, `missing_pnl`, `missing_leverage`, `source_shape`, `policy_mapping`, `privacy`, `other_safe_tag`, `none` |
| `workflow_fit` | `weekly_review`, `post_session_review`, `coach_review`, `governance_review`, `incident_review`, `none` |
| `next_action` | `send_redaction_checklist`, `schedule_private_export`, `revise_report`, `narrow_icp`, `no_fit` |

