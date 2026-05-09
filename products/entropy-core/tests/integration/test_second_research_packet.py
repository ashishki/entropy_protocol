"""Second research packet integration contract tests."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal

import pytest
import polars as pl
from pydantic import ValidationError

from entropy.evidence import (
    FIRST_RESEARCH_EVIDENCE_PACKET_SCHEMA_VERSION,
    FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS,
    EvidenceCollectionError,
    FirstResearchEvidencePacketError,
    build_first_research_evidence_packet,
    deterministic_research_packet_json,
)
from entropy.research import (
    ARCHIVE_DATASET_MANIFEST_SCHEMA_VERSION,
    ARCHIVE_EVALUATION_NO_CLAIM_LABELS,
    ARCHIVE_EVALUATION_SCHEMA_VERSION,
    FIRST_RESEARCH_CANDIDATE_SCHEMA_VERSION,
    FIRST_RESEARCH_NO_CLAIM_LABELS,
    REQUIRED_HASH_PLACEHOLDERS,
    ArchiveDatasetBinding,
    ArchiveEvaluationBar,
    ArchiveEvaluationError,
    CandidateSurfaceError,
    DatasetManifestError,
    FirstResearchCandidatePacket,
    bind_candidate_dataset_manifest,
    bind_candidate_evaluation_hashes,
    build_archive_dataset_manifest,
    build_first_research_candidate_packet,
    build_second_research_candidate_packet,
    deterministic_candidate_json,
    deterministic_evaluation_json,
    deterministic_manifest_json,
    run_archive_evaluation_harness,
    validate_candidate_requested_surfaces,
)
from entropy.hashing import compute_dataset_hash
from entropy.models.registry import FillSide
from entropy.simbroker import CostModelConfig, FillSignal
from entropy.walkforward import CheckStatus, LeakageCheckResult, LeakageReport

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SECOND_CANDIDATE_DOC = PROJECT_ROOT / "docs" / "research" / "second-packet" / "CANDIDATE_PACKET.md"
SECOND_DATASET_MANIFEST_DOC = (
    PROJECT_ROOT / "docs" / "research" / "second-packet" / "DATASET_MANIFEST.md"
)
SECOND_RESEARCH_EVIDENCE_PACKET_DOC = (
    PROJECT_ROOT / "docs" / "research" / "second-packet" / "RESEARCH_EVIDENCE_PACKET.md"
)


def test_second_candidate_packet_records_registration_requirements() -> None:
    first = build_first_research_candidate_packet()
    packet = build_second_research_candidate_packet()
    document = SECOND_CANDIDATE_DOC.read_text(encoding="utf-8")

    assert packet.schema_version == FIRST_RESEARCH_CANDIDATE_SCHEMA_VERSION
    assert packet.candidate_id == "SRC-001-STRUCTURE-RETEST-BOUNCE"
    assert packet.candidate_id in document
    assert packet.hypothesis_text in document
    assert packet.hypothesis_family == "Structure Levels"
    assert packet.hypothesis_family != first.hypothesis_family
    assert packet.hypothesis_family in document
    assert packet.scope in document
    assert len(packet.frozen_parameters) >= 1
    assert packet.required_human_registration_gate == "human_registration_required"
    assert "Status: CANDIDATE_ONLY_NOT_REGISTERED" in document
    for label in FIRST_RESEARCH_NO_CLAIM_LABELS:
        assert label in packet.no_claim_labels
        assert label in document


def test_second_candidate_packet_serializes_deterministically() -> None:
    packet = build_second_research_candidate_packet()

    assert deterministic_candidate_json(packet) == deterministic_candidate_json(packet)
    assert deterministic_candidate_json(packet).startswith('{"baseline_comparator"')
    for hash_name in REQUIRED_HASH_PLACEHOLDERS:
        placeholder = getattr(packet.hash_placeholders, hash_name)
        assert placeholder.startswith("PENDING_")
        assert hash_name in deterministic_candidate_json(packet)
        assert f"- {hash_name}: {placeholder}" in packet.to_markdown()
    assert packet.to_markdown().replace("First Research", "Second Research") == (
        SECOND_CANDIDATE_DOC.read_text(encoding="utf-8")
    )


@pytest.mark.parametrize(
    "requested_surface",
    [
        "holdout_read",
        "oos_performance_label",
        "performance_conclusion",
        "production_label",
        "capital_ready_label",
        "live_feed",
        "live_broker_api",
        "broker_exchange_integration",
        "exchange_api_client",
    ],
)
def test_second_candidate_packet_rejects_claim_and_live_surfaces(
    requested_surface: str,
) -> None:
    base = build_second_research_candidate_packet()

    with pytest.raises(ValidationError, match="Forbidden first research candidate surface"):
        FirstResearchCandidatePacket(
            **{
                **base.model_dump(mode="python"),
                "requested_surfaces": (requested_surface,),
            }
        )
    with pytest.raises(CandidateSurfaceError, match="Forbidden first research candidate surface"):
        validate_candidate_requested_surfaces((requested_surface,))

    FirstResearchCandidatePacket(
        **{
            **base.model_dump(mode="python"),
            "requested_surfaces": ("archive_local_fixture",),
        }
    )


def test_second_archive_dataset_manifest_hash_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first.parquet"
    second = tmp_path / "second.parquet"
    pl.DataFrame(
        {
            "timestamp": ["2026-02-02T00:00:00Z", "2026-02-01T00:00:00Z"],
            "symbol": ["ETH-USD", "ETH-USD"],
            "close": [201.0, 200.0],
        }
    ).write_parquet(first)
    pl.DataFrame(
        {
            "close": [200.0, 201.0],
            "symbol": ["ETH-USD", "ETH-USD"],
            "timestamp": ["2026-02-01T00:00:00Z", "2026-02-02T00:00:00Z"],
        }
    ).write_parquet(second)
    first_hash = compute_dataset_hash(first)
    second_hash = compute_dataset_hash(second)
    assert first_hash == second_hash

    first_binding = ArchiveDatasetBinding(
        dataset_id="eth-archive-formation",
        path="archive/eth/formation.parquet",
        dataset_hash=first_hash,
        row_count=2,
        role="formation",
    )
    second_binding = ArchiveDatasetBinding(
        dataset_id="eth-archive-evaluation-probe",
        path="archive/eth/evaluation_probe.parquet",
        dataset_hash=second_hash,
        row_count=2,
        role="evaluation_probe",
    )

    manifest_a = build_archive_dataset_manifest(
        candidate_id=build_second_research_candidate_packet().candidate_id,
        dataset_bindings=(second_binding, first_binding),
        formation_scope="first 60 percent ETH archive fixture rows",
        evaluation_scope="remaining ETH archive fixture rows; no holdout",
    )
    manifest_b = build_archive_dataset_manifest(
        candidate_id=build_second_research_candidate_packet().candidate_id,
        dataset_bindings=(first_binding, second_binding),
        formation_scope="first 60 percent ETH archive fixture rows",
        evaluation_scope="remaining ETH archive fixture rows; no holdout",
    )

    assert manifest_a.aggregate_dataset_hash == manifest_b.aggregate_dataset_hash
    assert manifest_a.manifest_hash == manifest_b.manifest_hash
    assert deterministic_manifest_json(manifest_a) == deterministic_manifest_json(manifest_b)
    assert manifest_a.schema_version == ARCHIVE_DATASET_MANIFEST_SCHEMA_VERSION


def test_second_archive_dataset_manifest_excludes_holdout() -> None:
    document = SECOND_DATASET_MANIFEST_DOC.read_text(encoding="utf-8")
    binding = ArchiveDatasetBinding(
        dataset_id="eth-archive-formation",
        path="archive/eth/formation.parquet",
        dataset_hash="a" * 64,
        row_count=30,
        role="formation",
    )
    manifest = build_archive_dataset_manifest(
        candidate_id=build_second_research_candidate_packet().candidate_id,
        dataset_bindings=(binding,),
        formation_scope="archive fixture formation rows only",
        evaluation_scope="archive fixture evaluation rows only",
    )

    assert manifest.holdout_exclusion == "holdout_locked_not_read"
    assert manifest.holdout_paths == ()
    assert "Status: ARCHIVE_ONLY_NO_HOLDOUT" in document
    assert "Holdout remains locked" in document
    assert "No holdout path is listed" in document

    with pytest.raises(DatasetManifestError, match="Holdout paths must be excluded"):
        build_archive_dataset_manifest(
            candidate_id=manifest.candidate_id,
            dataset_bindings=(binding,),
            formation_scope=manifest.formation_scope,
            evaluation_scope=manifest.evaluation_scope,
            holdout_paths=("holdout/eth.parquet",),
        )
    with pytest.raises(ValidationError, match="Holdout path is forbidden"):
        ArchiveDatasetBinding(
            dataset_id="eth-holdout",
            path="archive/eth_holdout.parquet",
            dataset_hash="b" * 64,
            row_count=30,
            role="evaluation_probe",
        )


def test_second_dataset_binding_preserves_registered_candidate_fields() -> None:
    packet = build_second_research_candidate_packet()
    manifest = build_archive_dataset_manifest(
        candidate_id=packet.candidate_id,
        dataset_bindings=(
            ArchiveDatasetBinding(
                dataset_id="eth-archive-formation",
                path="archive/eth/formation.parquet",
                dataset_hash="c" * 64,
                row_count=30,
                role="formation",
            ),
        ),
        formation_scope="archive fixture formation rows only",
        evaluation_scope="archive fixture evaluation rows only",
    )

    bound_packet = bind_candidate_dataset_manifest(packet, manifest)

    assert bound_packet.hypothesis_text == packet.hypothesis_text
    assert bound_packet.hypothesis_family == packet.hypothesis_family
    assert bound_packet.frozen_parameters == packet.frozen_parameters
    assert bound_packet.hash_placeholders.dataset_hash == manifest.aggregate_dataset_hash
    assert bound_packet.hash_placeholders.code_hash == packet.hash_placeholders.code_hash
    assert bound_packet.hash_placeholders.policy_hash == packet.hash_placeholders.policy_hash
    assert bound_packet.hash_placeholders.parameter_hash == packet.hash_placeholders.parameter_hash


def test_second_archive_evaluation_requires_all_hash_bindings() -> None:
    packet = build_second_research_candidate_packet()
    manifest = _second_manifest(packet.candidate_id)
    dataset_bound_packet = bind_candidate_dataset_manifest(packet, manifest)

    with pytest.raises(ArchiveEvaluationError, match="code_hash must be bound"):
        run_archive_evaluation_harness(
            packet=dataset_bound_packet,
            manifest=manifest,
            leakage_report=_passing_leakage_report(),
            fill_signal=_fill_signal(),
            fill_bar=_fill_bar(),
            cost_config=CostModelConfig(pct_commission=0.001),
            stream_a_return=Decimal("0.012"),
        )

    fully_bound_packet = bind_candidate_evaluation_hashes(
        dataset_bound_packet,
        code_hash="2" * 64,
        policy_hash="3" * 64,
        parameter_hash="4" * 64,
    )
    result = run_archive_evaluation_harness(
        packet=fully_bound_packet,
        manifest=manifest,
        leakage_report=_passing_leakage_report(),
        fill_signal=_fill_signal(),
        fill_bar=_fill_bar(),
        cost_config=CostModelConfig(pct_commission=0.001),
        stream_a_return=Decimal("0.012"),
    )

    assert result.schema_version == ARCHIVE_EVALUATION_SCHEMA_VERSION
    assert result.dataset_hash == manifest.aggregate_dataset_hash
    assert result.code_hash == "2" * 64
    assert result.policy_hash == "3" * 64
    assert result.parameter_hash == "4" * 64


def test_second_archive_evaluation_outputs_required_evidence_surfaces() -> None:
    result = _second_archive_evaluation_result()

    assert result.leakage_status == "PASS"
    assert result.leakage_check_ids == ()
    assert result.fill_log_ids[0].startswith("fill-log-")
    assert result.simbroker_version == "simbroker-reset-v1"
    for stream_key in ("stream_a", "stream_b", "stream_c", "stream_d"):
        assert stream_key in result.attribution_payload
        assert isinstance(result.attribution_payload[stream_key], list)
    assert result.attribution_payload["archive_only"] is True


def test_second_archive_evaluation_output_remains_no_claim() -> None:
    result = _second_archive_evaluation_result()
    payload = deterministic_evaluation_json(result)

    for label in ARCHIVE_EVALUATION_NO_CLAIM_LABELS:
        assert label in result.no_claim_labels
        assert label in payload
    assert result.performance_conclusion_status == "not_computed_no_performance_conclusion"
    assert result.holdout_used is False
    assert result.oos_label is False
    assert result.phase_gate_evidence is False
    assert result.production_label is False
    assert result.capital_ready_label is False
    assert 'performance_conclusion":true' not in payload


def test_second_research_packet_contains_required_sections() -> None:
    candidate, manifest, evaluation = _second_archive_evaluation_inputs()
    packet = build_first_research_evidence_packet(
        candidate=candidate,
        manifest=manifest,
        evaluation=evaluation,
        artifact_refs=_second_research_packet_artifact_refs(),
        project_root=PROJECT_ROOT,
        packet_id="SECOND-RESEARCH-EVIDENCE-PACKET-001",
    )
    markdown = packet.to_markdown()
    document = SECOND_RESEARCH_EVIDENCE_PACKET_DOC.read_text(encoding="utf-8")

    assert packet.schema_version == FIRST_RESEARCH_EVIDENCE_PACKET_SCHEMA_VERSION
    assert packet.packet_id == "SECOND-RESEARCH-EVIDENCE-PACKET-001"
    assert packet.candidate_id == candidate.candidate_id
    assert packet.dataset_hash == evaluation.dataset_hash
    assert packet.code_hash == evaluation.code_hash
    assert packet.policy_hash == evaluation.policy_hash
    assert packet.parameter_hash == evaluation.parameter_hash
    assert packet.leakage_status == evaluation.leakage_status
    assert packet.simbroker_fill_log_ids == evaluation.fill_log_ids
    for stream_key in ("stream_a", "stream_b", "stream_c", "stream_d"):
        assert stream_key in packet.attribution_streams
        assert f"- {stream_key}:" in markdown
    for label in FIRST_RESEARCH_PACKET_NO_CLAIM_LABELS:
        assert label in packet.no_claim_labels
        assert label in markdown
        assert label in document
    assert "Status: ARCHIVE_ONLY_NO_CLAIM" in document


def test_second_research_packet_fails_missing_artifact_or_hash() -> None:
    candidate, manifest, evaluation = _second_archive_evaluation_inputs()

    with pytest.raises(EvidenceCollectionError, match="Missing evidence artifact"):
        build_first_research_evidence_packet(
            candidate=candidate,
            manifest=manifest,
            evaluation=evaluation,
            artifact_refs=("docs/research/second-packet/MISSING.md",),
            project_root=PROJECT_ROOT,
            packet_id="SECOND-RESEARCH-EVIDENCE-PACKET-001",
        )

    broken_evaluation = evaluation.model_copy(update={"policy_hash": "PENDING_POLICY_HASH"})
    with pytest.raises(FirstResearchEvidencePacketError, match="policy_hash must be bound"):
        build_first_research_evidence_packet(
            candidate=candidate,
            manifest=manifest,
            evaluation=broken_evaluation,
            artifact_refs=("docs/research/second-packet/CANDIDATE_PACKET.md",),
            project_root=PROJECT_ROOT,
            packet_id="SECOND-RESEARCH-EVIDENCE-PACKET-001",
        )


def test_second_research_packet_blocks_claim_approvals() -> None:
    candidate, manifest, evaluation = _second_archive_evaluation_inputs()
    packet = build_first_research_evidence_packet(
        candidate=candidate,
        manifest=manifest,
        evaluation=evaluation,
        artifact_refs=_second_research_packet_artifact_refs(),
        project_root=PROJECT_ROOT,
        packet_id="SECOND-RESEARCH-EVIDENCE-PACKET-001",
    )
    payload = deterministic_research_packet_json(packet)

    assert packet.holdout_unlock is False
    assert packet.oos_performance_approval is False
    assert packet.phase_gate_approval is False
    assert packet.production_approval is False
    assert packet.capital_ready_approval is False
    assert packet.live_feed_approval is False
    assert packet.broker_exchange_approval is False
    assert "APPROVED" not in packet.to_markdown()
    assert 'oos_performance_approval":true' not in payload
    assert 'production_approval":true' not in payload
    assert 'capital_ready_approval":true' not in payload


def _second_archive_evaluation_result():
    _, _, evaluation = _second_archive_evaluation_inputs()
    return evaluation


def _second_archive_evaluation_inputs():
    packet = build_second_research_candidate_packet()
    manifest = _second_manifest(packet.candidate_id)
    packet = bind_candidate_dataset_manifest(packet, manifest)
    packet = bind_candidate_evaluation_hashes(
        packet,
        code_hash="2" * 64,
        policy_hash="3" * 64,
        parameter_hash="4" * 64,
    )
    evaluation = run_archive_evaluation_harness(
        packet=packet,
        manifest=manifest,
        leakage_report=_passing_leakage_report(),
        fill_signal=_fill_signal(),
        fill_bar=_fill_bar(),
        cost_config=CostModelConfig(pct_commission=0.001, slippage_linear=0.0005),
        stream_a_return=Decimal("0.012"),
    )
    return packet, manifest, evaluation


def _second_research_packet_artifact_refs() -> tuple[str, ...]:
    return (
        "docs/research/second-packet/CANDIDATE_PACKET.md",
        "docs/research/second-packet/DATASET_MANIFEST.md",
        "src/entropy/research/evaluation.py",
        "tests/integration/test_second_research_packet.py::test_second_research_packet_contains_required_sections",
    )


def _second_manifest(candidate_id: str):
    return build_archive_dataset_manifest(
        candidate_id=candidate_id,
        dataset_bindings=(
            ArchiveDatasetBinding(
                dataset_id="eth-archive-formation",
                path="archive/eth/formation.parquet",
                dataset_hash="c" * 64,
                row_count=30,
                role="formation",
            ),
        ),
        formation_scope="archive fixture formation rows only",
        evaluation_scope="archive fixture evaluation rows only",
    )


def _passing_leakage_report() -> LeakageReport:
    passing = LeakageCheckResult(status=CheckStatus.PASS, description="archive fixture check")
    return LeakageReport(
        normalization_leakage=passing,
        regime_label_lookahead=passing,
        universe_selection_bias=passing,
        within_window_optimization=passing,
    )


def _fill_signal() -> FillSignal:
    return FillSignal(
        symbol="ETH-USD",
        side=FillSide.BUY,
        quantity=1.0,
        proposed_price=200.0,
    )


def _fill_bar() -> ArchiveEvaluationBar:
    return ArchiveEvaluationBar(
        timestamp=datetime(2026, 5, 7, 12, 0, tzinfo=timezone.utc),
        high=202.0,
        low=198.0,
    )
