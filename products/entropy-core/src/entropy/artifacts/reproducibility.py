"""Reproducibility manifest schema for governed artifacts."""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from entropy.artifacts.contract import ARTIFACT_CONTRACT_VERSION

REPRODUCIBILITY_MANIFEST_VERSION = "entropy-artifact-reproducibility/v1"
HASH_METHODS = ("sha256",)
REPRODUCIBILITY_STATUSES = (
    "fully_reproducible",
    "partially_reproducible",
    "not_reproducible_by_design",
)
REPRODUCTION_RESULT_STATUSES = (
    "exact",
    "materially_equivalent",
    "partial",
    "declared_non_reproducible",
    "failed",
)
FORBIDDEN_COMMAND_TOKENS = (
    "bash",
    "cmd",
    "curl",
    "fish",
    "powershell",
    "pwsh",
    "scp",
    "sh",
    "ssh",
    "wget",
    "zsh",
)
FORBIDDEN_SHELL_MARKERS = ("&&", ";", "|", ">", "<", "$(", "`")


class ReproducibilityManifestViolation(ValueError):
    """Raised when a reproducibility manifest violates local safety rules."""


class ExpectedOutputHash(BaseModel):
    """Expected stable hash binding for one rerun output."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    output_ref: str = Field(min_length=1)
    expected_hash: str = Field(min_length=1)


class HashComparisonPolicy(BaseModel):
    """Hash comparison policy for stable and volatile output fields."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    method: Literal["sha256"] = "sha256"
    expected_hashes: tuple[ExpectedOutputHash, ...] = Field(min_length=1)
    ignored_volatile_fields: tuple[str, ...] = ()


class AcceptedNondeterminism(BaseModel):
    """One declared nondeterministic field and its bounded reason."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    field_path: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class ReproductionDiff(BaseModel):
    """Safe metadata for one stable-field reproduction difference."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    field_path: str
    change_type: Literal["added", "removed", "changed_type", "changed_value"]
    expected_type: str | None = None
    actual_type: str | None = None


class ReproductionCompareResult(BaseModel):
    """Deterministic reproduction comparison result without raw payload dumps."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    status: Literal[
        "exact",
        "materially_equivalent",
        "partial",
        "declared_non_reproducible",
        "failed",
    ]
    output_ref: str
    expected_hash: str
    actual_hash: str
    stable_expected_hash: str
    stable_actual_hash: str
    ignored_volatile_fields: tuple[str, ...] = ()
    diff_metadata: tuple[ReproductionDiff, ...] = ()


class ReproducibilityManifest(BaseModel):
    """Manifest describing how Core can rerun or classify artifact reproducibility."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    manifest_version: Literal["entropy-artifact-reproducibility/v1"] = (
        REPRODUCIBILITY_MANIFEST_VERSION
    )
    artifact_id: str = Field(min_length=1)
    artifact_contract_version: Literal["entropy-core-artifact/v1"] = ARTIFACT_CONTRACT_VERSION
    rerun_command: tuple[str, ...] = Field(min_length=1)
    input_refs: tuple[str, ...] = Field(min_length=1)
    expected_output_refs: tuple[str, ...] = Field(min_length=1)
    hash_policy: HashComparisonPolicy
    volatile_fields: tuple[str, ...] = ()
    accepted_nondeterminism: tuple[AcceptedNondeterminism, ...] = ()
    reproducibility_status: Literal[
        "fully_reproducible",
        "partially_reproducible",
        "not_reproducible_by_design",
    ]
    non_reproducible_fields: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_manifest(self) -> "ReproducibilityManifest":
        _validate_rerun_command(self.rerun_command)
        volatile = set(self.volatile_fields)
        ignored = set(self.hash_policy.ignored_volatile_fields)
        accepted = {entry.field_path for entry in self.accepted_nondeterminism}
        undeclared = ignored.union(accepted).difference(volatile)
        if undeclared:
            raise ReproducibilityManifestViolation(
                "Volatile or nondeterministic fields must be declared."
            )
        if self.reproducibility_status == "fully_reproducible" and self.non_reproducible_fields:
            raise ReproducibilityManifestViolation(
                "Fully reproducible manifests cannot list non-reproducible fields."
            )
        if (
            self.reproducibility_status != "fully_reproducible"
            and not self.non_reproducible_fields
        ):
            raise ReproducibilityManifestViolation(
                "Partial or non-reproducible manifests must declare affected fields."
            )
        return self


