"""Phase 1A archive baseline specification registration."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
    PHASE1A_VALIDATION_LABEL,
)

PHASE1A_BASELINE_REGISTRATION_ID = "PHASE1A-BASELINE-SPEC-REGISTRATION-v1"
PHASE1A_DEFAULT_BASELINE_SPEC_ID = "P1A-LONG-ONLY-BASELINE-SPEC-v1"
PHASE1A_DEFAULT_BASELINE_REGISTRATION_INSTANCE_ID = "P1A-BASELINE-REG-001"


@dataclass(frozen=True)
class Phase1APortfolioConstraints:
    """Portfolio constraints for the registered Phase 1A baseline shape."""

    direction: str = "long_only"
    gross_min: float = 0.0
    gross_max: float = 1.0
    short_exposure: float = 0.0
    leverage: str = "none"
    rebalance_policy: str = "deterministic_preregistered_before_validation"
    treasury_stream: str = "report_only_excluded_from_net_sharpe"


@dataclass(frozen=True)
class Phase1ABaselineSpec:
    """Machine-readable non-executable Phase 1A baseline specification."""

    spec_id: str = PHASE1A_DEFAULT_BASELINE_SPEC_ID
    version: str = "v1"
    direction: str = "long_only"
    max_skill_families: int = 6
    skill_families: tuple[str, ...] = (
        "trend_following",
        "breakout",
        "mean_reversion",
        "volatility_filter",
        "regime_state_filter",
        "cost_aware_risk_filter",
    )
    feature_scope: str = "ohlcv_1d_archive_derived_only"
    signal_runtime_status: str = "not_implemented"
    portfolio_constraints: Phase1APortfolioConstraints = Phase1APortfolioConstraints()
    allowed_split_labels: tuple[str, ...] = (
        PHASE1A_FORMATION_LABEL,
        PHASE1A_VALIDATION_LABEL,
    )
    forbidden_split_labels: tuple[str, ...] = (PHASE1A_HOLDOUT_LABEL,)
    allowed_report_labels: tuple[str, ...] = (
        "archive-only",
        "archive-formation",
        "archive-validation",
        "implementation-evidence",
        "not_phase_gate_approval",
    )
    forbidden_report_labels: tuple[str, ...] = (
        "live",
        "production",
        "capital-ready",
        "OOS performance",
        "validated alpha",
        "RDL telemetry closed",
        "K-report closed",
        "RBE activated",
    )


@dataclass(frozen=True)
class Phase1ABaselineRegistrationResult:
    """Result for a Phase 1A baseline specification registration manifest."""

    registration_id: str
    manifest_path: Path
    summary_path: Path
    manifest_hash: str
    baseline_spec_hash: str
    validation_registration_hash: str
    boundary_manifest_hash: str
    gate_claim_allowed: bool = False
    archive_only: bool = True


def build_phase1a_baseline_registration_manifest(
    *,
    boundary_manifest_path: Path | str,
    output_dir: Path | str,
    baseline_spec: Phase1ABaselineSpec | None = None,
    registration_instance_id: str = PHASE1A_DEFAULT_BASELINE_REGISTRATION_INSTANCE_ID,
    expected_boundary_manifest_hash: str | None = None,
) -> Phase1ABaselineRegistrationResult:
    """Register the non-executable Phase 1A archive baseline specification."""
    spec = baseline_spec or Phase1ABaselineSpec()
    _validate_baseline_spec(spec)
    if not registration_instance_id.strip():
        raise ValueError("registration_instance_id must not be blank")

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    boundary_path = Path(boundary_manifest_path)
    boundary_text = boundary_path.read_text(encoding="utf-8")
    boundary_manifest_hash = hashlib.sha256(boundary_text.encode("utf-8")).hexdigest()
    if (
        expected_boundary_manifest_hash is not None
        and boundary_manifest_hash != expected_boundary_manifest_hash
    ):
        raise ValueError("boundary manifest hash does not match expected hash")
    boundary_manifest = _read_json_object(boundary_path)
    _validate_boundary_manifest(boundary_manifest)

    spec_payload = _baseline_spec_payload(spec)
    baseline_spec_hash = _hash_payload(spec_payload)
    validation_registration_hash = _hash_payload(
        {
            "registration_instance_id": registration_instance_id,
            "baseline_spec_hash": baseline_spec_hash,
            "boundary_manifest_hash": boundary_manifest_hash,
            "validation_split_label": PHASE1A_VALIDATION_LABEL,
            "validation_read_purpose": "registered_validation",
        }
    )
    payload = _manifest_payload(
        boundary_manifest=boundary_manifest,
        boundary_manifest_path=boundary_path,
        boundary_manifest_hash=boundary_manifest_hash,
        spec_payload=spec_payload,
        baseline_spec_hash=baseline_spec_hash,
        validation_registration_hash=validation_registration_hash,
        registration_instance_id=registration_instance_id,
    )
    manifest_path = root / "PHASE1A_BASELINE_SPEC_REGISTRATION_MANIFEST.json"
    summary_path = root / "PHASE1A_BASELINE_SPEC_REGISTRATION_SUMMARY.md"
    manifest_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    manifest_path.write_text(manifest_text, encoding="utf-8")
    manifest_hash = hashlib.sha256(manifest_text.encode("utf-8")).hexdigest()
    summary_path.write_text(
        _render_summary(
            payload=payload,
            manifest_hash=manifest_hash,
            baseline_spec_hash=baseline_spec_hash,
            validation_registration_hash=validation_registration_hash,
        ),
        encoding="utf-8",
    )
    return Phase1ABaselineRegistrationResult(
        registration_id=PHASE1A_BASELINE_REGISTRATION_ID,
        manifest_path=manifest_path,
        summary_path=summary_path,
        manifest_hash=manifest_hash,
        baseline_spec_hash=baseline_spec_hash,
        validation_registration_hash=validation_registration_hash,
        boundary_manifest_hash=boundary_manifest_hash,
    )


def _read_json_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _validate_boundary_manifest(boundary_manifest: dict[str, object]) -> None:
    expected = {
        "boundary_id": PHASE1A_REGISTRATION_BOUNDARY_ID,
        "archive_only": True,
        "gate_claim_allowed": False,
        "status": "READ_GATE_ACTIVE_HOLDOUT_LOCKED",
        "boundary": "registration_read_gate_no_strategy_no_portfolio_no_performance_claim",
    }
    for key, value in expected.items():
        if boundary_manifest.get(key) != value:
            raise ValueError(f"boundary manifest has invalid {key}")
    rules = boundary_manifest.get("split_rules")
    if not isinstance(rules, list):
        raise ValueError("boundary manifest split_rules must be a list")
    holdout_rule = _rule_for_split(rules, PHASE1A_HOLDOUT_LABEL)
    if holdout_rule.get("default_access") != "LOCKED":
        raise ValueError("holdout split must remain locked")


def _validate_baseline_spec(spec: Phase1ABaselineSpec) -> None:
    if not spec.spec_id.strip():
        raise ValueError("baseline spec_id must not be blank")
    if spec.direction != "long_only":
        raise ValueError("Phase 1A baseline spec must be long_only")
    if spec.max_skill_families != 6:
        raise ValueError("Phase 1A baseline spec max_skill_families must equal 6")
    if not spec.skill_families:
        raise ValueError("Phase 1A baseline spec requires skill families")
    if len(spec.skill_families) > spec.max_skill_families:
        raise ValueError("Phase 1A baseline spec allows at most 6 skill families")
    _require_unique_strings(spec.skill_families, "skill_families")
    if spec.feature_scope != "ohlcv_1d_archive_derived_only":
        raise ValueError("Phase 1A baseline spec only allows OHLCV-derived 1d archive features")
    if spec.signal_runtime_status != "not_implemented":
        raise ValueError("Phase 1A baseline registration must not implement signals")
    constraints = spec.portfolio_constraints
    if constraints.direction != "long_only":
        raise ValueError("portfolio direction must be long_only")
    if constraints.gross_min != 0.0 or constraints.gross_max != 1.0:
        raise ValueError("portfolio gross bounds must be 0.0..1.0")
    if constraints.short_exposure != 0.0:
        raise ValueError("short exposure must be 0.0")
    if constraints.leverage != "none":
        raise ValueError("leverage must be none")
    if PHASE1A_HOLDOUT_LABEL not in spec.forbidden_split_labels:
        raise ValueError("holdout split must be forbidden in baseline registration")
    if PHASE1A_HOLDOUT_LABEL in spec.allowed_split_labels:
        raise ValueError("holdout split must not be allowed in baseline registration")
    if "OOS performance" not in spec.forbidden_report_labels:
        raise ValueError("OOS performance must remain a forbidden report label")


def _baseline_spec_payload(spec: Phase1ABaselineSpec) -> dict[str, object]:
    payload = asdict(spec)
    payload["portfolio_constraints"] = asdict(spec.portfolio_constraints)
    payload["archive_only"] = True
    payload["gate_claim_allowed"] = False
    payload["boundary"] = "baseline_spec_registration_no_executable_strategy"
    return payload


def _manifest_payload(
    *,
    boundary_manifest: dict[str, object],
    boundary_manifest_path: Path,
    boundary_manifest_hash: str,
    spec_payload: dict[str, object],
    baseline_spec_hash: str,
    validation_registration_hash: str,
    registration_instance_id: str,
) -> dict[str, object]:
    return {
        "registration_id": PHASE1A_BASELINE_REGISTRATION_ID,
        "registration_instance_id": registration_instance_id,
        "boundary_id": PHASE1A_REGISTRATION_BOUNDARY_ID,
        "boundary_manifest_path": boundary_manifest_path.as_posix(),
        "boundary_manifest_hash": boundary_manifest_hash,
        "freeze_id": boundary_manifest["freeze_id"],
        "freeze_manifest_hash": boundary_manifest["freeze_manifest_hash"],
        "baseline_spec": spec_payload,
        "baseline_spec_hash": baseline_spec_hash,
        "validation_registration_hash": validation_registration_hash,
        "formation_access": {
            "split_label": PHASE1A_FORMATION_LABEL,
            "read_purpose": "baseline_spec_drafting",
            "access": "allowed",
        },
        "validation_access": {
            "split_label": PHASE1A_VALIDATION_LABEL,
            "read_purpose": "registered_validation",
            "access": "allowed_with_registration",
            "baseline_registration_id": registration_instance_id,
            "baseline_spec_hash": baseline_spec_hash,
            "validation_registration_hash": validation_registration_hash,
        },
        "holdout_access": {
            "split_label": PHASE1A_HOLDOUT_LABEL,
            "access": "locked",
            "locked_reason": "HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION",
        },
        "archive_only": True,
        "gate_claim_allowed": False,
        "boundary": "baseline_spec_registration_no_strategy_no_portfolio_no_performance_claim",
    }


def _rule_for_split(
    rules: Sequence[object],
    split_label: str,
) -> dict[str, object]:
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("split rules must be objects")
        if rule.get("split_label") == split_label:
            return rule
    raise ValueError(f"missing split rule {split_label}")


def _require_unique_strings(values: Sequence[str], name: str) -> None:
    if not all(isinstance(value, str) and value.strip() for value in values):
        raise ValueError(f"{name} must contain nonblank strings")
    if len(set(values)) != len(values):
        raise ValueError(f"{name} must be unique")


def _hash_payload(payload: dict[str, object]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _render_summary(
    *,
    payload: dict[str, object],
    manifest_hash: str,
    baseline_spec_hash: str,
    validation_registration_hash: str,
) -> str:
    baseline_spec = payload["baseline_spec"]
    if not isinstance(baseline_spec, dict):
        raise ValueError("baseline_spec must be an object")
    skill_families = baseline_spec["skill_families"]
    if not isinstance(skill_families, Sequence) or isinstance(skill_families, str):
        raise ValueError("skill_families must be a string sequence")
    lines = [
        "# Phase 1A Baseline Specification Registration Summary",
        "",
        f"Registration ID: `{payload['registration_id']}`",
        f"Registration instance ID: `{payload['registration_instance_id']}`",
        f"Manifest hash: `{manifest_hash}`",
        f"Baseline spec hash: `{baseline_spec_hash}`",
        f"Validation registration hash: `{validation_registration_hash}`",
        f"Boundary manifest hash: `{payload['boundary_manifest_hash']}`",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Spec ID | {baseline_spec['spec_id']} |",
        f"| Direction | {baseline_spec['direction']} |",
        f"| Skill families | {len(skill_families)} |",
        f"| Feature scope | {baseline_spec['feature_scope']} |",
        f"| Runtime status | {baseline_spec['signal_runtime_status']} |",
        f"| Archive only | {payload['archive_only']} |",
        f"| Gate claim allowed | {payload['gate_claim_allowed']} |",
        "",
        "Registered skill families:",
        "",
    ]
    for family in skill_families:
        lines.append(f"- `{family}`")
    lines.extend(
        [
            "",
            "Access state:",
            "",
            "- `ARCHIVE_FORMATION`: allowed for baseline specification drafting.",
            "- `ARCHIVE_VALIDATION`: allowed only with the recorded registration metadata.",
            "- `ARCHIVE_HOLDOUT`: locked; no unlock is produced by this registration.",
            "",
            "Boundary: this registration records a non-executable baseline specification "
            "shape only. It does not implement strategies, run portfolio/backtest "
            "evaluation, activate Growth/RDL/RBE, activate live feeds, unlock holdout, "
            "or make OOS/performance claims.",
        ]
    )
    return "\n".join(lines) + "\n"
