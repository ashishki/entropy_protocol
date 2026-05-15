"""Unit tests for artifact reproducibility hash comparison."""

from __future__ import annotations

import hashlib
import json

from entropy.artifacts import (
    ArtifactHashCompareRunner,
    ExpectedOutputHash,
    HashComparisonPolicy,
    ReproducibilityManifest,
)


OUTPUT_REF = "artifacts/reproducibility/artifact-001/report.json"


def manifest_for_payload(
    payload: object,
    *,
    ignored_volatile_fields: tuple[str, ...] = (),
    volatile_fields: tuple[str, ...] = (),
    reproducibility_status: str = "fully_reproducible",
    non_reproducible_fields: tuple[str, ...] = (),
) -> ReproducibilityManifest:
    return ReproducibilityManifest.model_validate(
        {
            "artifact_id": "artifact-001",
            "rerun_command": ["python", "-m", "entropy.artifacts.replay_fixture", "artifact-001"],
            "input_refs": ["tests/fixtures/artifacts/valid_artifact.json"],
            "expected_output_refs": [OUTPUT_REF],
            "hash_policy": HashComparisonPolicy(
                expected_hashes=(
                    ExpectedOutputHash(output_ref=OUTPUT_REF, expected_hash=stable_hash(payload)),
                ),
                ignored_volatile_fields=ignored_volatile_fields,
            ),
            "volatile_fields": volatile_fields,
            "accepted_nondeterminism": [
                {"field_path": field, "reason": "declared volatile field"} for field in volatile_fields
            ],
            "reproducibility_status": reproducibility_status,
            "non_reproducible_fields": non_reproducible_fields,
        }
    )


def test_runner_classifies_reproduction_states() -> None:
    expected = {"finding": "same", "generated_at": "2026-05-14T10:00:00Z"}
    exact_manifest = manifest_for_payload(expected)
    runner = ArtifactHashCompareRunner()

    exact = runner.compare_json_output(exact_manifest, OUTPUT_REF, expected, expected)
    assert exact.status == "exact"

    equivalent_manifest = manifest_for_payload(
        expected,
        ignored_volatile_fields=("$.generated_at",),
        volatile_fields=("$.generated_at",),
    )
    equivalent = runner.compare_json_output(
        equivalent_manifest,
        OUTPUT_REF,
        expected,
        {"finding": "same", "generated_at": "2026-05-14T11:00:00Z"},
    )
    assert equivalent.status == "materially_equivalent"

    partial_manifest = manifest_for_payload(
        expected,
        ignored_volatile_fields=("$.generated_at",),
        volatile_fields=("$.generated_at", "$.public_source_capture"),
        reproducibility_status="partially_reproducible",
        non_reproducible_fields=("$.public_source_capture",),
    )
    partial = runner.compare_json_output(
        partial_manifest,
        OUTPUT_REF,
        expected,
        {"finding": "same", "generated_at": "2026-05-14T11:00:00Z"},
    )
    assert partial.status == "partial"

    declared_manifest = manifest_for_payload(
        expected,
        volatile_fields=("$.public_source_capture",),
        reproducibility_status="not_reproducible_by_design",
        non_reproducible_fields=("$.public_source_capture",),
    )
    declared = runner.compare_json_output(
        declared_manifest,
        OUTPUT_REF,
        expected,
        {"finding": "different", "generated_at": "2026-05-14T11:00:00Z"},
    )
    assert declared.status == "declared_non_reproducible"

    failed = runner.compare_json_output(
        equivalent_manifest,
        OUTPUT_REF,
        expected,
        {"finding": "different", "generated_at": "2026-05-14T11:00:00Z"},
    )
    assert failed.status == "failed"


def test_runner_ignores_only_declared_volatile_fields() -> None:
    expected = {"finding": "same", "generated_at": "2026-05-14T10:00:00Z"}
    manifest = manifest_for_payload(
        expected,
        ignored_volatile_fields=("$.generated_at",),
        volatile_fields=("$.generated_at",),
    )

    result = ArtifactHashCompareRunner().compare_json_output(
        manifest,
        OUTPUT_REF,
        expected,
        {"finding": "same", "generated_at": "2026-05-14T11:00:00Z"},
    )
    undeclared_diff = ArtifactHashCompareRunner().compare_json_output(
        manifest,
        OUTPUT_REF,
        expected,
        {"finding": "same", "source_row_count": 12, "generated_at": "2026-05-14T11:00:00Z"},
    )

    assert result.status == "materially_equivalent"
    assert undeclared_diff.status == "failed"
    assert [diff.field_path for diff in undeclared_diff.diff_metadata] == ["$.source_row_count"]


def test_failed_compare_reports_safe_metadata() -> None:
    expected = {"finding": "same", "customer_note": "SECRET_TOKEN_123"}
    actual = {"finding": "different", "customer_note": "SECRET_TOKEN_999"}
    manifest = manifest_for_payload(expected)

    result = ArtifactHashCompareRunner().compare_json_output(manifest, OUTPUT_REF, expected, actual)
    serialized = result.model_dump_json()

    assert result.status == "failed"
    assert result.diff_metadata[0].field_path == "$.customer_note"
    assert result.diff_metadata[0].change_type == "changed_value"
    assert "SECRET_TOKEN_123" not in serialized
    assert "SECRET_TOKEN_999" not in serialized


def stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()
