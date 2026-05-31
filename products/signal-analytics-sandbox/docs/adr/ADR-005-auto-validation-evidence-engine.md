# ADR-005 — Auto-Validation Evidence Engine

Date: 2026-05-29
Status: Proposed

## Context

Phase 38 proved that the current client-readiness bottleneck is not model
candidate discovery. The model found 9 plausible media candidates, but none can
be promoted to dashboard-safe or paid-report-safe use until the system proves:

- the source post preceded the relevant market move;
- OCR/chart levels are read correctly;
- entry, stop, target, direction, and RR describe one coherent setup;
- asset/proxy/provider mapping is approved and reproducible;
- the row is not post-factum or already-closed-position evidence;
- customer-facing use is legally and reputationally safe.

Model review alone remains triage. The desired automation is therefore not
"LLM says valid"; it is "independent validators produce enough auditable proof
to auto-accept, otherwise route to human review."

## Decision

Add an Auto-Validation Evidence Engine in Phases 40-42.

The engine may emit these final states:

- `auto_accepted`
- `auto_rejected`
- `excluded_provider_gap`
- `needs_human`
- `blocked_customer_facing`

`auto_accepted` is allowed only when all required proof checks pass:

1. pre-outcome timing;
2. OCR/level confidence;
3. setup math consistency;
4. asset/proxy/provider eligibility;
5. post-factum / closed-position cue detection;
6. customer-facing policy gate.

Any uncertainty, missing evidence, low confidence, conflicting validators, or
provider ambiguity routes to `needs_human` or an explicit exclusion. The system
must be conservative: false accepts are worse than false rejects.

## Boundaries

- No private scraping or access-control bypass.
- No model-only acceptance for customer-facing metrics.
- No bulk market-history storage; validator market windows use compact
  provenance refs and approved provider/proxy paths.
- No investment advice, future-profit claims, public ranking, marketplace
  framing, or payment promise.
- Auto-validation can reduce human review load, but cannot bypass the final
  customer-facing policy gate.

## Consequences

- New schemas are required for candidate evidence bundles, validation results,
  audit logs, and decision outputs.
- The current 9 Phase 38 candidates become the first evaluation set.
- Buyer discovery remains blocked until a later gate has accepted evidence,
  recomputed outcomes, and showable demo rows.
