"""Phase 1A archive baseline executable scaffold boundaries."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from entropy.evidence.phase1a_baseline import (
    PHASE1A_BASELINE_REGISTRATION_ID,
    Phase1APortfolioConstraints,
)
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_VALIDATION_LABEL,
    Phase1AReadAuthorization,
    Phase1AReadRequest,
    authorize_phase1a_archive_read,
)

PHASE1A_BASELINE_SCAFFOLD_ID = "PHASE1A-BASELINE-SCAFFOLD-v1"
PHASE1A_SCAFFOLD_WORKLOAD_BOUNDARY = "batch_table_oriented_no_per_row_strategy_loop"


@dataclass(frozen=True)
class Phase1ASkillFamilyPlaceholder:
    """Deterministic non-trading placeholder for one registered skill family."""

    family: str
    placeholder_id: str
    runtime_status: str = "placeholder_non_trading"
    interface: str = "batch_table_oriented"
    output_status: str = "no_signal_no_score_no_weight"


@dataclass(frozen=True)
class Phase1ABaselineScaffold:
    """Executable scaffold metadata for the registered Phase 1A baseline shape."""

    scaffold_id: str
    registration_id: str
    registration_instance_id: str
    spec_id: str
    baseline_spec_hash: str
    validation_registration_hash: str
    boundary_manifest_hash: str
    direction: str
    feature_scope: str
    portfolio_constraints: Phase1APortfolioConstraints
    skill_placeholders: tuple[Phase1ASkillFamilyPlaceholder, ...]
    workload_boundary: str = PHASE1A_SCAFFOLD_WORKLOAD_BOUNDARY
    gate_claim_allowed: bool = False
    archive_only: bool = True


@dataclass(frozen=True)
class Phase1AScaffoldPortfolioRequest:
    """Portfolio shape request checked by the scaffold constraints."""

    direction: str = "long_only"
    gross_exposure: float = 0.0
    short_exposure: float = 0.0
    leverage: str = "none"


@dataclass(frozen=True)
class Phase1AScaffoldConstraintDecision:
    """Constraint decision for a Phase 1A scaffold portfolio request."""

    allowed: bool
    reason_code: str


def load_phase1a_baseline_scaffold(
    *,
    registration_manifest_path: Path | str,
) -> Phase1ABaselineScaffold:
    """Load the registered Phase 1A baseline shape as an executable scaffold."""
    payload = _read_json_object(Path(registration_manifest_path))
    _validate_registration_manifest(payload)

    baseline_spec = _required_dict(payload, "baseline_spec")
    constraints_payload = _required_dict(baseline_spec, "portfolio_constraints")
    constraints = Phase1APortfolioConstraints(
        direction=_required_str(constraints_payload, "direction"),
        gross_min=_required_float(constraints_payload, "gross_min"),
        gross_max=_required_float(constraints_payload, "gross_max"),
        short_exposure=_required_float(constraints_payload, "short_exposure"),
        leverage=_required_str(constraints_payload, "leverage"),
        rebalance_policy=_required_str(constraints_payload, "rebalance_policy"),
        treasury_stream=_required_str(constraints_payload, "treasury_stream"),
    )
    skill_families = _required_str_sequence(baseline_spec, "skill_families")
    placeholders = tuple(
        Phase1ASkillFamilyPlaceholder(
            family=family,
            placeholder_id=f"P1A-SKILL-{index:02d}-{family}",
        )
        for index, family in enumerate(skill_families, start=1)
    )
    return Phase1ABaselineScaffold(
        scaffold_id=PHASE1A_BASELINE_SCAFFOLD_ID,
        registration_id=_required_str(payload, "registration_id"),
        registration_instance_id=_required_str(payload, "registration_instance_id"),
        spec_id=_required_str(baseline_spec, "spec_id"),
        baseline_spec_hash=_required_str(payload, "baseline_spec_hash"),
        validation_registration_hash=_required_str(payload, "validation_registration_hash"),
        boundary_manifest_hash=_required_str(payload, "boundary_manifest_hash"),
        direction=_required_str(baseline_spec, "direction"),
        feature_scope=_required_str(baseline_spec, "feature_scope"),
        portfolio_constraints=constraints,
        skill_placeholders=placeholders,
    )


def validate_phase1a_scaffold_constraints(
    scaffold: Phase1ABaselineScaffold,
    request: Phase1AScaffoldPortfolioRequest,
) -> Phase1AScaffoldConstraintDecision:
    """Validate long-only/no-leverage scaffold constraints without allocation."""
    constraints = scaffold.portfolio_constraints
    if request.direction != "long_only" or constraints.direction != "long_only":
        return Phase1AScaffoldConstraintDecision(False, "DIRECTION_NOT_LONG_ONLY")
    if request.gross_exposure < constraints.gross_min:
        return Phase1AScaffoldConstraintDecision(False, "GROSS_EXPOSURE_BELOW_MIN")
    if request.gross_exposure > constraints.gross_max:
        return Phase1AScaffoldConstraintDecision(False, "GROSS_EXPOSURE_ABOVE_MAX")
    if request.short_exposure != 0.0 or constraints.short_exposure != 0.0:
        return Phase1AScaffoldConstraintDecision(False, "SHORT_EXPOSURE_NOT_ALLOWED")
    if request.leverage != "none" or constraints.leverage != "none":
        return Phase1AScaffoldConstraintDecision(False, "LEVERAGE_NOT_ALLOWED")
    return Phase1AScaffoldConstraintDecision(True, "CONSTRAINTS_ALLOWED")


def authorize_phase1a_scaffold_read(
    *,
    scaffold: Phase1ABaselineScaffold,
    boundary_manifest_path: Path | str,
    symbol: str,
    split_label: str,
) -> Phase1AReadAuthorization:
    """Authorize scaffold archive access without loading market data."""
    if split_label == PHASE1A_FORMATION_LABEL:
        request = Phase1AReadRequest(
            symbol=symbol,
            split_label=split_label,
            read_purpose="instrumentation",
        )
    elif split_label == PHASE1A_VALIDATION_LABEL:
        request = Phase1AReadRequest(
            symbol=symbol,
            split_label=split_label,
            read_purpose="registered_validation",
            baseline_registration_id=scaffold.registration_instance_id,
            baseline_spec_hash=scaffold.baseline_spec_hash,
            validation_registration_hash=scaffold.validation_registration_hash,
        )
    elif split_label == PHASE1A_HOLDOUT_LABEL:
        request = Phase1AReadRequest(
            symbol=symbol,
            split_label=split_label,
            read_purpose="final_holdout_audit",
            baseline_registration_id=scaffold.registration_instance_id,
            baseline_spec_hash=scaffold.baseline_spec_hash,
            validation_registration_hash=scaffold.validation_registration_hash,
        )
    else:
        request = Phase1AReadRequest(
            symbol=symbol,
            split_label=split_label,
            read_purpose="instrumentation",
        )
    return authorize_phase1a_archive_read(
        boundary_manifest_path=boundary_manifest_path,
        request=request,
    )


def _read_json_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _validate_registration_manifest(payload: dict[str, object]) -> None:
    expected = {
        "registration_id": PHASE1A_BASELINE_REGISTRATION_ID,
        "archive_only": True,
        "gate_claim_allowed": False,
        "boundary": "baseline_spec_registration_no_strategy_no_portfolio_no_performance_claim",
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(f"baseline scaffold manifest has invalid {key}")

    baseline_spec = _required_dict(payload, "baseline_spec")
    if baseline_spec.get("signal_runtime_status") != "not_implemented":
        raise ValueError("baseline scaffold must not load executable signal logic")
    if baseline_spec.get("direction") != "long_only":
        raise ValueError("baseline scaffold direction must be long_only")
    if baseline_spec.get("feature_scope") != "ohlcv_1d_archive_derived_only":
        raise ValueError("baseline scaffold feature scope must remain archive OHLCV 1d")
    if baseline_spec.get("boundary") != "baseline_spec_registration_no_executable_strategy":
        raise ValueError("baseline scaffold spec boundary is invalid")
    if baseline_spec.get("archive_only") is not True:
        raise ValueError("baseline scaffold spec must be archive_only")
    if baseline_spec.get("gate_claim_allowed") is not False:
        raise ValueError("baseline scaffold spec must not allow gate claims")

    constraints = _required_dict(baseline_spec, "portfolio_constraints")
    if _required_str(constraints, "direction") != "long_only":
        raise ValueError("baseline scaffold portfolio direction must be long_only")
    if _required_float(constraints, "gross_min") != 0.0:
        raise ValueError("baseline scaffold gross_min must be 0.0")
    if _required_float(constraints, "gross_max") != 1.0:
        raise ValueError("baseline scaffold gross_max must be 1.0")
    if _required_float(constraints, "short_exposure") != 0.0:
        raise ValueError("baseline scaffold short exposure must be 0.0")
    if _required_str(constraints, "leverage") != "none":
        raise ValueError("baseline scaffold leverage must be none")

    skill_families = _required_str_sequence(baseline_spec, "skill_families")
    if len(skill_families) != 6 or len(set(skill_families)) != len(skill_families):
        raise ValueError("baseline scaffold requires six unique skill families")
    if PHASE1A_HOLDOUT_LABEL not in _required_str_sequence(baseline_spec, "forbidden_split_labels"):
        raise ValueError("baseline scaffold must forbid holdout split")
    if PHASE1A_HOLDOUT_LABEL in _required_str_sequence(baseline_spec, "allowed_split_labels"):
        raise ValueError("baseline scaffold must not allow holdout split")

    baseline_spec_hash = _required_str(payload, "baseline_spec_hash")
    if _hash_payload(baseline_spec) != baseline_spec_hash:
        raise ValueError("baseline scaffold spec hash mismatch")
    validation_registration_hash = _required_str(payload, "validation_registration_hash")
    expected_validation_hash = _hash_payload(
        {
            "registration_instance_id": _required_str(payload, "registration_instance_id"),
            "baseline_spec_hash": baseline_spec_hash,
            "boundary_manifest_hash": _required_str(payload, "boundary_manifest_hash"),
            "validation_split_label": PHASE1A_VALIDATION_LABEL,
            "validation_read_purpose": "registered_validation",
        }
    )
    if validation_registration_hash != expected_validation_hash:
        raise ValueError("baseline scaffold validation registration hash mismatch")

    holdout_access = _required_dict(payload, "holdout_access")
    if holdout_access.get("access") != "locked":
        raise ValueError("baseline scaffold holdout access must remain locked")


def _required_dict(payload: dict[str, object], key: str) -> dict[str, object]:
    value = payload[key]
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def _required_str(payload: dict[str, object], key: str) -> str:
    value = payload[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a nonblank string")
    return value


def _required_float(payload: dict[str, object], key: str) -> float:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{key} must be numeric")
    return float(value)


def _required_str_sequence(payload: dict[str, object], key: str) -> tuple[str, ...]:
    value = payload[key]
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise ValueError(f"{key} must be a string sequence")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{key} entries must be nonblank strings")
    return tuple(value)


def _hash_payload(payload: dict[str, object]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
