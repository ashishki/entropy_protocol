"""In-process internal artifact job model."""

from __future__ import annotations

import hashlib
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ArtifactJobOperation = Literal["validate_artifact", "build_evidence"]
ArtifactJobStatus = Literal["queued", "running", "succeeded", "failed"]


class ArtifactJobViolation(ValueError):
    """Raised when an internal job shape is invalid."""


class ArtifactJob(BaseModel):
    """Idempotent in-process artifact operation record."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    job_id: str = Field(min_length=1)
    operation: ArtifactJobOperation
    artifact_ref: str = Field(min_length=1)
    idempotency_key: str = Field(min_length=1)
    status: ArtifactJobStatus = "queued"
    result_ref: str | None = Field(default=None, min_length=1)
    error_code: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_job_result_shape(self) -> "ArtifactJob":
        if self.status == "succeeded" and not self.result_ref:
            raise ArtifactJobViolation("Succeeded jobs require a result ref.")
        if self.status == "failed" and not self.error_code:
            raise ArtifactJobViolation("Failed jobs require an error code.")
        if self.status != "failed" and self.error_code:
            raise ArtifactJobViolation("Only failed jobs may carry error codes.")
        return self


class InProcessArtifactJobRegistry:
    """Minimal deterministic idempotency registry for internal jobs."""

    def __init__(self) -> None:
        self._jobs_by_idempotency_key: dict[str, ArtifactJob] = {}

    def submit(
        self,
        *,
        operation: ArtifactJobOperation,
        artifact_ref: str,
        idempotency_key: str,
    ) -> ArtifactJob:
        """Return an existing job for duplicate idempotency keys or create one."""
        existing = self._jobs_by_idempotency_key.get(idempotency_key)
        if existing is not None:
            return existing
        job = ArtifactJob(
            job_id=_job_id(operation, artifact_ref, idempotency_key),
            operation=operation,
            artifact_ref=artifact_ref,
            idempotency_key=idempotency_key,
        )
        self._jobs_by_idempotency_key[idempotency_key] = job
        return job

    def complete(self, job: ArtifactJob, *, result_ref: str) -> ArtifactJob:
        """Return a completed copy and update the in-process registry."""
        completed = job.model_copy(update={"status": "succeeded", "result_ref": result_ref})
        self._jobs_by_idempotency_key[job.idempotency_key] = completed
        return completed

    def fail(self, job: ArtifactJob, *, error_code: str) -> ArtifactJob:
        """Return a failed copy and update the in-process registry."""
        failed = job.model_copy(update={"status": "failed", "error_code": error_code})
        self._jobs_by_idempotency_key[job.idempotency_key] = failed
        return failed


def _job_id(operation: str, artifact_ref: str, idempotency_key: str) -> str:
    payload = f"{operation}:{artifact_ref}:{idempotency_key}"
    return "artifact-job-" + hashlib.sha256(payload.encode()).hexdigest()[:16]


__all__ = [
    "ArtifactJob",
    "ArtifactJobOperation",
    "ArtifactJobStatus",
    "ArtifactJobViolation",
    "InProcessArtifactJobRegistry",
]
