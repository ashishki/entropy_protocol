# Entropy Protocol — System Architecture

**Version:** 1.0
**Last updated:** 2026-03-16
**Purpose:** Summarize the active system layers and their governance boundaries without redefining the protocol.

---

## Layer Map

### 1. Core Protocol Layer

Authority documents:
- `docs/core/PROTOCOL_SPEC.md`
- `docs/core/CHARTER.md`
- `docs/core/EVOLUTION.md`
- `docs/core/GLOSSARY.md`

Role:
- define non-negotiables
- define phase sequencing
- define evaluation, kill, and escalation rules

### 2. Evaluation Infrastructure Layer

Primary components:
- data pipeline
- walk-forward harness
- Trial Registry
- SimBroker
- P&L attribution engine

Role:
- produce admissible evidence
- enforce IS/OOS separation
- make cost and attribution auditable

### 3. Strategy and Portfolio Layer

Primary components:
- base skills
- portfolio allocation logic
- regime signal hierarchy P1-P4
- Growth Layer monitors

Role:
- translate governed signals into position targets
- enforce structural risk controls
- preserve gross and attribution constraints

### 4. Research Discovery Layer

Primary components:
- candidate hypothesis generation
- regime and event labeling research
- feature library development

Role:
- structure discovery work
- prepare candidates for human review and preregistration

Constraint:
- discovery is not evaluation
- no direct routing or phase-gate authority before governed promotion

### 5. Governance Layer

Primary components:
- research firewall
- experiment readiness gate
- hypothesis family registry
- hypothesis budget controls
- audit pipeline

Role:
- control admissibility
- control multiplicity exposure
- prevent research outputs from bypassing evaluation discipline

---

## Authority Boundaries

- The core protocol defines what is allowed.
- The architecture documents explain how layers fit together.
- Governance documents define when research outputs are admissible.
- Audit artifacts verify whether the documented rules remain coherent and enforceable.

No architecture document overrides the core protocol.
