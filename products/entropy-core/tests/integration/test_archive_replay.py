"""Archive evidence packet replay contract tests."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from entropy.evidence import (
    ARCHIVE_PACKET_REPLAY_SPECS,
    ArchivePacketReplayError,
    EvidenceCollectionError,
    replay_archive_research_packet,
    replay_archive_research_packets,
)
from entropy.research import ArchiveEvaluationError

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_archive_packet_replay_is_deterministic() -> None:
    first_replay = replay_archive_research_packets(project_root=PROJECT_ROOT)
    second_replay = replay_archive_research_packets(project_root=PROJECT_ROOT)

    assert len(first_replay) == 2
    assert tuple(result.packet.packet_id for result in first_replay) == (
        "FIRST-RESEARCH-EVIDENCE-PACKET-001",
        "SECOND-RESEARCH-EVIDENCE-PACKET-001",
    )
    assert tuple(result.packet.evidence_packet_hash for result in first_replay) == tuple(
        result.packet.evidence_packet_hash for result in second_replay
    )
    assert tuple(result.deterministic_json_hash for result in first_replay) == tuple(
        result.deterministic_json_hash for result in second_replay
    )
    for result in first_replay:
        assert len(result.packet.evidence_packet_hash) == 64
        assert len(result.deterministic_json_hash) == 64


@pytest.mark.parametrize("spec", ARCHIVE_PACKET_REPLAY_SPECS)
def test_archive_packet_replay_requires_all_artifacts(spec) -> None:
    missing_packet = replace(spec, packet_doc_path="docs/research/missing-packet.md")
    with pytest.raises(ArchivePacketReplayError, match="Missing packet artifact"):
        replay_archive_research_packet(project_root=PROJECT_ROOT, spec=missing_packet)

    missing_manifest = replace(spec, manifest_doc_path="docs/research/missing-manifest.md")
    with pytest.raises(ArchivePacketReplayError, match="Missing dataset manifest"):
        replay_archive_research_packet(project_root=PROJECT_ROOT, spec=missing_manifest)

    missing_artifact_ref = replace(
        spec,
        artifact_refs=("docs/research/missing-artifact.md",),
    )
    with pytest.raises(EvidenceCollectionError, match="Missing evidence artifact"):
        replay_archive_research_packet(project_root=PROJECT_ROOT, spec=missing_artifact_ref)

    missing_hash = replace(spec, code_hash="PENDING_CODE_HASH")
    with pytest.raises(ArchiveEvaluationError, match="code_hash must be bound"):
        replay_archive_research_packet(project_root=PROJECT_ROOT, spec=missing_hash)


def test_archive_packet_replay_preserves_no_claim_boundary() -> None:
    results = replay_archive_research_packets(project_root=PROJECT_ROOT)

    for result in results:
        packet = result.packet
        payload = packet.to_markdown()
        assert packet.holdout_unlock is False
        assert packet.oos_performance_approval is False
        assert packet.phase_gate_approval is False
        assert packet.production_approval is False
        assert packet.capital_ready_approval is False
        assert packet.live_feed_approval is False
        assert packet.broker_exchange_approval is False
        assert "APPROVED" not in payload
        assert "not_holdout_unlock" in packet.no_claim_labels
        assert "not_oos_performance" in packet.no_claim_labels
        assert "not_live_feed" in packet.no_claim_labels
        assert "not_broker_exchange" in packet.no_claim_labels
