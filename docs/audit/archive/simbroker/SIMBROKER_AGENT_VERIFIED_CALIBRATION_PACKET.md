# SimBroker Agent-Verified Calibration Packet

Date: 2026-05-05
Status: ACCEPTED_AS_SIMBROKER_CALIBRATION_EVIDENCE

## Scope

Close the Phase 0 SimBroker calibration evidence blocker using owner-approved
agent-assisted deterministic verification.

Authority:

- D-026 approves agent-assisted deterministic verification as equivalent to
  manual verification for Phase 0 SimBroker calibration evidence.
- Source approval remains limited to approved free public crypto sources.

## Artifacts

| Artifact | Path |
|---|---|
| Agent-verified rows | `artifacts/evidence/simbroker_calibration/agent_verified_001/SIMBROKER_AGENT_VERIFIED_CALIBRATION_ROWS.jsonl` |
| Agent-verified summary | `artifacts/evidence/simbroker_calibration/agent_verified_001/SIMBROKER_AGENT_VERIFIED_CALIBRATION_SUMMARY.md` |
| Source bootstrap manifest | `artifacts/evidence/simbroker_calibration/bootstrap_001/SIMBROKER_CALIBRATION_BOOTSTRAP_MANIFEST.json` |
| Raw quote extracts | `artifacts/evidence/simbroker_calibration/bootstrap_001/raw/` |

## Result

| Metric | Value |
|---|---:|
| Required included rows | 100 |
| Included rows | 100 |
| Excluded rows | 0 |
| Pass count | 100 |
| Failure count | 0 |
| Assets | 5 |
| Packet status | `PACKET_READY_FOR_REVIEW` |

Assets: BTC-USD, ETH-USD, LTC-USD, BCH-USD, XLM-USD.

Sources:

- Coinbase Exchange public API;
- Kraken public API.

Verifier: `codex_agent_assisted_verifier`.

## Acceptance

Accept this packet as SimBroker calibration evidence for the current Phase 0
gate packet. The SimBroker calibration evidence blocker is closed.

## Boundary

This packet does not approve Phase 0 by itself, start Phase 1, authorize live
capital, activate a broker, trade, or make OOS/performance claims.
