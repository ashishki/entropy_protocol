# Entropy Core And Gensyn References

Status: active portfolio reference
Last updated: 2026-05-29

## Entropy Core Role

Entropy Core is the portfolio's optional verification kernel. It should define
schemas and validators for:

- action receipts;
- responsibility records;
- signal analysis receipts;
- research brief receipts;
- validator/referee verdicts;
- evidence bundles.

It must not own product-specific business logic for Trader Risk Audit, Signal
Analytics Sandbox, Telegram Research Agent, Workflow Studio, or Training OS.

## Cross-Project Use Levels

| Level | Description | Default |
|---|---|---|
| Reference-only | Project links to Core docs and follows vocabulary manually. | Yes |
| Receipt-compatible | Project emits local receipts with Core-compatible fields. | Yes for active AI/research products |
| CLI validation | Project runs Core validator manually or in CI. | Later, only after schemas stabilize |
| Runtime adapter | Project calls Core from app runtime. | Deferred |

## Standard Receipt Fields

```yaml
type: action_receipt
schema_version: v0
source_project: example-project
artifact_path: docs/example.yml
actor:
  role: codex
  authority: implementation
claim_or_action:
  summary: "What was claimed or done."
evidence:
  - path: docs/example.yml
    sha256: "..."
verifier:
  method: human_review
  status: passed
status: passed
limitations: []
```

## Gensyn-Inspired Pattern

Gensyn is a reference for diverse candidate generation, role-separated
evaluation, receipts, and verification-before-trust. Entropy adapts this as:

```text
candidate lenses -> evidence receipts -> referee verdict -> reportable output
```

Allowed:

- heterogeneous analytical lenses;
- proposer/solver/evaluator or generator/critic/referee roles;
- contribution/action receipts;
- quality-diversity search as a design analogy;
- optional local validation.

Not adopted:

- decentralized training runtime;
- token incentives;
- on-chain coordination by default;
- P2P swarm execution;
- model training or RL loops;
- mandatory Gensyn dependency.

## Open-Source Code Reuse

Gensyn repositories may be inspected because they are open source, but copying
code into this portfolio requires:

- license check;
- source repo, commit, and file references;
- attribution/NOTICE if required;
- an ADR explaining why a local implementation is not sufficient;
- security review before adding any runtime dependency.

Default: learn from patterns, do not copy code.
