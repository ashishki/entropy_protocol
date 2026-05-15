# ADR-001: Telegram Intake and Delivery Boundary

Status: Accepted
Date: 2026-05-07

## Context

Trader Risk Audit is a local-first concierge workflow. Phase 6 needs a
constrained pilot intake and delivery surface where traders already communicate,
but the product must remain separate from signal analytics, broker control,
investment advice, and live trading behavior.

This ADR permits Telegram only as a pilot communication surface. It does not
approve live broker/exchange integration, order blocking, signal parsing,
AI-owned violation truth, SaaS onboarding, hosted storage, or automatic report
delivery without operator approval.

## Decision

Telegram may receive user files, return status, and deliver approved reports for
pilot audits. The allowed Telegram scope is limited to:

- receiving trade export files, written risk rules, and intake metadata from a
  user;
- returning non-sensitive audit status, such as `intake_received`,
  `needs_operator_review`, `ready_to_run`, `audit_generated`, or `delivered`;
- delivering approved reports and approved delivery packets after operator
  review;
- pointing the operator to local workspace file references, never raw trade rows
  in logs or status messages.

Telegram may not connect to brokers, accept API keys, block orders, parse signal
channels, generate trading advice, scrape private groups, execute trades,
change risk policy semantics, or decide violation truth.

## Operator Approval and Deterministic Truth

Operator approval is required before report delivery. The approval must be a
deterministic artifact or explicit local metadata field, not conversational
memory.

Final violation truth remains in deterministic audit artifacts:

- normalized trades;
- approved policy;
- violation records;
- attribution summary;
- report Markdown;
- artifact manifest hashes.

Telegram text may summarize approved report content, but it must not create new
claims, modify evaluated values, infer missing rules, or provide investment
advice.

## Security and Retention Boundaries

Secrets:

- Telegram bot credentials, if later implemented, must come from environment
  variables.
- Users must not send broker API keys, exchange API keys, passwords, seed
  phrases, access tokens, or trading credentials.
- The system must reject or quarantine messages that appear to contain
  credentials before audit processing.

Logging:

- Logs may contain message counts, file counts, status values, rule ids,
  manifest ids, and hashes.
- Logs must not contain raw user files, raw trade rows, account balances, trader
  names, emails, Telegram handles, broker account ids, free-text notes, or paid
  pilot customer identifiers.

Local storage:

- Pilot files remain local by default in an operator-controlled workspace.
- Telegram file downloads, if later implemented, must write to the local audit
  workspace convention and store non-sensitive file references in metadata.
- No hosted database, shared SaaS storage, multi-tenant account model, or public
  dashboard is approved by this ADR.

Retention:

- Pilot files and generated reports follow the local retention/delete workflow.
- Deletion must be explicit and operator-controlled.
- Retention status must be traceable through local metadata or manifest
  references without exposing raw trade contents.

## Consequences

This ADR allows a later minimal Telegram bot skeleton task to be designed inside
the boundaries above. It does not permit Telegram signal analytics, broker
control, order blocking, investment advice, live trading permissions, or
customer-facing claims beyond approved deterministic report content.
