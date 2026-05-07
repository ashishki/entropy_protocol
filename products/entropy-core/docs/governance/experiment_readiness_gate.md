# Entropy Protocol — Experiment Readiness Gate

**Version:** 1.0
**Last updated:** 2026-03-16
**Purpose:** Define the minimum checklist required before a new experiment enters the Trial Registry.

---

## Gate Rule

No new experiment enters active evaluation unless every readiness item below is answered explicitly.

---

## Required Checklist

- Hypothesis is falsifiable.
- Primary metric is defined.
- Baseline or control condition is defined.
- Evaluation window and sample requirements are defined.
- Leakage risks are identified.
- Hypothesis family is assigned.
- Trial Registry entry is prepared.
- Output interpretation rule is stated in advance.

---

## Minimum Specification

Each experiment proposal must contain:
- hypothesis ID
- plain-language hypothesis statement
- exact rule or feature definition being tested
- expected direction of effect
- primary metric
- baseline comparator
- minimum sample requirement
- failure condition or invalidation condition
- hypothesis family
- named human sponsor

---

## Leakage Review

Before registration, the proposal must identify the main leakage risks, including:
- look-ahead in labels or features
- reuse of calibration information across OOS boundaries
- post-hoc threshold tuning
- hidden dependence on recent charts or recent narrative context

If leakage risk cannot be described clearly, the experiment is not ready.

---

## Decision

An experiment is ready only when the checklist is complete.

If any required item is missing, the proposal stays in discovery status and does not enter the main evaluation protocol.
