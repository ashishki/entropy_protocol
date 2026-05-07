"""Phase 1B baseline feature contract guards."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass

from entropy.baseline.long_only import PHASE1B_FORBIDDEN_OUTPUT_COLUMNS

PHASE1B_FEATURE_CONTRACT_ID = "PHASE1B-BASELINE-FEATURE-CONTRACT-v1"

PHASE1B_REQUIRED_INPUT_COLUMNS: tuple[str, ...] = (
    "symbol",
    "timestamp_utc",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "dataset_hash",
)

PHASE1B_ALLOWED_FEATURE_COLUMNS: tuple[str, ...] = PHASE1B_REQUIRED_INPUT_COLUMNS

PHASE1B_FORBIDDEN_INPUT_COLUMNS: tuple[str, ...] = PHASE1B_FORBIDDEN_OUTPUT_COLUMNS + (
    "future_return",
    "forward_return",
    "label",
    "target",
    "target_return",
    "validation_label",
    "holdout_label",
)


@dataclass(frozen=True)
class Phase1BFeatureContract:
    """Allowed schema for Phase 1B formation-only baseline inputs."""

    contract_id: str = PHASE1B_FEATURE_CONTRACT_ID
    required_input_columns: tuple[str, ...] = PHASE1B_REQUIRED_INPUT_COLUMNS
    allowed_feature_columns: tuple[str, ...] = PHASE1B_ALLOWED_FEATURE_COLUMNS
    forbidden_input_columns: tuple[str, ...] = PHASE1B_FORBIDDEN_INPUT_COLUMNS
    feature_scope: str = "ohlcv_1d_archive_formation_only"
    lookahead_allowed: bool = False
    performance_fields_allowed: bool = False


@dataclass(frozen=True)
class Phase1BFeatureContractDecision:
    """Feature contract validation result."""

    allowed: bool
    reason_code: str


def validate_phase1b_feature_columns(
    columns: Sequence[str],
    contract: Phase1BFeatureContract | None = None,
) -> Phase1BFeatureContractDecision:
    """Validate input columns against the Phase 1B feature contract."""
    active_contract = contract or Phase1BFeatureContract()
    normalized_columns = set(_nonblank_columns(columns))
    forbidden = normalized_columns.intersection(active_contract.forbidden_input_columns)
    if forbidden:
        return Phase1BFeatureContractDecision(False, "FORBIDDEN_FEATURE_COLUMN")
    missing = set(active_contract.required_input_columns).difference(normalized_columns)
    if missing:
        return Phase1BFeatureContractDecision(False, "MISSING_REQUIRED_INPUT_COLUMN")
    unknown = normalized_columns.difference(active_contract.allowed_feature_columns)
    if unknown:
        return Phase1BFeatureContractDecision(False, "UNKNOWN_FEATURE_COLUMN")
    return Phase1BFeatureContractDecision(True, "FEATURE_COLUMNS_ALLOWED")


def phase1b_feature_contract_payload(
    contract: Phase1BFeatureContract | None = None,
) -> dict[str, object]:
    """Return deterministic feature contract payload."""
    active_contract = contract or Phase1BFeatureContract()
    return {
        "contract_id": active_contract.contract_id,
        "required_input_columns": list(active_contract.required_input_columns),
        "allowed_feature_columns": list(active_contract.allowed_feature_columns),
        "forbidden_input_columns": list(active_contract.forbidden_input_columns),
        "feature_scope": active_contract.feature_scope,
        "lookahead_allowed": active_contract.lookahead_allowed,
        "performance_fields_allowed": active_contract.performance_fields_allowed,
    }


def phase1b_feature_contract_hash(
    contract: Phase1BFeatureContract | None = None,
) -> str:
    """Hash the deterministic Phase 1B feature contract payload."""
    canonical = json.dumps(
        phase1b_feature_contract_payload(contract),
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _nonblank_columns(columns: Sequence[str]) -> tuple[str, ...]:
    if not all(isinstance(column, str) and column.strip() for column in columns):
        raise ValueError("Phase 1B feature columns must be nonblank strings")
    return tuple(columns)
