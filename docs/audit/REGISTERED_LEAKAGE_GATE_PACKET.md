# Registered Leakage Gate Packet

Date: 2026-05-05
Status: ACCEPTED_AS_LEAKAGE_GATE_EVIDENCE

## Scope

Assemble the Phase 0 registered leakage/temporal-shuffling gate packet from the
existing leakage checklist, OOS-blocking runner, accepted purge/embargo
methodology, and the new temporal-shuffling audit.

## Artifact

| Artifact | Path |
|---|---|
| Manifest | `artifacts/evidence/leakage_gate/REGISTERED_LEAKAGE_GATE_MANIFEST.json` |

## Components

| Component | Method | Status |
|---|---|---|
| Leakage checklist | T19 four-check checklist | PASS |
| Omitted detector policy | Missing detector callbacks return FAIL | PASS |
| OOS block | T20 runner blocks OOS if leakage check is missing or failing | PASS |
| Purge/embargo | `PE-MAX-HORIZON-v1` | PASS |
| Temporal shuffle | `TS-OOS-SHUFFLE-v1` | PASS |

## Temporal Shuffle Rule

`TS-OOS-SHUFFLE-v1` verifies that IS feature output is invariant to deterministic
OOS temporal shuffling. If the IS feature hash changes after OOS is reversed,
the audit fails.

This directly addresses the Phase 0 leakage criterion for zero forward-looking
features under temporal shuffling.

## Verification

Commands:

- `.venv/bin/pytest tests/unit/test_temporal_shuffle.py tests/integration/test_leakage.py tests/integration/test_walk_forward.py tests/unit/test_purge_embargo.py`
- `.venv/bin/ruff check entropy/walkforward/temporal_shuffle.py entropy/walkforward/__init__.py tests/unit/test_temporal_shuffle.py`

Result:

- pytest: 28 passed, 2 skipped;
- ruff: passed.

## Acceptance

Accept this packet as current Phase 0 leakage/temporal-shuffling gate evidence.
The registered leakage evidence blocker is closed.

## Boundary

This packet does not approve Phase 0 by itself, start Phase 1, authorize live
capital, or make OOS/performance claims.
