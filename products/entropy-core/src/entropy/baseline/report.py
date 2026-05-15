"""Phase 1I evaluation report packet assembly."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from entropy.baseline.evaluation import Phase1GEvaluationConfig, phase1g_evaluation_config_hash
from entropy.baseline.governed import Phase1HGovernedEvaluationResult
from entropy.baseline.registration import Phase1FPreRegistrationSurface

PHASE1I_EVALUATION_REPORT_ID = "PHASE1I-EVALUATION-REPORT-PACKET-v1"

PHASE1I_NO_CLAIM_LABELS: tuple[str, ...] = (
    "research_report_packet",
    "not_phase_gate_approval",
    "not_holdout_unlock",
    "not_production",
    "not_capital_ready",
)
PHASE1I_STAT_FIELD_STATUS = "not_computed_no_performance_conclusion"


@dataclass(frozen=True)
class Phase1IEvaluationReport:
    """Deterministic no-claim report packet for the first governed run."""

    report_id: str
    trial_id: str
    config_hash: str
    parameter_lock_hash: str
    run_id: str
    dataset_hash: str
    code_hash: str
    policy_hash: str
    leakage_status: str
    stat_fields: tuple[str, ...]
    stat_field_statuses: tuple[tuple[str, str], ...]
    no_claim_labels: tuple[str, ...]
    report_hash: str
    holdout_used: bool = False
    performance_conclusion: bool = False
    phase_gate_evidence: bool = False
    production_label: bool = False
    capital_ready_label: bool = False
    oos_label: bool = False


def build_phase1i_evaluation_report(
    config: Phase1GEvaluationConfig,
    preregistration: Phase1FPreRegistrationSurface,
    evaluation: Phase1HGovernedEvaluationResult,
) -> Phase1IEvaluationReport:
    """Assemble deterministic report metadata without approving claims."""
    if evaluation.run_record.trial_id != preregistration.trial_spec.trial_id:
        raise ValueError("Phase 1I report trial_id mismatch")
    if evaluation.run_record.dataset_hash != config.dataset_hash:
        raise ValueError("Phase 1I report dataset_hash mismatch")
    payload = _report_payload_without_hash(config, preregistration, evaluation)
    report_hash = _hash_payload(payload)
    return Phase1IEvaluationReport(
        report_id=PHASE1I_EVALUATION_REPORT_ID,
        trial_id=evaluation.run_record.trial_id,
        config_hash=phase1g_evaluation_config_hash(config),
        parameter_lock_hash=preregistration.parameter_lock_hash,
        run_id=evaluation.run_record.run_id,
        dataset_hash=evaluation.run_record.dataset_hash,
        code_hash=evaluation.run_record.code_hash,
        policy_hash=evaluation.run_record.policy_hash,
        leakage_status=evaluation.leakage_status.value,
        stat_fields=config.stat_report_fields,
        stat_field_statuses=_stat_field_statuses(config),
        no_claim_labels=PHASE1I_NO_CLAIM_LABELS,
        report_hash=report_hash,
    )


def phase1i_evaluation_report_payload(report: Phase1IEvaluationReport) -> dict[str, object]:
    """Return deterministic report payload."""
    return {
        "report_id": report.report_id,
        "trial_id": report.trial_id,
        "config_hash": report.config_hash,
        "parameter_lock_hash": report.parameter_lock_hash,
        "run_id": report.run_id,
        "dataset_hash": report.dataset_hash,
        "code_hash": report.code_hash,
        "policy_hash": report.policy_hash,
        "leakage_status": report.leakage_status,
        "stat_fields": list(report.stat_fields),
        "stat_field_statuses": [
            {"field": field, "status": status} for field, status in report.stat_field_statuses
        ],
        "no_claim_labels": list(report.no_claim_labels),
        "holdout_used": report.holdout_used,
        "performance_conclusion": report.performance_conclusion,
        "phase_gate_evidence": report.phase_gate_evidence,
        "production_label": report.production_label,
        "capital_ready_label": report.capital_ready_label,
        "oos_label": report.oos_label,
        "report_hash": report.report_hash,
    }


def _report_payload_without_hash(
    config: Phase1GEvaluationConfig,
    preregistration: Phase1FPreRegistrationSurface,
    evaluation: Phase1HGovernedEvaluationResult,
) -> dict[str, object]:
    return {
        "report_id": PHASE1I_EVALUATION_REPORT_ID,
        "trial_id": evaluation.run_record.trial_id,
        "config_hash": phase1g_evaluation_config_hash(config),
        "parameter_lock_hash": preregistration.parameter_lock_hash,
        "run_id": evaluation.run_record.run_id,
        "dataset_hash": evaluation.run_record.dataset_hash,
        "code_hash": evaluation.run_record.code_hash,
        "policy_hash": evaluation.run_record.policy_hash,
        "leakage_status": evaluation.leakage_status.value,
        "stat_fields": list(config.stat_report_fields),
        "stat_field_statuses": [
            {"field": field, "status": status} for field, status in _stat_field_statuses(config)
        ],
        "no_claim_labels": list(PHASE1I_NO_CLAIM_LABELS),
        "holdout_used": False,
        "performance_conclusion": False,
        "phase_gate_evidence": False,
        "production_label": False,
        "capital_ready_label": False,
        "oos_label": False,
    }


def _stat_field_statuses(
    config: Phase1GEvaluationConfig,
) -> tuple[tuple[str, str], ...]:
    return tuple((field, PHASE1I_STAT_FIELD_STATUS) for field in config.stat_report_fields)


def _hash_payload(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
