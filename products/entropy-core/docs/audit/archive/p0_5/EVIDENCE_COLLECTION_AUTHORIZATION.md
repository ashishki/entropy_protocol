# EVIDENCE_COLLECTION_AUTHORIZATION
_Date: 2026-05-05 · Scope: P0.6-008 evidence collection authorization packet_

## Decision

Decision: `APPROVED_LIMITED_FREE_CRYPTO_SOURCES`.

P0.6 implementation tooling is ready for offline evidence preparation. The human
owner approved a no-budget/free-source bootstrap on 2026-05-05 and delegated the
source choice to the implementation agent. The selected path is crypto-first:
Binance public archive as the primary OHLCV source, with Kraken and Coinbase
Exchange public APIs as cross-check sources for bid/ask and monitoring.

This is a limited approval only. It authorizes egress to the approved public
domains listed below for evidence bootstrap work. It does not authorize paid
services, authenticated broker APIs, live trading, Phase 0 approval, Phase 1
start, or OOS/performance claims.

## Approved Source Selection

Selection ID: `FREE-CRYPTO-SOURCES-v1`.

| Source | Role | Approved use cases | Domains | API key | Notes |
|--------|------|--------------------|---------|---------|-------|
| Binance public archive | Primary | P4 label coverage; data stability | `data.binance.vision` | No | Bulk historical crypto OHLCV from public archive |
| Kraken public API | Cross-check | SimBroker calibration; data stability | `api.kraken.com` | No | Public ticker/depth and short-window OHLC checks |
| Coinbase Exchange public API | Cross-check | SimBroker calibration; data stability | `api.exchange.coinbase.com` | No | Public product ticker/candles checks |

Rejected for the first no-budget bootstrap:

- Alpha Vantage free tier: too constrained for multi-asset evidence collection
  and unsuitable for free US equity bid/ask evidence.
- Stooq daily equities: useful for exploratory EOD equity OHLCV, but no reliable
  bid/ask path for SimBroker calibration and not selected for Phase 0 evidence.

## Current Tooling State

| Evidence surface | Tooling status | Evidence status |
|------------------|----------------|-----------------|
| P4 label coverage | `P4-RBL-v1` labeler and label artifact generator implemented | Missing approved target universe and historical data coverage |
| SimBroker calibration | Calibration row validation, JSONL round-trip, and summary tooling implemented | Missing >=100 manually verified bid/ask rows |
| Data stability | Monitoring row validation, JSONL round-trip, and summary tooling implemented | Missing >=90 continuous monitored days |

## Authorization Requirements

### P4 Historical Label Coverage

Required human approvals:

- target 20-asset universe snapshot;
- approved 1D data source or local dataset family;
- data license and storage boundary;
- source/dataset hash manifest location;
- calendar profile per asset (`weekday` or `continuous`);
- minimum accepted history window;
- artifact storage path for label JSONL files and coverage summaries;
- whether external network egress is allowed for data acquisition.

Current authorization status: `APPROVED_LIMITED`.

Approved source: Binance public archive on `data.binance.vision`.
Approved universe class: crypto only.
Approved calendar profile: `continuous`.
Approved timeframe: `1d`.
Storage boundary: local project artifacts only.
External egress: allowed only to `data.binance.vision`.

### SimBroker Bid/Ask Calibration

Required human approvals:

- quote source name;
- source type: broker export, exchange quote export, or approved historical
  quote dataset;
- asset universe and sample design;
- timestamp tolerance and timezone normalization rule;
- quote staleness limit;
- allowed spread anomalies and pre-scoring exclusion rules;
- raw quote extract storage path;
- manual verifier identity or verification procedure;
- whether external network egress is allowed for quote acquisition.

Current authorization status: `APPROVED_LIMITED`.

Approved sources: Kraken public API and Coinbase Exchange public API.
Approved universe class: crypto only.
Approved mode: prospective bid/ask snapshots for synthetic/SimBroker fills.
External egress: allowed only to `api.kraken.com` and
`api.exchange.coinbase.com`.

### Data-Stability Monitoring

Required human approvals:

- target universe snapshot;
- provider/source name;
- data license and storage boundary;
- monitored timeframe(s);
- calendar profile per asset;
- expected session schedule;
- allowed maintenance windows;
- gap classification policy;
- artifact storage path;
- whether external network egress is allowed for monitoring.

Current authorization status: `APPROVED_LIMITED`.

Approved sources: Binance public archive for historical OHLCV and Kraken /
Coinbase Exchange public APIs for short-window cross-checks.
Approved universe class: crypto only.
Approved calendar profile: `continuous`.
Approved timeframes: `1d` and `1h`.
External egress: allowed only to `data.binance.vision`, `api.kraken.com`, and
`api.exchange.coinbase.com`.

## Approval Record

| Field | Value |
|-------|-------|
| `approval_id` | `P0.6-HUMAN-001-FREE-CRYPTO` |
| `approved_by` | Human owner via chat instruction |
| `approval_ts_utc` | 2026-05-05 |
| `scope` | `all_phase0_evidence` limited to free crypto sources |
| `approved_sources` | Binance public archive; Kraken public API; Coinbase Exchange public API |
| `approved_universe_hash` | `6d4287839640086728536ab5b40f4592e924f1b22e18c6c1c8e3190bf7d4d4cd` |
| `egress_allowed` | Yes, only approved public domains above |
| `storage_boundary` | Local project artifacts; no paid service storage |
| `artifact_paths` | Pending concrete evidence run paths |
| `exclusion_or_gap_policy_hash` | Existing P0.6 calibration and stability policies; concrete run hash pending |
| `notes` | No paid data, no authenticated broker API, no live trading |

## Minimum Approval Record

Before any real evidence run starts, the human owner must add or approve a
record with:

| Field | Required |
|-------|----------|
| `approval_id` | Yes |
| `approved_by` | Yes |
| `approval_ts_utc` | Yes |
| `scope` | One of `p4_label_coverage`, `simbroker_calibration`, `data_stability`, or `all_phase0_evidence` |
| `approved_sources` | Yes |
| `approved_universe_hash` | Yes where a universe is required |
| `egress_allowed` | Explicit yes/no |
| `storage_boundary` | Yes |
| `artifact_paths` | Yes |
| `exclusion_or_gap_policy_hash` | Yes where applicable |
| `notes` | Optional |

## Collection Boundary

Even with this limited approval:

- do not use paid APIs;
- do not use authenticated broker APIs;
- do not trade or route capital;
- do not fetch from unapproved domains;
- do not claim P4 coverage closure;
- do not claim SimBroker calibration closure;
- do not claim 90-day data stability closure;
- do not approve Phase 0 or start Phase 1.

Evidence collection must still produce reviewable packets using the P0.6 tooling
and must keep all artifacts marked as evidence, not performance or OOS claims.

## Next Human Action

The target crypto universe snapshot and first source-manifest bootstrap are now
recorded in `products/entropy-core/docs/audit/CRYPTO_UNIVERSE_SNAPSHOT.md` and
`products/entropy-core/docs/audit/SOURCE_MANIFEST_BOOTSTRAP.md`. Next, run a tiny hash-recorded
Binance OHLCV canary before attempting full P4 coverage or 90-day monitoring.