class ArtifactHashCompareRunner:
    """Compare expected and rerun artifact outputs without executing commands."""

    def compare_json_output(
        self,
        manifest: ReproducibilityManifest,
        output_ref: str,
        expected_payload: object,
        actual_payload: object,
    ) -> ReproductionCompareResult:
        """Compare one JSON-like output using the manifest hash and volatility policy."""
        expected_hash = _expected_hash_for_output(manifest, output_ref)
        actual_hash = _stable_hash(actual_payload)

        ignored_fields = manifest.hash_policy.ignored_volatile_fields
        stable_expected = _without_fields(expected_payload, ignored_fields)
        stable_actual = _without_fields(actual_payload, ignored_fields)
        stable_expected_hash = _stable_hash(stable_expected)
        stable_actual_hash = _stable_hash(stable_actual)
        diff_metadata = tuple(_diff_payloads(stable_expected, stable_actual, "$"))

        if manifest.reproducibility_status == "not_reproducible_by_design":
            status = "declared_non_reproducible"
        elif actual_hash == expected_hash:
            status = "exact"
        elif stable_expected_hash == stable_actual_hash:
            status = (
                "partial"
                if manifest.reproducibility_status == "partially_reproducible"
                else "materially_equivalent"
            )
        else:
            status = "failed"

        return ReproductionCompareResult(
            status=status,
            output_ref=output_ref,
            expected_hash=expected_hash,
            actual_hash=actual_hash,
            stable_expected_hash=stable_expected_hash,
            stable_actual_hash=stable_actual_hash,
            ignored_volatile_fields=ignored_fields,
            diff_metadata=diff_metadata,
        )


def _validate_rerun_command(command: tuple[str, ...]) -> None:
    executable = command[0].lower()
    if executable in FORBIDDEN_COMMAND_TOKENS:
        raise ReproducibilityManifestViolation("Rerun command uses a forbidden executable.")
    for token in command:
        lowered = token.lower()
        if lowered in FORBIDDEN_COMMAND_TOKENS:
            raise ReproducibilityManifestViolation("Rerun command uses a forbidden token.")
        if any(marker in token for marker in FORBIDDEN_SHELL_MARKERS):
            raise ReproducibilityManifestViolation("Rerun command uses shell syntax.")


def _expected_hash_for_output(manifest: ReproducibilityManifest, output_ref: str) -> str:
    for expected_hash in manifest.hash_policy.expected_hashes:
        if expected_hash.output_ref == output_ref:
            return expected_hash.expected_hash
    raise ReproducibilityManifestViolation("Output ref is not declared in hash policy.")


def _without_fields(payload: object, field_paths: Sequence[str]) -> object:
    cloned = copy.deepcopy(payload)
    for field_path in field_paths:
        _delete_field_path(cloned, field_path)
    return cloned


def _delete_field_path(payload: object, field_path: str) -> None:
    parts = _field_path_parts(field_path)
    if not parts:
        return
    current = payload
    for part in parts[:-1]:
        if not isinstance(current, dict):
            return
        current = current.get(part)
    if isinstance(current, dict):
        current.pop(parts[-1], None)


def _field_path_parts(field_path: str) -> tuple[str, ...]:
    if not field_path.startswith("$."):
        return ()
    return tuple(part for part in field_path[2:].split(".") if part)


def _stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _diff_payloads(expected: object, actual: object, field_path: str) -> list[ReproductionDiff]:
    if isinstance(expected, Mapping) and isinstance(actual, Mapping):
        diffs: list[ReproductionDiff] = []
        keys = sorted(set(expected).union(actual))
        for key in keys:
            child_path = f"{field_path}.{key}"
            if key not in expected:
                diffs.append(
                    ReproductionDiff(
                        field_path=child_path,
                        change_type="added",
                        actual_type=_type_name(actual[key]),
                    )
                )
            elif key not in actual:
                diffs.append(
                    ReproductionDiff(
                        field_path=child_path,
                        change_type="removed",
                        expected_type=_type_name(expected[key]),
                    )
                )
            else:
                diffs.extend(_diff_payloads(expected[key], actual[key], child_path))
        return diffs
    if type(expected) is not type(actual):
        return [
            ReproductionDiff(
                field_path=field_path,
                change_type="changed_type",
                expected_type=_type_name(expected),
                actual_type=_type_name(actual),
            )
        ]
    if expected != actual:
        return [
            ReproductionDiff(
                field_path=field_path,
                change_type="changed_value",
                expected_type=_type_name(expected),
                actual_type=_type_name(actual),
            )
        ]
    return []


def _type_name(value: object) -> str:
    return type(value).__name__


__all__ = [
    "FORBIDDEN_COMMAND_TOKENS",
    "FORBIDDEN_SHELL_MARKERS",
    "HASH_METHODS",
    "REPRODUCTION_RESULT_STATUSES",
    "REPRODUCIBILITY_MANIFEST_VERSION",
    "REPRODUCIBILITY_STATUSES",
    "AcceptedNondeterminism",
    "ArtifactHashCompareRunner",
    "ExpectedOutputHash",
    "HashComparisonPolicy",
    "ReproductionCompareResult",
    "ReproductionDiff",
    "ReproducibilityManifest",
    "ReproducibilityManifestViolation",
]
