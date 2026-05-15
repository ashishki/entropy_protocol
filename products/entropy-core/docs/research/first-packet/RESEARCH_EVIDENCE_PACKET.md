# First Research Evidence Packet

Status: ARCHIVE_ONLY_NO_CLAIM
Schema version: first-research-evidence-packet/v1
Packet id: FIRST-RESEARCH-EVIDENCE-PACKET-001
Candidate id: FRC-001-VC-BREAKOUT-CONTINUATION
Evidence packet hash: GENERATED_BY_T18_TEST_FIXTURE

## Hash Bindings

- dataset_hash: bound by `docs/research/first-packet/DATASET_MANIFEST.md`
- code_hash: bound by T17 archive evaluation harness fixture
- policy_hash: bound by T17 archive evaluation harness fixture
- parameter_hash: bound by T17 archive evaluation harness fixture

## Evaluation Evidence

- leakage_status: PASS
- simbroker_fill_log_ids: generated deterministically by `src/entropy/research/evaluation.py`

## Attribution Streams

- stream_a: separated archive-only attribution stream
- stream_b: separated archive-only attribution stream
- stream_c: separated archive-only attribution stream
- stream_d: separated archive-only attribution stream

## No-Claim Labels

- archive_only_research_packet
- not_holdout_unlock
- not_oos_performance
- not_phase_gate_approval
- not_production
- not_capital_ready
- not_live_feed
- not_broker_exchange

## Blocked Approvals

- holdout_unlock: False
- oos_performance_approval: False
- phase_gate_approval: False
- production_approval: False
- capital_ready_approval: False
- live_feed_approval: False
- broker_exchange_approval: False

## Artifact References

- `docs/research/first-packet/CANDIDATE_PACKET.md`
- `docs/research/first-packet/DATASET_MANIFEST.md`
- `src/entropy/research/evaluation.py`
- `tests/integration/test_first_research_packet.py::test_research_packet_contains_required_sections`
