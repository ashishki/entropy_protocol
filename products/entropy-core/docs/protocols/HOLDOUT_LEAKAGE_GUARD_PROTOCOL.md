# Holdout Leakage Guard Protocol

Status: HOLDOUT_LEAKAGE_GUARD_INCOMPLETE
Task: T38 Holdout Leakage Guard Protocol Fixture
Last updated: 2026-05-09

This protocol defines local guard inputs that any future approved holdout access
would need before a holdout read could be considered. It is fixture/protocol
work only. It does not approve, unlock, open, or read holdout data.

## Required Guard Inputs

| Input | Required proof |
|-------|----------------|
| candidate binding | Candidate id, candidate hash, and matching approval scope. |
| dataset partition proof | Deterministic proof that train, validation, archive, and holdout partitions do not overlap. |
| code hash | Code hash bound to the evidence packet and approval scope. |
| policy hash | Policy hash bound to the approval event and protocol version. |
| parameter hash | Parameter/config hash bound to the candidate and evidence packet. |
| training-window proof | Training and archive windows end before any holdout window begins. |
| no-prior-holdout-read evidence | Audit log proof that no prior holdout path was opened, read, or unlocked for the candidate. |
| approval event validity | Explicit human holdout approval event is present, unexpired, unrevoked, and scope-matched. |
| audit logging readiness | Audit logging contract fields are present before any read could be considered. |

## Leakage Checks

The guard must fail closed unless all checks have passing evidence:

- candidate binding check
- dataset partition overlap check
- code/policy/parameter hash freshness check
- training-window boundary check
- no-prior-holdout-read check
- approval event validity check
- audit logging readiness check
- unresolved evidence check

## Fail-Closed Behavior

The guard records `BLOCKED` for any of the following:

- missing approval
- stale hashes
- partition overlap
- prior holdout read
- unresolved evidence
- missing candidate binding
- missing training-window proof
- missing audit logging readiness
- expired approval
- revoked approval
- scope mismatch

## Fixture Matrix

| Fixture | Expected status | Reason code |
|---------|-----------------|-------------|
| missing approval | BLOCKED | MISSING_HUMAN_HOLDOUT_APPROVAL |
| stale hashes | BLOCKED | STALE_HASH_BINDING |
| partition overlap | BLOCKED | HOLDOUT_PARTITION_OVERLAP |
| prior holdout read | BLOCKED | PRIOR_HOLDOUT_READ_DETECTED |
| unresolved evidence | BLOCKED | UNRESOLVED_GUARD_EVIDENCE |
| missing training-window proof | BLOCKED | MISSING_TRAINING_WINDOW_PROOF |
| missing audit logging readiness | BLOCKED | AUDIT_LOGGING_INCOMPLETE |

## Current Boundary

- guard status: incomplete
- current holdout approval event: absent
- holdout path opened: false
- holdout read executed: false
- holdout unlock requested: false
- holdout read: blocked
- holdout unlock: blocked
- OOS/performance approval: blocked

## Source References

- `src/entropy/walkforward/leakage.py`
- `src/entropy/data/holdout.py`
- `docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md`
- `docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md`
- `docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md`
