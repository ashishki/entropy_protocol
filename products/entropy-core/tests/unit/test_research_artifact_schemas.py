"""Unit tests for research artifact schemas."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    REQUIRED_RESEARCH_NO_CLAIM_LABELS,
    ResearchArtifact,
    research_artifact_from_archive_packet,
)
from entropy.evidence.first_research_packet import (
    FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS,
    FirstResearchEvidencePacket,
)


def test_research_artifacts_bind_required_hashes() -> None:
    artifact = research_artifact()
    contract = artifact.to_artifact_contract()

    assert artifact.candidate_id == "FRC-001"
    assert artifact.dataset_hash == "sha256:dataset"
    assert artifact.code_hash == "git:code"
    assert artifact.policy_hash == "sha256:policy"
    assert artifact.leakage_status == "PASS"
    assert set(REQUIRED_RESEARCH_NO_CLAIM_LABELS).issubset(artifact.no_claim_labels)
    assert contract.product == "entropy-core-research"
    assert contract.run_id == artifact.candidate_id
    assert contract.input_hashes == ("sha256:dataset",)
    assert contract.external_delivery_approval_status == "not_requested"

    with pytest.raises(ValidationError, match="dataset_hash must be bound"):
        research_artifact(dataset_hash="PENDING_DATASET_HASH")


def test_research_artifacts_reject_unsupported_claims() -> None:
    with pytest.raises(ValidationError, match="cannot claim OOS/performance"):
        research_artifact(no_claim_labels=(*REQUIRED_RESEARCH_NO_CLAIM_LABELS, "oos_performance"))

    with pytest.raises(ValidationError, match="cannot claim OOS/performance"):
        research_artifact(no_claim_labels=(*REQUIRED_RESEARCH_NO_CLAIM_LABELS, "production"))


def test_existing_archive_packets_map_to_no_claim_artifacts() -> None:
    packet = FirstResearchEvidencePacket(
        packet_id="FIRST-RESEARCH-EVIDENCE-PACKET-001",
        candidate_id="FRC-001",
        dataset_hash="sha256:dataset",
        code_hash="git:code",
        policy_hash="sha256:policy",
        parameter_hash="sha256:params",
        leakage_status="PASS",
        simbroker_fill_log_ids=("fill-log-001",),
        attribution_streams={
            "stream_a": {"status": "archive_only"},
            "stream_b": {"status": "archive_only"},
            "stream_c": {"status": "archive_only"},
            "stream_d": {"status": "archive_only"},
        },
        no_claim_labels=FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS,
        artifact_refs=("docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md",),
        evidence_packet_hash="sha256:evidence",
    )

    artifact = research_artifact_from_archive_packet(packet)
    contract = artifact.to_artifact_contract()

    assert artifact.artifact_kind == "report"
    assert artifact.candidate_id == packet.candidate_id
    assert artifact.no_claim_labels == ("archive_only_research", *packet.no_claim_labels)
    assert "not_oos_performance" in contract.no_claim_boundary
    assert contract.generated_artifact_refs == packet.artifact_refs


def research_artifact(**overrides: object) -> ResearchArtifact:
    payload: dict[str, object] = {
        "artifact_kind": "evaluation",
        "candidate_id": "FRC-001",
        "dataset_hash": "sha256:dataset",
        "code_hash": "git:code",
        "policy_hash": "sha256:policy",
        "leakage_status": "PASS",
        "no_claim_labels": REQUIRED_RESEARCH_NO_CLAIM_LABELS,
        "source_refs": ("docs/research/first-packet/DATASET_MANIFEST.md",),
        "generated_artifact_refs": ("docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md",),
        "limitations": ("archive-only no-claim representation",),
    }
    payload.update(overrides)
    return ResearchArtifact.model_validate(payload)
