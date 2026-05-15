# Archive Evidence Reproducibility Matrix

Status: ARCHIVE_ONLY_HASH_BOOKKEEPING
Task: T27 Evidence Hash Reproducibility Matrix
Last updated: 2026-05-08

This matrix records deterministic hash bindings for the existing archive-only
research evidence packets. It is bookkeeping for reproducibility only. It does
not rank hypotheses, compare profitability, open holdout, approve OOS or
performance claims, or approve live, broker/exchange, production, phase-gate, or
capital-ready use.

## Required Hash Categories

- candidate_packet_hash
- dataset_hash
- code_hash
- policy_hash
- parameter_hash
- evidence_artifact_hash
- replay_json_hash

## Packet Matrix

| Packet | Candidate id | candidate_packet_hash | dataset_hash | code_hash | policy_hash | parameter_hash | evidence_artifact_hash | replay_json_hash | Source artifacts |
|--------|--------------|-----------------------|--------------|-----------|-------------|----------------|------------------------|------------------|------------------|
| first | FRC-001-VC-BREAKOUT-CONTINUATION | 42ad5b14e954012c8fb64c8c7d20c858d3c263ebabdac5d1ea1f9c571732f56e | 535813acc11619778ebc437ecb78a9c9aaa86aab1cd69a8b74b48627a643e050 | eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee | ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff | 1111111111111111111111111111111111111111111111111111111111111111 | d1340fed9b140c728c53a71b9eacf47bc0320ef6d69dd2ef09bfe29862ce71ca | b166399c65dcee07b6883efe101c05b8941c27c9e7eef88704c10fbc8aa0028d | `docs/research/first-packet/CANDIDATE_PACKET.md`; `docs/research/first-packet/DATASET_MANIFEST.md`; `docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md`; `tests/integration/test_archive_replay.py` |
| second | SRC-001-STRUCTURE-RETEST-BOUNCE | 7eff68b12d1e3f236639d24bc993203511d23bb326c28e82e9d4ad7d23be570d | 3c93958592a682c5817728c3659796af281d9350f004d056960de1a8509321cb | 2222222222222222222222222222222222222222222222222222222222222222 | 3333333333333333333333333333333333333333333333333333333333333333 | 4444444444444444444444444444444444444444444444444444444444444444 | c06616447252c68d5c3c58a02f93ed1876f5bfea5a4f3b3c5aa0555647861ad0 | 2ac8a76480903aea82c76a4dd7670c99c8f75dd86c14b0a31772ca2dea804ccd | `docs/research/second-packet/CANDIDATE_PACKET.md`; `docs/research/second-packet/DATASET_MANIFEST.md`; `docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md`; `tests/integration/test_archive_replay.py` |

## Boundary Notes

- Both rows are archive-only replay records.
- Holdout remains locked and unread.
- No OOS/performance, phase-gate, live-feed, broker/exchange, production, or
  capital-ready approval is created by this matrix.
- Duplicate packet rows or unresolved placeholder hashes invalidate the matrix.
