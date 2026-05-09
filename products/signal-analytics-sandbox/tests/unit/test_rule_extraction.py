from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.capture.loader import CapturedPost, compute_text_sha256
from signal_sandbox.extraction.base import ExtractionStatus
from signal_sandbox.extraction.rule import RuleExtractionAdapter
from signal_sandbox.ledger.record import Direction


def post(raw_text: str) -> CapturedPost:
    return CapturedPost(
        capture_id="cap-001",
        source_id="pilot",
        evidence_url="https://t.me/pifagortrade/1",
        capture_timestamp_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        raw_text=raw_text,
        text_sha256=compute_text_sha256(raw_text),
    )


def test_match_and_defer() -> None:
    adapter = RuleExtractionAdapter(template="binance_spot_v1")
    matched_post = post("BTC long entry 100 target 110 stop 90")

    result = adapter.extract(matched_post)

    assert result.status == ExtractionStatus.DRAFT_PENDING_REVIEW
    assert result.record is not None
    assert result.record.asset_symbol == "BTC"
    assert result.record.direction == Direction.LONG
    assert result.record.entry == Decimal("100")
    assert result.record.stop == Decimal("90")
    assert result.record.target == Decimal("110")
    assert result.record.evidence_url == matched_post.evidence_url
    assert result.record.text_sha256 == matched_post.text_sha256
    assert result.record.extraction_metadata["adapter_id"] == ("rule/binance_spot_v1")

    deferred = adapter.extract(post("No structured setup here"))

    assert deferred.status == ExtractionStatus.DEFER_TO_HUMAN
    assert deferred.record is None
    assert deferred.reason == "no match for template binance_spot_v1"
