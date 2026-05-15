# Product Validation Approval Intake Contract

Status: PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT_NO_APPROVAL
Task: T58 Product Validation Approval Intake Contract
Last updated: 2026-05-09

This contract defines local-only intake requirements for any future product
validation approval event. It does not create, infer, accept, or grant approval.
It does not open holdout, connect to live feeds, place orders, connect to broker
or exchange systems, load production credentials, activate capital, or confirm
the product hypothesis.

## Required Approval Fields

- `approval_event_id`
- `approval_type`
- `scope`
- `validation_path`
- `human_approver`
- `risk_owner`
- `requested_by`
- `created_at_utc`
- `expires_at_utc`
- `revocation_status`
- `approval_status`
- `evidence_packet_hash`
- `risk_signoff_hash`
- `rollback_plan_hash`
- `maximum_allowed_effect`
- `blocked_action_overrides`

## Required Evidence References

- request packet: `docs/approvals/PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md`
- broker sandbox review: `docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md`
- holdout approval decision review: `docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md`
- live-feed readiness review: `docs/audit/LIVE_FEED_READINESS_REVIEW.md`
- reproducibility matrix: `docs/research/REPRODUCIBILITY_MATRIX.md`

## Valid Approval Constraints

- approval source: explicit_human_operator_only
- generated approval: rejected
- inferred approval: rejected
- stale approval: rejected
- revoked approval: rejected
- incomplete approval: rejected
- overbroad approval: rejected
- missing expiry: rejected
- missing risk owner: rejected
- missing rollback plan hash: rejected
- missing evidence packet hash: rejected
- blocked action override present: rejected

## Current Intake Decision

- current approval event: absent
- intake decision: rejected
- rejection reason: MISSING_EXPLICIT_HUMAN_VALIDATION_APPROVAL
- product hypothesis confirmation approval: absent
- holdout approval: absent
- live-feed activation approval: absent
- broker/exchange execution approval: absent
- production credential approval: absent
- live capital approval: absent

## Blocked Restricted Actions

- holdout read: blocked
- holdout unlock: blocked
- live feed activation: blocked
- live order placement: blocked
- live broker/exchange execution: blocked
- production credential loading: blocked
- production credential deployment: blocked
- live capital action: blocked
- production label: blocked
- capital-ready label: blocked

## Intake Boundary

- no approval event created: true
- no restricted action requested: true
- no product hypothesis confirmation claimed: true
- no production/capital readiness claimed: true
