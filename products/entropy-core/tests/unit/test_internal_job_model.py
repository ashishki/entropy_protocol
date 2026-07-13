"""Unit tests for in-process internal artifact job model."""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

import entropy.artifacts.jobs as jobs_module
from entropy.artifacts import ArtifactJob, InProcessArtifactJobRegistry


def test_job_model_requires_idempotency_fields() -> None:
    job = ArtifactJob(
        job_id="artifact-job-001",
        operation="validate_artifact",
        artifact_ref="tests/fixtures/artifacts/valid_artifact.json",
        idempotency_key="idem-001",
    )

    assert job.status == "queued"
    assert job.result_ref is None
    assert job.error_code is None
    with pytest.raises(ValidationError):
        ArtifactJob(
            job_id="artifact-job-002",
            operation="validate_artifact",
            artifact_ref="tests/fixtures/artifacts/valid_artifact.json",
            idempotency_key="",
        )
    with pytest.raises(ValidationError, match="Succeeded jobs require"):
        ArtifactJob(
            job_id="artifact-job-003",
            operation="build_evidence",
            artifact_ref="artifact-001",
            idempotency_key="idem-003",
            status="succeeded",
        )


def test_job_idempotency_is_deterministic() -> None:
    registry = InProcessArtifactJobRegistry()
    first = registry.submit(
        operation="validate_artifact",
        artifact_ref="tests/fixtures/artifacts/valid_artifact.json",
        idempotency_key="idem-001",
    )
    duplicate = registry.submit(
        operation="build_evidence",
        artifact_ref="different-artifact",
        idempotency_key="idem-001",
    )
    completed = registry.complete(first, result_ref="artifact://filesystem/result")

    assert first is duplicate
    assert first.job_id == duplicate.job_id
    assert completed.job_id == first.job_id
    assert completed.status == "succeeded"
    assert (
        registry.submit(
            operation="validate_artifact",
            artifact_ref="ignored",
            idempotency_key="idem-001",
        )
        == completed
    )


def test_job_model_has_no_worker_runtime_dependency() -> None:
    source = inspect.getsource(jobs_module).lower()

    assert "celery" not in source
    assert "redis" not in source
    assert "temporal" not in source
    assert "kafka" not in source
    assert "subprocess" not in source
    assert "threading" not in source
    assert "multiprocessing" not in source
