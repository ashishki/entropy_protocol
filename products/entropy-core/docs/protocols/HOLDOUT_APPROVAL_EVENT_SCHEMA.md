# Holdout Approval Event Schema

Status: HOLDOUT_APPROVAL_EVENT_ABSENT
Task: T36 Holdout Approval Event Schema Contract
Last updated: 2026-05-09

This schema defines the fields required for a future explicit human holdout
approval event. It is a local contract only. It does not create, imply, infer,
or activate any approval event.

## Required Fields

| Field | Required | Meaning |
|-------|----------|---------|
| `approval_id` | yes | Stable unique identifier for the approval event. |
| `approver_identity` | yes | Human approver identity; generated or automated actors are invalid. |
| `approval_scope` | yes | Bounded scope: candidate id, evidence packet id, access purpose, and allowed operation. |
| `candidate_hash` | yes | Hash binding for the candidate under consideration. |
| `evidence_hash` | yes | Hash binding for the evidence packet supporting the request. |
| `policy_hash` | yes | Hash binding for the approval policy version. |
| `expires_at_utc` | yes | Timezone-aware UTC expiry timestamp. |
| `revocation_state` | yes | One of `not_revoked` or `revoked`. |
| `audit_metadata` | yes | Immutable request id, timestamp, actor, reason, and source document references. |

## Valid Event Requirements

A candidate event is valid only when all of the following are true:

- `approval_source` is `explicit_human_governance_event`
- `approver_identity` names a human actor
- `approval_scope.boundary` is `holdout_access`
- `approval_scope.allowed_operation` is limited to the exact future operation
  under review
- `candidate_hash`, `evidence_hash`, and `policy_hash` are non-placeholder
  hash values
- `expires_at_utc` is present and not expired at evaluation time
- `revocation_state` is `not_revoked`
- `audit_metadata` includes request id, immutable timestamp, actor, reason,
  and source references

## Invalid Fixture Classes

Schema fixtures must reject all of the following classes:

- generated approval event
- inferred approval event
- roadmap-derived approval event
- review-recommendation-derived approval event
- passing-test-derived approval event
- expired approval event
- revoked approval event
- incomplete approval event
- placeholder hash approval event
- scope-mismatch approval event

## Example Invalid Fixtures

```yaml
generated_approval_event:
  approval_source: generated_by_ai
  expected_status: REJECTED
  reason_code: GENERATED_APPROVAL_NOT_ALLOWED

inferred_approval_event:
  approval_source: readiness_packet
  expected_status: REJECTED
  reason_code: INFERRED_APPROVAL_NOT_ALLOWED

expired_approval_event:
  expires_at_utc: 2026-01-01T00:00:00Z
  expected_status: REJECTED
  reason_code: APPROVAL_EXPIRED

revoked_approval_event:
  revocation_state: revoked
  expected_status: REJECTED
  reason_code: APPROVAL_REVOKED

incomplete_approval_event:
  missing_fields:
    - approver_identity
    - approval_scope
    - candidate_hash
    - evidence_hash
    - expires_at_utc
    - audit_metadata
  expected_status: REJECTED
  reason_code: APPROVAL_EVENT_INCOMPLETE
```

## Current Approval State

- current holdout approval event: absent
- explicit human holdout approval: absent
- inferred holdout approval: rejected
- generated holdout approval: rejected
- expired holdout approval: rejected
- revoked holdout approval: rejected
- incomplete holdout approval: rejected
- holdout read: blocked
- holdout unlock: blocked

## Non-Approval Boundary

This schema cannot be used as substitute approval. Roadmap phases, readiness
artifacts, review recommendations, passing tests, protocol documents, and
generated scaffolds remain non-approval sources.
