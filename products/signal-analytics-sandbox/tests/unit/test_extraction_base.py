from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from signal_sandbox.capture.loader import CapturedPost, compute_text_sha256
from signal_sandbox.extraction.base import (
    ExtractionAdapter,
    ExtractionResult,
    ExtractionStatus,
)
from signal_sandbox.ledger.record import Direction, SignalRecord


def post() -> CapturedPost:
    raw_text = "BTC long entry 100 target 110 stop 90"
    return CapturedPost(
        capture_id="cap-001",
        source_id="pilot",
        evidence_url="https://t.me/bablos79/1",
        capture_timestamp_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        raw_text=raw_text,
        text_sha256=compute_text_sha256(raw_text),
    )


def record(captured: CapturedPost, *, evidence_url: str | None = None) -> SignalRecord:
    return SignalRecord(
        source_id=captured.source_id,
        capture_id=captured.capture_id,
        evidence_url=evidence_url or captured.evidence_url,
        text_sha256=captured.text_sha256,
        capture_timestamp_utc=captured.capture_timestamp_utc,
        extracted_timestamp_utc=datetime(2026, 5, 7, 10, 5, tzinfo=UTC),
        asset_symbol="BTC",
        direction=Direction.LONG,
        entry=Decimal("100"),
        stop=Decimal("90"),
        target=Decimal("110"),
    )


def test_abstract_method_required() -> None:
    missing_extract = type("MissingExtract", (ExtractionAdapter,), {})

    with pytest.raises(TypeError):
        missing_extract()


def test_envelope_invariants() -> None:
    captured = post()
    draft = record(captured)

    result = ExtractionResult(
        status=ExtractionStatus.DRAFT_PENDING_REVIEW,
        post=captured,
        record=draft,
    )
    assert result.record == draft

    with pytest.raises(ValidationError):
        ExtractionResult(status=ExtractionStatus.DRAFT_PENDING_REVIEW, post=captured)

    with pytest.raises(ValidationError):
        ExtractionResult(
            status=ExtractionStatus.DEFER_TO_HUMAN,
            post=captured,
            record=draft,
            reason="operator review required",
        )

    with pytest.raises(ValidationError):
        ExtractionResult(status=ExtractionStatus.DEFER_TO_HUMAN, post=captured)

    deferred = ExtractionResult(
        status=ExtractionStatus.DEFER_TO_HUMAN,
        post=captured,
        reason="missing target",
    )
    assert deferred.reason == "missing target"


def test_evidence_preserved() -> None:
    captured = post()

    with pytest.raises(ValidationError):
        ExtractionResult(
            status=ExtractionStatus.DRAFT_PENDING_REVIEW,
            post=captured,
            record=record(captured, evidence_url="https://t.me/other/1"),
        )

    result = ExtractionResult(
        status=ExtractionStatus.DRAFT_PENDING_REVIEW,
        post=captured,
        record=record(captured),
    )

    assert result.record is not None
    assert result.record.evidence_url == captured.evidence_url
    assert result.record.text_sha256 == captured.text_sha256
