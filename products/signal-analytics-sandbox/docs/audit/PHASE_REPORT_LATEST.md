# Phase 27 Report - Three-Channel V1 Metric Report

Date: 2026-05-19

## What Was Built

Phase 27 produced the internal V1 channel utility package:

- V1 approval matrix;
- false-positive/false-negative review and extractor calibration;
- deterministic structured claim extractor;
- level-aware outcome engine;
- reviewed-media claim path and media inventory;
- provider/proxy config and fetch planning;
- V1 metric recompute and scorecard;
- customer-readable internal report;
- external-ready gate;
- Phase 27 deep review and archive.

## Why It Matters

The product now demonstrates an end-to-end internal V1 workflow for measuring
public channel utility while preserving evidence, provider, media, and
no-overclaim boundaries.

## Validation

- `.venv/bin/python -m pytest tests/ -q`: 215 passed
- `.venv/bin/ruff check src/ tests/ scripts/`: pass
- `.venv/bin/ruff format --check src/ tests/ scripts/`: pass
- `.venv/bin/pyright`: pass
- Phase 27 review archived at `docs/archive/PHASE27_REVIEW.md`

## Review Results

- P0: 0
- P1: 0
- P2: 0
- Stop-Ship for internal closure: No
- External delivery: not approved
- Gate decision: `approve_internal_only`

## Final Product State

- Planned phases 0-27 are complete.
- Internal V1 product validation package is complete.
- External/customer-facing delivery remains blocked.
- V1 metrics are internal research/product-validation artifacts.

## Open Product Gate Findings

The Phase 27 close carries these limitations:

- full-corpus human/operator extraction review is not complete;
- false negatives remain pending extraction and outcome handling;
- futures, FX, broad indices, US ETFs/funds, commodities, and benchmarks need
  provider/proxy expansion;
- no media-backed claim is customer-facing eligible;
- RR/setup coverage is too sparse for paid external delivery.

## Health Verdict

OK for internal V1 validation. Not ready for external delivery.

The implementation preserved Hybrid / Lean / T0, RAG ON, Agentic ON, Tool-Use
OFF, Planning OFF, Compliance OFF, public-source-only handling,
draft-evidence/human-review media posture, deterministic outcome ownership,
source-truth preservation, and non-advice boundaries.

## Next Action

No further planned implementation task is defined. Next decision is operator
strategy: full human review, provider/media expansion, or internal buyer-demo
packaging.

## Notification Summary

Ph27 V1 Channel Utility DONE
Built: approval matrix, calibration, extractor, outcomes, media gate, provider config, V1 metrics, report, external gate, deep review
Tests: 215 pass / 0 skip
Issues: P1:0 P2:0 implementation; external delivery not approved
Health: internal V1 validation OK, not external-ready
Next: operator strategy decision
