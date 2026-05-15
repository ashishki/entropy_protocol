"""Replay checks for archive-only research evidence packets."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from entropy.evidence.first_research_packet import (
    FirstResearchEvidencePacket,
    build_first_research_evidence_packet,
    deterministic_research_packet_json,
)
from entropy.models.registry import FillSide
from entropy.research import (
    ArchiveDatasetBinding,
    ArchiveEvaluationBar,
    FirstResearchCandidatePacket,
    bind_candidate_dataset_manifest,
    bind_candidate_evaluation_hashes,
    build_archive_dataset_manifest,
    build_first_research_candidate_packet,
    build_second_research_candidate_packet,
    run_archive_evaluation_harness,
)
from entropy.simbroker import CostModelConfig, FillSignal
from entropy.walkforward import CheckStatus, LeakageCheckResult, LeakageReport


class ArchivePacketReplayError(ValueError):
    """Raised when an archive packet replay does not match its stored contract."""


@dataclass(frozen=True)
class ArchivePacketReplaySpec:
    """Deterministic replay inputs for one archive-only research packet."""

    packet_name: str
    packet_id: str
    packet_doc_path: str
    manifest_doc_path: str
    candidate_factory: Callable[[], FirstResearchCandidatePacket]
    dataset_id: str
    dataset_path: str
    dataset_hash: str
    code_hash: str
    policy_hash: str
    parameter_hash: str
    symbol: str
    proposed_price: float
    high: float
    low: float
    stream_a_return: Decimal
    artifact_refs: tuple[str, ...]


@dataclass(frozen=True)
class ArchivePacketReplayResult:
    """Result of replaying one archive-only research evidence packet."""

    packet_name: str
    packet: FirstResearchEvidencePacket
    deterministic_json_hash: str
    packet_doc_path: str
    manifest_doc_path: str


FIRST_ARCHIVE_PACKET_REPLAY_SPEC = ArchivePacketReplaySpec(
    packet_name="first",
    packet_id="FIRST-RESEARCH-EVIDENCE-PACKET-001",
    packet_doc_path="docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md",
    manifest_doc_path="docs/research/first-packet/DATASET_MANIFEST.md",
    candidate_factory=build_first_research_candidate_packet,
    dataset_id="btc-archive-formation",
    dataset_path="archive/btc/formation.parquet",
    dataset_hash="d" * 64,
    code_hash="e" * 64,
    policy_hash="f" * 64,
    parameter_hash="1" * 64,
    symbol="BTC-USD",
    proposed_price=100.0,
    high=101.0,
    low=99.0,
    stream_a_return=Decimal("0.01"),
    artifact_refs=(
        "docs/research/first-packet/CANDIDATE_PACKET.md",
        "docs/research/first-packet/DATASET_MANIFEST.md",
        "src/entropy/research/evaluation.py",
        "tests/integration/test_first_research_packet.py::test_research_packet_contains_required_sections",
    ),
)
SECOND_ARCHIVE_PACKET_REPLAY_SPEC = ArchivePacketReplaySpec(
    packet_name="second",
    packet_id="SECOND-RESEARCH-EVIDENCE-PACKET-001",
    packet_doc_path="docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md",
    manifest_doc_path="docs/research/second-packet/DATASET_MANIFEST.md",
    candidate_factory=build_second_research_candidate_packet,
    dataset_id="eth-archive-formation",
    dataset_path="archive/eth/formation.parquet",
    dataset_hash="c" * 64,
    code_hash="2" * 64,
    policy_hash="3" * 64,
    parameter_hash="4" * 64,
    symbol="ETH-USD",
    proposed_price=200.0,
    high=202.0,
    low=198.0,
    stream_a_return=Decimal("0.012"),
    artifact_refs=(
        "docs/research/second-packet/CANDIDATE_PACKET.md",
        "docs/research/second-packet/DATASET_MANIFEST.md",
        "src/entropy/research/evaluation.py",
        "tests/integration/test_second_research_packet.py::test_second_research_packet_contains_required_sections",
    ),
)
ARCHIVE_PACKET_REPLAY_SPECS = (
    FIRST_ARCHIVE_PACKET_REPLAY_SPEC,
    SECOND_ARCHIVE_PACKET_REPLAY_SPEC,
)


def replay_archive_research_packets(
    *,
    project_root: Path | str,
    specs: Sequence[ArchivePacketReplaySpec] = ARCHIVE_PACKET_REPLAY_SPECS,
) -> tuple[ArchivePacketReplayResult, ...]:
    """Replay all configured archive-only research evidence packets."""
    return tuple(
        replay_archive_research_packet(project_root=project_root, spec=spec) for spec in specs
    )


def replay_archive_research_packet(
    *,
    project_root: Path | str,
    spec: ArchivePacketReplaySpec,
) -> ArchivePacketReplayResult:
    """Replay one archive-only research evidence packet from deterministic inputs."""
    root = Path(project_root)
    candidate = spec.candidate_factory()
    _require_file(root / spec.packet_doc_path, "packet artifact")
    _require_file(root / spec.manifest_doc_path, "dataset manifest")

    manifest = build_archive_dataset_manifest(
        candidate_id=candidate.candidate_id,
        dataset_bindings=(
            ArchiveDatasetBinding(
                dataset_id=spec.dataset_id,
                path=spec.dataset_path,
                dataset_hash=spec.dataset_hash,
                row_count=30,
                role="formation",
            ),
        ),
        formation_scope="archive fixture formation rows only",
        evaluation_scope="archive fixture evaluation rows only",
    )
    candidate = bind_candidate_dataset_manifest(candidate, manifest)
    candidate = bind_candidate_evaluation_hashes(
        candidate,
        code_hash=spec.code_hash,
        policy_hash=spec.policy_hash,
        parameter_hash=spec.parameter_hash,
    )
    evaluation = run_archive_evaluation_harness(
        packet=candidate,
        manifest=manifest,
        leakage_report=_passing_leakage_report(),
        fill_signal=FillSignal(
            symbol=spec.symbol,
            side=FillSide.BUY,
            quantity=1.0,
            proposed_price=spec.proposed_price,
        ),
        fill_bar=ArchiveEvaluationBar(
            timestamp=datetime(2026, 5, 7, 12, 0, tzinfo=timezone.utc),
            high=spec.high,
            low=spec.low,
        ),
        cost_config=CostModelConfig(pct_commission=0.001, slippage_linear=0.0005),
        stream_a_return=spec.stream_a_return,
    )
    packet = build_first_research_evidence_packet(
        candidate=candidate,
        manifest=manifest,
        evaluation=evaluation,
        artifact_refs=spec.artifact_refs,
        project_root=root,
        packet_id=spec.packet_id,
    )
    _verify_replay_document_contract(
        packet=packet,
        packet_doc=(root / spec.packet_doc_path).read_text(encoding="utf-8"),
        manifest_doc=(root / spec.manifest_doc_path).read_text(encoding="utf-8"),
        artifact_refs=spec.artifact_refs,
    )
    deterministic_json = deterministic_research_packet_json(packet)
    return ArchivePacketReplayResult(
        packet_name=spec.packet_name,
        packet=packet,
        deterministic_json_hash=_sha256_text(deterministic_json),
        packet_doc_path=spec.packet_doc_path,
        manifest_doc_path=spec.manifest_doc_path,
    )


def _verify_replay_document_contract(
    *,
    packet: FirstResearchEvidencePacket,
    packet_doc: str,
    manifest_doc: str,
    artifact_refs: Sequence[str],
) -> None:
    _require_fragments(
        packet_doc,
        (
            "Status: ARCHIVE_ONLY_NO_CLAIM",
            f"Packet id: {packet.packet_id}",
            f"Candidate id: {packet.candidate_id}",
        ),
        "packet artifact",
    )
    _require_fragments(
        manifest_doc,
        (
            "Status: ARCHIVE_ONLY_NO_HOLDOUT",
            f"Candidate id: {packet.candidate_id}",
            "Holdout remains locked",
            "No holdout path is listed",
        ),
        "dataset manifest",
    )
    _require_fragments(packet_doc, packet.no_claim_labels, "packet artifact")
    _require_fragments(
        packet_doc,
        (f"`{artifact_ref}`" for artifact_ref in artifact_refs),
        "packet artifact",
    )

    blocked_approvals = (
        packet.holdout_unlock,
        packet.oos_performance_approval,
        packet.phase_gate_approval,
        packet.production_approval,
        packet.capital_ready_approval,
        packet.live_feed_approval,
        packet.broker_exchange_approval,
    )
    if any(blocked_approvals):
        raise ArchivePacketReplayError("Replay packet opened a restricted approval surface")


def _require_file(path: Path, artifact_name: str) -> None:
    if not path.is_file():
        raise ArchivePacketReplayError(f"Missing {artifact_name}: {path}")


def _require_fragments(text: str, fragments: Iterable[str], artifact_name: str) -> None:
    missing = tuple(fragment for fragment in fragments if fragment not in text)
    if missing:
        raise ArchivePacketReplayError(
            f"Missing {artifact_name} replay fragment: " + ", ".join(missing)
        )


def _passing_leakage_report() -> LeakageReport:
    passing = LeakageCheckResult(status=CheckStatus.PASS, description="archive fixture check")
    return LeakageReport(
        normalization_leakage=passing,
        regime_label_lookahead=passing,
        universe_selection_bias=passing,
        within_window_optimization=passing,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


__all__ = [
    "ARCHIVE_PACKET_REPLAY_SPECS",
    "FIRST_ARCHIVE_PACKET_REPLAY_SPEC",
    "SECOND_ARCHIVE_PACKET_REPLAY_SPEC",
    "ArchivePacketReplayError",
    "ArchivePacketReplayResult",
    "ArchivePacketReplaySpec",
    "replay_archive_research_packet",
    "replay_archive_research_packets",
]
