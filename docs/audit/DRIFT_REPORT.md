# DRIFT_REPORT — D-K Deep Review

**Audit cycle:** Cycle 5 — Phase 1D-K archive-only baseline deep review
**Date:** 2026-05-06
**Prior artifact:** `DRIFT_ASSERTIONS.md`
**Status:** Draft — pending Spec Owner acceptance

## Executive Summary

Twelve D-K invariants were checked. After fix closure, twelve pass.
No finding authorizes Phase 1 trading, holdout access, production labels,
capital-ready labels, live feeds, broker integration, Growth/RDL/RBE activation,
or performance claims.

The critical engineering drift found during review was reproducibility in P1F
code hashing. The main reporting ambiguity was that P1I listed statistic field
names although P1H intentionally does not compute strategy performance
statistics. The governance drift was prompt metadata. All three are fixed in the
current working tree.

## Fixed Findings

### DK-INV-005 — P1F Reproducible Code Hash

Expected: identical repository source contents produce identical code hashes
regardless of whether callers pass repository-local paths as relative or
absolute paths.

Found during review: `_hash_source_files()` hashed `path.as_posix()` directly.
Absolute and relative references to the same file could produce different code
hashes.

Impact: preregistration reproducibility can diverge across machines or calling
contexts. Severity: P1. Finding: F-DK-001.

Applied action: repository-local source paths are normalized before inclusion in
the code hash payload, with regression coverage.

### DK-INV-012 — Prompt Current Metadata

Expected: active prompt headers identify the current D-K review state.

Found during review: the prompt sequence was labeled Cycle 4 / Post-Phase-1A
while current state was full D-K deep review after `P1K-HUMAN-001`.

Impact: future audit sessions may load stale context before reading current
state docs. Severity: P2. Finding: F-DK-003.

Applied action: prompt headers/current-cycle context were refreshed without
changing the six-step protocol or hard constraints.

### DK-INV-010 — P1I Statistic Status Clarity

Expected: report packets distinguish required statistic inventory from computed
statistics and phase-gate evidence.

Found during review: `Phase1IEvaluationReport` recorded `stat_fields` only.
Since P1H is a metadata-only mechanics run, these fields are not computed
performance statistics.

Impact: a reader can mistake inventory for produced statistical evidence.
Severity: P2. Finding: F-DK-002.

Applied action: deterministic per-field status metadata now records
`not_computed_no_performance_conclusion`.

## Growth / RDL Surface

D-K does not activate Growth, RDL, RBE, live feeds, broker integration, or
capital allocation. Existing dormant-module constraints remain intact.

## Scope Of Next Actions

| Finding | Required action | Frozen non-negotiable modified? | ADR required? |
|---|---|---|---|
| F-DK-001 | Applied code/test fix in P1F hash binding | No | No |
| F-DK-002 | Applied code/test fix in P1I report status fields | No | No |
| F-DK-003 | Applied prompt metadata refresh | No | No |
