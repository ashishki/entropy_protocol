# SimBroker Agent-Assisted Verification Decision

Date: 2026-05-05
Status: APPROVED_BY_OWNER

## Question

Can Codex automate selection and verification of SimBroker calibration rows
instead of requiring the user to manually pick rows?

## Decision

Automated row selection and candidate assembly are allowed as engineering
tooling.

Agent-assisted deterministic verification is approved as equivalent to manual
verification for Phase 0 SimBroker calibration evidence, provided the packet
records raw source hashes, approved source IDs, deterministic row construction,
stale/mismatch rejection, and outlier checks.

## What Codex Can Do

- select representative assets and timestamps;
- fetch approved public bid/ask quotes;
- hash raw source extracts;
- pair quotes with real SimBroker `FillLog` records;
- compute reference price, deviation, and `pass_15pct`;
- reject stale/mismatched quotes;
- produce candidate JSONL rows and summaries;
- surface outliers for review.

## Approval Record

Owner approval was given in-session on 2026-05-05: "разрешаю".

This approval authorizes `manual_verifier` values such as
`codex_agent_assisted_verifier` for Phase 0 calibration packets when the
deterministic verification procedure is reproducible from recorded artifacts.

## Boundary

This decision only changes verification authority for SimBroker calibration
rows. It does not approve Phase 0, start Phase 1, authorize live capital, or make
OOS/performance claims.
