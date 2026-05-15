"""First archive-only research evidence packet."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from entropy.evidence.artifacts import EvidenceCollectionError
from entropy.research import (
    ARCHIVE_EVALUATION_NO_CLAIM_LABELS,
    ArchiveDatasetManifest,
    ArchiveEvaluationResult,
    FirstResearchCandidatePacket,
)

FIRST_RESEARCH_EVIDENCE_PACKET_SCHEMA_VERSION = "first-research-evidence-packet/v1"
FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS = (
    "archive_only_research_packet",
    "not_holdout_unlock",
    "not_oos_performance",
    "not_phase_gate_approval",
    "not_production",
    "not_capital_ready",
    "not_live_feed",
    "not_broker_exchange",
)


class FirstResearchEvidencePacketError(ValueError):
    """Raised when the first research evidence packet boundary is violated."""


class FirstResearchPacketBaseModel(BaseModel):
    """Base model for frozen deterministic research evidence packet schemas."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")


class FirstResearchEvidencePacket(FirstResearchPacketBaseModel):
    """Concrete archive-only packet for first research evidence."""

    schema_version: Literal["first-research-evidence-packet/v1"] = (
        FIRST_RESEARCH_EVIDENCE_PACKET_SCHEMA_VERSION
    )
    packet_id: str
    candidate_id: str
    dataset_hash: str
    code_hash: str
    policy_hash: str
    parameter_hash: str
    leakage_status: Literal["PASS", "FAIL"]
    simbroker_fill_log_ids: tuple[str, ...] = Field(min_length=1)
    attribution_streams: dict[str, object]
    no_claim_labels: tuple[str, ...] = FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS
    artifact_refs: tuple[str, ...] = Field(min_length=1)
    evidence_packet_hash: str
    holdout_unlock: bool = False
    oos_performance_approval: bool = False
    phase_gate_approval: bool = False
    production_approval: bool = False
    capital_ready_approval: bool = False
    live_feed_approval: bool = False
    broker_exchange_approval: bool = False

    def to_markdown(self) -> str:
        """Render the evidence packet as stable Markdown."""
        lines = [
            "# First Research Evidence Packet",
            "",
            "Status: ARCHIVE_ONLY_NO_CLAIM",
            f"Schema version: {self.schema_version}",
            f"Packet id: {self.packet_id}",
            f"Candidate id: {self.candidate_id}",
            f"Evidence packet hash: {self.evidence_packet_hash}",
            "",
            "## Hash Bindings",
            "",
            f"- dataset_hash: {self.dataset_hash}",
            f"- code_hash: {self.code_hash}",
            f"- policy_hash: {self.policy_hash}",
            f"- parameter_hash: {self.parameter_hash}",
            "",
            "## Evaluation Evidence",
            "",
            f"- leakage_status: {self.leakage_status}",
            "- simbroker_fill_log_ids: " + ", ".join(self.simbroker_fill_log_ids),
            "",
            "## Attribution Streams",
            "",
        ]
        for stream_key in ("stream_a", "stream_b", "stream_c", "stream_d"):
            lines.append(f"- {stream_key}: {self.attribution_streams.get(stream_key)}")
        lines.extend(
            [
                "",
                "## No-Claim Labels",
                "",
            ]
        )
        lines.extend(f"- {label}" for label in self.no_claim_labels)
        lines.extend(
            [
                "",
                "## Blocked Approvals",
                "",
                f"- holdout_unlock: {self.holdout_unlock}",
                f"- oos_performance_approval: {self.oos_performance_approval}",
                f"- phase_gate_approval: {self.phase_gate_approval}",
                f"- production_approval: {self.production_approval}",
                f"- capital_ready_approval: {self.capital_ready_approval}",
                f"- live_feed_approval: {self.live_feed_approval}",
                f"- broker_exchange_approval: {self.broker_exchange_approval}",
                "",
                "## Artifact References",
                "",
            ]
        )
        lines.extend(f"- `{artifact_ref}`" for artifact_ref in self.artifact_refs)
        lines.append("")
        return "\n".join(lines)


