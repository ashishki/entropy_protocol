# Holdout Approval Evidence Intake Contract

Status: HOLDOUT_APPROVAL_INTAKE_CONTRACT_NO_EVENT
Task: T41 Holdout Approval Evidence Intake Contract
Last updated: 2026-05-09

This contract defines local intake checks for a future explicit holdout approval
event. It does not create, infer, accept, or activate any approval event.

## Required Approval Fields

- `approval_id`
- `approver_identity`
- `approval_source`
- `approval_scope`
- `candidate_hash`
- `evidence_hash`
- `policy_hash`
- `parameter_hash`
- `expires_at_utc`
- `revocation_state`
- `audit_metadata`

## Required Hash Bindings

- candidate hash matches the requested candidate id
- evidence hash matches the request packet evidence bundle
- policy hash matches the approval policy version
- parameter hash matches the frozen candidate/config parameters
- approval scope references the same candidate and evidence hashes

## Rejected Intake Fixtures

| Fixture | Expected status | Reason code |
|---------|-----------------|-------------|
| absent approval evidence | REJECTED | APPROVAL_EVENT_ABSENT |
| generated approval evidence | REJECTED | GENERATED_APPROVAL_NOT_ALLOWED |
| inferred approval evidence | REJECTED | INFERRED_APPROVAL_NOT_ALLOWED |
| expired approval evidence | REJECTED | APPROVAL_EXPIRED |
| revoked approval evidence | REJECTED | APPROVAL_REVOKED |
| stale hash evidence | REJECTED | STALE_HASH_BINDING |
| scope-mismatched evidence | REJECTED | APPROVAL_SCOPE_MISMATCH |
| incomplete approval evidence | REJECTED | APPROVAL_EVENT_INCOMPLETE |

## Current Intake State

- current holdout approval event: absent
- intake decision: rejected
- explicit human holdout approval: absent
- holdout read: blocked
- holdout unlock: blocked
- OOS/performance approval: blocked

## Non-Approval Boundary

Approval evidence intake cannot treat roadmap phases, protocol documents,
request packets, review recommendations, passing tests, readiness artifacts, or
generated scaffolds as approval evidence.
