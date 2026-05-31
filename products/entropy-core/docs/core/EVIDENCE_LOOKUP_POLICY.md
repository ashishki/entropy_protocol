# Core V2 Evidence Lookup Policy

Status: Active policy
Date: 2026-05-29
Scope: Local deterministic evidence lookup

This policy defines how Core V2 may add local evidence lookup and packet
inspection helpers without becoming runtime RAG, hosted search, public API, or
service infrastructure.

## Local Lookup Boundary

Evidence lookup is a deterministic local helper over checked-in evidence
indexes, review artifacts, generated evidence packets, and synthetic fixtures.
It is not:

- runtime RAG;
- embedding search;
- hosted search;
- public API;
- public SDK;
- service behavior;
- external provider integration;
- autonomous agent retrieval.

Lookup helpers may parse local Markdown or JSON artifacts that are already in
Core's evidence scope. They must not retrieve from the network, read holdout
data, load production credentials, or inspect product workspaces outside an
explicit bridge contract.

## Allowed Query Inputs

Allowed inputs:

- exact task id, such as `T125`;
- exact topic text from `docs/EVIDENCE_INDEX.md`;
- artifact path under `docs/`, `tests/`, `src/`, or generated audit output;
- review cycle id from `docs/audit/AUDIT_INDEX.md`;
- schema or artifact id when an evidence row explicitly names it.

Disallowed inputs:

- raw customer data;
- secrets, credentials, tokens, or private keys;
- free-form prompts that ask the lookup helper to infer conclusions;
- holdout paths or production data paths;
- URLs or external fetch instructions.

## Result Metadata

Lookup results must include only safe metadata:

- `query`;
- `status`;
- `topic`;
- `artifact_type`;
- `locations`;
- `scope_covered`;
- `last_verified`;
- `canonical`;
- `reason_code`;
- `approval_state`.

Results must not include raw confidential payload content, source rows,
customer data, secrets, private research payloads, or long report excerpts.

## Missing Evidence Behavior

When no matching evidence exists, lookup must return an explicit
`insufficient_evidence` status with a reason code such as
`evidence_topic_not_found`. It must not fabricate citations, infer approval,
or promote a task based on similar-looking rows.

## Redaction Expectations

Evidence lookup may return file paths and short metadata from canonical rows.
It must redact or omit:

- secrets and credentials;
- raw customer data;
- private strategy payloads;
- raw product pilot data;
- raw holdout paths;
- full report bodies or packet payload dumps.

## Blocked Surfaces

Evidence lookup never approves:

- holdout read or unlock;
- OOS/performance conclusions;
- live feeds by default;
- broker/exchange execution;
- order placement or order blocking;
- live capital;
- production credentials;
- production labels;
- capital-ready labels;
- investment advice;
- public SDK;
- hosted service or SaaS;
- public API;
- runtime RAG or embeddings;
- auth, SSO, RBAC, or tenant isolation;
- external compliance certification;
- enterprise SLA claims.

Any task that needs one of these surfaces must stop for explicit human approval
and any required ADR before implementation.
