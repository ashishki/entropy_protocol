# Shared Artifact Contract

Version: 1.0
Date: 2026-05-12
Status: FROZEN_FOR_PHASE_15_ADOPTION

This contract defines the minimal shared artifact shape that Trader Risk Audit
and Signal Analytics Sandbox may attach to real report outputs. It is an
internal Core support contract, not a public SDK, hosted service, product
runtime, or approval surface.

## Purpose

The contract gives product agents a common way to prove that a report artifact
is traceable, manually reviewed, and bounded by explicit no-claim language. It
does not move product-specific report logic into Core.

## Required Fields

Every product report artifact adopting this contract must record:

| Field | Required | Notes |
|---|---:|---|
| `artifact_contract_version` | Yes | Use `entropy-core-artifact/v1`. |
| `product` | Yes | Product identifier such as `trader-risk-audit` or `signal-analytics-sandbox`. |
| `run_id` | Yes | Product-local run, report, or packet identifier. |
| `input_refs` | Yes | Stable references to allowed input manifests, source packets, or redacted source lists. |
| `input_hashes` | Conditional | Required where safe and deterministic; omit or fingerprint only when raw input is private or externally volatile. |
| `policy_config_hash` | Yes | Hash of policy, extraction, report, or review configuration used by the product. |
| `code_version_ref` | Yes | Git SHA, branch plus commit, package version, or reviewed source snapshot. |
| `generated_artifact_refs` | Yes | Report, manifest, source pack, evidence table, or delivery packet references. |
| `limitations` | Yes | Known gaps, unsupported fields, volatile sources, manual judgment areas, and excluded claims. |
| `no_claim_boundary` | Yes | Product-specific no-claim labels and blocked surfaces. |
| `manual_validation_status` | Yes | One of the decision states below. |
| `error_register_ref` | Yes | Link or path to product-local error register, even when empty. |
| `external_delivery_approval_status` | Yes | Explicit delivery state; contract adoption is never delivery approval. |

## Decision States

`manual_validation_status` must be one of:

- `not_reviewed`
- `review_in_progress`
- `validated_internal_only`
- `validated_for_controlled_external_pilot`
- `blocked_by_errors`
- `rejected`

`external_delivery_approval_status` must be one of:

- `not_requested`
- `blocked`
- `approved_for_internal_demo`
- `approved_for_controlled_external_pilot`

No other value may imply public release, production readiness, capital
readiness, investment advice, future-performance claims, holdout approval, live
execution approval, or Core platformization approval.

## No-Claim Boundary

Contract adoption must preserve these blocked surfaces unless a later explicit
human decision and scoped task changes the boundary:

- no public Core SDK or hosted Core service;
- no Core-owned product-specific report generation;
- no holdout read, holdout unlock, or OOS/performance conclusion;
- no live feed activation, live order placement, broker/exchange execution, or
  live capital action;
- no production, capital-ready, investment advice, future-performance, or
  automated enforcement claim.

## Core Ownership Boundary

Core owns only the shared artifact validity vocabulary:

- required field names;
- decision-state vocabulary;
- no-claim boundary language;
- evidence and reproducibility expectations;
- product-neutral manual validation templates.

Trader Risk Audit and Signal Analytics Sandbox own:

- product-specific report logic;
- source ingestion and transformation rules;
- policy interpretation and domain findings;
- customer/pilot data handling;
- report copy, layout, and delivery decisions;
- product-local error registers and feedback logs.

Core must not rewrite Trader or Signal report logic during artifact validation.
Core may provide checklist language and product-neutral templates only.

## Trader Risk Audit Adoption Notes

Trader artifacts should bind the contract to product-local audit inputs:

- `product`: `trader-risk-audit`;
- `input_refs`: redacted trade export manifest, policy/rule manifest, violation
  source rows, and report source packet;
- `input_hashes`: required for redacted exports, policy/config files, violation
  tables, and generated report packets when hashing does not expose private raw
  customer data;
- `policy_config_hash`: hash of the approved risk policy, rule thresholds,
  attribution settings, and report configuration;
- `generated_artifact_refs`: audit report, violation table, attribution packet,
  limitation note, and delivery packet;
- `no_claim_boundary`: not order blocking, not live trading, not broker/exchange
  execution, not production, not capital-ready, and not investment advice;
- `manual_validation_status`: product operator must confirm that material
  findings match the source export and policy interpretation before any
  controlled external pilot.

The product may use limited fingerprints instead of raw input hashes when raw
customer exports must remain outside the repository.

## Signal Analytics Sandbox Adoption Notes

Signal artifacts should bind the contract to public-source research packets:

- `product`: `signal-analytics-sandbox`;
- `input_refs`: public source list, source capture notes, retrieval timestamps,
  quoted evidence refs, ambiguity register, and report packet;
- `input_hashes`: required for checked-in source packs or redacted captures;
  optional for live public pages whose content may change or disappear;
- `policy_config_hash`: hash of source selection rules, synthesis constraints,
  claim language rules, and review configuration;
- `generated_artifact_refs`: research report, evidence/source table,
  unsupported-field register, ambiguity register, and delivery packet;
- `no_claim_boundary`: not trading advice, not future-performance prediction,
  not investment recommendation, not automated signal execution, not production,
  and not capital-ready;
- `manual_validation_status`: product operator must confirm source traceability,
  ambiguity handling, and claim safety before any controlled external pilot.

Public-source capture reproducibility may be partial. The artifact must say
which fields are hash-reproducible, which depend on source availability, and
which require manual review.

## Minimum Artifact Skeleton

```yaml
artifact_contract_version: entropy-core-artifact/v1
product: ""
run_id: ""
input_refs: []
input_hashes: []
policy_config_hash: ""
code_version_ref: ""
generated_artifact_refs: []
limitations: []
no_claim_boundary: []
manual_validation_status: not_reviewed
error_register_ref: ""
external_delivery_approval_status: not_requested
```

## Adoption Rule

Products may copy this contract into product-local report packets or reference
it from their own artifact docs. Product-local copies are allowed when they keep
the same required fields, decision states, no-claim boundary, and Core ownership
boundary.
