# Entropy Protocol — Research Knowledge Graph

**Version:** 1.0
**Last updated:** 2026-03-16
**Purpose:** Define a minimal structured metadata layer for long-term research memory.

---

## Role

The Research Knowledge Graph is a lightweight metadata layer for tracking research objects and their relationships over time.

It is not a predictive model and not a trading engine.

Its purpose is to:
- track hypotheses
- track experiments
- track results
- avoid repeating failed ideas
- support AI-assisted research analysis with structured memory

---

## Core Entities

### Hypothesis

A structured research claim that can be tested.

### Feature

A versioned input or transformation used by a hypothesis or experiment.

### Experiment

A registered test instance that evaluates a hypothesis under a defined protocol.

### Result

The recorded outcome of an experiment, including success, failure, invalidation, or ambiguity.

### Dataset

The data source or versioned data slice used for an experiment or feature.

### Regime

A governed market-state object used for conditioning, segmentation, or review.

---

## Example Relationships

- `Hypothesis -> uses_feature -> Feature`
- `Experiment -> tests -> Hypothesis`
- `Experiment -> produces -> Result`
- `Result -> invalidates -> Hypothesis`
- `Hypothesis -> belongs_to -> Family`
- `Experiment -> uses_dataset -> Dataset`
- `Hypothesis -> conditioned_on -> Regime`

---

## Governance Use

The graph helps:
- detect duplicate or near-duplicate ideas
- track which families are saturated
- preserve memory of invalidated hypotheses
- connect experiment outcomes back to feature and dataset lineage
- support AI critique without relying on unstructured session memory

---

## Constraint

The Research Knowledge Graph is a metadata layer only.

It does not override:
- the Trial Registry
- the walk-forward harness
- phase-gating rules
- protocol kill logic

It improves research memory and traceability, but it is not admissible evidence by itself.
