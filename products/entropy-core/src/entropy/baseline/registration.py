"""Phase 1F baseline registration and hash-binding surfaces.

This module builds deterministic preregistration payloads only. It does not
write to the Trial Registry, run evaluation, or read validation/holdout data.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from entropy.baseline.bounded import (
    PHASE1E_BOUNDED_BASELINE_LOGIC_ID,
    PHASE1E_NO_CLAIM_LABELS,
    PHASE1E_REQUIRED_OUTPUT_COLUMNS,
    Phase1EBoundedBaselineOutput,
)
from entropy.baseline.formation import Phase1BFormationInputFrame
from entropy.baseline.implementation import (
    Phase1DImplementationContract,
    phase1d_implementation_contract_hash,
)
from entropy.baseline.long_only import (
    Phase1BBaselineSurface,
    phase1b_surface_schema_hash,
)
from entropy.models.registry import TrialSpec

PHASE1F_BASELINE_HASH_BINDING_ID = "PHASE1F-BASELINE-CODE-POLICY-HASH-BINDING-v1"
PHASE1F_TRIAL_PREREGISTRATION_SURFACE_ID = "PHASE1F-TRIAL-PREREGISTRATION-SURFACE-v1"

PHASE1F_TRIAL_ID = "P1-LONG-ONLY-BASELINE-TRIAL-v1"
PHASE1F_FAMILY_TAG = "long_only_baseline"
PHASE1F_HYPOTHESIS = (
    "Deterministic long-only archive baseline can be registered for future governed "
    "evaluation without holdout access or performance claims."
)

PHASE1F_NO_CLAIM_LABELS: tuple[str, ...] = PHASE1E_NO_CLAIM_LABELS + (
    "preregistration_surface_only",
    "not_registry_write",
)


@dataclass(frozen=True)
class Phase1FBaselineHashBinding:
    """Code, policy, input, and dataset hashes for the bounded baseline."""

    binding_id: str
    trial_id: str
    family_tag: str
    surface_id: str
    baseline_spec_hash: str
    logic_id: str
    code_hash: str
    policy_hash: str
    input_contract_hash: str
    dataset_hash: str
    surface_schema_hash: str
    implementation_contract_hash: str
    skill_families: tuple[str, ...]
    output_hashes: tuple[str, ...]
    no_claim_labels: tuple[str, ...]
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False
    registry_write_allowed: bool = False
    phase_gate_evidence: bool = False


@dataclass(frozen=True)
class Phase1FPreRegistrationSurface:
    """TrialSpec surface prepared for future explicit registry write approval."""

    surface_id: str
    binding_id: str
    trial_spec: TrialSpec
    parameter_lock_hash: str
    no_claim_labels: tuple[str, ...]
    registry_write_allowed: bool = False
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False
    phase_gate_evidence: bool = False


def build_phase1f_baseline_hash_binding(
    surface: Phase1BBaselineSurface,
    formation_input: Phase1BFormationInputFrame,
    contract: Phase1DImplementationContract,
    outputs: Sequence[Phase1EBoundedBaselineOutput],
    *,
    source_paths: Sequence[Path | str],
) -> Phase1FBaselineHashBinding:
    """Bind bounded baseline code, policy, input, and output hashes."""
    ordered_outputs = _validate_outputs(surface, outputs)
    code_hash = _hash_source_files(source_paths)
    implementation_contract_hash = phase1d_implementation_contract_hash(contract)
    surface_schema_hash = phase1b_surface_schema_hash(surface)
    policy_hash = _hash_payload(
        {
            "logic_id": PHASE1E_BOUNDED_BASELINE_LOGIC_ID,
            "surface_schema_hash": surface_schema_hash,
            "implementation_contract_hash": implementation_contract_hash,
            "required_output_columns": PHASE1E_REQUIRED_OUTPUT_COLUMNS,
            "no_claim_labels": PHASE1F_NO_CLAIM_LABELS,
        }
    )
    return Phase1FBaselineHashBinding(
        binding_id=PHASE1F_BASELINE_HASH_BINDING_ID,
        trial_id=PHASE1F_TRIAL_ID,
        family_tag=PHASE1F_FAMILY_TAG,
        surface_id=surface.surface_id,
        baseline_spec_hash=surface.baseline_spec_hash,
        logic_id=PHASE1E_BOUNDED_BASELINE_LOGIC_ID,
        code_hash=code_hash,
        policy_hash=policy_hash,
        input_contract_hash=formation_input.feature_contract_hash,
        dataset_hash=_hash_payload({"dataset_hashes": formation_input.dataset_hashes}),
        surface_schema_hash=surface_schema_hash,
        implementation_contract_hash=implementation_contract_hash,
        skill_families=tuple(output.skill_family for output in ordered_outputs),
        output_hashes=tuple(output.output_hash for output in ordered_outputs),
        no_claim_labels=PHASE1F_NO_CLAIM_LABELS,
    )


def build_phase1f_preregistration_surface(
    binding: Phase1FBaselineHashBinding,
    *,
    registered_at: datetime,
) -> Phase1FPreRegistrationSurface:
    """Build a TrialSpec payload without writing it to the registry."""
    parameter_lock = {
        "binding_id": binding.binding_id,
        "logic_id": binding.logic_id,
        "surface_id": binding.surface_id,
        "baseline_spec_hash": binding.baseline_spec_hash,
        "input_contract_hash": binding.input_contract_hash,
        "surface_schema_hash": binding.surface_schema_hash,
        "implementation_contract_hash": binding.implementation_contract_hash,
        "skill_families": list(binding.skill_families),
        "output_hashes": list(binding.output_hashes),
        "no_claim_labels": list(binding.no_claim_labels),
        "evaluation_allowed": binding.evaluation_allowed,
        "gate_claim_allowed": binding.gate_claim_allowed,
        "registry_write_allowed": binding.registry_write_allowed,
    }
    trial_spec = TrialSpec(
        trial_id=binding.trial_id,
        family_tag=binding.family_tag,
        hypothesis=PHASE1F_HYPOTHESIS,
        dataset_hash=binding.dataset_hash,
        code_hash=binding.code_hash,
        policy_hash=binding.policy_hash,
        parameter_lock=parameter_lock,
        registered_at=registered_at,
    )
    return Phase1FPreRegistrationSurface(
        surface_id=PHASE1F_TRIAL_PREREGISTRATION_SURFACE_ID,
        binding_id=binding.binding_id,
        trial_spec=trial_spec,
        parameter_lock_hash=_hash_payload(parameter_lock),
        no_claim_labels=PHASE1F_NO_CLAIM_LABELS,
    )


def phase1f_hash_binding_payload(binding: Phase1FBaselineHashBinding) -> dict[str, object]:
    """Return deterministic hash-binding payload."""
    return {
        "binding_id": binding.binding_id,
        "trial_id": binding.trial_id,
        "family_tag": binding.family_tag,
        "surface_id": binding.surface_id,
        "baseline_spec_hash": binding.baseline_spec_hash,
        "logic_id": binding.logic_id,
        "code_hash": binding.code_hash,
        "policy_hash": binding.policy_hash,
        "input_contract_hash": binding.input_contract_hash,
        "dataset_hash": binding.dataset_hash,
        "surface_schema_hash": binding.surface_schema_hash,
        "implementation_contract_hash": binding.implementation_contract_hash,
        "skill_families": list(binding.skill_families),
        "output_hashes": list(binding.output_hashes),
        "no_claim_labels": list(binding.no_claim_labels),
        "evaluation_allowed": binding.evaluation_allowed,
        "gate_claim_allowed": binding.gate_claim_allowed,
        "registry_write_allowed": binding.registry_write_allowed,
        "phase_gate_evidence": binding.phase_gate_evidence,
    }


def phase1f_hash_binding_hash(binding: Phase1FBaselineHashBinding) -> str:
    """Hash the deterministic Phase 1F hash-binding payload."""
    return _hash_payload(phase1f_hash_binding_payload(binding))


def _validate_outputs(
    surface: Phase1BBaselineSurface,
    outputs: Sequence[Phase1EBoundedBaselineOutput],
) -> tuple[Phase1EBoundedBaselineOutput, ...]:
    if not outputs:
        raise ValueError("Phase 1F hash binding requires bounded baseline outputs")
    ordered = tuple(sorted(outputs, key=lambda output: output.skill_family))
    expected_families = {skill.family for skill in surface.skill_interfaces}
    output_families = {output.skill_family for output in ordered}
    if output_families != expected_families:
        raise ValueError("Phase 1F hash binding requires outputs for all registered skill families")
    for output in ordered:
        if output.logic_id != PHASE1E_BOUNDED_BASELINE_LOGIC_ID:
            raise ValueError("Phase 1F hash binding requires Phase 1E bounded outputs")
        if output.evaluation_allowed or output.gate_claim_allowed or output.phase_gate_evidence:
            raise ValueError("Phase 1F hash binding requires no-claim outputs")
    return ordered


def _hash_source_files(source_paths: Sequence[Path | str]) -> str:
    paths = tuple(Path(path) for path in source_paths)
    if not paths:
        raise ValueError("Phase 1F code hash requires at least one source path")
    payload = []
    for path in sorted(paths, key=_source_identity):
        if not path.is_file():
            raise ValueError(f"Phase 1F code hash source does not exist: {path}")
        payload.append(
            {
                "path": _source_identity(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    return _hash_payload(payload)


def _source_identity(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def _hash_payload(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
