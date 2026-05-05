# Data Stability Archive Packet

Date: 2026-05-05
Task: P0.7-028
Packet ID: `DATA-STABILITY-ARCHIVE-90D-v1`
Status: `PACKET_READY_FOR_REVIEW`

## Decision

The archive-mode data-stability packet is accepted for the current archive-only
research foundation. It closes the data-stability blocker only under D-027
archive-only evidence mode.

It does not prove live feed stability, provider uptime, streaming reliability,
or readiness for live capital.

## Inputs

| Input | Value |
|---|---|
| Source family | Binance public archive files already collected for revised P4 evidence |
| Source manifest count | 15 |
| Window | 2020-01-01 through 2025-12-31 |
| Timeframe | 1d |
| Target assets | ADAUSDT, ALGOUSDT, ATOMUSDT, BCHUSDT, BNBUSDT, BTCUSDT, DOGEUSDT, ETCUSDT, ETHUSDT, LINKUSDT, LTCUSDT, TRXUSDT, VETUSDT, XLMUSDT, XRPUSDT |

## Results

| Metric | Value |
|---|---|
| Row count | 32880 |
| Monitored archive days | 2192 |
| Required days | 90 |
| Missing symbol-days | 0 |
| Unexplained gaps | 0 |
| Packet status | `PACKET_READY_FOR_REVIEW` |

## Artifacts

| Artifact | Path |
|---|---|
| Archive rows | `artifacts/evidence/data_stability/archive_2020_2025/DATA_STABILITY_ARCHIVE_ROWS.jsonl` |
| Archive summary | `artifacts/evidence/data_stability/archive_2020_2025/DATA_STABILITY_ARCHIVE_SUMMARY.md` |
| Archive manifest | `artifacts/evidence/data_stability/archive_2020_2025/DATA_STABILITY_ARCHIVE_MANIFEST.json` |
| Tooling | `entropy/evidence/data_stability_archive.py` |
| Tests | `tests/unit/test_data_stability_archive.py` |

## Boundary

The packet is archive-only. `gate_claim_allowed` is false in the manifest to
preserve manual gate review. The packet supports archive research foundation
closure under D-027 and must not be cited as live feed stability evidence.

