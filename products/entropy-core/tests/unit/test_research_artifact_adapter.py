"""Unit tests for archive research artifact adapters."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    archive_packet_to_artifact_payload,
    research_artifact_from_archive_packet,
    validate_artifact_payload,
)
from entropy.evidence.first_research_packet import (
    FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS,
    FirstResearchEvidencePacket,
)


def test_archive_packet_converts_to_artifact_payload() -> None:
    payload = archive_packet_to_artifact_payload(archive_packet())
    result = validate_artifact_payload(payload)

    assert result.ok is True
    assert result.artifact is not None
    assert payload["artifact_contract_version"] == "entropy-core-artifact/v1"
    assert payload["product"] == "entropy-core-research"
    assert payload["run_id"] == "FRC-001"
    assert payload["input_hashes"] == ["sha256:dataset", "sha256:evidence"]
    assert payload["external_delivery_approval_status"] == "not_requested"


def test_adapter_preserves_no_claim_boundaries() -> None:
    artifact = research_artifact_from_archive_packet(archive_packet())
    payload = artifact.to_artifact_contract().model_dump(mode="json")

    assert artifact.no_claim_labels == (
        "archive_only_research",
        *FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS,
    )
    assert payload["no_claim_boundary"] == list(artifact.no_claim_labels)
    assert "not_holdout_unlock" in payload["no_claim_boundary"]
    assert "not_oos_performance" in payload["no_claim_boundary"]
    assert "not_production" in payload["no_claim_boundary"]
    assert "not_capital_ready" in payload["no_claim_boundary"]


def test_adapter_rejects_unresolved_hashes() -> None:
    for field in ("dataset_hash", "code_hash", "policy_hash", "evidence_packet_hash"):
        packet = archive_packet(**{field: "PENDING_HASH"})
        with pytest.raises(ValidationError, match="must be bound"):
            archive_packet_to_artifact_payload(packet)


def archive_packet(**overrides: object) -> FirstResearchEvidencePacket:
    payload: dict[str, object] = {
        "packet_id": "FIRST-RESEARCH-EVIDENCE-PACKET-001",
        "candidate_id": "FRC-001",
        "dataset_hash": "sha256:dataset",
        "code_hash": "git:code",
        "policy_hash": "sha256:policy",
        "parameter_hash": "sha256:params",
        "leakage_status": "PASS",
        "simbroker_fill_log_ids": ("fill-log-001",),
        "attribution_streams": {
            "stream_a": {"status": "archive_only"},
            "stream_b": {"status": "archive_only"},
            "stream_c": {"status": "archive_only"},
            "stream_d": {"status": "archive_only"},
        },
        "no_claim_labels": FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS,
        "artifact_refs": ("docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md",),
        "evidence_packet_hash": "sha256:evidence",
    }
    payload.update(overrides)
    return FirstResearchEvidencePacket.model_validate(payload)
