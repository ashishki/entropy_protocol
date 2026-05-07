# Evidence Index - Trader Risk Audit

Version: 1.0
Last updated: 2026-05-07

This file indexes durable proof so agents can retrieve evidence quickly. It is not authoritative by itself; every row must point to the real artifact.

---

## When To Use

Maintain this file because Trader Risk Audit has a heavy P&L attribution task and will accumulate pilot evidence, golden fixtures, and phase review reports.

## Evidence Table

| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |
|------------------------|---------------|----------|---------------|---------------|------------|

No evidence rows are recorded yet. Add rows only after the referenced artifact exists.

## Retrieval Rules

- Prefer rows that match the current task's `Context-Refs`, open findings, or heavy-task evidence.
- If an evidence row points to a stale or missing artifact, fix the artifact or mark the row pending until the artifact exists.
- Do not treat a journal note as proof when a test, eval, fixture, or review report exists.
