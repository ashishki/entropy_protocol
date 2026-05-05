"""Phase 1A archive split registration and read-gate boundary."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from entropy.evidence.phase1a_freeze import PHASE1A_ARCHIVE_FREEZE_ID

PHASE1A_REGISTRATION_BOUNDARY_ID = "PHASE1A-ARCHIVE-REGISTRATION-BOUNDARY-v1"
PHASE1A_FORMATION_LABEL = "ARCHIVE_FORMATION"
PHASE1A_VALIDATION_LABEL = "ARCHIVE_VALIDATION"
PHASE1A_HOLDOUT_LABEL = "ARCHIVE_HOLDOUT"


@dataclass(frozen=True)
class Phase1ARegistrationBoundaryResult:
    """Result for a Phase 1A archive registration boundary manifest."""

    boundary_id: str
    manifest_path: Path
    summary_path: Path
    manifest_hash: str
    freeze_manifest_hash: str
    split_count: int
    dataset_count: int
    gate_claim_allowed: bool = False
    archive_only: bool = True


@dataclass(frozen=True)
class Phase1AReadRequest:
    """Archive read request checked by the Phase 1A registration boundary."""

    symbol: str
    split_label: str
    read_purpose: str
    baseline_registration_id: str | None = None
    baseline_spec_hash: str | None = None
    validation_registration_hash: str | None = None
    holdout_unlock_id: str | None = None


@dataclass(frozen=True)
class Phase1AReadAuthorization:
    """Authorization decision for one Phase 1A archive read request."""

    allowed: bool
    reason_code: str
    boundary_id: str
    freeze_id: str
    symbol: str
    split_label: str
    window_start: str | None = None
    window_end: str | None = None
    dataset_hash: str | None = None
    parquet_path: str | None = None
    gate_claim_allowed: bool = False
    archive_only: bool = True


def build_phase1a_registration_boundary_manifest(
    *,
    freeze_manifest_path: Path | str,
    output_dir: Path | str,
    expected_freeze_manifest_hash: str | None = None,
) -> Phase1ARegistrationBoundaryResult:
    """Build the Phase 1A archive split registration/read-gate manifest."""
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    freeze_path = Path(freeze_manifest_path)
    freeze_text = freeze_path.read_text(encoding="utf-8")
    freeze_manifest_hash = hashlib.sha256(freeze_text.encode("utf-8")).hexdigest()
    if (
        expected_freeze_manifest_hash is not None
        and freeze_manifest_hash != expected_freeze_manifest_hash
    ):
        raise ValueError("freeze manifest hash does not match expected hash")
    freeze_manifest = _read_json_object(freeze_path)
    _validate_freeze_manifest(freeze_manifest)

    payload = _manifest_payload(
        freeze_manifest=freeze_manifest,
        freeze_manifest_path=freeze_path,
        freeze_manifest_hash=freeze_manifest_hash,
    )
    manifest_path = root / "PHASE1A_ARCHIVE_REGISTRATION_BOUNDARY_MANIFEST.json"
    summary_path = root / "PHASE1A_ARCHIVE_REGISTRATION_BOUNDARY_SUMMARY.md"
    manifest_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    manifest_path.write_text(manifest_text, encoding="utf-8")
    manifest_hash = hashlib.sha256(manifest_text.encode("utf-8")).hexdigest()
    summary_path.write_text(
        _render_summary(
            payload=payload,
            manifest_hash=manifest_hash,
            freeze_manifest_hash=freeze_manifest_hash,
        ),
        encoding="utf-8",
    )
    return Phase1ARegistrationBoundaryResult(
        boundary_id=PHASE1A_REGISTRATION_BOUNDARY_ID,
        manifest_path=manifest_path,
        summary_path=summary_path,
        manifest_hash=manifest_hash,
        freeze_manifest_hash=freeze_manifest_hash,
        split_count=len(_split_rules()),
        dataset_count=_required_int(freeze_manifest, "dataset_count"),
    )


def authorize_phase1a_archive_read(
    *,
    boundary_manifest_path: Path | str,
    request: Phase1AReadRequest,
) -> Phase1AReadAuthorization:
    """Authorize one archive read request against the registration boundary."""
    boundary = _read_json_object(Path(boundary_manifest_path))
    _validate_boundary_manifest(boundary)
    dataset = _dataset_for_symbol(boundary, request.symbol)
    if dataset is None:
        return _deny(boundary, request, "SYMBOL_NOT_IN_FROZEN_UNIVERSE")
    rule = _rule_for_split(boundary, request.split_label)
    if rule is None:
        return _deny(boundary, request, "SPLIT_NOT_REGISTERED")
    if not _purpose_allowed(rule, request.read_purpose):
        return _deny(boundary, request, "READ_PURPOSE_NOT_ALLOWED")
    if str(rule["default_access"]) == "LOCKED":
        return _deny(boundary, request, str(rule["locked_reason"]))
    missing_fields = _missing_required_fields(rule, request)
    if missing_fields:
        return _deny(boundary, request, "MISSING_REQUIRED_REGISTRATION_FIELDS")

    return Phase1AReadAuthorization(
        allowed=True,
        reason_code="READ_ALLOWED",
        boundary_id=str(boundary["boundary_id"]),
        freeze_id=str(boundary["freeze_id"]),
        symbol=request.symbol,
        split_label=request.split_label,
        window_start=str(rule["window_start"]),
        window_end=str(rule["window_end"]),
        dataset_hash=str(dataset["dataset_hash"]),
        parquet_path=str(dataset["parquet_path"]),
    )


def _read_json_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _validate_freeze_manifest(freeze_manifest: dict[str, object]) -> None:
    expected = {
        "freeze_id": PHASE1A_ARCHIVE_FREEZE_ID,
        "archive_only": True,
        "gate_claim_allowed": False,
        "boundary": "manifest_only_no_strategy_no_portfolio_no_performance_claim",
    }
    for key, value in expected.items():
        if freeze_manifest.get(key) != value:
            raise ValueError(f"freeze manifest has invalid {key}")
    if _required_int(freeze_manifest, "dataset_count") < 1:
        raise ValueError("freeze manifest must contain at least one dataset")
    if not isinstance(freeze_manifest.get("datasets"), list):
        raise ValueError("freeze manifest datasets must be a list")
    if not isinstance(freeze_manifest.get("split_policy"), dict):
        raise ValueError("freeze manifest split_policy must be an object")


def _validate_boundary_manifest(boundary: dict[str, object]) -> None:
    expected = {
        "boundary_id": PHASE1A_REGISTRATION_BOUNDARY_ID,
        "freeze_id": PHASE1A_ARCHIVE_FREEZE_ID,
        "archive_only": True,
        "gate_claim_allowed": False,
        "boundary": "registration_read_gate_no_strategy_no_portfolio_no_performance_claim",
    }
    for key, value in expected.items():
        if boundary.get(key) != value:
            raise ValueError(f"registration boundary manifest has invalid {key}")
    if not isinstance(boundary.get("datasets"), list):
        raise ValueError("registration boundary datasets must be a list")
    if not isinstance(boundary.get("split_rules"), list):
        raise ValueError("registration boundary split_rules must be a list")


def _manifest_payload(
    *,
    freeze_manifest: dict[str, object],
    freeze_manifest_path: Path,
    freeze_manifest_hash: str,
) -> dict[str, object]:
    datasets = _frozen_datasets(freeze_manifest)
    return {
        "boundary_id": PHASE1A_REGISTRATION_BOUNDARY_ID,
        "freeze_id": PHASE1A_ARCHIVE_FREEZE_ID,
        "freeze_manifest_path": freeze_manifest_path.as_posix(),
        "freeze_manifest_hash": freeze_manifest_hash,
        "archive_only": True,
        "gate_claim_allowed": False,
        "status": "READ_GATE_ACTIVE_HOLDOUT_LOCKED",
        "dataset_count": len(datasets),
        "split_count": len(_split_rules()),
        "split_rules": [rule.copy() for rule in _split_rules()],
        "datasets": datasets,
        "allowed_report_labels": freeze_manifest["allowed_report_labels"],
        "forbidden_report_labels": freeze_manifest["forbidden_report_labels"],
        "boundary": "registration_read_gate_no_strategy_no_portfolio_no_performance_claim",
    }


def _split_rules() -> tuple[dict[str, object], ...]:
    return (
        {
            "split_label": PHASE1A_FORMATION_LABEL,
            "window_start": "2020-01-01",
            "window_end": "2022-12-31",
            "default_access": "ALLOW",
            "allowed_purposes": (
                "feature_design",
                "baseline_spec_drafting",
                "instrumentation",
            ),
            "required_fields": (),
            "locked_reason": None,
        },
        {
            "split_label": PHASE1A_VALIDATION_LABEL,
            "window_start": "2023-01-01",
            "window_end": "2024-12-31",
            "default_access": "ALLOW_WITH_REGISTRATION",
            "allowed_purposes": ("registered_validation",),
            "required_fields": (
                "baseline_registration_id",
                "baseline_spec_hash",
                "validation_registration_hash",
            ),
            "locked_reason": None,
        },
        {
            "split_label": PHASE1A_HOLDOUT_LABEL,
            "window_start": "2025-01-01",
            "window_end": "2025-12-31",
            "default_access": "LOCKED",
            "allowed_purposes": ("final_holdout_audit",),
            "required_fields": (
                "baseline_registration_id",
                "baseline_spec_hash",
                "validation_registration_hash",
                "holdout_unlock_id",
            ),
            "locked_reason": "HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION",
        },
    )


def _frozen_datasets(freeze_manifest: dict[str, object]) -> list[dict[str, object]]:
    datasets = freeze_manifest["datasets"]
    if not isinstance(datasets, list):
        raise ValueError("freeze manifest datasets must be a list")
    result = []
    for dataset in datasets:
        if not isinstance(dataset, dict):
            raise ValueError("freeze manifest dataset entries must be objects")
        result.append(
            {
                "symbol": str(dataset["symbol"]),
                "timeframe": str(dataset["timeframe"]),
                "calendar_profile": str(dataset["calendar_profile"]),
                "dataset_hash": str(dataset["dataset_hash"]),
                "parquet_path": str(dataset["parquet_path"]),
            }
        )
    return sorted(result, key=lambda item: item["symbol"])


def _dataset_for_symbol(
    boundary: dict[str, object],
    symbol: str,
) -> dict[str, object] | None:
    datasets = boundary["datasets"]
    if not isinstance(datasets, list):
        raise ValueError("registration boundary datasets must be a list")
    for dataset in datasets:
        if not isinstance(dataset, dict):
            raise ValueError("registration boundary dataset entries must be objects")
        if dataset.get("symbol") == symbol:
            return dataset
    return None


def _rule_for_split(
    boundary: dict[str, object],
    split_label: str,
) -> dict[str, object] | None:
    rules = boundary["split_rules"]
    if not isinstance(rules, list):
        raise ValueError("registration boundary split_rules must be a list")
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("registration boundary split rules must be objects")
        if rule.get("split_label") == split_label:
            return rule
    return None


def _purpose_allowed(rule: dict[str, object], read_purpose: str) -> bool:
    allowed_purposes = _required_str_sequence(rule, "allowed_purposes")
    return read_purpose in allowed_purposes


def _missing_required_fields(
    rule: dict[str, object],
    request: Phase1AReadRequest,
) -> tuple[str, ...]:
    required_fields = _required_str_sequence(rule, "required_fields")
    missing = []
    for field in required_fields:
        value = getattr(request, field)
        if value is None or value == "":
            missing.append(field)
    return tuple(missing)


def _deny(
    boundary: dict[str, object],
    request: Phase1AReadRequest,
    reason_code: str,
) -> Phase1AReadAuthorization:
    return Phase1AReadAuthorization(
        allowed=False,
        reason_code=reason_code,
        boundary_id=str(boundary.get("boundary_id", PHASE1A_REGISTRATION_BOUNDARY_ID)),
        freeze_id=str(boundary.get("freeze_id", PHASE1A_ARCHIVE_FREEZE_ID)),
        symbol=request.symbol,
        split_label=request.split_label,
    )


def _required_int(payload: dict[str, object], key: str) -> int:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    return value


def _required_str_sequence(payload: dict[str, object], key: str) -> tuple[str, ...]:
    value = payload[key]
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise ValueError(f"{key} must be a string sequence")
    if not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} entries must be strings")
    return tuple(value)


def _render_summary(
    *,
    payload: dict[str, object],
    manifest_hash: str,
    freeze_manifest_hash: str,
) -> str:
    lines = [
        "# Phase 1A Archive Registration Boundary Summary",
        "",
        f"Boundary ID: `{payload['boundary_id']}`",
        f"Manifest hash: `{manifest_hash}`",
        f"Freeze manifest hash: `{freeze_manifest_hash}`",
        "Status: `READ_GATE_ACTIVE_HOLDOUT_LOCKED`",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Dataset count | {payload['dataset_count']} |",
        f"| Split count | {payload['split_count']} |",
        f"| Archive only | {payload['archive_only']} |",
        f"| Gate claim allowed | {payload['gate_claim_allowed']} |",
        "",
        "| Split | Window | Default access | Required fields |",
        "|---|---|---|---|",
    ]
    rules = payload["split_rules"]
    if not isinstance(rules, list):
        raise ValueError("split_rules must be a list")
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("split rules must be objects")
        required = ", ".join(_required_str_sequence(rule, "required_fields")) or "none"
        lines.append(
            "| "
            f"{rule['split_label']} | "
            f"{rule['window_start']} through {rule['window_end']} | "
            f"{rule['default_access']} | "
            f"{required} |"
        )
    lines.extend(
        [
            "",
            "Boundary: this registration gate only controls archive read access. It does "
            "not implement strategies, run archive evaluation, activate Growth/RDL/RBE, "
            "activate live feeds, or make OOS/performance claims.",
        ]
    )
    return "\n".join(lines) + "\n"
