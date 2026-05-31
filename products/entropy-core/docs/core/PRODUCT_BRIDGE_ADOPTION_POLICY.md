# Core V2 Product Bridge Adoption Policy

Status: Active policy
Date: 2026-05-29
Scope: Core-owned product bridge profile readiness

This policy defines how Core V2 may assess whether product-shaped artifacts are
ready to use Core validation primitives. It does not move product runtime logic,
report authorship, external delivery decisions, or product workspace ownership
into Core.

## Core Validation Boundary

Core may own:

- product bridge profile identifiers;
- artifact schema overlays;
- synthetic fixture validation;
- no-claim and blocked-surface checks;
- evidence references for Core validation outputs;
- local readiness results for Core adoption.

Core must not own:

- product runtime behavior;
- Trader Risk Audit or Signal Analytics Sandbox runtime behavior;
- product report authorship;
- product policy interpretation;
- product workspace edits;
- customer delivery decisions;
- external pilot approval;
- hosted service behavior.

## Adoption Readiness Inputs

Every product bridge adoption readiness check must name:

- `profile_id`;
- `artifact_contract_version`;
- `synthetic_fixture_refs`;
- `evidence_refs`;
- `allowed_core_primitives`;
- `forbidden_product_calls`;
- `no_claim_boundaries`;
- `blocked_surfaces`;
- `owner`;
- `reviewer`;

The readiness check may only evaluate Core-owned validation metadata. Product
teams remain responsible for product-specific findings, report wording, user
workflow, and customer delivery choices.

## Synthetic Fixture Requirements

Synthetic fixtures must:

- use redacted or generated data only;
- cover valid adoption metadata;
- cover missing evidence references;
- cover unsafe claim labels;
- cover attempted product runtime ownership;
- cover attempted product report authorship;
- cover hosted service or external delivery approval violations.

Fixtures must not include real customer data, private product artifacts,
holdout data, production credentials, or live execution payloads.

## Failure Handling

Failed adoption readiness must return a local `blocked` or
`needs_manual_review` result with safe reason codes. Corrections are represented
by new artifacts, fixtures, or review notes. Core must not mutate prior
registry, governance, or evidence records to hide a failed adoption check.

## Evidence Expectations

Adoption readiness evidence must include:

- fixture paths;
- validation result status;
- rejected claim or surface reason codes;
- referenced Core tests;
- review artifact path when readiness is reviewed;
- explicit statement that Core did not edit product workspaces or own product
  reports.

## Blocked Surfaces

Product bridge adoption never approves:

- product workspace edits from Core;
- product runtime ownership;
- product report authorship;
- external delivery approval;
- public SDK;
- hosted service or SaaS;
- public API;
- live feeds by default;
- broker/exchange execution;
- order placement or order blocking;
- holdout read or unlock;
- OOS/performance conclusions;
- production credentials;
- production labels;
- capital-ready labels;
- live capital;
- investment advice;
- external compliance certification;
- enterprise SLA claims.

Any task that needs one of these surfaces must stop for explicit human approval
and any required ADR before implementation.
