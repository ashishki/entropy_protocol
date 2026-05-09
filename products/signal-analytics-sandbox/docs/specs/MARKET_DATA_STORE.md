# Market Data Store Contract

Version: 0.1
Date: 2026-05-09
Status: specification for `SAS-MI-004`

## Purpose

The market-data store persists local OHLCV snapshots for deterministic thesis
evaluation. It records enough metadata to prove what provider/source, symbol,
range, timeframe, checksum, license, and provenance were used.

This task introduces local storage only. It does not add paid providers, network
fetching, embeddings, retrieval, or batch-agent behavior.

## Interface

`MarketDataStoreProtocol` supports:

| Method | Rule |
|--------|------|
| `write_snapshot(snapshot)` | Persist one snapshot immutably. Rewriting identical bytes is idempotent; rewriting different bytes to the same ID raises. |
| `load_snapshot(snapshot_id)` | Load bytes and metadata, then verify checksum before returning. |
| `list_snapshots()` | Return metadata sorted by snapshot ID. |

## Snapshot Metadata

Every snapshot records:

| Field | Required | Rule |
|-------|----------|------|
| `snapshot_id` | yes | Single path segment; stable caller-provided ID. |
| `provider` | yes | `operator_file` for the first local fixture path. |
| `canonical_asset_id` | yes | Asset universe ID such as `CRYPTO:BTC`. |
| `provider_symbol` | yes | Provider/local-file symbol such as `BTC/USDT`. |
| `timeframe` | yes | Resolution such as `1d` or `1h`. |
| `source_range_start_utc` | yes | First timestamp covered by the source rows. |
| `source_range_end_utc` | yes | Last timestamp covered by the source rows. |
| `captured_at_utc` | yes | When the operator captured or exported the local fixture. |
| `data_sha256` | yes | SHA-256 of stored OHLCV bytes. |
| `license` | yes | License/provenance status, initially `operator_provided`. |
| `provenance` | yes | Human-readable source/fixture description. |

## Storage Layout

Snapshots are stored under:

```text
<workspace>/market_data/snapshots/<snapshot_id>/
  ohlcv.parquet
  metadata.json
```

The snapshot ID must be a single path segment. This prevents path traversal and
keeps local fixture storage deterministic.

## Immutability

If a snapshot directory already exists:

- identical data bytes and metadata bytes are accepted as idempotent;
- any different data or metadata raises `SnapshotAlreadyExists`;
- checksum mismatch at model construction or load raises
  `SnapshotChecksumMismatch`.

## Operator Fixture Path

`make_operator_file_snapshot()` creates an `operator_file` snapshot from local
operator-provided OHLCV rows. This is the first supported path because it avoids
new paid or network provider behavior while preserving the deterministic data
contract needed by future horizon metrics.

## Non-Goals

- No network market-data fetching.
- No paid provider activation.
- No provider licensing inference beyond explicit metadata fields.
- No RAG/vector store.
- No horizon metric computation; `SAS-MI-005` owns metrics.
