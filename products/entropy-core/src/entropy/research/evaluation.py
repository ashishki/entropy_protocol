"""Archive-only evaluation harness for the first research packet."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from entropy.attribution import AttributionInput, archive_only_attribution_payload, compute_streams
from entropy.research.candidate import (
    CandidateHashPlaceholders,
    FirstResearchCandidatePacket,
)
from entropy.research.manifest import ArchiveDatasetManifest
from entropy.simbroker import CostModelConfig, FillSignal, process_fill
from entropy.walkforward import LeakageReport

ARCHIVE_EVALUATION_SCHEMA_VERSION = "archive-evaluation-harness/v1"
ARCHIVE_EVALUATION_NO_CLAIM_LABELS = (
    "archive_only_evaluation",
    "not_holdout_unlock",
    "not_oos_performance",
    "not_phase_gate_approval",
    "not_production",
    "not_capital_ready",
)
NO_PERFORMANCE_CONCLUSION_STATUS = "not_computed_no_performance_conclusion"


class ArchiveEvaluationError(ValueError):
    """Raised when the archive-only evaluation harness boundary is violated."""


class EvaluationBaseModel(BaseModel):
    """Base model for frozen deterministic evaluation schemas."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")


class ArchiveEvaluationBar(EvaluationBaseModel):
    """Minimal bar input consumed by SimBroker."""

    timestamp: datetime
    high: float = Field(gt=0.0)
    low: float = Field(gt=0.0)


class ArchiveEvaluationResult(EvaluationBaseModel):
    """Archive-only evaluation output with separated evidence surfaces."""

    schema_version: Literal["archive-evaluation-harness/v1"] = ARCHIVE_EVALUATION_SCHEMA_VERSION
    candidate_id: str
    dataset_hash: str
    code_hash: str
    policy_hash: str
    parameter_hash: str
    leakage_status: Literal["PASS", "FAIL"]
    leakage_check_ids: tuple[str, ...]
    simbroker_version: Literal["simbroker-reset-v1"] = "simbroker-reset-v1"
    fill_log_ids: tuple[str, ...] = Field(min_length=1)
    attribution_payload: dict[str, object]
    no_claim_labels: tuple[str, ...] = ARCHIVE_EVALUATION_NO_CLAIM_LABELS
    performance_conclusion_status: Literal["not_computed_no_performance_conclusion"] = (
        NO_PERFORMANCE_CONCLUSION_STATUS
    )
    holdout_used: bool = False
    oos_label: bool = False
    phase_gate_evidence: bool = False
    production_label: bool = False
    capital_ready_label: bool = False


def bind_candidate_evaluation_hashes(
    packet: FirstResearchCandidatePacket,
    *,
    code_hash: str,
    policy_hash: str,
    parameter_hash: str,
) -> FirstResearchCandidatePacket:
    """Bind code, policy, and parameter hashes without changing candidate prereg fields."""
    _require_bound_hash("code_hash", code_hash)
    _require_bound_hash("policy_hash", policy_hash)
    _require_bound_hash("parameter_hash", parameter_hash)
    hash_placeholders = CandidateHashPlaceholders(
        **{
            **packet.hash_placeholders.model_dump(mode="python"),
            "code_hash": code_hash,
            "policy_hash": policy_hash,
            "parameter_hash": parameter_hash,
        }
    )
    return packet.model_copy(update={"hash_placeholders": hash_placeholders})


def run_archive_evaluation_harness(
    *,
    packet: FirstResearchCandidatePacket,
    manifest: ArchiveDatasetManifest,
    leakage_report: LeakageReport,
    fill_signal: FillSignal,
    fill_bar: ArchiveEvaluationBar,
    cost_config: CostModelConfig,
    stream_a_return: Decimal,
    stream_b_return: Decimal = Decimal("0"),
    stream_d_return: Decimal = Decimal("0"),
) -> ArchiveEvaluationResult:
    """Run one deterministic archive-only evaluation step."""
    _validate_ready_hashes(packet, manifest)
    fill_log = process_fill(signal=fill_signal, bar=fill_bar, cost_config=cost_config)
    pnl_streams = compute_streams(
        (
            AttributionInput(
                fill_log=fill_log,
                stream_a_return=stream_a_return,
                stream_b_return=stream_b_return,
                stream_d_return=stream_d_return,
            ),
        )
    )
    return ArchiveEvaluationResult(
        candidate_id=packet.candidate_id,
        dataset_hash=packet.hash_placeholders.dataset_hash,
        code_hash=packet.hash_placeholders.code_hash,
        policy_hash=packet.hash_placeholders.policy_hash,
        parameter_hash=packet.hash_placeholders.parameter_hash,
        leakage_status=leakage_report.overall_status.value,
        leakage_check_ids=tuple(leakage_report.failing_check_ids),
        fill_log_ids=(_fill_log_id(fill_log.model_dump(mode="json")),),
        attribution_payload=archive_only_attribution_payload(pnl_streams),
    )


def deterministic_evaluation_json(result: ArchiveEvaluationResult) -> str:
    """Serialize archive evaluation output with stable key ordering."""
    return json.dumps(result.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))


def _validate_ready_hashes(
    packet: FirstResearchCandidatePacket,
    manifest: ArchiveDatasetManifest,
) -> None:
    if packet.candidate_id != manifest.candidate_id:
        raise ArchiveEvaluationError("Candidate id does not match dataset manifest")
    if packet.hash_placeholders.dataset_hash != manifest.aggregate_dataset_hash:
        raise ArchiveEvaluationError("Candidate dataset hash is not bound to manifest")
    _require_bound_hash("dataset_hash", packet.hash_placeholders.dataset_hash)
    _require_bound_hash("code_hash", packet.hash_placeholders.code_hash)
    _require_bound_hash("policy_hash", packet.hash_placeholders.policy_hash)
    _require_bound_hash("parameter_hash", packet.hash_placeholders.parameter_hash)


def _require_bound_hash(name: str, value: str) -> None:
    if not value.strip() or value.startswith("PENDING_"):
        raise ArchiveEvaluationError(f"{name} must be bound before archive evaluation")


def _fill_log_id(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return "fill-log-" + digest[:16]


__all__ = [
    "ARCHIVE_EVALUATION_NO_CLAIM_LABELS",
    "ARCHIVE_EVALUATION_SCHEMA_VERSION",
    "NO_PERFORMANCE_CONCLUSION_STATUS",
    "ArchiveEvaluationBar",
    "ArchiveEvaluationError",
    "ArchiveEvaluationResult",
    "bind_candidate_evaluation_hashes",
    "deterministic_evaluation_json",
    "run_archive_evaluation_harness",
]
