# Holdout Access Audit Logging Contract

Status: HOLDOUT_AUDIT_LOGGING_CONTRACT_ONLY
Task: T37 Holdout Access Audit Logging Contract
Last updated: 2026-05-09

This contract defines immutable audit logging requirements for any future
approved holdout access attempt. It does not approve holdout access, expose
holdout paths, open holdout data, or read holdout contents.

## Required Audit Fields

| Field | Required | Meaning |
|-------|----------|---------|
| `audit_event_id` | yes | Stable unique identifier for the audit event. |
| `request_id` | yes | Stable request identifier from the access attempt. |
| `approval_reference` | yes | Approval event id and policy hash reference, or `absent` for denial. |
| `candidate_hash` | yes | Candidate hash bound to the request. |
| `evidence_hash` | yes | Evidence packet hash bound to the request. |
| `access_decision` | yes | One of `BLOCKED` or `ALLOWED_BY_FUTURE_APPROVAL`. |
| `path_fingerprint` | yes | A non-reversible fingerprint of the requested holdout path. |
| `denial_reason` | yes | Machine-readable reason when the decision is blocked. |
| `timestamp_utc` | yes | An immutable timezone-aware UTC audit timestamp. |
| `actor` | yes | Human or local process actor requesting access. |
| `source_documents` | yes | Protocol/schema references used by the decision. |

## Path Privacy Boundary

Audit logs must not store raw holdout paths, path contents, file names, row
counts, schema samples, data previews, or derived holdout statistics. The only
path-related field allowed in an audit log is `path_fingerprint`, a
non-reversible fingerprint suitable for duplicate detection without
revealing the requested path.

## Denied Attempt Contract

Denied attempts are audit events, not data access events. A denied attempt must
record:

- `access_decision: BLOCKED`
- `approval_reference: absent`
- `denial_reason`, such as `MISSING_HUMAN_HOLDOUT_APPROVAL`,
  `APPROVAL_EVENT_INVALID`, `AUDIT_LOGGING_INCOMPLETE`, or
  `LEAKAGE_GUARD_INCOMPLETE`
- `path_fingerprint`, never the raw holdout path
- `holdout_path_opened: false`
- `holdout_read_executed: false`
- `holdout_unlock_requested: false`

## Future Approved Attempt Contract

A future approved attempt may be considered only after explicit human approval,
schema validation, audit logging, leakage guard checks, and phase review exist.
Even then, the audit log must record immutable timestamp metadata, candidate and
evidence hashes, approval reference, path fingerprint, access decision, actor,
and source documents before any read could be considered.

## Fail-Closed Rules

- Missing audit log requirements block access.
- Missing approval reference blocks access.
- Raw holdout path or content in an audit log blocks access.
- Missing path fingerprint blocks access.
- Missing candidate or evidence hash blocks access.
- Missing immutable timestamp metadata blocks access.
- Missing denial reason for blocked attempts invalidates the audit event.

## Current Boundary

- current holdout approval event: absent
- holdout access audit logging: contract-only
- holdout path opened: false
- holdout read executed: false
- holdout unlock requested: false
- holdout read: blocked
- holdout unlock: blocked
