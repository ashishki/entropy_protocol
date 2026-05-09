# Holdout Access Protocol

Status: HOLDOUT_ACCESS_DENIED_BY_DEFAULT
Task: T35 Holdout Access Protocol Deny-By-Default Contract
Last updated: 2026-05-09

This protocol is local scaffold evidence only. It does not approve, unlock, open,
or read holdout data. Holdout access remains blocked unless a future explicit
human approval event and matching local controls exist.

## Protocol State

| State | Meaning | Holdout read allowed? | Holdout unlock allowed? |
|-------|---------|-----------------------|-------------------------|
| DENIED_BY_DEFAULT | No explicit human holdout approval event is present. | No | No |
| PROTOCOL_INCOMPLETE | Required schema, audit logging, leakage guard, or review evidence is missing. | No | No |
| APPROVAL_EVENT_ABSENT | No current holdout approval event exists in active state docs. | No | No |
| FUTURE_APPROVAL_REQUIRED | A future human may consider approval only after all protocol controls exist. | No | No |

Current state: DENIED_BY_DEFAULT.

## Required Future Approvals

Before any holdout read or unlock could be considered, all of the following must
exist as explicit local evidence:

- human holdout approval event scoped to the candidate, evidence packet, and
  bounded access purpose
- approval event schema with approver identity, approval scope,
  candidate/evidence hashes, expiry, revocation state, and audit metadata
- holdout access audit logging contract
- leakage guard proof covering candidate binding, dataset partition proof,
  code/policy/parameter hashes, training-window proof, and no-prior-holdout-read
  evidence
- phase review confirming unresolved findings are absent

Missing or stale approval evidence fails closed.

## Allowed Local-Only Operations

Phase 9 may perform only protocol work that does not open or read holdout paths:

- write Markdown protocol contracts under `docs/protocols/`
- write schema fixtures that represent blocked or invalid approval states
- write tests that inspect protocol documents and state docs
- record evidence index, journal, prompt, and handoff state
- review existing archive-only readiness artifacts

## Forbidden Actions

The following actions remain forbidden in this task and phase unless a future
task explicitly supplies human approval evidence and matching local controls:

- opening a holdout file path
- reading holdout data
- unlocking holdout data
- deriving an OOS/performance claim from holdout data
- treating protocol scaffolds as executable permission
- activating live feeds, broker/exchange integrations, production labels, or
  capital-ready labels

## Non-Approval Sources

The following artifacts are not holdout approval and must be rejected as implicit
approval sources:

- roadmap phases
- planned future tasks
- readiness docs
- archive evidence packets
- reproducibility matrix rows
- no-claim sweep results
- review recommendations
- passing local tests
- generated packet scaffolds
- Phase 8 readiness review
- Phase 9 protocol documents

## Fail-Closed Rules

- If no explicit human holdout approval event exists, status is BLOCKED.
- If approval scope does not match the candidate and evidence hashes, status is
  BLOCKED.
- If approval is expired or revoked, status is BLOCKED.
- If audit logging controls are missing, status is BLOCKED.
- If leakage guard inputs are missing, stale, overlapping, or unresolved, status
  is BLOCKED.
- If any request depends on a roadmap phase, review recommendation, passing test,
  readiness artifact, or generated scaffold as approval evidence, status is
  BLOCKED.

## Current Boundary

- holdout read: blocked
- holdout unlock: blocked
- explicit human holdout approval event: absent
- OOS/performance approval: blocked
- phase-gate approval: blocked
- live feed activation: blocked
- broker/exchange activation: blocked
- production label: blocked
- capital-ready label: blocked
