# SimBroker Calibration Bootstrap

Date: 2026-05-05
Status: BOOTSTRAP_COMPLETE_NOT_GATE_EVIDENCE

## Scope

Prepare the no-budget SimBroker calibration evidence path using only approved
public quote sources. This bootstrap records raw bid/ask quote snapshots and
source hashes for future manual calibration review.

## Source Boundary

| Source | Domain | Use case | Result |
|---|---|---|---|
| `coinbase_exchange_public_api` | `api.exchange.coinbase.com` | `simbroker_calibration` | PASS |
| `kraken_public_api` | `api.kraken.com` | `simbroker_calibration` | PASS |

Rejected/not used:

- paid APIs;
- authenticated broker APIs;
- live trading endpoints;
- non-approved domains.

## Artifacts

| Artifact | Path |
|---|---|
| Manifest | `artifacts/evidence/simbroker_calibration/bootstrap_001/SIMBROKER_CALIBRATION_BOOTSTRAP_MANIFEST.json` |
| Summary | `artifacts/evidence/simbroker_calibration/bootstrap_001/SIMBROKER_CALIBRATION_BOOTSTRAP_SUMMARY.md` |
| Raw quote extracts | `artifacts/evidence/simbroker_calibration/bootstrap_001/raw/` |

## Bootstrap Result

| Metric | Value |
|---|---:|
| Quote targets | 10 |
| Done | 10 |
| Failed | 0 |
| Sources | 2 |
| Representative assets | 5 |
| Calibration rows created | 0 |
| Manual verification complete | false |
| Gate claim allowed | false |

Assets: BTC-USD, ETH-USD, LTC-USD, BCH-USD, XLM-USD.

## Decision

Accept the public quote source path as bootstrap-ready for SimBroker calibration
candidate work.

This does not close the SimBroker calibration gate. The Phase 0 gate still
requires >=100 manually verified calibration rows with SimBroker fill prices,
approved quote references, source hashes, and review notes.

## Boundary

This bootstrap does not approve Phase 0, start Phase 1, activate a broker, trade,
create manually verified calibration rows, or make OOS/performance claims.

## Next Step

Start P0.7-019: SimBroker Calibration Candidate Row Plan. Define how real
SimBroker fill logs will be paired with these approved public quote snapshots
without synthetic gate closure or post-hoc tuning.
