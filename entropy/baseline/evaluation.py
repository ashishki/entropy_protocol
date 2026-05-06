"""Phase 1G evaluation configuration contract.

This module creates configuration and guard payloads only. It does not execute
evaluation, read holdout data, compute performance conclusions, or approve a
phase gate.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta

from entropy.baseline.registration import Phase1FPreRegistrationSurface
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_VALIDATION_LABEL,
)
from entropy.walkforward.runner import SIMBROKER_VERSION

PHASE1G_EVALUATION_CONFIG_CONTRACT_ID = "PHASE1G-EVALUATION-CONFIGURATION-CONTRACT-v1"
PHASE1G_EVALUATION_APPROVAL_GUARD_ID = "PHASE1G-EVALUATION-APPROVAL-GUARD-v1"

PHASE1G_REQUIRED_LEAKAGE_CHECKS: tuple[str, ...] = (
    "normalization_leakage",
    "regime_label_lookahead",
    "universe_selection_bias",
    "within_window_optimization",
)

PHASE1G_REQUIRED_STAT_FIELDS: tuple[str, ...] = (
    "net_sharpe_streams_abc_only",
    "stream_d_reported_separately",
    "sharpe_ci_method_id",
    "harvey_liu_family_method_id",
    "drawdown",
    "sample_count",
)

PHASE1G_NO_CLAIM_LABELS: tuple[str, ...] = (
    "configuration_only",
    "not_evaluation_execution",
    "not_holdout",
    "not_oos_claim",
    "not_performance_conclusion",
    "not_phase_gate_evidence",
    "not_capital_ready",
)


@dataclass(frozen=True)
class Phase1GEvaluationConfig:
    """Machine-readable governed evaluation configuration."""

    contract_id: str
    trial_id: str
    dataset_hash: str
    code_hash: str
    policy_hash: str
    parameter_lock_hash: str
    formation_start: datetime
    formation_end: datetime
    validation_start: datetime
    validation_end: datetime
    embargo_bars: int
    allowed_split_labels: tuple[str, ...]
    denied_split_labels: tuple[str, ...]
    leakage_checks_required: tuple[str, ...]
    simbroker_version: str
    simbroker_assumption: str
    stat_report_fields: tuple[str, ...]
    family_accounting: str
    required_human_gates: tuple[str, ...]
    no_claim_labels: tuple[str, ...]
    evaluation_execution_allowed: bool = False
    holdout_allowed: bool = False
    gate_claim_allowed: bool = False
    phase_gate_evidence: bool = False


@dataclass(frozen=True)
class Phase1GEvaluationRequest:
    """Request to validate against the Phase 1G evaluation contract."""

    split_label: str = PHASE1A_VALIDATION_LABEL
    purpose: str = "governed_archive_evaluation_config_check"
    evaluation_run_requested: bool = False
    approval_gate_id: str | None = None
    holdout_requested: bool = False
    live_feed_requested: bool = False
    broker_requested: bool = False
    performance_conclusion_requested: bool = False
    phase_gate_claim_requested: bool = False
    production_label_requested: bool = False
    capital_ready_label_requested: bool = False


@dataclass(frozen=True)
class Phase1GEvaluationDecision:
    """Allow/deny result for a Phase 1G evaluation request."""

    allowed: bool
    reason_code: str


def build_phase1g_evaluation_config(
    preregistration: Phase1FPreRegistrationSurface,
    *,
    formation_start: datetime,
    formation_end: datetime,
    validation_start: datetime,
    validation_end: datetime,
    embargo_bars: int,
    simbroker_version: str = SIMBROKER_VERSION,
) -> Phase1GEvaluationConfig:
    """Build a governed evaluation config without running evaluation."""
    _validate_preregistration(preregistration)
    _validate_windows(formation_start, formation_end, validation_start, validation_end)
    if embargo_bars < 0:
        raise ValueError("Phase 1G embargo_bars must be nonnegative")
    if not simbroker_version.strip():
        raise ValueError("Phase 1G simbroker_version must be nonblank")
    trial = preregistration.trial_spec
    return Phase1GEvaluationConfig(
        contract_id=PHASE1G_EVALUATION_CONFIG_CONTRACT_ID,
        trial_id=trial.trial_id,
        dataset_hash=trial.dataset_hash,
        code_hash=trial.code_hash,
        policy_hash=trial.policy_hash,
        parameter_lock_hash=preregistration.parameter_lock_hash,
        formation_start=formation_start,
        formation_end=formation_end,
        validation_start=validation_start,
        validation_end=validation_end,
        embargo_bars=embargo_bars,
        allowed_split_labels=(PHASE1A_FORMATION_LABEL, PHASE1A_VALIDATION_LABEL),
        denied_split_labels=(PHASE1A_HOLDOUT_LABEL,),
        leakage_checks_required=PHASE1G_REQUIRED_LEAKAGE_CHECKS,
        simbroker_version=simbroker_version,
        simbroker_assumption="registered_simbroker_version_no_live_broker",
        stat_report_fields=PHASE1G_REQUIRED_STAT_FIELDS,
        family_accounting="harvey_liu_family_tag_required",
        required_human_gates=(
            "phase1g_evaluation_run_approval",
            "holdout_unlock_approval",
            "phase_exit_approval",
        ),
        no_claim_labels=PHASE1G_NO_CLAIM_LABELS,
    )


def validate_phase1g_evaluation_request(
    config: Phase1GEvaluationConfig,
    request: Phase1GEvaluationRequest,
) -> Phase1GEvaluationDecision:
    """Validate an evaluation request without executing it."""
    if config.contract_id != PHASE1G_EVALUATION_CONFIG_CONTRACT_ID:
        return Phase1GEvaluationDecision(False, "CONFIG_CONTRACT_NOT_ALLOWED")
    if request.purpose != "governed_archive_evaluation_config_check":
        return Phase1GEvaluationDecision(False, "PURPOSE_NOT_ALLOWED")
    if request.split_label in config.denied_split_labels or request.holdout_requested:
        return Phase1GEvaluationDecision(False, "HOLDOUT_NOT_ALLOWED")
    if request.split_label not in config.allowed_split_labels:
        return Phase1GEvaluationDecision(False, "SPLIT_LABEL_NOT_ALLOWED")
    if request.live_feed_requested:
        return Phase1GEvaluationDecision(False, "LIVE_FEED_NOT_ALLOWED")
    if request.broker_requested:
        return Phase1GEvaluationDecision(False, "BROKER_NOT_ALLOWED")
    if request.performance_conclusion_requested:
        return Phase1GEvaluationDecision(False, "PERFORMANCE_CONCLUSION_NOT_ALLOWED")
    if request.phase_gate_claim_requested:
        return Phase1GEvaluationDecision(False, "PHASE_GATE_CLAIM_NOT_ALLOWED")
    if request.production_label_requested:
        return Phase1GEvaluationDecision(False, "PRODUCTION_LABEL_NOT_ALLOWED")
    if request.capital_ready_label_requested:
        return Phase1GEvaluationDecision(False, "CAPITAL_READY_LABEL_NOT_ALLOWED")
    if (
        request.evaluation_run_requested
        and request.approval_gate_id != "phase1g_evaluation_run_approval"
    ):
        return Phase1GEvaluationDecision(False, "EVALUATION_APPROVAL_REQUIRED")
    return Phase1GEvaluationDecision(True, "EVALUATION_CONFIG_REQUEST_ALLOWED")


def phase1g_evaluation_config_payload(config: Phase1GEvaluationConfig) -> dict[str, object]:
    """Return deterministic Phase 1G config payload."""
    return {
        "contract_id": config.contract_id,
        "trial_id": config.trial_id,
        "dataset_hash": config.dataset_hash,
        "code_hash": config.code_hash,
        "policy_hash": config.policy_hash,
        "parameter_lock_hash": config.parameter_lock_hash,
        "formation_start": config.formation_start.isoformat(),
        "formation_end": config.formation_end.isoformat(),
        "validation_start": config.validation_start.isoformat(),
        "validation_end": config.validation_end.isoformat(),
        "embargo_bars": config.embargo_bars,
        "allowed_split_labels": list(config.allowed_split_labels),
        "denied_split_labels": list(config.denied_split_labels),
        "leakage_checks_required": list(config.leakage_checks_required),
        "simbroker_version": config.simbroker_version,
        "simbroker_assumption": config.simbroker_assumption,
        "stat_report_fields": list(config.stat_report_fields),
        "family_accounting": config.family_accounting,
        "required_human_gates": list(config.required_human_gates),
        "no_claim_labels": list(config.no_claim_labels),
        "evaluation_execution_allowed": config.evaluation_execution_allowed,
        "holdout_allowed": config.holdout_allowed,
        "gate_claim_allowed": config.gate_claim_allowed,
        "phase_gate_evidence": config.phase_gate_evidence,
    }


def phase1g_evaluation_config_hash(config: Phase1GEvaluationConfig) -> str:
    """Hash the deterministic Phase 1G config payload."""
    canonical = json.dumps(
        phase1g_evaluation_config_payload(config),
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validate_preregistration(preregistration: Phase1FPreRegistrationSurface) -> None:
    if (
        preregistration.registry_write_allowed
        or preregistration.evaluation_allowed
        or preregistration.gate_claim_allowed
        or preregistration.phase_gate_evidence
    ):
        raise ValueError("Phase 1G requires no-claim preregistration state")


def _validate_windows(
    formation_start: datetime,
    formation_end: datetime,
    validation_start: datetime,
    validation_end: datetime,
) -> None:
    for name, value in (
        ("formation_start", formation_start),
        ("formation_end", formation_end),
        ("validation_start", validation_start),
        ("validation_end", validation_end),
    ):
        _require_utc(value, name)
    if formation_end <= formation_start:
        raise ValueError("Phase 1G formation_end must be after formation_start")
    if validation_start <= formation_end:
        raise ValueError("Phase 1G validation_start must be after formation_end")
    if validation_end <= validation_start:
        raise ValueError("Phase 1G validation_end must be after validation_start")


def _require_utc(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError(f"Phase 1G {name} must be timezone-aware UTC")
