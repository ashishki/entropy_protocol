"""Bounded batch analyst schema and deterministic runner."""

from __future__ import annotations

import hashlib
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AllowedAnalystTool(StrEnum):
    RETRIEVE_CONTEXT = "retrieve_context"
    READ_METRICS = "read_metrics"
    DRAFT_INTERNAL_MEMO = "draft_internal_memo"


class StopReason(StrEnum):
    MAX_ITERATIONS = "max_iterations"
    MISSING_REQUIRED_DATA = "missing_required_data"
    COST_CAP = "cost_cap"
    COMPLETED_MEMO = "completed_memo"


class BatchAnalystJob(BaseModel):
    model_config = ConfigDict(strict=True)

    channel_id: str = Field(min_length=1)
    window_start_utc: datetime
    window_end_utc: datetime
    allowed_tools: list[AllowedAnalystTool]
    max_iterations: int = Field(gt=0)
    max_retrieved_documents: int = Field(gt=0)
    cost_cap_usd: Decimal = Field(ge=Decimal("0"))
    stop_reasons: list[StopReason]

    @field_validator("window_start_utc", "window_end_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("window timestamp must be a datetime or ISO-8601 string")


class AnalystAuditStep(BaseModel):
    model_config = ConfigDict(strict=True)

    step_type: str = Field(min_length=1)
    checksum: str = Field(min_length=64, max_length=64)
    item_count: int = Field(ge=0)


class AnalystAuditLog(BaseModel):
    model_config = ConfigDict(strict=True)

    steps: list[AnalystAuditStep] = Field(default_factory=list)


class BatchAnalystRunResult(BaseModel):
    model_config = ConfigDict(strict=True)

    stop_reason: StopReason
    iterations_used: int
    audit_log: AnalystAuditLog
    memo_checksum: str | None = None


class BatchAnalystRunner:
    def run(
        self,
        job: BatchAnalystJob,
        *,
        retrieved_document_ids: list[str],
        metric_ids: list[str],
        prompt_input: str,
        generated_memo: str | None = None,
        iterations_used: int = 1,
        cost_used_usd: Decimal = Decimal("0"),
    ) -> BatchAnalystRunResult:
        audit_log = AnalystAuditLog(
            steps=[
                _audit_step("retrieval", retrieved_document_ids),
                _audit_step("metric_read", metric_ids),
                _audit_step("prompt_input", [prompt_input]),
            ]
        )

        if iterations_used >= job.max_iterations:
            return _result(StopReason.MAX_ITERATIONS, iterations_used, audit_log)
        if not retrieved_document_ids or not metric_ids:
            return _result(StopReason.MISSING_REQUIRED_DATA, iterations_used, audit_log)
        if cost_used_usd >= job.cost_cap_usd:
            return _result(StopReason.COST_CAP, iterations_used, audit_log)
        if generated_memo:
            memo_checksum = _checksum([generated_memo])
            audit_log.steps.append(
                AnalystAuditStep(
                    step_type="generated_memo",
                    checksum=memo_checksum,
                    item_count=1,
                )
            )
            return _result(
                StopReason.COMPLETED_MEMO,
                iterations_used,
                audit_log,
                memo_checksum=memo_checksum,
            )
        return _result(StopReason.MISSING_REQUIRED_DATA, iterations_used, audit_log)


def _result(
    stop_reason: StopReason,
    iterations_used: int,
    audit_log: AnalystAuditLog,
    *,
    memo_checksum: str | None = None,
) -> BatchAnalystRunResult:
    return BatchAnalystRunResult(
        stop_reason=stop_reason,
        iterations_used=iterations_used,
        audit_log=audit_log,
        memo_checksum=memo_checksum,
    )


def _audit_step(step_type: str, items: list[str]) -> AnalystAuditStep:
    return AnalystAuditStep(
        step_type=step_type,
        checksum=_checksum(items),
        item_count=len(items),
    )


def _checksum(items: list[str]) -> str:
    payload = "\n".join(items)
    return hashlib.sha256(payload.encode()).hexdigest()
