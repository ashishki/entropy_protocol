from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.batch_analyst import (
    AllowedAnalystTool,
    BatchAnalystJob,
    BatchAnalystRunner,
    StopReason,
)


def test_batch_job_schema() -> None:
    job = _job()

    assert job.channel_id == "bablos79"
    assert job.allowed_tools == [
        AllowedAnalystTool.RETRIEVE_CONTEXT,
        AllowedAnalystTool.READ_METRICS,
        AllowedAnalystTool.DRAFT_INTERNAL_MEMO,
    ]
    assert job.max_iterations == 3
    assert job.max_retrieved_documents == 5
    assert job.cost_cap_usd == Decimal("1.00")
    assert StopReason.COMPLETED_MEMO in job.stop_reasons


def test_runner_stop_reasons() -> None:
    runner = BatchAnalystRunner()
    job = _job()

    assert (
        runner.run(
            job,
            retrieved_document_ids=["doc-1"],
            metric_ids=["metric-1"],
            prompt_input="prompt",
            iterations_used=3,
        ).stop_reason
        == StopReason.MAX_ITERATIONS
    )
    assert (
        runner.run(
            job,
            retrieved_document_ids=[],
            metric_ids=["metric-1"],
            prompt_input="prompt",
        ).stop_reason
        == StopReason.MISSING_REQUIRED_DATA
    )
    assert (
        runner.run(
            job,
            retrieved_document_ids=["doc-1"],
            metric_ids=["metric-1"],
            prompt_input="prompt",
            cost_used_usd=Decimal("1.00"),
        ).stop_reason
        == StopReason.COST_CAP
    )
    assert (
        runner.run(
            job,
            retrieved_document_ids=["doc-1"],
            metric_ids=["metric-1"],
            prompt_input="prompt",
            generated_memo="internal memo",
        ).stop_reason
        == StopReason.COMPLETED_MEMO
    )


def test_audit_log_records_steps() -> None:
    result = BatchAnalystRunner().run(
        _job(),
        retrieved_document_ids=["doc-1"],
        metric_ids=["metric-1"],
        prompt_input="prompt",
        generated_memo="internal memo",
    )

    steps = {step.step_type: step for step in result.audit_log.steps}

    assert len(steps["retrieval"].checksum) == 64
    assert steps["retrieval"].item_count == 1
    assert len(steps["metric_read"].checksum) == 64
    assert len(steps["prompt_input"].checksum) == 64
    assert len(steps["generated_memo"].checksum) == 64
    assert result.memo_checksum == steps["generated_memo"].checksum


def _job() -> BatchAnalystJob:
    return BatchAnalystJob(
        channel_id="bablos79",
        window_start_utc=datetime(2026, 5, 1, tzinfo=UTC),
        window_end_utc=datetime(2026, 5, 9, tzinfo=UTC),
        allowed_tools=[
            AllowedAnalystTool.RETRIEVE_CONTEXT,
            AllowedAnalystTool.READ_METRICS,
            AllowedAnalystTool.DRAFT_INTERNAL_MEMO,
        ],
        max_iterations=3,
        max_retrieved_documents=5,
        cost_cap_usd=Decimal("1.00"),
        stop_reasons=[
            StopReason.MAX_ITERATIONS,
            StopReason.MISSING_REQUIRED_DATA,
            StopReason.COST_CAP,
            StopReason.COMPLETED_MEMO,
        ],
    )