def build_first_research_evidence_packet(
    *,
    candidate: FirstResearchCandidatePacket,
    manifest: ArchiveDatasetManifest,
    evaluation: ArchiveEvaluationResult,
    artifact_refs: Sequence[str],
    project_root: Path | str,
    packet_id: str = "FIRST-RESEARCH-EVIDENCE-PACKET-001",
) -> FirstResearchEvidencePacket:
    """Build and verify the first archive-only research evidence packet."""
    _verify_artifacts(artifact_refs, project_root=Path(project_root))
    _verify_consistency(candidate=candidate, manifest=manifest, evaluation=evaluation)
    payload = {
        "schema_version": FIRST_RESEARCH_EVIDENCE_PACKET_SCHEMA_VERSION,
        "packet_id": packet_id,
        "candidate_id": evaluation.candidate_id,
        "dataset_hash": evaluation.dataset_hash,
        "code_hash": evaluation.code_hash,
        "policy_hash": evaluation.policy_hash,
        "parameter_hash": evaluation.parameter_hash,
        "leakage_status": evaluation.leakage_status,
        "simbroker_fill_log_ids": list(evaluation.fill_log_ids),
        "attribution_streams": _attribution_streams(evaluation),
        "no_claim_labels": list(FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS),
        "artifact_refs": sorted(artifact_refs),
        "holdout_unlock": False,
        "oos_performance_approval": False,
        "phase_gate_approval": False,
        "production_approval": False,
        "capital_ready_approval": False,
        "live_feed_approval": False,
        "broker_exchange_approval": False,
    }
    return FirstResearchEvidencePacket(
        **payload,
        evidence_packet_hash=_hash_payload(payload),
    )


def deterministic_research_packet_json(packet: FirstResearchEvidencePacket) -> str:
    """Serialize a research evidence packet with stable key ordering."""
    return json.dumps(packet.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))


def _verify_artifacts(artifact_refs: Sequence[str], *, project_root: Path) -> None:
    if not artifact_refs:
        raise EvidenceCollectionError("First research packet requires artifact references")
    for artifact_ref in artifact_refs:
        file_path, _, symbol_name = artifact_ref.partition("::")
        path = project_root / file_path
        if not path.is_file():
            raise EvidenceCollectionError("Missing evidence artifact: " + artifact_ref)
        if symbol_name and not path.read_text(encoding="utf-8").count(symbol_name):
            raise EvidenceCollectionError("Missing evidence symbol: " + artifact_ref)


def _verify_consistency(
    *,
    candidate: FirstResearchCandidatePacket,
    manifest: ArchiveDatasetManifest,
    evaluation: ArchiveEvaluationResult,
) -> None:
    if candidate.candidate_id != manifest.candidate_id:
        raise FirstResearchEvidencePacketError("Candidate id does not match manifest")
    if candidate.candidate_id != evaluation.candidate_id:
        raise FirstResearchEvidencePacketError("Candidate id does not match evaluation")
    if evaluation.dataset_hash != manifest.aggregate_dataset_hash:
        raise FirstResearchEvidencePacketError("Evaluation dataset hash does not match manifest")
    for name, value in (
        ("dataset_hash", evaluation.dataset_hash),
        ("code_hash", evaluation.code_hash),
        ("policy_hash", evaluation.policy_hash),
        ("parameter_hash", evaluation.parameter_hash),
    ):
        if not value.strip() or value.startswith("PENDING_"):
            raise FirstResearchEvidencePacketError(name + " must be bound")
    missing_labels = set(ARCHIVE_EVALUATION_NO_CLAIM_LABELS).difference(evaluation.no_claim_labels)
    if missing_labels:
        raise FirstResearchEvidencePacketError("Evaluation no-claim labels are incomplete")


def _attribution_streams(evaluation: ArchiveEvaluationResult) -> dict[str, object]:
    return {
        stream_key: evaluation.attribution_payload[stream_key]
        for stream_key in ("stream_a", "stream_b", "stream_c", "stream_d")
    }


def _hash_payload(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


__all__ = [
    "FIRST_RESEARCH_EVIDENCE_PACKET_SCHEMA_VERSION",
    "FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS",
    "FirstResearchEvidencePacket",
    "FirstResearchEvidencePacketError",
    "build_first_research_evidence_packet",
    "deterministic_research_packet_json",
]
