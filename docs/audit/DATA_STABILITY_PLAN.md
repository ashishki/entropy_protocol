# DATA_STABILITY_PLAN
_Date: 2026-05-05 · Scope: P0.6-007 data-stability monitor tooling_

## Purpose

Define how to satisfy the Phase 0 data pipeline stability criterion: zero
unexplained gaps in the target universe over >=90 continuous days of feed
monitoring.

This plan does not activate a provider, fetch external data, approve Phase 0, or
make any performance claim.

## Gate Requirement

| Item | Requirement |
|------|-------------|
| Criterion | Data pipeline stable |
| Minimum duration | >=90 continuous days |
| Universe | Target universe |
| Gap tolerance | Zero unexplained gaps |
| Current status | `TOOLING_READY_EVIDENCE_MISSING` |
| Current implementation | Provider abstraction, local fixture adapter, data quality checks, monitoring row validation, JSONL round-trip, and summary tooling exist |

## Source Approval Required

Before monitoring starts, the human owner must approve:

- target universe snapshot;
- provider/source name;
- data license and storage boundary;
- whether external network egress is allowed;
- timeframe(s) monitored;
- calendar profile per asset (`weekday` or `continuous`);
- expected session schedule;
- allowed maintenance windows;
- gap classification policy;
- artifact storage path.

No provider activation or network egress is authorized by this document.

## Monitoring Scope

The future monitoring run should cover:

- all assets in the declared target universe;
- at least one canonical Phase 1 timeframe, with 1D required if P4 evidence uses
  the same dataset family;
- every calendar day in the 90-day window;
- source ingestion status;
- row-count status;
- timestamp continuity;
- OHLCV sanity checks;
- provider outage classification;
- manual disposition for every gap candidate.

## Daily Monitor Row Schema

Each asset/day/timeframe row should include:

| Field | Description |
|-------|-------------|
| `monitor_id` | Unique row ID |
| `monitor_date` | UTC date of check |
| `symbol` | Asset symbol |
| `timeframe` | Monitored timeframe |
| `calendar_profile` | `weekday` or `continuous` |
| `provider` | Approved source identifier |
| `provider_status` | `ok`, `partial`, `down`, or `unknown` |
| `expected_bars` | Expected bar count for the day/profile |
| `observed_bars` | Observed bar count |
| `first_ts` | First observed timestamp |
| `last_ts` | Last observed timestamp |
| `timestamp_check` | PASS/FAIL |
| `gap_check` | PASS/FAIL |
| `ohlcv_sanity_check` | PASS/FAIL |
| `dataset_hash` | Hash of ingested data slice or cumulative dataset |
| `raw_source_hash` | Hash of raw source extract if available |
| `gap_candidate` | Boolean |
| `gap_explained` | Boolean |
| `gap_reason_code` | Null or approved reason |
| `disposition_note_hash` | Hash of manual note if gap exists |
| `checked_at` | UTC timestamp of monitoring check |
| `checker` | Automated job or manual checker ID |

## Gap Reason Codes

Allowed reason codes must be declared before the monitoring run:

| Code | Meaning | Counts as unexplained? |
|------|---------|------------------------|
| `market_closed` | Expected no-session day for the asset calendar | No |
| `provider_announced_outage` | Source outage with independent provider notice | No if documented |
| `asset_halt` | Exchange/security halt with source evidence | No if documented |
| `symbol_mapping_change` | Approved mapping or corporate-action transition | No if documented |
| `late_arrival_corrected` | Data arrived late and was corrected with audit trail | No if corrected before packet close |
| `unknown_missing_bars` | Missing bars without approved explanation | Yes |
| `timestamp_discontinuity` | Unexpected timestamp break | Yes unless explained |
| `ohlcv_invalid` | Invalid OHLCV values | Yes unless corrected with audit trail |

The Phase 0 criterion requires zero unexplained gaps. Explained gaps may remain
visible, but every explanation must include evidence and a disposition note.

## Acceptance Packet

The future 90-day packet must include:

- monitoring window start/end;
- target universe snapshot hash;
- provider/source approval note;
- daily monitor table;
- per-asset summary table;
- total expected rows and observed rows;
- unexplained gap count;
- explained gap count by reason code;
- data quality summary;
- raw/cumulative dataset hash manifest;
- manual disposition notes;
- reproduction command or procedure;
- explicit statement that no performance/OOS claim is made.

Pass condition:

- >=90 continuous monitored days;
- every target-universe asset has daily status rows;
- unexplained gap count is zero;
- every explained gap has approved reason evidence;
- artifact hashes are present.

## Failure Handling

| Failure | Required action |
|---------|-----------------|
| Monitoring stops before 90 days | Restart or extend until a continuous 90-day window exists |
| Target universe changes mid-window | Restart unless change is pre-approved and versioned |
| Provider changes mid-window | Restart or create separate provider-version packet |
| Unknown missing bars | Fail the packet until explained or corrected |
| Missing hashes | Packet invalid |
| Manual notes missing | Explained gap becomes unexplained |

## Relationship To P4

If the same 1D data family is used for P4 evidence, the stability packet should
share source manifests and dataset hashes with the P4 label artifacts. Stability
evidence still does not prove P4 correctness; it only proves feed continuity and
quality monitoring.

## Non-Closure Rules

- T12-T14 tests do not close the 90-day criterion.
- Fixture data does not close the 90-day criterion.
- Provider interface existence does not close the criterion.
- A monitoring plan does not close the criterion.
- No OOS/performance report may imply stable live data until the 90-day packet
  passes.

## Implemented Tooling

P0.6-007 added:

- monitoring row model;
- daily monitor JSONL writer/reader;
- gap reason-code validator;
- summary generator;
- tests using synthetic fixtures only to validate monitoring logic.

This does not close the gate until a real approved 90-day monitoring packet
exists.
