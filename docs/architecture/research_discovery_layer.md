# Entropy Protocol — Research Discovery Layer

**Version:** 1.0
**Last updated:** 2026-03-16
**Purpose:** Define the AI-assisted discovery layer that produces research artifacts without bypassing protocol discipline.

---

## Role

The Research Discovery Layer (RDL) is the research-facing layer where AI can assist with discovery work before anything enters the governed evaluation path.

Its output is limited to research artifacts.

The RDL does not:
- authorize experiments
- influence portfolio routing
- influence exposure sizing
- create admissible OOS evidence by itself

---

## Capabilities

### Market Observation

AI can summarize market structure, recurring conditions, event clusters, and candidate anomalies for human review.

### Hypothesis Generation

AI can propose explicit candidate hypotheses in structured form, including signal statement, threshold, metric, and expected direction.

### Research Critique

AI can challenge weak assumptions, detect ambiguity, surface multiplicity risk, and identify missing controls or missing baselines.

### Experiment Proposal

AI can draft experiment proposals that are ready for human review and Trial Registry preparation.

---

## Output Types

Typical RDL outputs include:
- `CandidateHypothesis`
- candidate `FeatureSpec`
- candidate `RegimeTag`
- candidate `EventLabel`
- research notes and critique memos

These are discovery objects, not protocol-authoritative artifacts.

---

## Boundary Rule

RDL outputs are research artifacts only.

They cannot influence the portfolio or evaluation pipeline directly.

Required path:
1. AI-assisted discovery
2. human review
3. experiment readiness review
4. Trial Registry registration
5. evaluation through the main protocol

If that path is not followed, the output remains discovery-only.

---

## Relationship to Core Protocol

The core protocol remains evaluation-first.

The RDL exists to improve research throughput while preserving:
- preregistration
- multiplicity control
- walk-forward discipline
- phase-gated rollout

The RDL expands research capacity, not protocol authority.
