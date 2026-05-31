# Entropy Core Proof Layer Strategy

Status: active portfolio strategy
Last updated: 2026-05-31

## Position

Entropy Core is the portfolio proof layer. Products are the application points
for the protocol.

Core should validate artifact contracts, evidence references, schema evolution,
blocked surfaces, and product bridge adoption metadata. Products should own
their runtime behavior, user workflows, report language, customer delivery
decisions, and product-specific validators.

## Why This Matters

The current portfolio already has products that generate evidence-rich claims:

- Signal Analytics Sandbox now has an auto-validation evidence engine with
  bundles, validators, audit logs, decisions, and MVP value assessment.
- Telegram Research Agent has research brief receipts, delivery refs,
  verification checks, operator review, and channel intelligence backlog.
- Demand-to-MVP Radar produces opportunity/source-trust evidence and weekly
  report decisions.
- Workflow-to-Agent Studio will generate workflow/agent blueprints that need
  permission-boundary proof.
- AI Rollout Training OS will generate permission judgment outcomes that need
  explainable scoring.

Without a shared proof layer, each product will reinvent schema versioning,
evidence refs, verifier status, and blocked-surface language. With too much
centralization, Core becomes a platform and starts owning product logic. The
right boundary is shared proof contracts, not shared product behavior.

## Core-Owned Layer

Core owns:

- artifact schema compatibility;
- local evidence lookup semantics;
- evidence ref and missing-evidence behavior;
- product bridge adoption metadata;
- blocked-surface vocabulary;
- proof artifact validation primitives;
- internal review artifacts for Core-owned boundaries.

Core does not own:

- product runtime behavior;
- product report authorship;
- product workspace edits;
- customer delivery approval;
- external pilot approval;
- hosted service behavior;
- public SDK behavior;
- live trading, broker/exchange, capital, holdout, or performance claims.

## Product Integration Pattern

Use this sequence:

```text
product artifact
  -> product-local receipt/evidence bundle
  -> product-local deterministic validators
  -> Core-compatible schema/evidence/product-bridge checks
  -> reviewer/verifier verdict
  -> reportable output or explicit blocker
```

The product artifact is the source of truth. Core-compatible checks are proof
guards.

## Integration Levels

| Level | Name | Description |
|---|---|---|
| 0 | Reference-only | Product uses Core vocabulary in docs only. |
| 1 | Receipt-compatible | Product emits local receipts with Core-compatible fields. |
| 2 | Schema-compatible | Product pins schema ids and can classify compatibility. |
| 3 | Evidence-lookup compatible | Product evidence refs can be checked deterministically. |
| 4 | Product bridge readiness | Core validates adoption metadata and blocked surfaces. |
| 5 | Runtime adapter | Product calls Core directly; deferred and ADR-gated. |

Default: Level 1 or 2 for active products. Level 4 only after product-local
validators exist.

## Current Product Mapping

| Product | Current proof surface | Recommended Core level | Next step |
|---|---|---:|---|
| Signal Analytics Sandbox | `auto_validation` evidence bundles, validator results, audit logs, decisions, MVP value run | 3 -> 4 | Map `auto_validation_result.v1` and `auto_validation_audit_log.v1` to Core schema/evidence lookup and product bridge adoption readiness. |
| Telegram Research Agent | `research_brief_receipt`, delivery refs, verification, operator review | 2 -> 3 | Add Core-compatible schema id and evidence lookup refs for research brief receipts and future channel intelligence receipts. |
| Demand-to-MVP Radar | opportunity/source trust/weekly report evidence | 1 -> 3 | Define weekly report proof receipt and evidence lookup rows before customer-facing recommendations. |
| Workflow-to-Agent Studio | workflow blueprint and permission boundary receipts planned | 1 -> 2 | Define blueprint receipt schema and schema compatibility before export automation. |
| AI Rollout Training OS | permission judgment and learner feedback planned | 1 -> 2 | Define scenario decision receipt and scoring verifier status. |
| Dream Motif Interpreter | privacy-sensitive memory action receipts optional | 0 -> 1 later | Keep Core optional; use only for export/deletion/memory receipts if needed. |

## Signal Sandbox Implication

The new Signal `auto_validation` engine should remain product-local. Core should
not import channel-specific market logic, provider eligibility, OCR rules,
customer-facing wording, or buyer discovery gates.

Core can add value by validating:

- schema ids and compatibility for evidence bundles, audit logs, and decisions;
- evidence refs exist and resolve to safe metadata;
- non-passed validator results carry blocker reasons;
- customer-facing approval remains blocked unless product policy gate passes;
- product bridge adoption metadata does not claim Core owns runtime/reporting.

## Playbook Interaction

The AI Workflow Playbook should reference Core as an optional proof layer for
high-evidence projects. It should not require Core for ordinary tasks. A
playbook project should adopt Core only when it has recurring proof artifacts
or repeated review risk around evidence, claims, schema drift, or verifier
status.

## Next Implementation Slice

Do not expand Core beyond the current human gate automatically. The next
human-approved Core slice should be narrow:

1. Define a generic `product_proof_receipt` vocabulary aligned with current
   Signal and Telegram receipt fields.
2. Add schema compatibility examples for Signal auto-validation artifacts.
3. Add evidence lookup examples for product-local evidence rows.
4. Add product bridge adoption metadata fixtures for Signal and Telegram.
5. Keep runtime adapters deferred.

Success means products can prove what their artifacts claim without Core
becoming their runtime or report owner.
